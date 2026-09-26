---
id: recipe-gamut
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: gamut
output_format: skill

target_locations:
  - path: ~/.claude/skills/gamut/
  - path: ~/.agents/skills/gamut/
  - path: zk@100.82.51.63:~/.agents/skills/gamut/
  - path: ~/.hermes/skills/user/gamut/

sources:
  skill_md:
    frontmatter:
      name: gamut
      description: >-
        Use when the user asks for five distinct perspectives with explicit uncertainty across a question.
      metadata:
        author: zk
        type: pseudo-skill
    body:
      - file: prompts/gamut.md

validate_agentskills_spec: true
```
