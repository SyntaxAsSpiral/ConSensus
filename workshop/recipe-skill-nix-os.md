---
id: recipe-skill-nix-os
created: 2026-01-29
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: nix-os
output_format: skill

target_locations:
  - path: ~/.claude/skills/nix-os/
  - path: ~/.agents/skills/nix-os/
  - path: zk@100.115.135.104:~/.claude/skills/nix-os/
  - path: zk@100.115.135.104:~/.agents/skills/nix-os/
  - path: zk@100.82.51.63:~/.claude/skills/nix-os/
  - path: zk@100.82.51.63:~/.agents/skills/nix-os/

sources:
  skill_md:
    frontmatter:
      name: nix-os
      description: Use when working in a Nix environment outside the mesh flake — nix shell, nix develop, nix fmt, flakes, and one-shot tools. The mesh flake at /mnt/echo/nix-os has its own AGENTS.md. Do not install tools with pip, npm, or cargo.
    body:
      - file: skills/nix-os/SKILL.md

validate_agentskills_spec: true
```
