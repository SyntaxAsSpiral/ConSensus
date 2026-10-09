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
# └── references/reference.md

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
      description: Use when calling local models on the mesh, loading or tuning an LM Studio JIT preset, or checking why llama.cpp or a CUDA/ROCm build does not see the GPU. Covers the gateway at http://100.89.32.9:1234/v1, reasoning dials, KV and prediction-stream presets, and the family-cookbook and esocortex callers.
      compatibility: Daemonturgy mesh (nxiz/zrrh/adeck). Tailscale required. zrrh needs its GUI session for CUDA.
      metadata:
        author: zk
        version: "2.5"
        category: inference
    
    body:  # Markdown instructions for agents
      - file: skills/local-inference/SKILL.md
  
  references:
    - file: skills/local-inference/references/reference.md
      output_name: reference.md
    - file: skills/local-inference/references/gpu.md
      output_name: gpu.md

# Validation
validate_agentskills_spec: true  # Ensure compliance with agentskills.io standard
```
