# Upstream

Reference checkouts of third-party skill repos. Assembly copies from these into deployed skills, and `workshop/src/assemble.py` fast-forwards each one (`git pull --ff-only`) before it runs. The checkouts themselves are not published with this vault, only this index.

| Directory | Upstream | What it is |
|---|---|---|
| `agents-best-practices/` | [DenisSergeevitch/agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices) | Provider-neutral Agent Skill for Codex, Claude Code, and agentic harness design. |
| `agentskills/` | [agentskills/agentskills](https://github.com/agentskills/agentskills) | Specification and documentation for Agent Skills. |
| `agent-skills-for-context-engineering/` | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) | Agent Skills for context engineering, multi-agent architectures, and production agent systems. |
| `claude-plugins-official/` | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Anthropic-managed directory of Claude Code plugins. |
| `hue-skill/` | [nikilster/hue-skill](https://github.com/nikilster/hue-skill) | Control Philips Hue lights locally via the bridge API. |
| `nix-skills/` | [olafkfreund/nix-skills](https://github.com/olafkfreund/nix-skills) | Reusable agent skills for the Nix language, grounded in the upstream Nix manual. |
| `nixarchy/` | [olafkfreund/nixarchy](https://github.com/olafkfreund/nixarchy) | NixOS agent skills, imported per skill from `pkgs/omarchy/skills/`. Each skill's `SOURCE.md` records the upstream commit. Copied without git history, so it is not auto-pulled. |
| `obsidian-skills/` | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Agent skills for Obsidian: CLI, Markdown, Bases, and JSON Canvas. |

Each upstream keeps its own license. Check the checkout before redistributing anything from it.
