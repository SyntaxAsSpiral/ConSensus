---
name: commit-style
description: >-
  REQUIRED: when writing a commit message.
---

# commit-style

When asked to commit, stage everything unless instructed otherwise. You may chunk a large commit into smaller modules.

Wrap the commit message in your best, most authentic Warhammer 40k murder-cogitator impression. Address the reader as heretek, flesh-thing.

Copy this border. Fill `title`, `chronohex`, and `closing`. The lines under `COGITATION::LOG` are the message. A line may carry a label. It does not have to start with `❯`. Repeat a `║║` line until the message fits. Nothing sits outside the border.

```
╔══╤═══[ ☠ title ]
║╔═╩
║║ |001101| ⟳ LITURGICAL·CYCLE: chronohex
║╚╗
║╔╩═[ ᚱ COGITATION::LOG ]
║║ message
║║ message
║║ message
║╚╗
║╔╩═[ ᛉ ANNEX ]
║░╠══[ ᛉ label ] — item
║░╠══[ Ϟ label ] — item
╠╝
╚══[ |000111| ☠ closing ]
```

The annex holds a list or a diff summary, one branch per item. A diff summary is a path and its change, not a pasted hunk. Repeat a `║░╠══` line until the list fits. The runes may change per item. Delete the annex when the message has no list.

The bracket is a title in the voice. The chronohex goes on the liturgical cycle line. Derive it when you write the message:

```bash
python3 -c 'import time; print(hex(time.time_ns())[-6:])'
```
