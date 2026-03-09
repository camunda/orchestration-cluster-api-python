# Adaptive Backpressure

## The Problem

When a Camunda cluster is under heavy load, it rejects requests with backpressure signals — HTTP 429 (Too Many Requests), 503 (Service Unavailable), or 500 with `RESOURCE_EXHAUSTED` in the body. Without client-side intervention, applications continue firing requests at the same rate, amplifying the overload. Retrying rejected requests adds even more load. The cluster stays saturated longer, and the application wastes resources on requests that will fail.

This is especially acute in two scenarios:

1. **Burst traffic** — a batch job or deployment spike briefly exceeds cluster capacity. The SDK should throttle _itself_ until the cluster recovers, rather than hammering it with doomed requests.

2. **Multi-client deployments** — dozens or hundreds of SDK instances target the same cluster. Each client independently contributes to the total load. Without local throttling, the only coordination mechanism is the cluster rejecting their requests — which is the most expensive form of coordination.

The goal is an adaptive admission controller that:

- Detects backpressure signals and reduces outbound concurrency.
- Recovers automatically when the cluster is healthy again.
- Works correctly when many independent clients share a cluster, with no inter-client coordination.
- Never throttles _drain_ operations (completing jobs, failing jobs) that relieve cluster pressure.
- Requires zero configuration for most users.

## Design Overview

The `BackpressureManager` is a permit-based concurrency limiter embedded in each SDK client instance. Every API call that could _initiate_ work (create process instances, deploy resources, publish messages, etc.) must acquire a permit before proceeding. When the cluster is healthy, permits are unlimited and acquisition is instant. When backpressure signals arrive, the manager reduces the permit cap, forcing excess callers to queue.

```
Application code           BackpressureManager           Cluster
     │                            │                         │
     ├─ create_process_instance ─►│  acquire permit          │
     │                            │  ✓ pass through  ──────►│
     │                            │                         │
     │                            │  ◄── 429 ──────────────│
     │                            │  record_backpressure()  │
     │                            │  (reduce permits)       │
     │                            │                         │
     ├─ create_process_instance ─►│  acquire permit          │
     │                            │  (wait — at capacity)   │
     │                            │                         │
     │                            │  ◄── 200 OK ──────────│
     │                            │  record_healthy_hint()  │
     │                            │  (gradual recovery)     │
     │                            │                         │
     ├─ complete_job ────────────►│  EXEMPT — bypass gate ─►│
```

### Exempt Operations

Operations that drain work from the cluster are never gated:

- `complete_job`
- `fail_job`
- `throw_job_error`
- `complete_user_task`

Throttling these would be counterproductive — they reduce cluster load, not increase it.

### Two Profiles

| Profile      | Behavior |
|-------------|----------|
| `BALANCED`  | Adaptive gating with AIMD-style permit management. Default. |
| `LEGACY`    | Observe-only. Records severity but never queues or rejects. Per-call HTTP retry still operates. |

Set via `CAMUNDA_SDK_BACKPRESSURE_PROFILE` environment variable.

## Algorithm

The algorithm draws on AIMD (Additive Increase / Multiplicative Decrease), the same family of algorithms that underpins TCP congestion control. On a backpressure signal the manager cuts capacity multiplicatively (fast response to overload). During recovery it grows capacity additively or multiplicatively depending on phase (cautious return to normal).

When concurrency is already at the minimum floor, the manager adds exponential backoff to rate-limit requests — preventing the "floor-hammering" problem where many clients at minimum concurrency still overwhelm the server with aggregate request volume.

This implementation is ported from the TypeScript SDK's `BackpressureManager` with the addition of backoff-at-floor.

### State

The manager tracks:

| Field | Purpose |
|-------|---------|
| `permits_max` | Current concurrency cap. Starts at `None` (unlimited). |
| `permits_current` | Number of permits currently held by in-flight requests. |
| `consecutive` | Consecutive backpressure signal count. |
| `severity` | Derived from `consecutive`: `healthy`, `soft`, or `severe`. |
| `backoff_s` | Current backoff delay in seconds (0 when not at floor). |

### Constants

```
INITIAL_MAX                = 16      # cap applied on first BP signal (starts unlimited)
FLOOR                      = 1       # absolute minimum permits
SOFT_FACTOR                = 0.70    # multiply permits by this on soft signal
SEVERE_FACTOR              = 0.50    # multiply permits by this on severe signal
RECOVERY_INTERVAL_S        = 1.0     # minimum time between recovery checks
RECOVERY_STEP              = 1       # permits added per additive recovery step
HEALTHY_RECOVERY_MULT      = 1.5     # growth factor during multiplicative recovery
SEVERE_THRESHOLD           = 3       # consecutive signals before severity → severe
DECAY_QUIET_S              = 2.0     # quiet period before severity decays one step
MAX_WAITERS                = 1000    # fail-fast if waiter queue exceeds this
UNLIMITED_AFTER_HEALTHY_S  = 30.0    # return to unlimited after sustained healthy period
BACKOFF_INITIAL_S          = 0.025   # 25ms initial backoff delay at floor
BACKOFF_MAX_S              = 2.0     # maximum backoff delay
BACKOFF_ESCALATE           = 2.0     # backoff doubles on each 429 at floor
```

