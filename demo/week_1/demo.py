import asyncio
from functools import partial
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.runtime.job_worker import WorkerConfig
from camunda_orchestration_sdk.models.processcreationbykey import Processcreationbykey

from cancel_processes import cancel_running_process_instances
from cpu_bound_workload import simulate_cpu_work  # pyright: ignore[reportUnusedImport]
from io_bound_workload import (
    simulate_io_work_async, # pyright: ignore[reportUnusedImport]
)  
from subprocess_workload import simulate_subprocess_work # pyright: ignore[reportUnusedImport]

NUM_PROCESSES_TO_START = 10
WORK_DURATION_SECONDS = 5


async def main():
    camunda = CamundaClient()

    # Deploy the process definition
    deployed_resources = await camunda.deploy_resources_from_files_async(
        files=["./tests/integration/resources/job_worker_load_test_process_1.bpmn"]
    )

    # Access the process definition from the  result
    process_definition = deployed_resources.processes[0]
    process_definition_key = process_definition.process_definition_key
    process_definition_id = process_definition.process_definition_id

    print(
        f"Deployed process definition: {process_definition_id} (Key: {process_definition_key})"
    )

    cancel_running_process_instances(
        camunda, process_definition_key=process_definition_key
    )

    # Configure and start the worker
    config = WorkerConfig(
        job_type="job-worker-load-test-1-task-1",
        job_timeout_milliseconds=30_000,
        max_concurrent_jobs=5,
        execution_strategy="process",
    )

    # Single worker starts and starts working on jobs
    camunda.create_job_worker(
        config=config,
        callback=partial(
            simulate_subprocess_work, 
            duration=WORK_DURATION_SECONDS
        ),
    )

    # Start process instances
    for i in range(NUM_PROCESSES_TO_START):
        process_instance = await camunda.create_process_instance_async(
            data=Processcreationbykey(process_definition_key=process_definition_key)
        )

        print(
            f"Started process instance {i}/{NUM_PROCESSES_TO_START}: {process_instance.process_instance_key}"
        )

    # Keep the script running to allow the worker to process jobs
    try:
        await camunda.run_workers()
    except KeyboardInterrupt:
        print("Stopping workers...")


if __name__ == "__main__":
    asyncio.run(main())
