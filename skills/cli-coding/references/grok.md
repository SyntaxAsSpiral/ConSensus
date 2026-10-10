# Grok

The current primary. Read this before launching it. The seat and the handoff contract are in `SKILL.md`.

`grok` 1.0.46 (`2765805b9442`) at `/run/current-system/sw/bin/grok`. Login is grok.com. `grok models` lists default `grok-4.7`, plus `grok-4.7-build-fast`, `grok-4.6`, and `grok-4.5`. Re-read `grok --help` before copying a flag that is not in the one-shot block below.

This leaf blends three upstream skills. The open-session client is copied under `scripts/`. grapeot's files and franke's `cdx.py` are not.

- One-shot contract from grapeot `ai-agent-cli-skill` `skills/grok_cli.md` (MIT, Copyright (c) 2026 grapeot). They verified Grok Build 1.0.4 on 2026-08-16. Their model list and their `install.sh` pin to 1.0.4 do not apply here. This machine's `grok` comes from Nix.
- Open session from scarletkc `agents` `skills/grok-cli` (Apache-2.0). Their client is copied at `skills/cli-coding/scripts/`. The argv below is what that script builds.
- Detached worker limits from boldprojekte `franke_skills` `skills/engineering/cxcc-subagent` (MIT, Copyright (c) 2026 Jan Franke). Their default backend is Codex and their model table seats Grok as the budget option. Neither is adopted. The Grok limits in their `references/runtime.md` are.

Invoke `grok`. On this machine `agent` on `PATH` is Grok's own `agent-launcher` (same store path, `grok 1.0.46`); still call `grok`. This is xAI Grok Build, not the community `grok-cli` package and not Groq. Runs on 2026-10-09 used `grok-4.7-build-fast` wherever a model could be chosen. That id stays off the routing sequence.

## One-shot

The roster line. Use it when the task is one turn and the caller can wait.

```bash
grok --prompt-file <task> --output-format json --cwd <absolute-dir>
```

`--prompt-file` and `-p` / `--single` are single-turn. They stay up until the turn ends. There is no `grok exec` or `grok print`.

Flags present on 1.0.46 and useful on that command: `--permission-mode` (`default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`), `--always-approve`, `--max-turns`, `-m` / `--model`, `--reasoning-effort` / `--effort`, `--json-schema` (implies `--output-format json`), `--cwd`. `--output-format` also accepts `plain`, `streaming-json`, and `streaming-messages-json`.

`~/.grok/config.toml` sets `[cli] permission_mode = "always-approve"`. Without `--permission-mode` every tool runs unasked. Headless with `-p`, `default`, `acceptEdits`, `dontAsk` and `plan` never prompt. The turn ends without doing the gated work and exits 0. Only `auto` and `--always-approve` act. Do not pass `bypassPermissions`.

Granularity is `-m` / `--model` and `--reasoning-effort` (`xhigh`, `high`, `medium`, `low`). Which step to run is [routing.md](routing.md). Step 4 leaves both unset. `~/.grok/config.toml` has `models.default` `grok-4.7` and `default_reasoning_effort` `medium`.

Exit 0 means the process ended. The proof is the diff and the command in the prompt file. A stdout summary is not that proof. If the prompt required a result file, the file has to be on disk and non-empty. Exit 0 also happens when a command inside the task failed (the failure is only in the text). Exit 1 is `max turns reached`, an unknown `-m`, an unknown effort, a missing `--cwd` (before any cost), and an empty `-p`. Unset `-m` reports as `grok-4.7-build` in `modelUsage`. json output is one object: `text`, `usage`, `num_turns`, `total_cost_usd`, `modelUsage`. There is no `result` field. A tiny turn on `grok-4.7-build-fast` costs about $0.03 because of the fixed system prompt. stdin left open does not hang `grok -p`.

If `XAI_API_KEY` is set, grapeot's 1.0.4 billed the API key instead of the grok.com login. That case was not re-run; the key is unset here.

