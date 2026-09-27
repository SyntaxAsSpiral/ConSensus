---
id: recipe-agent-zed
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - agent
---
```yaml
name: Zed
output_format: agent
output_name: AGENTS.md

target_locations:
  - path: ~/.config/zed/AGENTS.md
  - path: zk@100.115.135.104:~/.config/zed/AGENTS.md
  - path: zk@100.77.90.79:~/.config/zed/AGENTS.md
  - path: zk@100.82.51.63:~/.config/zed/AGENTS.md

sources:
  - slice: agent=zed
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
  - file: agents/steering-global-principles.md
```
