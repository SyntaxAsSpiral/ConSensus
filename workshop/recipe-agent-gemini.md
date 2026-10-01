---
id: recipe-agent-gemini
created: 2026-01-24
modified: 2026-10-01
status: active
type:
  - agent
---

```yaml
name: Gemini
output_format: agent
output_name: GEMINI.md

target_locations:
  - path: ~/.gemini/GEMINI.md
  - path: zk@100.115.135.104:~/.gemini/GEMINI.md
  - path: zk@100.77.90.79:~/.gemini/GEMINI.md
  - path: zk@100.82.51.63:~/.gemini/GEMINI.md

sources:
  - slice: persona=murder-cogitator
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
```
