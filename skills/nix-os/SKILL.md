---
name: nix-os
description: Use when working in a Nix environment outside the mesh flake — nix shell, nix develop, nix fmt, flakes, and one-shot tools. The mesh flake at /mnt/echo/nix-os has its own AGENTS.md. Do not install tools with pip, npm, or cargo.
---

# Nix

Use Nix for the project in front of you. Do not install tools into the user environment with pip, npm, or cargo.

## One-shot tools

```bash
nix shell nixpkgs#<tool> --command <tool>
```

## A repo with a flake

```bash
nix develop
nix flake check
nix fmt
nix run
nix build
```

`nix fmt` runs the formatter that flake declares. Do not add a package to a profile just to run one command.

## The mesh flake

`/mnt/echo/nix-os/AGENTS.md` is the manual for that repository. Read it when the work is in that tree. Mesh system changes go through `zcli deploy`, which the mesh steering file already states.
