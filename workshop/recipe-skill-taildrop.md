---
id: recipe-taildrop
created: 2026-10-14
modified: 2026-10-14
status: active
type:
  - skill
---

```yaml
name: taildrop
output_format: skill

target_locations:
  - path: ~/.claude/skills/taildrop/
  - path: ~/.agents/skills/taildrop/
  - path: zk@100.115.135.104:~/.claude/skills/taildrop/
  - path: zk@100.115.135.104:~/.agents/skills/taildrop/
  - path: zk@100.82.51.63:~/.claude/skills/taildrop/
  - path: zk@100.82.51.63:~/.agents/skills/taildrop/
  - path: zk@100.77.90.79:~/.claude/skills/taildrop/
  - path: zk@100.77.90.79:~/.agents/skills/taildrop/

  - path: fleet:/home/box/agent-data/workflows/taildrop/
sources:
  skill_md:
    frontmatter:
      name: taildrop
      description: >-
        Retrieve a Taildrop file onto this host. Use when a phone or another mesh
        node has sent a file and it has not landed in the inbox yet.
    body:
      - file: skills/taildrop/SKILL.md
```
