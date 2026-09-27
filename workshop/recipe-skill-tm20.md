---
id: recipe-tm20
created: 2026-09-05
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: tm20
output_format: skill

target_locations:
  - path: ~/.claude/skills/tm20/
  - path: ~/.agents/skills/tm20/
  - path: zk@100.115.135.104:~/.claude/skills/tm20/
  - path: zk@100.115.135.104:~/.agents/skills/tm20/
  - path: zk@100.82.51.63:~/.claude/skills/tm20/
  - path: zk@100.82.51.63:~/.agents/skills/tm20/

sources:
  skill_md:
    frontmatter:
      name: tm20
      description: >-
        Print 80 mm thermal slips and receipts on the mesh Epson TM-T20III via tm20/tm20-set
        or the tm20 print receiver. Use when designing or printing tape, item listings,
        logos, QR, ESC/POS, 1-bit art, or when the user mentions tm20, TM-T20III, thermal
        printer, 80 mm receipts, or the mesh print receiver. Slash: /tm20
      metadata:
        author: zk
        version: "0.5.0"
        category: print
        compatibility: USB and tm20 binaries are the tm20 Pi only; other hosts POST the receiver. No CUPS. Paper must be loaded.

    body:
      - file: skills/tm20/SKILL.md

  references:
    - file: skills/tm20/references/motifs.md
      output_name: motifs.md

validate_agentskills_spec: true
```
