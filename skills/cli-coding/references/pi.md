# Pi

The local frontline. Read this before launching it. Models, JIT presets, prediction-stream counts, and the GPU check are `local-inference`. This file is the CLI.

## Launch

```bash
pi --thinking off
```

That is one session, provider `local`, model `qwen/qwen3.8-27b`.

The other local model:

```bash
pi --provider local --model meta/muse-glimmer
```

`--provider` requires `--model`. Loading Muse replaces the other large model.

Last resort, only when the primary is at limit:

```bash
pi --provider openrouter --model <id>
```

Take `<id>` from `pi --list-models openrouter`.

`pi-subagents` children are more Pi sessions on the same local gateway. They share the one loaded model and its streams. Start them after `lms ps` shows a single instance. `pi-teams` opens more panes of the same agent and shares that cap.

## Checked config

Checked 2026-10-09 on adeck. These files were not edited.

- `pi` 1.1.0 is on `PATH`.
- `~/.pi/agent/settings.json` selects provider `local`, model `qwen/qwen3.8-27b`, `defaultThinkingLevel` `high`. Frontline passes `--thinking off` because that setting is `high`. `compaction.reserveTokens` is 131072, larger than the 100000 window.
- `~/.pi/agent/models.json` provider `local`: `api` `openai-completions`, `apiKey` `lms`, `contextWindow` 100000. `baseUrl` must be `http://100.89.32.9:1234/v1`. On that check it still said `http://adeck:1234/v1`. From adeck that hostname does not resolve.
- Whether `--thinking off` sends `reasoning_effort: "none"` to the gateway was not checked.
- The same file pins OpenRouter model `stealth/ox-alpha`. `pi --list-models openrouter` also prints Pi's built-in catalog.
- Extensions under `~/.pi/agent/git/` come from Pi's installer, not the Nix flake: `nicobailon/pi-subagents`, `burggraf/pi-teams`, `nicobailon/pi-mcp-adapter`. The flake documents an `npx` wrapper on nxiz only (`modules/home/daemonturgy/pi/README.md`).

## From another agent

No public skill encodes this seating. When a caller shells out instead of sitting in the TUI, `pi` 1.1.0 help shows the read-only shape:

```bash
pi --thinking off --tools read,grep,find,ls -p "<prompt>"
```

Add `edit,write` when the task writes files. Add `bash` only when it must run a command. `--no-tools` disables tools. `--mode json` and `--mode rpc` exist. `--no-session` skips saving the session. `-p` exits when the prompt finishes. The same proof rule as `SKILL.md` applies. The exit is not the diff.

yu-iskw `coding-agent-skills` `skills/pi-agent-cli` (license UNKNOWN, so the file is not copied) is that handoff, and it says project trust is not a sandbox. That claim was not re-checked in Pi's source. K-Dense `scientific-agent-skills` `skills/pi-agent` is MIT and was reviewed by them against Pi 0.99.2. The flags above were read from `pi --help` on 1.1.0. counterposition `skills/pi` is GPL-3.0. Do not paste it.

`pi-subagents` and `pi-teams` assume the caller is already inside Pi. Child model and thinking sit in their settings, not on the `pi` command. `pi-subagents` `docs/models.md` is that page. One failed provider does not fail over to another model.
