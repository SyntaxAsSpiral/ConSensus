---
name: cli-coding
description: >-
  Seat a CLI coding agent when orchestrating a roster, a model route,
  granularity, pi, grok build, a handoff, or a prompt. 
metadata:
  author: zk
  version: "0.11"
  category: coding
---

# cli-coding

Who runs the work. Model quirks, the JIT table, and the GPU check are the mesh-ops inference leaf. Stream counts live only there.

Playbooks are not here yet. Read the leaf for the CLI you are about to launch.

## Roster

Always Pi on the local gateway, plus one primary cloud coder. One designation at a time.

Frontline is [references/pi.md](references/pi.md). The sequence is [references/routing.md](references/routing.md): money, then time, then quality. Home is the loaded local model at thinking `high`.

The current primary is Grok: `grok --prompt-file <task> --output-format json`. Read [references/grok.md](references/grok.md) before launching it.

Granularity is a model or effort change inside the seated CLI. The order is [references/routing.md](references/routing.md). Flag names stay in the Pi and Grok leaves. A second CLI is a different seat.

Other coding agents are logged under `Coding Agents` in `agents/agent-roles.md` and are not seated. Personas stay in that file. Fleet roles are not coding CLIs. Changing the primary is an edit of this section.

## Seats

| Seat | Who | When |
|---|---|---|
| Frontline | one `pi` session, provider `local`, `qwen/qwen3.8-27b`, thinking `high` | Read, narrow edit, local repro, one context. |
| Local alternate | `pi --provider local --model meta/muse-glimmer` | Qwen is the wrong local model. Loading it replaces the other large model. |
| Local fan-out | up to that model's JIT `parallel` | Independent slices, after `lms ps` shows a single instance. The number is in the mesh-ops inference leaf. |
| Escalation | the primary cloud coder | Free steps missed, or wider than the loaded streams. The launch line is in Roster. |
| Last resort | `pi --provider openrouter --model <id>` | The primary is at limit. Take `<id>` from `pi --list-models openrouter`. `--provider` requires `--model`. |

`pi-subagents` children are more Pi sessions on the same gateway. They share the one loaded model and its streams. Start them after that single instance is up. `pi-teams` opens more panes of the same agent and shares the same cap.

Concurrency and fan-out rules live in the Pi and Grok leaves.

The handoff carries the goal, absolute paths, the scope, and the command that proves the work. The caller reads the diff afterward. The other CLI's exit is not the proof.
