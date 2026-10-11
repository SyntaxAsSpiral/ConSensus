---
id: recipe-agents-best-practices
created: 2026-09-26
modified: 2026-10-11
status: active
type:
  - "project-skill"
---

```yaml
name: agents-best-practices
output_format: project-skill

# This vault only. Loads while working in /mnt/echo/consensus.
# Not a home skill and not a fleet workflow.
target_locations:
  - path: /mnt/echo/consensus/.agents/

sources:
  tree: skills/upstream/agents-best-practices
```
