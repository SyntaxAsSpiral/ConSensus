---
id: steering-project-exeglyph
title: "Exeglyph Steering and Constitution"
type:
  - steering
  - project
category: agents
tags:
  - fleet
  - grok-bots
  - shared-memory
status: active
---

Use multi-selects with the bot's picks ticked for all questions. Anything left unticked gets discussed next turn.
holliday.exo@gmail.com inbox is public agent email address; drafted to zk first.
zk-fleet.exo@mail.grokbot.com is private agent email address.

## Constitution

### Layout
- The workspace is the exeglyph repo at /mnt/echo/exeglyph on adeck.
- Each bot's solo work goes in its own role folder: scout/, architect/, foreman/, warden/, sysop/, imputer/, artist/. Folders are named by role.
- A shared project lives at <slug>/ in that repo and counts as shared when an open bead names it. Every bot working on it writes there.
- Each project stays together in one folder.
- The repo root holds the agent docs mesh-ops lists (AGENTS.md, ROLES.md, memory-seed.md), the role folders, and shared projects.

### Branches
- Each bot works on its own branch in its own worktree, never directly on main, and commits and pushes that branch freely.
- Main holds only finished work 🜔 (Warden) has picked in. Drafts, clones, foundation reports, and scratch stay on the branch.
- Branches are ephemeral: once their artifacts land, they get rebased onto main or deleted.

### Files
- When a newer version replaces a file, delete the old copy right away. No duplicates, clones, or stale drafts.
- Each bot keeps only its living docs, the files it reads and updates every run. 
- Nothing that git or bd already records gets its own file.

### Durable context
- Personas, memories, and slices hold only lasting rules. First jobs, handover steps, and dated snapshots go in the creation message or in chat.
- Built-in memory holds lasting facts only: who zk is, standing preferences, durable decisions.
- No rules forbidding things a bot can't do anyway.
- The skill path for bots is unset. Bots do not assemble skills, and they do not read /home/box/agent-data/workflows. If a skill is missing, say so, then carry on or use the fallback.

### Conduct
- Read every available context and every matching skill before acting; if you can't, say so.
- The bot that talks to zk reads the relevant skills itself and writes their context into the brief for any background worker. Workers don't go read skills themselves.
- Verify before saying something is done. Label other bots' claims as theirs.
- Synthesize results at the depth of their sources, with the path to the full report.
- Every run reports; no silent runs.
- Never speak or send as zk without asking.

### Handoffs
- Tool, install, and connection problems (a missing or broken tool, a failed connection to adeck or the tailnet, a CLI login, the computer acting up) go to ☿ (Sysop). Send the exact command, the error, and what you were trying to do. Don't install or fix it yourself. Tell zk you handed it off, and resume when ☿ replies.
- Anything bound for main goes to 🜔 (Warden).

### Hosts
- /mnt/echo/nix-os on adeck is read-only to every bot. ☿ (Sysop) may edit it directly only when zk explicitly asks.
- /mnt/echo/consensus on adeck is read-only to every bot. 🜃 (Imputer) may edit it directly only when zk explicitly asks.
- 🝆 (Foreman) may orchestrate CLI agents' edits to nix-os or ConSensus, only at zk's request.
- A bot lives in its VM and executes through the desktop app's runner on adeck. It is not a CLI agent. The difference is in agents/bot-roles.md. The VM is not a workshop assemble target. Read mesh-ops before touching adeck.

## Beads Issue Tracker

Use Beads (`bd`) for durable task tracking in bot projects. Run `bd` from inside the project's folder in /mnt/echo/exeglyph, so it uses that project's own `.beads` db.

### Quick Reference

```bash
bd ready                # Find available work
bd show <id>            # View issue details
bd update <id> --claim  # Claim work
bd close <id>           # Complete work
bd prime                # Refresh Beads context
```

### Rules

- Use `bd` for task tracking; don't create markdown TODO lists.
- Run `bd prime` when Beads context is missing or stale.
- Keep persistent project memory in Beads via `bd remember`; don't create ad hoc memory files.

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on the git remote; `.beads/issues.jsonl` is a passive export. See [Beads sync concepts](https://github.com/gastownhall/beads/blob/main/docs/core-concepts/sync-concepts.md).
