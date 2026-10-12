---
id: recipe-agent-fleet
created: 2026-10-07
modified: 2026-10-12
status: active
type:
  - agent
---
```yaml
name: FleetRoles
output_format: agent
output_name: ROLES.md

target_locations:
  - path: fleet:/workspace/ROLES.md

sources:
  - slice: agent=fleet
    slice-file: agents/agent-roles.md
```
