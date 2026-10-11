# Taildrop

Inbox: `/tmp/taildrop-inbox/` on the host.

Files sent from phones or other mesh nodes via Taildrop land here but require explicit retrieval:

```bash
# Retrieve pending files (requires sudo)
sudo tailscale file get /tmp/taildrop-inbox/

# Check inbox contents
ls -lt /tmp/taildrop-inbox/
```

- Files are owned by root after retrieval.
- The inbox is in `/tmp`. Contents do not survive reboot.
- Taildrop sends show as delivered on the sender before retrieval on the receiver. Run `sudo tailscale file get` to flush pending transfers.
- `tailscale file get` without sudo fails with "Access denied" unless `sudo tailscale set --operator=$USER` has been run.
