# USB

On the `tm20` host only. From another host, SSH these commands for design, debug, or smoke. App-driven copies use [receiver.md](receiver.md).

`tm20` is the protocol: `hello`, `list`, `text`, `qr`, `status`. `tm20-set` typesets markdown and sheets to a `GS ( L)` raster. Type, figures, and QR-as-image go through `tm20-set print md`.

Live group `plugdev` is required, which means a new login after `usermod`. This session may still need `-g plugdev`. If `id` already shows `plugdev`, drop the `sudo` wrapper.

```bash
tm20-set --dry --png /tmp/tm20-preview print md /path/to/slip.md

sudo -u zk -g plugdev tm20-set print md /path/to/slip.md

sudo -u zk -g plugdev tm20 list
sudo -u zk -g plugdev tm20 hello
sudo -u zk -g plugdev tm20 status
```

`list` must show `* 04b8:0e28`. `hello` prints `SYSTEM ONLINE` and cuts. `status` is cover closed and paper present.

Do not print if the cover is open or the roll is out. The head will cook the platen.

Read the preview PNG before the print. `tm20` / `tm20-set` and the receiver sit on the appliance. udev is already in the sdImage.
