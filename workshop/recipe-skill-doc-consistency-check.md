---
id: recipe-doc-consistency-check
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: doc-consistency-check
output_format: skill

target_locations:
  - path: ~/.claude/skills/doc-consistency-check/
  - path: ~/.agents/skills/doc-consistency-check/
  - path: zk@100.115.135.104:~/.claude/skills/doc-consistency-check/
  - path: zk@100.115.135.104:~/.agents/skills/doc-consistency-check/
  - path: zk@100.82.51.63:~/.claude/skills/doc-consistency-check/
  - path: zk@100.82.51.63:~/.agents/skills/doc-consistency-check/

sources:
  skill_md:
    frontmatter:
      name: doc-consistency-check
      description: >-
        Use when the user requests a documentation consistency check or repair of confirmed terminology drift.
      metadata:
        author: zk
        type: pseudo-skill
    body:
      - file: prompts/doc-consistency-check.md

validate_agentskills_spec: true
```
