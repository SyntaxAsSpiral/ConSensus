---
name: local-inference
description: Use when calling local models on the mesh, loading or tuning an LM Studio JIT preset, or checking why llama.cpp or a CUDA/ROCm build does not see the GPU. Covers the gateway at http://100.89.32.9:1234/v1, reasoning dials, KV and prediction-stream presets, and the family-cookbook and esocortex callers.
compatibility: Daemonturgy mesh (nxiz/zrrh/adeck). Tailscale required. zrrh needs its GUI session for CUDA.
metadata:
  author: zk
  version: "2.5"
  category: inference
---

# local-inference

LM Studio on zrrh, through one OpenAI-compatible gateway. This skill is the model, the JIT preset, and whether the binary can see the GPU. Dials and source paths are in [references/reference.md](references/reference.md). The portable GPU check is in [references/gpu.md](references/gpu.md). Driving a coding CLI is `cli-coding`.

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

All three are VLMs on the zrrh 4090, served at **100K** context. Do not raise it unless asked. Gemma does not fit entirely on the GPU and is slower for it. Leave its quant. Operator rates `meta/muse-glimmer` good. Use so far is light.

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

`lms ls` is the inventory.

## JIT

The preset is the load contract: context, KV quant, KV offload, and how many prediction streams (`parallel`) that one loaded instance serves. The numbers are the table in the reference.

- Chat picks the preset up from the first completion. `POST /api/v1/models/load` skips it.
- Wait until `lms ps` shows one instance, then run up to that row's streams. Concurrent first requests race and load the model more than once.
- `unloadPreviousJITModelOnLoad` is on. zrrh is one 24 GB GPU, so one large model at a time.
- 100K is the context this setup uses. Card maxima are larger.
- Idle TTL is 1 h. A model missing after that is eviction, not a missing install.
- Embeddings are the exception. A bare `/v1/embeddings` uses the GGUF `n_ctx` and can OOM the 4090. Pin first:

```bash
curl -s http://100.89.32.9:1234/api/v1/models/load -H 'Content-Type: application/json' \
  -d '{"model":"text-embedding-qwen3-embedding-8b","context_length":8192}'
```

A dead GUI session on zrrh is a 502 or 503, not a wake failure.

## GPU

The chat server is LM Studio's own llama.cpp. `nixpkgs.config.cudaSupport` and `pkgs.llama-cpp` do not change that binary. When a Nix-built llama.cpp or PyTorch misses the GPU, walk kernel driver, userspace, then the application build, in [references/gpu.md](references/gpu.md), before changing a quant or a context length.

## Gone

vLLM on `zrrh:8000`, a direct llama-server, the forge probe lab, and the old lmlink router. This gateway is LM Studio, LM Link, and the wake proxy.

## Callers

family-cookbook (OCR, repair, babette) and esocortex use this URL. Their schemas, the GPU lock, and the flake paths are in the reference.
