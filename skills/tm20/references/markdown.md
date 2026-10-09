# Markdown

A strict printable subset of CommonMark and GFM, not a browser. Unsupported constructs, missing glyphs, and clipped content fail.

## Design

- One short `#` masthead, then context, substance, conclusion. `##` marks sections. H3–H6 do not get smaller.
- Short paragraphs and concrete labels. Keep the necessary detail. Move sources into notes.
- Bold for key facts, italic for secondary emphasis, monospace for literals. No walls of bold, all-caps paragraphs, decorative emoji, ASCII boxes, or space-padded columns.
- Two-column tables for label/value pairs and prices. Three columns only when the data is compact. Wide records become stacked labeled paragraphs.
- A rule before a total or a major transition, not between every paragraph. One blank line between blocks.
- Receipts run masthead, context, items, total. Reading tapes use short sections. A checklist is one concrete action per task.

## Constructs

| Construct | Rendering | Authoring constraints |
| --- | --- | --- |
| Paragraphs | 11 pt sans; word wrapping, no hyphenation | Avoid long unbroken strings. Source soft breaks become spaces; use a trailing backslash or two spaces for a hard break. |
| Headings | H1: 18 pt; H2–H6: 11 pt bold | Nonempty plain text only: no emphasis, code, links, images, or math. Prefer ATX `#` syntax. |
| Inline styles | `*italic*`, `**bold**`, combinations, `~~strike~~` | Styles can nest; strikethrough spans wrapped lines. Keep them out of headings. |
| Code spans | Monospace; whitespace normalized | For short literals, not manual alignment. Fitting spans stay unbroken. |
| Code blocks | Fenced or indented monospace | No highlighting or wrapping. Split long lines explicitly; indentation consumes width. |
| Lists | Dash bullets; ordered starts and `.` / `)` delimiters preserved | At most three list levels. Blank lines distinguish loose from tight lists. |
| Tasks | `- [ ]` and `- [x]` boxes | Use list-item syntax, not free-standing bracket decorations. |
| Quotes | Indented blocks | At most three quote levels, counted separately from list levels. Nesting reduces usable width. |
| Rules | Full-tape two-dot line | Put blank lines around `---`; immediately beneath text it can become a Setext heading. |
| Tables | Two or three columns; bold header; left/right alignment | Use `---` or `---:`; never centered `:---:`. Every row needs exactly the header's cell count. Cells contain inline content, not nested blocks. |
| Links | Italic labels; numbered destination endnotes when needed | Inline, reference, angle, and recognized bare links work. Define references; use consistent titles for repeated destinations. Long URLs can overflow even in notes. A link is not a QR. |
| Footnotes | First-use numbering shared with link notes; multiblock definitions | Define every `[^name]`. Unused definitions disappear. Indent continuation blocks. |
| Images | Standalone PNG/JPEG, shrunk to fit and dithered; never upscaled | Image alone in its paragraph, not inside a link or table. Alt text is not printed: put meaningful captions in a separate paragraph. |
| Math | LaTeX via RaTeX: `\(inline\)` and `\[display\]` | Dollars are currency, not delimiters. No heading math; display math belongs in a separate paragraph, outside styles, links, and tables. Unsupported formulas/glyphs fail. |
| Text conventions | Escapes/entities decoded; smart quotes, dashes, ellipses in prose | Use code for literal punctuation. Glyph coverage is finite; do not assume emoji or arbitrary scripts are available. |

Linux faces are Liberation Sans and Liberation Mono. Serif, tracked display, or a feast title goes in the raster. See [tape.md](tape.md).

Images dither by the rule in [tape.md](tape.md). A figure wider than the tape shrinks. It never scales up. A 111 px QR stays 111 px, so render a QR around 200 px, 1-bit, quiet zone included.

Image paths are local, or `file:` relative to the `.md`. Remote URLs are not for a deterministic job. A receiver markdown job cannot see the caller's files. That constraint is [receiver.md](receiver.md).

## Footguns

- No raw HTML, including comments or `<br>`. No CSS, YAML front matter, definition lists, image-size attributes, or browser layout.
- Escape a literal table pipe as `\|`, even inside a code span. Backticks do not protect a pipe.
- Escape literal square brackets (`\[` and `\]`) when they are not a link, a footnote, or a task. An apparent reference with no definition rejects.
- Right-align amount columns and keep the decimal precision. Digits are tabular. There is no spreadsheet number format.
- Narrow a table by shortening labels or moving detail into prose. Do not drop data, invent a glyph, or omit an overflow.
- An empty header wastes a white band. An empty tick cell collapses. Use a task list, or put `[ ]` in the cell when the table is required.

## Receipt

A header-only table after a rule aligns the total with the items and emphasizes the header. Keep the separator row.

```markdown
# Corner shop

Order 42\
5 September 2026

| Item | Amount |
| --- | ---: |
| Coffee | 6.00 |
| Bread | 4.50 |

---

| Total | 10.50 |
| --- | ---: |

Thank you.
```
