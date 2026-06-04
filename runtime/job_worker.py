from __future__ import annotations
import asyncio
import inspect
import random
import threading
import functools
import attrs
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import (
    Callable,
    Literal,
    Any,
    TYPE_CHECKING,
    cast,
    Coroutine,
    Union,
    Tuple,
)
from dataclasses import dataclass
from .logging import SdkLogger, NullLogger, create_logger
from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest
from camunda_orchestration_sdk.models.activated_job_result import (
    ActivatedJobResult,
)
from camunda_orchestration_sdk.models.job_completion_request import JobCompletionRequest
from camunda_orchestration_sdk.models.job_completion_request_variables import (
    JobCompletionRequestVariables,
)
from camunda_orchestration_sdk.models.job_fail_request import JobFailRequest
from camunda_orchestration_sdk.models.job_error_request import JobErrorRequest
from camunda_orchestration_sdk.types import UNSET

if TYPE_CHECKING:
    from collections.abc import Mapping

    from camunda_orchestration_sdk import CamundaAsyncClient, CamundaClient

_EFFECTIVE_EXECUTION_STRATEGY = Literal["thread", "process", "async"]
EXECUTION_STRATEGY = _EFFECTIVE_EXECUTION_STRATEGY | Literal["auto"]

# Define action types for type narrowing
ActionComplete = Tuple[
    Literal["complete"], Union[dict[str, Any], JobCompletionRequest, None]
]
ActionFail = Tuple[Literal["fail"], Tuple[str, int | None, int, dict[str, Any] | None]]
ActionError = Tuple[Literal["error"], Tuple[str, str, dict[str, Any] | None]]
ActionSubprocessError = Tuple[Literal["subprocess_error"], str]

JobAction = Union[ActionComplete, ActionFail, ActionError, ActionSubprocessError]


@attrs.define
class JobContext(ActivatedJobResult):
    """Read-only context for a job execution.

    Attributes:
        log: A scoped logger bound to this job's context (job type, job key).
            Use ``job.log.info(...)`` etc. inside your handler to emit
            structured log messages.
    """

    log: SdkLogger = attrs.field(factory=lambda: SdkLogger(NullLogger()))

    @classmethod
    def from_job(
        cls, job: ActivatedJobResult, logger: SdkLogger | None = None
    ) -> "JobContext":
        # Extract init fields from the parent data class
        init_fields = {
            f.name: getattr(job, f.name)
            for f in attrs.fields(ActivatedJobResult)
            if f.init
        }
        if logger is not None:
            init_fields["log"] = logger
        return cls(**init_fields)


@attrs.define
class ConnectedJobContext(JobContext):
    """Context for **async** handlers — includes an async client reference.

    Extends :class:`JobContext` with a ``client`` attribute that provides
    access to the Camunda API from within an async job handler.  Use
    ``await job.client.method(...)`` to call API methods.

    This context is provided when the execution strategy is ``"async"``.
    For ``"thread"`` handlers, see :class:`SyncJobContext`.
    For ``"process"`` handlers, see :class:`JobContext`.
    """

    client: CamundaAsyncClient = attrs.field(kw_only=True, repr=False, eq=False)

    @classmethod
    def create(
        cls,
        job: ActivatedJobResult,
        client: Any,
        logger: SdkLogger | None = None,
    ) -> "ConnectedJobContext":
        init_fields = {
            f.name: getattr(job, f.name)
            for f in attrs.fields(ActivatedJobResult)
            if f.init
        }
        if logger is not None:
            init_fields["log"] = logger
        init_fields["client"] = client
        return cls(**init_fields)


# Backward-compatible alias
AsyncJobContext = ConnectedJobContext


@attrs.define
class SyncJobContext(JobContext):
    """Context for **thread** handlers — includes a sync client reference.

    Extends :class:`JobContext` with a ``client`` attribute that provides
    access to the Camunda API from within a synchronous (thread) handler.
    Call ``job.client.method(...)`` directly — no ``await`` needed.

    This context is provided when the execution strategy is ``"thread"``.
    For ``"async"`` handlers, see :class:`ConnectedJobContext`.
    For ``"process"`` handlers, see :class:`JobContext`.
    """

    client: CamundaClient = attrs.field(kw_only=True, repr=False, eq=False)

    @classmethod
    def create(
        cls,
        job: ActivatedJobResult,
        client: Any,
        logger: SdkLogger | None = None,
    ) -> "SyncJobContext":
        init_fields = {
            f.name: getattr(job, f.name)
            for f in attrs.fields(ActivatedJobResult)
            if f.init
        }
        if logger is not None:
            init_fields["log"] = logger
        init_fields["client"] = client
        return cls(**init_fields)


# ---------------------------------------------------------------------------
# Handler type aliases
# ---------------------------------------------------------------------------

