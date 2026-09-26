---
id: recipe-moeverse
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: moeverse
output_format: skill

target_locations:
  - path: ~/.claude/skills/moeverse/
  - path: ~/.agents/skills/moeverse/
  - path: zk@100.82.51.63:~/.agents/skills/moeverse/
  - path: ~/.hermes/skills/user/moeverse/

sources:
  skill_md:
    frontmatter:
      name: moeverse
      description: >-
        Use when the user asks for an anime character personification of a system or concept.
      metadata:
        author: zk
        type: pseudo-skill
    body:
      - file: prompts/moeverse.md

validate_agentskills_spec: true
```
