---
id: recipe-agent-fleet
created: 2026-10-14
modified: 2026-10-14
status: active
type:
  - agent
---

```yaml
name: Fleet
output_format: agent
output_name: scout.md
target_locations: []
sources:
  - slice: agent=scout
    slice-file: agents/bot-roles.md
---
output_name: architect.md
target_locations: []
sources:
  - slice: agent=architect
    slice-file: agents/bot-roles.md
---
output_name: foreman.md
target_locations: []
sources:
  - slice: agent=foreman
    slice-file: agents/bot-roles.md
---
output_name: warden.md
target_locations: []
sources:
  - slice: agent=warden
    slice-file: agents/bot-roles.md
---
output_name: sysop.md
target_locations: []
sources:
  - slice: agent=sysop
    slice-file: agents/bot-roles.md
---
output_name: imputer.md
target_locations: []
sources:
  - slice: agent=imputer
    slice-file: agents/bot-roles.md
---
output_name: artist.md
target_locations: []
sources:
  - slice: agent=artist
    slice-file: agents/bot-roles.md
```
