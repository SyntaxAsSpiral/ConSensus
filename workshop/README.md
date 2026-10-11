# Workshop

Recipes in `workshop/recipe-*.md` assemble agent files and skills from sources in this vault. The scripts use `/mnt/echo/consensus` as their source root. `output_format: skill` deploys to home agent directories. `output_format: project-skill` deploys only under a project's `.agents/skills/`.

```bash
python workshop/src/assemble.py --dry-run
python workshop/src/assemble.py
```

Assembly replaces `workshop/staging/` and refreshes the active entries in `workshop/manifest-recipes.md`. Inspect the staged files before deployment.

```bash
python workshop/src/sync.py --dry-run
python workshop/src/sync.py --host
python workshop/src/sync.py --host fleet
python workshop/src/sync.py
```

`--host` syncs copies to one machine. With no name it means adeck, the paths on this computer. `--host fleet` (or `nxiz`, `zrrh`, `quita`, or an address) retries that host. A single-host run deletes retired paths on that host only, and it skips manifest updates and git. The snapshot stays, so a later full sync still purges every retired path, including ones the one-host run already deleted. An unreachable host fails in about ten seconds, and later targets for that host are skipped. A full sync deploys staged files, removes targets orphaned by recipe changes, then runs `git add -A`, commits, and pushes. Use the full sync only when those effects are intended. A full sync that hits a failed host does not commit or push.

Epistemic frames live in [skills/bruh](../skills/bruh/) and deploy via [recipe-skill-bruh.md](recipe-skill-bruh.md). Documentation purge is [skills/inquisition](../skills/inquisition/) via [recipe-skill-inquisition.md](recipe-skill-inquisition.md). The dev diary is [skills/rhapsody](../skills/rhapsody/) via [recipe-skill-rhapsody.md](recipe-skill-rhapsody.md). Mesh operations are [skills/mesh-ops](../skills/mesh-ops/) via [recipe-skill-mesh-ops.md](recipe-skill-mesh-ops.md). Commit style is [skills/commit-style](../skills/commit-style/) via [recipe-skill-commit-style.md](recipe-skill-commit-style.md). The corpus API is [skills/esocortex](../skills/esocortex/) via [recipe-skill-esocortex.md](recipe-skill-esocortex.md). praxis-archeoform, praxis-harmonion, praxis-morphognome, praxis-taxeia, praxis-triquetra, and cli-coding are still in development and have no recipes.
