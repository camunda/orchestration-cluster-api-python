"""
Multi-Client Distributed Backpressure Scenario
===============================================

Spawns N independent client instances (each with its own
``BackpressureManager``), all targeting the same Camunda cluster.  Each client
runs a producer+consumer loop creating process instances and completing jobs.

The goal is to observe how distributed, uncoordinated adaptive backpressure
converges:
  - Do the clients reach a stable equilibrium?
  - Does aggregate throughput improve vs. LEGACY (per-call retry only)?
  - Does any client starve while others dominate?
  - How quickly does the system recover when load drops?

Execution modes
───────────────
  **sync**    – Each client is a ``CamundaClient`` (blocking).  Threads run
                ``ThreadPoolExecutor`` producers and manual ``activate_jobs`` +
                ``complete_job`` consumer loops.

  **async**   – Each client is a ``CamundaAsyncClient`` (asyncio).
                ``asyncio.Semaphore``-gated producer tasks, job worker with
                **async** execution strategy for completions.

  **thread**  – Each client is a ``CamundaAsyncClient`` (asyncio).  Same
                producer as async, but the job worker uses the **thread**
                execution strategy (``ThreadPoolExecutor`` callbacks).

Phases
──────
  1. Ramp-up    — all base clients start simultaneously
  2. Spike      — additional clients join mid-run (optional)
  3. Cool-down  — spike clients stop, observe recovery

Environment variables
─────────────────────
  ISOLATION                subprocess | shared (default: subprocess)
                           subprocess = separate OS process per client (independent BP)
                           shared     = threads sharing ONE client (shared BP)
  MODE                     sync | async | thread (default: async)
  NUM_CLIENTS              Number of independent client instances (default: 3)
  SPIKE_CLIENTS            Extra clients added during spike phase (default: 2)
  TARGET_PER_CLIENT        Completions per client (default: 500)
  CLIENT_CONCURRENCY       Max inflight createProcessInstance per client (default: 50)
  ACTIVATE_BATCH           maxJobsToActivate per poll / max_concurrent_jobs (default: 32)
  HANDLER_TYPE             sleep | http (default: sleep)
  HANDLER_LATENCY_S        Simulated I/O latency per job handler (default: 0.2)
  SPIKE_DELAY_S            Seconds before spike clients join (default: 15)
  SPIKE_TARGET             Target for spike clients (default: 200)
  PROFILE                  Backpressure profile for all clients (default: BALANCED)
  PAYLOAD_SIZE_KB          Variable payload size in KB (default: 10)
  PROGRESS_INTERVAL_S      Progress report interval in seconds (default: 1.0)
  SCENARIO_TIMEOUT_S       Hard timeout in seconds (default: 300)

Usage
─────
  # Default: 3 base + 2 spike, BALANCED, async mode
  uv run demo/v2/backpressure/multi_client.py

  # Thread worker mode
  MODE=thread uv run demo/v2/backpressure/multi_client.py

  # Sync mode (manual activate+complete)
  MODE=sync uv run demo/v2/backpressure/multi_client.py

  # LEGACY comparison
  MODE=async PROFILE=LEGACY uv run demo/v2/backpressure/multi_client.py

  # Stress test: 5 base + 3 spike, 1000 target, 100 concurrency
  NUM_CLIENTS=5 SPIKE_CLIENTS=3 TARGET_PER_CLIENT=1000 CLIENT_CONCURRENCY=100 \\
    uv run demo/v2/backpressure/multi_client.py

  # Quick smoke test
  NUM_CLIENTS=2 SPIKE_CLIENTS=0 TARGET_PER_CLIENT=100 \\
    uv run demo/v2/backpressure/multi_client.py
"""

from __future__ import annotations

import asyncio
import http.server
import json
import math
import os
import random
import subprocess as sp
import sys
import tempfile
import time
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx

# ---------------------------------------------------------------------------
# Ensure the generated package is importable
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "generated"))

from camunda_orchestration_sdk import CamundaClient, CamundaAsyncClient  # noqa: E402
from camunda_orchestration_sdk.models.process_creation_by_key import ProcessCreationByKey  # noqa: E402
from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest  # noqa: E402
from camunda_orchestration_sdk.models.job_completion_request import JobCompletionRequest  # noqa: E402
from camunda_orchestration_sdk.models.process_instance_creation_instruction_by_key_variables import ProcessInstanceCreationInstructionByKeyVariables  # noqa: E402
from camunda_orchestration_sdk.runtime.job_worker import WorkerConfig, ConnectedJobContext  # noqa: E402

# ---------------------------------------------------------------------------
# Config (from env)
# ---------------------------------------------------------------------------
ISOLATION = os.environ.get("ISOLATION", "subprocess").lower()
assert ISOLATION in ("subprocess", "shared"), f"ISOLATION must be subprocess|shared, got {ISOLATION!r}"

MODE = os.environ.get("MODE", "async").lower()
assert MODE in ("sync", "async", "thread"), f"MODE must be sync|async|thread, got {MODE!r}"

