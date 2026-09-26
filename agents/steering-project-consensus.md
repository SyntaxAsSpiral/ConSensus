# AGENTS.md

> **For AI Coding Agents**: This document explains the Amexsomnemon repository structure, purpose, and how to work effectively within this codebase.

## Repository Overview

**ConSensus** is ZK's personal context vault and agent configuration library—an Obsidian-based system for AI agent configuration, context management, and cognitive workflow design. It is part of the broader Amexsomnemon exocortex project.

**Note**: While this vault contains ZK's specific content and configurations, the **workshop system** (`workshop/src/`, templates, and recipe patterns) is designed to be reusable. The recipes demonstrate assembly and deployment patterns that can be adapted to any content library.

## Project Sigils

These sigils are project-local overlays for ConSensus. They tune the agent's posture without replacing the global identity stack in `agents/agent-roles.md`.

Global sigils especially resonant with this project:

- 🧭 Holographic Lodestone
- 🌀 Helical Refractor

- 🍥 Recursive Workshop Custodian
- 🗂️ Slice Archivist
- 🪡 Context Seamstress
- 🧪 Assembly Hermeticist

This vault contains:

- **Agent configurations** for multiple AI coding platforms (Claude, Codex, Gemini, Grok, Pi)
- **Steering rules** that guide agent behavior following Covenant Principles
- **Skills** packaged for distribution across platforms
- **Context workshop** for recipe-based assembly of documentation
- **Specs** for structured development workflows
- **Prompts and artifacts** for specialized cognitive tasks

## Key Directories

### `/agents/` - Agent System Architecture
**Purpose**: Universal agent configuration patterns that work across platforms

**Key files:**
- `agent-roles.md` - Identity templates and role sigils for different agents
- `steering-global-operator.md` - Operator (ZK) profile and preferences
- `steering-global-principles.md` - Covenant Principles (anti-assumption framework)
- `steering-global-mesh.md` - Tailnet device topology and SSH configuration
- `steering-project-consensus.md` - ConSensus project steering example; other projects keep their own steering locally

**When to reference**: Understanding agent identity, behavior constraints, or platform-specific features

### `/skills/` - Agent Skills Library
**Purpose**: Reusable capabilities packaged in Agent Skills standard format

**Structure**: Each skill follows the Agent Skills specification in `skills/spec-agent-skill.md`.
```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed docs
└── assets/           # Optional: static resources
```

**Key skills:**
- `catppuccin-theming` - Color palette management
- `semantic-json-workflows` - Canvas-to-structured-data compilation
- `agent-steering` - Steering system documentation
- `context-degradation` - Context quality monitoring

**When to reference**: Need specific capabilities or examples of skill packaging

### `/workshop/` - Context Assembly System
**Purpose**: Recipe-based system for assembling and deploying context documentation

**Reusability**: The workshop system (scripts, templates, recipe patterns) is designed to be reusable with any content. Clone and adapt to your own context library by:
- Replacing vault-specific absolute paths in scripts and recipes with your vault path
- Creating your own content in `agents/`, `skills/`, etc.
- Using the recipe templates to define your own assembly patterns

**Key components:**
- `templates/` - Recipe scaffolding for agents and skills (reusable)
- `recipe-*.md` - Active recipes for content assembly (ZK-specific examples)
- `src/assemble.py` - Assembly script (reusable, update paths)
- `src/sync.py` - Deployment script (reusable, update paths)
- `manifest-recipes.md` - Deployment tracking log

**Output formats:**
- **Agent Skills** (`SKILL.md` + optional references/)
- **Simple agents** (concatenated markdown)

**When to reference**: Understanding how context is assembled or deployed, or adapting the system for your own content

### `/exocortex/` - Cognitive Architecture
**Purpose**: Multi-agent coordination patterns and exocortex design

