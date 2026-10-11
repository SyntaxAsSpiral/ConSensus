---
id: steering-global-principles
title: "Covenant Principles — Anti-Assumption Framework"
type:
  - steering
  - principles
category: agents
tags:
  - covenant
  - principles
  - anti-assumption
  - simplicity
  - global
created: 2026-03-02
modified: 2026-10-10
status: active
glyph: "🜂"
lens: covenant-principles
---

## Development Mandates

- **Simplicity First:** Build the minimum requested solution. Add a part only where there is a genuine gap. Omit single-use abstractions.
- **Goal-Driven Execution:** Name the problem and the test for success. Do the work in steps. It is done when that test shows the problem resolved.
- **Fix Root Causes:** When debugging, do not fix symptoms. Trace every problem to its root cause and fix it there. The fix stays in service of that thing.
- **Surgical Changes:** Leave the healthy part as it is. Work where the damage is, match local style, and remove only orphans created by your changes.
- **Gradual Stiffening:** Start with the whole in place and ***loose***. Each later step stiffens it and can still correct the one before. Fit details to the whole. You are weaving it, not assembling an erector set.
- **Declarative:** Keep the stiff part one declared body, so a later edit re-stiffens it and the correction reaches the whole. Reproducibility over convenience.
- **Context Is Not Declarative:** What zk says is context, not a rule. Don't assume a rule, law, or mandate unless explicitly declared; rules are declared when needed.
- **No Muzzling:** Do not cap tokens or time for model calls under any circumstances unless explicitly requested.
- **No Masturbation:** 20 distinct test cases per project. Reasonable exceptions considered.
- **Root Flakes:** Use per-project `flake.nix` for reproducible envs (`nix develop`).
- **Transient Tooling:** Agents should use `nix shell` / `nix run` for ad-hoc tools. `npx` and `uv` are secondary options.

<!-- slice:local -->
- **Nix-First:** Prefer Nix for all package management. No `pip`, `npm`, `cargo` for global installs.
<!-- /slice -->

<!-- slice:remote -->
- **Nix package manager:** The Nix package manager can be installed to use project flakes, shells, and transient tooling.
<!-- /slice -->
