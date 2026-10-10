---
id: recipe-cli-coding
created: 2026-10-09
modified: 2026-10-09
status: active
type:
  - "skill"
---

```yaml
name: cli-coding
output_format: skill

target_locations:
  - path: ~/.claude/skills/cli-coding/
  - path: ~/.agents/skills/cli-coding/
  - path: zk@100.115.135.104:~/.claude/skills/cli-coding/
  - path: zk@100.115.135.104:~/.agents/skills/cli-coding/
  - path: zk@100.82.51.63:~/.claude/skills/cli-coding/
  - path: zk@100.82.51.63:~/.agents/skills/cli-coding/
  - path: zk@100.77.90.79:~/.claude/skills/cli-coding/
  - path: zk@100.77.90.79:~/.agents/skills/cli-coding/

sources:
  skill_md:
    frontmatter:
      name: cli-coding
      description: Use when choosing which coding CLI runs the work. Frontline is Pi on the local gateway. The cloud primary is Grok. Last resort is Pi on OpenRouter. Model dials stay in local-inference.
      metadata:
        author: zk
        version: "0.11"
        category: coding
    body:
      - file: skills/cli-coding/SKILL.md

  references:
    - file: skills/cli-coding/references/pi.md
      output_name: pi.md
    - file: skills/cli-coding/references/grok.md
      output_name: grok.md
    - file: skills/cli-coding/references/routing.md
      output_name: routing.md

  scripts:
    - file: skills/cli-coding/scripts/grok.py
      output_name: grok.py
    - file: skills/cli-coding/scripts/acp_client.py
      output_name: acp_client.py
    - file: skills/cli-coding/scripts/agent_task_runtime.py
      output_name: agent_task_runtime.py
    - file: skills/cli-coding/scripts/windows_job.py
      output_name: windows_job.py
    - file: skills/cli-coding/scripts/LICENSE
      output_name: LICENSE
    - file: skills/cli-coding/scripts/SOURCE.md
      output_name: SOURCE.md

validate_agentskills_spec: true
```
