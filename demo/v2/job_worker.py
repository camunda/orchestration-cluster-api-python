import asyncio
import os
import time
from typing import Callable, Literal, get_args
from loguru import logger
from camunda_orchestration_sdk.semantic_types import ProcessDefinitionKey
from camunda_orchestration_sdk.models.complete_job_data import CompleteJobData
from camunda_orchestration_sdk.models.complete_job_data_variables_type_0 import (
    CompleteJobDataVariablesType0,
)
from camunda_orchestration_sdk.models.processcreationbykey import Processcreationbykey
from camunda_orchestration_sdk.models.state_exactmatch_3 import StateExactmatch3
from camunda_orchestration_sdk.types import File
from camunda_orchestration_sdk.models.activate_jobs_response_200_jobs_item import (
    ActivateJobsResponse200JobsItem,
)
from camunda_orchestration_sdk.models.create_deployment_data import CreateDeploymentData
from camunda_orchestration_sdk.models.search_process_instances_data import (
    SearchProcessInstancesData,
)
from camunda_orchestration_sdk.models.search_process_instances_data_filter import (
    SearchProcessInstancesDataFilter,
)
from camunda_orchestration_sdk import CamundaClient, WorkerConfig
from camunda_orchestration_sdk.runtime.job_worker import ExecutionHint, EXECUTION_STRATEGY

strategies = [s for arg in get_args(EXECUTION_STRATEGY) for s in get_args(arg)]

def make_client(base_url: str | None = None) -> CamundaClient:
    """Create a new Camunda client instance.

    Args:
        base_url: Override the base URL. Defaults to CAMUNDA_BASE_URL env var or localhost.
    """
    host = base_url or os.environ.get("CAMUNDA_BASE_URL", "http://localhost:8080/v2")
    return CamundaClient(base_url=host)


def simulate_cpu_work(duration: float):
    """Simulate CPU-bound work by spinning in a loop."""
    end_time = time.time() + duration
    while time.time() < end_time:
        pass


def create_default_callback(
    client: CamundaClient,
    job_counter: dict[str, int] | None = None,
    strategy: str = "async"
) -> Callable:
    """Create a default job callback that completes jobs with dummy data.

    Args:
        client: The Camunda client to use for completing jobs.
        job_counter: Optional dict to track completed jobs. If provided, increments 'completed' key.
        strategy: Execution strategy - determines whether to create async or sync callback.

    Returns:
        A callback function (async or sync depending on strategy).
    """
    if strategy in ["async", "auto"]:
        @ExecutionHint.async_safe
        async def async_callback(job: ActivateJobsResponse200JobsItem):
            # Simulate some CPU / IO-bound work
            logger.info(f"Starting work on: {job.job_key}")
            simulate_cpu_work(3)
            logger.info(f"Finished work on: {job.job_key}")
            # Example of completing a job
            await client.complete_job_async(
                job_key=job.job_key,
                data=CompleteJobData(
                    variables=CompleteJobDataVariablesType0().from_dict(
                        {"quoteAmount": 2345432}
                    )
                ),
            )

            # Track completion if counter provided
            if job_counter is not None:
                job_counter['completed'] = job_counter.get('completed', 0) + 1
                logger.info(f"Jobs completed: {job_counter['completed']}")

        return async_callback
    else:
        # For thread/process strategies, create a synchronous callback
        @ExecutionHint.io_bound
        def sync_callback(job: ActivateJobsResponse200JobsItem):
            # Simulate some CPU / IO-bound work
            logger.info(f"Starting work on: {job.job_key}")
            simulate_cpu_work(3)
            logger.info(f"Finished work on: {job.job_key}")
            # Example of completing a job synchronously
            client.complete_job(
                job_key=job.job_key,
                data=CompleteJobData(
                    variables=CompleteJobDataVariablesType0().from_dict(
                        {"quoteAmount": 2345432}
                    )
                ),
            )

            # Track completion if counter provided
            if job_counter is not None:
                job_counter['completed'] = job_counter.get('completed', 0) + 1
                logger.info(f"Jobs completed: {job_counter['completed']}")

        return sync_callback


