---
name: house-git
description: REQUIRED before an agent clones, writes, commits, or pushes a repo. House commit style for every project.
---

# House git

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

The frames in [references/frames.md](references/frames.md) are templates. Copy the border. Write the message on the inner lines, and repeat an inner line until it fits. Nothing sits outside the border. The editor template is [references/gitmessage](references/gitmessage).

The bracket is a title in the voice, then the chronohex. The chronohex is the last six hex digits of the nanosecond. A `⟳` context seal already counts.

The mode is how the message is written. Do not print its name.

- War cogitation. Tactical, clipped.
- Archival reconnaissance. Elegiac. What the archive now keeps.
- Binary glossolalia. Half logic, half vision.
- Heretekal communion. Gentle, curious, reverent.
