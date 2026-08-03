# ClearFrame Studio — Automated AI Video Creation Suite
### System Architecture & Data Flow (v1.0)

**Design goals:** zero-token free local operation, rights-cleared generation path,
provider-agnostic adapter layer, backend-ready module boundaries.

---

## 1. Operating Modes

| Mode | Cost | What runs |
|------|------|-----------|
| `LOCAL_FREE` (default) | $0 / 0 tokens / keyless | Real generation on the free stack: AI scene stills from Pollinations.ai (FLUX, keyless) through the same-origin `/img` proxy in `server.py`, animated with Ken Burns motion; on-device OS narration (en/hi/mr); WebAudio-synthesized music; `.webm` export via MediaRecorder. Offline, scenes fall back to the procedural illustrator. |
| `ENTERPRISE_API` | Provider-billed | Same pipeline, but the Generation Gateway swaps free resolvers for authenticated fetch adapters (ElevenLabs / Runway / Mubert enterprise tiers). Flip one config flag. |

**Free-tier caveat (flagged deliberately):** Pollinations is a free public API —
no indemnification, no SLA, and burst requests get rate-limited (the client
paces fetches ~1.5s apart with one retry). The enterprise adapters exist for
when those guarantees matter.

The front-end is **identical** in both modes — the adapter layer is the only seam.

---

## 2. End-to-End Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER INPUT: RAW TEXT SCRIPT                      │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │  1. SCRIPT PARSER +          │
                    │     LANGUAGE ENGINE          │
                    │  • Auto-detect EN / हिंदी /  │
                    │    मराठी (Devanagari ratio + │
                    │    marker-word scoring), or  │
                    │    manual override           │
                    │  • Sentence/paragraph split  │
                    │    (danda । aware)           │
                    │  • Duration estimate         │
                    │    (words ÷ per-lang wps)    │
                    │  • Visual keyword extraction │
                    │    (Latin + Devanagari)      │
                    └──────────────┬───────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │  2. PROMPT SANITIZER (IP     │
                    │     FIREWALL — runs BEFORE   │
                    │     any prompt leaves the    │
                    │     client)                  │
                    │  • Blocklist scan: public    │
                    │    figures, trademarks,      │
                    │    studio IP, artist names   │
                    │  • Appends restrictive       │
                    │    negative/safety tokens    │
                    │  • Emits per-scene audit log │
                    └──────────────┬───────────────┘
                                   ▼
        ┌──────────────────────────────────────────────────────┐
        │  3. GENERATION GATEWAY  (Promise.allSettled fan-out) │
        │     One job envelope per scene per modality;         │
        │     scenes run in PARALLEL, modalities in PARALLEL.  │
        └───────┬──────────────────┬──────────────────┬────────┘
                ▼                  ▼                  ▼
     ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
     │ VIDEO ADAPTER    │ │ VOICE ADAPTER    │ │ MUSIC ADAPTER    │
     │ Runway Gen-3     │ │ ElevenLabs       │ │ Mubert / Suno    │
     │ Enterprise API   │ │ Enterprise TTS   │ │ Commercial API   │
     │ (indemnified)    │ │ (no-retrain SLA) │ │ (cleared output) │
     │ ── FREE MODE:    │ │ ── FREE MODE:    │ │ ── FREE MODE:    │
     │ Pollinations.ai  │ │ on-device Web    │ │ WebAudio         │
     │ FLUX stills via  │ │ Speech API       │ │ procedural       │
     │ same-origin /img │ │ (hi-IN/mr-IN/en) │ │ synthesis        │
     │ proxy (paced +   │ │                  │ │ (output 100%     │
     │ retried) + Ken   │ │                  │ │  owned)          │
     │ Burns motion;    │ │                  │ │                  │
     │ procedural scene │ │                  │ │                  │
     │ illustrator      │ │                  │ │                  │
     │ offline fallback │ │                  │ │                  │
     └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
              │    retry w/ backoff, per-job status      │
              └──────────────────┬──────────────────────┘
                                 ▼
                    ┌──────────────────────────────┐
                    │  4. ASSET REGISTRY           │
                    │  • assetId → blob/URL        │
                    │  • SHA-256 content hash      │
                    │    (crypto.subtle)           │
                    │  • provider + license ref    │
                    │  • sanitizer audit trail     │
                    └──────────────┬───────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │  5. TIMELINE COMPOSER        │
                    │  Track A: Video clips        │
                    │  Track B: Voiceover (TTS)    │
                    │  Track C: Background music   │
                    │  • Scene-locked sync offsets │
                    │  • Crossfade/duck metadata   │
                    └──────────────┬───────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │  6. SECURE MIX & MUX         │
                    │  (backend target: ffmpeg/    │
                    │   WebCodecs worker)          │
                    │  • Audio duck under VO       │
                    │  • C2PA-style provenance     │
                    │    manifest embedded         │
                    │  • Visible + metadata        │
                    │    watermark ("AI Generated")│
                    └──────────────┬───────────────┘
                                   ▼
        ┌──────────────────────────────────────────────────────┐
        │  7. COMPLIANCE OUTPUTS (always generated)            │
        │  • license-manifest.json  (asset → license mapping)  │
        │  • provenance hashes per asset + final container     │
        │  • sanitizer audit log                               │
        └──────────────────────────────────────────────────────┘
