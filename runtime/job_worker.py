import asyncio
import inspect
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, Literal, Protocol, Any, runtime_checkable, TYPE_CHECKING, Awaitable
from functools import wraps
from dataclasses import dataclass
from loguru import logger
from camunda_orchestration_sdk.models.activate_jobs_data import ActivateJobsData
from camunda_orchestration_sdk.models.activate_jobs_response_200 import ActivateJobsResponse200
from camunda_orchestration_sdk.models.activate_jobs_response_200_jobs_item import ActivateJobsResponse200JobsItem
from camunda_orchestration_sdk.models.complete_job_data import CompleteJobData
from camunda_orchestration_sdk.models.complete_job_data_variables_type_0 import CompleteJobDataVariablesType0
from camunda_orchestration_sdk.models.fail_job_data import FailJobData
from camunda_orchestration_sdk.models.throw_job_error_data import ThrowJobErrorData
from camunda_orchestration_sdk.types import Unset, UNSET

if TYPE_CHECKING:
    from camunda_orchestration_sdk import CamundaClient

_EFFECTIVE_EXECUTION_STRATEGY = Literal["thread", "process", "async"]
EXECUTION_STRATEGY = _EFFECTIVE_EXECUTION_STRATEGY | Literal["auto"]

@runtime_checkable
class HintedCallable(Protocol):
    _execution_hint: _EFFECTIVE_EXECUTION_STRATEGY
    def __call__(self, job: Any) -> "JobFinalized" | Awaitable["JobFinalized"]: ...

JobHandler = Callable[["ActivatedJob"], Awaitable["JobFinalized"]] | Callable[["SyncActivatedJob"], "JobFinalized"] | HintedCallable

@dataclass
class WorkerConfig:
    """User-facing configuration"""
    job_type: str
    """How long the job is reserved for this worker only"""
    job_timeout_milliseconds: int
    max_concurrent_jobs: int = 10  # Max jobs executing at once
    execution_strategy: EXECUTION_STRATEGY = "auto"
    fetch_variables: list[str] | None = None
    worker_name: str = "camunda-python-sdk-worker"

class ExecutionHint:
    """Decorators for users to hint at their workload characteristics"""
    
    @staticmethod
    def io_bound(func: Callable) -> "HintedCallable":
        """Hint that this is I/O bound work (use threads)"""
        func._execution_hint = "thread" # type: ignore
        return func # type: ignore
    
    @staticmethod
    def cpu_bound(func: Callable) -> "HintedCallable":
        """Hint that this is CPU bound work (use processes)"""
        func._execution_hint = "process" # type: ignore
        return func # type: ignore
    
    @staticmethod
    def async_safe(func: Callable) -> "HintedCallable":
        """Hint that this is already async"""
        func._execution_hint = "async" # type: ignore
        return func # type: ignore

@dataclass
class JobFinalized:
    """Result of a job finalization action."""
    response: Any = None

class _ActivatedJob:
    def __init__(self, job: ActivateJobsResponse200JobsItem, client: "CamundaClient", worker: "JobWorker"):
        self.job = job
        self._client = client
        self._worker = worker
        self._finalized = False
        self._lock = threading.Lock()

    def __getattr__(self, name):
        return getattr(self.job, name)

    def _decrement_if_needed(self):
        with self._lock:
            if not self._finalized:
                self._finalized = True
                self._worker._decrement_active_jobs()

    def _check_finalized(self):
        if self._finalized:
            raise RuntimeError(f"Job {self.job.job_key} has already been finalized (completed, failed, or errored).")

    def _ensure_complete_job_data(self, data: CompleteJobData | dict | None) -> CompleteJobData:
        if data is None:
            return CompleteJobData()
        if isinstance(data, dict):
            return CompleteJobData(variables=CompleteJobDataVariablesType0.from_dict(data))
        return data

    def ignore(self) -> JobFinalized:
        self._check_finalized()
        self._decrement_if_needed()
        return JobFinalized()

class ActivatedJob(_ActivatedJob):
    async def complete(self, data: CompleteJobData | dict | None = None) -> JobFinalized:
        self._check_finalized()
        complete_data = self._ensure_complete_job_data(data)
        try:
            resp = await self._client.complete_job_async(job_key=self.job.job_key, data=complete_data)
            return JobFinalized(response=resp)
        finally:
            self._decrement_if_needed()

    async def fail(self, error_message: str, retries: int, retry_back_off: int = 0) -> JobFinalized:
        self._check_finalized()
        data = FailJobData(error_message=error_message, retries=retries, retry_back_off=retry_back_off)
        try:
            resp = await self._client.fail_job_async(job_key=self.job.job_key, data=data)
            return JobFinalized(response=resp)
        finally:
            self._decrement_if_needed()

    async def error(self, error_code: str, error_message: str) -> JobFinalized:
        self._check_finalized()
        data = ThrowJobErrorData(error_code=error_code, error_message=error_message)
        try:
            resp = await self._client.throw_job_error_async(job_key=self.job.job_key, data=data)
            return JobFinalized(response=resp)
        finally:
            self._decrement_if_needed()

