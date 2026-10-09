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

Epistemic frames live in [skills/bruh](../skills/bruh/) and deploy via [recipe-skill-bruh.md](recipe-skill-bruh.md). Remaining prompt templates in `prompts/` (for example doc-consistency-check) still assemble as standalone skills; assembly strips prompt frontmatter and writes skill frontmatter into generated `SKILL.md` files.
