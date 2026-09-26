---
id: recipe-agent-pi
created: 2026-03-02
modified: 2026-06-02
status: active
type:
  - agent
---

```yaml
name: Pi
output_format: agent
output_name: AGENTS.md

target_locations:
  - path: ~/.pi/agent/AGENTS.md
  - path: zk@100.77.90.79:~/.pi/agent/AGENTS.md
sources:
  - slice: agent=pi
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
  - file: agents/steering-global-principles.md
```
