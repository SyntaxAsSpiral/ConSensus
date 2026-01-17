# AGENTS.md

This AGENTS.md serves as a self-documenting example of project-level steering within the context vault. This template is rendered as AGENTS.md at the root of this repo so all instructions here are actually applied to agents working within the repo. It also serves as a template for generating project-scope AGENTS.md or CLAUDE.md docs for any project.

> **Note for Agents!** To update `./AGENTS.md`, make changes on THIS document `agents/steering-project-context-vault.md`. Then rerun the assembly and sync processes to sync changes.

> **Reference Implementation**: See [zk-context-vault](https://github.com/SyntaxAsSpiral/zk-context-vault) for a working example with real content.

## What This Is

A template repository for building AI agent context systems using:
- **Obsidian** for editing and visual modeling
- **Recipe system** for assembling content from multiple sources
- **Python scripts** for automated deployment

## Directory Structure

### `/agents/` - Agent Configurations
Example agent configurations and steering rules. Replace with your own.

**Example files:**
- `agent-roles.md` - Agent identity templates
- `steering-global-operator.md` - Operator profile template
- `steering-global-principles.md` - Core principles template
- `steering-project-context-vault.md` - This file (project steering example)

### `/skills/` - Agent Skills
Skills following the [Agent Skills standard](https://agentskills.io).

**Structure:**
```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed docs
└── assets/           # Optional: static resources
```

**Example skills:**
- `catppuccin-theming/` - Color palette management
- `mcp-builder/` - MCP server development guide
- `spec-agent-skill.md` - Agent Skills specification
- `spec-kiro-power.md` - Kiro Power specification

### `/prompts/` - Prompt Templates
Example prompt templates for different cognitive modes.

**Subdirectories:**
- `hook-prompts/` - Markdown sources for Kiro hook creation

### `/artifacts/` - Visual Models
Obsidian Canvas files for visual modeling.

**Subdirectories:**
- `golden/` - Reference implementations and examples

### `/workshop/` - Assembly System
Recipe-based system for assembling and deploying context.

**Key files:**
- `src/assemble.py` - Assembles recipes into staging
- `src/sync.py` - Deploys staging to targets
- `templates/` - Recipe templates
- `recipe-*.md` - Active recipes
- `recipe-manifest.md` - Deployment tracking log
- `staging/` - Generated outputs (not committed)

## Using This Template

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd context-vault-template
```

Open in Obsidian:
- Launch Obsidian
- "Open folder as vault"
- Select the repository directory

### 2. Replace Example Content

- Update `agents/` with your agent configurations
- Create your own skills in `skills/`
- Add your prompts to `prompts/`
- Customize `workshop/recipe-*.md` for your deployment targets

### 3. Update Paths

Edit `workshop/src/assemble.py` and `sync.py`:
- Update absolute paths to match your system
- Adjust deployment targets (`~/.claude/`, `~/.kiro/`, etc.)

### 4. Run the Workflow

```bash
# Assemble recipes
python workshop/src/assemble.py

# Deploy to targets
python workshop/src/sync.py
```

## Recipe System

Recipes define what content to assemble and where to deploy it.

### Recipe Format

```yaml
name: example
output_format: agent  # or skill, power, command
target_locations:
  - path: ~/.claude/CLAUDE.md
sources:
  - file: agents/example.md
```

### Output Formats

- **agent** - Simple concatenation of markdown files
- **skill** - Agent Skills standard structure
- **power** - Kiro Power with POWER.md + steering/
- **command** - Platform-specific commands/hooks

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

## Path Conventions

- **Recipes**: Use `~/` for home directory (cross-platform)
- **Scripts**: Update absolute paths for your system
- **Targets**: Common locations:
  - `~/.kiro/` - Kiro IDE
  - `~/.claude/` - Claude Code
  - `~/.codex/` - Codex

## Working with This Codebase

### File Organization
- **Dotfolders are first-class citizens**: Always use `ls -a` or include `.*` in searches
- **Frontmatter everywhere**: Most markdown files have YAML frontmatter with metadata
- **Slice architecture**: Content marked with `<!-- slice:id -->` for modular assembly
- **Obsidian integration**: This is an Obsidian vault with Canvas files and templates

### Development Patterns
- **Fast-fail**: Enforce invariants at boundaries, fail loudly on missing capabilities
- **Deterministic**: Avoid time-based logic, prefer stable ordering
- **Data fidelity**: UNKNOWN > INVENTED - never invent data

### Context Assembly Workflow
When working with workshop recipes:
1. **Recipes** define what to assemble (in `workshop/`)
2. **assemble.py** processes recipes → `workshop/staging/`
3. **Inspect staging** before deployment
4. **sync.py** deploys staging → target locations **and auto-commits + pushes**
5. **Manifest** tracks deployments in `recipe-manifest.md`

## Common Tasks

### Finding Agent Configurations
- **Kiro**: `agents/agent-roles.md` (slice:agent=kiro)
- **Claude**: `agents/agent-roles.md` (slice:agent=claudi-claude-code)
- **Codex**: `agents/agent-roles.md` (slice:agent=gpt-codex)

### Working with Skills
- **Spec**: `skills/spec-agent-skill.md` (agentskills.io standard)
- **Examples**: Browse `skills/` directory
- **Templates**: `workshop/templates/recipe-skill-{{name}}.md`

### Working with Powers
- **Spec**: `skills/spec-kiro-power.md` (Kiro Power format)
- **Examples**: `skills/*-power/` directories
- **Templates**: `workshop/templates/recipe-power-{{name}}.md`

### Creating Recipes
1. Use Obsidian template from `workshop/templates/`
2. Configure sources, targets, output_format
3. Run `python workshop/src/assemble.py --dry-run` to preview
4. Run `python workshop/src/assemble.py` to generate staging
5. Inspect `workshop/staging/`
6. Run `python workshop/src/sync.py` to deploy

## Requirements

- Python 3.8+
- Obsidian (recommended)
- Git

## Next Steps

1. Explore `workshop/templates/` for recipe examples
2. Check `skills/spec-agent-skill.md` for skill format
3. See `skills/spec-kiro-power.md` for power format
4. Create your first recipe and run the workflow
5. See [zk-context-vault](https://github.com/SyntaxAsSpiral/zk-context-vault) for a working example
