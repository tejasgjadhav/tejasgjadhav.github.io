# Handoff — ClearFrame Studio (AI Video Creation Suite)
_Updated: 2026-07-10 by Claude Code — HD/FLUX quality fix verified; app ready to demo_

## Status note (2026-07-10)
Latest: shot-list bridge shipped. User now asking strategy question — what
it takes to build a Kling/Hailuo/Luma-class product (answered in chat; no
code change). App itself is stable/demo-ready. User is now evaluating a
strategy proposal (orchestration platform over swappable video models,
"AI Director" concept, Indic/finance niche) — assessment given in chat;
possible future direction: evolve ClearFrame into that orchestration
layer (model router, character memory, storyboard stage).
BLUEPRINT.md written (KALPANA ENGINE v1 — full AI film studio design).
DESIGN-REVIEW-V2.md done (panel critique + V2: animatic-first, derivation
graph, absorption doctrine, Critic, CineBench, data engine). V2 is FROZEN
as target architecture per user. Now writing ENGINEERING-PLAN.md — the
implementation master plan (dependency graph, milestones, repo layout,
interfaces, tech choices, risks, research-vs-engineering, solo build
order, definitions of done).

User's verdict: output doesn't feel natural/real — expectation is true
generative motion video (Sora/Veo/Runway class), which no free keyless API
provides. Candid conversation held about the free-tier ceiling. User approved building the "shot list + prompts" export: a 🎬 Shot List
button that downloads ready-to-paste, motion-cued, character-consistent
prompts (per scene per shot) for Kling/Hailuo/Luma/Pika/Runway free web
tiers, plus dialog blocks for lip-sync tools. DONE & verified 2026-07-10:
ShotList module + 🎬 header button (auto-analyzes, downloads
clearframe-shot-list.txt; verified 3 scenes/6 prompts/3 dialog blocks).

## Goal
User wants a **free, no-token, no-API-key** web app that turns a raw text script
(English / Hindi / Marathi) into a real-feeling AI video — matching visuals with
characters and scenes as described in the script, narration, background music,
and a downloadable video file — with legal/IP risk minimized (sanitization,
license manifest, provenance hashing). Stated ambition: "better than Runway,
world's #1 free AI video app." Enterprise adapters (Runway/ElevenLabs/Mubert)
exist as documented placeholders for a future paid backend.

