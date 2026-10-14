---
name: reflect
description: Spawn three parallel reviewers over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Before fanning out, find this conversation's transcript under `~/.pi/agent/sessions/<cwd-slug>/`. The slug is the working directory with slashes replaced by dashes, padded with a dash at each end (`/mnt/echo/consensus` becomes `--mnt-echo-consensus--`), so glob around it:

```bash
slug=$(printf '%s' "$PWD" | tr / -)
ls -t ~/.pi/agent/sessions/*${slug}*/*.jsonl 2>/dev/null | head -10
```

For each candidate, read the first lines. The first line is the session header (it carries `cwd`); the first `message` line with role `user` is the conversation's opening prompt. Take the file whose opening prompt matches this conversation. If none matches, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

Start three herdr panes of pi, started with no `--model` and no `--provider`; the herdr skill has the pane and agent idiom. Reviewers need tool access to look up the tickets, chat threads, and observability traces the transcript references.

| Lens | Prompt template |
|---|---|
| Judgment | `references/judgment-reviewer.md` |
| Tooling | `references/tooling-reviewer.md` |
| Divergent | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return their findings in the pane's reply.

## 3. Synthesize

Start a fourth herdr pane of pi, started with no `--model` and no `--provider`, as the synthesizer. It spot-verifies citations with the tools available in its environment. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle in poteto-patterns.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent. Do not auto-apply.

File each Backlog item to your team's devex or backlog tracker without waiting. Only the Accepted list waits for approval.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): the parent drafts, tests, and iterates the change itself, matching the conventions of the skills already deployed.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): the parent rewrites the description until it fires, testing it against the session that should have matched.
- `new skill: <kebab-name>`: the parent creates it, following the conventions of the skills already deployed. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
