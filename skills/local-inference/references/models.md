# Model cards

Stream counts are in [jit.md](jit.md).

100K is `defaultContextLength: 100000` (runtime 100096). Card maxima are larger and do not fit this KV/parallel setup.

**`qwen/qwen3.8-27b`** — Q4_K_M, ~17.7 GB, arch `qwen35`. Card context 262144. Official efforts: `xhigh` (default), `medium`, `low`. Official off-switch is `chat_template_kwargs.enable_thinking: false`; on this gateway use `reasoning_effort: "none"`. `preserve_thinking` defaults on. mmproj `mmproj-Qwen3.8-27B-BF16.gguf`. MTP head is inside the GGUF. Thinking sample: temp 1.0, top_p 0.95, top_k 20. Instruct: temp 0.7, top_p 0.8, presence_penalty 1.5. Hub `lmstudio-community/Qwen3.8-27B-GGUF`.

**`google/gemma-4-31b`** — Q4_K_M, ~19.9 GB, arch `gemma4`. Card context 262144. At this quant and 100K it does not fit entirely on the 24 GB GPU, so it spills and is slower. Do not quantize harder. Thinking is `<|think|>` in the system turn. LMS v1 options are `off|on` only. Thoughts are `<|channel>thought`. On 31B, thinking-off still emits an empty thought channel. Strip prior thoughts from history. Sampling: temp 1.0, top_p 0.95, top_k 64. Hub `lmstudio-community/gemma-4-31B-it-GGUF`.

**`meta/muse-glimmer`** — 30B card (LMS `params_string: 28B` is the text decoder; ~1.8–2B vision encoder on top). Card context 131072. A client label of "26b" is stale. There is no off switch. Send `chat_template_kwargs: {"reasoning_strength": "low"}`. `reasoning_effort` and `enable_thinking` are absent from the template. LMS v1 exposes only `on`. Sampling: temp 1.0, top_p 0.95, top_k 64. JSON, when constrained, belongs in `to=user` → `message.content`. Speculative decoding is a separate draft (Meta DFlash), not a baked MTP head. Hub `lmstudio-community/Muse-Glimmer-30B-GGUF`. Prompting: <https://ai.developer.meta.com/docs/muse-glimmer/prompting.md>.
