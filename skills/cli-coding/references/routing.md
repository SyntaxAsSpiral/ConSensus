# Routing

Order is money, then time, then quality. Take the first step that holds. A later step spends more of an earlier axis.

Local rows share one GPU. Loading a second large model replaces the first. Pi thinking is `--thinking`: `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`. Grok effort is `--reasoning-effort`: `xhigh`, `high`, `medium`, `low`. A cloud model's control is its own.

Local reasoning is unmetered and the model needs it, so the floor is `high`. Grok bills more as effort rises. Higher effort costs time on both.

Quality is assumed to rise with reasoning effort. That link is untested. The check is one scored throughput task, same model, two efforts, production score against step latency. Setup, including the solver pin, is `local-inference` `references/bench.md`.

| Step | Cell | Money | Time | Quality |
|---|---|---|---|---|
| 1 | Loaded local model, usually `qwen/qwen3.8-27b`, thinking `high` | Zero | Floor | Home while it holds |
| 2 | Same model, one effort step up | Zero | Worse | After a miss on the right tool. The gain is the untested assumption |
| 3 | Other local model. Muse when Qwen is the wrong tool. Gemma last, because at 100K it spills | Zero | Swap, plus that model's own cost | Wrong tool. Muse has no off switch. Its knob is `reasoning_strength` |
| 4 | `grok-4.7` at `medium` | Billed | Configured floor | Free steps missed, or the work is wider than the loaded streams |
| 5 | Same Grok model, one effort step | More | More | Medium missed. Same untested assumption |
| 6 | `~z-ai/glm-latest`, effort named on this row | OpenRouter | Named | Grok is at its limit. This row does not inherit the local floor |

`grok-4.6`, `grok-4.5`, and `grok-4.7-build-fast` stay off this order until a row says when they beat `grok-4.7`. `pi --list-models openrouter` also lists the concrete id `z-ai/glm-5.3`. Step 6 uses the moving alias.

A miss, or the wrong tool, is the quality signal. There is no quality rank across families.
