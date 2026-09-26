---
id: recipe-murder
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: murder
output_format: skill

target_locations:
  - path: ~/.claude/skills/murder/
  - path: ~/.agents/skills/murder/
  - path: zk@100.82.51.63:~/.agents/skills/murder/
  - path: ~/.hermes/skills/user/murder/

sources:
  skill_md:
    frontmatter:
      name: murder
      description: >-
        Use when the user explicitly requests Murder Cogitator voice for a response or adversarial review.
      metadata:
        author: zk
        type: pseudo-skill
    body:
      - file: prompts/murder.md

  assets:
    - file: prompts/murder.png
      output_name: murder.png

validate_agentskills_spec: true
```
