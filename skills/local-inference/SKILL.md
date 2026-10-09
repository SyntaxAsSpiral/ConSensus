---
name: local-inference
description: Use when calling local models on the mesh. Adeck is the gateway for LM Studio, Qwen TTS, and any later embedder gateway. Covers the LM Studio proxy at http://100.89.32.9:1234/v1, JIT presets, reasoning dials, and the family-cookbook and esocortex callers.
compatibility: Daemonturgy mesh (nxiz/zrrh/adeck). Tailscale required. zrrh needs its GUI session for CUDA.
metadata:
  author: zk
  version: "2.8"
  category: inference
---

# local-inference

Adeck is the mesh gateway for local inference. Backends on it compete for the mesh. Read the leaf for the dial you are about to change. Driving a coding CLI is `cli-coding`.

| Backend | Gateway |
|---|---|
| LM Studio chat and the current embedding ids | `http://100.89.32.9:1234/v1`. Weights for the large models run on zrrh. |
| Qwen TTS | Separate backend on adeck. [tts](references/tts.md). |
| Embedders | No gateway of their own yet. |

| Leaf | When |
|---|---|
| [wake](references/wake.md) | Gated paths, WoL, timeouts. |
| [api](references/api.md) | Schema, `reasoning_effort`, vision preflight. |
| [models](references/models.md) | Cards, thinking dials, the Gemma spill. |
| [jit](references/jit.md) | KV, streams, embedding pin, TTL. |
| [tts](references/tts.md) | Qwen TTS on adeck. |
| [logs](references/logs.md) | Which host's LM Studio file to read. |
| [callers](references/callers.md) | family-cookbook and esocortex. |
| [paths](references/paths.md) | Flake paths and doc links. |
| [gpu](references/gpu.md) | A Nix-built binary misses the GPU. |

## URL

`http://100.89.32.9:1234/v1`

On adeck, `http://127.0.0.1:1234/v1` also works. From adeck, SSH by Tailscale IP. Hostnames do not resolve on that box.

## Call

```bash
curl -s http://100.89.32.9:1234/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen/qwen3.8-27b","messages":[{"role":"user","content":"Reply with exactly: PONG"}],"reasoning_effort":"none"}'
```

Cheap work sends `reasoning_effort` `"none"`. `"off"` is a 400. Do not set a small `max_tokens` on a thinking model. Omit it, or set it in the thousands. Structured output uses `json_schema`, `strict: true`, `additionalProperties: false`, and `required` on every object. Read `content` and `reasoning_content`.

Retry HTTP 408, 429, 502, 503, 504, and bodies that contain `LM Link connection closed`. A dead GUI session on zrrh is a 502 or 503.

```bash
ssh zk@100.89.32.9 lms ps
ssh zk@100.89.32.9 lms ls
ssh zk@100.89.32.9 lms link status
```

## Gone

This gateway is LM Studio, LM Link, and the wake proxy.