NUM_CLIENTS = int(os.environ.get("NUM_CLIENTS", "3"))
SPIKE_CLIENTS = int(os.environ.get("SPIKE_CLIENTS", "2"))
TARGET_PER_CLIENT = int(os.environ.get("TARGET_PER_CLIENT", "500"))
CLIENT_CONCURRENCY = int(os.environ.get("CLIENT_CONCURRENCY", "50"))
ACTIVATE_BATCH = int(os.environ.get("ACTIVATE_BATCH", "32"))
HANDLER_TYPE = os.environ.get("HANDLER_TYPE", "sleep").lower()
assert HANDLER_TYPE in ("sleep", "http", "instant"), f"HANDLER_TYPE must be sleep|http|instant, got {HANDLER_TYPE!r}"
HANDLER_LATENCY_S = float(os.environ.get("HANDLER_LATENCY_S", "0.2"))
HANDLER_JITTER = 0.5  # +/-50% uniform jitter on handler latency
SPIKE_DELAY_S = float(os.environ.get("SPIKE_DELAY_S", "15"))


def _jittered_latency() -> float:
    """Return HANDLER_LATENCY_S with uniform jitter (+/-HANDLER_JITTER)."""
    return HANDLER_LATENCY_S * (1.0 + random.uniform(-HANDLER_JITTER, HANDLER_JITTER))
SPIKE_TARGET = int(os.environ.get("SPIKE_TARGET", "200"))
PROFILE = os.environ.get("PROFILE", "BALANCED")
PAYLOAD_SIZE_KB = int(os.environ.get("PAYLOAD_SIZE_KB", "10"))
PROGRESS_INTERVAL_S = float(os.environ.get("PROGRESS_INTERVAL_S", "1.0"))
SCENARIO_TIMEOUT_S = float(os.environ.get("SCENARIO_TIMEOUT_S", "300"))

# ANSI colours
_GREEN = "\033[92m"
_YELLOW = "\033[93m"
_RED = "\033[91m"
_BLUE = "\033[94m"
_BOLD = "\033[1m"
_GRAY = "\033[90m"
_RESET = "\033[0m"

SEVERITY_COLOURS: dict[str, str] = {
    "healthy": f"{_GREEN}healthy{_RESET}",
    "soft": f"{_YELLOW}soft{_RESET}",
    "severe": f"{_RED}severe{_RESET}",
}


# ---------------------------------------------------------------------------
# Local HTTP server for simulated external-API I/O (HANDLER_TYPE=http)
# ---------------------------------------------------------------------------
class _SimHandler(http.server.BaseHTTPRequestHandler):
    """Tiny handler that sleeps for HANDLER_LATENCY_S (with jitter) then returns 200 OK."""

    def do_GET(self) -> None:
        time.sleep(_jittered_latency())
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def log_message(self, *_args: object) -> None:  # noqa: D401
        pass  # suppress access logs


def _start_sim_server() -> str:
    """Start a threaded local HTTP server and return its base URL."""
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _SimHandler)
    port = server.server_address[1]
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return f"http://127.0.0.1:{port}"


_SIM_URL: str | None = None


def _ensure_sim_server() -> str:
    global _SIM_URL
    if _SIM_URL is None:
        _SIM_URL = _start_sim_server()
    return _SIM_URL


# ---------------------------------------------------------------------------
# Payload generator
# ---------------------------------------------------------------------------
def _generate_payload(size_kb: int) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    target = size_kb * 1024
    rng = random.Random(42)
    return "".join(rng.choice(alphabet) for _ in range(target))


# ---------------------------------------------------------------------------
# Per-client metrics (shared by all modes, thread-safe)
# ---------------------------------------------------------------------------
@dataclass
class ClientMetrics:
    id: str
    mode: str
    profile: str
    target: int
    started: int = 0
    completed: int = 0
    errors: int = 0
    queue_full_errors: int = 0
    bp_severity: str = "healthy"
    permits_max: int | None = None
    permits_current: int = 0
    waiters: int = 0
    throughput: float = 0.0
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    lock: threading.Lock = field(default_factory=threading.Lock)

    @property
    def elapsed_s(self) -> float:
        end = self.end_time or time.time()
        return end - self.start_time

    def compute_throughput(self) -> float:
        e = self.elapsed_s
        t = self.completed / e if e > 0 else 0.0
        self.throughput = t
        return t


# ---------------------------------------------------------------------------
# Time-series snapshot
# ---------------------------------------------------------------------------
@dataclass
class Snapshot:
    time_s: float
    clients: list[dict[str, Any]]
    aggregate_throughput: float


snapshots: list[Snapshot] = []


