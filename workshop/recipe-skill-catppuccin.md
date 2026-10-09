---
id: recipe-catppuccin
created: 2026-01-15
modified: 2026-10-09
status: active
type:
  - skill
---

```yaml
name: catppuccin
output_format: skill

target_locations:
  - path: ~/.claude/skills/catppuccin/
  - path: ~/.agents/skills/catppuccin/
  - path: zk@100.115.135.104:~/.claude/skills/catppuccin/
  - path: zk@100.115.135.104:~/.agents/skills/catppuccin/
  - path: zk@100.82.51.63:~/.claude/skills/catppuccin/
  - path: zk@100.82.51.63:~/.agents/skills/catppuccin/

sources:
  skill_md:
    frontmatter:
      name: catppuccin
      description: Use when applying Catppuccin colors to a config, stylesheet, terminal theme, or prompt, including the variants rose, sage, grape, honey, and blueberry.
      license: MIT
      metadata:
        author: zk
        version: "2.0"
        category: theming
    body:
      - file: skills/catppuccin/SKILL.md

  references:
    - file: skills/catppuccin/references/flavors.md
      output_name: flavors.md
    - file: skills/catppuccin/references/variants.md
      output_name: variants.md
    - file: skills/catppuccin/references/terminal.md
      output_name: terminal.md
    - file: skills/catppuccin/references/roles.md
      output_name: roles.md
    - file: skills/catppuccin/references/css.md
      output_name: css.md
    - file: skills/catppuccin/references/starship.md
      output_name: starship.md
    - file: skills/catppuccin/references/palette.md
      output_name: palette.md

  assets:
    - file: skills/catppuccin/assets/palette-mutator.html
      output_name: palette-mutator.html

validate_agentskills_spec: true
```
