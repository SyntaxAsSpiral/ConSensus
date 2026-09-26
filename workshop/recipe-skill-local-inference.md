---
id: recipe-local-inference
created: 2026-04-20
modified: 2026-09-18
status: active
type:
  - "skill"
---

```yaml
name: local-inference
output_format: skill  # Creates Agent Skills standard structure

# Agent Skills standard structure:
# local-inference/
# ├── SKILL.md (required - with YAML frontmatter + markdown body)
# └── references/ (optional - additional docs loaded on demand)
#     ├── process.md
#     ├── harness.md
#     └── links.md

target_locations:
  - path: ~/.claude/skills/local-inference/
  - path: ~/.agents/skills/local-inference/
  - path: zk@100.82.51.63:~/.agents/skills/local-inference/
  - path: ~/.gemini/antigravity/skills/local-inference/

# Source mapping to skill structure
sources:
  skill_md:
    # SKILL.md with required frontmatter
    frontmatter:
      name: local-inference
      description: Use when working with local inference on the mesh — the adeck:1234 gateway (wake proxy + LM Link), model loading/JIT config on zrrh/adeck/nxiz, structured output, reasoning budgets/toggles (reasoning_effort), MTP draft decoding, embeddings, pi's `local` provider, or the family-cookbook OCR/repair and esocortex consumers.
      compatibility: Designed for the daemonturgy mesh (nxiz/zrrh/adeck). Requires Tailscale mesh access; zrrh GUI session for CUDA.
      metadata:
        author: zk
        version: "2.0"
        category: inference
    
    body:  # Markdown instructions for agents
      - file: skills/local-inference/SKILL.md
  
  references:  # Optional - go to references/ folder (loaded on demand)
    - file: skills/local-inference/process.md
      output_name: process.md
    - file: skills/local-inference/harness.md
      output_name: harness.md
    - file: skills/local-inference/links.md
      output_name: links.md

# Validation
validate_agentskills_spec: true  # Ensure compliance with agentskills.io standard
```
