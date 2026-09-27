# Hue proposal

No local Hue CLI lives here. General control is the upstream `hue` skill. This note is only the house.

The bridge is on the LAN at `192.168.0.98`, HTTPS port 443, reachable from adeck. Agents call that address. Do not forward a WAN port to it, and do not put a public address in a client. The 2025-06-20 chat that said to publish port 443 or 8443 was wrong.

The application key stays in `HUE_API_KEY` or in `~/.clawdbot/hue/config.json` after `scripts/hue.sh pair`. It is also written in `daemon-chromasorix-bindu-02`. It does not get copied into a skill.

That bindu is a 2025 snapshot. Its frontmatter says API v2 and its script calls `/api/<key>/`. The light and room ids in it, including the three living lamps, are not the current set. The bridge has more bulbs now. Discover lights, rooms, and scenes from the bridge when a command needs them.

The old shell hook was `theme <name> -h` on zrrh. It synced a theme onto a fixed front-zone map. That map is retired with the snapshot.
