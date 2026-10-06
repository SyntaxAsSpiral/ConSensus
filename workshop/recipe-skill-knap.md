---
id: recipe-knap
created: 2026-09-26
modified: 2026-10-06
status: active
type:
  - "project-skill"
---

```yaml
name: knap
output_format: project-skill

# Project root or its .agents/ directory. Deployed to <project>/.agents/skills/knap/.
# /mnt/mount does not exist on adeck; esocortex is /mnt/echo/esocortex.
target_locations:
  - path: /mnt/echo/esocortex/.agents/

sources:
  tree: skills/upstream/obsidian-skills/skills/knap
```