# Handlers that accept ConnectedJobContext (async strategy).
ConnectedAsyncJobHandler = Callable[
    [ConnectedJobContext],
    Coroutine[Any, Any, dict[str, Any] | JobCompletionRequest | None],
]
# Handlers that accept SyncJobContext (thread strategy).
ConnectedSyncJobHandler = Callable[[SyncJobContext], dict[str, Any] | JobCompletionRequest | None]
ConnectedJobHandler = ConnectedAsyncJobHandler | ConnectedSyncJobHandler

# Handlers that accept only JobContext (process strategy).
# A handler typed with ConnectedJobContext will NOT satisfy this type.
IsolatedAsyncJobHandler = Callable[
    [JobContext], Coroutine[Any, Any, dict[str, Any] | JobCompletionRequest | None]
]
IsolatedSyncJobHandler = Callable[[JobContext], dict[str, Any] | JobCompletionRequest | None]
IsolatedJobHandler = IsolatedAsyncJobHandler | IsolatedSyncJobHandler

# Internal union — used by JobWorker internals.
JobHandler = ConnectedJobHandler | IsolatedJobHandler

# Keep the old names usable for backward compat in user code
AsyncJobHandler = IsolatedAsyncJobHandler
SyncJobHandler = IsolatedSyncJobHandler


@dataclass
class WorkerConfig:
    """User-facing configuration.

    Fields left as ``None`` inherit the global default from
    ``CAMUNDA_WORKER_*`` environment variables (or the client constructor),
    falling back to the hardcoded SDK default when neither is set.
    """

    job_type: str
    """Job type to activate and process."""
    job_timeout_milliseconds: int | None = None
    """How long the job is reserved for this worker only. Falls back to
    ``CAMUNDA_WORKER_TIMEOUT`` env var if not set."""
    request_timeout_milliseconds: int | None = None
    """Long-poll request timeout in milliseconds. Falls back to
    ``CAMUNDA_WORKER_REQUEST_TIMEOUT`` env var, then ``0``."""
    max_concurrent_jobs: int | None = None
    """Max jobs executing at once. Falls back to
    ``CAMUNDA_WORKER_MAX_CONCURRENT_JOBS`` env var, then ``10``."""
    fetch_variables: list[str] | None = None
    worker_name: str | None = None
    """Worker identifier. Falls back to ``CAMUNDA_WORKER_NAME`` env var,
    then ``"camunda-python-sdk-worker"``."""


def resolve_worker_config(
    config: WorkerConfig,
    configuration: Any,
) -> WorkerConfig:
    """Return a new WorkerConfig with ``None`` fields filled from *configuration*.

    Precedence: explicit field value > ``CAMUNDA_WORKER_*`` config > hardcoded default.
    Raises ``ValueError`` if ``job_timeout_milliseconds`` is still unset after merging.
    """

    job_timeout = config.job_timeout_milliseconds
    if job_timeout is None:
        job_timeout = getattr(configuration, "CAMUNDA_WORKER_TIMEOUT", None)
    if job_timeout is None:
        raise ValueError(
            "job_timeout_milliseconds is required: set it on WorkerConfig "
            "or via CAMUNDA_WORKER_TIMEOUT environment variable."
        )

    def _pick(explicit: Any, env_attr: str, default: Any) -> Any:
        if explicit is not None:
            return explicit
        env_val = getattr(configuration, env_attr, None)
        if env_val is not None:
            return env_val
        return default

    return WorkerConfig(
        job_type=config.job_type,
        job_timeout_milliseconds=job_timeout,
        request_timeout_milliseconds=_pick(
            config.request_timeout_milliseconds,
            "CAMUNDA_WORKER_REQUEST_TIMEOUT",
            0,
        ),
        max_concurrent_jobs=_pick(
            config.max_concurrent_jobs,
            "CAMUNDA_WORKER_MAX_CONCURRENT_JOBS",
            10,
        ),
        fetch_variables=config.fetch_variables,
        worker_name=_pick(
            config.worker_name,
            "CAMUNDA_WORKER_NAME",
            "camunda-python-sdk-worker",
        ),
    )


@dataclass
class _ResolvedWorkerConfig:
    """Internal config with all defaults applied (no Optional sentinels)."""

    job_type: str
    job_timeout_milliseconds: int
    request_timeout_milliseconds: int
    max_concurrent_jobs: int
    fetch_variables: list[str] | None
    worker_name: str


class JobError(Exception):
    """Raise this exception to throw a BPMN error."""

    def __init__(
        self,
        error_code: str,
        message: str = "",
        variables: dict[str, Any] | None = None,
    ):
        self.error_code = error_code
        self.message = message
        self.variables = variables
        super().__init__(f"JobError[{error_code}]: {message}")


