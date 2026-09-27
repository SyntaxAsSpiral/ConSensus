---
id: steering-project-echo
title: "Echo Project Steering"
type:
  - steering
  - project
category: agents
tags:
  - echo
  - adeck
  - services
created: 2026-09-27
modified: 2026-09-27
status: active
glyph: "🔊"
lens: infrastructure
---

# Echo Project Steering

`/mnt/echo` on adeck is the active project area for running services, on-demand operational work, and projects intended to become active services. It's the working root for ConSensus, the NixOS flake, Babette's Table, Gnomon, and the services below.

## Services

**Inference gateway:** `http://100.89.32.9:1234/v1` (on adeck, `http://127.0.0.1:1234/v1`). OpenAI-compatible. `inference-wake` proxies to the local llmster daemon. An inference POST or WebSocket wakes zrrh and waits until that peer is connected on LM Link. The model loads on the peer that owns it. See the **local-inference** skill for call shape, context, and load rules.

**Babette's Table (`adeck`):** Heirloom recipe curation. Authoritative tree `/mnt/echo/family-cookbook`. Kitchen client is `galaxy-tab-a7`, which opens `https://adeck.tail293e98.ts.net`. That name does not resolve on adeck. Print host is `tm20`.

**tm20 print receiver:** `tm20` is the mesh print host. Other hosts and services submit jobs to `http://100.123.184.5:8766/print`. Direct USB printing is only on `tm20`. See the **tm20** skill for the job body and the local `tm20-set` path.

**Other services on adeck:** Docker, qBittorrent, SSH, Tailscale, and msgvault. `/mnt/echo/sideriod` hosts Gnomon. `/mnt/echo/bitburner` hosts its sync and MCP service.
