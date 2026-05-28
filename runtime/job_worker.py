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
ActionFail = Tuple[Literal["fail"], Tuple[str, int | None, int]]
ActionError = Tuple[Literal["error"], Tuple[str, str]]
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

    client: "CamundaAsyncClient" = attrs.field(kw_only=True, repr=False, eq=False)

    @classmethod
    def create(
        cls,
        job: ActivatedJobResult,
        client: "CamundaAsyncClient",
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

    client: "CamundaClient" = attrs.field(kw_only=True, repr=False, eq=False)

    @classmethod
    def create(
        cls,
        job: ActivatedJobResult,
        client: "CamundaClient",
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

    def __init__(self, error_code: str, message: str = ""):
        self.error_code = error_code
        self.message = message
        super().__init__(f"JobError[{error_code}]: {message}")


class JobFailure(Exception):
    """Raise this exception to explicitly fail a job with custom retries/backoff."""

    def __init__(
        self, message: str, retries: int | None = None, retry_back_off: int = 0
    ):
        self.message = message
        self.retries = retries
        self.retry_back_off = retry_back_off
        super().__init__(f"JobFailure: {message}")


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
        return ("error", (e.error_code, e.message))
    except JobFailure as e:
        return ("fail", (e.message, e.retries, e.retry_back_off))
    except Exception as e:
        # Catch-all for other exceptions -> Fail job
        return ("fail", (str(e), None, 0))


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

        # Dedicated event loop for async user code — also lazy. Each
        # asyncio.new_event_loop() opens a self-pipe (2 FDs), so we only
        # spin one up if something actually requests it.
        self._worker_loop: asyncio.AbstractEventLoop | None = None
        self._worker_thread: threading.Thread | None = None

        self.logger.info(f"Using execution strategy: {self._strategy}")

    @property
    def thread_pool(self) -> ThreadPoolExecutor:
        if self._thread_pool is None:
            self._thread_pool = ThreadPoolExecutor(
                max_workers=self.config.max_concurrent_jobs
            )
        return self._thread_pool

    @property
    def process_pool(self) -> ProcessPoolExecutor:
        if self._process_pool is None:
            self._process_pool = ProcessPoolExecutor(
                max_workers=self.config.max_concurrent_jobs
            )
        return self._process_pool

    @property
    def worker_loop(self) -> asyncio.AbstractEventLoop:
        if self._worker_loop is None:
            self._worker_loop = asyncio.new_event_loop()
            self._worker_thread = threading.Thread(
                target=self._run_worker_loop, daemon=True
            )
            self._worker_thread.start()
        return self._worker_loop

    def _run_worker_loop(self):
        """Runs the dedicated event loop for async user code"""
        assert self._worker_loop is not None
        asyncio.set_event_loop(self._worker_loop)
        self._worker_loop.run_forever()

    def close(self) -> None:
        """Release any resources this worker lazily allocated.

        Safe to call multiple times. Use as a context manager
        (``with JobWorker(...) as worker:``) or in a pytest fixture
        teardown to avoid leaking file descriptors across many short-lived
        worker instances (see issue #148).

        Blocks until pools have finished shutdown so file descriptors and
        worker processes are reliably released before the references are
        cleared.
        """
        if self._thread_pool is not None:
            self._thread_pool.shutdown(wait=True, cancel_futures=True)
            self._thread_pool = None
        if self._process_pool is not None:
            self._process_pool.shutdown(wait=True, cancel_futures=True)
            self._process_pool = None
        if self._worker_loop is not None:
            if self._worker_loop.is_running():
                self._worker_loop.call_soon_threadsafe(self._worker_loop.stop)
            if self._worker_thread is not None and self._worker_thread.is_alive():
                self._worker_thread.join(timeout=1.0)
            # Only close + clear the loop if the worker thread actually
            # stopped. Otherwise we'd leak the self-pipe FDs *and* hide the
            # failure by dropping the references. Log so the leak is
            # diagnosable.
            thread_stopped = (
                self._worker_thread is None or not self._worker_thread.is_alive()
            )
            if thread_stopped:
                try:
                    self._worker_loop.close()
                except Exception as exc:
                    self.logger.warning(
                        f"Failed to close worker event loop: {exc!r}"
                    )
                else:
                    self._worker_loop = None
                    self._worker_thread = None
            else:
                self.logger.warning(
                    "Worker loop thread did not stop within timeout; "
                    "leaving loop reference in place to avoid hiding the leak."
                )

    def __enter__(self) -> "JobWorker":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    async def __aenter__(self) -> "JobWorker":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

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
                self.logger.info(f"Delaying worker start by {jitter:.2f}s (jitter)")
                self.polling_task = asyncio.create_task(self._start_with_jitter(jitter))
            else:
                self.polling_task = asyncio.create_task(self.poll_loop())
            self.logger.info("Worker started")

    async def _start_with_jitter(self, jitter: float):
        await asyncio.sleep(jitter)
        await self.poll_loop()

    def stop(self):
        if self.running:
            self.running = False
            if self.polling_task:
                self.polling_task.cancel()

            # Release all lazily allocated resources (pools, worker loop).
            # close() is idempotent and a no-op for anything that was never
            # allocated.
            self.close()

            self.logger.info("Worker stopped")

    async def poll_loop(self):
        """Background polling loop - always async"""
        while self.running:
            try:
                # Non-blocking HTTP poll using httpx
                jobs = await self._poll_for_jobs()

                # Spawn tasks for each job
                if jobs:
                    tasks = [self._execute_job(job) for job in jobs]
                    # Don't await - let them run in background
                    for task in tasks:
                        asyncio.create_task(task)

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
        if self._strategy == "async":
            job_context = ConnectedJobContext.create(
                job_item, client=self.client, logger=job_logger
            )
        elif self._strategy == "thread":
            job_context = SyncJobContext.create(
                job_item, client=self._get_sync_client(), logger=job_logger
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
                        action = ("error", (e.error_code, e.message))
                    except JobFailure as e:
                        action = ("fail", (e.message, e.retries, e.retry_back_off))
                    except Exception as e:
                        action = ("fail", (str(e), None, 0))

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
                    if action[0] == "complete":
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
                        _, (error_message, retries, retry_back_off) = action
                        # Calculate retries if not provided
                        if retries is None:
                            retries = (
                                job_context.retries - 1
                                if job_context.retries > 0
                                else 0
                            )

                        await self.client.fail_job(
                            job_key=job_context.job_key,
                            data=JobFailRequest(
                                error_message=error_message,
                                retries=retries,
                                retry_back_off=retry_back_off,
                            ),
                        )
                        self.logger.info(
                            f"Job failed: {job_context.job_key} - {error_message}"
                        )

                    elif action[0] == "error":
                        _, (error_code, error_message) = action
                        await self.client.throw_job_error(
                            job_key=job_context.job_key,
                            data=JobErrorRequest(
                                error_code=error_code, error_message=error_message
                            ),
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
