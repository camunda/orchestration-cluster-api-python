"""
Single-Client Backpressure Scenario
====================================

Creates process instances with variable payloads while simultaneously servicing
jobs.  Measures throughput and observes the adaptive backpressure controller's
response.

The scenario can be run in three execution modes:

  **sync**    – ``CamundaClient`` (blocking).  A ``ThreadPoolExecutor`` fires
                ``create_process_instance`` calls.  A separate thread polls
                ``activate_jobs`` + ``complete_job`` in a loop.

  **async**   – ``CamundaAsyncClient`` (asyncio).  ``asyncio.Semaphore``-gated
                tasks fire ``create_process_instance``.  A job worker with the
                **async** execution strategy handles completions.

  **thread**  – ``CamundaAsyncClient`` (asyncio).  Same ``Semaphore``-gated
                producer as *async* mode, but the job worker uses the **thread**
                execution strategy (``ThreadPoolExecutor`` under the hood).

Environment variables
─────────────────────
  MODE                     sync | async | thread (default: async)
  TARGET                   Total completions to reach (default: 1000)
  START_CONCURRENCY        Max inflight createProcessInstance (default: 200)
  ACTIVATE_BATCH           maxJobsToActivate per poll / max_concurrent_jobs (default: 32)
  HANDLER_TYPE             sleep | http (default: sleep)
  HANDLER_LATENCY_S        Simulated I/O latency per job handler (default: 0.2)
  PAYLOAD_SIZE_KB          Variable payload size in KB (default: 10)
  PROGRESS_INTERVAL_S      Report interval in seconds (default: 0.25)
  SCENARIO_TIMEOUT_S       Hard timeout in seconds (default: 480)
  CAMUNDA_SDK_BACKPRESSURE_PROFILE   LEGACY | BALANCED (default: BALANCED)

Usage
─────
  # Run async mode (default), BALANCED profile
  uv run demo/v2/backpressure/single_client.py

  # Run thread-worker mode
  MODE=thread uv run demo/v2/backpressure/single_client.py

  # Run sync mode (manual activate+complete, no job worker)
  MODE=sync uv run demo/v2/backpressure/single_client.py

  # Compare LEGACY vs BALANCED in async mode
  CAMUNDA_SDK_BACKPRESSURE_PROFILE=LEGACY uv run demo/v2/backpressure/single_client.py
  CAMUNDA_SDK_BACKPRESSURE_PROFILE=BALANCED uv run demo/v2/backpressure/single_client.py

  # Short smoke test
  TARGET=100 START_CONCURRENCY=50 uv run demo/v2/backpressure/single_client.py
"""

from __future__ import annotations

import asyncio
import http.server
import os
import random
import sys
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

from camunda_orchestration_sdk import CamundaClient, CamundaAsyncClient, ProcessDefinitionKey  # noqa: E402
from camunda_orchestration_sdk.models.process_creation_by_key import ProcessCreationByKey  # noqa: E402
from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest  # noqa: E402
from camunda_orchestration_sdk.models.job_completion_request import JobCompletionRequest  # noqa: E402
from camunda_orchestration_sdk.models.process_instance_creation_instruction_by_key_variables import ProcessInstanceCreationInstructionByKeyVariables  # noqa: E402
from camunda_orchestration_sdk.runtime.job_worker import WorkerConfig, ConnectedJobContext  # noqa: E402

# ---------------------------------------------------------------------------
# Config (from env)
# ---------------------------------------------------------------------------
MODE = os.environ.get("MODE", "async").lower()
assert MODE in ("sync", "async", "thread"), f"MODE must be sync|async|thread, got {MODE!r}"

