---
name: catppuccin
description: Use when applying Catppuccin colors to a config, stylesheet, terminal theme, or prompt, including the variants rose, sage, grape, honey, and blueberry.
metadata:
  author: zk
  version: "2.0"
  category: theming
---

# catppuccin

Read the leaf for the surface you are coloring. Official hex is in [flavors](references/flavors.md). Variant hex is in [variants](references/variants.md). Do not invent a hex.

The NixOS desktop is Macchiato, set in `/mnt/echo/nix-os/modules/home/catppuccin.nix`. A Mocha hex on that desktop is the wrong flavor.

| Leaf | When |
|---|---|
| [flavors](references/flavors.md) | Latte, Frappé, Macchiato, Mocha. |
| [variants](references/variants.md) | rose, sage, grape, honey, blueberry, mochafrappe, au café. |
| [terminal](references/terminal.md) | ANSI 0–17 and window colors. |
| [roles](references/roles.md) | UI, syntax, and diff roles. |
| [css](references/css.md) | `--ctp-*` variables. |
| [starship](references/starship.md) | The prompt. |
| [palette](references/palette.md) | The Python palette object. |
| [assets/palette-mutator.html](assets/palette-mutator.html) | Hue, saturation, lightness, contrast, then export. |
