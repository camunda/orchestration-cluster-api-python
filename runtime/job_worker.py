import asyncio
import inspect
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, Literal, Protocol, Any, runtime_checkable, TYPE_CHECKING
from functools import wraps
from dataclasses import dataclass
from loguru import logger
from camunda_orchestration_sdk.models.activate_jobs_data import ActivateJobsData
from camunda_orchestration_sdk.models.activate_jobs_response_200 import ActivateJobsResponse200
from camunda_orchestration_sdk.types import Unset, UNSET

if TYPE_CHECKING:
    from camunda_orchestration_sdk import CamundaClient

_EFFECTIVE_EXECUTION_STRATEGY = Literal["thread", "process", "async"]
EXECUTION_STRATEGY = _EFFECTIVE_EXECUTION_STRATEGY | Literal["auto"]

@runtime_checkable
class HintedCallable(Protocol):
    _execution_hint: _EFFECTIVE_EXECUTION_STRATEGY
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

@dataclass
class WorkerConfig:
    """User-facing configuration"""
    job_type: str
    """How long the job is reserved for this worker only"""
    timeout: int
    max_concurrent_jobs: int = 10  # Max jobs executing at once
    execution_strategy: EXECUTION_STRATEGY = "auto"
    fetch_variables: list[str] | None = None
    worker_name: str = "camunda-python-sdk-worker"

class ExecutionHint:
    """Decorators for users to hint at their workload characteristics"""
    
    @staticmethod
    def io_bound(func: Callable) -> HintedCallable:
        """Hint that this is I/O bound work (use threads)"""
        func._execution_hint = "thread" # type: ignore
        return func # type: ignore
    
    @staticmethod
    def cpu_bound(func: Callable) -> HintedCallable:
        """Hint that this is CPU bound work (use processes)"""
        func._execution_hint = "process" # type: ignore
        return func # type: ignore
    
    @staticmethod
    def async_safe(func: Callable) -> HintedCallable:
        """Hint that this is already async"""
        func._execution_hint = "async" # type: ignore
        return func # type: ignore

class JobWorker:
    _strategy: _EFFECTIVE_EXECUTION_STRATEGY = "async"
    def __init__(self, client: "CamundaClient", callback: Callable, config: WorkerConfig):
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
        
        # Resource pools
        self.thread_pool = ThreadPoolExecutor(max_workers=config.max_concurrent_jobs)
        self.process_pool = ProcessPoolExecutor(max_workers=config.max_concurrent_jobs)
        
        # Semaphore to limit concurrent executions
        self.semaphore = asyncio.Semaphore(config.max_concurrent_jobs)
        
        self.running = False
        self.polling_task = None
        
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
        self.logger.debug('Polling for jobs...')
        jobsResult = await self.client.activate_jobs_async(data=
            ActivateJobsData(
                type_=self.config.job_type, 
                timeout=self.config.timeout, 
                max_jobs_to_activate=self.config.max_concurrent_jobs,
                request_timeout=0, # This allows the server to autonegotiate the poll timeout
                fetch_variable = self.config.fetch_variables if self.config.fetch_variables is not None else UNSET,
                worker=self.config.worker_name
            )
        )
        if isinstance(jobsResult, ActivateJobsResponse200):
            return jobsResult.jobs  # Return list of jobs
        elif jobsResult == None:
            self.logger.warning('jobsResult is type None')
            return []
        else: # Error channel ("isLeft")
            self.logger.error(jobsResult.type_)
            return []
    
    async def _execute_job(self, job):
        """Execute a single job with appropriate strategy"""
        async with self.semaphore:  # Limit concurrent executions
            try:
                if self._strategy == "async":
                    result = await self.callback(job)
                
                elif self._strategy == "thread":
                    # Run blocking sync code in thread pool
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.thread_pool, 
                        self.callback, 
                        job
                    )
                
                elif self._strategy == "process":
                    # CPU-intensive work in process pool
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.process_pool,
                        self.callback,
                        job
                    )
                
                self.logger.debug(f"Job completed: {job.job_key}") # type: ignore - this is set for auto
                
            except Exception as e:
                self.logger.error(f"Job failed: {e}")
                # Your error handling/retry logic

