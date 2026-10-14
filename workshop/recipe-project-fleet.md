---
id: recipe-project-fleet
created: 2026-10-07
modified: 2026-10-13
status: active
type:
  - agent
  - project
---
```yaml
name: Fleet
output_format: project
output_name: AGENTS.md

target_locations:
  - path: /mnt/echo/exeglyph/AGENTS.md

sources:
  - file: agents/steering-global-principles.md
    audience: exeglyph
  - file: agents/steering-project-exeglyph.md
---
output_name: memory-seed.md

target_locations:
  - path: /mnt/echo/exeglyph/memory-seed.md

sources:
  - file: agents/steering-fleet.md
```