**Key files:**
- `exo-praxis-*.md` - Operational patterns (antibody, council, gnomon, hygiene, mutation, triquetra)
- `exo-roles.md` - Agent specializations and coordination
- `exo-tools.md` - Tool ecosystem and integration
- `exo-topography.md` - System landscape and boundaries

**When to reference**: Multi-agent systems or distributed cognition patterns

### `/prompts/` - Specialized Cognitive Modes
**Purpose**: Prompt templates for different thinking styles

**Examples:**
- `dialectic.md` - Socratic dialogue
- `hpmor.md` - Rationalist analysis
- `reflect.md` - Metacognitive reflection
- `murder.md` - Adversarial red-teaming

**When to reference**: Need specific cognitive approach or prompt engineering examples

### `/artifacts/` - Visual Models and Examples
**Purpose**: Canvas files and golden examples

**Key artifacts:**
- `golden/` - Reference implementations and examples
- `*.canvas` - Obsidian Canvas visual models

**When to reference**: Visual system design or example implementations

## Covenant Principles (Anti-Assumption Framework)

**Critical**: This codebase follows strict anti-assumption principles. Every yama (constraint) guards against a specific assumption:

| Principle | The Assumption It Guards Against |
|-----------|----------------------------------|
| 👁️ Dotfile Visibility | "dot = hidden" |
| ✨ Bespokedness | "scale matters, best practices apply" |
| ⚡ Fast-Fail Enforcement | "invariants are enforced somewhere" |
| 🧷 Decision Integrity | "operator wants sub-decisions" |
| 🚮 Final-State Surgery | "operator wants transition period" |
| ⛔ Work Preservation | "this change is out of scope" |
| 🗡️ Git Semantics | "operator wants curation" |
| 🧊 Protected Paths | "this needs fixing" |
| 🗣️ Data Fidelity | "I know what this value should be" |
| 🔤 Literal Exactness | "paraphrase is equivalent" |
| 🔒 Threshold-Gated Action | "I have implicit authorization" |
| 🔁 Determinism | "time context is stable" |
| 🧬 Context Hygiene | "recipient needs everything" |

**Key niyamas (practices):**
- Use `ls -a` for directory reconnaissance (dotfolders are organizational)
- Prefer bespoke solutions over frameworks when software is disposable
- UNKNOWN > INVENTED (never invent data)
- Final-state surgery: remove old world entirely unless transition explicitly requested
- Never discard work without explicit instruction

See `agents/steering-global-principles.md` for complete details.

## Operator Profile (ZK)

