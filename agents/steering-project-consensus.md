# ConSensus Project Steering

ConSensus is ZK's canonical context vault at `/mnt/echo/consensus`. It holds source guidance, skills, prompts, and design artifacts; the workshop assembles selected sources for agents and services. Treat workshop staging as generated output, not source.

## Vault map

- `agents/` — shared and project-specific steering
- `skills/` — reusable agent capabilities
- `prompts/` — source prompts, some packaged as skills
- `artifacts/` and `exocortex/` — visual models and cognitive architecture notes
- `workshop/` — recipes, assembly, deployment, and the deployment manifest

## Working here

- Check `ls -a`, `git status`, and the relevant diff before editing. Preserve unrelated work.
- Keep changes scoped. Preserve exact names, IDs, and source provenance; use UNKNOWN rather than inventing missing details.
- Treat vault content as source and assembled files as projections. Inspect generated output before deployment.

## Workshop flow

1. Preview and assemble with `python workshop/src/assemble.py --dry-run` and `python workshop/src/assemble.py`.
2. Inspect `workshop/staging/`.
3. Preview deployment with `python workshop/src/sync.py --dry-run`; deploy without Git actions with `python workshop/src/sync.py --no-git`. This updates the manifest without committing or pushing.
4. To seal context, run `python workshop/src/sync.py`. It deploys, records the manifest, stages all worktree changes, commits, and pushes. Check `git status` first.
