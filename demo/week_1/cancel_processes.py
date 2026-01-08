from camunda_orchestration_sdk import CamundaClient, ProcessDefinitionKey
from camunda_orchestration_sdk.models.search_process_instances_data import (
    SearchProcessInstancesData,
)
from camunda_orchestration_sdk.models.search_process_instances_data_filter import (
    SearchProcessInstancesDataFilter,
)
from camunda_orchestration_sdk.models.state_advancedfilter_6 import StateAdvancedfilter6
from camunda_orchestration_sdk.models.state_advancedfilter_6_eq import (
    StateAdvancedfilter6Eq,
)

def cancel_running_process_instances(client: CamundaClient, process_definition_key: ProcessDefinitionKey):
     # Cancel all running instances of process
    searchQuery = SearchProcessInstancesData(
        filter_=SearchProcessInstancesDataFilter(
            process_definition_key=process_definition_key,
            state=StateAdvancedfilter6(eq=StateAdvancedfilter6Eq("ACTIVE")),
        )
    )
    print('Searching for already running process instances...')
    alreadyRunningProcesses = client.search_process_instances(data=searchQuery)
    print(f'Found {len(alreadyRunningProcesses.items)} processes to cancel.')
    for process in alreadyRunningProcesses.items:
        print(f"Canceling process instance: {process.process_instance_key}")
        client.cancel_process_instance(
            data=None, process_instance_key=process.process_instance_key
        )
