---
name: recall
description: "Reconstruct your recent working context from your own chat history, live state, and the shared record (user reports, prior fixes, incidents), then hand back a tight current-state brief. Use for 'recall my work on X', 'catch me up', 'what have I been working on', 'where did I leave off', before starting or resuming work."
---

# Recall

**Before you start or resume work, you rebuild the user's recent working context and hand back a tight capsule of where things stand now and what to do next.**

Keep it tight and on-topic. Read only what the in-scope threads need, then stop.

Your context lives in two records. Your own session history holds what you did and decided. The shared record holds everything that happened around the same code under other names: the symptoms users keep reporting, the fixes that shipped and got reverted, the errors still firing in prod. That second record lives across source control, the issue tracker, chat and issue channels, long-form docs, and error tracking. A feature with a long bug tail keeps most of its story there, so don't reconstruct it from your sessions alone.

Sessions live at `~/.pi/agent/sessions/<cwd-slug>/*.jsonl`, where the slug is the working directory with slashes turned into dashes (`/mnt/echo/consensus` becomes `--mnt-echo-consensus--`). Pi exports the current one as `$PI_SESSION_FILE`; if the variable is not set, take the newest `*.jsonl` in that directory. Every line is one message or event.

1. Classify, then route. Resuming one specific prior session is a narrower job — open that one file and continue where it left off; that is not this. Turning habits into a durable skill is a different task. A human-readable summary of your work is a different task. Recall loads working context across recent sessions before you act. If the user already gave you a full state capsule (paths, branch, the change), use it and skip the mining.
2. Lock the scope before searching. Pin the window ("recent" is a real range, default the last 7 days), the topic if named, and the working directory (default the active one. Never read another project's session files without being asked). State the scope back. Never quietly turn "all" into "recent N".
3. Fan out across your session history. Spawn parallel subagents, each a fresh pi in another herdr pane, started with no `--model` and no `--provider`, each taking a slice of the corpus; see the herdr skill for the CLI (`pane split`, `agent start --kind pi`, `agent prompt --wait`, `agent read`). Tell every subagent to order candidates by real modification time (`ls -t`), grep the topic first and then read only the matching sessions and only their relevant regions, and skip the current session (the one named by `$PI_SESSION_FILE`) plus obvious noise (subagent, eval, and test sessions). Each returns the same schema, one block per session: topic, the user's goal, decisions, open threads, struggles and corrections, and artifacts (PRs, tickets, branches), each citing the session id. For one or two sessions, skip the fan-out and search directly. The raw session data stays in the subagents. The main thread gets only their findings.
4. Sweep the shared record whenever the topic names a feature, file, subsystem, area, or bug. This is the default, not a judgment call, and "my work on X" does not exempt it. Steer the question from "why was this built this way" to "what's the current state, what's been tried and didn't hold, and what are users still reporting". Run one investigator per source (source control, the issue tracker, chat and issue channels, long-form docs, error tracking), in parallel with the session mining. Null results are findings. Skip an unavailable source and say so. Fold what comes back into the brief. Skip this step only for pure activity recall with no named target ("what did I do this week"), where your own history and live state are the entire answer.
5. Verify against live state. Take the PRs, branches, and tickets that the mining and the sweep surfaced and check them with `git` and `gh`. When the answer hinges on what an agent actually did (the tools it ran, files it read, errors it hit), read the full session file, not just a trimmed copy.
6. Write the brief to the contract below. Group by thread. Stay on the named topic.

## Output contract

Lead with the capsule, then the thread status, then the problems, then the next move. Deeper detail goes below or gets cut.

- **Capsule.** At most 5 bullets. What this work is and where it stands overall.
- **Threads.** One line each, prefixed with exactly one status tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, or `[planned, not started]`. A thread with no tag is not done yet, so tag it.
- **Problems.** At most 5, the recurring ones. Include the symptoms users keep reporting and any fix that shipped and was reverted, so the next attempt starts where the last one failed.
- **Next move.** The single most useful next action, concrete.

An adjacent feature or ticket stays out unless it blocks this one. When the capsule and thread lines outgrow a screen, cut detail before you cut threads. Write the brief in plain words with no AI speak, cite session findings by their session id and shared-record findings by their source (PR #, ticket ID, chat permalink, error-tracker issue), and sanitize private context before any public output.

**Reply:** the brief, to the contract above.
