---
title: Voicebox — local AI voice studio (dev checkout)
type: project
tags: [voice, tts, stt, mlx, local, tauri]
created: 2026-07-04
updated: 2026-07-04
sources: [~/files/voicebox, https://github.com/jamiepine/voicebox]
---

Dev checkout of **[jamiepine/voicebox](https://github.com/jamiepine/voicebox)** (MIT,
v0.5.0), cloned and installed 2026-07-03/04. A local-first open-source alternative to
ElevenLabs + WisprFlow: zero-shot voice cloning, 7 TTS engines, Whisper STT/dictation,
and a built-in MCP server so agents (e.g. Claude Code — [[claude-anthropic]]) can speak
via `voicebox.speak`. Stack: Tauri (Rust) desktop app + React front end + FastAPI
(Python) backend on port 17493, MLX inference on Apple Silicon.

**Working state (as of 2026-07-04):** fully installed and verified end-to-end — a voice
profile "TEJAS JADHAV" exists and generated cloned speech successfully with Qwen3-TTS
0.6B (~2.3 tokens/s).

## How to run

`cd ~/files/voicebox && just dev` (backend + desktop app). Toolchain was installed
user-locally (no Homebrew on this machine): bun (`~/.bun`), just + uv (`~/.local/bin`),
rustup (`~/.cargo`), Python 3.12 via uv → venv at `backend/venv`.

## Constraints & quirks (hard-won)

- **8 GB RAM machine → always use the 0.6B model.** Qwen3-TTS 1.7B (4.3 GB) swap-thrashes
  at ~37 s/token (≈45 min per sentence); 0.6B runs ~85× faster. LuxTTS is a fast
  English-only alternative. Select the model in the app's generate screen.
- `just setup` misses two packages: `pip install --no-deps mlx-audio==0.4.1` and
  `pip install --no-deps mlx-lm==0.31.1`. A bare `pip install mlx-lm` upgrades
  transformers to 5.x and breaks qwen-tts (pins `transformers==4.57.3`).
- `tauri/src-tauri/build.rs` is **patched locally**: without full Xcode (only Command
  Line Tools installed), `actool` is missing, so the patch writes placeholder
  `Assets.car`/`partial.plist` instead of panicking. Don't revert unless Xcode is installed.
- REST `/generate` selects models via `engine` + `model_size` ("0.6B"/"1.7B") — a
  `model_name` field is silently ignored and defaults to 1.7B.
- uvicorn `--reload` hangs on shutdown while the app holds SSE connections; recover by
  killing the `spawn_main` worker child and `touch backend/main.py`.
- Models cache to `~/.cache/huggingface/hub` (Qwen3-TTS 0.6B ≈1.5 GB, 1.7B ≈4.3 GB,
  Whisper Base ≈281 MB downloaded).

Related: [[jarvis]] is the other local voice project (assistant with Claude brain);
Voicebox could give it — or any MCP-aware agent — a cloned local voice instead of a
cloud TTS. Part of [[files-repo]].
