---
id: recipe-defuddle
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: defuddle
output_format: skill

target_locations:
  - path: ~/.claude/skills/defuddle/
  - path: ~/.agents/skills/defuddle/
  - path: zk@100.115.135.104:~/.claude/skills/defuddle/
  - path: zk@100.115.135.104:~/.agents/skills/defuddle/
  - path: zk@100.82.51.63:~/.claude/skills/defuddle/
  - path: zk@100.82.51.63:~/.agents/skills/defuddle/

sources:
  skill_md:
    frontmatter:
      name: defuddle
      description: Extract clean Markdown from HTML pages with Defuddle CLI.
    body:
      - file: skills/defuddle/SKILL.md
  assets:
    - file: skills/defuddle/LICENSE
      output_name: LICENSE

validate_agentskills_spec: true
```
