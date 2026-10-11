# Pi

The local frontline. Read this before launching it. Models, JIT presets, prediction-stream counts, and the GPU check are the mesh-ops inference leaf. This file is the CLI.

## Launch

```bash
pi
```

That is one session, provider `local`, model `qwen/qwen3.8-27b`, thinking at `defaultThinkingLevel` (`high`). The reason that level stays on is in `SKILL.md`.

Granularity on this CLI is `--thinking` (`off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`) and `--model`. The model id may carry the level (`id:high`). Which step to run is [routing.md](routing.md). Another large local model replaces the one on the GPU. The model cards are in the mesh-ops inference leaf.

`--thinking` is Pi's level, not the gateway's `reasoning_effort`. An invalid level only warns and runs at the default; it doesn't fail.

The other local model:

```bash
pi --provider local --model meta/muse-glimmer
```

`--provider` requires `--model`. Loading Muse replaces the other large model.

Last resort, only when the primary is at limit:

```bash
pi --provider openrouter --model ~z-ai/glm-latest
```

That alias moves. A `stealth/` id is temporary and is never pinned.

Live JIT `parallel`: `qwen/qwen3.8-27b` 4, `meta/muse-glimmer` 2. On adeck run `lms ps` directly. The `ssh zk@100.89.32.9 lms ps` form fails from adeck itself. Model swap cost: about 10s to load Muse, about 7s back to Qwen.

## Concurrency

Fan-out is N parallel `pi -p` runs, or one run that calls `subagent`. Both share the loaded model's JIT `parallel` streams (Qwen 4, Muse 2). Timings below were measured with `--no-session` and `--thinking off`. Frontline thinking stays `high`.

- Before fanning out, send one small request so the model is loaded. Parallel first requests to an unloaded model race the JIT load, and LM Studio cancels all but one (seen as `400 Failed to load model … Operation canceled`).
- zrrh suspends after about 30 minutes idle, and running inference does not count as activity. Keep each fan-out chunk under 30 minutes and wake with `zcli wake` rather than blocking sleep.
- Past the cap, requests queue in LM Studio. They don't error. A 6th run waits for a free stream (measured: 6 × ~80-word runs took 58 s of wall time vs ~26 s for 4).
- Parallelism helps throughput for real outputs, but each run gets slower. Tiny prompts gain nothing. Single-run latency on Qwen varies 4–25 s even at `--thinking off`.
- `pi-subagents` headless: the `subagent` tool with `tasks: [{agent: "delegate", task: ...}, ...]` runs in `mode: "parallel"` on the same model. Expect about 4.4k input tokens per child, and the parent spends one turn on `action: "list"` first. Telling it which agent to use skips that turn.
- Parallel `--tools read,edit` runs on separate files don't conflict. Give each run its own file. The diff is the proof.
- Never send a request for the other model while runs are in flight. A Muse request during Qwen runs failed (`400 … Engine protocol startup was aborted`), and the Qwen runs stalled while the model reloaded. Swap only when `lms ps` shows IDLE and nothing else is running, then reload the frontline model afterward.
- Exit 0 isn't output. Qwen sometimes prints raw `<tool_call>` text and exits 0, so check stdout.

## Config

- `pi` 1.1.0 is on `PATH`.
- `~/.pi/agent/settings.json` selects provider `local`, model `qwen/qwen3.8-27b`, `defaultThinkingLevel` `high`. The frontline inherits that level. `compaction.reserveTokens` is 131072, larger than the 100000 window.
- `~/.pi/agent/models.json` provider `local`: `api` `openai-completions`, `apiKey` `lms`, `contextWindow` 100000, `baseUrl` `http://adeck:1234/v1`. It resolves on adeck (checked 2026-10-09). From other hosts the gateway is `http://100.89.32.9:1234/v1`.
- No OpenRouter model is pinned in that file; Pi's built-in catalog covers it. Last resort is `~z-ai/glm-latest` (verified 2026-10-09). `pi auth check --provider openrouter` should print `ready`.
- Extensions under `~/.pi/agent/git/` come from Pi's installer, not the Nix flake: `nicobailon/pi-subagents`, `burggraf/pi-teams`, `nicobailon/pi-mcp-adapter`. The flake documents an `npx` wrapper on nxiz only (`modules/home/daemonturgy/pi/README.md`).

## From another agent

No public skill encodes this seating. When a caller shells out instead of sitting in the TUI, `pi --help` shows the read-only shape:

```bash
timeout 300 pi --no-session --tools read,grep,find,ls -p "<prompt>" </dev/null
```

`</dev/null` is required. Pi reads stdin as part of the prompt, and when stdin is an open pipe or socket (any agent shell) `-p` waits forever without calling the model. Add `edit,write` when the task writes files. Add `bash` only when it must run a command. `--no-tools` disables tools. `--no-session` skips saving a session under `~/.pi/agent/sessions/`. `--mode json` emits JSONL ending in `agent_settled`, including the whole system prompt. `--mode rpc` needs a client that keeps stdin open. `-p` exits after the turn. Each run prints three extension warnings to stderr (pi-subagents and pi-mcp-adapter peerDependencies, and pi-mcp-adapter shadowing the built-in `mcp`); ignore them or filter `^Warning: Extension`. The exit is not the diff.

`pi-subagents` works headless under `-p` (tool `subagent`, default agent `delegate`). `pi-teams` needs an interactive terminal and isn't usable from `-p`. Child model and thinking sit in their settings, not on the `pi` command. One failed provider does not fail over to another model.
