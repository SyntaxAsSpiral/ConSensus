---
id: recipe-bedtime
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: bedtime
output_format: skill

target_locations:
  - path: ~/.claude/skills/bedtime/
  - path: ~/.agents/skills/bedtime/
  - path: zk@100.115.135.104:~/.claude/skills/bedtime/
  - path: zk@100.115.135.104:~/.agents/skills/bedtime/
  - path: zk@100.82.51.63:~/.claude/skills/bedtime/
  - path: zk@100.82.51.63:~/.agents/skills/bedtime/
  - path: fleet:/home/box/agent-data/workflows/bedtime/

sources:
  skill_md:
    frontmatter:
      name: bedtime
      description: >-
        Use when the user asks for a bedtime-story explanation of a complex concept.
      metadata:
        author: zk
        type: pseudo-skill
    body:
      - file: prompts/bedtime.md

validate_agentskills_spec: true
```
