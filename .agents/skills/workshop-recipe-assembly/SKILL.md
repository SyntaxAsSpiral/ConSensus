---
name: workshop-recipe-assembly
description: Create, inspect, assemble, and deploy context recipes in the ConSensus workshop. Use when editing workshop recipes, source slices, assembly behavior, staged agent files or skills, deployment targets, or the recipe manifest.
---

# Recipe Assembly

The ConSensus workshop assembles agent guidance and skills from vault sources, stages generated artifacts, and optionally deploys them to configured targets. Recipes are Markdown files with Obsidian frontmatter and a fenced YAML configuration block.

## Workshop layout

| Resource | Location |
|---|---|
| Active recipes | `workshop/recipe-*.md` |
| Recipe templates | `workshop/templates/` |
| Assembly script | `workshop/src/assemble.py` |
| Deployment script | `workshop/src/sync.py` |
| Generated staging tree | `workshop/staging/` |
| Deployment manifest | `workshop/manifest-recipes.md` |

Active recipe discovery is non-recursive: only `recipe-*.md` directly under `workshop/` are processed. Templates and archived recipes are not active recipes.

## Recipe file format

Obsidian frontmatter describes the note; the first fenced `yaml` block in the body is the configuration the scripts parse:

````markdown
---
id: recipe-agent-example
status: active
type:
  - agent
---

```yaml
name: Example
output_format: agent
target_locations:
  - path: ~/.config/example/AGENTS.md
sources:
  - slice: agent=example
    slice-file: agents/agent-roles.md
  - file: agents/steering-global-principles.md
```
````

The recipe filename is conventionally `recipe-<name>.md`. The configuration's `name` determines the staging subdirectory and is not inferred from the Obsidian `id`.

### Configuration keys

