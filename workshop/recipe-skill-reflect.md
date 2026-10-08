---
id: recipe-reflect
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: reflect
output_format: skill

target_locations:
  - path: ~/.claude/skills/reflect/
  - path: ~/.agents/skills/reflect/
  - path: zk@100.115.135.104:~/.claude/skills/reflect/
  - path: zk@100.115.135.104:~/.agents/skills/reflect/
  - path: zk@100.82.51.63:~/.claude/skills/reflect/
  - path: zk@100.82.51.63:~/.agents/skills/reflect/
  - path: fleet:/home/box/agent-data/workflows/reflect/

sources:
  skill_md:
    frontmatter:
      name: reflect
      description: >-
        Use when the user requests a reflective development diary entry for a work session.
      metadata:
        author: zk
        type: pseudo-skill
    body:
      - file: prompts/reflect.md

validate_agentskills_spec: true
```
