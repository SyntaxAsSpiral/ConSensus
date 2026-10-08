---
id: recipe-agent-fleet
created: 2026-10-07
modified: 2026-10-07
status: active
type:
  - agent
---
```yaml
name: FleetRoles
output_format: agent
output_name: ROLES.md

target_locations: []

sources:
  - slice: agent=fleet-lead
    slice-file: agents/agent-roles.md
  - slice: agent=fleet-ops
    slice-file: agents/agent-roles.md
  - slice: agent=fleet-research
    slice-file: agents/agent-roles.md
  - slice: agent=fleet-design
    slice-file: agents/agent-roles.md
  - slice: agent=fleet-comms
    slice-file: agents/agent-roles.md
  - slice: agent=fleet-capital
    slice-file: agents/agent-roles.md
```
