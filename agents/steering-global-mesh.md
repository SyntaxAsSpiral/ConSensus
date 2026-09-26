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

Always check `hostname -s` and state: “You are on `<host>`.” at the start of work. If unsure, compare the target with the detected local host before using SSH. From adeck, connect to other hosts by Tailscale IP.

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

- `/mnt/echo/nix-os` is the canonical NixOS flake on adeck. Adeck, nxiz, and zrrh use `/etc/nixos` checkouts; tm20 receives secrets only.
- `/mnt/echo/consensus` is **ConSensus**, the canonical context vault. Its `workshop/` assembles agent instructions and skills; `workshop/src/sync.py` currently deploys them separately from zcli and also commits and pushes.
- `zcli` comes from `nix-os`. Today `zcli sync` distributes the canonical committed-and-staged flake snapshot, local Git history, and secrets; `build`, `deploy`, and `image` use zrrh for evaluation and builds. Direct `nh os` remains local to the invoking host.

## Project and service trees on adeck

`/mnt/echo` also contains `family-cookbook` (Babette's Table and OCR), `holliday-estate` (estate catalog), `esocortex` (knowledge processing), `sideriod` (Gnomon), `bitburner` (game sync/MCP server), `inf-bench` (inference benchmarking, including ad hoc FLE eval runs), `stack-chan` (device and house-AI work), and `web/` (`whisperbell` and the dormant `lexemancy-site`, awaiting a revamp). Directory presence identifies a project tree, not service health; check the relevant service or worker before acting on it.

## Services

**Inference Gateway (`adeck:1234`):** All inference requests target `adeck:1234`. Adeck routes via `lmlink` — large models to `zrrh`, small models/embeddings local or to `nxiz`. OpenAI-compatible API (`/v1/chat/completions`, `/v1/embeddings`).

**Babette's Table (`adeck`):** Heirloom recipe curation agent at `https://adeck.tail293e98.ts.net`. Authoritative tree `/mnt/echo/family-cookbook`. Kitchen / family client is `galaxy-tab-a7`. Print host is `tm20` (Pi).

**tm20 thermal mesh print receiver (`tm20` Pi 3B+, `tm20:8766`):** Official mesh print host. NixOS aarch64 appliance configured in adeck's canonical `/mnt/echo/nix-os` flake (`nixosConfigurations.tm20`, no Home-Manager). First boot is `zcli image tm20` — sdImage built on zrrh (`boot.binfmt.emulatedSystems = [ "aarch64-linux" ]`). Live on tailnet at 100.123.184.5 (NixOS 26.11). Epson TM-T20III USB (`04b8:0e28`, 24V brick, USB-B); USB execution is **tm20 only**. udev (plugdev, unbind `usblp`) is configured in `hosts/tm20/configuration.nix`. No CUPS. CLIs open USB only (library TCP :9100 is unused). Paper: generic 80 mm / 3-1/8" thermal. Linux faces: Liberation Sans/Mono. The shared print receiver gates USB access for Holliday Table, holliday-estate, and sideriod. It accepts `POST http://tm20:8766/print` with a unique `job_id` plus a 576px PNG (`image`) or markdown (`markdown`); duplicate ids are not reprinted, and it uses one USB lock. Token `PRINT_TOKEN` (alias `HOLIDAY_PRINT_TOKEN`). Prefer the receiver from other hosts and long-running services. Use `tm20` / `tm20-set` while sitting at the print host for design, preview, hello, status, and recovering a jammed job. How to compose and when to use USB versus the receiver: skill **tm20**.

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
