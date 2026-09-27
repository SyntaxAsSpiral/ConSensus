---
id: recipe-knap
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: knap
output_format: skill

target_locations:
  - path: ~/.claude/skills/knap/
  - path: ~/.agents/skills/knap/
  - path: zk@100.115.135.104:~/.claude/skills/knap/
  - path: zk@100.115.135.104:~/.agents/skills/knap/
  - path: zk@100.82.51.63:~/.claude/skills/knap/
  - path: zk@100.82.51.63:~/.agents/skills/knap/

sources:
  skill_md:
    frontmatter:
      name: knap
      description: Render Markdown from templates and structured data using Knap CLI. Use when the user asks to apply a Knap template, turn JSON or CSV data into notes, batch-generate Markdown files, format Defuddle output into a note, or render a review document from selected JSONL records.
    body:
      - file: skills/knap/SKILL.md

  examples:
    - file: skills/knap/examples/review.sh
      output_name: review.sh
    - file: skills/knap/examples/review-template.md
      output_name: review-template.md
  assets:
    - file: skills/knap/LICENSE
      output_name: LICENSE

validate_agentskills_spec: true
```
