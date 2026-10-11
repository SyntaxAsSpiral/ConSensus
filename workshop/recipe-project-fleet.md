---
id: recipe-project-fleet
created: 2026-10-07
modified: 2026-10-11
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
  - path: fleet:/workspace/AGENTS.md

sources:
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-principles.md
    audience: remote
---
output_name: memory-seed.md

target_locations:
  - path: fleet:/workspace/memory-seed.md

sources:
  - file: agents/steering-fleet.md
```
!!!!! THIS RECIPE IS A PLACEHOLDER !!!!!!!