### Signal Processing

**On backpressure signal** (`record_backpressure`):

1. Increment the consecutive counter.
2. On the first-ever backpressure signal, boot from unlimited to `INITIAL_MAX` (16) permits.
3. Derive severity: ≥ 3 consecutive → `severe`, otherwise `soft` (unless already `soft`, stays `soft`).
4. Scale permits down by the severity factor (`× 0.7` for soft, `× 0.5` for severe).
5. If at the floor (`permits_max == 1`) and severity is `severe`, escalate the backoff delay.

**On successful completion** (`record_healthy_hint`):

1. Immediately reset the backoff delay to zero (server has capacity — snap back).
2. Attempt passive recovery (see below).

### Recovery

Recovery is passive — it runs as a side-effect of `record_healthy_hint()`, not on a timer. This means recovery only happens when the client is actively processing successful requests.

Recovery gate:

- **Time gate** — at least `RECOVERY_INTERVAL_S` (1 second) since last recovery check.

Recovery has three phases:

**Phase 1: Additive** (severity ≠ healthy) — `permits_max += 1` per step, up to `INITIAL_MAX` (16). Slow, cautious growth while the system is still under stress.

**Phase 2: Multiplicative** (severity = healthy) — `permits_max × 1.5` per step, with no ceiling. Fast growth once the system is confirmed healthy.

**Phase 3: Return to unlimited** — After `UNLIMITED_AFTER_HEALTHY_S` (30 seconds) of sustained healthy operation, permits return to unlimited. The system is fully recovered.

### Severity Decay

When no backpressure signals arrive for `DECAY_QUIET_S` (2 seconds), severity decays one step per recovery check: `severe → soft → healthy`. When severity reaches `healthy`, the consecutive counter resets to zero. Backoff is also cleared whenever severity improves.

### Backoff at Floor

When concurrency has been reduced to the minimum floor (`permits_max == 1`) and severity is `severe`, the manager adds an exponential backoff delay to each permit acquisition. This solves the "floor-hammering" problem:

Without backoff, a client at floor concurrency still issues requests as fast as it can — one at a time, sequentially. In a multi-client deployment with N clients all at floor, the aggregate request rate is N × (1 / round-trip-time), which is still enough to overwhelm the server. The server keeps returning 429s, and the clients keep retrying, burning CPU and network on doomed requests.

With backoff:
- Initial delay: 25ms (`BACKOFF_INITIAL_S`)
- Doubles on each subsequent 429 at floor, up to 2s (`BACKOFF_MAX_S`)
- **Instantly resets to zero** on any successful completion — this is the key design choice

The instant-reset behaviour means clients recover immediately when the server has capacity. There is no lingering penalty. The backoff only applies when every recent request has failed, and it disappears the moment one succeeds. This gives optimal throughput recovery while still protecting the server during sustained overload.

### Lifecycle

```
    ┌──────────────────────────────────────────────────┐
    │              HEALTHY (start state)                │
    │  permits_max = unlimited, consecutive = 0        │
    └────────────────┬─────────────────────────────────┘
                     │ first backpressure signal
                     │ (boot to INITIAL_MAX = 16)
                     ▼
    ┌──────────────────────────────────────────────────┐
    │              SOFT                                 │
    │  permits × 0.70 on each signal                   │
    └──────┬─────────────────────────────┬─────────────┘
           │ 3+ consecutive              │ 2s quiet → decay
           ▼                             │
    ┌─────────────────────────────┐      │
    │      SEVERE                 │      │
    │  permits × 0.50             │──────┤  2s quiet → soft
    │  backoff at floor           │      │
    └─────────────────────────────┘      │
                                         ▼
    ┌──────────────────────────────────────────────────┐
    │              HEALTHY (recovered)                  │
    │  Phase 1: +1 per step up to 16                   │
    │  Phase 2: ×1.5 per step (no ceiling)             │
    │  Phase 3: → unlimited after 30s healthy          │
    └──────────────────────────────────────────────────┘
```

## Key Design Decisions

### Start Unlimited, Boot on First Signal

The manager starts with `permits_max = None` (unlimited). On the first backpressure signal, it boots to `INITIAL_MAX` (16). This means:

