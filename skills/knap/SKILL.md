---
name: knap
description: Render Markdown from templates and structured data using Knap CLI. Use when the user asks to apply a Knap template, turn JSON or CSV data into notes, batch-generate Markdown files, format Defuddle output into a note, or render a review document from selected JSONL records.
---

# Knap

Use Knap CLI to render Markdown templates with variables, filters, and logic.

If not installed: `npm install -g knap` (requires Node.js 20 or later). Alternatively, use `npx knap`.

Run `knap --help` for available commands and options. Discover the language through the CLI's offline reference:

```bash
knap help syntax
knap help filters
knap help filter date
knap help tags
knap help tag for
```

Use the lists to find names, then request individual help for syntax, parameters, and examples with expected output.

## Usage

Render a template with JSON variables:

```bash
knap render template.md --data article.json -o note.md
```

Supply a template and data inline:

```bash
knap render -t '# {{ title | trim }}' --data-json '{"title":"Hello"}'
```

Override a variable or pipe JSON data:

```bash
knap render template.md --data article.json --set 'title=Custom title'
cat article.json | knap render template.md --data -
```

Data must be a JSON object; its properties become template variables. `--set` overrides literal top-level keys with strings. Use JSON for nested objects, arrays, numbers, and booleans.

Choose one template source (file, `-t`, or stdin) and one data source (`--data` or `--data-json`). Only one input can read stdin. Without a template file or `-t`, Knap reads the template from stdin.

Output defaults to stdout. `-o` creates parent directories and overwrites the destination after rendering succeeds. Errors exit with status `1`; diagnostics go to stderr. Warnings can accompany successful output.

## Templates

Use `{{ variable }}` for values, `|` for filters, and `{% ... %}` for logic. For example, save this as `template.md`:

```knap
---
{{ title | yaml_property:"title" }}
{{ tags | yaml_property:"tags" }}
---
# {{ title | trim }}
{% if author %}
By {{ author }}
{% endif %}

{{ content }}
```

Use `yaml_property` for complete frontmatter properties so values are quoted and indented correctly. The CLI includes standard filters, but does not supply Web Clipper browser variables, selectors, prompts, or DOM-dependent HTML filters. Supply variables through JSON.

Check a template before rendering:

```bash
knap validate template.md
```

Validation checks syntax, filter names, and static filter arguments without data or file output. It does not check variable existence, runtime values, or dynamic arguments; render with real data to check runtime behavior. Diagnostics go to stderr and include relevant help commands.

## Defuddle pipeline

Extract a web page as JSON with Markdown content, then render it into a note:

```bash
defuddle parse https://example.com/article --md --json \
  | knap render template.md --data - -o note.md
```

Defuddle's JSON properties, such as `title` and `content`, become template variables directly.

## Batch rendering

Create one file per CSV row, JSON array object, or JSON file in a folder:

```bash
knap batch template.md --data articles.csv --output-dir notes \
  --filename '{{ title | safe_name }}.md'
```

Use `--data articles.json` for an array or `--data ./articles` for a folder of JSON objects. CSV headers become variable names and values remain strings. Piped data defaults to JSON; add `--format csv` for piped CSV.

Use `--dry-run` to validate and list output paths without writing files. Existing files require `--overwrite`, including during a dry run. Duplicate output names within a batch are errors even with `--overwrite`.

Filename templates must produce a single filename with its extension, without directories. Use `safe_name` for data-derived names. Without `--filename`, Knap preserves source JSON basenames or numbers CSV rows and array items as `1.md`, `2.md`, and so on.

## JSONL review documents

Esocortex renders one review from selected JSONL records. The JSONL stays authoritative. The review is a disposable projection. Preserve `augment_output` in failure reviews.

`examples/review.sh` selects with jq, builds one JSON object, and renders `examples/review-template.md`. In the esocortex repo those files live at `knap/review.sh` and `knap/review-template.md`, and the script writes `docs/review/<chronohex>-<label>`. `--output` is a filename label, not a path. Chronohex is the last six hex digits of `time.time_ns()`. The renderer is pinned at `knap@0.6.0`.

```bash
knap/review.sh \
  --select '.augment_error != null' \
  --title 'ISTA augmentation errors' \
  --output ista-augmentation-errors.md \
  data/aug/*.jsonl
```

The template walks `entries` with `{% for entry in entries %}`, optional metadata rows, a warning callout for `augment_error`, and `blockquote` / `list` filters for model text and key names.

If `npx` cannot reach the registry, find the cached `knap@0.6.0` `package.json` under `~/.npm/_npx/` and run its `dist/cli.js` with `node` against the same template and selection data. Keep Knap as the renderer.