```

---

## 3. Parallel Request Handling

- The Gateway builds `scenes.length × 2 + 1` job envelopes (video + VO per scene,
  one music bed per project) and dispatches with `Promise.allSettled` — a single
  failed clip never aborts the batch.
- Each job carries: `jobId`, `sceneId`, `sanitizedPrompt`, `providerConfig`,
  `attempt`. Failed jobs retry with exponential backoff (max 3), then surface as
  a per-clip error chip in the timeline rather than a global failure.
- In `ENTERPRISE_API` mode, adapters respect provider rate limits with a simple
  token-bucket queue (`maxConcurrent` per provider in `PROVIDERS` config).

## 3a. Multilingual Pipeline (English · Hindi · Marathi)

- **Detection:** Devanagari codepoint ratio separates English from Indic text;
  Hindi vs Marathi is disambiguated by high-frequency marker words
  (है/और → Hindi, आहे/आणि → Marathi). Per-scene, so mixed-language scripts work.
- **Voiceover:** each VO job carries `lang` and a routed TTS model
  (`PROVIDERS.voice.modelByLang`): `eleven_multilingual_v2` for EN/HI,
  `eleven_v3` for MR — all under the same enterprise license umbrella.
- **Video prompts:** Devanagari keywords are extracted natively; the backend
  LLM pass translates them to English before hitting the video API.
- **Sanitizer:** blocklists include Devanagari-script public figures and
  trademarks so Indic prompts get the same IP firewall as English ones.
- **Manifest:** every voice asset records `language` and `ttsModel`.

## 4. Legal Risk Minimization — Layer Map

| Layer | Control |
|-------|---------|
| Input | Prompt Sanitizer blocklists (public figures, trademarks, studio IP, "in the style of <artist>") + appended restrictive negative tokens |
| Provider selection | Only enterprise tiers with (a) commercial output rights, (b) no-training-on-inputs clauses, (c) indemnification (Runway Enterprise, ElevenLabs Enterprise, Mubert Business) |
| Output | SHA-256 provenance hash per asset; C2PA-style manifest; visible AI-content watermark |
| Records | Downloadable license manifest mapping every `assetId` → provider license URL + terms snapshot date |

## 5. Backend Integration Points

Every module is a self-contained object with a stable interface. To go live:
1. Point `CONFIG.mode = 'ENTERPRISE_API'` and fill `PROVIDERS.*.apiKey` **server-side**
   (move `GenerationGateway` behind your API; the front-end already talks to it
   through a single `dispatch(job)` function).
2. Replace `MixEngine.renderLocal()` with an ffmpeg/WebCodecs render service.
3. Persist `AssetRegistry` + manifests to your store of record.