On 1.0.46, `-p "/deep-research"` with no query prints usage and ends in about 2s. With a query, ask the model to call the `deep-research` workflow and wait; if the report file is missing look under `~/.grok/sessions/<urlencoded-cwd>/<sessionId>/workflows/wf_*/scratch/report.md`. (The query case was not re-run.)

## Open session

Use this when the same Grok session has to take a follow-up, an approval, or a cancel. The caller still cannot see Grok's conversation. `completed` means the turn ended.

scarletkc launches:

```text
grok [--permission-mode <mode>] [--sandbox <profile>] agent --no-leader [--model <id>] [--reasoning-effort <effort>] stdio
```

`--permission-mode` and `--sandbox` go before `agent`. `--model` and `--reasoning-effort` go after `--no-leader`. Then `stdio`. `--no-leader` and `agent stdio` both exist on 1.0.46.

The client is `skills/cli-coding/scripts/grok.py`, with `acp_client.py`, `agent_task_runtime.py`, and `windows_job.py`. Apache-2.0 text is `scripts/LICENSE`. Python 3.12 or newer. There is no Nix package. State is `$XDG_STATE_HOME/grok-acp` or `~/.local/state/grok-acp`.

```bash
python3 skills/cli-coding/scripts/grok.py start --cwd <absolute-dir> --prompt-file <task>
```

Verbs: `start --cwd (--prompt | --prompt-file)` (stdin otherwise; empty is an error), plus `--turn-timeout`, `--idle-timeout`, `--startup-timeout`; `wait [--timeout N]`; `status`; `reply`; `permission --request-id --option-id`; `cancel`; `close`. `start` returns `starting` with `session_id` null; the id appears once the turn runs. Read `status` before treating the turn as finished. `wait` returning on timeout does not cancel. `reply` during a turn is refused (`Wait for the current turn to finish before replying`); wait, then reply. With config inherited, nothing prompts (always-approve). Pass `--permission-mode default` to get `needs_approval`; offered options are `allow-once`, `allow-edits-session`, `reject-once`. `cancel` keeps the session (`cancelled`, `closed:false`). `close` prints the pre-close state; `status` afterwards shows `closed:true`. Each task leaves `~/.local/state/grok-acp/<task_id>/` (events.jsonl, grok.log, worker.log) and a row in `tasks.sqlite3`. Delete the folder when done. Sessions also land in `~/.grok/sessions/<urlencoded-cwd>/`. Do not pass `bypassPermissions`.

This client drives Grok only. The command is hardcoded to `grok agent --no-leader stdio`. It does not start Pi, Claude, Codex, or Gemini.

## Detached

Use this only when the run has to outlive the caller. franke's `cdx.py` is that watchdog (`spawn`, `wait`, `send`, `result`, `peek`). It is not installed here. State would live under `~/.codex-agents`. Python 3.10+. `spawn --backend grok` is the Grok path. Their default backend is Codex, so a copied command that omits `--backend grok` does not start Grok.

Their Grok limits, from `references/runtime.md`:

- Grok exposes less activity than their other backends, so a long tool call raises `stall_suspect` sooner. Inspect `peek` once, then wait or replace the worker.
- Grok publishes a resumable session id only after the first turn completes. If that first turn stalls, spawn a fresh worker.
- A successful read of `cdx` exits 0 even when the task failed. The state field is the result. The shell exit is not.

The work order is the same handoff as `SKILL.md`. Their role files and their model taste table stay upstream.

## Parallel

Caller-side: parallel one-shots work (3 at once: 6.5s vs 15.7s serial, no lock or rate errors), and ACP sessions run side by side with separate task ids. Those runs used `grok-4.7-build-fast`. The leader is unused here; the client forces `--no-leader`. Shared-leader mode was not tested. Grok self fan-out: asked for parallel children, it calls `spawn_subagent` (kind `task`) and returns one joined answer; the caller sees the tool calls in `streaming-json`, not the child work. Whether the children ran truly in parallel was not measured. Use caller-side runs when each slice needs its own proof.