class JobFailure(Exception):
    """Raise this exception to explicitly fail a job with custom retries/backoff."""

    def __init__(
        self,
        message: str,
        retries: int | None = None,
        retry_back_off: int = 0,
        variables: dict[str, Any] | None = None,
    ):
        self.message = message
        self.retries = retries
        self.retry_back_off = retry_back_off
        self.variables = variables
        super().__init__(f"JobFailure: {message}")


class _AckFlag:
    """Mutable flag shared between a job-scoped client wrapper and the worker dispatch."""

    __slots__ = ("value",)

    def __init__(self) -> None:
        self.value = False


class _JobScopedAsyncClient:
    """Wraps ``CamundaAsyncClient`` to detect when a job has been explicitly
    completed, failed, or errored by the handler \u2014 suppressing the worker's
    automatic completion for that job."""

    def __init__(
        self,
        client: "CamundaAsyncClient",
        job_key: str,
        ack: _AckFlag,
    ) -> None:
        object.__setattr__(self, "_inner", client)
        object.__setattr__(self, "_job_key", job_key)
        object.__setattr__(self, "_ack", ack)
        object.__setattr__(self, "__wrapped__", client)

    def __getattr__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "_inner"), name)

    async def complete_job(self, job_key: Any, **kwargs: Any) -> Any:
        result = await object.__getattribute__(self, "_inner").complete_job(
            job_key, **kwargs
        )
        if job_key == object.__getattribute__(self, "_job_key"):
            object.__getattribute__(self, "_ack").value = True
        return result

    async def fail_job(self, job_key: Any, **kwargs: Any) -> Any:
        result = await object.__getattribute__(self, "_inner").fail_job(
            job_key, **kwargs
        )
        if job_key == object.__getattribute__(self, "_job_key"):
            object.__getattribute__(self, "_ack").value = True
        return result

    async def throw_job_error(self, job_key: Any, **kwargs: Any) -> Any:
        result = await object.__getattribute__(self, "_inner").throw_job_error(
            job_key, **kwargs
        )
        if job_key == object.__getattribute__(self, "_job_key"):
            object.__getattribute__(self, "_ack").value = True
        return result


class _JobScopedSyncClient:
    """Sync equivalent of :class:`_JobScopedAsyncClient` for thread-strategy handlers."""

    def __init__(
        self,
        client: "CamundaClient",
        job_key: str,
        ack: _AckFlag,
    ) -> None:
        object.__setattr__(self, "_inner", client)
        object.__setattr__(self, "_job_key", job_key)
        object.__setattr__(self, "_ack", ack)
        object.__setattr__(self, "__wrapped__", client)

    def __getattr__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "_inner"), name)

    def complete_job(self, job_key: Any, **kwargs: Any) -> Any:
        result = object.__getattribute__(self, "_inner").complete_job(
            job_key, **kwargs
        )
        if job_key == object.__getattribute__(self, "_job_key"):
            object.__getattribute__(self, "_ack").value = True
        return result

    def fail_job(self, job_key: Any, **kwargs: Any) -> Any:
        result = object.__getattribute__(self, "_inner").fail_job(
            job_key, **kwargs
        )
        if job_key == object.__getattribute__(self, "_job_key"):
            object.__getattribute__(self, "_ack").value = True
        return result

    def throw_job_error(self, job_key: Any, **kwargs: Any) -> Any:
        result = object.__getattribute__(self, "_inner").throw_job_error(
            job_key, **kwargs
        )
        if job_key == object.__getattribute__(self, "_job_key"):
            object.__getattribute__(self, "_ack").value = True
        return result


def _execute_task_isolated(
    callback: JobHandler, job_context: JobContext
) -> JobAction | None:
    """
    Universal wrapper to execute a job in an isolated context (Thread or Process).
    Handles both sync and async callbacks by creating a fresh event loop for async code.
    Returns the result action to be executed by the main loop.
    """
    try:
        # Unwrap partials to find the real function for inspection
        actual_func = callback
        while isinstance(actual_func, functools.partial):
            actual_func = actual_func.func

        result = None
        if inspect.iscoroutinefunction(actual_func):
            # Async callback in isolated context: needs a fresh loop
            async_callback = cast(AsyncJobHandler, callback)
            result = asyncio.run(async_callback(job_context))
        else:
            # Sync callback: run directly
            sync_callback = cast(SyncJobHandler, callback)
            result = sync_callback(job_context)

        # If we got here, the job completed successfully
        return ("complete", result)

    except JobError as e:
        return ("error", (e.error_code, e.message, e.variables))
    except JobFailure as e:
        return ("fail", (e.message, e.retries, e.retry_back_off, e.variables))
    except Exception as e:
        # Catch-all for other exceptions -> Fail job
        return ("fail", (str(e), None, 0, None))


