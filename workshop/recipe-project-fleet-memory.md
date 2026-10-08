---
id: recipe-project-fleet-memory
created: 2026-10-08
modified: 2026-10-08
status: active
type:
  - agent
  - project
---

```yaml
name: FleetMemory
output_format: project
output_name: MEMORY.md

target_locations:
  - path: fleet:/workspace/shared/MEMORY.md

sources:
  - file: agents/steering-fleet-memory.md
```
