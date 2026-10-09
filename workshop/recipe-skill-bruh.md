---
id: recipe-bruh
created: 2026-10-08
modified: 2026-10-08
status: active
type:
  - skill
---

```yaml
name: bruh
output_format: skill

target_locations:
  - path: ~/.claude/skills/bruh/
  - path: ~/.agents/skills/bruh/
  - path: zk@100.115.135.104:~/.claude/skills/bruh/
  - path: zk@100.115.135.104:~/.agents/skills/bruh/
  - path: zk@100.82.51.63:~/.claude/skills/bruh/
  - path: zk@100.82.51.63:~/.agents/skills/bruh/
  - path: fleet:/home/box/agent-data/workflows/bruh/

sources:
  skill_md:
    frontmatter:
      name: bruh
      description: >-
        Use when the user asks to bruh, reframe, restyle, eli*, or render
        work through a creative lens (bedtime, cave, debate, pentasoph,
        gamut, hpmor, moeverse, quest, or a new frame).
      metadata:
        author: zk
        type: metaskill
    body:
      - file: skills/bruh/SKILL.md

  references:
    - file: skills/bruh/references/bedtime.md
      output_name: bedtime.md
    - file: skills/bruh/references/cave.md
      output_name: cave.md
    - file: skills/bruh/references/debate.md
      output_name: debate.md
    - file: skills/bruh/references/pentasoph.md
      output_name: pentasoph.md
    - file: skills/bruh/references/gamut.md
      output_name: gamut.md
    - file: skills/bruh/references/hpmor.md
      output_name: hpmor.md
    - file: skills/bruh/references/moeverse.md
      output_name: moeverse.md
    - file: skills/bruh/references/quest.md
      output_name: quest.md

validate_agentskills_spec: true
```
