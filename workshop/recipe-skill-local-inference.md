---
id: recipe-local-inference
created: 2026-04-20
modified: 2026-10-09
status: active
type:
  - "skill"
---

```yaml
name: local-inference
output_format: skill  # Creates Agent Skills standard structure

# Agent Skills standard structure:
# local-inference/
# ├── SKILL.md
# └── references/{wake,api,models,jit,logs,callers,paths,gpu}.md

target_locations:
  - path: ~/.claude/skills/local-inference/
  - path: ~/.agents/skills/local-inference/
  - path: zk@100.115.135.104:~/.claude/skills/local-inference/
  - path: zk@100.115.135.104:~/.agents/skills/local-inference/
  - path: zk@100.82.51.63:~/.claude/skills/local-inference/
  - path: zk@100.82.51.63:~/.agents/skills/local-inference/
  - path: zk@100.77.90.79:~/.claude/skills/local-inference/
  - path: zk@100.77.90.79:~/.agents/skills/local-inference/

# Source mapping to skill structure
sources:
  skill_md:
    # SKILL.md with required frontmatter
    frontmatter:
      name: local-inference
      description: Use when calling local models on the mesh. Adeck is the gateway for LM Studio, Qwen TTS, and any later embedder gateway. Covers the LM Studio proxy at http://100.89.32.9:1234/v1, JIT presets, reasoning dials, and the family-cookbook and esocortex callers.
      compatibility: Daemonturgy mesh (nxiz/zrrh/adeck). Tailscale required. zrrh needs its GUI session for CUDA.
      metadata:
        author: zk
        version: "2.8"
        category: inference
    
    body:  # Markdown instructions for agents
      - file: skills/local-inference/SKILL.md
  
  references:
    - file: skills/local-inference/references/wake.md
      output_name: wake.md
    - file: skills/local-inference/references/api.md
      output_name: api.md
    - file: skills/local-inference/references/models.md
      output_name: models.md
    - file: skills/local-inference/references/jit.md
      output_name: jit.md
    - file: skills/local-inference/references/tts.md
      output_name: tts.md
    - file: skills/local-inference/references/logs.md
      output_name: logs.md
    - file: skills/local-inference/references/callers.md
      output_name: callers.md
    - file: skills/local-inference/references/paths.md
      output_name: paths.md
    - file: skills/local-inference/references/gpu.md
      output_name: gpu.md

# Validation
validate_agentskills_spec: true  # Ensure compliance with agentskills.io standard
```
