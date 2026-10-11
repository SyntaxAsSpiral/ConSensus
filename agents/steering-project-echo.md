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
modified: 2026-10-10
status: active
glyph: "🔊"
lens: infrastructure
---

# Echo Project Steering

`/mnt/echo` on adeck is the active project area for running services, on-demand operational work, and projects intended to become active services. ConSensus and nix-os/zk-nix are the canonical checkouts. The other trees below are echo repos.

Checked against the running host on 2026-10-10. MagicDNS names do not resolve on adeck. Use the Tailscale IP or a loopback address from this box.

## Git

Echo repos other than the canonical pair: commit and push, without waiting to be asked, when the merge is clean and the change does not break anything. Fleet may clone, fork, and push those repos, and may work in a local checkout or through a CLI agent on adeck.

A checkout with no remote can be committed locally. `stack-chan`'s origin is `m5stack/StackChan`. Do not push there under this rule.

## Listeners

| Service | Bind | Tailnet | Tree |
|---|---|---|---|
| Holliday Table | `127.0.0.1:8876` | `https://adeck.tail293e98.ts.net` → this port | `/mnt/echo/family-cookbook` (`babette.git`) |
| Gnomon | `127.0.0.1:8878` | `https://adeck.tail293e98.ts.net:8878` | `/mnt/echo/sideriod` |
| Esocortex API | `127.0.0.1:8880` | `https://adeck.tail293e98.ts.net:8880` | `/mnt/echo/esocortex` |
| Hermes dashboard | `127.0.0.1:9119` | `https://adeck.tail293e98.ts.net:9119` | none (`~/.hermes`) |
| inference-wake | `0.0.0.0:1234` | `http://100.89.32.9:1234/v1` | none |
| llmster | `127.0.0.1:1235`, `127.0.0.1:41343` | none | none |
| LM Link connector | `0.0.0.0:55381` | none | none |
| Bitburner file sync | `*:12525` | `http://100.89.32.9:12525` | `/mnt/echo/bitburner` |
| Bitburner MCP | `*:9000` | `http://100.89.32.9:9000` | `/mnt/echo/bitburner` |
| qBittorrent WebUI | `0.0.0.0:8080` | `http://100.89.32.9:8080` | none |
| qBittorrent | tcp/udp `22008` on lo, `192.168.0.140`, and `100.89.32.9` | that address | none |
| SSH | `0.0.0.0:22`, `[::]:22` | `100.89.32.9:22` | none |

Holliday Table is the kitchen service. `galaxy-tab-a7` opens the tailnet name. Print host is `tm20` at `http://100.123.184.5:8766/print`. Direct USB printing is only on `tm20`.

`inference-wake` proxies to llmster on `127.0.0.1:1235`. An inference POST or WebSocket wakes zrrh and waits until that peer is connected on LM Link. See the **local-inference** skill. Esocortex is read-only. See the **esocortex** skill. Bitburner MCP is `http://100.89.32.9:9000`. See the **tm20** skill for print jobs.

Hermes gateway is running and has no listening port. Jolt is running and has no listening port. Docker is running and has no containers. msgvault is not running.

## Checkouts with no listener

`/mnt/echo/holliday-estate`, `/mnt/echo/inf-bench`, `/mnt/echo/stack-chan`, `/mnt/echo/web/lexemancy-site`, `/mnt/echo/web/whisperbell`.

`/mnt/echo/consensus` and `/mnt/echo/nix-os` are the canonical checkouts. They are not in the commit rule above.
