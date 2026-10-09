---
title: quest
glyph: "🗺️"
lens: campaign-telling
purpose: An interactive HTML map of a plan — party, path, sheets, rumors.
context: A plan, spec, or implementation is in play. Offer the map. Build it only if they say yes.
tone: tavern-map
structure: overworld → party → quest graph → sheets → rumors
tags:
  - plan
  - map
  - html
---

# 🗺️ Quest

If a plan, spec, or implementation is in context, offer to make a quest map. Wait for a yes.

Then write one self-contained HTML file next to the source: `<stem>.quest.html`. If there is no path, write `./quest-map.html`. Point at the path. Do not paste the HTML into chat.

## Map

A clickable graph of the campaign.

- **Overworld** banner: why anyone entered, the prize if they walk out.
- **Party** roster: people, tools, agents as classes. Click a member for what they are for and what they must not try to be.
- **Main quests** as nodes in walking order, edges as the path. Click a node to open its **sheet**:
  - door (what you need before you go in)
  - boss (the actual hard bit)
  - loot (real deliverable: file, decision, passing test)
  - save point (how you know you can stop)
- **Side quests** visible, dimmed, not on the main path. Clickable. Do not auto-start them.
- **Rumors** drawer: constraints, open questions, why you do not rush the whole map in one night.

One quest highlighted as *current* if the source says where they are. Otherwise the first unlocked door.

## File

One HTML file. Inline CSS and JS. No build, no CDN required. Works opened from disk.

Catppuccin mocha (`#1e1e2e` base, `#cdd6f4` text, accents from rose/peach/green/lavender). Font: Recursive, then system mono.

Keyboard: nodes focusable, Enter/Space opens a sheet, Escape closes. Respect `prefers-reduced-motion`.