async def deploy_process(
    client: CamundaClient,
    bpmn_path: str = "./demo/v2/resources/job_worker_load_test_process_1.bpmn"
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


async def cleanup_active_instances(client: CamundaClient, process_definition_key: str) -> None:
    """Cancel all active instances of a process.

    Args:
        client: The Camunda client to use.
        process_definition_key: The process definition key to clean up.
    """
    search_query = SearchProcessInstancesData(
        filter_=SearchProcessInstancesDataFilter(
            process_definition_key=process_definition_key,
            state=StateExactmatch3("ACTIVE"),
        )
    )
    already_running = client.search_process_instances(data=search_query)
    for process in already_running.items:
        logger.info(f"Canceling process instance: {process.process_instance_key}")
        await client.cancel_process_instance_async(
            data=None, process_instance_key=process.process_instance_key
        )


async def run_worker_scenario(
    client: CamundaClient,
    process_definition_key: ProcessDefinitionKey,
    worker_config: WorkerConfig,
    num_instances: int = 1,
    expected_jobs: int | None = None,
    scenario_timeout_seconds: int | None = 30
) -> dict[str, float]:
    """Run a worker scenario with configurable settings.

    Args:
        client: The Camunda client to use.
        process_definition_key: The process to start instances of.
        worker_config: Configuration for the worker.
        num_instances: Number of process instances to start.
        expected_jobs: Number of jobs to wait for before stopping. If None, uses num_instances.
        timeout: Timeout in seconds to run the worker. None means run indefinitely.

    Returns:
        dict with timing stats: {'total_time', 'jobs_completed', 'jobs_per_second', 'expected_jobs'}
    """
    logger.debug(f'Running worker with config: {worker_config}')
    if expected_jobs is None:
        expected_jobs = num_instances

    # Job counter to track completions
    job_counter = {'completed': 0, 'start_time': None}

    # Create callback with counter (pass strategy to create appropriate callback type)
    tracked_callback = create_default_callback(client, job_counter, worker_config.execution_strategy)

    # Start process instances
    logger.info(f"\n=== Starting {num_instances} process instances ===")
    for i in range(num_instances):
        process_instance = client.create_process_instance(
            data=Processcreationbykey(process_definition_key=process_definition_key)
        )
        logger.info(f"Started process instance {i+1}/{num_instances}: {process_instance.process_instance_key}")

    # Record start time after all instances are started
    job_counter['start_time'] = time.time()
    logger.info(f"\n=== All instances started. Waiting for {expected_jobs} jobs to complete ===")

    # Create worker
    client.create_job_worker(config=worker_config, callback=tracked_callback)

    # Monitor for completion
    async def wait_for_completion():
        while job_counter['completed'] < expected_jobs:
            await asyncio.sleep(0.1)  # Check every 100ms

    # Run workers and monitor concurrently
    worker_task = asyncio.create_task(client.run_workers())

    try:
        if scenario_timeout_seconds is not None:
            await asyncio.wait_for(wait_for_completion(), timeout=scenario_timeout_seconds)
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
        total_time = end_time - job_counter['start_time']
        jobs_completed = job_counter['completed']
        jobs_per_second = jobs_completed / total_time if total_time > 0 else 0

        logger.info(f"\n=== Test Complete ===")
        logger.info(f"Jobs completed: {jobs_completed}/{expected_jobs}")
        logger.info(f"Total time: {total_time:.2f}s")
        logger.info(f"Throughput: {jobs_per_second:.2f} jobs/second")

        result = {
            'total_time': total_time,
            'jobs_completed': jobs_completed,
            'jobs_per_second': jobs_per_second,
            'expected_jobs': expected_jobs
        }
        return result


async def run_test(
    num_instances: int = 10,
    strategy: EXECUTION_STRATEGY = "auto",
    max_concurrent_jobs: int = 10,
    repeats: int = 1,
    timeout: int = 5000
) -> dict[str, float]:
    """Run a parameterized test with optional averaging over multiple runs.

    Args:
        num_instances: Number of process instances to start per run.
        strategy: Execution strategy ("auto", "async", "thread", "process").
        max_concurrent_jobs: Maximum concurrent jobs for the worker.
        repeats: Number of times to repeat the test (results will be averaged).
        timeout: Timeout in seconds for each run.

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
                job_timeout_milliseconds=5000,
                max_concurrent_jobs=max_concurrent_jobs,
                execution_strategy=strategy,
            ),
            num_instances=num_instances,
            scenario_timeout_seconds=timeout
        )
        all_stats.append(stats)

        if repeats > 1:
            logger.info(f"\nRun {run_num + 1} Summary:")
            logger.info(f"  Time: {stats['total_time']:.2f}s")
            logger.info(f"  Throughput: {stats['jobs_per_second']:.2f} jobs/sec")

    # Calculate averages if multiple runs
    if repeats == 1:
        result = all_stats[0]
        result['repeats'] = 1
        return result
    else:
        total_times = [s['total_time'] for s in all_stats]
        throughputs = [s['jobs_per_second'] for s in all_stats]

        result = {
            'total_time_avg': sum(total_times) / len(total_times),
            'total_time_min': min(total_times),
            'total_time_max': max(total_times),
            'total_time_std': (sum((x - sum(total_times)/len(total_times))**2 for x in total_times) / len(total_times)) ** 0.5,
            'jobs_per_second_avg': sum(throughputs) / len(throughputs),
            'jobs_per_second_min': min(throughputs),
            'jobs_per_second_max': max(throughputs),
            'jobs_per_second_std': (sum((x - sum(throughputs)/len(throughputs))**2 for x in throughputs) / len(throughputs)) ** 0.5,
            'jobs_completed': all_stats[0]['jobs_completed'],
            'expected_jobs': all_stats[0]['expected_jobs'],
            'repeats': repeats,
            'all_runs': all_stats
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
            job_timeout_milliseconds=5000,
            max_concurrent_jobs=10,
            execution_strategy="auto",
        ),
        num_instances=1
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
            job_timeout_milliseconds=5000,
            max_concurrent_jobs=50,  # Higher concurrency
            execution_strategy="auto",
        ),
        num_instances=100,  # More instances
        scenario_timeout_seconds=120  # 2 minute timeout for load test
    )
    return stats


async def multi_strategy_scenario():
    """Test different execution strategies."""
    results = {}

    for strategy in strategies:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing strategy: {strategy}")
        logger.info('='*60)

        client = make_client()
        process_definition_key = await deploy_process(client)
        await cleanup_active_instances(client, process_definition_key)

        stats = await run_worker_scenario(
            client=client,
            process_definition_key=process_definition_key,
            worker_config=WorkerConfig(
                job_type="job-worker-load-test-1-task-1",
                job_timeout_milliseconds=5000,
                max_concurrent_jobs=10,
                execution_strategy=strategy,
            ),
            num_instances=10,
            scenario_timeout_seconds=60
        )
        results[strategy] = stats

    # Print comparison
    logger.info(f"\n{'='*60}")
    logger.info("STRATEGY COMPARISON")
    logger.info('='*60)
    for strategy, stats in results.items():
        logger.info(f"{strategy:10} | {stats['jobs_per_second']:6.2f} jobs/sec | {stats['total_time']:6.2f}s total")

    return results


async def benchmark_strategies():
    """Compare different strategies with multiple runs for statistical significance."""
    results = {}

    for strategy in strategies:
        results[strategy] = await run_test(
            num_instances=20,
            strategy=strategy,
            max_concurrent_jobs=10,
            repeats=3,  # Run 3 times and average
            timeout=60
        )

    # Print final comparison
    logger.info(f"\n{'='*70}")
    logger.info("FINAL STRATEGY COMPARISON")
    logger.info(f"{'='*70}")
    logger.info(f"{'Strategy':<12} | {'Avg Time':<10} | {'Avg Throughput':<15} | {'Consistency'}")
    logger.info(f"{'-'*70}")
    for strategy, stats in results.items():
        if stats['repeats'] > 1:
            # Show variability using coefficient of variation
            cv = (stats['total_time_std'] / stats['total_time_avg']) * 100
            consistency = f"±{cv:.1f}%"
            logger.info(f"{strategy:<12} | {stats['total_time_avg']:>8.2f}s | {stats['jobs_per_second_avg']:>13.2f}/s | {consistency}")
        else:
            logger.info(f"{strategy:<12} | {stats['total_time']:>8.2f}s | {stats['jobs_per_second']:>13.2f}/s | single run")
    logger.info(f"{'='*70}\n")

    return results


async def quick_test():
    """Quick single test - useful for development."""
    return await run_test(
        num_instances=5,
        strategy="auto",
        max_concurrent_jobs=5,
        repeats=1,
        timeout=30
    )


async def stress_test():
    """Heavy load test with multiple runs."""
    return await run_test(
        num_instances=100,
        strategy="auto",
        max_concurrent_jobs=50,
        repeats=3,
        timeout=120
    )


def main():
    """Entry point - run the simple scenario by default."""
    import sys

    if len(sys.argv) > 1:
        scenario = sys.argv[1]

        if scenario == "test":
            # Parse test parameters from command line
            num_instances = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            strategy_arg = sys.argv[3] if len(sys.argv) > 3 else "auto"
            if strategy_arg not in strategies:
                logger.error(f"Invalid strategy: {strategy_arg}. Valid options: {strategies}")
                sys.exit(1)
            strategy: EXECUTION_STRATEGY = strategy_arg  # type: ignore
            repeats = int(sys.argv[4]) if len(sys.argv) > 4 else 1
            max_concurrent = int(sys.argv[5]) if len(sys.argv) > 5 else 10

            asyncio.run(run_test(
                num_instances=num_instances,
                strategy=strategy,
                max_concurrent_jobs=max_concurrent,
                repeats=repeats
            ))
        elif scenario == "benchmark":
            asyncio.run(benchmark_strategies())
        elif scenario == "quick":
            asyncio.run(quick_test())
        elif scenario == "stress":
            asyncio.run(stress_test())
        elif scenario == "load":
            asyncio.run(load_test_scenario())
        elif scenario == "multi":
            asyncio.run(multi_strategy_scenario())
        else:
            logger.error(f"Unknown scenario: {scenario}")
            logger.info("Available scenarios: test, benchmark, quick, stress, load, multi")
            sys.exit(1)
    else:
        # Default: run simple scenario
        asyncio.run(simple_scenario())


if __name__ == "__main__":
    main()
