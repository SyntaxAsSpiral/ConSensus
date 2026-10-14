---
id: recipe-local-inference
created: 2026-04-20
modified: 2026-10-13
status: active
type:
  - skill
---

```yaml
name: local-inference
output_format: skill

target_locations:
  - path: ~/.claude/skills/local-inference/
  - path: ~/.agents/skills/local-inference/
  - path: zk@100.115.135.104:~/.claude/skills/local-inference/
  - path: zk@100.115.135.104:~/.agents/skills/local-inference/
  - path: zk@100.82.51.63:~/.claude/skills/local-inference/
  - path: zk@100.82.51.63:~/.agents/skills/local-inference/
  - path: zk@100.77.90.79:~/.claude/skills/local-inference/
  - path: zk@100.77.90.79:~/.agents/skills/local-inference/

sources:
  skill_md:
    frontmatter:
      name: local-inference
      description: >-
        Use when calling a local model on the mesh gateway. The gateway, the wake,
        JIT, and the 100k context cap.
      compatibility: Daemonturgy mesh (nxiz/zrrh/adeck). GUI session for CUDA.
      metadata:
        author: zk
        version: "3.0"
        category: inference
    body:
      - file: skills/local-inference/SKILL.md
```
