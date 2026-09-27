---
id: recipe-obsidian-cli
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: obsidian-cli
output_format: skill

target_locations:
  - path: ~/.claude/skills/obsidian-cli/
  - path: ~/.agents/skills/obsidian-cli/
  - path: zk@100.115.135.104:~/.claude/skills/obsidian-cli/
  - path: zk@100.115.135.104:~/.agents/skills/obsidian-cli/
  - path: zk@100.82.51.63:~/.claude/skills/obsidian-cli/
  - path: zk@100.82.51.63:~/.agents/skills/obsidian-cli/

sources:
  skill_md:
    frontmatter:
      name: obsidian-cli
      description: Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.
    body:
      - file: skills/obsidian-cli/SKILL.md
  assets:
    - file: skills/obsidian-cli/LICENSE
      output_name: LICENSE

validate_agentskills_spec: true
```
