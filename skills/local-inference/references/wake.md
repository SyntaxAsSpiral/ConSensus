# Wake proxy

Source: `nix-os/modules/home/daemonturgy/lmstudio/adeck/inference-wake.py`, declared by `default.nix` beside it.

- Binds `0.0.0.0:1234`, upstream `http://127.0.0.1:1235` (`lms daemon up`).
- Gated (these POSTs, plus any WebSocket): `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/responses`, `/api/v0/chat/completions`, `/api/v0/completions`, `/api/v0/embeddings`, `/api/v1/chat`, `/api/v1/models/load`. A wake check runs before each downstream frame on a WebSocket.
- Ready means zrrh is TCP-reachable at `192.168.0.110:22` and `lms link status --json` shows peer `zrrh` with `status: "connected"`. Otherwise WoL (`60cf8461d800` → `192.168.0.255:9`) every 3 s for 120 s, then 503 `zrrh did not reconnect to LM Link within 120 seconds.` A 2 s cache covers a burst.
- Embeddings are gated too. `mxbai-embed-large-v1` lives on adeck and still pays the wake cost if zrrh is asleep.
- Timeouts: connect 10 s, read 600 s, no total. `auto_decompress: false`. Upstream failure → 502 `LM Studio upstream unavailable.`
- `GET /v1/models` and `GET /api/v0/models` pass through without a wake.

Where the lines land is [logs.md](logs.md).
