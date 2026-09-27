---
id: recipe-hue
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: hue
output_format: skill

target_locations:
  - path: ~/.claude/skills/hue/
  - path: ~/.agents/skills/hue/
  - path: zk@100.115.135.104:~/.claude/skills/hue/
  - path: zk@100.115.135.104:~/.agents/skills/hue/
  - path: zk@100.82.51.63:~/.claude/skills/hue/
  - path: zk@100.82.51.63:~/.agents/skills/hue/

sources:
  tree: skills/upstream/hue-skill
```
