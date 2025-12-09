import asyncio
import inspect
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, Literal
from functools import wraps
from dataclasses import dataclass
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.models.activate_jobs_body import ActivateJobsBody
from camunda_orchestration_sdk.models.activate_jobs_response_200 import ActivateJobsResponse200

@dataclass
class WorkerConfig:
    """User-facing configuration"""
    job_type: str
    timeout: int
    max_concurrent_jobs: int = 10  # Max jobs executing at once
    execution_strategy: Literal["auto", "thread", "process", "async"] = "auto"

class ExecutionHint:
    """Decorators for users to hint at their workload characteristics"""
    
    @staticmethod
    def io_bound(func: Callable) -> Callable:
        """Hint that this is I/O bound work (use threads)"""
        func._execution_hint = "thread"
        return func
    
    @staticmethod
    def cpu_bound(func: Callable) -> Callable:
        """Hint that this is CPU bound work (use processes)"""
        func._execution_hint = "process"
        return func
    
    @staticmethod
    def async_safe(func: Callable) -> Callable:
        """Hint that this is already async"""
        func._execution_hint = "async"
        return func

class JobWorker:
    def __init__(self, client: CamundaClient, callback: Callable, config: WorkerConfig):
        self.callback = callback
        self.config = config
        self.client = client
        
        # Execution strategy detection
        self.strategy = self._determine_strategy()
        
        # Resource pools
        self.thread_pool = ThreadPoolExecutor(max_workers=config.max_concurrent_jobs)
        self.process_pool = ProcessPoolExecutor(max_workers=config.max_concurrent_jobs)
        
        # Semaphore to limit concurrent executions
        self.semaphore = asyncio.Semaphore(config.max_concurrent_jobs)
        
        print(f"[{config.job_type}] Using execution strategy: {self.strategy}")
    
    def _determine_strategy(self) -> str:
        """Smart detection of execution strategy"""
        # User explicitly configured?
        if self.config.execution_strategy != "auto":
            return self.config.execution_strategy
        
        # User provided hint via decorator?
        if hasattr(self.callback, '_execution_hint'):
            return self.callback._execution_hint
        
        # Auto-detect based on function signature
        if inspect.iscoroutinefunction(self.callback):
            return "async"
        
        # Default to thread for sync functions (safe for most I/O work)
        return "thread"
    
    async def poll_loop(self):
        """Background polling loop - always async"""
        while True:
            try:
                # Non-blocking HTTP poll using httpx
                jobs = await self._poll_for_jobs()
                
                # Spawn tasks for each job
                if jobs:
                    tasks = [self._execute_job(job) for job in jobs]
                    # Don't await - let them run in background
                    for task in tasks:
                        asyncio.create_task(task)
                
            except Exception as e:
                print(f"Error polling: {e}")
            
            await asyncio.sleep(1)  # Polling interval
    
    async def _poll_for_jobs(self):
        """Your SDK's async HTTP polling logic"""
        jobsResult = await self.client.activate_jobs_async(
            ActivateJobsBody(
                type_=self.config.job_type, 
                timeout=self.config.timeout, 
                max_jobs_to_activate=self.config.max_concurrent_jobs
            )
        )
        if isinstance(jobsResult, ActivateJobsResponse200):
            return jobsResult.jobs  # Return list of jobs
        elif jobsResult == None:
            print('jobsResult is type None')
            return []
        else: # Error channel ("isLeft")
            print(jobsResult.type_)
            return []
    
    async def _execute_job(self, job):
        """Execute a single job with appropriate strategy"""
        async with self.semaphore:  # Limit concurrent executions
            try:
                if self.strategy == "async":
                    result = await self.callback(job)
                
                elif self.strategy == "thread":
                    # Run blocking sync code in thread pool
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.thread_pool, 
                        self.callback, 
                        job
                    )
                
                elif self.strategy == "process":
                    # CPU-intensive work in process pool
                    result = await asyncio.get_event_loop().run_in_executor(
                        self.process_pool,
                        self.callback,
                        job
                    )
                
                print(f"Job completed: {result}")
                
            except Exception as e:
                print(f"Job failed: {e}")
                # Your error handling/retry logic

