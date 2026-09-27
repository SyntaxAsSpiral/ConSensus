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
modified: 2026-09-27
status: active
glyph: "🕸️"
lens: infrastructure
---

# Mesh Infrastructure

## Tailscale Mesh — tail293e98.ts.net (SyntaxAsSpiral)

| Host | IP | Role | OS | GPU |
|------|----|------|----|-----|
| adeck | 100.89.32.9 | Central service host / relay (always on) | NixOS | AMD Vangogh (Vulkan, 5.5 GiB) |
| nxiz | 100.115.135.104 | Workstation | NixOS | RTX 3070 |
| zrrh | 100.77.90.79 | Compute Node | NixOS | RTX 4090 |
| zdeck | 100.64.136.57 | Gaming | SteamOS | AMD Vangogh (Vulkan) |
| quita | 100.82.51.63 | Family laptop | Linux Mint | — |
| tm20 | 100.123.184.5 | Mesh print host (Pi 3B+) | NixOS 26.11 aarch64 | — |
| galaxy-tab-a7 | 100.119.0.71 | Kitchen / family client | Android | — |
| zk-pixel | 100.96.213.111 | Android phone | Android | — |
| zk-note | 100.105.239.55 | Android phone | Android | — |

## Host check

**SSH / Mullvad (`adeck`):** adeck runs Mullvad. From adeck, SSH by Tailscale IP only (adeck = `100.89.32.9`; other hosts from the table above). MagicDNS / hostnames (`adeck`, `adeck.tail293e98.ts.net`, other mesh names) do not work from that box. Always check `hostname -s` at the start of a session.

## Key Mounts

**Access:** Shared trees are accessed remotely through Taildrive WebDAV or SSH; filesystem mounts are available only on their respective local hosts.

| Host | Path | Purpose |
|------|------|---------|
| nxiz | `/mnt/repository` | Shared sandbox |
| nxiz | `/mnt/archive` | Archive storage |
| zrrh | `/mnt/media` | Media library |
| zrrh | `/mnt/games` | Game storage |
| adeck | `/mnt/vault` | Data lake |
| adeck | `/mnt/echo` | Active projects and mesh services |

`/mnt/echo` on adeck is the active project area for running services, on-demand operational work, and projects intended to become active services. The `adeck/echo` Taildrive share exposes this tree to other hosts.

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

## Mesh control plane

- `/mnt/echo/nix-os` is the canonical **NixOS** flake on adeck. Adeck, nxiz, and zrrh use `/etc/nixos` checkouts; tm20 receives secrets only and is built remotely.
- `/mnt/echo/consensus` is **ConSensus**, the canonical context vault. Its `workshop/` assembles agent instructions and skills; `zcli sync context` deploys the staged context without committing or pushing.
- `zcli` comes from `nix-os`. `zcli sync context` deploys the ConSensus workshop from adeck without committing or pushing. `zcli sync [host|all]` publishes committed and staged files, local git history, and secrets (tm20 receives secrets only). `zcli build`, `deploy`, and `image` wake zrrh and build there from `adeck:/mnt/echo/nix-os`. `zcli deploy <host>` schedules a reboot; `--switch` activates without rebooting. Apply system changes with `zcli deploy`. `zcli image tm20` builds the SD card. `zcli build tm20` does not.
