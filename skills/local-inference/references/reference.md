# local-inference reference

Verified against the live mesh on 2026-09-18. The operating rules are in `SKILL.md`. This file is the dial detail, the callers, and the source paths.

## Wake proxy

Source: `nix-os/modules/home/daemonturgy/lmstudio/adeck/inference-wake.py`, declared by `default.nix` beside it.

- Binds `0.0.0.0:1234`, upstream `http://127.0.0.1:1235` (`lms daemon up`).
- Gated (these POSTs, plus any WebSocket): `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/responses`, `/api/v0/chat/completions`, `/api/v0/completions`, `/api/v0/embeddings`, `/api/v1/chat`, `/api/v1/models/load`. A wake check runs before each downstream frame on a WebSocket.
- Ready means zrrh is TCP-reachable at `192.168.0.110:22` and `lms link status --json` shows peer `zrrh` with `status: "connected"`. Otherwise WoL (`60cf8461d800` → `192.168.0.255:9`) every 3 s for 120 s, then 503 `zrrh did not reconnect to LM Link within 120 seconds.` A 2 s cache covers a burst.
- Embeddings are gated too. `mxbai-embed-large-v1` lives on adeck and still pays the wake cost if zrrh is asleep.
- Timeouts: connect 10 s, read 600 s, no total. `auto_decompress: false`. Upstream failure → 502 `LM Studio upstream unavailable.`
- `GET /v1/models` and `GET /api/v0/models` pass through without a wake.

Diagnostics: `journalctl --user -u inference-wake -u llmster` on adeck. Load failures land in `~/.lmstudio/server-logs/YYYY-MM/*.log` on the host running the model (`LMSTUDIO_STARTUP_ERROR`, `gguf_init_from_reader`).

## API

`POST /v1/chat/completions`. Streaming is SSE: `delta.content` and `delta.reasoning_content`, then `data: [DONE]`.

Strict schema:

```json
{"response_format":{"type":"json_schema","json_schema":{
  "name":"probe","strict":true,
  "schema":{"type":"object","properties":{"n":{"type":"integer"}},
            "required":["n"],"additionalProperties":false}}}}
```

In production: cookbook OCR `page_ocr`, cookbook repair `ocr_character_repairs`, esocortex `esocortex_augment`. Prefer `content` when it holds a JSON object; otherwise take `reasoning_content`. On HTTP 4xx/5xx log `response.text`. `raise_for_status()` hides the gateway's reason.

`reasoning_effort` is a template label, not a token cap. Re-checked on `qwen/qwen3.8-27b` through the gateway:

| Request | Result |
|---|---|
| omitted, or `"xhigh"` | Thinks. A small `max_tokens` is consumed by reasoning. `content` empty. |
| `"none"` | `reasoning_tokens: 0`. Answer in `content`. |
| `"off"` | 400. Not in the enum. |
| `thinking_budget: 0` | No effect on this qwen. |

Native `POST /api/v1/chat` uses `reasoning` = `off|low|medium|high|on`. Do not send `reasoning: {"effort": ...}` to `/v1/chat/completions`. `/v1/responses` does take that object. The cookbook's OpenRouter fallback uses the object against OpenRouter, not against this gateway.

When the jinja never reads `reasoning_effort`, sending it is a no-op. The hub `model.yaml` `customFields` → `setJinjaVariable` and the official prompting guide win over the gateway's enum.

Vision preflight: `GET /api/v0/models/{id}` → `type == "vlm"`. `GET /api/v1/models` → `capabilities.vision == true`. `architecture.input_modalities` is not on the live `/api/v0` payload. pi's `models.json` still says `input: ["text"]` for all three. Vision is the raw API.

## Model cards

100K is `defaultContextLength: 100000` (runtime 100096). Card maxima are larger and do not fit this KV/parallel setup.

**`qwen/qwen3.8-27b`** — Q4_K_M, ~17.7 GB, arch `qwen35`. Card context 262144. Official efforts: `xhigh` (default), `medium`, `low`. Official off-switch is `chat_template_kwargs.enable_thinking: false`; on this gateway use `reasoning_effort: "none"`. `preserve_thinking` defaults on. mmproj `mmproj-Qwen3.8-27B-BF16.gguf`. MTP head is inside the GGUF. Thinking sample: temp 1.0, top_p 0.95, top_k 20. Instruct: temp 0.7, top_p 0.8, presence_penalty 1.5. Hub `lmstudio-community/Qwen3.8-27B-GGUF`.

**`google/gemma-4-31b`** — Q4_K_M, ~19.9 GB, arch `gemma4`. Card context 262144. Thinking is `<|think|>` in the system turn. LMS v1 options are `off|on` only. Thoughts are `<|channel>thought`. On 31B, thinking-off still emits an empty thought channel. Strip prior thoughts from history. Sampling: temp 1.0, top_p 0.95, top_k 64. Hub `lmstudio-community/gemma-4-31B-it-GGUF`.

**`meta/muse-glimmer`** — 30B card (LMS `params_string: 28B` is the text decoder; ~1.8–2B vision encoder on top). Card context 131072. pi's display name "26b" is stale. There is no off switch. Send `chat_template_kwargs: {"reasoning_strength": "low"}`. `reasoning_effort` and `enable_thinking` are absent from the template. LMS v1 exposes only `on`. Sampling: temp 1.0, top_p 0.95, top_k 64. JSON, when constrained, belongs in `to=user` → `message.content`. Speculative decoding is a separate draft (Meta DFlash), not a baked MTP head. Hub `lmstudio-community/Muse-Glimmer-30B-GGUF`. Prompting: <https://ai.developer.meta.com/docs/muse-glimmer/prompting.md>.

