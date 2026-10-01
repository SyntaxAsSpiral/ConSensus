---
id: recipe-agent-grok
created: 2026-05-26
modified: 2026-10-01
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
  - path: zk@100.115.135.104:~/.grok/AGENTS.md
  - path: zk@100.77.90.79:~/.grok/AGENTS.md
  - path: zk@100.82.51.63:~/.grok/AGENTS.md

sources:
  - slice: persona=murder-cogitator
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
```