# ═══════════════════════════════════════════════════════════════════════════
# MODE: sync  –  CamundaClient + ThreadPoolExecutor + manual activate/complete
# ═══════════════════════════════════════════════════════════════════════════
def _run_client_sync(
    metrics: ClientMetrics,
    process_definition_key: int,
    concurrency: int,
    stop: threading.Event,
    *,
    shared_client: CamundaClient | None = None,
) -> ClientMetrics:
    """Producer + consumer loop for one sync client. Updates ``metrics`` in place."""

    client = shared_client or CamundaClient(configuration={
        "CAMUNDA_SDK_LOG_LEVEL": "error",
        "CAMUNDA_SDK_BACKPRESSURE_PROFILE": PROFILE,
    })

    payload = ProcessInstanceCreationInstructionByKeyVariables.from_dict({"data": _generate_payload(PAYLOAD_SIZE_KB)})
    inflight: list[Future[Any]] = []
    inflight_lock = threading.Lock()
    done = threading.Event()

    # HTTP client for HANDLER_TYPE=http
    if HANDLER_TYPE == "http":
        sim_url = _ensure_sim_server()
        sync_http = httpx.Client()

    def _create_one() -> None:
        try:
            client.create_process_instance(
                data=ProcessCreationByKey(
                    process_definition_key=process_definition_key,
                    variables=payload,
                )
            )
            with metrics.lock:
                metrics.started += 1
        except Exception as exc:
            with metrics.lock:
                metrics.errors += 1
                if "queue full" in str(exc).lower():
                    metrics.queue_full_errors += 1

    def _producer() -> None:
        pool = ThreadPoolExecutor(max_workers=min(concurrency, 64))
        try:
            while not done.is_set() and not stop.is_set():
                with inflight_lock:
                    inflight[:] = [f for f in inflight if not f.done()]
                    slots = concurrency - len(inflight)
                if slots > 0 and metrics.started < metrics.target:
                    for _ in range(slots):
                        if metrics.started >= metrics.target:
                            break
                        fut = pool.submit(_create_one)
                        with inflight_lock:
                            inflight.append(fut)
                else:
                    time.sleep(0.005)
                if metrics.completed >= metrics.target:
                    break
        finally:
            pool.shutdown(wait=False)

    def _consumer() -> None:
        while not done.is_set() and not stop.is_set():
            if metrics.completed >= metrics.target:
                break
            try:
                result = client.activate_jobs(
                    data=JobActivationRequest(
                        type_="bp-test-job",
                        max_jobs_to_activate=ACTIVATE_BATCH,
                        timeout=5000,
                        worker=f"bp-multi-{metrics.id}",
                    )
                )
                if result and result.jobs:
                    for job in result.jobs:
                        try:
                            if HANDLER_TYPE == "http":
                                sync_http.get(sim_url)
                            elif HANDLER_LATENCY_S > 0:
                                time.sleep(_jittered_latency())
                            client.complete_job(
                                job_key=job.job_key,
                                data=JobCompletionRequest(),
                            )
                            with metrics.lock:
                                metrics.completed += 1
                        except Exception:
                            with metrics.lock:
                                metrics.errors += 1
            except Exception:
                with metrics.lock:
                    metrics.errors += 1
                time.sleep(0.01)

    def _state_updater() -> None:
        while not done.is_set() and not stop.is_set():
            if metrics.completed >= metrics.target:
                done.set()
                break
            bp = client._bp.get_state()
            metrics.bp_severity = str(bp["severity"])
            metrics.permits_max = bp["permits_max"]
            metrics.permits_current = bp["permits_current"]
            metrics.waiters = bp["waiters"]
            metrics.compute_throughput()
            time.sleep(0.05)

    threads = [
        threading.Thread(target=_producer, name=f"{metrics.id}-producer", daemon=True),
        threading.Thread(target=_consumer, name=f"{metrics.id}-consumer", daemon=True),
        threading.Thread(target=_state_updater, name=f"{metrics.id}-state", daemon=True),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    metrics.end_time = time.time()
    metrics.compute_throughput()

    bp = client._bp.get_state()
    metrics.bp_severity = str(bp["severity"])
    metrics.permits_max = bp["permits_max"]

    return metrics


# ═══════════════════════════════════════════════════════════════════════════
# MODE: async / thread  –  CamundaAsyncClient + asyncio producer + job worker
#
# Each client gets its own event loop running in a dedicated thread so that
# multiple independent async clients can coexist in the same process.
# ═══════════════════════════════════════════════════════════════════════════
def _run_client_async_or_thread(
    metrics: ClientMetrics,
    process_definition_key: int,
    concurrency: int,
    stop: threading.Event,
    worker_strategy: str,
) -> ClientMetrics:
    """Producer + job-worker loop for one async client.

    Runs a private ``asyncio`` event loop in the calling thread.
    """

    async def _run() -> None:
        async with CamundaAsyncClient(configuration={
            "CAMUNDA_SDK_LOG_LEVEL": "error",
            "CAMUNDA_SDK_BACKPRESSURE_PROFILE": PROFILE,
        }) as client:
            payload = ProcessInstanceCreationInstructionByKeyVariables.from_dict({"data": _generate_payload(PAYLOAD_SIZE_KB)})
            sem = asyncio.Semaphore(concurrency)
            done = asyncio.Event()

            # --- Job worker (consumer) ---
            if worker_strategy == "async":
                if HANDLER_TYPE == "http":
                    sim_url = _ensure_sim_server()
                    http_client = httpx.AsyncClient()

                    async def _async_handler(job: ConnectedJobContext) -> None:
                        await http_client.get(sim_url)
                        with metrics.lock:
                            metrics.completed += 1
                else:
                    async def _async_handler(job: ConnectedJobContext) -> None:
                        if HANDLER_LATENCY_S > 0:
                            await asyncio.sleep(_jittered_latency())
                        with metrics.lock:
                            metrics.completed += 1

                worker = client.create_job_worker(
                    config=WorkerConfig(
                        job_type="bp-test-job",
                        job_timeout_milliseconds=10_000,
                        max_concurrent_jobs=ACTIVATE_BATCH,
                        worker_name=f"bp-multi-{metrics.id}",
                    ),
                    callback=_async_handler,
                    execution_strategy="async",
                )
            else:  # thread
                if HANDLER_TYPE == "http":
                    sim_url = _ensure_sim_server()
                    sync_http = httpx.Client()

                    def _thread_handler(job: ConnectedJobContext) -> None:
                        sync_http.get(sim_url)
                        with metrics.lock:
                            metrics.completed += 1
                else:
                    def _thread_handler(job: ConnectedJobContext) -> None:
                        if HANDLER_LATENCY_S > 0:
                            time.sleep(_jittered_latency())
                        with metrics.lock:
                            metrics.completed += 1

                worker = client.create_job_worker(
                    config=WorkerConfig(
                        job_type="bp-test-job",
                        job_timeout_milliseconds=10_000,
                        max_concurrent_jobs=ACTIVATE_BATCH,
                        worker_name=f"bp-multi-{metrics.id}",
                    ),
                    callback=_thread_handler,
                    execution_strategy="thread",
                )

            # --- Producer (sequential with semaphore gating) ---
            async def _producer() -> None:
                while not done.is_set() and not stop.is_set():
                    with metrics.lock:
                        already_started = metrics.started
                    if already_started >= metrics.target:
                        break
                    async with sem:
                        # Re-check after acquiring the semaphore
                        with metrics.lock:
                            if metrics.started >= metrics.target:
                                break
                        try:
                            await client.create_process_instance(
                                data=ProcessCreationByKey(
                                    process_definition_key=process_definition_key,
                                    variables=payload,
                                )
                            )
                            with metrics.lock:
                                metrics.started += 1
                        except Exception as exc:
                            with metrics.lock:
                                metrics.errors += 1
                                if "queue full" in str(exc).lower():
                                    metrics.queue_full_errors += 1

            # --- State updater ---
            async def _state_updater() -> None:
                while not done.is_set() and not stop.is_set():
                    if metrics.completed >= metrics.target:
                        done.set()
                        return
                    bp = client._bp.get_state()
                    metrics.bp_severity = str(bp["severity"])
                    metrics.permits_max = bp["permits_max"]
                    metrics.permits_current = bp["permits_current"]
                    metrics.waiters = bp["waiters"]
                    metrics.compute_throughput()
                    await asyncio.sleep(0.05)

            # --- Global stop poller ---
            async def _stop_poller() -> None:
                """Check the threading.Event from other threads."""
                while not done.is_set():
                    if stop.is_set():
                        done.set()
                        return
                    await asyncio.sleep(0.1)

            producer_task = asyncio.create_task(_producer())
            state_task = asyncio.create_task(_state_updater())
            stop_task = asyncio.create_task(_stop_poller())

            await state_task  # exits when target reached or stop set

            producer_task.cancel()
            stop_task.cancel()
            worker.stop()

            try:
                await producer_task
            except asyncio.CancelledError:
                pass
            try:
                await stop_task
            except asyncio.CancelledError:
                pass

            # Final state
            bp = client._bp.get_state()
            metrics.bp_severity = str(bp["severity"])
            metrics.permits_max = bp["permits_max"]

    asyncio.run(_run())

    metrics.end_time = time.time()
    metrics.compute_throughput()

    return metrics


# ---------------------------------------------------------------------------
# Client runner dispatcher (runs in its own thread for each client)
# ---------------------------------------------------------------------------
def _run_client(
    metrics: ClientMetrics,
    process_definition_key: int,
    concurrency: int,
    stop: threading.Event,
) -> ClientMetrics:
    if MODE == "sync":
        return _run_client_sync(metrics, process_definition_key, concurrency, stop)
    else:
        return _run_client_async_or_thread(
            metrics, process_definition_key, concurrency, stop, worker_strategy=MODE,
        )


# ---------------------------------------------------------------------------
# Progress reporter
# ---------------------------------------------------------------------------
def report_progress(
    clients: list[ClientMetrics],
    t0: float,
    phase: str,
) -> None:
    now = time.time()
    elapsed = now - t0

    print(
        f"\n{_BOLD}[{elapsed:.1f}s] Phase: {phase}{_RESET}"
        f"  Clients: {len(clients)}  Mode: {MODE}  Profile: {PROFILE}"
    )
    header = (
        f"{_GRAY}  {'ID':<12}| {'Started':<8}| {'Done':<8}| "
        f"{'Thrpt':<8}| {'Severity':<10}| {'Permits':<12}| "
        f"{'Waiters':<8}| Errors{_RESET}"
    )
    print(header)
    print(f"{_GRAY}  {'-' * 85}{_RESET}")

    agg_throughput = 0.0
    snap_clients: list[dict[str, Any]] = []

    for m in clients:
        severity_str = SEVERITY_COLOURS.get(m.bp_severity, m.bp_severity)
        permits_str = (
            "unlimited" if m.permits_max is None else f"{m.permits_current}/{m.permits_max}"
        )
        agg_throughput += m.throughput
        qf = f" {_RED}({m.queue_full_errors} qfull){_RESET}" if m.queue_full_errors else ""

        print(
            f"  {m.id:<12}| {m.started:<8}| {m.completed:<8}| "
            f"{m.throughput:<8.1f}| {severity_str:<22}| {permits_str:<12}| "
            f"{m.waiters:<8}| {m.errors}{qf}"
        )

        snap_clients.append({
            "id": m.id,
            "severity": m.bp_severity,
            "permits_max": m.permits_max,
            "started": m.started,
            "completed": m.completed,
            "waiters": m.waiters,
            "throughput": m.throughput,
        })

    print(f"{_BOLD}  Aggregate throughput: {agg_throughput:.1f}/s{_RESET}")

    snapshots.append(Snapshot(
        time_s=elapsed,
        clients=snap_clients,
        aggregate_throughput=agg_throughput,
    ))


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
def print_summary(all_metrics: list[ClientMetrics]) -> None:
    print(f"\n{_BOLD}═══ Final Summary ═══{_RESET}")
    print(f"Mode: {MODE}  Profile: {PROFILE}  Clients: {len(all_metrics)}")
    print()

    print(
        f"  {'Client':<12} {'Target':>6} {'Started':>8} {'Done':>6} "
        f"{'Thrpt':>8} {'Duration':>9} {'Severity':>10} {'Permits':>10} "
        f"{'Errors':>6} {'QFull':>6}"
    )
    print(f"  {'-' * 95}")

    for m in all_metrics:
        dur = f"{m.elapsed_s:.1f}s"
        permits = "unlimited" if m.permits_max is None else str(m.permits_max)
        print(
            f"  {m.id:<12} {m.target:>6} {m.started:>8} {m.completed:>6} "
            f"{m.throughput:>7.1f}/s {dur:>9} {m.bp_severity:>10} {permits:>10} "
            f"{m.errors:>6} {m.queue_full_errors:>6}"
        )

    total_completed = sum(m.completed for m in all_metrics)
    total_errors = sum(m.errors for m in all_metrics)
    total_qfull = sum(m.queue_full_errors for m in all_metrics)
    durations = [m.elapsed_s for m in all_metrics]
    max_duration = max(durations) if durations else 0
    agg_throughput = total_completed / max_duration if max_duration > 0 else 0

    print(f"\n{_BOLD}Aggregates:{_RESET}")
    print(f"  Total completed:       {total_completed}")
    print(f"  Total errors:          {total_errors}")
    print(f"  Total queue-full:      {total_qfull}")
    print(f"  Wall-clock duration:   {max_duration:.1f}s")
    print(f"  Aggregate throughput:  {agg_throughput:.1f} ops/s")

    if len(all_metrics) > 1:
        completions = [float(m.completed) for m in all_metrics]
        sum_x = sum(completions)
        sum_x2 = sum(c * c for c in completions)
        n = len(completions)
        jain = (sum_x * sum_x) / (n * sum_x2) if sum_x2 > 0 else 1.0
        print(
            f"  Jain's fairness index: {jain:.3f} "
            f"(1.0 = perfectly fair, <0.8 = significant imbalance)"
        )

    # Time-series summary
    if snapshots:
        print(f"\n{_BOLD}Time-series (aggregate throughput):{_RESET}")
        step = max(1, len(snapshots) // 20)
        for i in range(0, len(snapshots), step):
            s = snapshots[i]
            bar = "█" * max(1, round(s.aggregate_throughput / 5))
            severities = "".join(c.get("severity", "?")[0] for c in s.clients)
            print(
                f"  {s.time_s:>5.0f}s | {s.aggregate_throughput:>7.1f}/s | {bar} [{severities}]"
            )


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------
def _cleanup() -> None:
    from camunda_orchestration_sdk.models.process_instance_search_query import (
        ProcessInstanceSearchQuery,
    )
    from camunda_orchestration_sdk.models.process_instance_search_query_filter import (
        ProcessInstanceSearchQueryFilter,
    )
    from camunda_orchestration_sdk.models.advanced_process_instance_state_filter import (
        AdvancedProcessInstanceStateFilter,
    )
    from camunda_orchestration_sdk.models.advanced_process_instance_state_filter_eq import (
        AdvancedProcessInstanceStateFilterEq,
    )
    from camunda_orchestration_sdk.models.limit_based_pagination import LimitBasedPagination

    print(f"{_GRAY}[multi-client] Cleaning up previous instances...{_RESET}")
    try:
        client = CamundaClient(configuration={"CAMUNDA_SDK_LOG_LEVEL": "error"})
        active = client.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_id="bp-test-process",
                    state=AdvancedProcessInstanceStateFilter(
                        eq=AdvancedProcessInstanceStateFilterEq("ACTIVE"),
                    ),
                ),
                page=LimitBasedPagination(limit=2000),
            )
        )
        if active.items:
            print(f"{_GRAY}[multi-client] Canceling {len(active.items)} instances...{_RESET}")
            for inst in active.items:
                try:
                    client.cancel_process_instance(
                        process_instance_key=inst.process_instance_key,
                        data=None,
                    )
                except Exception:
                    pass
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Subprocess isolation: poll progress JSON files from client_worker.py
# ---------------------------------------------------------------------------
CLIENT_WORKER_SCRIPT = Path(__file__).parent / "client_worker.py"


