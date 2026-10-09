# Terminal

Map ANSI slots to flavor names. Take the hex from [flavors.md](flavors.md). Window background is `base`. Window foreground is `text`.

## Window

| Slot | Dark flavors | Latte |
|---|---|---|
| Cursor | rosewater | rosewater |
| Cursor text | crust | base |
| Active border | lavender | lavender |
| Inactive border | overlay0 | overlay0 |
| Bell border | yellow | yellow |

## ANSI

| Slot | Dark flavors | Latte |
|---|---|---|
| 0 | surface1 | subtext1 |
| 1 | red | red |
| 2 | green | green |
| 3 | yellow | yellow |
| 4 | blue | blue |
| 5 | pink | pink |
| 6 | teal | teal |
| 7 | subtext0 | surface2 |
| 8 | surface2 | subtext0 |
| 9–14 | bright red, green, yellow, blue, pink, teal | same, light formula |
| 15 | subtext1 | surface1 |
| 16 | peach | peach |
| 17 | rosewater | rosewater |

Bright accents, slots 9–14, are generated. On the dark flavors: lightness × 0.94, chroma + 8, hue + 2. On Latte: lightness × 1.09, hue + 2. Black and white are the named slots above, not generated. A port that repeats the normal accent hex for 9–14 is that port's choice.

The operator variants in [variants.md](variants.md) use a different 16-slot order.
