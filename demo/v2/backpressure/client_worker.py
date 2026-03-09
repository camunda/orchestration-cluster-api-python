#!/usr/bin/env python3
"""
Single-Client Worker Process
=============================

Standalone script that runs ONE client (producer + consumer) against Camunda.
Designed to be spawned as a subprocess by ``multi_client.py`` so each client
gets its own Python interpreter — simulating an independent Docker container.

Barrier protocol
────────────────
  1. Worker starts, initialises SDK client, prepares payload.
  2. Worker writes a sentinel file to ``READY_DIR/<CLIENT_ID>`` to signal
     readiness.
  3. Worker polls for ``GO_FILE``: blocks until the orchestrator creates it.
  4. Worker resets its clock and runs the workload with **zero IPC** —
     no progress files, no polling.
  5. On completion (target reached or ``STOP_FILE`` appears or timeout) the
     worker writes ONE results JSON to ``RESULTS_DIR/<CLIENT_ID>.json``
     and exits.

This ensures startup / import / warm-up time is excluded from measurements
and there is no I/O overhead during the timed portion.

Environment variables (required)
────────────────────────────────
  CLIENT_ID                 Unique identifier for this worker (e.g. "client-1")
  PROCESS_DEFINITION_KEY    The deployed process definition key (string)
  READY_DIR                 Directory to write ready sentinel into
  GO_FILE                   Path to the start-signal file (created by orchestrator)
  RESULTS_DIR               Directory to write final results JSON into
  STOP_FILE                 Path to a sentinel file; when it exists, stop

Environment variables (tuning — same semantics as multi_client.py)
──────────────────────────────────────────────────────────────────
  MODE                      sync | async | thread  (default: async)
  TARGET                    Completion target for this client (default: 500)
  CONCURRENCY               Max inflight creations (default: 50)
  ACTIVATE_BATCH            Max jobs per poll / max_concurrent_jobs (default: 32)
  HANDLER_TYPE              sleep | http | instant  (default: sleep)
  HANDLER_LATENCY_S         Simulated I/O latency (default: 0.2)
  PROFILE                   Backpressure profile (default: BALANCED)
  PAYLOAD_SIZE_KB           Variable payload size in KB (default: 10)
  SCENARIO_TIMEOUT_S        Hard timeout in seconds (default: 300)
"""

from __future__ import annotations

import asyncio
import http.server
import json
import os
import random
import sys
import tempfile
import time
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from pathlib import Path
from typing import Any

import httpx

# ---------------------------------------------------------------------------
# Ensure the generated package is importable
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "generated"))

from camunda_orchestration_sdk import CamundaClient, CamundaAsyncClient, ProcessDefinitionKey  # noqa: E402
from camunda_orchestration_sdk.models.process_creation_by_key import ProcessCreationByKey  # noqa: E402
from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest  # noqa: E402
from camunda_orchestration_sdk.models.job_completion_request import JobCompletionRequest  # noqa: E402
from camunda_orchestration_sdk.models.process_instance_creation_instruction_by_key_variables import ProcessInstanceCreationInstructionByKeyVariables  # noqa: E402
from camunda_orchestration_sdk.runtime.job_worker import WorkerConfig, ConnectedJobContext  # noqa: E402


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
CLIENT_ID = os.environ["CLIENT_ID"]
PROCESS_DEFINITION_KEY = ProcessDefinitionKey(os.environ["PROCESS_DEFINITION_KEY"])
READY_DIR = Path(os.environ["READY_DIR"])
GO_FILE = Path(os.environ["GO_FILE"])
RESULTS_DIR = Path(os.environ["RESULTS_DIR"])
STOP_FILE = Path(os.environ["STOP_FILE"])

MODE = os.environ.get("MODE", "async").lower()
assert MODE in ("sync", "async", "thread"), f"MODE must be sync|async|thread, got {MODE!r}"