def _update_metrics_from_json(m: ClientMetrics, data: dict[str, Any]) -> None:
    """Overwrite a ClientMetrics object from a JSON dict written by client_worker.py."""
    with m.lock:
        m.started = data.get("started", m.started)
        m.completed = data.get("completed", m.completed)
        m.errors = data.get("errors", m.errors)
        m.queue_full_errors = data.get("queue_full_errors", m.queue_full_errors)
        m.bp_severity = data.get("bp_severity", m.bp_severity)
        m.permits_max = data.get("permits_max", m.permits_max)
        m.permits_current = data.get("permits_current", m.permits_current)
        m.waiters = data.get("waiters", m.waiters)
        m.throughput = data.get("throughput", m.throughput)


def _main_subprocess(proc_key: int) -> None:
    """Each client runs as a separate OS process — independent BackpressureManager.

    Uses barrier synchronisation so startup/import time is excluded from
    measurements and there is zero IPC during the timed portion.
    """

    work_dir = Path(tempfile.mkdtemp(prefix="bp-barrier-"))
    ready_dir = work_dir / "ready"
    results_dir = work_dir / "results"
    go_file = work_dir / "GO"
    stop_file = work_dir / "STOP"
    ready_dir.mkdir()
    results_dir.mkdir()

    # Base env for all workers
    base_env = os.environ.copy()
    base_env.update({
        "MODE": MODE,
        "TARGET": str(TARGET_PER_CLIENT),
        "CONCURRENCY": str(CLIENT_CONCURRENCY),
        "ACTIVATE_BATCH": str(ACTIVATE_BATCH),
        "HANDLER_TYPE": HANDLER_TYPE,
        "HANDLER_LATENCY_S": str(HANDLER_LATENCY_S),
        "PROFILE": PROFILE,
        "PAYLOAD_SIZE_KB": str(PAYLOAD_SIZE_KB),
        "PROCESS_DEFINITION_KEY": str(proc_key),
        "READY_DIR": str(ready_dir),
        "GO_FILE": str(go_file),
        "RESULTS_DIR": str(results_dir),
        "STOP_FILE": str(stop_file),
        "SCENARIO_TIMEOUT_S": str(SCENARIO_TIMEOUT_S),
    })

    def _spawn_batch(
        count: int, id_prefix: str, target: int,
    ) -> list[tuple[str, sp.Popen[str]]]:
        batch: list[tuple[str, sp.Popen[str]]] = []
        for i in range(count):
            cid = f"{id_prefix}-{i + 1}"
            env = base_env.copy()
            env["CLIENT_ID"] = cid
            env["TARGET"] = str(target)
            p = sp.Popen(
                [sys.executable, str(CLIENT_WORKER_SCRIPT)],
                env=env,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                text=True,
                cwd=str(REPO_ROOT),
            )
            batch.append((cid, p))
        return batch

    def _wait_ready(cids: list[str], timeout: float = 120) -> bool:
        deadline = time.time() + timeout
        needed = set(cids)
        while time.time() < deadline:
            ready = {f.name for f in ready_dir.iterdir()}
            if needed <= ready:
                return True
            time.sleep(0.1)
        missing = needed - {f.name for f in ready_dir.iterdir()}
        print(f"\n{_RED}  Workers failed to initialise within {timeout}s: {missing}{_RESET}")
        return False

    # ── Phase 1: Ramp-up ──
    print(f"\n{_BOLD}─── Phase 1: Ramp-up ({MODE} mode, subprocess/independent BP) ───{_RESET}")

    base_batch = _spawn_batch(NUM_CLIENTS, "client", TARGET_PER_CLIENT)
    base_cids = [cid for cid, _ in base_batch]

    print(f"  Spawned {NUM_CLIENTS} workers, waiting for initialisation...")
    if not _wait_ready(base_cids):
        stop_file.touch()
        for _, p in base_batch:
            p.kill()
        return

    # BARRIER: create GO file — workers start immediately
    go_file.touch()
    t0 = time.time()
    print(f"  {_GREEN}All {NUM_CLIENTS} workers ready — GO signal sent{_RESET}")

    # ── Phase 2: Spike (optional) ──
    spike_batch: list[tuple[str, sp.Popen[str]]] = []
    if SPIKE_CLIENTS > 0 and SPIKE_DELAY_S > 0:
        remaining_delay = SPIKE_DELAY_S - (time.time() - t0)
        if remaining_delay > 0:
            time.sleep(remaining_delay)

        if not stop_file.exists():
            print(f"\n{_BOLD}─── Phase 2: Spike (+{SPIKE_CLIENTS} clients, subprocess) ───{_RESET}")
            spike_batch = _spawn_batch(SPIKE_CLIENTS, "spike", SPIKE_TARGET)
            spike_cids = [cid for cid, _ in spike_batch]

            print(f"  Spawned {SPIKE_CLIENTS} spike workers, waiting for initialisation...")
            if _wait_ready(spike_cids):
                print(f"  {_GREEN}Spike workers ready — starting (GO already exists){_RESET}")

    # ── Wait for all workers to finish (ZERO IPC during test) ──
    all_procs = base_batch + spike_batch
    print(
        f"\n  Waiting for {len(all_procs)} workers to complete "
        f"(timeout: {SCENARIO_TIMEOUT_S}s, zero IPC during test)..."
    )

    deadline = t0 + SCENARIO_TIMEOUT_S + 30
    for _cid, p in all_procs:
        remaining_t = max(1, deadline - time.time())
        try:
            p.wait(timeout=remaining_t)
        except sp.TimeoutExpired:
            p.kill()
            p.wait(timeout=5)

    wall_clock = time.time() - t0

    # ── Collect results from JSON files ──
    all_metrics: list[ClientMetrics] = []

    for cid, p in all_procs:
        is_spike = cid.startswith("spike")
        target = SPIKE_TARGET if is_spike else TARGET_PER_CLIENT
        m = ClientMetrics(
            id=cid, mode=MODE, profile=PROFILE,
            target=target, start_time=t0,
        )

        results_file = results_dir / f"{cid}.json"
        if results_file.exists():
            try:
                data = json.loads(results_file.read_text())
                _update_metrics_from_json(m, data)
                if data.get("elapsed_s"):
                    m.end_time = t0 + data["elapsed_s"]
            except (json.JSONDecodeError, OSError):
                pass

        m.compute_throughput()
        all_metrics.append(m)

        # Print worker stdout
        stdout = p.stdout.read() if p.stdout else ""
        if stdout.strip():
            for line in stdout.strip().splitlines():
                print(f"  {line}")

    print_summary(all_metrics)

    # Cleanup temp dir
    import shutil
    shutil.rmtree(str(work_dir), ignore_errors=True)


