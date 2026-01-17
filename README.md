
![consensus](context-vault.png)
# 🧩 ConSensus

**Shared context interface for AI agents** - a recipe-based assembly system for deploying agent configurations, skills, and prompts across heterogeneous AI platforms.

> *ConSensus: "conjoined sensing" - a system for shared perception without requiring unified consciousness.*  

*[Template Repository]* The reference implementation with real content is [zk-context-vault](https://github.com/SyntaxAsSpiral/zk-context-vault).

## 🔗 Concept

ConSensus enables shared context across AI platforms with different architectures and capabilities:

- **Synthesist pattern**: Recipe system interprets structural patterns without understanding semantic content
- **Write once, deploy everywhere**: Author in one place, assemble into platform-specific formats
- **Heterogeneous platforms**: Deploy to Kiro, Claude, Codex, Cursor, or custom agents
- **Standards-compliant**: Follows Agent Skills and Kiro Powers specifications
- **Path registry**: Single source of truth for agent paths via `agent-paths.yaml`

The system uses Obsidian as the authoring environment and Python scripts for assembly and deployment.

## 🪜 Architecture

### The Synthesist Model

Like the synthesist in Blindsight, the workshop system doesn't need to understand the content it processes. It recognizes structural patterns (slices, frontmatter, output formats) and assembles them into coherent deployments:

```
Raw Content → Recipe Patterns → Platform-Specific Outputs
(vault files)  (synthesist)     (deployed artifacts)
```

Each platform maintains its own "sensory apparatus" (tools, context windows, capabilities) but consumes the same assembled context through its respective interface.

### Directory Structure

```
agents/          # Agent configurations and steering rules
skills/          # Reusable agent skills (Agent Skills standard)
prompts/         # Prompt templates and cognitive modes
artifacts/       # Visual models (Obsidian Canvas files)
workshop/        # Assembly system
  agent-paths.yaml    # Path registry (single source of truth)
  src/                # Python scripts (assemble.py, sync.py)
  templates/          # Recipe templates
  recipe-*.md         # Active recipes
  staging/            # Generated outputs (gitignored)
  recipe-manifest.md  # Deployment tracking
```

### Workflow

1. **Author content** in `agents/`, `skills/`, `prompts/` using Obsidian
2. **Write recipes** in `workshop/` to define assembly targets
3. **Run assembly** (`python workshop/src/assemble.py`) → generates `workshop/staging/`
4. **Run sync** (`python workshop/src/sync.py`) → deploys to targets + auto-commits

## 🎮 Quick Start

See [workshop/QUICKSTART.md](workshop/QUICKSTART.md) for concise workflow guide.

### Setup

```bash
# Clone this template
git clone <your-fork-url>
cd consensus

# Open in Obsidian (optional but recommended)
# Launch Obsidian → "Open folder as vault" → Select consensus directory
```

### Basic Workflow

```bash
# Preview assembly
python workshop/src/assemble.py --dry-run --verbose

# Assemble recipes into staging
python workshop/src/assemble.py

# Preview deployment
python workshop/src/sync.py --dry-run --verbose

# Deploy staging to targets (auto-commits + pushes)
python workshop/src/sync.py
```

### Path Configuration

The system uses **relative paths** from script location - no hardcoded paths to update.

**Path conventions:**
- `~/` - Home directory (cross-platform)
- `.` - Current repo root (only for project steering recipes)
- `agent-paths.yaml` - Registry for agent-specific paths

## 🔗 Key Concepts

### Recipes

Recipes are Obsidian notes with embedded YAML defining assembly instructions:

```yaml
name: my-agent
output_format: agent  # or skill, power, command
target_locations:
  - path: ~/.claude/CLAUDE.md
sources:
  - file: agents/my-config.md
  # or slice extraction:
  # - slice: id=example
  #   slice-file: agents/multi.md
```

**Output formats:**
- `agent` - Simple markdown concatenation
- `skill` - Agent Skills standard (SKILL.md + folders)
- `power` - Kiro Power (POWER.md + steering/)
- `command` - Platform commands/prompts/hooks

### Slice Architecture

Extract specific sections using HTML comments:

```markdown
<!-- slice:id=example -->
Content to extract
<!-- /slice -->
```

Reference in recipes:
```yaml
sources:
  - slice: id=example
    slice-file: source.md
```

### Skills

Skills follow the [Agent Skills standard](https://agentskills.io):
```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed docs
└── assets/           # Optional: static resources
```

### Powers

Kiro Powers package skills with steering files:
```
power-name/
├── POWER.md          # Main documentation with frontmatter
├── mcp.json          # Optional: MCP server config
└── steering/         # Required: all guides as .md
```

## 📚 Documentation

- [workshop/QUICKSTART.md](workshop/QUICKSTART.md) - Concise workflow guide
- [workshop/README.md](workshop/README.md) - Detailed system documentation
- [workshop/templates/](workshop/templates/) - Recipe templates
- [skills/spec-agent-skill.md](skills/spec-agent-skill.md) - Agent Skills specification
- [skills/spec-kiro-power.md](skills/spec-kiro-power.md) - Kiro Power specification

## 🛸 Reference Implementation

See [zk-context-vault](https://github.com/SyntaxAsSpiral/zk-context-vault) for a working example with real content, active recipes, and deployed artifacts.

## Requirements

- Python 3.8+
- Obsidian (recommended for authoring)
- Git

## ⚠️ Template Notice

This is a template repository with placeholder content. Customize for your environment:
1. Replace example content in `agents/`, `skills/`, `prompts/`
2. Update `workshop/agent-paths.yaml` if needed
3. Create recipes for your deployment targets
4. Run the workflow

## Contributing

Issues and PRs welcome. This is an exploration of context-first AI workflows and the synthesist pattern for multi-platform agent deployment.

## License

MIT

---

*Shared perception without unified consciousness - context as compiled substrate 🜍⧉*
