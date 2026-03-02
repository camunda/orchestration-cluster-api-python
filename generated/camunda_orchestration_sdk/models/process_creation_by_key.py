from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    BusinessId,
    ProcessDefinitionKey,
    TenantId,
    lift_business_id,
    lift_process_definition_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.process_instance_creation_instruction_by_key_variables import (
        ProcessInstanceCreationInstructionByKeyVariables,
    )
    from ..models.process_instance_creation_start_instruction import (
        ProcessInstanceCreationStartInstruction,
    )
    from ..models.process_instance_creation_terminate_instruction import (
        ProcessInstanceCreationTerminateInstruction,
    )


T = TypeVar("T", bound="ProcessCreationByKey")


@_attrs_define
class ProcessCreationByKey:
    """
    Attributes:
        process_definition_key (str): The unique key identifying the process definition, for example, returned for a
            process in the
            deploy resources endpoint.
             Example: 2251799813686749.
        process_definition_version (int | Unset): As the version is already identified by the `processDefinitionKey`,
            the value of this field is ignored.
            It's here for backwards-compatibility only as previous releases accepted it in request bodies.
             Default: -1.
        variables (ProcessInstanceCreationInstructionByKeyVariables | Unset): Set of variables as JSON object to
            instantiate in the root variable scope of the process
            instance. Can include nested complex objects.
        start_instructions (list[ProcessInstanceCreationStartInstruction] | Unset): List of start instructions. By
            default, the process instance will start at
            the start event. If provided, the process instance will apply start instructions
            after it has been created.
        runtime_instructions (list[ProcessInstanceCreationTerminateInstruction] | Unset): Runtime instructions (alpha).
            List of instructions that affect the runtime behavior of
            the process instance. Refer to specific instruction types for more details.

            This parameter is an alpha feature and may be subject to change
            in future releases.
        tenant_id (str | Unset): The tenant id of the process definition.
            If multi-tenancy is enabled, provide the tenant id of the process definition to start a
            process instance of. If multi-tenancy is disabled, don't provide this parameter.
             Example: customer-service.
        operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
            from this operation.
            Must be > 0 if provided.
        await_completion (bool | Unset): Wait for the process instance to complete. If the process instance does not
            complete
            within the request timeout limit, a 504 response status will be returned. The process
            instance will continue to run in the background regardless of the timeout. Disabled by
            default.
             Default: False.
        request_timeout (int | Unset): Timeout (in ms) the request waits for the process to complete. By default or
            when set to 0, the generic request timeout configured in the cluster is applied.
             Default: 0.
        fetch_variables (list[str] | Unset): List of variables by name to be included in the response when
            awaitCompletion is set to true.
            If empty, all visible variables in the root scope will be returned.
        tags (list[str] | Unset): List of tags. Tags need to start with a letter; then alphanumerics, `_`, `-`, `:`, or
            `.`; length ≤ 100. Example: ['high-touch', 'remediation'].
        business_id (str | Unset): An optional, user-defined string identifier that identifies the process instance
            within the scope of a process definition (scoped by tenant). If provided and uniqueness
            enforcement is enabled, the engine will reject creation if another root process instance
            with the same business id is already active for the same process definition.
            Note that any active child process instances with the same business id are not taken into account.
             Example: order-12345.
    """

    process_definition_key: ProcessDefinitionKey
    process_definition_version: int | Unset = -1
    variables: ProcessInstanceCreationInstructionByKeyVariables | Unset = UNSET
    start_instructions: list[ProcessInstanceCreationStartInstruction] | Unset = UNSET
    runtime_instructions: list[ProcessInstanceCreationTerminateInstruction] | Unset = (
        UNSET
    )
    tenant_id: TenantId | Unset = UNSET
    operation_reference: int | Unset = UNSET
    await_completion: bool | Unset = False
    request_timeout: int | Unset = 0
    fetch_variables: list[str] | Unset = UNSET
    tags: list[str] | Unset = UNSET
    business_id: BusinessId | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        process_definition_key = self.process_definition_key

        process_definition_version = self.process_definition_version

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        start_instructions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.start_instructions, Unset):
            start_instructions = []
            for start_instructions_item_data in self.start_instructions:
                start_instructions_item = start_instructions_item_data.to_dict()
                start_instructions.append(start_instructions_item)

        runtime_instructions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.runtime_instructions, Unset):
            runtime_instructions = []
            for runtime_instructions_item_data in self.runtime_instructions:
                runtime_instructions_item = runtime_instructions_item_data.to_dict()
                runtime_instructions.append(runtime_instructions_item)

        tenant_id = self.tenant_id

        operation_reference = self.operation_reference

        await_completion = self.await_completion

        request_timeout = self.request_timeout

        fetch_variables: list[str] | Unset = UNSET
        if not isinstance(self.fetch_variables, Unset):
            fetch_variables = self.fetch_variables

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        business_id = self.business_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "processDefinitionKey": process_definition_key,
            }
        )
        if process_definition_version is not UNSET:
            field_dict["processDefinitionVersion"] = process_definition_version
        if variables is not UNSET:
            field_dict["variables"] = variables
        if start_instructions is not UNSET:
            field_dict["startInstructions"] = start_instructions
        if runtime_instructions is not UNSET:
            field_dict["runtimeInstructions"] = runtime_instructions
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference
        if await_completion is not UNSET:
            field_dict["awaitCompletion"] = await_completion
        if request_timeout is not UNSET:
            field_dict["requestTimeout"] = request_timeout
        if fetch_variables is not UNSET:
            field_dict["fetchVariables"] = fetch_variables
        if tags is not UNSET:
            field_dict["tags"] = tags
        if business_id is not UNSET:
            field_dict["businessId"] = business_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_instance_creation_instruction_by_key_variables import (
            ProcessInstanceCreationInstructionByKeyVariables,
        )
        from ..models.process_instance_creation_start_instruction import (
            ProcessInstanceCreationStartInstruction,
        )
        from ..models.process_instance_creation_terminate_instruction import (
            ProcessInstanceCreationTerminateInstruction,
        )

        d = dict(src_dict)
        process_definition_key = lift_process_definition_key(
            d.pop("processDefinitionKey")
        )

        process_definition_version = d.pop("processDefinitionVersion", UNSET)

        _variables = d.pop("variables", UNSET)
        variables: ProcessInstanceCreationInstructionByKeyVariables | Unset
        if isinstance(_variables, Unset):
            variables = UNSET
        else:
            variables = ProcessInstanceCreationInstructionByKeyVariables.from_dict(
                _variables
            )

        _start_instructions = d.pop("startInstructions", UNSET)
        start_instructions: list[ProcessInstanceCreationStartInstruction] | Unset = (
            UNSET
        )
        if _start_instructions is not UNSET:
            start_instructions = []
            for start_instructions_item_data in _start_instructions:
                start_instructions_item = (
                    ProcessInstanceCreationStartInstruction.from_dict(
                        start_instructions_item_data
                    )
                )

                start_instructions.append(start_instructions_item)

        _runtime_instructions = d.pop("runtimeInstructions", UNSET)
        runtime_instructions: (
            list[ProcessInstanceCreationTerminateInstruction] | Unset
        ) = UNSET
        if _runtime_instructions is not UNSET:
            runtime_instructions = []
            for runtime_instructions_item_data in _runtime_instructions:
                runtime_instructions_item = (
                    ProcessInstanceCreationTerminateInstruction.from_dict(
                        runtime_instructions_item_data
                    )
                )

                runtime_instructions.append(runtime_instructions_item)

        tenant_id = (
            lift_tenant_id(_val)
            if (_val := d.pop("tenantId", UNSET)) is not UNSET
            else UNSET
        )

        operation_reference = d.pop("operationReference", UNSET)

        await_completion = d.pop("awaitCompletion", UNSET)

        request_timeout = d.pop("requestTimeout", UNSET)

        fetch_variables = cast(list[str], d.pop("fetchVariables", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        business_id = (
            lift_business_id(_val)
            if (_val := d.pop("businessId", UNSET)) is not UNSET
            else UNSET
        )

        process_creation_by_key = cls(
            process_definition_key=process_definition_key,
            process_definition_version=process_definition_version,
            variables=variables,
            start_instructions=start_instructions,
            runtime_instructions=runtime_instructions,
            tenant_id=tenant_id,
            operation_reference=operation_reference,
            await_completion=await_completion,
            request_timeout=request_timeout,
            fetch_variables=fetch_variables,
            tags=tags,
            business_id=business_id,
        )

        return process_creation_by_key
