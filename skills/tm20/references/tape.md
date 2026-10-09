# Tape

Thermal is a stamp, not a screen.

| Job | How |
|---|---|
| Mark, lockup, QR, type | Solid black (`fill=0` / mode `1`). Filled shapes, punched counters. |
| Engraving, hatch, gilding, still-life | Gray `L`. `tm20-set` Floyd–Steinbergs it. |

Do not threshold a hatch plate. Do not bake lettering in an image model. OpenType comes from `tm20-set` or from PIL.

- Stroke at least 4 px at the size that hits the tape, for a solid mark. Hatch can be finer. The dither carries it.
- Take the motif from the object, or from the meal.
- A full lockup, about 400 dots, is a masthead. A short item slip needs a smaller mark.
- A Celtic knot or vine band needs about 160–180 dots of height, or Floyd–Steinberg collapses it to a rule. Lighten it after it has that height.
- A week menu is one cartouche: double line, corner knots, head and foot vine. Do not lace every day.
- A photo is a thumbnail only if it survives dither.

Rebuild a lockup in the project's renderer when one exists. Estate: `brand/render_logo.py`. Feast: `family-cookbook/slips/template/render.py`. Change geometry there.

Which mark to fetch is [motifs.md](motifs.md).
