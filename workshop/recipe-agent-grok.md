---
id: recipe-agent-grok
created: 2026-05-26
modified: 2026-09-18
status: active
type:
  - agent
---
```yaml
name: Grok
output_format: agent
output_name: AGENTS.md

target_locations:
  - path: ~/.grok/AGENTS.md
  - path: zk@100.82.51.63:~/.grok/AGENTS.md   # Mesh (quita)

sources:
  - slice: agent=grok
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
  - file: agents/steering-global-principles.md
```