## Current state
- **Done (all verified in browser):**
  - `index.html` — entire single-file app (Tailwind CDN, dark studio UI):
    script workspace with EN/HI/MR samples, language auto-detect
    (Devanagari ratio + marker words: है/और→hi, आहे/आणि→mr), danda-aware
    sentence split, scene breakdown with visual-keyword extraction,
    generation control panel (voice, pace, mood, style, aspect),
    multi-track timeline (video thumbs + VO/music waveforms),
    compliance dashboard, downloadable license manifest JSON,
    SHA-256 provenance hashing, prompt sanitizer (EN + Devanagari
    blocklists for public figures/trademarks + negative-token suffix).
  - Real generation stack (free): Pollinations.ai FLUX stills per scene
    via same-origin `/img` proxy in `server.py` (direct CORS requests get
    403 — proxy is REQUIRED); Ken Burns motion over stills; on-device
    Web Speech narration routed per language (en-US/hi-IN/mr-IN);
    WebAudio procedural music; `.webm` export via MediaRecorder
    (canvas + music track; OS TTS can't be captured — known limitation).
  - Procedural scene illustrator fallback (offline): keyword-driven flat
    illustration (dawn sun, city skyline, drones, person at desk, notes).
  - One-click Generate (auto-analyzes script if not parsed).
  - `ARCHITECTURE.md` — flowchart + modes + multilingual section.
- **Done (2nd wave, verified):** multi-shot cinematography (2 shots/scene
  wide+close via `SceneVisuals.SHOTS`, crossfade cuts, alternate Ken Burns),
  CharacterEngine consistent-protagonist prompts, film-look pass (vignette,
  grain, letterbox). Cache is `sceneId → Image[]`.
- **Done (3rd wave, verified 2026-07-09):** screenplay semantics — parser
  splits scenes into `description` (action lines → image prompts only) and
  `dialog` (`NAME: line` → the ONLY narration/subtitles); silent scenes =
  music only (dim VO slot); per-speaker OS voice + stable pitch signature;
  subtitles `SPEAKER: line` timed by word share; samples rewritten as
  screenplays (MAYA/ARIA, माया/आरव); image prompts use description only.
  Verified: Hindi sample → 2 scenes, 5 assets (VO only for dialog), 4 AI
  shots export-safe, subtitle frame rendered with speaker name.
- **In progress (2026-07-10):** user reports audio is bad ("worst sound
  plus video"). Legit flaws found on self-review: (1) music is a static
  3-oscillator drone — no rhythm/progression, sounds like a test tone;
  (2) scene changes call speechSynthesis.cancel() mid-sentence → dialog
  gets chopped when TTS runs longer than the estimated scene duration;
  (3) no music ducking under dialog; (4) en voice picked arbitrarily.
  FIXED & verified 2026-07-10: generative music engine (chord progression,
  bass, melody, hats, compressor, lookahead scheduler), event-driven scene
  advance (never cuts dialog mid-sentence, 12s guard), music ducking under
  speech, novelty-voice blacklist (headless env cast "Bad News"!) +
  preferred natural en voices. Remaining ceiling: OS TTS quality (Lekha).
- **Previously fixed:** poor image quality / "non-real"
  output. Suspected causes: (a) Pollinations now defaults to the cheap
  `sana` model (seen in curl EXIF metadata) — need explicit `model=flux`;
  (b) images requested at only 640×360 then upscaled; (c) user may have
  hit Play before AI shots finished → procedural cartoon fallback played.
  FIXED & verified: images now 1280×720 (720×1280 / 1024² by aspect) with
  explicit `model=flux` (server.py whitelist gained model/enhance params);
  canvas render res bumped to match; Play now warns when AI shots aren't
  loaded yet so the procedural fallback can't masquerade as AI output.
  HD flux render through proxy verified photoreal (~9s/image).
- **Not started:** true motion AI video (requires paid APIs — flagged to
  user repeatedly); enterprise backend proxy; voice capture into export.

## Next steps
1. In `index.html`: add `CharacterEngine` (regex person-words EN+Devanagari
   → fixed descriptor string), set `SceneVisuals.character` in the
   btnGenerate handler before visual loads.
2. Rework `SceneVisuals`: `SHOTS = ['cinematic establishing wide shot',
   'intimate close-up shot, shallow depth of field']`; load both shots per
   scene sequentially through the existing paced `_queue` (1.5s spacing,
   proxy → direct → retry chain per shot, seed = hash-derived + shotIdx*7);
   cache arrays progressively.
3. Rework `RenderEngine.drawFrame` image branch: pick shot by
   `local / (scene.duration/shots.length)`, crossfade ~0.5s before each cut,
   per-shot Ken Burns; then vignette (radial), ~150 grain specks, letterbox
   bars; keep subtitle band, scene chip, progress bar, watermark.
4. Update timeline thumbnail code in btnGenerate to use `imgs[0].src`, and
   export-safety filter to `cached.filter(i => i._exportSafe)`.
5. Verify in preview: generate EN sample → expect 6 proxy image requests,
   cache size 3 (arrays of 2), export recorder `recording`, screenshot.

## Key files
| File | Why it matters |
|------|----------------|
| `/Users/sayali/files/clearframe-studio/index.html` | Entire app — all modules (CONFIG, PROVIDERS, FREE_PROVIDERS, LanguageEngine, ScriptParser, PromptSanitizer, Provenance, GenerationGateway, AssetRegistry, LicenseManifest, SceneVisuals, Narrator, MusicEngine, RenderEngine, UI layer) |
| `/Users/sayali/files/clearframe-studio/server.py` | Static server + `/img` same-origin Pollinations proxy — REQUIRED for AI images + untainted export |
| `/Users/sayali/files/clearframe-studio/ARCHITECTURE.md` | System design doc, kept in sync with code |
| `/Users/sayali/files/.claude/launch.json` | `clearframe-studio` entry runs `python3 clearframe-studio/server.py`, port 3462 |

## Decisions & gotchas
- **Pollinations 403s ALL cross-origin browser requests** (fetch or
  `img.crossOrigin`) from unregistered origins, but plain `<img>` embeds
  and server-side HTTP work. Hence `server.py` proxy. Don't retry CORS.
- **Canvas taint is permanent** — direct-embed fallback images taint the
  canvas; export clones a fresh canvas element and skips non-`_exportSafe`
  images (falls back to procedural illustrator for those scenes).
- Free anonymous tier **rate-limits bursts** → `SceneVisuals._queue` paces
  requests 1.5s apart + one 6s-delayed retry. Keep pacing when adding shots.
- **RAF doesn't fire in the headless preview tab** (0×0 viewport) — playback
  appears frozen there; test rendering by calling
  `RenderEngine.drawFrame(...)` directly, or use the user's real Chrome via
  claude-in-chrome MCP (tab was 1008457682).
- User rejected the framing that TTS/static-Ken-Burns output = "video";
  requirement is scene/character depiction with real feel. Be honest that
  Runway-class motion needs paid APIs (user's machine: 8GB RAM, can't run
  local video models).
- Manifest maps free-mode assets to FREE_PROVIDERS honestly (Pollinations:
  commercial-use-per-terms, NO indemnification; music: WebAudio, 100% owned).
- Header claim "FREE MODE · 0 TOKENS · KEYLESS" is accurate — keep it that way.

## How to resume
Read `index.html` (focus: SceneVisuals, RenderEngine.drawFrame, the
btnGenerate handler) and `server.py`, then continue with step 1 above.
Run with `python3 clearframe-studio/server.py` (or the `clearframe-studio`
launch.json config) and open `http://localhost:3462`. Test flow: click
"Sample EN" → "⚡ GENERATE AI VIDEO" → wait for "AI scene visuals rendering…"
to finish → "▶ Play Video" → "⬇ Export .webm".
