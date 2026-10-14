---
name: local-inference
description: >-
  Use when calling a local model on the mesh gateway. The gateway, the wake,
  JIT, and the 100k context cap.
compatibility: Daemonturgy mesh (nxiz/zrrh/adeck). GUI session for CUDA.
metadata:
  author: zk
  version: "3.0"
  category: inference
---

# local-inference

Adeck is the mesh gateway. Large-model weights run on zrrh. This gateway is LM Studio, LM Link, and the wake proxy.

## Gateway

`http://100.89.32.9:1234/v1`

On adeck, `http://127.0.0.1:1234/v1` also works. From adeck, SSH by Tailscale IP. Hostnames do not resolve on that box.

## Context

The gateway context cap is 100000. A card that says 262144 or 131072 still stops at 100k. That cap limits a fan-out and it limits a larger task. Both have to fit inside it.

## JIT

Do not load a chat model directly. `POST /api/v1/models/load` or `lms load` skips the JIT preset. The first `/v1/chat/completions` loads it.

adeck `http-server-config.json`: context 100000, `jitModelTTL` 1 h, `unloadPreviousJITModelOnLoad`.

| Model | KV | offload KV | streams (`parallel`) |
|---|---|---|---|
| `qwen/qwen3.8-27b` | q8_0 | true | 4 |
| `meta/muse-glimmer` | f16 | true | 2 |
| `google/gemma-4-31b` | flash + q4_0 | false | 2 |

`parallel` is not permission to pass the 100k cap. Embeddings are the exception that does load directly: qwen3-embedding-8b's own context is 40k and OOMs the 24 GB card, so pin `context_length: 8192`.

## Wake

Source: `nix-os/modules/home/daemonturgy/lmstudio/adeck/inference-wake.py`.

The proxy binds `0.0.0.0:1234` and forwards to `http://127.0.0.1:1235` (`lms daemon up`). These POSTs, and any WebSocket, wake zrrh before they proceed: `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/responses`, `/api/v0/chat/completions`, `/api/v0/completions`, `/api/v0/embeddings`, `/api/v1/chat`, `/api/v1/models/load`. A wake check runs before each downstream WebSocket frame.

Ready means zrrh is TCP-reachable at `192.168.0.110:22` and `lms link status --json` shows peer `zrrh` with `status: "connected"`. Otherwise WoL (`60cf8461d800` → `192.168.0.255:9`) every 3 s for 120 s, then 503 `zrrh did not reconnect to LM Link within 120 seconds.`

`GET /v1/models` does not wake. Connect timeout 10 s, read timeout 600 s. Upstream failure is 502 `LM Studio upstream unavailable.` A dead GUI session on zrrh is a 502 or 503.

## Call

Cheap work sends `reasoning_effort` `"none"`. `"off"` is a 400. Do not set a small `max_tokens` on a thinking model. Retry HTTP 408, 429, 502, 503, 504, and bodies that contain `LM Link connection closed`.

On adeck, run `lms ps` directly. `ssh zk@100.89.32.9 lms ps` fails from adeck itself.
