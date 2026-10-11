---
name: esocortex
description: >-
  Look up the corpus when the topic is abstract, philosophical, esoteric, occult, or reflective. 
  /topic/astro food taxeia, /symbol/, /chunk/, corpus lookup on port 8880.
---

# esocortex

Read-only JSON. `GET` and `HEAD`. A list row has no passage. The passage is a second request.

## Address

| From | URL |
|---|---|
| adeck | `http://127.0.0.1:8880` |
| tailnet | `https://adeck.tail293e98.ts.net:8880` |

On adeck, use loopback. Hostnames do not resolve there. User service `esocortex-api` binds `127.0.0.1`. Tailscale serve publishes port 8880 on the tailnet.

`GET /` returns the live caps, the chunk count, and the route list. Trust that payload when it and this page disagree.

## Routes

| GET | Params | Body |
|---|---|---|
| `/` or `/health` | — | status, caps, routes |
| `/topic` | — | `{topics:[{topic, count}]}` |
| `/topic/{topic}` | `limit` default 20, max 100; `offset` max 2000 | `{topic, count, limit, offset, hits}` |
| `/symbol/{symbol}` | `limit` default 20, max 100; `offset` max 2000; `topic` | `{symbol, count, limit, offset, topic, hits}` |
| `/symbol/{symbol}/co` | `limit` default 20, max 50; `topic` | `{symbol, limit, topic, co:[{symbol, count}]}` |
| `/chunk/{id}` | — | `{chunk, text_truncated}` |

Percent-encode the symbol (`Basil Valentine` → `Basil%20Valentine`). A chunk id may contain `/` and `:`. Encoding the whole id is safe. A raw id after `/chunk/` also resolves. `..`, `\`, or a leading `/` is `400`.

`limit` above the max is clamped. `offset` above 2000, `limit` below 1, and a topic outside `^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$` are `400`.

Omit `topic` on a symbol search to search every label. Set it to keep chunks whose `topic` array contains that label.

## Topics

| topic | holds |
|---|---|
| `astro` | ista, carey-salts, zachary-reading |
| `food` | ista |
| `taxeia` | A Pattern Language (`source` `pattern-language`) |

`GET /topic` returns the live labels and counts. `GET /topic/taxeia` lists the pattern language. A symbol search inside that book sets `topic=taxeia`.

Symbol match is case-insensitive. An unknown symbol, topic, or chunk id is `404`.

## Rows

`id`, `kind`, `parent_id`, `collection`, `source`, `source_path`, `title`, `heading`, `word_count`, `translation`, `topic`, `keys`.

`topic` is a list of labels. `keys` is a list of `{name}`. `translation` is the stored gloss. `chunk.text` is the passage, cut at 65536 characters, with `text_truncated` set when that happens. Co-occurrence counts distinct shared chunks.

```bash
# adeck. From the tailnet, swap in the https origin.
curl -fsS 'http://127.0.0.1:8880/topic'
curl -fsS 'http://127.0.0.1:8880/topic/taxeia?limit=5'
curl -fsS 'http://127.0.0.1:8880/symbol/Ethnography?limit=5'
curl -fsS 'http://127.0.0.1:8880/symbol/Ethnography/co?limit=10'
curl -fsS 'http://127.0.0.1:8880/chunk/ista:alc/antimony.htm:c1'
curl -fsS --get 'http://127.0.0.1:8880/symbol/Antimony' \
  --data-urlencode 'topic=astro' --data-urlencode 'limit=5'
```

`curl --get` encodes the query. A space in the path still needs encoding.

## Failures

`400` bad request, symbol, or id. `404` missing. `405` anything besides GET or HEAD. `414` request line or query over the cap. `429` rate limit, `Retry-After: 1` (bucket 30, refill 15/s; loopback keys off the first `X-Forwarded-For` hop). `503` the query passed 3 seconds.

Model calls belong to the mesh-ops inference leaf. Corpus writes belong in `/mnt/echo/esocortex`.
