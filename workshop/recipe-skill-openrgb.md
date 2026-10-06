---
id: recipe-openrgb
created: 2026-03-09
modified: 2026-10-06
status: active
type:
  - "project-skill"
---

```yaml
name: openrgb
output_format: project-skill

# zrrh OpenRGB config project. Not a home skill, and not the flake checkout.
# SSH by Tailscale IP; MagicDNS does not resolve from adeck.
target_locations:
  - path: zk@100.77.90.79:~/.config/OpenRGB/.agents/

sources:
  tree: skills/openrgb
```
