# Backpressure Benchmarks

Stress-tests the Python SDK's adaptive backpressure system under realistic
multi-client deployments (25 and 50 independent clients hitting the same
Camunda cluster).

## Prerequisites

- Python 3.10+ with `uv`
- Docker (the Camunda container is managed automatically)
- The SDK must be generated first: `make generate` (from repo root)

## Quick Start

```bash
# Run the full 72-configuration matrix (container restarted between each run)
uv run demo/v2/backpressure/run_matrix.py

# Preview what would run
uv run demo/v2/backpressure/run_matrix.py --dry-run
```

## Matrix Dimensions

| Dimension | Values | Purpose |
|-----------|--------|---------|
| **Clients** | 25, 50 | Simulates real customer deployment scale |
| **Mode** | `sync`, `async`, `thread` | SDK execution strategy |
| **Workload** | `instant`, `sleep`, `http` | Simulated handler cost (no-op, 0.2s sleep, 0.2s HTTP call to local server) |
| **Profile** | `BALANCED`, `LEGACY` | Backpressure configuration (adaptive vs retry-only) |
| **Isolation** | `subprocess`, `inprocess` | `subprocess` = separate OS process per client (no GIL); `inprocess` = threading.Thread per client (shared GIL) |

Total: 2 × 3 × 3 × 2 × 2 = **72 configurations**.

## What It Measures

For each configuration the runner collects:

- **Throughput** (ops/s) — aggregate completions per second
- **Errors** — failed API calls (429s, timeouts, etc.)
- **Queue-full** — subset of errors caused by full backpressure queue
- **Wall-clock time** — total run duration
- **Jain's fairness index** — distribution of work across clients (1.0 = perfectly fair)

## Container Restart

Between every run the Camunda Docker container is **stopped and restarted**
so each configuration starts from an identical clean baseline. This eliminates
carry-over effects like warmed caches, lingering backpressure state, or
accumulated process instances.

You can skip restarts for faster (but less reliable) runs:

```bash
uv run demo/v2/backpressure/run_matrix.py --no-restart
```

## Running Subsets

```bash
# Only 25 clients
uv run demo/v2/backpressure/run_matrix.py --clients 25

# Only async and thread modes
uv run demo/v2/backpressure/run_matrix.py --modes async thread

# Only BALANCED profile
uv run demo/v2/backpressure/run_matrix.py --profiles BALANCED

# Only subprocess isolation (skip in-process/GIL runs)
uv run demo/v2/backpressure/run_matrix.py --isolations subprocess

# Only instant and http workloads
uv run demo/v2/backpressure/run_matrix.py --workloads instant http

# Custom target per client (default: 20)
uv run demo/v2/backpressure/run_matrix.py --target 50

# Custom max inflight per client (default: 10)
uv run demo/v2/backpressure/run_matrix.py --concurrency 20
```

## Output

Results are written to `demo/v2/backpressure/results/`:

| File | Contents |
|------|----------|
| `report.md` | Markdown report with tables, analysis, and recommendations |
| `results.json` | Raw metrics for all runs (machine-readable) |
| `<label>.txt` | Raw stdout/stderr from each individual run |

Labels follow the pattern `{clients}c-{B|L}-{mode}-{workload}-{sub|inp}`, e.g. `50c-B-async-sleep-sub.txt`.

## Individual Scripts

The matrix runner orchestrates the lower-level scripts. You can also run them
directly:

### Single Client

```bash
# Default: async, BALANCED, 1000 completions
uv run demo/v2/backpressure/single_client.py

# Thread worker, LEGACY profile, 200 completions
MODE=thread CAMUNDA_SDK_BACKPRESSURE_PROFILE=LEGACY TARGET=200 \
  uv run demo/v2/backpressure/single_client.py
```

### Multi Client

```bash
# 3 clients, async, BALANCED, 100 per client
NUM_CLIENTS=3 TARGET_PER_CLIENT=100 \
  uv run demo/v2/backpressure/multi_client.py

# 50 clients, sync, LEGACY, no spike phase, subprocess isolation
NUM_CLIENTS=50 MODE=sync PROFILE=LEGACY SPIKE_CLIENTS=0 TARGET_PER_CLIENT=20 \
  ISOLATION=subprocess \
  uv run demo/v2/backpressure/multi_client.py

# Same but with in-process/GIL (threading) isolation
NUM_CLIENTS=50 MODE=sync PROFILE=LEGACY SPIKE_CLIENTS=0 TARGET_PER_CLIENT=20 \
  ISOLATION=inprocess \
  uv run demo/v2/backpressure/multi_client.py
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODE` | `async` | `sync` / `async` / `thread` |
| `ISOLATION` | `subprocess` | `subprocess` (separate OS process per client) or `inprocess` (shared GIL) |
| `TARGET` / `TARGET_PER_CLIENT` | 1000 / 500 | Completions to reach |
| `START_CONCURRENCY` / `CLIENT_CONCURRENCY` | 200 / 50 | Max inflight creates per client |
| `ACTIVATE_BATCH` | 32 | Jobs per poll / `max_concurrent_jobs` |
| `HANDLER_TYPE` | `sleep` | `sleep` (time.sleep / asyncio.sleep) or `http` (httpx to local sim server) |
| `HANDLER_LATENCY_S` | `0.2` | Simulated handler latency in seconds |
| `CAMUNDA_SDK_BACKPRESSURE_PROFILE` / `PROFILE` | `BALANCED` | `BALANCED` or `LEGACY` |
| `NUM_CLIENTS` | 3 | Number of independent clients (multi_client only) |
| `SPIKE_CLIENTS` | 2 | Extra clients added mid-run (multi_client only) |
| `SPIKE_DELAY_S` | 15 | Seconds before spike phase (multi_client only) |

## Process Under Test

All scenarios deploy `resources/bp-test-process.bpmn`: a minimal
Start → ServiceTask(`bp-test-job`) → End process. The service task handler
simulates I/O based on `HANDLER_TYPE` and `HANDLER_LATENCY_S`.
