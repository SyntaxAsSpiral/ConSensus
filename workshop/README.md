# Workshop

Recipes in `workshop/recipe-*.md` assemble agent files and skills from sources in this vault. The scripts use `/mnt/echo/consensus` as their source root. `output_format: skill` deploys to home agent directories. `output_format: project-skill` deploys only under a project's `.agents/skills/`.

```bash
python workshop/src/assemble.py --dry-run
python workshop/src/assemble.py
```

Assembly replaces `workshop/staging/` and refreshes the active entries in `workshop/manifest-recipes.md`. Inspect the staged files before deployment.

```bash
python workshop/src/sync.py --dry-run
python workshop/src/sync.py
```

Sync deploys staged files, removes targets orphaned by recipe changes, then runs `git add -A`, commits, and pushes. Use it only when those effects are intended.

Prompt pseudo-skills use `output_format: skill` recipes such as [recipe-skill-bedtime.md](recipe-skill-bedtime.md). Their source text stays in `prompts/`; assembly strips its prompt frontmatter and writes the skill frontmatter into generated `SKILL.md` files.
