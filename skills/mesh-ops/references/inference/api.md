# API

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

Vision preflight: `GET /api/v0/models/{id}` → `type == "vlm"`. `GET /api/v1/models` → `capabilities.vision == true`. `architecture.input_modalities` is not on the live `/api/v0` payload. Vision is the raw API. A client that still advertises text-only input is stale.