class SyncActivatedJob(_ActivatedJob):
    def complete(self, data: CompleteJobData | dict | None = None) -> JobFinalized:
        self._check_finalized()
        complete_data = self._ensure_complete_job_data(data)
        try:
            resp = self._client.complete_job(job_key=self.job.job_key, data=complete_data)
            return JobFinalized(response=resp)
        finally:
            self._decrement_if_needed()

    def fail(self, error_message: str, retries: int, retry_back_off: int = 0) -> JobFinalized:
        self._check_finalized()
        data = FailJobData(error_message=error_message, retries=retries, retry_back_off=retry_back_off)
        try:
            resp = self._client.fail_job(job_key=self.job.job_key, data=data)
            return JobFinalized(response=resp)
        finally:
            self._decrement_if_needed()

    def error(self, error_code: str, error_message: str) -> JobFinalized:
        self._check_finalized()
        data = ThrowJobErrorData(error_code=error_code, error_message=error_message)
        try:
            resp = self._client.throw_job_error(job_key=self.job.job_key, data=data)
            return JobFinalized(response=resp)
        finally:
            self._decrement_if_needed()

class JobWorker:
    _strategy: _EFFECTIVE_EXECUTION_STRATEGY = "async"
    def __init__(self, client: "CamundaClient", callback: JobHandler, config: WorkerConfig):
        self.callback = callback
        self.config = config
        self.client = client
        
        # Bind logger with context
        self.logger = logger.bind(
            sdk="camunda_orchestration_sdk",
            worker=config.worker_name,
            job_type=config.job_type
        )

        # Execution strategy detection
        self._strategy = self._determine_strategy()
        self._validate_strategy()
        
        # Resource pools
        self.thread_pool = ThreadPoolExecutor(max_workers=config.max_concurrent_jobs)
        self.process_pool = ProcessPoolExecutor(max_workers=config.max_concurrent_jobs)
        
        # Semaphore to limit concurrent executions
        self.semaphore = asyncio.Semaphore(config.max_concurrent_jobs)
        
        self.running = False
        self.polling_task = None
        
        self.active_jobs = 0
        self.lock = threading.Lock()
        
        self.logger.info(f"Using execution strategy: {self._strategy}")
    
    def _determine_strategy(self) -> _EFFECTIVE_EXECUTION_STRATEGY:
        """Smart detection of execution strategy"""
        # User explicitly configured?
        if self.config.execution_strategy != "auto":
            return self.config.execution_strategy
        
        # User provided hint via decorator?
        if isinstance(self.callback, HintedCallable):
            return self.callback._execution_hint # type: ignore
        
        # Auto-detect based on function signature
        if inspect.iscoroutinefunction(self.callback):
            return "async"
        
        # Default to thread for sync functions (safe for most I/O work)
        return "thread"
    
    def _validate_strategy(self):
        """Ensure the strategy matches the callback type"""
        is_async_callback = inspect.iscoroutinefunction(self.callback)
        
        if self._strategy == "async" and not is_async_callback:
            raise ValueError(
                f"Execution strategy is 'async' but callback '{self.callback.__name__}' is synchronous. "
                "Async strategy requires an 'async def' callback."
            )
            
        if self._strategy in ["thread", "process"] and is_async_callback:
            raise ValueError(
                f"Execution strategy is '{self._strategy}' but callback '{self.callback.__name__}' is asynchronous. "
                "Thread/Process strategies require a synchronous 'def' callback."
            )

    def _decrement_active_jobs(self):
        with self.lock:
            self.active_jobs -= 1
            self.logger.trace(f"Active jobs: {self.active_jobs}")

    def start(self):
        if not self.running:
            self.running = True
            self.polling_task = asyncio.create_task(self.poll_loop())
            self.logger.info("Worker started")

    def stop(self):
        if self.running:
            self.running = False
            if self.polling_task:
                self.polling_task.cancel()
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
            return []

        self.logger.debug(f'Polling for jobs (capacity: {capacity})...')
        jobsResult = await self.client.activate_jobs_async(data=
            ActivateJobsData(
                type_=self.config.job_type, 
                timeout=self.config.job_timeout_milliseconds, 
                max_jobs_to_activate=capacity,
                request_timeout=0, # This allows the server to autonegotiate the poll timeout
                fetch_variable = self.config.fetch_variables if self.config.fetch_variables is not None else UNSET,
                worker=self.config.worker_name
            )
        )
        if isinstance(jobsResult, ActivateJobsResponse200):
            self.logger.trace(f'Received {len(jobsResult.jobs)}')
            self.logger.trace(f'Jobs received: {[job.job_key for job in jobsResult.jobs]}')
            if jobsResult.jobs:
                with self.lock:
                    self.active_jobs += len(jobsResult.jobs)
            return jobsResult.jobs  # Return list of jobs
        elif jobsResult == None:
            self.logger.warning('jobsResult is type None')
            return []
        else: # Error channel ("isLeft")
            self.logger.error(jobsResult.type_)
            return []
    
    async def _execute_job(self, job):
        """Execute a single job with appropriate strategy"""
        
        # Instantiate the correct job wrapper based on strategy
        if self._strategy == "async":
            activated_job = ActivatedJob(job, self.client, self)
        else:
            activated_job = SyncActivatedJob(job, self.client, self)

        try:
            async with self.semaphore:  # Limit concurrent executions
                try:
                    if self._strategy == "async":
                        result = await self.callback(activated_job)
                    
                    elif self._strategy == "thread":
                        # Run blocking sync code in thread pool
                        result = await asyncio.get_event_loop().run_in_executor(
                            self.thread_pool, 
                            self.callback, 
                            activated_job
                        )
                    
                    elif self._strategy == "process":
                        # CPU-intensive work in process pool
                        result = await asyncio.get_event_loop().run_in_executor(
                            self.process_pool,
                            self.callback,
                            activated_job
                        )
                    
                    self.logger.debug(f"Job completed: {job.job_key}") # type: ignore - this is set for auto
                    
                except Exception as e:
                    self.logger.error(f"Job failed: {e}")
                    # Your error handling/retry logic
        finally:
            activated_job._decrement_if_needed()