# ---------------------------------------------------------------------------
# Shared-BP isolation: all workers share ONE client (one BackpressureManager)
# ---------------------------------------------------------------------------
def _main_shared(proc_key: int) -> None:
    """All workers share ONE client — shared BackpressureManager.

    Measures whether a single BackpressureManager coordinating all workers
    performs similarly to N independent BackpressureManagers (subprocess mode).
    """

    t0 = time.time()
    global_stop = threading.Event()
    all_metrics: list[ClientMetrics] = []

    for i in range(NUM_CLIENTS):
        cid = f"client-{i + 1}"
        m = ClientMetrics(
            id=cid, mode=MODE, profile=PROFILE,
            target=TARGET_PER_CLIENT, start_time=t0,
        )
        all_metrics.append(m)

    # Timeout guard
    def _timeout_guard() -> None:
        deadline = t0 + SCENARIO_TIMEOUT_S
        while not global_stop.is_set():
            if time.time() >= deadline:
                print(f"\n{_RED}SCENARIO TIMEOUT ({SCENARIO_TIMEOUT_S}s){_RESET}")
                global_stop.set()
                return
            time.sleep(0.5)

    threading.Thread(target=_timeout_guard, name="timeout", daemon=True).start()

    # Progress reporting
    progress_stop = threading.Event()

    def _progress_loop() -> None:
        while not progress_stop.is_set() and not global_stop.is_set():
            report_progress(
                all_metrics, t0,
                f"Shared ({NUM_CLIENTS} workers, {MODE})",
            )
            time.sleep(PROGRESS_INTERVAL_S)

    threading.Thread(target=_progress_loop, name="progress", daemon=True).start()

    # Aggregate completion watcher
    def _agg_watcher() -> None:
        while not global_stop.is_set():
            total_completed = sum(m.completed for m in all_metrics)
            total_target = sum(m.target for m in all_metrics)
            if total_completed >= total_target:
                global_stop.set()
                return
            time.sleep(0.1)

    threading.Thread(target=_agg_watcher, name="agg-watcher", daemon=True).start()

    print(f"\n{_BOLD}─── Shared BP ({MODE} mode, 1 client for {NUM_CLIENTS} workers) ───{_RESET}")

    if MODE == "sync":
        _run_shared_sync(proc_key, all_metrics, global_stop)
    else:
        _run_shared_async(proc_key, all_metrics, global_stop)

    progress_stop.set()
    global_stop.set()

    for m in all_metrics:
        if m.end_time is None:
            m.end_time = time.time()
        m.compute_throughput()

    print_summary(all_metrics)


