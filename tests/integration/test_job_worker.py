import os
from camunda_orchestration_sdk.models.deployment_process_result import (
    DeploymentProcessResult,
)
from camunda_orchestration_sdk.models.process_creation_by_key import (
    ProcessCreationByKey,
)
from camunda_orchestration_sdk.types import File

from camunda_orchestration_sdk.models.create_deployment_data import CreateDeploymentData
from camunda_orchestration_sdk.models.search_process_instances_data import (
    SearchProcessInstancesData,
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
from loguru import logger
import pytest
from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.runtime.job_worker import WorkerConfig, JobContext
from typing import cast

pytestmark = pytest.mark.skipif(
    os.environ.get("CAMUNDA_INTEGRATION") != "1",
    reason="Integration tests are disabled unless CAMUNDA_INTEGRATION=1",
)


def _make_client():
    return CamundaAsyncClient()


# TODO: workloads (maybe multiple with different scenarios)
# TODO: multiplex on execution_strategy


# Worker callback function
def callback(job: JobContext):
    # Simulate some CPU / IO-bound work
    logger.info(f"Job Key: {job.job_key}")
    return


@pytest.mark.asyncio
async def test_job_worker_performance():
    async with _make_client() as camunda:
        with open(
            "./tests/integration/resources/job_worker_load_test_process_1.bpmn", "rb"
        ) as f:
            process_file = File(
                payload=f, file_name="job_worker_load_test_process_1.bpmn"
            )
            deployed_resources = await camunda.create_deployment(
                data=CreateDeploymentData(resources=[process_file])
            )

        process_definition = cast(
            DeploymentProcessResult,
            deployed_resources.deployments[0].process_definition,
        )

        process_definition_key = process_definition.process_definition_key
        _ = process_definition.process_definition_id

        # Cancel all running instances of process
        searchQuery = SearchProcessInstancesData(
            filter_=ProcessInstanceSearchQueryFilter(
                process_definition_key=process_definition_key,
                state=AdvancedProcessInstanceStateFilter(
                    eq=AdvancedProcessInstanceStateFilterEq("ACTIVE")
                ),
            )
        )
        alreadyRunningProcesses = await camunda.search_process_instances(
            data=searchQuery
        )
        for process in alreadyRunningProcesses.items:
            print(f"Canceling process instance: {process.process_instance_key}")
            await camunda.cancel_process_instance(
                data=None, process_instance_key=process.process_instance_key
            )
        # Start 100 instances

        config = WorkerConfig(
            job_type="load-test",
            execution_strategy="auto",
            job_timeout_milliseconds=30_000,
        )

        # Single worker starts and starts working on jobs
        _ = camunda.create_job_worker(config=config, callback=callback)

        process_instance = await camunda.create_process_instance(
            data=ProcessCreationByKey(process_definition_key=process_definition_key)
        )

        print(f"Started process instance: {process_instance.process_instance_key}")
