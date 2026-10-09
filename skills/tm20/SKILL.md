---
name: tm20
description: >-
  Print 80 mm thermal slips and receipts on the mesh Epson TM-T20III via tm20/tm20-set
  or the tm20 print receiver. Use when designing or printing tape, item listings,
  logos, QR, ESC/POS, 1-bit art, or when the user mentions tm20, TM-T20III, thermal
  printer, 80 mm receipts, or the mesh print receiver. Slash: /tm20
metadata:
  author: zk
  version: "0.6.0"
  category: print
  compatibility: USB and tm20 binaries are the tm20 Pi only; other hosts POST the receiver. No CUPS. Paper must be loaded.
---

# tm20

80 mm tape. One loom, on the `tm20` Pi. Do not sit at it and POST the same job.

Tape is 576 dots wide, about 203 dpi. Length can grow. Width cannot. Host, USB id, udev, and the binaries are mesh Services → tm20 thermal. Do not install tm20 on every box. Do not CUPS. Do not router-USB.

Read the leaf for the dial you are about to turn.

| Leaf | When |
|---|---|
| [usb](references/usb.md) | On `tm20`: preview, print, smoke the head. |
| [receiver](references/receiver.md) | Any other host, or a script that prints unattended. |
| [markdown](references/markdown.md) | Composing the slip. |
| [tape](references/tape.md) | Marks, hatch, QR, lockups, gilding. |
| [motifs](references/motifs.md) | Which mark, and where it lives. |

## Checklist

1. Paper in, cover closed.
2. Compose the slip, or an inspected PNG at tape width. Gray plates stay gray. Type stays black.
3. Preview and read the PNG.
4. On `tm20`, print from [usb](references/usb.md). From anywhere else, POST [receiver](references/receiver.md) with a new `job_id`.
5. Blank tape: the heat side of the roll faces the head, paper over the top.
