# ConSensus Project Steering

ConSensus is zk's canonical context vault at `/mnt/echo/consensus`. It holds agent steering, skills, and workshop recipes. The workshop assembles selected sources for agents and services. Treat workshop staging as generated output, not source. List the tree when you need a map. Visual models live in exeglyph at `/mnt/echo/exeglyph/artifacts/`, not in this vault.

## Working here

- Check `ls -a`, `git status`, and the relevant diff before editing. Preserve unrelated work.
- Keep changes scoped. Preserve exact names, IDs, and source provenance; use UNKNOWN rather than inventing missing details.
- Treat vault content as source and assembled files as projections. Inspect generated output before deployment.

## Workshop flow

1. Preview and assemble with `python workshop/src/assemble.py --dry-run` and `python workshop/src/assemble.py`.
2. Inspect `workshop/staging/`.
3. Preview deployment with `python workshop/src/sync.py --dry-run`. Sync one machine with `python workshop/src/sync.py --host` (adeck) or `--host nxiz`, `zrrh`, `quita`, or an address. That run purges retired paths on that host only, and it skips the manifest update and git. A full sync still purges every retired path except paths on the retired fleet node `zk@100.105.160.85`. Deploy without Git actions with `python workshop/src/sync.py --no-git`. This updates the manifest without committing or pushing.
4. To seal context, run `python workshop/src/sync.py`. It deploys, records the manifest, stages all worktree changes, commits, and pushes. Check `git status` first. Bot agent docs deploy to `/mnt/echo/exeglyph` on adeck. Sync writes them with the other local paths. It does not contact the retired fleet node.

Do not edit this document.

Source:

- `/mnt/echo/consensus/agents/steering-project-consensus.md`
