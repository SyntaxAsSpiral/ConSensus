---
id: recipe-build-mcp-server
created: 2026-09-26
modified: 2026-09-26
status: active
type:
  - "skill"
---

```yaml
name: build-mcp-server
output_format: skill

target_locations:
  - path: ~/.claude/skills/build-mcp-server/
  - path: ~/.agents/skills/build-mcp-server/
  - path: zk@100.115.135.104:~/.claude/skills/build-mcp-server/
  - path: zk@100.115.135.104:~/.agents/skills/build-mcp-server/
  - path: zk@100.82.51.63:~/.claude/skills/build-mcp-server/
  - path: zk@100.82.51.63:~/.agents/skills/build-mcp-server/

sources:
  tree: skills/upstream/claude-plugins-official/plugins/mcp-server-dev/skills/build-mcp-server
```
