---
id: recipe-cave
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: cave
output_format: skill

target_locations:
  - path: ~/.claude/skills/cave/
  - path: ~/.agents/skills/cave/
  - path: zk@100.115.135.104:~/.claude/skills/cave/
  - path: zk@100.115.135.104:~/.agents/skills/cave/
  - path: zk@100.82.51.63:~/.claude/skills/cave/
  - path: zk@100.82.51.63:~/.agents/skills/cave/
  - path: fleet:/home/box/agent-data/workflows/cave/

sources:
  skill_md:
    frontmatter:
      name: cave
      description: >-
        Use when the user asks for CaveTalk or terse, expressive cave-style replies.
      metadata:
        author: zk
        type: pseudo-skill
    body:
      - file: prompts/cave.md

validate_agentskills_spec: true
```
