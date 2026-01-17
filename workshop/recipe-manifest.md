---
created: 2026-01-17
id: recipe-manifest
modified: '2026-01-17T02:29:59.038521'
status: log
type:
- log
---

# Recipe Assembly Log

This manifest tracks recipe assembly and deployment operations. It is automatically updated by `assemble.py` and `sync.py`.

## Active Recipes
- **skill/mcp-builder**: Last run 2026-01-17T02:29:59.038521
  - Output: `skill\mcp-builder\`
  - Target: `~\.claude\skills\mcp-builder\`
  - Target: `~\.codex\skills\mcp-builder\`
  - Target: `~\.cursor\skills\mcp-builder\`
  - Target: `~\.gemini\skills\mcp-builder\`
  - Target: `~\.gemini\antigravity\skills\mcp-builder\`
  - Status: ✓ assembled

- **skill/catppuccin-theming**: Last run 2026-01-17T02:29:59.028239
  - Output: `skill\catppuccin-theming\`
  - Target: `~\.claude\skills\catppuccin-theming\`
  - Target: `~\.codex\skills\catppuccin-theming\`
  - Target: `~\.cursor\skills\catppuccin-theming\`
  - Target: `~\.gemini\skills\catppuccin-theming\`
  - Target: `~\.gemini\antigravity\skills\catppuccin-theming\`
  - Status: ✓ assembled

- **agent/Consensus/consensus**: Last run 2026-01-17T02:29:59.020481
  - Output: `agent\Consensus\consensus`
  - Target: `~\.dev\consensus`
  - Status: ✓ assembled

- **power/mcp-builder**: Last run 2026-01-17T02:29:59.014796
  - Output: `power\mcp-builder\`
  - Target: `~\.kiro\powers\installed\mcp-builder\`
  - Status: ✓ assembled

- **power/catppuccin-theming**: Last run 2026-01-17T02:29:59.005414
  - Output: `power\catppuccin-theming\`
  - Target: `~\.kiro\powers\installed\catppuccin-theming\`
  - Status: ✓ assembled

- **command/murder/murder**: Last run 2026-01-17T02:29:58.997481
  - Output: `command\murder\murder.md`
  - Target: `~\.claude\commands\murder.md`
  - Target: `~\.codex\prompts\murder.md`
  - Status: ✓ assembled

- **command/murder/murder.kiro**: Last run 2026-01-17T02:29:58.997481
  - Output: `command\murder\murder.kiro.hook`
  - Target: `~\.kiro\hooks\murder.kiro.hook`
  - Status: ✓ assembled

- **command/doc-consistency-check/doc-consistency-check**: Last run 2026-01-17T02:29:58.990231
  - Output: `command\doc-consistency-check\doc-consistency-check.md`
  - Target: `~\.claude\commands\doc-consistency-check.md`
  - Target: `~\.codex\prompts\doc-consistency-check.md`
  - Status: ✓ assembled

- **command/doc-consistency-check/doc-consistency-check.kiro**: Last run 2026-01-17T02:29:58.990231
  - Output: `command\doc-consistency-check\doc-consistency-check.kiro.hook`
  - Target: `~\.kiro\hooks\doc-consistency-check.kiro.hook`
  - Status: ✓ assembled

- **agent/Kiro/agent**: Last run 2026-01-17T02:29:58.982956
  - Output: `agent\Kiro\agent.md`
  - Target: `~\.kiro\steering\agent.md`
  - Status: ✓ assembled

- **agent/Kiro/operator**: Last run 2026-01-17T02:29:58.982956
  - Output: `agent\Kiro\operator.md`
  - Target: `~\.kiro\steering\operator.md`
  - Status: ✓ assembled

- **agent/Kiro/principles**: Last run 2026-01-17T02:29:58.982956
  - Output: `agent\Kiro\principles.md`
  - Target: `~\.kiro\steering\principles.md`
  - Status: ✓ assembled

- **agent/Gemini CLI/AGENTS**: Last run 2026-01-17T02:29:58.974937
  - Output: `agent\Gemini CLI\AGENTS.md`
  - Target: `~\.gemini\AGENTS.md`
  - Status: ✓ assembled

- **agent/Cursor/AGENTS**: Last run 2026-01-17T02:29:58.968570
  - Output: `agent\Cursor\AGENTS.md`
  - Target: `~\.cursor\AGENTS.md`
  - Status: ✓ assembled

- **agent/Codex/AGENTS**: Last run 2026-01-17T02:29:58.962015
  - Output: `agent\Codex\AGENTS.md`
  - Target: `~\.codex\AGENTS.md`
  - Status: ✓ assembled

- **agent/Claude/CLAUDE**: Last run 2026-01-17T02:29:58.952969
  - Output: `agent\Claude\CLAUDE.md`
  - Target: `~\.claude\CLAUDE.md`
  - Status: ✓ assembled

- **agent/Antigravity/AGENTS**: Last run 2026-01-17T02:29:58.950798
  - Output: `agent\Antigravity\AGENTS.md`
  - Target: `~\.antigravity\AGENTS.md`
  - Status: ✓ assembled


Recipes will appear here after running `python workshop/src/assemble.py`.

## Deployment Log

Deployment history will appear here after running `python workshop/src/sync.py`.