TARGET = int(os.environ.get("TARGET", "500"))
CONCURRENCY = int(os.environ.get("CONCURRENCY", "50"))
ACTIVATE_BATCH = int(os.environ.get("ACTIVATE_BATCH", "32"))
HANDLER_TYPE = os.environ.get("HANDLER_TYPE", "sleep").lower()
assert HANDLER_TYPE in ("sleep", "http", "instant"), f"HANDLER_TYPE must be sleep|http|instant, got {HANDLER_TYPE!r}"
HANDLER_LATENCY_S = float(os.environ.get("HANDLER_LATENCY_S", "0.2"))
HANDLER_JITTER = 0.5  # +/-50% uniform jitter on handler latency
PROFILE = os.environ.get("PROFILE", "BALANCED")


def _jittered_latency() -> float:
    """Return HANDLER_LATENCY_S with uniform jitter (+/-HANDLER_JITTER)."""
    return HANDLER_LATENCY_S * (1.0 + random.uniform(-HANDLER_JITTER, HANDLER_JITTER))
PAYLOAD_SIZE_KB = int(os.environ.get("PAYLOAD_SIZE_KB", "10"))
SCENARIO_TIMEOUT_S = float(os.environ.get("SCENARIO_TIMEOUT_S", "300"))


# ---------------------------------------------------------------------------
# Metrics (thread-safe)
# ---------------------------------------------------------------------------
class Metrics:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.started = 0
        self.completed = 0
        self.errors = 0
        self.queue_full_errors = 0
        self.bp_severity = "healthy"
        self.permits_max: int | None = None
        self.permits_current = 0
        self.waiters = 0
        self.throughput = 0.0
        self.start_time = time.time()
        self.end_time: float | None = None

    @property
    def elapsed_s(self) -> float:
        end = self.end_time or time.time()
        return end - self.start_time

    def compute_throughput(self) -> float:
        e = self.elapsed_s
        t = self.completed / e if e > 0 else 0.0
        self.throughput = t
        return t

    def to_dict(self, status: str = "running") -> dict[str, Any]:
        return {
            "status": status,
            "client_id": CLIENT_ID,
            "started": self.started,
            "completed": self.completed,
            "errors": self.errors,
            "queue_full_errors": self.queue_full_errors,
            "bp_severity": self.bp_severity,
            "permits_max": self.permits_max,
            "permits_current": self.permits_current,
            "waiters": self.waiters,
            "throughput": self.throughput,
            "elapsed_s": self.elapsed_s,
            "target": TARGET,
        }


metrics = Metrics()


# ---------------------------------------------------------------------------
# Barrier helpers
# ---------------------------------------------------------------------------
def write_ready_signal() -> None:
    """Signal the orchestrator that this worker is initialised and waiting."""
    sentinel = READY_DIR / CLIENT_ID
    sentinel.write_text("")


def wait_for_go() -> None:
    """Block until the orchestrator creates GO_FILE (busy-poll, 10 ms)."""
    while not GO_FILE.exists():
        time.sleep(0.01)


def write_results(status: str = "done") -> None:
    """Write a single results JSON — the ONLY file I/O during shutdown."""
    data = metrics.to_dict(status)
    results_file = RESULTS_DIR / f"{CLIENT_ID}.json"
    fd, tmp = tempfile.mkstemp(dir=str(RESULTS_DIR), suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(data, f)
    os.replace(tmp, str(results_file))


# ---------------------------------------------------------------------------
# Stop-signal / timeout checker
# ---------------------------------------------------------------------------
def should_stop() -> bool:
    if STOP_FILE.exists():
        return True
    if metrics.elapsed_s >= SCENARIO_TIMEOUT_S:
        return True
    return False


# ---------------------------------------------------------------------------
# Sim server (for HANDLER_TYPE=http)
# ---------------------------------------------------------------------------
class _SimHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        time.sleep(_jittered_latency())
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def log_message(self, *_args: object) -> None:
        pass


_SIM_URL: str | None = None


def _ensure_sim_server() -> str:
    global _SIM_URL
    if _SIM_URL is None:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _SimHandler)
        port = server.server_address[1]
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        _SIM_URL = f"http://127.0.0.1:{port}"
    return _SIM_URL