| Key | Use |
|---|---|
| `name` | Output name and staging directory. |
| `output_format` | Selects the artifact type: `agent`, `project`, `skill`, `project-skill`, `command`, `prompt`, or `hook`. If omitted, assembly defaults to `agent`. |
| `target_locations` | Deployment destinations as path strings or mappings with a `path` key. Entries starting with `fleet:` belong to the fleet runner; see [Fleet targets](#fleet-targets). |
| `sources` | Source list for agent/project output; role mapping for skill and command-like output. |
| `template` | Optional literal `{content}` wrapper for agent/project or command-like output. |
| `output_name` | Optional explicit filename for agent/project output. |
| `validate_agentskills_spec` | Enables the assembler's limited skill-name/description checks. |

Recipes may contain multiple YAML documents separated by `---` inside the fenced block. Each document becomes a section. Only `name` and `output_format` are inherited from the first document; other keys must be repeated where needed.

### Fleet targets

A `target_locations` entry whose raw path starts with `fleet:` (plain string or `path:` value) is owned by the fleet runner on the shared fleet PC, not by adeck. Everything after the prefix is the literal path on that PC:

```yaml
target_locations:
  - path: ~/.agents/skills/example-skill/
  - path: fleet:/workspace/shared/skills/example-skill/
```

`assemble.py` and `sync.py` drop these entries before path expansion, so adeck never deploys them or purges them. A skill recipe that has one also gets a copy at `workshop/staging/skill/fleet/<name>/` for the fleet wrapper. That copy is recorded with no deploy targets. Fleet entries are ignored when an agent/project filename is inferred from a single target; set `output_name` to be explicit. Every other target is handled as before. The two scripts keep separate copies of the check (`_location_is_fleet`), so change both together.

A recipe with `target_locations: []`, or only `fleet:` targets, is assembled into staging and not deployed by adeck. The fleet runner is a separate modified copy of the assembler on the fleet PC and is not part of this repository's scripts.

## Source forms and slices

For agent/project and command-like source lists, each entry can use one of these forms:

```yaml
sources:
  - inline: "Short literal content"
  - file: agents/steering-global-principles.md
  - slice: agent=example
    slice-file: agents/agent-roles.md
```

Use one source form per entry. Whole-file Markdown inclusion strips leading YAML frontmatter. Slice markers are exact HTML comments:

```markdown
<!-- slice:agent=example -->
Content to include
<!-- /slice -->
```

The `slice` value must exactly match the start marker, including any prefix such as `agent=`. Extraction ends at the first `<!-- /slice -->` or the next `<!-- slice:` marker, whichever comes first. A closing marker is optional if the next slice or end of file bounds the content, but add one after the last slice of a group that is followed by a heading or other prose; otherwise that text is captured too. Slices are not nested or parsed as a structured language.

Missing source files or slice markers are reported and skipped; they do **not** reliably stop the build. If at least one source succeeds, the result may contain partial content. If a recipe produces no artifacts, assembly logs a failure for that recipe but may still exit successfully overall. Review the output and logs rather than treating exit status alone as proof that every recipe assembled correctly.

## Output formats

### Agent and project

`agent` and `project` recipes use a list of sources and stage one Markdown file per section:

- Agents: `workshop/staging/agent/<name>/<filename>`
- Projects: `workshop/staging/project/<name>/<filename>`

For example, the project recipe stages the repository guidance used by this vault. A target ending in `/` is treated as a directory: the assembler chooses `CLAUDE.md` for paths under `.claude`, otherwise `AGENTS.md`. A target without a trailing slash is treated as a file path. Use `output_name` when a specific staged filename is required independent of the target.

If `template` contains the literal `{content}`, it is replaced with assembled source text. If it does not, the template text is prepended to the assembled sources. This is literal replacement, not Python formatting or general variable interpolation.

### Skills

`skill` recipes use a mapping of source roles and stage a directory at `workshop/staging/skill/global/<name>/`. The `skill_md` role defines generated frontmatter and body sources:

```yaml
name: example-skill
output_format: skill
target_locations:
  - path: ~/.agents/skills/example-skill/
sources:
  skill_md:
    frontmatter:
      name: example-skill
      description: Describe the capability and when to use it.
    body:
      - file: skills/example-skill/SKILL.md
  references:
    - file: skills/example-skill/REFERENCE.md
      output_name: REFERENCE.md
  scripts:
    - file: skills/example-skill/check.py
      output_name: check.py
  examples:
    - file: skills/example-skill/example.json
      output_name: example.json
validate_agentskills_spec: true
```

Supported optional directory roles are `references`, `assets`, `scripts`, and `examples`. Each item may use `inline`, `file`, or `slice` plus `slice-file`; `output_name` sets its destination name and may include subdirectories. The skill body uses whole-file/slice source handling and strips leading frontmatter; role files are copied as bytes.

The current `validate_agentskills_spec` implementation only checks a basic lowercase/digit/hyphen name pattern and the description's maximum length. It does not enforce every Agent Skills specification rule, so validate generated skills against the full specification when compliance matters.

### Project skills

`project-skill` uses the same source mapping and tree copy as `skill`, and stages at `workshop/staging/skill/project/<name>/`. It does not deploy to `~/.agents/skills/` or `~/.claude/skills/`.

Each target is a project root or that project's `.agents/` directory, including an SSH path such as `zk@100.77.90.79:~/.config/OpenRGB/.agents/`. Assembly and sync resolve it to `<project>/.agents/skills/<name>/` and keep a remote `~/` unexpanded. A target under a home agent directory (`~/.agents`, `~/.claude`, `~/.codex`, and the other home agent dirs) is refused. Home-wide skills stay on `output_format: skill`.

```yaml
name: example-skill
output_format: project-skill
target_locations:
  - path: /mnt/echo/example/.agents/
sources:
  tree: skills/upstream/example/skills/example-skill
```

### Command-like formats

`command`, `prompt`, and `hook` formats stage a Markdown file under `workshop/staging/command/<name>/<name>.md`. Their `sources` mapping accepts `command_md` or `prompt_md`, each a list of source entries. These formats share the command output path and deployment handling; check the consuming tool's expected layout before adding a recipe.

## Assembly and deployment workflow

Run commands from the repository root:

```bash
python workshop/src/assemble.py --dry-run
python workshop/src/assemble.py
```

Before assembling, `assemble.py` fast-forwards (`git pull --ff-only`) every git checkout under `skills/upstream/` and `.agents/upstream/`; a failed pull stops the run. A dry run only reports what it would pull.

The dry run reports prospective output paths without writing staging files or updating the manifest. A real assembly **deletes and recreates `workshop/staging/`** before producing current artifacts, then refreshes the active recipe entries in `workshop/manifest-recipes.md`. An existing `workshop/staging/.previous-manifest.md` is kept across that wipe until sync consumes it. Treat staging as generated output; do not keep source material there.

Inspect `workshop/staging/` and the assembly logs before deploying. Then preview and choose the appropriate sync mode:

```bash
python workshop/src/sync.py --dry-run
python workshop/src/sync.py --no-git
```

Sync deploys staged artifacts to local or SSH targets. Skill directories are mirrored, so extra files already present at a skill target can be removed. Sync removes targets listed in `workshop/staging/.previous-manifest.md` that the current recipes no longer use. Assemble keeps that file across later assembles until a purge finishes with every retired path removed or already gone. A failed purge leaves the file in place. Do not delete it to retry a cleanup.

`--dry-run` does not copy file contents, update the manifest, or commit. For local file targets, the current sync code may still create missing parent directories during a dry run. `--no-git` performs deployment and updates the manifest but skips Git automation. Without either option, sync deploys, updates the manifest, then runs `git add -A`, commits, and pushes the current branch. Check `git status` first; use `--no-git` when deployment is intended but those repository-wide Git effects are not.

See [the workshop README](../../../workshop/README.md), [assembler](../../../workshop/src/assemble.py), and [sync script](../../../workshop/src/sync.py) for the current workflow and implementation details.

## Practical checks

Before assembly:

- Confirm the recipe is directly in `workshop/` and its YAML block parses.
- Confirm each source path and slice marker exists; ensure a failed source will not leave unintended partial output.
- Check target paths carefully, especially trailing slashes and multi-section recipes.
- For skills, inspect generated `SKILL.md` frontmatter and verify all expected role files appear in staging.

Before sync:

- Review all staged content and targets, including any SSH destinations.
- Run sync with `--dry-run` and inspect proposed copies and orphan removals.
- Check the manifest and `git status`; use `--no-git` unless automatic commit and push are explicitly intended.

## Troubleshooting

| Symptom | What to check |
|---|---|
| Slice reported missing | The marker must exactly match `<!-- slice:<value> -->`; confirm the recipe uses `slice-file`, not `file`, for slice sources. |
| Output is incomplete | Missing files/slices are skipped. Read assembly logs and inspect every staged artifact. |
| Template text is not substituted | Only literal `{content}` is replaced; other placeholders remain unchanged. |
| Agent filename differs from expectation | Directory targets must end in `/`; otherwise the path is treated as a file. Use `output_name` to choose the staged filename explicitly. |
| Old target was not cleaned up | `workshop/staging/.previous-manifest.md` must still list the path. Sync deletes that file only after every retired path is removed or already gone. |
| Skill target has unexpected files removed | Skill deployment mirrors the staged directory, deleting target-side files not present in staging. |
| Unexpected Git changes or push | Normal sync runs `git add -A`, commits, and pushes. Use `--no-git` for deployment without Git automation. |

## Related skills

- [Agent steering](../../../skills/archive/agent-steering/SKILL.md) — archived role/slice conventions
- [Covenant patterns](../../../skills/archive/covenant-patterns/SKILL.md) — archived workshop principles
