---
name: cli-coding
description: Use when choosing which coding CLI runs the work. The roster is always Pi on the local gateway plus one designated primary cloud coder. The current primary is Grok. Covers local fan-out up to one loaded model's prediction streams, escalation to that primary, and Pi on OpenRouter when the primary is at limit. Model dials, JIT presets, and GPU checks stay in local-inference.
metadata:
  author: zk
  version: "0.6"
  category: coding
---

# cli-coding

Who runs the work. Model quirks, the JIT table, and the GPU check are `local-inference`. Stream counts live only there.

Playbooks are not here yet. Read the leaf for the CLI you are about to launch.

## Roster

Always Pi on the local gateway, plus one primary cloud coder. One designation at a time.

Frontline is [references/pi.md](references/pi.md).

The current primary is Grok: `grok --prompt-file <task> --output-format json`. Read [references/grok.md](references/grok.md) before launching it.

Other coding agents are logged under `Coding Agents` in `agents/agent-roles.md` and are not seated. Personas stay in that file. Fleet roles are not coding CLIs. Changing the primary is an edit of this section.

## Seats

| Seat | Who | When |
|---|---|---|
| Frontline | one `pi` session, provider `local`, `qwen/qwen3.8-27b`, `--thinking off` | Read, narrow edit, local repro, one context. |
| Local alternate | `pi --provider local --model meta/muse-glimmer` | Qwen is the wrong local model. Loading it replaces the other large model. |
| Local fan-out | up to that instance's prediction streams | Independent slices, after `lms ps` shows a single instance. The count is the JIT `parallel` value in `local-inference`. |
| Escalation | the primary cloud coder | Hard work, or fan-out past the loaded streams. The launch line is in Roster. |
| Last resort | `pi --provider openrouter --model <id>` | The primary is at limit. Take `<id>` from `pi --list-models openrouter`. `--provider` requires `--model`. |

`pi-subagents` children are more Pi sessions on the same gateway. They share the one loaded model and its streams. Start them after that single instance is up. `pi-teams` opens more panes of the same agent and shares the same cap.

The handoff carries the goal, absolute paths, the scope, and the command that proves the work. The caller reads the diff afterward. The other CLI's exit is not the proof.