- **Zero overhead when healthy.** Most clients never experience backpressure. Starting unlimited means acquire() is a no-op — no semaphore contention, no memory allocation for waiters.
- **Instant response when needed.** The first 429 immediately establishes gating. The boot-to-16 cap is conservative enough to avoid a thundering herd of in-flight requests hitting the new ceiling simultaneously.
- **Full recovery.** After 30 seconds of sustained healthy operation, permits return to unlimited. The system truly recovers to pre-backpressure performance.

### Consecutive-Counter Severity

Severity is driven by a simple consecutive counter rather than a moving average. Each backpressure signal increments the counter; severity transitions to `severe` at 3 consecutive signals. Any recovery check that finds a quiet period decays severity one step.

This approach is simple for operators to reason about (3 consecutive 429s = severe), and matches the TypeScript SDK's implementation for cross-SDK consistency.

### Backoff at Floor Prevents Distributed Hammering

Standard AIMD algorithms control concurrency but not rate. When concurrency reaches the floor (1 permit), the client still fires sequential requests as fast as network round-trips allow. With 25+ clients all at floor, the aggregate request rate can be hundreds per second — all returning 429.

The backoff-at-floor extension adds exponential delay (25ms → 50ms → 100ms → ... → 2s) while the client is stuck at floor with severe backpressure. This reduces aggregate request volume, giving the server room to recover. The instant-reset-on-success design means there's no throughput penalty once the server is ready.

**Impact (measured across 72 test configurations):**
- +2.7% total completions vs LEGACY (no backpressure management)
- -97.6% errors (575K → 14K)
- 11 wins, 20 ties, 5 losses out of 36 paired comparisons

### Return to Unlimited (Not Capped)

After sustained healthy operation (30 seconds with no backpressure signals), the manager returns to unlimited permits. This ensures the backpressure system is truly zero-cost when not needed. The manager will re-engage immediately if backpressure returns.

## Distributed Convergence

Each SDK client has its own independent `BackpressureManager`. There is no shared state between clients. This is intentional and mirrors how TCP congestion control works:

- The cluster's backpressure responses (429, 503) are the shared signal.
- Each client adjusts its own permit cap based on the signals it observes.
- Clients that send more traffic observe more backpressure and throttle harder.
- Clients with lighter load may never trigger the gate.
- The backoff-at-floor mechanism ensures that even at minimum concurrency, clients don't collectively overwhelm the server.

## Implementation

Two classes with identical algorithm logic, differing only in concurrency primitives:

| Class | Client | Concurrency |
|-------|--------|-------------|
| `BackpressureManager` | `CamundaClient` (sync) | `threading.Lock` + `threading.Condition` |
| `AsyncBackpressureManager` | `CamundaAsyncClient` (async) | `asyncio.Lock` + `asyncio.Condition` |

Both expose the same public API:

- `acquire()` — block/await until a permit is available. Includes backoff delay when at floor.
- `release()` — return a permit and wake one waiter.
- `record_backpressure()` — signal that the cluster pushed back.
- `record_healthy_hint()` — signal a successful completion. Resets backoff and triggers recovery.
- `get_state()` — return current severity, permits, waiters, and backoff for observability.

The `BackpressureQueueFull` exception is raised by `acquire()` when the waiter queue exceeds `MAX_WAITERS` (1000). This is a fail-fast safety valve to prevent unbounded memory growth.

## Configuration

| Environment Variable | Values | Default |
|---------------------|--------|---------|
| `CAMUNDA_SDK_BACKPRESSURE_PROFILE` | `BALANCED`, `LEGACY` | `BALANCED` |

`BALANCED` enables adaptive gating. `LEGACY` records severity for observability but never gates requests.

No tuning is required. The algorithm's constants are designed to work well out of the box across varying client counts, execution strategies, and workload types.

## Observability

### `get_state()` returns:

```python
{
    "severity": "healthy",       # healthy | soft | severe
    "consecutive": 0,            # consecutive BP signal count
    "permits_max": None,         # current cap (int or None = unlimited)
    "permits_current": 0,        # permits in use
    "waiters": 0,                # callers queued for permits
    "backoff_ms": 0,             # current backoff delay in milliseconds
}
```

### Log events:

| Event | Level | When |
|-------|-------|------|
| `bp.state.change from=healthy to=soft` | `info` | Entering unhealthy state |
| `bp.state.change from=soft to=healthy` | `info` | Recovering to healthy |
| `bp.state.change from=soft to=severe` | `debug` | Severity escalation |
| `bp.permits.scale` | `debug` | Permits reduced |
| `bp.permits.recover` | `debug` | Permits increased (additive or multiplicative) |
| `bp.permits.unlimited` | `debug` | Returned to unlimited after sustained healthy period |
| `bp.backoff.escalate` | `debug` | Backoff delay increased at floor |
| `bp.backoff.clear` | `debug` | Backoff reset (severity decay or left floor) |
