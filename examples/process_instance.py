# Compilable usage examples for process instance operations.
# These examples are type-checked during build to guard against API regressions.
from __future__ import annotations

from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.models.limit_based_pagination import (
    LimitBasedPagination,
)
from camunda_orchestration_sdk.models.process_creation_by_id import (
    ProcessCreationById,
)
from camunda_orchestration_sdk.models.process_creation_by_key import (
    ProcessCreationByKey,
)
from camunda_orchestration_sdk.models.process_instance_search_query_filter import (
    ProcessInstanceSearchQueryFilter,
)
from camunda_orchestration_sdk.models.process_instance_search_query_sort_request import (
    ProcessInstanceSearchQuerySortRequest,
)
from camunda_orchestration_sdk.models.process_instance_search_query_sort_request_field import (
    ProcessInstanceSearchQuerySortRequestField,
)
from camunda_orchestration_sdk.models.process_instance_search_query import (
    ProcessInstanceSearchQuery,
)
from camunda_orchestration_sdk.models.sort_order_enum import SortOrderEnum
from camunda_orchestration_sdk.semantic_types import (
    ProcessDefinitionId,
    ProcessDefinitionKey,
)


# region CreateProcessInstanceByKey
def create_process_instance_by_key_example() -> None:
    client = CamundaClient()

    # Deploy a process and obtain the typed key from the response
    deployment = client.deploy_resources_from_files(["order-process.bpmn"])
    process_key = deployment.processes[0].process_definition_key

    # Use the typed key directly — no manual string lifting needed
    result = client.create_process_instance(
        data=ProcessCreationByKey(
            process_definition_key=process_key,
        )
    )

    print(f"Process instance key: {result.process_instance_key}")
# endregion CreateProcessInstanceByKey


# region CreateProcessInstanceByKeyFromStorage
def create_process_instance_by_key_from_storage_example() -> None:
    client = CamundaClient()

    # When restoring a key from a database or message queue,
    # wrap the raw string with the semantic type constructor:
    stored_key = "2251799813685249"  # e.g. from a DB row
    result = client.create_process_instance(
        data=ProcessCreationByKey(
            process_definition_key=ProcessDefinitionKey(stored_key),
        )
    )

    print(f"Process instance key: {result.process_instance_key}")
# endregion CreateProcessInstanceByKeyFromStorage


# region CreateProcessInstanceById
def create_process_instance_by_id_example() -> None:
    client = CamundaClient()

    result = client.create_process_instance(
        data=ProcessCreationById(
            process_definition_id=ProcessDefinitionId("order-process"),
        )
    )

    print(f"Process instance key: {result.process_instance_key}")
# endregion CreateProcessInstanceById


# region CancelProcessInstance
def cancel_process_instance_example() -> None:
    client = CamundaClient()

    # Create a process instance and get its key from the response
    created = client.create_process_instance(
        data=ProcessCreationById(process_definition_id=ProcessDefinitionId("order-process"))
    )

    # Cancel it using the key from the creation response
    client.cancel_process_instance(
        process_instance_key=created.process_instance_key,
    )
# endregion CancelProcessInstance


# region SearchProcessInstances
def search_process_instances_example() -> None:
    client = CamundaClient()

    result = client.search_process_instances(
        data=ProcessInstanceSearchQuery(
            filter_=ProcessInstanceSearchQueryFilter(
                process_definition_id="order-process",
            ),
            sort=[
                ProcessInstanceSearchQuerySortRequest(
                    field=ProcessInstanceSearchQuerySortRequestField.STARTDATE,
                    order=SortOrderEnum.DESC,
                )
            ],
            page=LimitBasedPagination(limit=10),
        )
    )

    for instance in result.items:
        print(f"{instance.process_instance_key}: {instance.state}")
    print(f"Total: {result.page.total_items}")
# endregion SearchProcessInstances
