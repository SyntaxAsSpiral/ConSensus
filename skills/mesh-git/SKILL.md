---
name: mesh-git
description: >-
  Mesh git style and preferences. Use when writing a commit message, setting
  the commit template, changing a canonical repo, or committing an echo repo.
---

# mesh-git

## Canonical

- ConSensus
- nix-os/zk-nix 

A canonical repo is written only in its local checkout on adeck, by a CLI agent — not via ssh. It also does not accept pushes except under extremely rare circumstances.

## Echo repos

Repos under `/mnt/echo` owned by zk (not 3rd party) other than the canonical pair are not canonical. Commit and push them, without waiting to be asked, when the merge is clean and the change does not break anything. Fleet may clone and push changes those repos, and may work in a local checkout or through a CLI agent on adeck.

## Commit

When asked to commit stage EVERYTHING by default, unless instructed otherwise. You may chunk large commits into smaller modules though. 

Wrap commit message in your best, most authentic Warhammer 40k murder-cogitator impression. About 40% should resemble terminal output. Address reader as heretek, flesh-thing. The closed frames are [references/frames.md](references/frames.md).

Copy the template's border. Fill `title`, `chronohex`, and `closing`. The lines under `COGITATION::LOG` are the message. A line may carry a label. It does not have to start with `❯`. Repeat a `║║` line until the message fits. Nothing sits outside the border.

The annex holds a list or a diff summary, one branch per item. A diff summary is a path and its change, not a pasted hunk. Repeat a `║░╠══` line until the list fits. The runes may change per item. Delete the annex when the message has no list.

The bracket is a title in the voice. The chronohex goes on the liturgical cycle line. The chronohex is the last six hex digits of the nanosecond. A `⟳` context seal already counts.
