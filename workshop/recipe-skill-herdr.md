---
id: recipe-herdr
created: 2026-10-12
modified: 2026-10-12
status: active
type:
  - "skill"
---

```yaml
name: herdr
output_format: skill

target_locations:
  - path: ~/.claude/skills/herdr/
  - path: ~/.agents/skills/herdr/
  - path: zk@100.115.135.104:~/.claude/skills/herdr/
  - path: zk@100.115.135.104:~/.agents/skills/herdr/
  - path: zk@100.82.51.63:~/.claude/skills/herdr/
  - path: zk@100.82.51.63:~/.agents/skills/herdr/

  - path: fleet:/home/box/agent-data/workflows/herdr/
sources:
  tree: skills/upstream/herdr/skills/herdr
```