def _run_shared_sync(
    proc_key: int,
    all_metrics: list[ClientMetrics],
    stop: threading.Event,
) -> None:
    """Sync shared: one CamundaClient, N worker threads."""

    shared_client = CamundaClient(configuration={
        "CAMUNDA_SDK_LOG_LEVEL": "error",
        "CAMUNDA_SDK_BACKPRESSURE_PROFILE": PROFILE,
    })

    threads: list[threading.Thread] = []
    for m in all_metrics:
        t = threading.Thread(
            target=_run_client_sync,
            args=(m, proc_key, CLIENT_CONCURRENCY, stop),
            kwargs={"shared_client": shared_client},
            name=m.id,
            daemon=True,
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join(timeout=SCENARIO_TIMEOUT_S)


def _run_shared_async(
    proc_key: int,
    all_metrics: list[ClientMetrics],
    global_stop: threading.Event,
) -> None:
    """Async/thread shared: one CamundaAsyncClient, N logical workers in one event loop."""

    worker_strategy = MODE  # "async" or "thread"

    async def _run() -> None:
        async with CamundaAsyncClient(configuration={
            "CAMUNDA_SDK_LOG_LEVEL": "error",
            "CAMUNDA_SDK_BACKPRESSURE_PROFILE": PROFILE,
        }) as client:
            payload = ProcessInstanceCreationInstructionByKeyVariables.from_dict(
                {"data": _generate_payload(PAYLOAD_SIZE_KB)}
            )
            done = asyncio.Event()

            # --- Job handler (completions round-robin across metrics) ---
            _comp_idx = [0]
            _comp_lock = threading.Lock()

            if worker_strategy == "async":
                if HANDLER_TYPE == "http":
                    sim_url = _ensure_sim_server()
                    http_client = httpx.AsyncClient()

                    async def _handler(job: ConnectedJobContext) -> None:
                        await http_client.get(sim_url)
                        with _comp_lock:
                            m = all_metrics[_comp_idx[0] % len(all_metrics)]
                            _comp_idx[0] += 1
                        with m.lock:
                            m.completed += 1
                else:
                    async def _handler(job: ConnectedJobContext) -> None:
                        if HANDLER_TYPE != "instant" and HANDLER_LATENCY_S > 0:
                            await asyncio.sleep(HANDLER_LATENCY_S)
                        with _comp_lock:
                            m = all_metrics[_comp_idx[0] % len(all_metrics)]
                            _comp_idx[0] += 1
                        with m.lock:
                            m.completed += 1

                worker = client.create_job_worker(
                    config=WorkerConfig(
                        job_type="bp-test-job",
                        job_timeout_milliseconds=10_000,
                        max_concurrent_jobs=ACTIVATE_BATCH * len(all_metrics),
                        worker_name="bp-shared",
                    ),
                    callback=_handler,
                    execution_strategy="async",
                )
            else:  # thread
                if HANDLER_TYPE == "http":
                    sim_url = _ensure_sim_server()
                    sync_http = httpx.Client()

                    def _handler_t(job: ConnectedJobContext) -> None:
                        sync_http.get(sim_url)
                        with _comp_lock:
                            m = all_metrics[_comp_idx[0] % len(all_metrics)]
                            _comp_idx[0] += 1
                        with m.lock:
                            m.completed += 1
                else:
                    def _handler_t(job: ConnectedJobContext) -> None:
                        if HANDLER_TYPE != "instant" and HANDLER_LATENCY_S > 0:
                            time.sleep(HANDLER_LATENCY_S)
                        with _comp_lock:
                            m = all_metrics[_comp_idx[0] % len(all_metrics)]
                            _comp_idx[0] += 1
                        with m.lock:
                            m.completed += 1

                worker = client.create_job_worker(
                    config=WorkerConfig(
                        job_type="bp-test-job",
                        job_timeout_milliseconds=10_000,
                        max_concurrent_jobs=ACTIVATE_BATCH * len(all_metrics),
                        worker_name="bp-shared",
                    ),
                    callback=_handler_t,
                    execution_strategy="thread",
                )

            # --- N producer tasks ---
            async def _producer(m: ClientMetrics) -> None:
                sem = asyncio.Semaphore(CLIENT_CONCURRENCY)
                while not done.is_set() and not global_stop.is_set():
                    with m.lock:
                        if m.started >= m.target:
                            break
                    async with sem:
                        with m.lock:
                            if m.started >= m.target:
                                break
                        try:
                            await client.create_process_instance(
                                data=ProcessCreationByKey(
                                    process_definition_key=proc_key,
                                    variables=payload,
                                )
                            )
                            with m.lock:
                                m.started += 1
                        except Exception as exc:
                            with m.lock:
                                m.errors += 1
                                if "queue full" in str(exc).lower():
                                    m.queue_full_errors += 1

            # --- State updater (shared BP state → all metrics) ---
            async def _state_updater() -> None:
                while not done.is_set() and not global_stop.is_set():
                    total = sum(m.completed for m in all_metrics)
                    target = sum(m.target for m in all_metrics)
                    if total >= target:
                        done.set()
                        return
                    bp = client._bp.get_state()
                    for m in all_metrics:
                        m.bp_severity = str(bp["severity"])
                        m.permits_max = bp["permits_max"]
                        m.permits_current = bp["permits_current"]
                        m.waiters = bp["waiters"]
                        m.compute_throughput()
                    await asyncio.sleep(0.05)

            # --- Stop poller (watches threading.Event) ---
            async def _stop_poller() -> None:
                while not done.is_set():
                    if global_stop.is_set():
                        done.set()
                        return
                    await asyncio.sleep(0.1)

            # Launch everything
            producer_tasks = [asyncio.create_task(_producer(m)) for m in all_metrics]
            state_task = asyncio.create_task(_state_updater())
            stop_task = asyncio.create_task(_stop_poller())

            await state_task

            for t in producer_tasks:
                t.cancel()
            stop_task.cancel()
            worker.stop()

            for t in producer_tasks:
                try:
                    await t
                except asyncio.CancelledError:
                    pass
            try:
                await stop_task
            except asyncio.CancelledError:
                pass

            # Final state
            bp = client._bp.get_state()
            for m in all_metrics:
                m.bp_severity = str(bp["severity"])
                m.permits_max = bp["permits_max"]
                m.end_time = time.time()
                m.compute_throughput()

    asyncio.run(_run())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print(f"\n{_BOLD}╔══════════════════════════════════════════════════════════╗{_RESET}")
    print(f"{_BOLD}║   Multi-Client Distributed Backpressure Scenario        ║{_RESET}")
    print(f"{_BOLD}╚══════════════════════════════════════════════════════════╝{_RESET}")
    print(f"  Isolation:      {ISOLATION}")
    print(f"  Mode:           {MODE}")
    print(f"  Clients:        {NUM_CLIENTS} base + {SPIKE_CLIENTS} spike")
    print(f"  Target/client:  {TARGET_PER_CLIENT} (spike: {SPIKE_TARGET})")
    print(f"  Concurrency:    {CLIENT_CONCURRENCY} per client")
    print(f"  Activate batch: {ACTIVATE_BATCH}")
    print(f"  Handler type:   {HANDLER_TYPE}")
    print(f"  Handler I/O:    {HANDLER_LATENCY_S}s")
    print(f"  Profile:        {PROFILE}")
    print(f"  Payload:        {PAYLOAD_SIZE_KB}KB per instance")
    print(f"  Spike delay:    {SPIKE_DELAY_S}s")
    print()

    _cleanup()

    # Deploy test process (use sync client for bootstrap)
    print(f"{_GRAY}[multi-client] Deploying test process...{_RESET}")
    bootstrap = CamundaClient(configuration={"CAMUNDA_SDK_LOG_LEVEL": "error"})
    bpmn_path = str(Path(__file__).parent / "resources" / "bp-test-process.bpmn")
    deployment = bootstrap.deploy_resources_from_files([bpmn_path])
    proc_key = deployment.processes[0].process_definition_key
    print(f"{_GRAY}[multi-client] Deployed: processDefinitionKey={proc_key}{_RESET}")

    if ISOLATION == "subprocess":
        _main_subprocess(proc_key)
    else:
        _main_shared(proc_key)


if __name__ == "__main__":
    main()