TARGET = int(os.environ.get("TARGET", "1000"))
START_CONCURRENCY = int(os.environ.get("START_CONCURRENCY", "200"))
ACTIVATE_BATCH = int(os.environ.get("ACTIVATE_BATCH", "32"))
HANDLER_TYPE = os.environ.get("HANDLER_TYPE", "sleep").lower()
assert HANDLER_TYPE in ("sleep", "http"), f"HANDLER_TYPE must be sleep|http, got {HANDLER_TYPE!r}"
HANDLER_LATENCY_S = float(os.environ.get("HANDLER_LATENCY_S", "0.2"))
PAYLOAD_SIZE_KB = int(os.environ.get("PAYLOAD_SIZE_KB", "10"))
PROGRESS_INTERVAL_S = float(os.environ.get("PROGRESS_INTERVAL_S", "0.25"))
SCENARIO_TIMEOUT_S = float(os.environ.get("SCENARIO_TIMEOUT_S", "480"))
PROFILE = os.environ.get("CAMUNDA_SDK_BACKPRESSURE_PROFILE", "BALANCED")

# ANSI colours (terminal only)
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
    """Tiny handler that sleeps for HANDLER_LATENCY_S then returns 200 OK."""

    def do_GET(self) -> None:
        time.sleep(HANDLER_LATENCY_S)
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


# Lazy-started; only created when HANDLER_TYPE=http
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
# Metrics (thread-safe)
# ---------------------------------------------------------------------------
@dataclass
class ScenarioMetrics:
    mode: str = ""
    profile: str = ""
    started: int = 0
    completed: int = 0
    errors: int = 0
    queue_full: int = 0
    t0: float = field(default_factory=time.time)
    lock: threading.Lock = field(default_factory=threading.Lock)

    @property
    def elapsed_s(self) -> float:
        return time.time() - self.t0

    @property
    def throughput(self) -> float:
        e = self.elapsed_s
        return self.completed / e if e > 0 else 0.0


# ---------------------------------------------------------------------------
# Progress reporter
# ---------------------------------------------------------------------------
def _write_progress(
    m: ScenarioMetrics,
    bp_state: dict[str, Any],
    *,
    tag: str = "",
) -> None:
    severity_str = SEVERITY_COLOURS.get(
        str(bp_state.get("severity", "?")), str(bp_state.get("severity", "?"))
    )
    permits_max = bp_state.get("permits_max")
    permits_cur = bp_state.get("permits_current", "?")
    permits_str = "unlimited" if permits_max is None else f"{permits_cur}/{permits_max}"
    waiters = bp_state.get("waiters", 0)

    line = (
        f"\r[bp] mode={m.mode} profile={m.profile}"
        f"  {_GREEN}started={m.started}/{TARGET}{_RESET}"
        f"  {_RED}completed={m.completed}/{TARGET}{_RESET}"
        f"  bp={severity_str}"
        f"  permits={permits_str}"
        f"  waiters={waiters}"
        f"  thrpt={m.throughput:.1f}/s"
        f"  elapsed={m.elapsed_s:.1f}s"
        f"  errors={m.errors}"
    )
    if tag:
        line += f"  {tag}"
    sys.stdout.write(line + "    ")
    sys.stdout.flush()


