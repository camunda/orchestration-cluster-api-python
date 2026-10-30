from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields
from camunda_orchestration_sdk.semantic_types import (
    BusinessId,
    ProcessDefinitionId,
    TenantId,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.process_instance_creation_instruction_base_variables import (
        ProcessInstanceCreationInstructionBaseVariables,
    )
    from ..models.process_instance_creation_instruction_base_variables_metadata import (
        ProcessInstanceCreationInstructionBaseVariablesMetadata,
    )
    from ..models.process_instance_creation_start_instruction import (
        ProcessInstanceCreationStartInstruction,
    )
    from ..models.process_instance_creation_terminate_instruction import (
        ProcessInstanceCreationTerminateInstruction,
    )


T = TypeVar("T", bound="ProcessCreationByVersionTag")


@_attrs_define
class ProcessCreationByVersionTag:
    """
    Attributes:
        process_definition_id (str): The BPMN process id of the process definition to start an instance of.
             Example: new-account-onboarding-workflow.
        process_definition_version_tag (str): The version tag of the process definition to start an instance of.
            If several deployed versions carry the same tag, the most recently deployed one is used.
        variables (ProcessInstanceCreationInstructionBaseVariables | Unset): JSON object that will instantiate the
            variables for the root variable scope
            of the process instance.
        variables_metadata (ProcessInstanceCreationInstructionBaseVariablesMetadata | Unset): Metadata of the variables,
            keyed by variable name. Use it to set how a variable is
            treated, for example to protect its value. A variable without an entry has no
            metadata.
        tenant_id (str | Unset): The tenant id of the process definition.
            If multi-tenancy is enabled, provide the tenant id of the process definition to start a
            process instance of. If multi-tenancy is disabled, don't provide this parameter.
             Example: customer-service.
        operation_reference (int | Unset): A reference key chosen by the user that will be part of all records resulting
            from this operation.
            Must be > 0 if provided.
        start_instructions (list[ProcessInstanceCreationStartInstruction] | Unset): List of start instructions. By
            default, the process instance will start at
            the start event. If provided, the process instance will apply start instructions
            after it has been created.
        runtime_instructions (list[ProcessInstanceCreationTerminateInstruction] | Unset): Runtime instructions (alpha).
            List of instructions that affect the runtime behavior of
            the process instance. Refer to specific instruction types for more details.

            This parameter is an alpha feature and may be subject to change
            in future releases.
        await_completion (bool | Unset): Wait for the process instance to complete. If the process instance does not
            complete
            within the request timeout limit, a 504 response status will be returned. The process
            instance will continue to run in the background regardless of the timeout. Disabled by
            default.
             Server default: False.
        fetch_variables (list[str] | Unset): List of variables by name to be included in the response when
            awaitCompletion is set to true.
            If empty, all visible variables in the root scope will be returned.
        request_timeout (int | Unset): Timeout (in ms) the request waits for the process to complete. By default or
            when set to 0, the generic request timeout configured in the cluster is applied.
             Server default: 0.
        tags (list[str] | Unset): List of tags. Tags need to start with a letter; then alphanumerics, `_`, `-`, `:`, or
            `.`; length ≤ 100. Example: ['high-touch', 'remediation'].
        business_id (str | Unset): An optional, user-defined string identifier that identifies the process instance
            within the scope of a process definition (scoped by tenant). If provided and uniqueness
            enforcement is enabled, the engine will reject creation if another root process instance
            with the same business id is already active for the same process definition.
            Note that any active child process instances with the same business id are not taken into account.
             Example: order-12345.
    """

    process_definition_id: ProcessDefinitionId
    process_definition_version_tag: str
    variables: ProcessInstanceCreationInstructionBaseVariables | Unset = UNSET
    variables_metadata: (
        ProcessInstanceCreationInstructionBaseVariablesMetadata | Unset
    ) = UNSET
    tenant_id: TenantId | Unset = UNSET
    operation_reference: int | Unset = UNSET
    start_instructions: list[ProcessInstanceCreationStartInstruction] | Unset = UNSET
    runtime_instructions: list[ProcessInstanceCreationTerminateInstruction] | Unset = (
        UNSET
    )
    await_completion: bool | Unset = UNSET
    fetch_variables: list[str] | Unset = UNSET
    request_timeout: int | Unset = UNSET
    tags: list[str] | Unset = UNSET
    business_id: BusinessId | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definition_id = self.process_definition_id

        process_definition_version_tag = self.process_definition_version_tag

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        variables_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables_metadata, Unset):
            variables_metadata = self.variables_metadata.to_dict()

        tenant_id = self.tenant_id

        operation_reference = self.operation_reference

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

        await_completion = self.await_completion

        fetch_variables: list[str] | Unset = UNSET
        if not isinstance(self.fetch_variables, Unset):
            fetch_variables = self.fetch_variables

        request_timeout = self.request_timeout

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        business_id = self.business_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinitionId": process_definition_id,
                "processDefinitionVersionTag": process_definition_version_tag,
            }
        )
        if variables is not UNSET:
            field_dict["variables"] = variables
        if variables_metadata is not UNSET:
            field_dict["variablesMetadata"] = variables_metadata
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if operation_reference is not UNSET:
            field_dict["operationReference"] = operation_reference
        if start_instructions is not UNSET:
            field_dict["startInstructions"] = start_instructions
        if runtime_instructions is not UNSET:
            field_dict["runtimeInstructions"] = runtime_instructions
        if await_completion is not UNSET:
            field_dict["awaitCompletion"] = await_completion
        if fetch_variables is not UNSET:
            field_dict["fetchVariables"] = fetch_variables
        if request_timeout is not UNSET:
            field_dict["requestTimeout"] = request_timeout
        if tags is not UNSET:
            field_dict["tags"] = tags
        if business_id is not UNSET:
            field_dict["businessId"] = business_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_instance_creation_instruction_base_variables import (
            ProcessInstanceCreationInstructionBaseVariables,
        )
        from ..models.process_instance_creation_instruction_base_variables_metadata import (
            ProcessInstanceCreationInstructionBaseVariablesMetadata,
        )
        from ..models.process_instance_creation_start_instruction import (
            ProcessInstanceCreationStartInstruction,
        )
        from ..models.process_instance_creation_terminate_instruction import (
            ProcessInstanceCreationTerminateInstruction,
        )

        d = RequiredFields(src_dict, cls.__name__)
        process_definition_id = ProcessDefinitionId(
            d.pop_required("processDefinitionId")
        )

        process_definition_version_tag = d.pop_required("processDefinitionVersionTag")

        _variables = d.pop("variables", UNSET)
        variables: ProcessInstanceCreationInstructionBaseVariables | Unset
        if isinstance(_variables, Unset):
            variables = UNSET
        else:
            variables = ProcessInstanceCreationInstructionBaseVariables.from_dict(
                _variables
            )

        _variables_metadata = d.pop("variablesMetadata", UNSET)
        variables_metadata: (
            ProcessInstanceCreationInstructionBaseVariablesMetadata | Unset
        )
        if isinstance(_variables_metadata, Unset):
            variables_metadata = UNSET
        else:
            variables_metadata = (
                ProcessInstanceCreationInstructionBaseVariablesMetadata.from_dict(
                    _variables_metadata
                )
            )

        tenant_id = (
            TenantId(_val) if (_val := d.pop("tenantId", UNSET)) is not UNSET else UNSET
        )

        operation_reference = d.pop("operationReference", UNSET)

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

        await_completion = d.pop("awaitCompletion", UNSET)

        fetch_variables = cast(list[str], d.pop("fetchVariables", UNSET))

        request_timeout = d.pop("requestTimeout", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        business_id = (
            BusinessId(_val)
            if (_val := d.pop("businessId", UNSET)) is not UNSET
            else UNSET
        )

        process_creation_by_version_tag = cls(
            process_definition_id=process_definition_id,
            process_definition_version_tag=process_definition_version_tag,
            variables=variables,
            variables_metadata=variables_metadata,
            tenant_id=tenant_id,
            operation_reference=operation_reference,
            start_instructions=start_instructions,
            runtime_instructions=runtime_instructions,
            await_completion=await_completion,
            fetch_variables=fetch_variables,
            request_timeout=request_timeout,
            tags=tags,
            business_id=business_id,
        )

        process_creation_by_version_tag.additional_properties = d
        return process_creation_by_version_tag

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
