---
id: recipe-inquisition
created: 2026-10-08
modified: 2026-10-08
status: active
type:
  - skill
---

```yaml
name: inquisition
output_format: skill

target_locations:
  - path: ~/.claude/skills/inquisition/
  - path: ~/.agents/skills/inquisition/
  - path: zk@100.115.135.104:~/.claude/skills/inquisition/
  - path: zk@100.115.135.104:~/.agents/skills/inquisition/
  - path: zk@100.82.51.63:~/.claude/skills/inquisition/
  - path: zk@100.82.51.63:~/.agents/skills/inquisition/

sources:
  skill_md:
    frontmatter:
      name: inquisition
      description: >-
        Purge drift and slop from the documentation when asked for an inquisition,
        to purge, to excise, to lathe, to sker, to check documentatation, or when
        the user mentions drift, slop, cancer, corruption, or other heresies.
      metadata:
        author: zk
        type: skill
    body:
      - file: skills/inquisition/SKILL.md

  references:
    - file: skills/inquisition/references/unslop.md
      output_name: unslop.md

validate_agentskills_spec: true
```
