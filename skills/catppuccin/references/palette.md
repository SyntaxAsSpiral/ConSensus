# Palette object

Use this when a flavor is missing from [flavors.md](flavors.md), or when you need every `--ctp-*` line emitted.

```bash
nix shell --impure --expr 'with import <nixpkgs> {}; python3.withPackages (ps: [ ps.catppuccin ])' -c python
```

```python
from catppuccin import PALETTE

mocha = PALETTE.mocha
for color in mocha.colors:
    name = color.name.lower().replace(" ", "")
    print(f"{name} {color.hex}")
```

`PALETTE.latte`, `PALETTE.frappe`, `PALETTE.macchiato`, and `PALETTE.mocha` are the flavors. `color.hex` includes the leading `#`. Do not `pip install` the package.
