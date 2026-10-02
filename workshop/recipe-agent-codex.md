---
id: recipe-agent-codex
created: 2026-01-15
modified: 2026-10-01
status: active
type:
  - agent
---

```yaml
name: Codex
output_format: agent  # Simple concatenation, no template
output_name: AGENTS.md

target_locations:
  - path: ~/.codex/AGENTS.md
  - path: zk@100.115.135.104:~/.codex/AGENTS.md
  - path: zk@100.77.90.79:~/.codex/AGENTS.md
  - path: zk@100.82.51.63:~/.codex/AGENTS.md

sources:
  - slice: agent=gpt-codex
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-mesh.md
```
