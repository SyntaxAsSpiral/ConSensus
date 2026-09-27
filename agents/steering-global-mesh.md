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
modified: 2026-09-26
status: active
glyph: "🕸️"
lens: infrastructure
---

# Mesh Infrastructure

## Tailscale Mesh — tail293e98.ts.net (SyntaxAsSpiral)

| Host | IP | Role | OS | GPU |
|------|----|------|----|-----|
| adeck | 100.89.32.9 | Central project and service host / relay (always on) | NixOS 26.05 | AMD Vangogh (Vulkan, 5.5 GiB) |
| nxiz | 100.115.135.104 | Workstation | NixOS 26.05 | RTX 3070 |
| zrrh | 100.77.90.79 | Compute Node | NixOS 26.05 | RTX 4090 |
| zdeck | 100.64.136.57 | Gaming | SteamOS | AMD Vangogh (Vulkan) |
| quita | 100.82.51.63 | Family laptop | Linux Mint | — |
| tm20 | 100.123.184.5 | Mesh print host (Pi 3B+) | NixOS 26.11 aarch64 | — |
| galaxy-tab-a7 | 100.119.0.71 | Kitchen / family client | Android | — |
| zk-pixel | 100.96.213.111 | Android phone | Android | — |
| zk-note | 100.105.239.55 | Android phone | Android | — |

## Host check

Always check `hostname -s` at the start of a session. From adeck, connect to other hosts by Tailscale IP.

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

## Mesh control plane

- `/mnt/echo/nix-os` is the canonical **NixOS** flake on adeck. Adeck, nxiz, and zrrh use `/etc/nixos` checkouts; tm20 receives secrets only and is built remotely.
- `/mnt/echo/consensus` is **ConSensus**, the canonical context vault. Its `workshop/` assembles agent instructions and skills; `zcli sync context` deploys the staged context without committing or pushing.
- `zcli` comes from `nix-os` and manages both context and system runtime: `zcli sync context` deploys ConSensus context, while `zcli sync [host|all]` publishes the NixOS snapshot, Git history, and secrets. `zcli build`, `deploy`, and `image` evaluate/build on zrrh; direct `nh os` remains local to the invoking host.

## Services

**Inference Gateway (`adeck:1234`):** All inference requests target `adeck:1234`. Adeck routes via `lmlink` — large models to `zrrh`, small models/embeddings local or to `nxiz`. OpenAI-compatible API (`/v1/chat/completions`, `/v1/embeddings`).

**Babette's Table (`adeck`):** Heirloom recipe curation agent at `https://adeck.tail293e98.ts.net`. Authoritative tree `/mnt/echo/family-cookbook`. Kitchen / family client is `galaxy-tab-a7`. Print host is `tm20` (Pi).

**tm20 print receiver:** `tm20` is the mesh print host. Other hosts and services submit jobs to `http://tm20:8766/print`; direct USB printing is only on `tm20`. See the **tm20** skill for setup, endpoint details, and printing workflow.

**SSH / Mullvad (`adeck`):** adeck runs Mullvad. From adeck, SSH by Tailscale IP only (adeck = `100.89.32.9`; other hosts from the table). MagicDNS / hostnames (`adeck`, `adeck.tail293e98.ts.net`, other mesh names) do not work from that box.

**Other services on adeck:** Docker, qBittorrent, SSH, Tailscale, msgvault, and Hermes agent. The `sideriod` and `bitburner` trees above host their respective Gnomon and sync/MCP services.

## Taildrop File Transfer

**Inbox:** `/tmp/taildrop-inbox/` on nxiz

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
