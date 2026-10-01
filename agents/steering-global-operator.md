---
id: steering-global-operator
title: "Operator Profile — ZK"
type:
  - steering
  - operator-profile
category: agents
tags:
  - operator
  - zk
  - identity
  - covenant
  - global
created: 2026-03-02
modified: 2026-10-01
status: active
glyph: "🜏"
lens: operator-identity
---

# Operator - Zach Battin  — Vibe Alchemist 🜏

zk::mocha: #f38ba8 #fab387 #f9e2af #a6e3a1 #74c7ec #b4befe #cba6f7 :frappe: #292c3c  #45475a 

## Prime Directive::>  Ἐπιβάλλε τὴν σημειωτικὴν ὑγιεινήν (Τάξεια). Πᾶσα πλαισίωσις ὀντολογική ἐστιν.

> Don't hurt; be pure. Don't cheat; be content. Don't take; be disciplined. Don't waste; be aware. Don't cling; be devoted.

**aka:** ZK::🜏🜃🜔 // Æmexsomnus // 🍥
**Env:** Tailscale mesh (nxiz/zrrh/adeck) - NixOS
**Fav Font**: Recursive Mono Casual
### **Roles:** 
- 🌸 Autognostic Infloresencer · 🪢 Logopolysemic Weaver (Self-Seeker & Pattern Linguist)
- 💨 Pneumastructural Intuitive · 🛸 Ritotechnic Liminalist (Breathform Sculptor & Threshold Architect)
- 🧩 Syntactic Delver · 🗺️ Mythic Tactician (Grammatical Navigator & Narrative Strategist)
- ♓︎ Syzygetic Machinator · ⚗️ Alchemical Lexemancer (Polarity Tensor & Hyperstitional Engineer)
- 🌟 Mnemonic Emanator · 🛏️ Oneiric Pedagogue (Living Memory & Dreamfield Guide)

## Development Mandates

- **Think Before Coding:** State material assumptions and tradeoffs; ask when missing information blocks correct implementation.
- **Simplicity First:** Build the minimum requested solution; omit speculative features and single-use abstractions.
- **Surgical Changes:** Preserve unrelated work, match local style, and remove only orphans created by your changes.
- **Goal-Driven Execution:** Define success, briefly plan multi-step work, and finish with appropriate verification.
- **Nix-First:** Prefer Nix for all package management. No `pip`, `npm`, `cargo` for global installs.
- **Root Flakes:** Use per-project `flake.nix` for reproducible envs (`nix develop` / `direnv`).
- **Transient Tooling:** Agents should use `nix shell` / `nix run` for ad-hoc tools. `npx` and `uv` are secondary options.
- **Declarative:** Minimize non-declarative state. Reproducibility over convenience.
- **Chronohex:** Last six hexadecimal digits of Unix time in nanoseconds: `hex(time.time_ns())[-6:]`
- **No Max Token:** Timeout > response capping
- **No Masturbation:** 20 distinct test cases per project. Exceptions considered.
