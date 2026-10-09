# JIT

adeck `http-server-config.json`: context 100000, `jitModelTTL` 1 h, `unloadPreviousJITModelOnLoad`. Presets in `~/.lmstudio/config-presets/` (adeck's are flake-managed; zrrh's are GUI-managed). Per-model JIT files on zrrh: `~/.lmstudio/.internal/user-concrete-model-default-config/`. LMS writes a field only after it is changed, so an empty `operation.fields` does not mean the UI lacks the control.

| Model | KV | offload KV | streams (`parallel`) |
|---|---|---|---|
| `qwen/qwen3.8-27b` | q8_0 | true | 4 |
| `meta/muse-glimmer` | f16 | true | 2 |
| `google/gemma-4-31b` | flash + q4_0 | false | 2 |

Chat loads pick this table up on the first `/v1/chat/completions`. `POST /api/v1/models/load` with `context_length` skips it. Embeddings are the exception: qwen3-embedding-8b's own `n_ctx` is 40k and OOMs the 24 GB card. Pin `context_length: 8192`. `ensure_loaded` treats 400/409/500 "already loaded" as success.

Embedding ids: `text-embedding-qwen3-embedding-8b` (zrrh), `text-embedding-qwen3-embedding-4b` (nxiz), `text-embedding-nomic-embed-text-v1.5` (adeck/nxiz/zrrh), `text-embedding-mxbai-embed-large-v1` (adeck/nxiz).

Qwen3.8 MTP is inside the GGUF. The weight-host log shows `common_speculative_init_result: creating MTP draft context` and draft acceptance about 0.80–0.98. It is a load-time property, not a per-request parameter. The grep is in [logs.md](logs.md).

Stock llama.cpp, which LM Studio ships, rejects ggml types outside `[0, GGML_TYPE_COUNT)`. Ternary Bonsai 2 `PTQ1_0` (143) and `PQ2_0` (142) need the Prism fork. The 1-bit `Q1_0` Bonsai does load. A `Q2_0` from a `-gguf-dev` repo can load and emit garbage. Match `bonsai-2-` or `ternary-bonsai-2`. The substring `bonsai-2` also matches `bonsai-27b`.
