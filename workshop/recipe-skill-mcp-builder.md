---
id: recipe-skill-mcp-builder
created: 2026-01-16
modified: 2026-01-16
status: active
type:
  - "skill"
---

```yaml
name: mcp-builder
output_format: skill  # Creates Agent Skills standard structure

# Agent Skills standard structure:
# mcp-builder/
# ├── SKILL.md (required - with YAML frontmatter + markdown body)
# ├── scripts/ (optional - executable code)
# │   ├── evaluation.py
# │   └── connections.py
# ├── references/ (optional - additional docs loaded on demand)
# │   ├── python_mcp_server.md
# │   ├── node_mcp_server.md
# │   ├── mcp_best_practices.md
# │   ├── evaluation.md
# │   └── example-evaluation.xml.md
# └── assets/ (optional - static resources)

target_locations:
  - path: ~/.claude/skills/mcp-builder/
  - path: ~/.codex/skills/mcp-builder/
  - path: ~/.cursor/skills/mcp-builder/
  - path: ~/.gemini/skills/mcp-builder/
  - path: ~/.gemini/antigravity/skills/mcp-builder/

# Source mapping to skill structure
sources:
  skill_md:
    # SKILL.md with required frontmatter
    frontmatter:
      name: mcp-builder
      description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
      license: Complete terms in LICENSE.txt
      compatibility: Python 3.8+ for evaluation scripts; Node.js 16+ or Python 3.8+ for server development
      metadata:
        author: zk
        version: "1.0"
        category: integration
    
    body:  # Markdown instructions for agents
      - file: skills/mcp-builder/SKILL.md
  
  scripts:  # Optional - go to scripts/ folder
    - file: skills/mcp-builder/evaluation.py.md
      output_name: evaluation.py
    - file: skills/mcp-builder/connections.py.md
      output_name: connections.py
  
  references:  # Optional - go to references/ folder (loaded on demand)
    - file: skills/mcp-builder/python_mcp_server.md
      output_name: python_mcp_server.md
    - file: skills/mcp-builder/node_mcp_server.md
      output_name: node_mcp_server.md
    - file: skills/mcp-builder/mcp_best_practices.md
      output_name: mcp_best_practices.md
    - file: skills/mcp-builder/evaluation.md
      output_name: evaluation.md
    - file: skills/mcp-builder/example-evaluation.xml.md
      output_name: example-evaluation.xml.md

# Validation
validate_agentskills_spec: true  # Ensure compliance with agentskills.io standard
```
