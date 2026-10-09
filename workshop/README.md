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

Epistemic frames live in [skills/bruh](../skills/bruh/) and deploy via [recipe-skill-bruh.md](recipe-skill-bruh.md). Documentation purge is [skills/inquisition](../skills/inquisition/) via [recipe-skill-inquisition.md](recipe-skill-inquisition.md). Adversarial structural review is [skills/praxis-taxeia](../skills/praxis-taxeia/) via [recipe-skill-praxis-taxeia.md](recipe-skill-praxis-taxeia.md). Design judgment is [skills/morphognome](../skills/morphognome/) via [recipe-skill-morphognome.md](recipe-skill-morphognome.md). Walkthroughs are [skills/consilience](../skills/consilience/) via [recipe-skill-consilience.md](recipe-skill-consilience.md). Repeated mistakes made impossible are [skills/archeoform](../skills/archeoform/) via [recipe-skill-archeoform.md](recipe-skill-archeoform.md). Triquetra evaluation is [skills/praxis-triquetra](../skills/praxis-triquetra/) via [recipe-skill-praxis-triquetra.md](recipe-skill-praxis-triquetra.md). The dev diary is [skills/dear-diary](../skills/dear-diary/) via [recipe-skill-dear-diary.md](recipe-skill-dear-diary.md). Repo rights and the house commit style are [skills/git](../skills/git/) via [recipe-skill-git.md](recipe-skill-git.md).
