import argparse
import asyncio
import multiprocessing
import os
import subprocess
import time
import tracemalloc
import resource
import threading
import random
import psutil
from functools import partial
from typing import Literal, get_args, Any
from loguru import logger
from camunda_orchestration_sdk.semantic_types import ProcessDefinitionKey

from camunda_orchestration_sdk.models.processcreationbykey import Processcreationbykey
from camunda_orchestration_sdk.models.state_exactmatch_3 import StateExactmatch3
from camunda_orchestration_sdk.types import File

from camunda_orchestration_sdk.models.create_deployment_data import CreateDeploymentData
from camunda_orchestration_sdk.models.search_process_instances_data import (
    SearchProcessInstancesData,
)
from camunda_orchestration_sdk.models.search_process_instances_data_filter import (
    SearchProcessInstancesDataFilter,
)
from camunda_orchestration_sdk import CamundaClient, WorkerConfig
from camunda_orchestration_sdk.runtime.job_worker import (
    JobContext,
    EXECUTION_STRATEGY,
    JobHandler,
)

strategies = [s for arg in get_args(EXECUTION_STRATEGY) for s in get_args(arg)]
JOB_TIMEOUT_MILLISECONDS = 30_000


def make_client(base_url: str | None = None) -> CamundaClient:
    """Create a new Camunda client instance.

    Args:
        base_url: Override the base URL. Defaults to CAMUNDA_BASE_URL env var or localhost.
    """
    host = base_url or os.environ.get("CAMUNDA_BASE_URL", "http://localhost:8080/v2")
    return CamundaClient(base_url=host)


def get_process_memory_mb() -> tuple[float, float]:
    """Get the current memory usage of the process and all its children.
    
    Returns:
        Tuple of (total_rss_mb, children_rss_mb)
    """
    try:
        current_process = psutil.Process(os.getpid())
        
        # Get memory of current process
        total_rss = current_process.memory_info().rss
        children_rss = 0
        
        # Get memory of all children recursively
        children = current_process.children(recursive=True)
        for child in children:
            try:
                child_rss = child.memory_info().rss
                total_rss += child_rss
                children_rss += child_rss
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Process might have died or we can't access it
                pass
                
        return total_rss / (1024 * 1024), children_rss / (1024 * 1024)
    except Exception as e:
        logger.warning(f"Failed to get process memory: {e}")
        return 0.0, 0.0


def generate_balanced_durations(count: int, mean: float, jitter_pct: float) -> list[float]:
    """Generate a list of durations with jitter, ensuring the total sum is exactly count * mean.
    
    Uses a balanced pair approach: for every (mean + offset), there is a (mean - offset).
    """
    if jitter_pct <= 0:
        return [mean] * count
    
    durations: list[float] = []
    num_pairs = count // 2
    
    # Use a fixed seed for reproducibility of the sequence
    rng = random.Random(42) 
    
    for _ in range(num_pairs):
        # Random offset within jitter range
        offset = rng.uniform(0, mean * jitter_pct)
        durations.append(mean - offset)
        durations.append(mean + offset)
        
    if count % 2 != 0:
        durations.append(mean)
        
    rng.shuffle(durations)
    return durations


def simulate_cpu_work(duration: float):
    """Simulate CPU-bound work that heavily engages the Python interpreter (GIL-bound).

    Performs arithmetic operations and list comprehensions to ensure the
    Global Interpreter Lock (GIL) is held, preventing multi-threaded parallelism.
    """
    end_time = time.time() + duration
    while time.time() < end_time:
        # Create and destroy objects, do math
        # This is pure Python work that cannot be parallelized by threads
        _ = [x * x for x in range(500_000)]


def simulate_io_work(duration: float):
    """Simulate I/O-bound work with actual file I/O operations.

    Performs repeated file read/write operations to simulate I/O blocking.
    """
    import tempfile

    end_time = time.time() + duration
    chunk_size = 1024 * 1024  # 1MB chunks

    with tempfile.NamedTemporaryFile(mode="w+b", delete=True) as f:
        data = b"0" * chunk_size
        while time.time() < end_time:
            # Write operation
            f.write(data)
            f.flush()
            os.fsync(f.fileno())  # Force write to disk

            # Read operation
            f.seek(0)
            _ = f.read(chunk_size)


async def simulate_io_work_async(duration: float):
    """Simulate I/O-bound work with async file I/O operations.

    Uses asyncio's thread pool executor for file I/O to avoid blocking the event loop.
    This demonstrates proper async I/O handling by offloading blocking operations to a thread pool.
    """
    import tempfile

    # Run blocking I/O in executor to avoid blocking the event loop
    loop = asyncio.get_event_loop()

    def blocking_io():
        end_time = time.time() + duration
        chunk_size = 1024 * 1024  # 1MB chunks

        with tempfile.NamedTemporaryFile(mode="w+b", delete=True) as f:
            data = b"0" * chunk_size
            while time.time() < end_time:
                # Write operation
                f.write(data)
                f.flush()
                os.fsync(f.fileno())  # Force write to disk

                # Read operation
                f.seek(0)
                _ = f.read(chunk_size)

    await loop.run_in_executor(None, blocking_io)


