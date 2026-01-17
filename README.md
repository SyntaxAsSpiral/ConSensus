
![consensus](context-vault.png)
# 🧩 Consensus

**Context vault assembly workshop** for building AI agent context systems.<br>
*[Template]* A recipe-based workflow for deploying agent configurations, skills, and prompts across multiple AI platforms. The reference implementation is [zk-context-vault](https://github.com/SyntaxAsSpiral/zk-context-vault).

## 🔗 Concept

Consensus provides a structured approach to managing AI agent context:
- **Write once, deploy everywhere**: Create content in one place, assemble into multiple formats
- **Recipe-based assembly**: Define what goes where using declarative recipes
- **Multi-platform support**: Deploy to Kiro, Claude, custom agents, or MCP servers
- **Standards-compliant**: Follows Agent Skills and Kiro Powers specifications

The system uses Obsidian as the authoring environment and Python scripts for assembly and deployment.

## 🪜 Current Status

**Template repository.** This is a clean starting point for building your own context vault. For a working example with real content, see [zk-context-vault](https://github.com/SyntaxAsSpiral/zk-context-vault).

**Planned**: The workshop assembly functions will be integrated as a built-in Obsidian plugin, allowing recipe execution directly from the vault interface.

## Architecture

### Directory Structure

```
agents/          # Agent configurations and steering rules
skills/          # Reusable agent skills (Agent Skills standard)
prompts/         # Prompt templates for different cognitive modes
artifacts/       # Visual models (Obsidian Canvas files)
workshop/        # Assembly system for deploying context
  src/           # Python scripts (assemble.py, sync.py)
  templates/     # Recipe templates
  recipe-*.md    # Active recipes
  staging/       # Generated outputs (gitignored)
```

### Workflow

1. **Author content** in `agents/`, `skills/`, `prompts/` using Obsidian
2. **Write recipes** in `workshop/` to define assembly targets
3. **Run assembly** to generate outputs in `workshop/staging/`
4. **Run sync** to deploy to target locations (like `~/.kiro/`, `~/.claude/`)

## 🔗 Key Concepts

### Recipes

Recipes are Obsidian notes with embedded YAML that define:
- What content to assemble
- Where to deploy it
- What format to use (agent, skill, power, command)

Example recipe:
```yaml
name: my-agent
output_format: agent
target_locations:
  - path: ~/.claude/CLAUDE.md
sources:
  - file: agents/my-config.md
```

### Skills

Skills follow the [Agent Skills standard](https://agentskills.io):
- Flat directory structure
- `SKILL.md` with YAML frontmatter
- Optional `scripts/`, `references/`, `assets/` folders

### Powers

Kiro Powers package skills with steering files:
- `POWER.md` - Main documentation
- `steering/` - Additional guides
- `mcp.json` - Optional MCP server config

## 🎮 Usage

### Setup

```bash
# Clone this template
git clone <your-fork-url>
cd consensus

# Open in Obsidian
# Launch Obsidian → "Open folder as vault" → Select consensus directory
```

### Basic Workflow

```bash
# Assemble recipes into staging
python workshop/src/assemble.py

# Deploy staging to targets
python workshop/src/sync.py
```

### Customization

1. **Replace example content** with your own agents, skills, and prompts
2. **Update paths** in `workshop/src/assemble.py` and `sync.py` for your environment
3. **Create recipes** for your deployment targets
4. **Run the workflow** to deploy

## 📚 Learn More

- Check `workshop/templates/` for recipe examples
- See `skills/spec-agent-skill.md` for skill format
- See `skills/spec-kiro-power.md` for power format
- Review [zk-context-vault](https://github.com/SyntaxAsSpiral/zk-context-vault) for a working implementation

## Requirements

- Python 3.8+
- Obsidian (optional, but recommended for authoring)
- Git

## ⚠️ Development Warning

This is a template for personal context systems. Customize paths and content for your environment.

## Contributing

Issues and PRs welcome! This is an exploration of context-first AI workflows.

## License

Private research tool - not for distribution.

---

*Context as compiled substrate, recipes as assembly instructions 🜍*
