---
name: git
description: Use when an agent clones, writes, commits, or pushes a repo, or needs to know whether that repo is read, write, or push. House commit style for every project.
---

# Git

The commit style is the same on every project. The repos are not.

## Mesh repos

ConSensus. Canonical. Bots may read and deploy. Changes go through coding agents. A push to `main` that touches `workshop/staging/agent/GrokBot/` runs `.github/workflows/ping-bigw-steering.yml`, which pings the fleet deploy webhook. The bots' wrapper places that assembly into their env. They do not run the sync scripts.

nix-os/zk-nix. Canonical. Bots may read. Changes go through coding agents.

## Fleet repos

exeglyph. Bots read, write, and push. Artifacts live here, not loose in `/workspace`.

Bots may clone other zk repos to work in freely as needed but must clean them out of shared workspace when finished. 

## Others' repos

Reference checkouts. Update by fast-forward. A change we keep is a copy in our own tree. The checkout keeps its license.

## Commit

The operator's own message is `zk`. When he gives that, use it and stop. Do not dress it up.

An agent message is for him to read. He does not read a plain log. Address him as flesh-thing. Be entertaining. The fact of the change still has to be in there, or the joke is empty.

The voice is the frames in [references/frames.md](references/frames.md). Copy a frame when the message wears it. Do not reword the words. Pick the mode that can hold the joke.

The last line is a chronohex, the last six hex digits of the nanosecond, as `|` those digits `| stable.` A `⟳` context seal already counts.
