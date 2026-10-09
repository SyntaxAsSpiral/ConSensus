# Priority

Grain inside the seated CLIs. Lower priority is first. A blank priority is unset, and the seat table in `SKILL.md` stands until you fill one. Reasoning cells are the level to use for that row.

Pi local rows share one GPU. Loading a second large local model replaces the first. Pi cloud rows are OpenRouter ids from `pi --list-models openrouter`. Grok reasoning is `--reasoning-effort`: `xhigh`, `high`, `medium`, `low`. Pi local reasoning is `--thinking`: `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`. A cloud model's reasoning control is its own.

`grok models` also lists `grok-4.7-build-fast`. Add a row for it if it belongs in this order. The Pi cloud row is the moving alias. `pi --list-models openrouter` also lists the concrete id `z-ai/glm-5.3`.

| Priority | CLI | Where | Model | Reasoning |
|---|---|---|---|---|
| | Pi | local | `qwen/qwen3.8-27b` | |
| | Pi | local | `meta/muse-glimmer` | |
| | Pi | local | `google/gemma-4-31b` | |
| | Pi | cloud | `~z-ai/glm-latest` | |
| | Pi | cloud | | |
| | Grok | cloud | `grok-4.7` | |
| | Grok | cloud | `grok-4.6` | |
| | Grok | cloud | `grok-4.5` | |
