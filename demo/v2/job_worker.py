import asyncio
import os
from camunda_orchestration_sdk.models.create_deployment_response_200_deployments_item_process_definition import CreateDeploymentResponse200DeploymentsItemProcessDefinition
from camunda_orchestration_sdk.models.processcreationbykey import Processcreationbykey
from camunda_orchestration_sdk.types import File
from camunda_orchestration_sdk.models.activate_jobs_response_200_jobs_item import ActivateJobsResponse200JobsItem
from camunda_orchestration_sdk.models.create_deployment_body import CreateDeploymentBody
from camunda_orchestration_sdk.models.search_process_instances_body import SearchProcessInstancesBody
from camunda_orchestration_sdk.models.search_process_instances_body_filter import SearchProcessInstancesBodyFilter
from camunda_orchestration_sdk.models.state_advancedfilter_6 import StateAdvancedfilter6
from camunda_orchestration_sdk.models.state_advancedfilter_6_eq import StateAdvancedfilter6Eq
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.runtime.job_worker import JobWorker, WorkerConfig

def _make_client():
    host = os.environ.get("CAMUNDA_BASE_URL", "http://localhost:8080/v2")
    return CamundaClient(base_url=host)

# TODO: workloads (maybe multiple with different scenarios)
# TODO: multiplex on execution_strategy

# Worker callback function
def callback(job: ActivateJobsResponse200JobsItem):
    # Simulate some CPU / IO-bound work
    print(f'Job Key: {job.job_key}')

async def main():
    async with _make_client() as camunda:
        with open('./tests/integration/resources/job_worker_load_test_process_1.bpmn', 'rb') as f:
            process_file = File(payload=f, file_name='job_worker_load_test_process_1.bpmn')
            deployed_resources = await camunda.create_deployment_async(data=CreateDeploymentBody(resources=[process_file]))

        process_definition: CreateDeploymentResponse200DeploymentsItemProcessDefinition = deployed_resources.deployments[0].process_definition # type: ignore
        # Cancel all running instances of process
        searchQuery = SearchProcessInstancesBody(
            filter_=SearchProcessInstancesBodyFilter(
                process_definition_key=process_definition.process_definition_key, 
                state=StateAdvancedfilter6(eq=StateAdvancedfilter6Eq('ACTIVE'))
                )
        )
        alreadyRunningProcesses = camunda.search_process_instances(data=searchQuery)
        for process in alreadyRunningProcesses.items:
            print(f'Canceling process instance: {process.process_instance_key}')
            await camunda.cancel_process_instance_async(data=None, process_instance_key=process.process_instance_key)

        config = WorkerConfig(job_type='load-test', execution_strategy="auto", timeout=30_000)
        
        # Single worker starts and starts working on jobs

        # Start 100 instances
        process_instance = camunda.create_process_instance(data=Processcreationbykey(process_definition_key=process_definition.process_definition_key))
        print(f'Started process instance: {process_instance.process_instance_key}')

        worker = JobWorker(callback=callback, client=camunda, config=config)

if __name__ == "__main__":
    asyncio.run(main())