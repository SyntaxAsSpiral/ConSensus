# Receiver

POST `http://100.123.184.5:8766/print` from any mesh host. The hostname `tm20` does not resolve on adeck.

The receiver takes one pattern at a time, refuses to print the same `job_id` twice, and cuts only after the pattern has finished. Use it from adeck, a phone, or a long-running service, and when two projects might arrive at once.

Token: `PRINT_TOKEN` (alias `HOLIDAY_PRINT_TOKEN`). Unique `job_id` (alias `slip_id`). Send a PNG at tape width or markdown, not both. Optional `source`: `holliday-table`, `holliday-estate`, `sideriod`.

```bash
curl -fsS -H "Authorization: Bearer $PRINT_TOKEN" http://100.123.184.5:8766/health
```

```json
{"job_id": "", "source": "", "sha256": "", "image": "<base64 png>"}
```

```json
{"job_id": "", "source": "", "sha256": "", "markdown": "# HLD-0028\n\n..."}
```

Inspect a preview before the POST. A duplicate `job_id` returns the prior status and does not print again. If the status is uncertain, check the tape before minting a new id.

A markdown POST cannot see files on the caller. The markdown must be self-contained, with assets that already exist on `tm20`, or you send the PNG.