# ---------------------------------------------------------------------------
# Payload
# ---------------------------------------------------------------------------
def _generate_payload(size_kb: int) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    target = size_kb * 1024
    rng = random.Random(42)
    return "".join(rng.choice(alphabet) for _ in range(target))


# ═══════════════════════════════════════════════════════════════════════════
# SYNC mode
# ═══════════════════════════════════════════════════════════════════════════
def run_sync() -> None:
    client = CamundaClient(configuration={
        "CAMUNDA_SDK_LOG_LEVEL": "error",
        "CAMUNDA_SDK_BACKPRESSURE_PROFILE": PROFILE,
    })

    payload = ProcessInstanceCreationInstructionByKeyVariables.from_dict(
        {"data": _generate_payload(PAYLOAD_SIZE_KB)}
    )
    inflight: list[Future[Any]] = []
    inflight_lock = threading.Lock()
    done = threading.Event()

    if HANDLER_TYPE == "http":
        sim_url = _ensure_sim_server()
        sync_http = httpx.Client()

    def _create_one() -> None:
        try:
            client.create_process_instance(
                data=ProcessCreationByKey(
                    process_definition_key=PROCESS_DEFINITION_KEY,
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
        pool = ThreadPoolExecutor(max_workers=min(CONCURRENCY, 64))
        try:
            while not done.is_set() and not should_stop():
                with inflight_lock:
                    inflight[:] = [f for f in inflight if not f.done()]
                    slots = CONCURRENCY - len(inflight)
                if slots > 0 and metrics.started < TARGET:
                    for _ in range(slots):
                        if metrics.started >= TARGET:
                            break
                        fut = pool.submit(_create_one)
                        with inflight_lock:
                            inflight.append(fut)
                else:
                    time.sleep(0.005)
                if metrics.completed >= TARGET:
                    break
        finally:
            pool.shutdown(wait=False)

    def _consumer() -> None:
        while not done.is_set() and not should_stop():
            if metrics.completed >= TARGET:
                break
            try:
                result = client.activate_jobs(
                    data=JobActivationRequest(
                        type_="bp-test-job",
                        max_jobs_to_activate=ACTIVATE_BATCH,
                        timeout=5000,
                        worker=f"bp-worker-{CLIENT_ID}",
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
        while not done.is_set() and not should_stop():
            if metrics.completed >= TARGET:
                done.set()
                break
            bp = client._bp.get_state()
            metrics.bp_severity = str(bp["severity"])
            metrics.permits_max = bp["permits_max"]  # type: ignore[assignment]
            metrics.permits_current = bp["permits_current"]  # type: ignore[assignment]
            metrics.waiters = bp["waiters"]  # type: ignore[assignment]
            metrics.compute_throughput()
            time.sleep(0.05)

    threads = [
        threading.Thread(target=_producer, name=f"{CLIENT_ID}-producer", daemon=True),
        threading.Thread(target=_consumer, name=f"{CLIENT_ID}-consumer", daemon=True),
        threading.Thread(target=_state_updater, name=f"{CLIENT_ID}-state", daemon=True),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# ═══════════════════════════════════════════════════════════════════════════
# ASYNC / THREAD mode
# ═══════════════════════════════════════════════════════════════════════════
def run_async_or_thread() -> None:
    worker_strategy = MODE  # "async" or "thread"

    async def _run() -> None:
        async with CamundaAsyncClient(configuration={
            "CAMUNDA_SDK_LOG_LEVEL": "error",
            "CAMUNDA_SDK_BACKPRESSURE_PROFILE": PROFILE,
        }) as client:
            payload = ProcessInstanceCreationInstructionByKeyVariables.from_dict(
                {"data": _generate_payload(PAYLOAD_SIZE_KB)}
            )
            sem = asyncio.Semaphore(CONCURRENCY)
            done_event = asyncio.Event()

            # --- Job worker (consumer) ---
            if worker_strategy == "async":
                if HANDLER_TYPE == "http":
                    sim_url = _ensure_sim_server()
                    http_client = httpx.AsyncClient()

                    async def _handler(job: ConnectedJobContext) -> None:
                        await http_client.get(sim_url)
                        with metrics.lock:
                            metrics.completed += 1
                else:
                    async def _handler(job: ConnectedJobContext) -> None:
                        if HANDLER_LATENCY_S > 0:
                            await asyncio.sleep(_jittered_latency())
                        with metrics.lock:
                            metrics.completed += 1

                worker = client.create_job_worker(
                    config=WorkerConfig(
                        job_type="bp-test-job",
                        job_timeout_milliseconds=10_000,
                        max_concurrent_jobs=ACTIVATE_BATCH,
                        worker_name=f"bp-worker-{CLIENT_ID}",
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
                        with metrics.lock:
                            metrics.completed += 1
                else:
                    def _handler_t(job: ConnectedJobContext) -> None:
                        if HANDLER_LATENCY_S > 0:
                            time.sleep(_jittered_latency())
                        with metrics.lock:
                            metrics.completed += 1

                worker = client.create_job_worker(
                    config=WorkerConfig(
                        job_type="bp-test-job",
                        job_timeout_milliseconds=10_000,
                        max_concurrent_jobs=ACTIVATE_BATCH,
                        worker_name=f"bp-worker-{CLIENT_ID}",
                    ),
                    callback=_handler_t,
                    execution_strategy="thread",
                )

            # --- Producer ---
            async def _producer() -> None:
                while not done_event.is_set() and not should_stop():
                    with metrics.lock:
                        already = metrics.started
                    if already >= TARGET:
                        break
                    async with sem:
                        with metrics.lock:
                            if metrics.started >= TARGET:
                                break
                        try:
                            await client.create_process_instance(
                                data=ProcessCreationByKey(
                                    process_definition_key=PROCESS_DEFINITION_KEY,
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
                while not done_event.is_set() and not should_stop():
                    if metrics.completed >= TARGET:
                        done_event.set()
                        return
                    bp = client._bp.get_state()
                    metrics.bp_severity = str(bp["severity"])
                    metrics.permits_max = bp["permits_max"]  # type: ignore[assignment]
                    metrics.permits_current = bp["permits_current"]  # type: ignore[assignment]
                    metrics.waiters = bp["waiters"]  # type: ignore[assignment]
                    metrics.compute_throughput()
                    await asyncio.sleep(0.05)

            # --- Stop poller ---
            async def _stop_poller() -> None:
                while not done_event.is_set():
                    if should_stop():
                        done_event.set()
                        return
                    await asyncio.sleep(0.1)

            producer_task = asyncio.create_task(_producer())
            state_task = asyncio.create_task(_state_updater())
            stop_task = asyncio.create_task(_stop_poller())

            await state_task

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

            bp = client._bp.get_state()
            metrics.bp_severity = str(bp["severity"])
            metrics.permits_max = bp["permits_max"]  # type: ignore[assignment]

    asyncio.run(_run())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    # --- Barrier: signal ready, wait for GO, then reset clock ---
    write_ready_signal()
    wait_for_go()
    metrics.start_time = time.time()

    if MODE == "sync":
        run_sync()
    else:
        run_async_or_thread()

    metrics.end_time = time.time()
    metrics.compute_throughput()

    # --- Write ONE results file (only I/O the orchestrator reads) ---
    write_results(status="done")

    print(
        f"[{CLIENT_ID}] mode={MODE} profile={PROFILE} "
        f"target={TARGET} started={metrics.started} completed={metrics.completed} "
        f"errors={metrics.errors} queue_full={metrics.queue_full_errors} "
        f"throughput={metrics.throughput:.1f}/s elapsed={metrics.elapsed_s:.1f}s "
        f"severity={metrics.bp_severity} permits_max={metrics.permits_max}"
    )


if __name__ == "__main__":
    main()
