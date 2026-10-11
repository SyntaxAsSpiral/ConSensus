# Workshop

Recipes in `workshop/recipe-*.md` assemble agent files and skills from sources in this vault. The scripts use `/mnt/echo/consensus` as their source root. `output_format: skill` deploys a vault skill to the house agent directories and to `fleet:/home/box/agent-data/workflows/<name>/`. A project-local skill keeps only the targets in its recipe. OpenRGB is the zrrh checkout. Knap is the esocortex project. The other deployed upstream skills use the house paths and `fleet:/home/box/agent-data/workflows/<name>/`.

```bash
python workshop/src/assemble.py --dry-run
python workshop/src/assemble.py
```

Assembly replaces `workshop/staging/` and refreshes the active entries in `workshop/manifest-recipes.md`. Inspect the staged files before deployment.

```bash
python workshop/src/sync.py --dry-run
python workshop/src/sync.py --host
python workshop/src/sync.py
```

`--host` syncs copies to one machine. With no name it means adeck, the paths on this computer. `--host nxiz`, `zrrh`, `quita`, or an address retries that host. A single-host run deletes retired paths on that host only, and it skips manifest updates and git. The snapshot stays, so a later full sync still purges every retired path, including ones the one-host run already deleted. An unreachable host fails in about ten seconds, and later targets for that host are skipped. A full sync deploys staged files, removes targets orphaned by recipe changes, then runs `git add -A`, commits, and pushes. Use the full sync only when those effects are intended. A full sync that hits a failed host does not commit or push. `fleet:` paths are assembled on the fleet PC. Sync does not rsync or purge them.

## Under construction

These vault skills have no recipe yet. Symlinked nix-os skills (`nixos-fleet`, `nixos-secrets`, `zcli`) and `skills/upstream` are not on this list.

- [cli-coding](../skills/cli-coding/)
- [praxis-archeoform](../skills/praxis-archeoform/)
- [praxis-harmonion](../skills/praxis-harmonion/)
- [praxis-morphognome](../skills/praxis-morphognome/)
- [praxis-taxeia](../skills/praxis-taxeia/)
- [praxis-triquetra](../skills/praxis-triquetra/)

## Upstream

Reference checkouts of third-party skill repos. Assembly copies from these into deployed skills, and `workshop/src/assemble.py` fast-forwards each one (`git pull --ff-only`) before it runs. A pull that does not finish within 30 seconds is killed, and assembly continues with that checkout as it stands. A pull that fails outright still stops the run. The checkouts themselves are not published with this vault, only this index.

| Directory | Upstream | What it is |
|---|---|---|
| `agents-best-practices/` | [DenisSergeevitch/agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices) | Provider-neutral Agent Skill for Codex, Claude Code, and agentic harness design. |
| `agentskills/` | [agentskills/agentskills](https://github.com/agentskills/agentskills) | Specification and documentation for Agent Skills. |
| `claude-plugins-official/` | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Anthropic-managed directory of Claude Code plugins. |
| `cursor-plugins/` | [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack/skills) | Cursor pstack skills. Sparse checkout of `pstack/skills`. |
| `hue-skill/` | [nikilster/hue-skill](https://github.com/nikilster/hue-skill) | Control Philips Hue lights locally via the bridge API. |
| `nix-skills/` | [olafkfreund/nix-skills](https://github.com/olafkfreund/nix-skills) | Reusable agent skills for the Nix language, grounded in the upstream Nix manual. |
| `nixarchy/` | [olafkfreund/nixarchy](https://github.com/olafkfreund/nixarchy) | NixOS agent skills, imported per skill from `pkgs/omarchy/skills/`. Each skill's `SOURCE.md` records the upstream commit. Copied without git history, so it is not auto-pulled. |
| `obsidian-skills/` | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Agent skills for Obsidian: CLI, Markdown, Bases, and JSON Canvas. |

### Deployed

Assembly copies only these. The recipe is `workshop/recipe-skill-<name>.md`. A checkout with no row is not deployed.

| Skill | Path |
|---|---|
| `agents-best-practices` | `agents-best-practices` |
| `build-mcp-app` | `claude-plugins-official/plugins/mcp-server-dev/skills/build-mcp-app` |
| `build-mcp-server` | `claude-plugins-official/plugins/mcp-server-dev/skills/build-mcp-server` |
| `build-mcpb` | `claude-plugins-official/plugins/mcp-server-dev/skills/build-mcpb` |
| `hue` | `hue-skill` |
| `devenv-project` | `nix-skills/skills/devenv-project` |
| `nix-language` | `nix-skills/skills/nix-language` |
| `nixos-wiki` | `nix-skills/skills/nixos-wiki` |
| `nixpkgs-development` | `nix-skills/skills/nixpkgs-development` |
| `knap` | `obsidian-skills/skills/knap` |

Each upstream keeps its own license. Check the checkout before redistributing anything from it.