def simulate_subprocess_work(duration: float):
    """Simulate work by calling an external CLI tool (subprocess).

    This tests how subprocess calls behave under different execution strategies.
    Uses 'sleep' command which is available on Unix-like systems.
    """
    # Call external sleep command for a short duration
    # This simulates calling an external CLI tool
    subprocess.call(
        ["sleep", str(duration)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def simulate_problematic_subprocess_work(duration: float):
    """Simulate a problematic subprocess that uses threading and locks.

    This demonstrates potential fork-safety issues when calling subprocess.run()
    from a multi-threaded parent process, where the subprocess itself creates threads
    and uses synchronization primitives like locks.

    This can expose deadlocks, hangs, or crashes in multi-threaded environments,
    especially when:
    - Parent has many threads (ThreadPoolExecutor)
    - Subprocess uses locks/mutexes
    - High concurrency increases chance of fork() happening while locks are held
    """
    # Create a Python subprocess that uses threading AND locks
    # This increases the chance of fork-safety issues:
    # 1. Parent process has multiple threads (ThreadPoolExecutor)
    # 2. subprocess.run() may use fork() on Unix (depending on Python version)
    # 3. Child process creates threads AND uses locks
    # 4. If fork happens while parent thread holds a lock, child inherits locked state = deadlock

    python_code = f"""
import threading
import time
import sys

# Shared lock and counter (simulates more complex threading scenario)
lock = threading.Lock()
counter = {{'value': 0}}

def worker(worker_id):
    '''Thread worker that uses locks - more likely to expose fork issues'''
    for i in range(3):
        with lock:
            counter['value'] += 1
            current = counter['value']
        time.sleep({duration} / 10)
        sys.stderr.write(f"Worker {{worker_id}} iteration {{i}}: count={{current}}\\n")
        sys.stderr.flush()

# Create multiple threads that compete for locks
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    threads.append(t)

# Wait for all threads
for t in threads:
    t.join()

print(f"Subprocess completed: final count={{counter['value']}}")
"""

    result = subprocess.run(
        ["python3", "-c", python_code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=duration * 5,  # Longer timeout since we have more work
    )

    if result.returncode != 0:
        logger.warning(
            f"Problematic subprocess failed with code {result.returncode}: {result.stderr.decode()}"
        )
    else:
        logger.debug(f"Problematic subprocess output: {result.stdout.decode().strip()}")
        if result.stderr:
            logger.debug(f"Subprocess stderr: {result.stderr.decode().strip()}")


async def simulate_subprocess_work_async(duration: float):
    """Simulate subprocess work in async context.

    Uses asyncio.create_subprocess_exec for proper async subprocess handling.
    """
    # Use async subprocess to avoid blocking the event loop
    process = await asyncio.create_subprocess_exec(
        "sleep",
        str(duration),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await process.wait()


def _get_job_duration(job_counter: Any | None, default_duration: float, lock: Any | None) -> float:
    """Get the duration for the next job from the pre-calculated list, or use default."""
    if job_counter is None:
        return default_duration
        
    # Check if durations are available (might not be if jitter=0 or old version)
    # For Manager dicts, we need to be careful with 'in' operator sometimes, but it should work.
    try:
        if "durations" not in job_counter:
            return default_duration
    except Exception:
        return default_duration

    if lock:
        with lock:
            idx = job_counter.get("duration_idx", 0)
            # Check bounds
            durations = job_counter["durations"]
            if idx < len(durations):
                duration = durations[idx]
                job_counter["duration_idx"] = idx + 1
                return duration
    else:
        # Async case (single threaded loop) or no lock needed
        idx = job_counter.get("duration_idx", 0)
        durations = job_counter["durations"]
        if idx < len(durations):
            duration = durations[idx]
            job_counter["duration_idx"] = idx + 1
            return duration
            
    return default_duration


# Module-level callback functions (picklable for multiprocessing)
async def _async_job_callback(
    job: JobContext,
    workload_type: Literal["cpu", "io", "subprocess", "subprocess_threaded"],
    work_duration: float,
    job_counter: dict[str, int] | None,
    lock: Any | None = None,
):
    """Async job callback for async/auto strategies.

    This is a module-level function so it can be pickled for multiprocessing.
    """
    # Determine duration (with jitter if configured)
    actual_duration = _get_job_duration(job_counter, work_duration, lock)
    
    logger.info(f"Starting {workload_type}-bound work on: {job.job_key} (duration: {actual_duration:.3f}s)")

    # Simulate workload based on type
    if workload_type == "cpu":
        simulate_cpu_work(actual_duration)
    elif workload_type == "io":
        await simulate_io_work_async(actual_duration)
    elif workload_type == "subprocess_threaded":
        # Run the problematic subprocess in executor to avoid blocking event loop
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, simulate_problematic_subprocess_work, actual_duration
        )
    else:  # subprocess
        await simulate_subprocess_work_async(actual_duration)

    logger.info(f"Finished work on: {job.job_key}")

    # Track completion if counter provided
    if job_counter is not None:
        # Async is single-threaded (per loop), so atomic enough for this
        job_counter["completed"] = job_counter.get("completed", 0) + 1
        logger.info(f"Jobs completed: {job_counter['completed']}")
    
    # Complete the job by returning variables
    return {"quoteAmount": 2345432}


def _sync_cpu_job_callback(
    job: JobContext,
    work_duration: float,
    job_counter: dict[str, int] | None,
    lock: Any | None = None,
):
    """Synchronous CPU-bound job callback.

    This is a module-level function so it can be pickled for multiprocessing.
    """
    # Determine duration (with jitter if configured)
    actual_duration = _get_job_duration(job_counter, work_duration, lock)
    
    logger.info(f"Starting cpu-bound work on: {job.job_key} (duration: {actual_duration:.3f}s)")
    simulate_cpu_work(actual_duration)
    logger.info(f"Finished work on: {job.job_key}")

    # Track completion if counter provided
    if job_counter is not None:
        if lock:
            with lock:
                job_counter["completed"] = job_counter.get("completed", 0) + 1
                val = job_counter["completed"]
            logger.info(f"Jobs completed: {val}")
        else:
            job_counter["completed"] = job_counter.get("completed", 0) + 1
            logger.info(f"Jobs completed: {job_counter['completed']}")
    
    # Complete the job by returning variables
    return {"quoteAmount": 2345432}


def _sync_io_job_callback(
    job: JobContext,
    workload_type: Literal["io", "subprocess", "subprocess_threaded"],
    work_duration: float,
    job_counter: dict[str, int] | None,
    lock: Any | None = None,
):
    """Synchronous I/O-bound job callback (handles both I/O and subprocess).

    This is a module-level function so it can be pickled for multiprocessing.
    """
    # Determine duration (with jitter if configured)
    actual_duration = _get_job_duration(job_counter, work_duration, lock)
    
    logger.info(f"Starting {workload_type}-bound work on: {job.job_key} (duration: {actual_duration:.3f}s)")

    # Simulate workload based on type
    if workload_type == "io":
        simulate_io_work(actual_duration)
    elif workload_type == "subprocess_threaded":
        simulate_problematic_subprocess_work(actual_duration)
    else:  # subprocess
        simulate_subprocess_work(actual_duration)

    logger.info(f"Finished work on: {job.job_key}")

    # Track completion if counter provided
    if job_counter is not None:
        if lock:
            with lock:
                job_counter["completed"] = job_counter.get("completed", 0) + 1
                val = job_counter["completed"]
            logger.info(f"Jobs completed: {val}")
        else:
            job_counter["completed"] = job_counter.get("completed", 0) + 1
            logger.info(f"Jobs completed: {job_counter['completed']}")
    
    # Complete the job by returning variables
    return {"quoteAmount": 2345432}


def create_default_callback(
    client: CamundaClient,
    job_counter: dict[str, int] | None = None,
    strategy: str = "async",
    workload_type: Literal["cpu", "io", "subprocess", "subprocess_threaded"] = "cpu",
    work_duration: float = 3.0,
    lock: Any | None = None,
) -> JobHandler:
    """Create a default job callback that completes jobs with dummy data.

    Uses functools.partial to bind parameters to module-level functions,
    making them picklable for multiprocessing (process strategy).

    Args:
        client: The Camunda client to use for completing jobs.
        job_counter: Optional dict to track completed jobs. If provided, increments 'completed' key.
        strategy: Execution strategy - determines whether to create async or sync callback.
        workload_type: Type of workload simulation - "cpu", "io", or "subprocess".
        work_duration: Duration of simulated work in seconds.
        lock: Optional lock for thread/process safety.

    Returns:
        A callback function (async or sync depending on strategy) bound with the necessary parameters.
    """
    if strategy in ["async", "auto"]:
        # Use partial to bind parameters to the async callback
        return partial(
            _async_job_callback,
            workload_type=workload_type,
            work_duration=work_duration,
            job_counter=job_counter,
            lock=lock,
        )
    else:
        # For thread/process strategies, use the appropriate sync callback
        if workload_type == "cpu":
            # CPU-bound callback
            return partial(
                _sync_cpu_job_callback,
                work_duration=work_duration,
                job_counter=job_counter,
                lock=lock,
            )
        else:
            # I/O-bound or subprocess callback
            return partial(
                _sync_io_job_callback,
                workload_type=workload_type,
                work_duration=work_duration,
                job_counter=job_counter,
                lock=lock,
            )


async def deploy_process(
    client: CamundaClient,
    bpmn_path: str = "./demo/v2/resources/job_worker_load_test_process_1.bpmn",
) -> ProcessDefinitionKey:
    """Deploy a BPMN process to Camunda.

    Args:
        client: The Camunda client to use.
        bpmn_path: Path to the BPMN file.

    Returns:
        The process definition key.
    """
    with open(bpmn_path, "rb") as f:
        process_file = File(payload=f, file_name=os.path.basename(bpmn_path))
        deployed_resources = await client.create_deployment_async(
            data=CreateDeploymentData(resources=[process_file])
        )

    process_definition_key = deployed_resources.deployments[0].process_definition.process_definition_key  # type: ignore
    logger.info(f"Deployed process: {process_definition_key}")
    return process_definition_key


async def cleanup_active_instances(
    client: CamundaClient, process_definition_key: str
) -> None:
    """Cancel all active instances of a process.

    Args:
        client: The Camunda client to use.
        process_definition_key: The process definition key to clean up.
    """
    from camunda_orchestration_sdk.errors import UnexpectedStatus

    search_query = SearchProcessInstancesData(
        filter_=SearchProcessInstancesDataFilter(
            process_definition_key=process_definition_key,
            state=StateExactmatch3("ACTIVE"),
        )
    )
    already_running = client.search_process_instances(data=search_query)
    for process in already_running.items:
        try:
            logger.info(f"Canceling process instance: {process.process_instance_key}")
            await client.cancel_process_instance_async(
                data=None, process_instance_key=process.process_instance_key
            )
        except UnexpectedStatus as e:
            # If the instance is already gone (404), that's fine - it completed or was already canceled
            if e.status_code == 404:
                logger.debug(
                    f"Process instance {process.process_instance_key} already completed or canceled"
                )
            else:
                # Re-raise other unexpected errors
                raise


async def run_worker_scenario(
    client: CamundaClient,
    process_definition_key: ProcessDefinitionKey,
    worker_config: WorkerConfig,
    num_instances: int = 1,
    expected_jobs: int | None = None,
    scenario_timeout_seconds: int | None = 30,
    workload_type: Literal["cpu", "io", "subprocess", "subprocess_threaded"] = "cpu",
    work_duration: float = 3.0,
    jitter_pct: float = 0.0,
) -> dict[str, float]:
    """Run a worker scenario with configurable settings.

    Args:
        client: The Camunda client to use.
        process_definition_key: The process to start instances of.
        worker_config: Configuration for the worker.
        num_instances: Number of process instances to start.
        expected_jobs: Number of jobs to wait for before stopping. If None, uses num_instances.
        scenario_timeout_seconds: Timeout in seconds to run the worker. None means run indefinitely.
        workload_type: Type of workload simulation - "cpu", "io", or "subprocess".
        work_duration: Duration of simulated work in seconds.
        jitter_pct: Percentage of jitter to apply to work duration (0.0 to 1.0).

    Returns:
        dict with timing stats: {'total_time', 'jobs_completed', 'jobs_per_second', 'expected_jobs',
                                  'memory_current_mb', 'memory_peak_mb'}
    """
    logger.debug(
        f"Running worker with config: {worker_config}, workload: {workload_type}, jitter: {jitter_pct}"
    )
    if expected_jobs is None:
        expected_jobs = num_instances

    # Generate balanced durations
    durations = generate_balanced_durations(expected_jobs, work_duration, jitter_pct)

    # Start memory tracking
    tracemalloc.start()
    initial_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # Job counter to track completions
    # For process strategy, use a multiprocessing.Manager dict (picklable and process-safe)
    # For other strategies, use a regular dict
    lock = None
    if worker_config.execution_strategy == "process":
        manager = multiprocessing.Manager()
        job_counter = manager.dict()
        job_counter["completed"] = 0
        job_counter["start_time"] = None
        # Store durations in shared list
        job_counter["durations"] = manager.list(durations)
        job_counter["duration_idx"] = 0
        lock = manager.Lock()
    elif worker_config.execution_strategy == "thread":
        job_counter = {
            "completed": 0, 
            "start_time": None,
            "durations": durations,
            "duration_idx": 0
        }
        lock = threading.Lock()
    else:
        job_counter = {
            "completed": 0, 
            "start_time": None,
            "durations": durations,
            "duration_idx": 0
        }
        lock = None

    # Create callback with counter (pass strategy and workload type)
    tracked_callback = create_default_callback(
        client,
        job_counter,
        worker_config.execution_strategy,
        workload_type,
        work_duration,
        lock,
    )

    # Start process instances
    logger.info(f"\n=== Starting {num_instances} process instances ===")
    for i in range(num_instances):
        process_instance = client.create_process_instance(
            data=Processcreationbykey(process_definition_key=process_definition_key)
        )
        logger.info(
            f"Started process instance {i+1}/{num_instances}: {process_instance.process_instance_key}"
        )

    # Record start time after all instances are started
    job_counter["start_time"] = time.time()
    logger.info(
        f"\n=== All instances started. Waiting for {expected_jobs} jobs to complete ==="
    )

    # Create worker
    client.create_job_worker(config=worker_config, callback=tracked_callback)

    # Monitor for completion
    # Track peak memory during execution
    memory_stats = {
        "peak_total_rss_mb": 0.0,
        "peak_children_rss_mb": 0.0
    }

    async def wait_for_completion():
        while job_counter["completed"] < expected_jobs:
            # Poll memory usage
            total_rss, children_rss = get_process_memory_mb()
            memory_stats["peak_total_rss_mb"] = max(memory_stats["peak_total_rss_mb"], total_rss)
            memory_stats["peak_children_rss_mb"] = max(memory_stats["peak_children_rss_mb"], children_rss)
            
            await asyncio.sleep(0.1)  # Check every 100ms

    # Run workers and monitor concurrently
    worker_task = asyncio.create_task(client.run_workers())

    try:
        if scenario_timeout_seconds is not None:
            await asyncio.wait_for(
                wait_for_completion(), timeout=scenario_timeout_seconds
            )
        else:
            await wait_for_completion()
    except asyncio.TimeoutError:
        logger.warning(f"\n⚠️  Timeout reached after {scenario_timeout_seconds}s")
    finally:
        # Stop the worker
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass  # Expected when we cancel

        # Calculate stats
        end_time = time.time()
        total_time = end_time - job_counter["start_time"]
        jobs_completed = job_counter["completed"]
        jobs_per_second = jobs_completed / total_time if total_time > 0 else 0

        # Get memory usage
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Get RSS memory (in bytes on macOS, KB on Linux)
        final_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # On macOS, ru_maxrss is in bytes; on Linux it's in KB
        # Detect platform and convert to MB
        import sys

        if sys.platform == "darwin":  # macOS
            rss_mb = (final_rss - initial_rss) / (1024 * 1024)
            max_rss_mb = final_rss / (1024 * 1024)
        else:  # Linux
            rss_mb = (final_rss - initial_rss) / 1024
            max_rss_mb = final_rss / 1024

        memory_current_mb = current_memory / (1024 * 1024)
        memory_peak_mb = peak_memory / (1024 * 1024)

        logger.info(f"\n=== Test Complete ===")
        logger.info(f"Jobs completed: {jobs_completed}/{expected_jobs}")
        logger.info(f"Total time: {total_time:.2f}s")
        logger.info(f"Throughput: {jobs_per_second:.2f} jobs/second")
        logger.info(f"\n=== Memory Usage ===")
        logger.info(f"Current Python memory: {memory_current_mb:.2f} MB")
        logger.info(f"Peak Python memory: {memory_peak_mb:.2f} MB")
        logger.info(f"Max RSS (total process): {max_rss_mb:.2f} MB")
        logger.info(f"RSS delta: {rss_mb:.2f} MB")
        logger.info(f"Peak Total RSS (incl children): {memory_stats['peak_total_rss_mb']:.2f} MB")
        logger.info(f"Peak Children RSS: {memory_stats['peak_children_rss_mb']:.2f} MB")

        result = {
            "total_time": total_time,
            "jobs_completed": jobs_completed,
            "jobs_per_second": jobs_per_second,
            "expected_jobs": expected_jobs,
            "memory_current_mb": memory_current_mb,
            "memory_peak_mb": memory_peak_mb,
            "max_rss_mb": max_rss_mb,
            "rss_delta_mb": rss_mb,
            "peak_total_rss_mb": memory_stats["peak_total_rss_mb"],
            "peak_children_rss_mb": memory_stats["peak_children_rss_mb"],
        }
        return result


async def run_test(
    num_instances: int = 10,
    strategy: EXECUTION_STRATEGY = "auto",
    workload_type: Literal["cpu", "io", "subprocess", "subprocess_threaded"] = "cpu",
    repeats: int = 1,
    max_concurrent_jobs: int = 10,
    timeout: int = 5000,
    work_duration: float = 3.0,
    job_timeout_ms: int = JOB_TIMEOUT_MILLISECONDS,
    jitter_pct: float = 0.0,
) -> dict[str, float]:
    """Run a parameterized test with optional averaging over multiple runs.

    Args:
        num_instances: Number of process instances to start per run.
        strategy: Execution strategy ("auto", "async", "thread", "process").
        workload_type: Type of workload simulation - "cpu", "io", or "subprocess".
        repeats: Number of times to repeat the test (results will be averaged).
        max_concurrent_jobs: Maximum concurrent jobs for the worker.
        timeout: Timeout in seconds for each run.
        work_duration: Duration of simulated work in seconds.
        job_timeout_ms: Job timeout in milliseconds.
        jitter_pct: Percentage of jitter to apply to work duration (0.0 to 1.0).

    Returns:
        dict with averaged timing stats: {
            'total_time_avg', 'total_time_min', 'total_time_max',
            'jobs_per_second_avg', 'jobs_per_second_min', 'jobs_per_second_max',
            'jobs_completed', 'expected_jobs', 'repeats'
        }
    """
    logger.info(f"\n{'='*70}")
    logger.info(f"TEST CONFIGURATION")
    logger.info(f"{'='*70}")
    logger.info(f"Instances per run:    {num_instances}")
    logger.info(f"Strategy:             {strategy}")
    logger.info(f"Max concurrent jobs:  {max_concurrent_jobs}")
    logger.info(f"Workload type:        {workload_type}")
    logger.info(f"Work duration:        {work_duration}s")
    logger.info(f"Jitter:               {jitter_pct*100:.1f}%")
    logger.info(f"Job timeout:          {job_timeout_ms}ms")
    logger.info(f"Repeats:              {repeats}")
    logger.info(f"Timeout per run:      {timeout}s")
    logger.info(f"{'='*70}\n")

    all_stats = []

    for run_num in range(repeats):
        if repeats > 1:
            logger.info(f"\n{'='*70}")
            logger.info(f"RUN {run_num + 1}/{repeats}")
            logger.info(f"{'='*70}")

        # Create fresh client for each run
        client = make_client()

        # Deploy process (or reuse if needed)
        process_definition_key = await deploy_process(client)

        # Cleanup existing instances
        await cleanup_active_instances(client, process_definition_key)

        # Run the test
        stats = await run_worker_scenario(
            client=client,
            process_definition_key=process_definition_key,
            worker_config=WorkerConfig(
                job_type="job-worker-load-test-1-task-1",
                job_timeout_milliseconds=job_timeout_ms,
                max_concurrent_jobs=max_concurrent_jobs,
                execution_strategy=strategy,
            ),
            num_instances=num_instances,
            scenario_timeout_seconds=timeout,
            workload_type=workload_type,
            work_duration=work_duration,
            jitter_pct=jitter_pct,
        )
        all_stats.append(stats)

        if repeats > 1:
            logger.info(f"\nRun {run_num + 1} Summary:")
            logger.info(f"  Time: {stats['total_time']:.2f}s")
            logger.info(f"  Throughput: {stats['jobs_per_second']:.2f} jobs/sec")

    # Calculate averages if multiple runs
    if repeats == 1:
        result = all_stats[0]
        result["repeats"] = 1
        return result
    else:
        total_times = [s["total_time"] for s in all_stats]
        throughputs = [s["jobs_per_second"] for s in all_stats]
        peak_memories = [s["memory_peak_mb"] for s in all_stats]
        max_rss_values = [s["max_rss_mb"] for s in all_stats]
        peak_total_rss_values = [s["peak_total_rss_mb"] for s in all_stats]
        peak_children_rss_values = [s["peak_children_rss_mb"] for s in all_stats]

        result = {
            "total_time_avg": sum(total_times) / len(total_times),
            "total_time_min": min(total_times),
            "total_time_max": max(total_times),
            "total_time_std": (
                sum((x - sum(total_times) / len(total_times)) ** 2 for x in total_times)
                / len(total_times)
            )
            ** 0.5,
            "jobs_per_second_avg": sum(throughputs) / len(throughputs),
            "jobs_per_second_min": min(throughputs),
            "jobs_per_second_max": max(throughputs),
            "jobs_per_second_std": (
                sum((x - sum(throughputs) / len(throughputs)) ** 2 for x in throughputs)
                / len(throughputs)
            )
            ** 0.5,
            "memory_peak_mb_avg": sum(peak_memories) / len(peak_memories),
            "memory_peak_mb_min": min(peak_memories),
            "memory_peak_mb_max": max(peak_memories),
            "max_rss_mb_avg": sum(max_rss_values) / len(max_rss_values),
            "max_rss_mb_min": min(max_rss_values),
            "max_rss_mb_max": max(max_rss_values),
            "peak_total_rss_mb_avg": sum(peak_total_rss_values) / len(peak_total_rss_values),
            "peak_total_rss_mb_min": min(peak_total_rss_values),
            "peak_total_rss_mb_max": max(peak_total_rss_values),
            "peak_children_rss_mb_avg": sum(peak_children_rss_values) / len(peak_children_rss_values),
            "peak_children_rss_mb_min": min(peak_children_rss_values),
            "peak_children_rss_mb_max": max(peak_children_rss_values),
            "jobs_completed": all_stats[0]["jobs_completed"],
            "expected_jobs": all_stats[0]["expected_jobs"],
            "repeats": repeats,
            "all_runs": all_stats,
        }

        logger.info(f"\n{'='*70}")
        logger.info(f"AVERAGED RESULTS ({repeats} runs)")
        logger.info(f"{'='*70}")
        logger.info(f"Total Time:")
        logger.info(f"  Average: {result['total_time_avg']:.2f}s")
        logger.info(f"  Min:     {result['total_time_min']:.2f}s")
        logger.info(f"  Max:     {result['total_time_max']:.2f}s")
        logger.info(f"  Std Dev: {result['total_time_std']:.2f}s")
        logger.info(f"\nThroughput:")
        logger.info(f"  Average: {result['jobs_per_second_avg']:.2f} jobs/sec")
        logger.info(f"  Min:     {result['jobs_per_second_min']:.2f} jobs/sec")
        logger.info(f"  Max:     {result['jobs_per_second_max']:.2f} jobs/sec")
        logger.info(f"  Std Dev: {result['jobs_per_second_std']:.2f} jobs/sec")
        logger.info(f"\nMemory Usage:")
        logger.info(f"  Peak Python Memory:")
        logger.info(f"    Average: {result['memory_peak_mb_avg']:.2f} MB")
        logger.info(f"    Min:     {result['memory_peak_mb_min']:.2f} MB")
        logger.info(f"    Max:     {result['memory_peak_mb_max']:.2f} MB")
        logger.info(f"  Max RSS:")
        logger.info(f"    Average: {result['max_rss_mb_avg']:.2f} MB")
        logger.info(f"    Min:     {result['max_rss_mb_min']:.2f} MB")
        logger.info(f"    Max:     {result['max_rss_mb_max']:.2f} MB")
        logger.info(f"  Peak Total RSS (incl children):")
        logger.info(f"    Average: {result['peak_total_rss_mb_avg']:.2f} MB")
        logger.info(f"    Min:     {result['peak_total_rss_mb_min']:.2f} MB")
        logger.info(f"    Max:     {result['peak_total_rss_mb_max']:.2f} MB")
        logger.info(f"  Peak Children RSS:")
        logger.info(f"    Average: {result['peak_children_rss_mb_avg']:.2f} MB")
        logger.info(f"    Min:     {result['peak_children_rss_mb_min']:.2f} MB")
        logger.info(f"    Max:     {result['peak_children_rss_mb_max']:.2f} MB")
        logger.info(f"{'='*70}\n")

        return result


async def simple_scenario():
    """Run a simple single-worker scenario (original behavior)."""
    client = make_client()

    # Deploy process
    process_definition_key = await deploy_process(client)

    # Cleanup existing instances
    await cleanup_active_instances(client, process_definition_key)

    # Run worker scenario
    stats = await run_worker_scenario(
        client=client,
        process_definition_key=process_definition_key,
        worker_config=WorkerConfig(
            job_type="job-worker-load-test-1-task-1",
            job_timeout_milliseconds=JOB_TIMEOUT_MILLISECONDS,
            max_concurrent_jobs=10,
            execution_strategy="auto",
        ),
        num_instances=1,
    )
    return stats


async def load_test_scenario():
    """Run a load test with multiple instances and high concurrency."""
    client = make_client()

    # Deploy process
    process_definition_key = await deploy_process(client)

    # Cleanup existing instances
    await cleanup_active_instances(client, process_definition_key)

    # Run load test scenario
    stats = await run_worker_scenario(
        client=client,
        process_definition_key=process_definition_key,
        worker_config=WorkerConfig(
            job_type="job-worker-load-test-1-task-1",
            job_timeout_milliseconds=JOB_TIMEOUT_MILLISECONDS,
            max_concurrent_jobs=50,  # Higher concurrency
            execution_strategy="auto",
        ),
        num_instances=100,  # More instances
        scenario_timeout_seconds=120,  # 2 minute timeout for load test
    )
    return stats


async def multi_strategy_scenario():
    """Test different execution strategies."""
    results = {}

    for strategy in strategies:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing strategy: {strategy}")
        logger.info("=" * 60)

        client = make_client()
        process_definition_key = await deploy_process(client)
        await cleanup_active_instances(client, process_definition_key)

        stats = await run_worker_scenario(
            client=client,
            process_definition_key=process_definition_key,
            worker_config=WorkerConfig(
                job_type="job-worker-load-test-1-task-1",
                job_timeout_milliseconds=JOB_TIMEOUT_MILLISECONDS,
                max_concurrent_jobs=10,
                execution_strategy=strategy,
            ),
            num_instances=10,
            scenario_timeout_seconds=60,
        )
        results[strategy] = stats

    # Print comparison
    logger.info(f"\n{'='*60}")
    logger.info("STRATEGY COMPARISON")
    logger.info("=" * 60)
    for strategy, stats in results.items():
        logger.info(
            f"{strategy:10} | {stats['jobs_per_second']:6.2f} jobs/sec | {stats['total_time']:6.2f}s total"
        )

    return results


async def benchmark_strategies(
    num_instances: int = 20,
    work_duration: float = 3.0,
    job_timeout_ms: int = JOB_TIMEOUT_MILLISECONDS,
    jitter_pct: float = 0.0,
):
    """Compare different strategies with multiple runs for statistical significance.

    Tests only CPU-bound workload across all strategies.

    Args:
        num_instances: Number of process instances to start per test run.
        work_duration: Duration of simulated work in seconds.
        job_timeout_ms: Job timeout in milliseconds.
        jitter_pct: Percentage of jitter to apply to work duration.
    """
    results = {}

    for strategy in strategies:
        results[strategy] = await run_test(
            num_instances=num_instances,
            strategy=strategy,
            workload_type="cpu",
            repeats=3,  # Run 3 times and average
            max_concurrent_jobs=10,
            timeout=60,
            work_duration=work_duration,
            job_timeout_ms=job_timeout_ms,
            jitter_pct=jitter_pct,
        )

    # Print final comparison
    logger.info(f"\n{'='*70}")
    logger.info("FINAL STRATEGY COMPARISON (CPU-bound workload)")
    logger.info(f"{'='*70}")
    logger.info(
        f"{'Strategy':<12} | {'Avg Time':<10} | {'Avg Throughput':<15} | {'Consistency'}"
    )
    logger.info(f"{'-'*70}")
    for strategy, stats in results.items():
        if stats["repeats"] > 1:
            # Show variability using coefficient of variation
            cv = (stats["total_time_std"] / stats["total_time_avg"]) * 100
            consistency = f"±{cv:.1f}%"
            logger.info(
                f"{strategy:<12} | {stats['total_time_avg']:>8.2f}s | {stats['jobs_per_second_avg']:>13.2f}/s | {consistency}"
            )
        else:
            logger.info(
                f"{strategy:<12} | {stats['total_time']:>8.2f}s | {stats['jobs_per_second']:>13.2f}/s | single run"
            )
    logger.info(f"{'='*70}\n")

    return results


async def benchmark_workloads(
    num_instances: int = 20,
    work_duration: float = 3.0,
    job_timeout_ms: int = JOB_TIMEOUT_MILLISECONDS,
    jitter_pct: float = 0.0,
):
    """Compare CPU-bound vs I/O-bound workloads across all strategies.

    Tests all combinations of strategies and workload types.

    Args:
        num_instances: Number of process instances to start per test run.
        work_duration: Duration of simulated work in seconds.
        job_timeout_ms: Job timeout in milliseconds.
        jitter_pct: Percentage of jitter to apply to work duration.
    """
    workload_types: list[Literal["cpu", "io"]] = ["cpu", "io"]
    results = {}

    for workload in workload_types:
        results[workload] = {}
        logger.info(f"\n{'='*70}")
        logger.info(f"TESTING {workload.upper()}-BOUND WORKLOAD")
        logger.info(f"{'='*70}\n")

        for strategy in strategies:
            logger.info(
                f"Running {strategy} strategy with {workload}-bound workload..."
            )
            results[workload][strategy] = await run_test(
                num_instances=num_instances,
                strategy=strategy,
                workload_type=workload,
                repeats=3,
                max_concurrent_jobs=10,
                timeout=60,
                work_duration=work_duration,
                job_timeout_ms=job_timeout_ms,
                jitter_pct=jitter_pct,
            )

    # Print comprehensive comparison
    logger.info(f"\n{'='*80}")
    logger.info("COMPREHENSIVE BENCHMARK: STRATEGIES × WORKLOAD TYPES")
    logger.info(f"{'='*80}")

    for workload in workload_types:
        logger.info(f"\n{workload.upper()}-BOUND WORKLOAD:")
        logger.info(f"{'-'*80}")
        logger.info(
            f"{'Strategy':<12} | {'Avg Time':<10} | {'Avg Throughput':<15} | {'Consistency'}"
        )
        logger.info(f"{'-'*80}")

        for strategy, stats in results[workload].items():
            if stats["repeats"] > 1:
                cv = (stats["total_time_std"] / stats["total_time_avg"]) * 100
                consistency = f"±{cv:.1f}%"
                logger.info(
                    f"{strategy:<12} | {stats['total_time_avg']:>8.2f}s | {stats['jobs_per_second_avg']:>13.2f}/s | {consistency}"
                )
            else:
                logger.info(
                    f"{strategy:<12} | {stats['total_time']:>8.2f}s | {stats['jobs_per_second']:>13.2f}/s | single run"
                )

    # Print side-by-side comparison
    logger.info(f"\n{'='*80}")
    logger.info("SIDE-BY-SIDE COMPARISON")
    logger.info(f"{'='*80}")
    logger.info(
        f"{'Strategy':<12} | {'CPU Throughput':<15} | {'I/O Throughput':<15} | {'Best For'}"
    )
    logger.info(f"{'-'*80}")

    for strategy in strategies:
        cpu_stats = results["cpu"][strategy]
        io_stats = results["io"][strategy]

        # Handle both single run (jobs_per_second) and multiple runs (jobs_per_second_avg)
        cpu_throughput = cpu_stats.get("jobs_per_second_avg") or cpu_stats.get(
            "jobs_per_second", 0
        )
        io_throughput = io_stats.get("jobs_per_second_avg") or io_stats.get(
            "jobs_per_second", 0
        )

        # Determine which workload type this strategy is better for
        if cpu_throughput > io_throughput * 1.1:  # 10% threshold
            best_for = "CPU-bound"
        elif io_throughput > cpu_throughput * 1.1:
            best_for = "I/O-bound"
        else:
            best_for = "Both"

        logger.info(
            f"{strategy:<12} | {cpu_throughput:>13.2f}/s | {io_throughput:>13.2f}/s | {best_for}"
        )

    logger.info(f"{'='*80}\n")

    return results


async def benchmark_subprocess(
    num_instances: int = 20,
    work_duration: float = 3.0,
    job_timeout_ms: int = JOB_TIMEOUT_MILLISECONDS,
    jitter_pct: float = 0.0,
):
    """Test subprocess workload across all strategies.

    This benchmark specifically tests subprocess.call() behavior to see if it crashes
    or has issues with different execution strategies (especially multi-threaded vs async).

    Args:
        num_instances: Number of process instances to start per test run.
        work_duration: Duration of simulated work in seconds.
        job_timeout_ms: Job timeout in milliseconds.
        jitter_pct: Percentage of jitter to apply to work duration.
    """
    logger.info(f"\n{'='*70}")
    logger.info("SUBPROCESS WORKLOAD BENCHMARK")
    logger.info(f"{'='*70}")
    logger.info("Testing subprocess.call() behavior across execution strategies")
    logger.info("This tests for potential crashes or deadlocks with subprocess calls")
    logger.info(f"{'='*70}\n")

    results = {}

    for strategy in strategies:
        logger.info(f"Testing {strategy} strategy with subprocess workload...")
        try:
            results[strategy] = await run_test(
                num_instances=num_instances,
                strategy=strategy,
                workload_type="subprocess",
                repeats=3,
                max_concurrent_jobs=10,
                timeout=120,  # Longer timeout for subprocess calls
                work_duration=work_duration,
                job_timeout_ms=job_timeout_ms,
                jitter_pct=jitter_pct,
            )
            logger.info(f"✓ {strategy} strategy completed successfully")
        except Exception as e:
            logger.error(f"✗ {strategy} strategy FAILED: {e}")
            results[strategy] = {"error": str(e)}

    # Print final comparison
    logger.info(f"\n{'='*70}")
    logger.info("SUBPROCESS BENCHMARK RESULTS")
    logger.info(f"{'='*70}")
    logger.info(
        f"{'Strategy':<12} | {'Avg Time':<10} | {'Avg Throughput':<15} | {'Status'}"
    )
    logger.info(f"{'-'*70}")

    for strategy, stats in results.items():
        if "error" in stats:
            logger.info(
                f"{strategy:<12} | {'N/A':<10} | {'N/A':<15} | FAILED: {stats['error']}"
            )
        elif stats["repeats"] > 1:
            cv = (stats["total_time_std"] / stats["total_time_avg"]) * 100
            consistency = f"±{cv:.1f}%"
            logger.info(
                f"{strategy:<12} | {stats['total_time_avg']:>8.2f}s | {stats['jobs_per_second_avg']:>13.2f}/s | OK {consistency}"
            )
        else:
            logger.info(
                f"{strategy:<12} | {stats['total_time']:>8.2f}s | {stats['jobs_per_second']:>13.2f}/s | OK (single run)"
            )

    logger.info(f"{'='*70}\n")

    return results


async def quick_test():
    """Quick single test - useful for development."""
    return await run_test(
        num_instances=5,
        strategy="auto",
        workload_type="cpu",
        repeats=1,
        max_concurrent_jobs=5,
        timeout=30,
    )


async def stress_test():
    """Heavy load test with multiple runs."""
    return await run_test(
        num_instances=100,
        strategy="auto",
        workload_type="cpu",
        repeats=3,
        max_concurrent_jobs=50,
        timeout=120,
    )


def main():
    """Entry point - run the simple scenario by default."""
    parser = argparse.ArgumentParser(description="Camunda Job Worker Benchmark Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Test command
    test_parser = subparsers.add_parser("test", help="Run a parameterized test")
    test_parser.add_argument(
        "--process_instances", type=int, default=10, help="Number of process instances"
    )
    test_parser.add_argument(
        "--worker_strategy",
        type=str,
        default="auto",
        choices=strategies,
        help="Execution strategy",
    )
    test_parser.add_argument(
        "--workload_type",
        type=str,
        default="cpu",
        choices=["cpu", "io", "subprocess", "subprocess_threaded"],
        help="Workload type",
    )
    test_parser.add_argument(
        "--repeat_runs", type=int, default=1, help="Number of repeats"
    )
    test_parser.add_argument(
        "--max_concurrent_jobs", type=int, default=10, help="Max concurrent jobs"
    )
    test_parser.add_argument(
        "--work_duration_seconds",
        type=float,
        default=3.0,
        help="Duration of simulated work in seconds",
    )
    test_parser.add_argument(
        "--job_timeout_milliseconds",
        type=int,
        default=JOB_TIMEOUT_MILLISECONDS,
        help="Job timeout in milliseconds",
    )
    test_parser.add_argument(
        "--jitter_pct",
        type=float,
        default=0.25,
        help="Percentage of jitter to apply to work duration (0.0 to 1.0)",
    )

    # Benchmark command
    bench_parser = subparsers.add_parser("benchmark", help="Benchmark strategies")
    bench_parser.add_argument(
        "--process_instances", type=int, default=20, help="Number of process instances"
    )
    bench_parser.add_argument(
        "--work_duration_seconds",
        type=float,
        default=3.0,
        help="Duration of simulated work in seconds",
    )
    bench_parser.add_argument(
        "--job_timeout_milliseconds",
        type=int,
        default=JOB_TIMEOUT_MILLISECONDS,
        help="Job timeout in milliseconds",
    )
    bench_parser.add_argument(
        "--jitter_pct",
        type=float,
        default=0.25,
        help="Percentage of jitter to apply to work duration (0.0 to 1.0)",
    )

    # Benchmark workloads command
    bench_work_parser = subparsers.add_parser(
        "benchmark-workloads", help="Benchmark workloads"
    )
    bench_work_parser.add_argument(
        "--process_instances", type=int, default=20, help="Number of process instances"
    )
    bench_work_parser.add_argument(
        "--work_duration_seconds",
        type=float,
        default=3.0,
        help="Duration of simulated work in seconds",
    )
    bench_work_parser.add_argument(
        "--job_timeout_milliseconds",
        type=int,
        default=JOB_TIMEOUT_MILLISECONDS,
        help="Job timeout in milliseconds",
    )
    bench_work_parser.add_argument(
        "--jitter_pct",
        type=float,
        default=0.0,
        help="Percentage of jitter to apply to work duration (0.0 to 1.0)",
    )

    # Benchmark subprocess command
    bench_sub_parser = subparsers.add_parser(
        "benchmark-subprocess", help="Benchmark subprocess"
    )
    bench_sub_parser.add_argument(
        "--process_instances", type=int, default=20, help="Number of process instances"
    )
    bench_sub_parser.add_argument(
        "--work_duration_seconds",
        type=float,
        default=3.0,
        help="Duration of simulated work in seconds",
    )
    bench_sub_parser.add_argument(
        "--job_timeout_milliseconds",
        type=int,
        default=JOB_TIMEOUT_MILLISECONDS,
        help="Job timeout in milliseconds",
    )
    bench_sub_parser.add_argument(
        "--jitter_pct",
        type=float,
        default=0.25,
        help="Percentage of jitter to apply to work duration (0.0 to 1.0)",
    )

    # Quick command
    subparsers.add_parser("quick", help="Run a quick test")

    # Stress command
    subparsers.add_parser("stress", help="Run a stress test")

    # Load command
    subparsers.add_parser("load", help="Run a load test")

    # Multi command
    subparsers.add_parser("multi", help="Run multi-strategy scenario")

    args = parser.parse_args()

    if args.command == "test":
        asyncio.run(
            run_test(
                num_instances=args.process_instances,
                strategy=args.worker_strategy,
                workload_type=args.workload_type,
                repeats=args.repeat_runs,
                max_concurrent_jobs=args.max_concurrent_jobs,
                work_duration=args.work_duration_seconds,
                job_timeout_ms=args.job_timeout_milliseconds,
                jitter_pct=args.jitter_pct,
            )
        )
    elif args.command == "benchmark":
        asyncio.run(
            benchmark_strategies(
                num_instances=args.process_instances,
                work_duration=args.work_duration_seconds,
                job_timeout_ms=args.job_timeout_milliseconds,
                jitter_pct=args.jitter_pct,
            )
        )
    elif args.command == "benchmark-workloads":
        asyncio.run(
            benchmark_workloads(
                num_instances=args.process_instances,
                work_duration=args.work_duration_seconds,
                job_timeout_ms=args.job_timeout_milliseconds,
                jitter_pct=args.jitter_pct,
            )
        )
    elif args.command == "benchmark-subprocess":
        asyncio.run(
            benchmark_subprocess(
                num_instances=args.process_instances,
                work_duration=args.work_duration_seconds,
                job_timeout_ms=args.job_timeout_milliseconds,
                jitter_pct=args.jitter_pct,
            )
        )
    elif args.command == "quick":
        asyncio.run(quick_test())
    elif args.command == "stress":
        asyncio.run(stress_test())
    elif args.command == "load":
        asyncio.run(load_test_scenario())
    elif args.command == "multi":
        asyncio.run(multi_strategy_scenario())
    else:
        # Default: run simple scenario if no command provided
        asyncio.run(simple_scenario())


if __name__ == "__main__":
    main()
