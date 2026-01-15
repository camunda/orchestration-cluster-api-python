import asyncio
import os
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
from camunda_orchestration_sdk.runtime.job_worker import ExecutionHint, JobContext


def _make_client():
    host = os.environ.get("CAMUNDA_REST_ADDRESS")
    if host:
        return CamundaClient(configuration={"CAMUNDA_REST_ADDRESS": host})
    return CamundaClient()


# TODO: workloads (maybe multiple with different scenarios)
# TODO: multiplex on execution_strategy

camunda = _make_client()


# Worker callback function
@ExecutionHint.async_safe
async def callback(job: JobContext):
    # Simulate some CPU / IO-bound work
    print(f"**** Job Worker **** \nJob Key: {job.job_key}")
    # Example of completing a job
    return {"quoteAmount": 2345432}


async def main():
    with open("./demo/v2/resources/job_worker_load_test_process_1.bpmn", "rb") as f:
        process_file = File(payload=f, file_name="job_worker_load_test_process_1.bpmn")
        deployed_resources = await camunda.create_deployment_async(
            data=CreateDeploymentData(resources=[process_file])
        )

    process_definition_key = deployed_resources.deployments[0].process_definition.process_definition_key  # type: ignore

    # Cancel all running instances of process
    searchQuery = SearchProcessInstancesData(
        filter_=SearchProcessInstancesDataFilter(
            process_definition_key=process_definition_key,
            state=StateExactmatch3("ACTIVE"),
        )
    )
    alreadyRunningProcesses = camunda.search_process_instances(data=searchQuery)
    for process in alreadyRunningProcesses.items:
        print(f"Canceling process instance: {process.process_instance_key}")
        await camunda.cancel_process_instance_async(
            data=None, process_instance_key=process.process_instance_key
        )

    # config = WorkerConfig(job_type='load-test', execution_strategy="auto", timeout=30_000)

    # Single worker starts and starts working on jobs

    # Start 100 instances
    process_instance = camunda.create_process_instance(
        data=Processcreationbykey(process_definition_key=process_definition_key)
    )
    print(f"Started process instance: {process_instance.process_instance_key}")

    camunda.create_job_worker(
        config=WorkerConfig(
            job_type="job-worker-load-test-1-task-1",
            timeout=5000,
            max_concurrent_jobs=10,
            execution_strategy="auto",
        ),
        callback=callback,
    )
    await camunda.run_workers()


if __name__ == "__main__":
    asyncio.run(main())