## JIT

adeck `http-server-config.json`: context 100000, `jitModelTTL` 1 h, `unloadPreviousJITModelOnLoad`. Presets in `~/.lmstudio/config-presets/` (adeck's are flake-managed; zrrh's are GUI-managed). Per-model JIT files on zrrh: `~/.lmstudio/.internal/user-concrete-model-default-config/`. LMS writes a field only after it is changed, so an empty `operation.fields` does not mean the UI lacks the control.

| Model | KV | offload KV | parallel |
|---|---|---|---|
| `qwen/qwen3.8-27b` | q8_0 | true | 4 |
| `meta/muse-glimmer` | f16 | true | 2 |
| `google/gemma-4-31b` | flash + q4_0 | false | 2 |

Chat loads pick this table up on the first `/v1/chat/completions`. `POST /api/v1/models/load` with `context_length` skips it. Embeddings are the exception: qwen3-embedding-8b's own `n_ctx` is 40k and OOMs the 24 GB card. Pin `context_length: 8192`. `ensure_loaded` treats 400/409/500 "already loaded" as success.

Embedding ids: `text-embedding-qwen3-embedding-8b` (zrrh), `text-embedding-qwen3-embedding-4b` (nxiz), `text-embedding-nomic-embed-text-v1.5` (adeck/nxiz/zrrh), `text-embedding-mxbai-embed-large-v1` (adeck/nxiz).

Qwen3.8 MTP is inside the GGUF. The zrrh log shows `common_speculative_init_result: creating MTP draft context` and draft acceptance about 0.80–0.98. It is a load-time property, not a per-request parameter. Confirm with `grep -i "draft acceptance"` in that host's `server-logs`.

Stock llama.cpp, which LM Studio ships, rejects ggml types outside `[0, GGML_TYPE_COUNT)`. Ternary Bonsai 2 `PTQ1_0` (143) and `PQ2_0` (142) need the Prism fork. The 1-bit `Q1_0` Bonsai does load. A `Q2_0` from a `-gguf-dev` repo can load and emit garbage. Match `bonsai-2-` or `ternary-bonsai-2`. The substring `bonsai-2` also matches `bonsai-27b`.

## Callers

### pi

`~/.pi/agent/models.json`, provider `local`. The file may still say `http://adeck:1234/v1`. Use `http://100.89.32.9:1234/v1`. `api` is `openai-completions`, `apiKey` is `lms`, `contextWindow` 100000. Default provider is `openrouter` / `stealth/ox-alpha`. Local is opt-in:

```bash
pi --provider local --model qwen/qwen3.8-27b
```

### family-cookbook — `/mnt/echo/family-cookbook`

- `ocr/sidecar.py` — 4 page workers, sqlite queue, per-tile transcribe then page assembly. Default base URL was `http://adeck:1234/v1`. Point it at `http://100.89.32.9:1234/v1`. The unit currently overrides to OpenRouter `google/gemini-3-flash-preview`. Strict schema `page_ocr`. Vision preflight is `GET /api/v0/models` and `type: "vlm"`. `finish_reason: "length"` is a hard fail. OpenRouter fallback adds `reasoning: {"effort": "low"}` and `provider: {"sort": "throughput"}`.
- `ocr/repair.py` — local `google/gemma-4-31b`, `temperature: 0`, `stream: true`, `reasoning_effort: "none"`. Schema `ocr_character_repairs`. Every `before` span must match the draft. It proposes. The operator applies.
- `babette/server.py` — `settings.base_url`, override `OPENAI_BASE_URL`, model `COOKBOOK_MODEL`.
- Unit: `cookbook-ocr.service` on adeck (`Restart=on-failure`, `KillMode=mixed`, `TimeoutStopSec=120`).

### esocortex — `/mnt/echo/esocortex`

`src/llm.py`. `ESOCORTEX_LLM_BASE` still defaults to `http://adeck:1234/v1`. Use the Tailscale IP.

- `complete()` retries `length` once by doubling `max_tokens` (4096 → 8192) unless the cap was omitted. That retry is the behavior to retire, not to copy. Harvest JSON from `content` or `reasoning_content`. Include HTTP error bodies. `exclusive=False` for in-flight workers after the lane holds `LOCK_EX`.
- `ensure_loaded(model, context_length)` is for embeddings only.
- `embed()` is `/v1/embeddings`, sorted by `index`.
- `src/augment.py` — schema `esocortex_augment` (translation, system, mode, keys).
- GPU lock `_gpu_lock` at `/tmp/esocortex-zrrh-gpu.lock`. Chat takes `LOCK_EX`. Embeds take `LOCK_SH`. One lock around the lane. Inner calls stay unlocked or the flock serializes them.

## Paths

- Flake: `modules/home/daemonturgy/lmstudio/adeck/` — `default.nix`, `inference-wake.py`, `settings.json`, `http-server-config.json`, `user-concrete-model-default-config/`, `config-presets/`.
- Structured output: <https://lmstudio.ai/docs/developer/openai-compat/structured-output>
- Chat completions: <https://lmstudio.ai/docs/developer/openai-compat/chat-completions>
- Load: <https://lmstudio.ai/docs/developer/rest/load>
- TTL: <https://lmstudio.ai/docs/developer/core/ttl-and-auto-evict>
- SDK `reasoningBudget` (experimental, not on `model.complete()`, not in the published chat-completions docs): `lmstudio.js` `LLMPredictionConfig.ts`
- Muse prompting: <https://ai.developer.meta.com/docs/muse-glimmer/prompting.md>