class JobWorker:
    _strategy: _EFFECTIVE_EXECUTION_STRATEGY = "async"

    def __init__(
        self,
        client: "CamundaAsyncClient",
        callback: JobHandler,
        config: WorkerConfig,
        logger: SdkLogger | None = None,
        execution_strategy: EXECUTION_STRATEGY = "auto",
        startup_jitter_max_seconds: float = 0,
    ):
        # Apply hardcoded defaults for any remaining None sentinels.
        # (env-var defaults are already applied by create_job_worker via
        # resolve_worker_config; this is the last fallback.)
        if config.job_timeout_milliseconds is None:
            raise ValueError(
                "job_timeout_milliseconds is required: set it on WorkerConfig "
                "or via CAMUNDA_WORKER_TIMEOUT environment variable."
            )
        resolved = _ResolvedWorkerConfig(
            job_type=config.job_type,
            job_timeout_milliseconds=config.job_timeout_milliseconds,
            request_timeout_milliseconds=config.request_timeout_milliseconds if config.request_timeout_milliseconds is not None else 0,
            max_concurrent_jobs=config.max_concurrent_jobs if config.max_concurrent_jobs is not None else 10,
            fetch_variables=config.fetch_variables,
            worker_name=config.worker_name if config.worker_name is not None else "camunda-python-sdk-worker",
        )

        self.callback = callback
        self.config = resolved
        self.client = client
        self._execution_strategy_override = execution_strategy
        self._startup_jitter_max_seconds = startup_jitter_max_seconds

        # Bind logger with context
        base_logger = logger if logger is not None else create_logger()
        self.logger = base_logger.bind(
            sdk="camunda_orchestration_sdk",
            worker=resolved.worker_name,
            job_type=resolved.job_type,
        )

        # Execution strategy detection
        self._strategy = self._determine_strategy()
        self._validate_strategy()

        # Sync client for thread strategy — created lazily on first job
        self._sync_client: "CamundaClient | None" = None

        # Resource pools — allocated lazily on first access so workers that
        # never use a given strategy don't pay its cost (see issue #148).
        # ProcessPoolExecutor in particular opens self-pipe FDs eagerly and
        # forks worker interpreters on first submit; we should only ever pay
        # that price if the worker actually runs jobs in the process strategy.
        self._thread_pool: ThreadPoolExecutor | None = None
        self._process_pool: ProcessPoolExecutor | None = None

        # Semaphore to limit concurrent executions
        self.semaphore = asyncio.Semaphore(resolved.max_concurrent_jobs)

        self.running = False
        self.polling_task = None

        self.active_jobs = 0
        self.lock = threading.Lock()

        # In-flight job tasks spawned by poll_loop. Tracked so stop()/
        # aclose() can cancel them deterministically before tearing down
        # the pools they're awaiting (issue #151). Without tracking, an
        # outstanding _execute_job that hits run_in_executor right after
        # close() would raise "cannot schedule new futures after shutdown"
        # or, post-#150, the use-after-close guard on the pool property.
        self._inflight_tasks: set[asyncio.Task[Any]] = set()

        # Set in close() under self.lock so concurrent close() calls are
        # idempotent and a single source-of-truth gates use-after-close in
        # the lazy property accessors. Without this, a close() racing a
        # property access could shut a pool down a microsecond before the
        # property creates a brand-new one — silently leaking the new one.
        self._closed = False

        # Dedicated event loop for async user code — also lazy. Each
        # asyncio.new_event_loop() opens a self-pipe (2 FDs), so we only
        # spin one up if something actually requests it.
        self._worker_loop: asyncio.AbstractEventLoop | None = None
        self._worker_thread: threading.Thread | None = None
        # Set by _run_worker_loop once asyncio.set_event_loop() has run
        # and the thread is about to enter run_forever(). close() waits
        # on this before stopping the loop, otherwise a close() that
        # races startup observes is_running()==False, never schedules
        # the stop callback, and leaks the loop + self-pipe FDs.
        self._worker_loop_started = threading.Event()

        self.logger.info(f"Using execution strategy: {self._strategy}")

    @property
    def thread_pool(self) -> ThreadPoolExecutor:
        # Double-checked locking: pool initialization must be one-shot even
        # under concurrent access (e.g. poll_loop spawning many _execute_job
        # tasks that all hit the property at once, or a sync caller racing
        # with an async caller). Without the lock two callers could both see
        # None, create separate executors, and leak the overwritten one.
        # _closed is checked under the lock so a property access that
        # races close() can't create a brand-new pool after teardown.
        if self._thread_pool is None:
            with self.lock:
                if self._closed:
                    raise RuntimeError("JobWorker is closed")
                if self._thread_pool is None:
                    self._thread_pool = ThreadPoolExecutor(
                        max_workers=self.config.max_concurrent_jobs
                    )
        return self._thread_pool

    @property
    def process_pool(self) -> ProcessPoolExecutor:
        if self._process_pool is None:
            with self.lock:
                if self._closed:
                    raise RuntimeError("JobWorker is closed")
                if self._process_pool is None:
                    self._process_pool = ProcessPoolExecutor(
                        max_workers=self.config.max_concurrent_jobs
                    )
        return self._process_pool

    @property
    def worker_loop(self) -> asyncio.AbstractEventLoop:
        if self._worker_loop is None:
            with self.lock:
                if self._closed:
                    raise RuntimeError("JobWorker is closed")
                if self._worker_loop is None:
                    loop = asyncio.new_event_loop()
                    thread = threading.Thread(
                        target=self._run_worker_loop, daemon=True
                    )
                    # Assign both before start() so _run_worker_loop never
                    # observes a partially initialized state.
                    self._worker_loop = loop
                    self._worker_thread = thread
                    thread.start()
        return self._worker_loop

    def _run_worker_loop(self):
        """Runs the dedicated event loop for async user code"""
        assert self._worker_loop is not None
        asyncio.set_event_loop(self._worker_loop)
        # Signal that the loop is fully owned by this thread and about to
        # start running. close() blocks on this so it can stop the loop
        # deterministically even if it races startup.
        self._worker_loop_started.set()
        self._worker_loop.run_forever()

    def _shutdown_pool(
        self,
        pool: ThreadPoolExecutor | ProcessPoolExecutor,
    ) -> bool:
        """Shut down an executor, avoiding self-join deadlocks.

        Returns True if the shutdown waited for tasks to finish, False if
        it had to fall back to a non-waiting shutdown because the caller
        is itself one of the pool's worker threads (where ``wait=True``
        would try to join the calling thread and raise RuntimeError).

        We catch RuntimeError rather than inspecting ``pool._threads``
        because the latter is unreliable across CPython versions
        (e.g. Python 3.13 may report an empty ``_threads`` set inside
        a running task).
        """
        try:
            pool.shutdown(wait=True, cancel_futures=True)
            return True
        except RuntimeError as exc:
            self.logger.warning(
                f"Pool shutdown(wait=True) raised {exc!r}; "
                "falling back to wait=False to avoid self-join deadlock. "
                "This typically means close()/stop() was called from "
                "within a pool worker thread (e.g. a sync job callback)."
            )
            pool.shutdown(wait=False, cancel_futures=True)
            return False

    def close(self) -> None:
        """Release any resources this worker lazily allocated.

        Safe to call multiple times and from multiple threads concurrently.
        Use as a context manager (``with JobWorker(...) as worker:``) or in
        a pytest fixture teardown to avoid leaking file descriptors across
        many short-lived worker instances (see issue #148).

        Blocks until pools have finished shutdown so file descriptors and
        worker processes are reliably released before the references are
        cleared. If invoked from inside a pool worker thread, falls back
        to a non-waiting shutdown for that pool to avoid a self-join
        deadlock. If invoked from the worker loop thread, skips joining
        the worker thread (same self-join hazard).

        After ``close()`` returns, accessing ``thread_pool``,
        ``process_pool``, or ``worker_loop`` raises ``RuntimeError``;
        a closed JobWorker cannot be reused.
        """
        # Atomically claim ownership of the teardown. A second concurrent
        # close() observes _closed=True and returns — without this guard,
        # two callers could each call self._worker_loop.close() and the
        # second would raise / leak the self-pipe FDs.
        with self.lock:
            if self._closed:
                return
            self._closed = True
            # Snapshot + null out under the lock so any racing property
            # accessor sees _closed and raises rather than handing back a
            # reference we're about to shut down.
            thread_pool = self._thread_pool
            process_pool = self._process_pool
            worker_loop = self._worker_loop
            worker_thread = self._worker_thread
            self._thread_pool = None
            self._process_pool = None

        # Heavy/blocking work happens outside the lock so lazy-init
        # callers don't block on a multi-second pool shutdown.
        if thread_pool is not None:
            self._shutdown_pool(thread_pool)
        if process_pool is not None:
            self._shutdown_pool(process_pool)

        if worker_loop is None:
            return

        # Wait for the loop thread to actually enter run_forever() before
        # trying to stop it. Without this, a close() that races startup
        # would never schedule the stop callback and would leak the loop.
        if not self._worker_loop_started.wait(timeout=1.0):
            self.logger.warning(
                "Worker loop thread did not start within timeout; "
                "leaving loop reference in place to avoid hiding the leak."
            )
            # Restore the references so a later operator inspection can
            # still find the leaked loop.
            with self.lock:
                self._worker_loop = worker_loop
                self._worker_thread = worker_thread
            return

        # call_soon_threadsafe is safe regardless of is_running(): the
        # callback is queued and processed once the loop runs. We've
        # already confirmed the loop has entered run_forever via the
        # started event.
        try:
            worker_loop.call_soon_threadsafe(worker_loop.stop)
        except RuntimeError as exc:
            # Loop was already closed by another caller; treat as
            # already-stopped.
            self.logger.debug(f"Worker loop already closed: {exc!r}")

        # Skip join() if close() was invoked from the worker thread itself
        # (e.g. an async callback running on worker_loop called
        # worker.close()). Joining the current thread would raise
        # RuntimeError — mirror of the pool self-join hazard.
        current = threading.current_thread()
        if (
            worker_thread is not None
            and worker_thread is not current
            and worker_thread.is_alive()
        ):
            worker_thread.join(timeout=1.0)

        thread_stopped = (
            worker_thread is None
            or worker_thread is current
            or not worker_thread.is_alive()
        )
        if thread_stopped:
            try:
                worker_loop.close()
            except Exception as exc:
                self.logger.warning(
                    f"Failed to close worker event loop: {exc!r}"
                )
                # Don't clear the started-event flag — the loop may still
                # be live and the reference is gone, so log and move on.
            finally:
                with self.lock:
                    self._worker_loop = None
                    self._worker_thread = None
                    self._worker_loop_started.clear()
        else:
            self.logger.warning(
                "Worker loop thread did not stop within timeout; "
                "leaving loop reference in place to avoid hiding the leak."
            )
            with self.lock:
                self._worker_loop = worker_loop
                self._worker_thread = worker_thread

    def __enter__(self) -> "JobWorker":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    async def __aenter__(self) -> "JobWorker":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.aclose()

    def _determine_strategy(self) -> _EFFECTIVE_EXECUTION_STRATEGY:
        """Determine execution strategy from explicit override or callback type."""
        # User explicitly configured?
        if self._execution_strategy_override != "auto":
            return self._execution_strategy_override

        # Unwrap partials to check the actual function
        actual_func = self.callback
        while isinstance(actual_func, functools.partial):
            actual_func = actual_func.func

        # Auto-detect based on function signature
        if inspect.iscoroutinefunction(actual_func):
            return "async"

        # Default to thread for sync functions (safe for most I/O work)
        return "thread"

    def _validate_strategy(self):
        """Ensure the strategy matches the callback type"""
        # Validation relaxed to allow dynamic exploration.
        pass

    def _get_sync_client(self) -> "CamundaClient":
        """Lazily create a sync CamundaClient for thread strategy handlers."""
        # Double-checked locking — same defect class as the thread/process
        # pool lazy init. Without the lock, two _execute_job calls in the
        # thread strategy can both observe None, both construct a
        # CamundaClient, and leak the overwritten one (along with its
        # httpx connection pool / FDs).
        if self._sync_client is None:
            with self.lock:
                if self._sync_client is None:
                    from camunda_orchestration_sdk import CamundaClient as _SyncClient
                    from camunda_orchestration_sdk.runtime.configuration_resolver import (
                        CamundaSdkConfigPartial,
                    )

                    self._sync_client = _SyncClient(
                        configuration=cast(
                            CamundaSdkConfigPartial,
                            self.client.configuration.model_dump(),
                        ),
                    )
        return self._sync_client

    def _decrement_active_jobs(self):
        with self.lock:
            self.active_jobs -= 1
            self.logger.trace(f"Active jobs: {self.active_jobs}")

    def start(self):
        if not self.running:
            self.running = True
            if self._startup_jitter_max_seconds > 0:
                jitter = random.uniform(0, self._startup_jitter_max_seconds)
                self.logger.info(f"Worker '{self.config.worker_name}' delaying start by {jitter:.2f}s (jitter)")
                self.polling_task = asyncio.create_task(self._start_with_jitter(jitter))
            else:
                self.polling_task = asyncio.create_task(self.poll_loop())
            self.logger.info(f"Worker '{self.config.worker_name}' started for type '{self.config.job_type}'")

    async def _start_with_jitter(self, jitter: float):
        await asyncio.sleep(jitter)
        await self.poll_loop()

    def stop(self):
        if self.running:
            self.running = False
            if self.polling_task:
                self.polling_task.cancel()

            # Cancel in-flight job tasks before tearing down the pools/
            # loop they may be awaiting. Cancellation is synchronous;
            # actual propagation happens on the next event-loop tick, so
            # async callers should prefer aclose() to also *await* the
            # cancellations before close() blocks on pool shutdown.
            for task in list(self._inflight_tasks):
                task.cancel()

            # Release all lazily allocated resources (pools, worker loop).
            # close() is idempotent and a no-op for anything that was never
            # allocated.
            self.close()

            self.logger.info(f"Worker '{self.config.worker_name}' stopped")

    async def aclose(self) -> None:
        """Async-aware teardown.

        Cancels any in-flight job tasks and awaits their cancellation
        (bounded by a timeout) before delegating to the synchronous
        ``close()``. Prefer this over ``stop()``/``close()`` from inside
        a running event loop — it gives cancelled tasks a chance to
        propagate before the pools they depend on are shut down, which
        prevents 'cannot schedule new futures after shutdown' (and the
        post-#150 'JobWorker is closed') errors from surfacing as task
        exceptions.
        """
        # Match stop()'s behaviour: flip running, cancel polling task.
        self.running = False
        if self.polling_task is not None and not self.polling_task.done():
            self.polling_task.cancel()
            try:
                await self.polling_task
            except asyncio.CancelledError:
                # Suppress only the polling task's expected cancellation.
                # If *our* task (aclose itself) was cancelled by the
                # caller, re-raise so the caller's cancellation is not
                # silently swallowed. ``Task.cancelling()`` (added in
                # Python 3.11) > 0 means cancel() was called on the
                # current task. On 3.10 the attribute is missing; treat
                # that as "no caller cancel" since we have no way to
                # tell — matches the prior behaviour on 3.10.
                current = asyncio.current_task()
                cancelling = getattr(current, "cancelling", lambda: 0)
                if cancelling() > 0:
                    raise
            except Exception:
                pass

        tasks = list(self._inflight_tasks)
        for task in tasks:
            task.cancel()
        if tasks:
            # Bounded wait so a misbehaving callback can't hang teardown.
            # We don't need the `done` set — only `pending` tells us
            # whether anything outlived the timeout.
            _, pending = await asyncio.wait(tasks, timeout=5.0)
            if pending:
                self.logger.warning(
                    f"{len(pending)} in-flight job task(s) did not cancel "
                    "within the aclose() timeout; proceeding with pool "
                    "shutdown — they may surface 'cannot schedule new "
                    "futures' errors."
                )

        self.close()
        self.logger.info("Worker closed (async)")

    async def poll_loop(self):
        """Background polling loop - always async"""
        while self.running:
            try:
                # Non-blocking HTTP poll using httpx
                jobs = await self._poll_for_jobs()

                # Spawn tasks for each job and track their handles so
                # stop()/aclose() can cancel them before tearing down the
                # pools they're awaiting (issue #151).
                if jobs:
                    for job in jobs:
                        task = asyncio.create_task(self._execute_job(job))
                        self._inflight_tasks.add(task)
                        task.add_done_callback(self._inflight_tasks.discard)

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error polling: {e}")

            await asyncio.sleep(1)  # Polling interval

    async def _poll_for_jobs(self):
        """SDK's async HTTP polling logic"""
        with self.lock:
            current_active = self.active_jobs

        capacity = self.config.max_concurrent_jobs - current_active
        if capacity <= 0:
            self.logger.trace("Max concurrent jobs reached, skipping poll")
            empty_jobs: list[ActivatedJobResult] = []
            return empty_jobs

        self.logger.debug(
            f"Polling for jobs of type {self.config.job_type} (capacity: {capacity} | request_timeout: {self.config.request_timeout_milliseconds})..."
        )
        jobsResult = await self.client.activate_jobs(
            data=JobActivationRequest(
                type_=self.config.job_type,
                timeout=self.config.job_timeout_milliseconds,
                max_jobs_to_activate=capacity,
                request_timeout=self.config.request_timeout_milliseconds,  # 0 means that the server will use its default timeout
                fetch_variable=self.config.fetch_variables
                if self.config.fetch_variables is not None
                else UNSET,
                worker=self.config.worker_name,
            )
        )
        self.logger.trace(f"Received {len(jobsResult.jobs)}")
        self.logger.trace(f"Jobs received: {[job.job_key for job in jobsResult.jobs]}")
        if jobsResult.jobs:
            with self.lock:
                self.active_jobs += len(jobsResult.jobs)
        return jobsResult.jobs  # Return list of jobs

    async def _execute_job(self, job_item: ActivatedJobResult):
        """Execute a single job with appropriate strategy"""

        # Create context with a job-scoped child logger
        job_logger = self.logger.bind(job_key=str(job_item.job_key))
        job_context: JobContext
        ack_flag = _AckFlag()
        if self._strategy == "async":
            wrapped_client = _JobScopedAsyncClient(self.client, job_item.job_key, ack_flag)
            job_context = ConnectedJobContext.create(
                job_item, client=wrapped_client, logger=job_logger
            )
        elif self._strategy == "thread":
            wrapped_sync = _JobScopedSyncClient(self._get_sync_client(), job_item.job_key, ack_flag)
            job_context = SyncJobContext.create(
                job_item, client=wrapped_sync, logger=job_logger
            )
        else:
            job_context = JobContext.from_job(job_item, logger=job_logger)

        # Unwrap partials to check the actual function
        actual_func = self.callback
        while isinstance(actual_func, functools.partial):
            actual_func = actual_func.func
        is_async_callback = inspect.iscoroutinefunction(actual_func)

        try:
            async with self.semaphore:  # Limit concurrent executions
                action: JobAction | None = None

                if self._strategy == "async":
                    # Run on the current event loop (same loop as the httpx client)
                    # so that job.client API calls work without cross-loop errors.
                    try:
                        result = None
                        if is_async_callback:
                            async_callback = cast(AsyncJobHandler, self.callback)
                            result = await async_callback(job_context)
                        else:
                            # Warning: Sync callback on Async strategy blocks the loop!
                            sync_callback = cast(SyncJobHandler, self.callback)
                            result = sync_callback(job_context)
                        action = ("complete", result)
                    except JobError as e:
                        action = ("error", (e.error_code, e.message, e.variables))
                    except JobFailure as e:
                        action = ("fail", (e.message, e.retries, e.retry_back_off, e.variables))
                    except Exception as e:
                        action = ("fail", (str(e), None, 0, None))

                elif self._strategy in ["thread", "process"]:
                    # Run in Pool (Isolated)
                    pool = (
                        self.thread_pool
                        if self._strategy == "thread"
                        else self.process_pool
                    )

                    action = await asyncio.get_event_loop().run_in_executor(
                        pool, _execute_task_isolated, self.callback, job_context
                    )

                # Handle the returned action
                if action:
                    if ack_flag.value:
                        job_logger.debug(
                            f"Job {job_context.job_key} already handled by handler; skipping auto-{action[0]}"
                        )
                    elif action[0] == "complete":
                        _, action_data = action
                        # Ensure data is in correct format
                        complete_data = JobCompletionRequest()
                        if isinstance(action_data, dict):
                            complete_data = JobCompletionRequest(
                                variables=JobCompletionRequestVariables.from_dict(
                                    cast("Mapping[str, Any]", action_data)
                                )
                            )
                        elif isinstance(action_data, JobCompletionRequest):
                            complete_data = action_data

                        await self.client.complete_job(
                            job_key=job_context.job_key, data=complete_data
                        )
                        self.logger.debug(f"Job completed: {job_context.job_key}")

                    elif action[0] == "fail":
                        _, (error_message, retries, retry_back_off, variables) = action
                        # Calculate retries if not provided
                        if retries is None:
                            retries = (
                                job_context.retries - 1
                                if job_context.retries > 0
                                else 0
                            )

                        fail_data = JobFailRequest(
                            error_message=error_message,
                            retries=retries,
                            retry_back_off=retry_back_off,
                        )
                        if variables is not None:
                            from camunda_orchestration_sdk.models.job_fail_request_variables import (
                                JobFailRequestVariables,
                            )

                            fail_data.variables = JobFailRequestVariables.from_dict(
                                variables
                            )

                        await self.client.fail_job(
                            job_key=job_context.job_key,
                            data=fail_data,
                        )
                        self.logger.info(
                            f"Job failed: {job_context.job_key} - {error_message}"
                        )

                    elif action[0] == "error":
                        _, (error_code, error_message, variables) = action
                        error_data = JobErrorRequest(
                            error_code=error_code, error_message=error_message
                        )
                        if variables is not None:
                            from camunda_orchestration_sdk.models.job_error_request_variables import (
                                JobErrorRequestVariables,
                            )

                            error_data.variables = JobErrorRequestVariables.from_dict(
                                variables
                            )

                        await self.client.throw_job_error(
                            job_key=job_context.job_key,
                            data=error_data,
                        )
                        self.logger.info(
                            f"Job error thrown: {job_context.job_key} - {error_code}"
                        )

                    elif action[0] == "subprocess_error":
                        _, error_details = action
                        # This is a system error in the worker infrastructure, not the job logic
                        raise RuntimeError(f"Worker execution error: {error_details}")

        except Exception as e:
            self.logger.error(f"System error executing job {job_item.job_key}: {e}")
            # Try to fail the job if possible
            try:
                await self.client.fail_job(
                    job_key=job_item.job_key,
                    data=JobFailRequest(
                        error_message=f"System error: {str(e)}",
                        retries=job_item.retries - 1 if job_item.retries else 0,
                    ),
                )
            except Exception:
                pass  # Best effort
        finally:
            self._decrement_active_jobs()