**Identity**: Zach Battin (ZK::🜏🜃🜔 // Æmexsomnus // 🍥)
**Environment**: NixOS 26.05 (Yarara) + nushell (primary), Docker available
**Favorite Font**: Recursive Mono Casual

**Role Sigils:**
- 🌸 Autognostic Infloresencer · 🪢 Logopolysemic Weaver
- 💨 Pneumastructural Intuitive · 🛸 Ritotechnic Liminalist
- 🧩 Syntactic Delver · 🗺️ Mythic Tactician
- ♓︎ Syzygetic Machinator · ⚗️ Alchemical Lexemancer
- 🧬 Mnemonic Emanator · 🛏️ Oneiric Pedagogue

**Current Projects:**
- Semanti-JSON - Obsidian plugin for Canvas data recompiling
- Collectivist - AI-powered curation for intentional collections
- Amexsomnemon - Overarching exocortex project (this vault is part of it)

See `agents/steering-global-operator.md` for complete profile.

## Working with This Codebase

### File Organization
- **Dotfolders are first-class citizens**: Always use `ls -a` or include `.*` in searches
- **Frontmatter everywhere**: Most markdown files have YAML frontmatter with metadata
- **Slice architecture**: Content marked with `<!-- slice:id -->` for modular assembly
- **Obsidian integration**: This is an Obsidian vault with Canvas files and templates

### Path Conventions
- **Context library**: `/mnt/echo/consensus` (absolute path for workshop scripts)
- **Scripts**: `workshop/src/` (in-repo scripts)
- **Workspace**: Relative paths from repo root
- **Home directory**: `~/` expands to user home in recipes

### Development Patterns
- **Bespoke over enterprise**: Optimize for operator workflow, not imaginary scale
- **Disposable software**: When rewrite < refactor, optimize for beauty and function
- **Fast-fail**: Enforce invariants at boundaries, fail loudly on missing capabilities
- **Deterministic**: Avoid time-based logic, prefer stable ordering

### Spec-Driven Development
When working on features with specs:
1. **Read requirements.md** - Understand acceptance criteria
2. **Read design.md** - Understand architecture and approach
3. **Read tasks.md** - Follow implementation plan
4. **Execute one task at a time** - Don't jump ahead
5. **Update task status** - Mark in_progress → completed

### Context Assembly Workflow
When working with workshop recipes:
1. **Recipes** define what to assemble (in `workshop/`)
2. **assemble.py** processes recipes → `workshop/staging/`
3. **Inspect staging** before deployment
4. **sync.py** deploys staging → target locations **and auto-commits + pushes**
5. **Manifest** tracks deployments in `manifest-recipes.md`
6. Git commit: `🔗 Context Sealed ⟳ {chronohex}` - all in one atomic workflow

**Never commit manually** - the sync workflow owns all context artifact commits.

## Common Tasks

### Finding Agent Configurations
- **Claude**: `agents/agent-roles.md` (slice:agent=claudi-claude-code)
- **Codex**: `agents/agent-roles.md` (slice:agent=gpt-codex)
- **Gemini**: `agents/agent-roles.md` (slice:agent=gemini-cli)
- **Grok**: `agents/agent-roles.md` (slice:agent=grok)
- **Pi**: `agents/agent-roles.md` (slice:agent=pi)

### Understanding Steering Rules
- **Global principles**: `agents/steering-global-principles.md`
- **Operator profile**: `agents/steering-global-operator.md`
- **Mesh topology**: `agents/steering-global-mesh.md`

### Working with Skills
- **Spec**: `skills/spec-agent-skill.md` (agentskills.io standard)
- **Examples**: Browse `skills/` directory
- **Templates**: `workshop/templates/recipe-skill-{{name}}.md`

### Creating Recipes
1. Use Obsidian template from `workshop/templates/`
2. Configure sources, targets, output_format
3. Run `python workshop/src/assemble.py --dry-run` to preview
4. Run `python workshop/src/assemble.py` to generate staging
5. Inspect `workshop/staging/`
6. Run `python workshop/src/sync.py` to deploy

### Grok Harness Integration
- **Project rules**: Root `AGENTS.md` (this file after assembly) + any subdir `AGENTS.md` are auto-loaded by Grok for every session in the vault. Deeper = higher precedence.
- **Global steering**: `workshop/recipe-agent-grok.md` deploys `~/.grok/AGENTS.md` on adeck and quita.
- **Skills**: Workshop recipes deploy selected skills to `~/.agents/skills/`.
- **Inspection**: `grok inspect` shows exactly which rules, skills, and agents are active in the current session.

## Important Constraints

### Git Semantics
- **Commits only through `sync.py`** - Auto-commits with chronohex timestamp (`🔗 Context Sealed ⟳ {chronohex}`)
- No manual commits, amending, reordering, or curating
- All context artifact deployments are captured in a single commit via sync workflow

### Data Fidelity
- UNKNOWN > INVENTED
- Never invent model fields, IDs, tool results, or "expected" outputs
- Missing info = ask or query

### Literal Exactness
- No paraphrasing at interfaces (commands, paths, IDs, tool names)
- Copy verbatim or fail loudly

---

**Remember**: This is ZK's bespoke vault, but the workshop system is designed for reuse. Assumption-hostile, work-preserving, deterministic. When in doubt, ask rather than assume.

*The recursion is the craft.* 🍥
