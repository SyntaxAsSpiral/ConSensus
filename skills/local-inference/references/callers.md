# Callers

## family-cookbook — `/mnt/echo/family-cookbook`

- `ocr/sidecar.py` — 4 page workers, sqlite queue, per-tile transcribe then page assembly. Default base URL was `http://adeck:1234/v1`. Point it at `http://100.89.32.9:1234/v1`. The unit currently overrides to OpenRouter `google/gemini-3-flash-preview`. Strict schema `page_ocr`. Vision preflight is `GET /api/v0/models` and `type: "vlm"`. `finish_reason: "length"` is a hard fail. OpenRouter fallback adds `reasoning: {"effort": "low"}` and `provider: {"sort": "throughput"}`.
- `ocr/repair.py` — local `google/gemma-4-31b`, `temperature: 0`, `stream: true`, `reasoning_effort: "none"`. Schema `ocr_character_repairs`. Every `before` span must match the draft. It proposes. The operator applies.
- `babette/server.py` — chat uses `settings.base_url`, override `OPENAI_BASE_URL`, model `COOKBOOK_MODEL`. Speech is [tts.md](tts.md).
- Unit: `cookbook-ocr.service` on adeck (`Restart=on-failure`, `KillMode=mixed`, `TimeoutStopSec=120`).

## esocortex — `/mnt/echo/esocortex`

`src/llm.py`. `ESOCORTEX_LLM_BASE` still defaults to `http://adeck:1234/v1`. Use the Tailscale IP.

- `complete()` retries `length` once by doubling `max_tokens` (4096 → 8192) unless the cap was omitted. That retry is the behavior to retire, not to copy. Harvest JSON from `content` or `reasoning_content`. Include HTTP error bodies. `exclusive=False` for in-flight workers after the lane holds `LOCK_EX`.
- `ensure_loaded(model, context_length)` is for embeddings only.
- `embed()` is `/v1/embeddings`, sorted by `index`.
- `src/augment.py` — schema `esocortex_augment` (translation, system, mode, keys).
- GPU lock `_gpu_lock` at `/tmp/esocortex-zrrh-gpu.lock`. Chat takes `LOCK_EX`. Embeds take `LOCK_SH`. One lock around the lane. Inner calls stay unlocked or the flock serializes them.
