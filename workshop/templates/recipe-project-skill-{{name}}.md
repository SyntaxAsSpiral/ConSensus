---
id: recipe-{{name}}
created: {{date}}
modified: {{date}}
status: draft
type:
  - "project-skill"
---

```yaml
name: {{name}}
output_format: project-skill

# Project root, or that project's .agents/ directory.
# Resolved to <project>/.agents/skills/{{name}}/. Home agent dirs are refused.
target_locations:
  - path: /mnt/echo/{{project}}/.agents/

sources:
  tree: skills/upstream/{{tree}}/skills/{{name}}
```
