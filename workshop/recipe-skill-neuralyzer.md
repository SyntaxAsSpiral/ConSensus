---
id: recipe-neuralyzer
created: 2026-10-10
modified: 2026-10-13
status: active
type:
  - skill
---

```yaml
name: neuralyzer
output_format: skill

target_locations:
  - path: ~/.claude/skills/neuralyzer/
  - path: ~/.agents/skills/neuralyzer/
  - path: zk@100.115.135.104:~/.claude/skills/neuralyzer/
  - path: zk@100.115.135.104:~/.agents/skills/neuralyzer/
  - path: zk@100.82.51.63:~/.claude/skills/neuralyzer/
  - path: zk@100.82.51.63:~/.agents/skills/neuralyzer/

sources:
  skill_md:
    frontmatter:
      name: neuralyzer
      description: >-
        Wipe this agent's stored memory when the user asks for a reset, a rewind, or to forget.
        Remove recent, project, or all global context.
    body:
      - file: skills/neuralyzer/SKILL.md
```
