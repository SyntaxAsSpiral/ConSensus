# Bench

Scored local-model runs are `/mnt/echo/inf-bench`. Whether a score says anything about reasoning effort is `cli-coding` routing. Impossible Moments, under `impossible-moments/`, is scored by hand.

The multiplayer sidecar is a persistent world. Do not point an evaluator at it. The scored path is `bin/fle-eval` or `bin/fle-throughput-suite` on disposable slots.

## Setup

```bash
cd /mnt/echo/inf-bench
nix develop path:.
uv sync --locked
set -a
source .env
set +a
```

`path:.` is required. A bare `nix develop` treats an incomplete `.git` as a Git flake and fails. `.env` is gitignored. Nix and the entrypoints do not load it. `.env.example` sets `OPENAI_API_KEY=local` and `OPENAI_BASE_URL=http://127.0.0.1:1234/v1`, which is the adeck loopback. From another host set `http://100.89.32.9:1234/v1`.

## Slots

```bash
nix develop path:. -c bin/fle-cluster start -n 2
```

Factorio `2.0.77`. Slot 0 is game port `34197` and RCON `27000`. Slot 1 is game port `34198` and RCON `27001`. From nxiz, observe slot 0 at `100.89.32.9:34197`. Join before the evaluator injects Lua. A join after injection can kill the server with `Cannot serialise lua functions`.

`bin/fle-cluster restart` restarts every slot. Reset one world with `docker restart cluster-factorio_0-1` or `cluster-factorio_1-1`. Each evaluator needs its own `FLE_SERVER_START` / `FLE_SERVER_END`. `--max-connections 1` does not isolate two processes.

## Run

Local models use Inspect's `openai/` prefix plus the gateway id. Use the model `lms ps` shows loaded. The inf-bench docs also name `openai/qwen/qwen3.6-27b`. The seated id is `qwen/qwen3.8-27b`.

```bash
FLE_SERVER_START=0 FLE_SERVER_END=1 \
nix develop path:. -c bin/fle-eval \
  --env-id iron_plate_throughput \
  --model openai/<loaded-id> \
  --limit 1 \
  --trajectory-length 1 \
  --max-connections 1 \
  --epochs 1 \
  --epochs-reducer pass_at_1 \
  --log-dir .fle/inspect_logs/smoke
```

`--trajectory-length 1` is a smoke test. A scored run uses `64`. `bin/fle-eval` drops upstream's 4096-token generation cap. Logs land under `.fle/inspect_logs/`.

`iron_plate_throughput` uses `factorio_controlled_solver`, which sends `reasoning_effort: "minimal"` on each generate. `fle inspect-eval --reasoning-effort` accepts `low`, `medium`, and `high`, and does not change that run while the pin is there.

One large model at a time. A second local model on the other slot unloads the first. An OpenRouter run uses the `openrouter/` prefix, slot 1, and is metered.

`--epochs` overrides `--pass-n`. A comma-separated `--tasks` list allocates one Factorio index per name. `bin/fle-throughput-suite` is sequential on slot 0 and restarts that slot between tasks. Set `FLE_MODEL`. Leave it idle while either slot is busy.
