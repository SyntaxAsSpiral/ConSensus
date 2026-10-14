---
id: recipe-project-fleet
created: 2026-10-07
modified: 2026-10-14
status: active
type:
  - agent
  - project
---
```yaml
name: Exeglyph
output_format: project
output_name: AGENTS.md

target_locations:
  - path: /mnt/echo/exeglyph/AGENTS.md

sources:
  - file: agents/steering-global-principles.md
    audience: exeglyph
  - file: agents/steering-project-exeglyph.md
```