# ═══════════════════════════════════════════════════════════════════════════
# MODE: sync  –  CamundaClient + ThreadPoolExecutor + manual activate/complete
# ═══════════════════════════════════════════════════════════════════════════
def _run_sync(process_definition_key: ProcessDefinitionKey) -> dict[str, Any]:
    client = CamundaClient(configuration={
        "CAMUNDA_SDK_LOG_LEVEL": "error",
        "CAMUNDA_SDK_BACKPRESSURE_PROFILE": PROFILE,
    })
    payload = ProcessInstanceCreationInstructionByKeyVariables.from_dict({"data": _generate_payload(PAYLOAD_SIZE_KB)})
    metrics = ScenarioMetrics(mode="sync", profile=PROFILE, t0=time.time())
    done = threading.Event()

    # HTTP client for HANDLER_TYPE=http
    if HANDLER_TYPE == "http":
        sim_url = _ensure_sim_server()
        sync_http = httpx.Client()

    inflight: list[Future[Any]] = []
    inflight_lock = threading.Lock()

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
                    metrics.queue_full += 1

    def _producer() -> None:
        pool = ThreadPoolExecutor(max_workers=min(START_CONCURRENCY, 64))
        try:
            while not done.is_set():
                with inflight_lock:
                    inflight[:] = [f for f in inflight if not f.done()]
                    slots = START_CONCURRENCY - len(inflight)
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
        while not done.is_set():
            if metrics.completed >= TARGET:
                break
            try:
                result = client.activate_jobs(
                    data=JobActivationRequest(
                        type_="bp-test-job",
                        max_jobs_to_activate=ACTIVATE_BATCH,
                        timeout=5000,
                        worker="bp-single-sync",
                    )
                )
                if result and result.jobs:
                    for job in result.jobs:
                        try:
                            if HANDLER_TYPE == "http":
                                sync_http.get(sim_url)
                            elif HANDLER_LATENCY_S > 0:
                                time.sleep(HANDLER_LATENCY_S)
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

    def _progress() -> None:
        last = 0.0
        while not done.is_set():
            now = time.time()
            if now - last >= PROGRESS_INTERVAL_S:
                bp = client._bp.get_state()
                _write_progress(metrics, bp)
                last = now
            time.sleep(0.05)

    def _watcher() -> None:
        deadline = time.time() + SCENARIO_TIMEOUT_S
        while not done.is_set():
            if metrics.completed >= TARGET:
                done.set()
                return
            if time.time() >= deadline:
                print(f"\n{_RED}TIMEOUT after {SCENARIO_TIMEOUT_S}s{_RESET}")
                done.set()
                return
            time.sleep(0.05)

    threads = [
        threading.Thread(target=_producer, name="producer", daemon=True),
        threading.Thread(target=_consumer, name="consumer", daemon=True),
        threading.Thread(target=_progress, name="progress", daemon=True),
        threading.Thread(target=_watcher, name="watcher", daemon=True),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    bp = client._bp.get_state()
    _write_progress(metrics, bp, tag=f"{_BOLD}FINAL{_RESET}")
    print()

    return _make_result(metrics, bp)


# ═══════════════════════════════════════════════════════════════════════════
# MODE: async / thread  –  CamundaAsyncClient + asyncio producer + job worker
# ═══════════════════════════════════════════════════════════════════════════
def _run_async_or_thread(process_definition_key: ProcessDefinitionKey, worker_strategy: str) -> dict[str, Any]:
    """Shared runner for async and thread modes.

    ``worker_strategy`` is ``"async"`` or ``"thread"`` — passed as
    ``execution_strategy`` to ``create_job_worker``.
    """

    metrics = ScenarioMetrics(mode=worker_strategy, profile=PROFILE, t0=time.time())

    async def _run() -> dict[str, Any]:
        async with CamundaAsyncClient(configuration={
            "CAMUNDA_SDK_LOG_LEVEL": "error",
            "CAMUNDA_SDK_BACKPRESSURE_PROFILE": PROFILE,
        }) as client:
            payload = ProcessInstanceCreationInstructionByKeyVariables.from_dict({"data": _generate_payload(PAYLOAD_SIZE_KB)})
            sem = asyncio.Semaphore(START_CONCURRENCY)
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
                            await asyncio.sleep(HANDLER_LATENCY_S)
                        with metrics.lock:
                            metrics.completed += 1

                worker = client.create_job_worker(
                    config=WorkerConfig(
                        job_type="bp-test-job",
                        job_timeout_milliseconds=10_000,
                        max_concurrent_jobs=ACTIVATE_BATCH,
                        worker_name="bp-single-async",
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
                            time.sleep(HANDLER_LATENCY_S)
                        with metrics.lock:
                            metrics.completed += 1

                worker = client.create_job_worker(
                    config=WorkerConfig(
                        job_type="bp-test-job",
                        job_timeout_milliseconds=10_000,
                        max_concurrent_jobs=ACTIVATE_BATCH,
                        worker_name="bp-single-thread",
                    ),
                    callback=_thread_handler,
                    execution_strategy="thread",
                )

            # --- Producer (sequential with semaphore gating) ---

            async def _producer() -> None:
                while not done.is_set():
                    with metrics.lock:
                        already_started = metrics.started
                    if already_started >= TARGET:
                        break
                    async with sem:
                        # Re-check after acquiring the semaphore
                        with metrics.lock:
                            if metrics.started >= TARGET:
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
                                    metrics.queue_full += 1

            # --- Progress ---
            async def _progress() -> None:
                while not done.is_set():
                    bp = client._bp.get_state()
                    _write_progress(metrics, bp)
                    await asyncio.sleep(PROGRESS_INTERVAL_S)

            # --- Watcher ---
            async def _watcher() -> None:
                deadline = time.time() + SCENARIO_TIMEOUT_S
                while not done.is_set():
                    if metrics.completed >= TARGET:
                        done.set()
                        return
                    if time.time() >= deadline:
                        print(f"\n{_RED}TIMEOUT after {SCENARIO_TIMEOUT_S}s{_RESET}")
                        done.set()
                        return
                    await asyncio.sleep(0.05)

            producer_task = asyncio.create_task(_producer())
            progress_task = asyncio.create_task(_progress())
            watcher_task = asyncio.create_task(_watcher())

            await watcher_task

            producer_task.cancel()
            progress_task.cancel()
            worker.stop()

            try:
                await producer_task
            except asyncio.CancelledError:
                pass
            try:
                await progress_task
            except asyncio.CancelledError:
                pass

            bp = client._bp.get_state()
            _write_progress(metrics, bp, tag=f"{_BOLD}FINAL{_RESET}")
            print()

            return _make_result(metrics, bp)

    return asyncio.run(_run())


# ---------------------------------------------------------------------------
# Result builder
# ---------------------------------------------------------------------------
def _make_result(metrics: ScenarioMetrics, bp_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "mode": metrics.mode,
        "profile": metrics.profile,
        "duration_s": round(metrics.elapsed_s, 2),
        "started": metrics.started,
        "completed": metrics.completed,
        "throughput": round(metrics.throughput, 1),
        "errors": metrics.errors,
        "queue_full": metrics.queue_full,
        "final_severity": bp_state.get("severity"),
        "final_permits_max": bp_state.get("permits_max"),
    }


# ---------------------------------------------------------------------------
# Cleanup helper
# ---------------------------------------------------------------------------
def _cleanup() -> None:
    """Best-effort cancel leftover active process instances from previous runs."""
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

    print(f"{_GRAY}[bp-single] Cleaning up previous instances...{_RESET}")
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
            print(f"{_GRAY}[bp-single] Canceling {len(active.items)} instances...{_RESET}")
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
def main() -> None:
    print(f"\n{_BOLD}╔══════════════════════════════════════════════════════╗{_RESET}")
    print(f"{_BOLD}║   Single-Client Backpressure Scenario                ║{_RESET}")
    print(f"{_BOLD}╚══════════════════════════════════════════════════════╝{_RESET}")
    print(f"  Mode:          {MODE}")
    print(f"  Profile:       {PROFILE}")
    print(f"  Target:        {TARGET} completions")
    print(f"  Concurrency:   {START_CONCURRENCY} inflight")
    print(f"  Activate batch:{ACTIVATE_BATCH}")
    print(f"  Handler type:  {HANDLER_TYPE}")
    print(f"  Handler I/O:   {HANDLER_LATENCY_S}s")
    print(f"  Payload:       {PAYLOAD_SIZE_KB}KB")
    print()

    _cleanup()

    # Deploy test process (use sync client for bootstrap)
    print(f"{_GRAY}[bp-single] Deploying test process...{_RESET}")
    bootstrap = CamundaClient(configuration={"CAMUNDA_SDK_LOG_LEVEL": "error"})
    bpmn_path = str(Path(__file__).parent / "resources" / "bp-test-process.bpmn")
    deployment = bootstrap.deploy_resources_from_files([bpmn_path])
    proc_key = deployment.processes[0].process_definition_key
    print(f"{_GRAY}[bp-single] Deployed: processDefinitionKey={proc_key}{_RESET}")

    # Dispatch to the right mode
    print(f"\n{_BOLD}─── Running: mode={MODE}  profile={PROFILE} ───{_RESET}")
    if MODE == "sync":
        result = _run_sync(proc_key)
    else:
        result = _run_async_or_thread(proc_key, worker_strategy=MODE)

    # Summary
    print(f"\n{_BOLD}═══ Result ═══{_RESET}")
    for k, v in result.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
