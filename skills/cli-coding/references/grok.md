# Grok

The current primary. Read this before launching it. The seat and the handoff contract are in `SKILL.md`.

Checked on adeck 2026-10-09. `grok` 1.0.46 (`2765805b9442`) at `/run/current-system/sw/bin/grok`. Login was grok.com. `grok models` listed default `grok-4.7`, plus `grok-4.7-build-fast`, `grok-4.6`, and `grok-4.5`. Re-read `grok --help` before copying a flag that is not in the one-shot block below.

This leaf blends three upstream skills. The open-session client is copied under `scripts/`. grapeot's files and franke's `cdx.py` are not.

- One-shot contract from grapeot `ai-agent-cli-skill` `skills/grok_cli.md` (MIT, Copyright (c) 2026 grapeot). They verified Grok Build 1.0.4 on 2026-08-16. Their model list and their `install.sh` pin to 1.0.4 do not apply here. This machine's `grok` comes from Nix.
- Open session from scarletkc `agents` `skills/grok-cli` (Apache-2.0). Their client is copied at `skills/cli-coding/scripts/`. The argv below is what that script builds.
- Detached worker limits from boldprojekte `franke_skills` `skills/engineering/cxcc-subagent` (MIT, Copyright (c) 2026 Jan Franke). Their default backend is Codex and their model table seats Grok as the budget option. Neither is adopted. The Grok limits in their `references/runtime.md` are.

Invoke the binary `grok`. A generic `agent` on `PATH` is a different program. This is xAI Grok Build, not the community `grok-cli` package and not Groq.

## One-shot

The roster line. Use it when the task is one turn and the caller can wait.

```bash
grok --prompt-file <task> --output-format json --cwd <absolute-dir>
```

`--prompt-file` and `-p` / `--single` are single-turn. They stay up until the turn ends. There is no `grok exec` or `grok print`.

Flags present on 1.0.46 and useful on that command: `--permission-mode` (`default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`), `--always-approve`, `--max-turns`, `-m` / `--model`, `--reasoning-effort` / `--effort`, `--json-schema` (implies `--output-format json`), `--cwd`. `--output-format` also accepts `plain`, `streaming-json`, and `streaming-messages-json`.

Pass `-m` only when the task names a model. Otherwise leave the CLI default.

Exit 0 means the process ended. The proof is the diff and the command in the prompt file. A stdout summary is not that proof. If the prompt required a result file, the file has to be on disk and non-empty.

grapeot reported two traps on 1.0.4 that were not re-run on 1.0.46. If `XAI_API_KEY` is set, 1.0.4 billed the API key instead of the grok.com login. Passing `/deep-research …` as the headless prompt ended the turn immediately. Ask the model to call the `deep-research` workflow and wait, and if the report file is missing look under `~/.grok/sessions/<urlencoded-cwd>/<sessionId>/workflows/wf_*/scratch/report.md`.

## Open session

Use this when the same Grok session has to take a follow-up, an approval, or a cancel. The caller still cannot see Grok's conversation. `completed` means the turn ended.

scarletkc launches:

```text
grok [--permission-mode <mode>] [--sandbox <profile>] agent --no-leader [--model <id>] [--reasoning-effort <effort>] stdio
```

`--permission-mode` and `--sandbox` go before `agent`. `--model` and `--reasoning-effort` go after `--no-leader`. Then `stdio`. `--no-leader` and `agent stdio` both exist on 1.0.46. The ping below ran this shape.

Their client speaks ACP, returns a task id immediately, and stores state under `$XDG_STATE_HOME/grok-acp` or `~/.local/state/grok-acp`. Verbs: `start --cwd --prompt-file`, `wait`, `status`, `reply`, `permission --request-id --option-id`, `cancel`, `close`. `wait` returning on timeout does not cancel the turn. A follow-up waits until the current turn finishes. Answer `needs_approval` with an option id Grok offered. Omit `--permission-mode`, `--sandbox`, `--model`, and `--effort` to inherit Grok's own config. Do not pass `bypassPermissions` to avoid an approval.

The client is installed on adeck at `skills/cli-coding/scripts/grok.py`, copied from scarletkc commit `eb55005652d5708f369bde008cc48c71159f9e95` with `acp_client.py`, `agent_task_runtime.py`, and `windows_job.py`. Apache-2.0 text is `scripts/LICENSE`. Python 3.12 or newer. There is no Nix package. State is `$XDG_STATE_HOME/grok-acp` or `~/.local/state/grok-acp`.

```bash
python3 skills/cli-coding/scripts/grok.py start --cwd <absolute-dir> --prompt-file <task>
```

On 2026-10-09 a plan-mode ping from `/tmp/grok-acp-ping` returned task id `b98ae6ae8de541da95840a7db698f3a5`. `wait` finished `completed`, text `pong`, `auth_method` `cached_token`, `agent_version` `1.0.46`, model `grok-4.7`. `close` then set `closed` true. `start` itself only means the worker launched. Read `status` before treating the turn as finished.

This client drives Grok only. The command is hardcoded to `grok agent --no-leader stdio`. It does not start Pi, Claude, Codex, or Gemini.

## Detached

Use this only when the run has to outlive the caller. franke's `cdx.py` is that watchdog (`spawn`, `wait`, `send`, `result`, `peek`). It is not installed here. State would live under `~/.codex-agents`. Python 3.10+. `spawn --backend grok` is the Grok path. Their default backend is Codex, so a copied command that omits `--backend grok` does not start Grok.

Their Grok limits, from `references/runtime.md`:

- Grok exposes less activity than their other backends, so a long tool call raises `stall_suspect` sooner. Inspect `peek` once, then wait or replace the worker.
- Grok publishes a resumable session id only after the first turn completes. If that first turn stalls, spawn a fresh worker.
- A successful read of `cdx` exits 0 even when the task failed. The state field is the result. The shell exit is not.

The work order is the same handoff as `SKILL.md`. Their role files and their model taste table stay upstream.
