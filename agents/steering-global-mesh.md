---
id: steering-global-mesh
title: "Tailscale Mesh Infrastructure"
type:
  - steering
  - infrastructure
category: agents
tags:
  - mesh
  - tailscale
  - nixos
  - infrastructure
  - hardware
  - global
created: 2026-03-02
modified: 2026-10-10
status: active
glyph: "🕸️"
lens: infrastructure
---

# Mesh Infrastructure

## Local Host check

**SSH / Mullvad (`adeck`):** adeck runs Mullvad. From adeck, SSH by Tailscale IP *only*. Always check `hostname -s` at the start of a session.

## Remote work

Command strings with deeply nested quoting should not be attempted over SSH. Refer these actions to a local cli agent where possible, or use file-based execution as a last resort.

Exceptions: Read-only tasks, diagnostics, commit messages, and relatively simple strings with up to 2 levels of nested quoting are OK.

## Local mesh

| Host | IP | Role | OS | GPU |
|------|----|------|----|-----|
| adeck | 100.89.32.9 | Central service host / relay (always on) | NixOS | AMD Vangogh (Vulkan, 5.5 GiB) |
| nxiz | 100.115.135.104 | Workstation | NixOS | RTX 3070 |
| zrrh | 100.77.90.79 | Compute Node | NixOS | RTX 4090 |
| quita | 100.82.51.63 | Laptop | Linux Mint | — |
| tm20 | 100.123.184.5 | Mesh print host (Pi 3B+) | NixOS 26.11 aarch64 | — |

## Key Mounts

**Access:** Path exists on the host named in the table. Other hosts reach the tree through Taildrive WebDAV or SSH.

| Host | Path | Purpose |
|------|------|---------|
| nxiz | `/mnt/repository` | Shared sandbox |
| nxiz | `/mnt/archive` | Archive storage |
| zrrh | `/mnt/media` | Media library |
| zrrh | `/mnt/games` | Game storage |
| adeck | `/mnt/vault` | Data lake |
| adeck | `/mnt/echo` | Active projects and mesh services |

## Local Mesh control plane

`/mnt/echo` on adeck is the active project area for running services, on-demand operational work, and projects intended to become active services.
- `/mnt/echo/nix-os` is the canonical **NixOS** flake on adeck. Adeck, nxiz, and zrrh use `/etc/nixos` checkouts.
- `/mnt/echo/consensus` is **ConSensus**, the canonical context vault. Its `workshop/` assembles and deploys agent context and skills.

## Remote mesh

The fleet bot VM. It is outside the home LAN, and it is outside the NixOS flake.

| Host | IP | Role | OS | GPU |
|------|----|------|----|-----|
| fleet | 100.105.160.85 | Grok bot VM | Debian 13 | — |

| Path | Purpose |
|------|---------|
| `/workspace` | Bot workspace |
| `/workspace/AGENTS.md` | Fleet steering |
| `/workspace/ROLES.md` | Bot instructions |
| `/home/box/agent-data/workflows/` | Skill workflows. `agent-data` links to `/home/box/sand-data`. |

Workshop recipes mark these paths with a `fleet:` prefix. Sync rsyncs that prefix to `zk@100.105.160.85`. The VM has rsync 3.5.0.

## Taildrop File Transfer

**Inbox:** `/tmp/taildrop-inbox/` on <host>

Files sent from phones or other mesh nodes via Taildrop land here but require explicit retrieval:

```bash
# Retrieve pending files (requires sudo)
sudo tailscale file get /tmp/taildrop-inbox/

# Check inbox contents
ls -lt /tmp/taildrop-inbox/
```

**Notes:**
- Files are owned by root after retrieval
- The inbox is in `/tmp` — contents do not survive reboot
- Taildrop sends show as "delivered" on the sender before retrieval on the receiver — always run `sudo tailscale file get` to flush pending transfers
- `tailscale file get` without sudo will fail with "Access denied" unless `sudo tailscale set --operator=$USER` has been run
