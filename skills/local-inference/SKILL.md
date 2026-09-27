---
name: local-inference
description: Use when calling local models on the mesh — the wake-gated gateway at http://100.89.32.9:1234/v1, LM Link peers, JIT load versus explicit embedding load, reasoning_effort, structured output, or the pi, family-cookbook, and esocortex callers.
compatibility: Daemonturgy mesh (nxiz/zrrh/adeck). Tailscale required. zrrh needs its GUI session for CUDA.
metadata:
  author: zk
  version: "2.1"
  category: inference
---

# local-inference

One OpenAI-compatible gateway. Dials, consumer wiring, and source paths are in [references/reference.md](references/reference.md).

## URL

`http://100.89.32.9:1234/v1`

On adeck, `http://127.0.0.1:1234/v1` also works. From adeck, SSH by Tailscale IP. Hostnames do not resolve on that box.

`inference-wake` listens on `0.0.0.0:1234` and proxies to llmster at `127.0.0.1:1235`. An inference POST or WebSocket wakes zrrh and waits until it is connected to LM Link (120 s, then HTTP 503). `GET /v1/models` does not wake anything.

## Call

```bash
curl -s http://100.89.32.9:1234/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen/qwen3.8-27b","messages":[{"role":"user","content":"Reply with exactly: PONG"}],"reasoning_effort":"none"}'
```

- `reasoning_effort` on `/v1/chat/completions`: `none | minimal | low | medium | high | xhigh`. `"off"` is a 400. Cheap work sends `"none"`.
- Do not set a small `max_tokens` on a thinking model. The cap is eaten by reasoning and `content` comes back empty. Omit it, or set it in the thousands. Do not retry by doubling it. esocortex `complete()` still does that once (4096 → 8192). Do not copy that.
- Structured output: `response_format.type` `json_schema`, `strict: true`, `additionalProperties: false`, and `required` on every object. Read both `content` and `reasoning_content`. Empty `content` means the budget went to thinking.
- A schema miss or empty content is a call-shape problem until the hub `model.yaml` and that model's prompting guide have been checked.

Retry HTTP 408, 429, 502, 503, 504, and bodies that contain `LM Link connection closed`.

## Models

pi's `local` provider. All three are VLMs on the zrrh 4090, served at **100K** context. That is the fit. Do not raise it unless asked.

| Model | Thinking |
|---|---|
| `qwen/qwen3.8-27b` | On by default. `reasoning_effort: "none"` turns it off. |
| `google/gemma-4-31b` | On by default. Gateway options are `off` or `on`. Thinking-off still emits an empty thought channel. |
| `meta/muse-glimmer` | Always on (`to=self`, then `to=user`). The dial is `chat_template_kwargs.reasoning_strength` (`xhigh`, `high`, `medium`, `low`; default `high`). `reasoning_effort` does nothing. CoT is thousands of tokens. |

```bash
ssh zk@100.89.32.9 lms ps            # loaded: context, parallel, device, TTL
ssh zk@100.89.32.9 lms ls            # union fleet
ssh zk@100.89.32.9 lms link status   # peers
```

`lms ls` is the inventory. A model missing after an idle hour is the 1 h JIT TTL, not a missing install.

## Load

Chat: do not call `POST /api/v1/models/load`. That bypasses the JIT preset (KV quant, parallel, context). Send one completion, wait until `lms ps` shows a single instance, then fan out up to that instance's `parallel`. Concurrent first requests race each other and load the model more than once.

Embeddings: a bare `/v1/embeddings` uses the GGUF `n_ctx` and can OOM the 4090. Pin first:

```bash
curl -s http://100.89.32.9:1234/api/v1/models/load -H 'Content-Type: application/json' \
  -d '{"model":"text-embedding-qwen3-embedding-8b","context_length":8192}'
```

zrrh is one 24 GB GPU. One large model at a time. A dead GUI session is a 502 or 503, not a wake failure.

## Gone

vLLM on `zrrh:8000`, a direct llama-server, the forge probe lab, and the old lmlink router. This gateway is LM Studio, LM Link, and the wake proxy.

## Callers

pi, family-cookbook (OCR, repair, babette), and esocortex all use this URL. Their schemas, the GPU lock, and the flake paths are in the reference.
