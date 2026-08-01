---
title: ClearFrame Studio — free multilingual AI video suite
type: project
tags: [video, multilingual, pollinations, prototype]
created: 2026-08-01
updated: 2026-08-01
sources: [~/files/clearframe-studio/HANDOFF.md]
---

Single-file web app at `~/files/clearframe-studio` (`index.html`, Tailwind CDN, dark studio
UI) that turns a raw script in English, Hindi or Marathi into a narrated video — with **no
API keys and no tokens**. Language auto-detect uses Devanagari ratio plus marker words
(है/और → hi, आहे/आणि → mr); sentence splitting is danda-aware.

Generation stack, all free: Pollinations.ai FLUX stills per scene, Ken Burns motion over
the stills, on-device Web Speech narration routed per language (en-US/hi-IN/mr-IN),
procedural WebAudio music, `.webm` export via MediaRecorder. A keyword-driven procedural
illustrator is the offline fallback. Compliance side: prompt sanitiser with English and
Devanagari blocklists for public figures and trademarks, downloadable license manifest
JSON, SHA-256 provenance hashing.

**Two hard-won facts.** Pollinations must be called through the same-origin `/img` proxy in
`server.py` — direct CORS requests get 403. And OS TTS cannot be captured by MediaRecorder,
so exported files carry the music track but not the narration.

The honest verdict (2026-07-10): the output does not feel like true generative motion
video, and no free keyless API provides that. Rather than fake it, the app grew a 🎬 **Shot
List** export — ready-to-paste motion-cued, character-consistent prompts per scene and shot
for the free web tiers of Kling/Hailuo/Luma/Pika/Runway, plus dialog blocks for lip-sync
tools.

That ceiling is what produced [[kalpana]]: ClearFrame stays as the demo and as the parser
seed (its `ScriptParser` dialog/description/danda logic), while the real architecture was
redesigned from scratch.
