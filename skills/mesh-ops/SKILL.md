---
name: mesh-ops
description: >-
  REQUIRED: for all cross-host infrastructure, host configuration, system
  administration, and shared platform tasks outside a local project directory. Use this when interacting with system files, mounting storage, adjusting
  network parameters, modifying NixOS profiles, updating shared skill workflows,
  managing bot workspace paths on adeck, executing operations over SSH, or working
  with Tailscale or the tailnet.
---

# mesh-ops

## Hosts

| Host | IP | Role | OS | GPU |
|---|---|---|---|---|
| adeck | 100.89.32.9 | Central service host / relay (always on) | NixOS | AMD Vangogh (Vulkan, 5.5 GiB) |
| nxiz | 100.115.135.104 | Workstation | NixOS | RTX 3070 |
| zrrh | 100.77.90.79 | Compute Node | NixOS | RTX 4090 |
| quita | 100.82.51.63 | Laptop | Linux Mint | — |
| tm20 | 100.123.184.5 | Mesh print host (Pi 3B+) | NixOS 26.11 aarch64 | — |
| fleet | 100.88.86.114 | Bot VM. Where the bots live. Not a workshop deploy target | Debian 13 | — |

## Local host check

adeck runs Mullvad. From adeck, SSH by Tailscale IP only. Always check `hostname -s` at the start of a session.

## Remote work

Command strings with deeply nested quoting should not be attempted over SSH. Refer these actions to a local cli agent where possible, or use file-based execution as a last resort.

Exceptions: Read-only tasks, diagnostics, commit messages, and relatively simple strings with up to 2 levels of nested quoting are OK.

## Key mounts

Path exists on the host named in the table. Other hosts reach the tree through Taildrive WebDAV or SSH.

| Host | Path | Purpose |
|---|---|---|
| nxiz | `/mnt/repository` | Shared sandbox |
| nxiz | `/mnt/archive` | Archive storage |
| zrrh | `/mnt/media` | Media library |
| zrrh | `/mnt/games` | Game storage |
| adeck | `/mnt/vault` | Data lake |
| adeck | `/mnt/echo` | Active projects and mesh services |

## Control plane

`/mnt/echo` on adeck is the active project area for running services, on-demand operational work, and projects intended to become active services.

- `/mnt/echo/nix-os` is the canonical NixOS flake on adeck. Adeck, nxiz, and zrrh use `/etc/nixos` checkouts.
- `/mnt/echo/consensus` is ConSensus, the canonical context vault. Its `workshop/` assembles and deploys agent context and skills.

## Fleet paths

Bots live in the fleet VM and execute through the desktop app's runner on adeck. They are not CLI agents. `agents/bot-roles.md` holds that distinction. Their workspace is synced with the `/mnt/echo/exeglyph`.

A skill recipe marked `fleet:/home/box/agent-data/workflows/<name>/` is one the bots should take. The copy is `workshop/staging/skill/fleet/<name>/` in the consensus checkout on adeck. Sync does not write or purge that `fleet:` path.

## Canonical

- ConSensus
- nix-os/zk-nix

A canonical repo is written only in its local checkout on adeck, not via ssh. It also does not accept pushes except under extremely rare circumstances.

## Echo repos

Repos under `/mnt/echo` owned by zk (not 3rd party) other than the canonical pair are not canonical. Commit and push them, without waiting to be asked, when the merge is clean and the change does not break anything. Bots work in `/mnt/echo/exeglyph` through the adeck execution runner. They are not CLI agents. A CLI agent on adeck may also work in an echo repo.
