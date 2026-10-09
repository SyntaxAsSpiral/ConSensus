# Logs

LM Studio logs are split. The gateway and the host running the weights write different files.

## adeck

- `journalctl --user -u inference-wake -u llmster` is the wake proxy and the local llmster unit.
- `~/.lmstudio/server-logs/YYYY-MM/*.log` is adeck's LM Studio HTTP server on port 1235.
- `lmstudio-log-retention.service` prunes those server logs older than seven days.

## Weight host

Load failures and llama.cpp lines land in `~/.lmstudio/server-logs/YYYY-MM/*.log` on the host running the weights. For the chat models that host is zrrh. Markers: `LMSTUDIO_STARTUP_ERROR`, `gguf_init_from_reader`. Qwen MTP confirmation is `grep -i "draft acceptance"` in that directory.
