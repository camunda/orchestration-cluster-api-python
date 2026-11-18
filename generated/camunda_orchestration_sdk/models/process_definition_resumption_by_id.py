from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields
from camunda_orchestration_sdk.semantic_types import ProcessDefinitionId, TenantId

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessDefinitionResumptionByID")


@_attrs_define
class ProcessDefinitionResumptionByID:
    """
    Attributes:
        process_definition_id (str): The BPMN process ID of the process definition. Example: new-account-onboarding-
            workflow.
        process_definition_version (int | Unset): The version of the process definition. Must be 1 or greater; `-1` is
            not accepted.
            If omitted, all versions are affected.
        tenant_id (str | Unset): The tenant of the process definition. Required when multi-tenancy is enabled;
            if multi-tenancy is disabled, it can be omitted and the default tenant is used.
             Example: customer-service.
        include_process_instances (bool | Unset): Whether to also resume the process instances of the affected
            process definition versions. The instances are changed by a batch operation.
             Server default: False.
    """

    process_definition_id: ProcessDefinitionId
    process_definition_version: int | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    include_process_instances: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        process_definition_id = self.process_definition_id

        process_definition_version = self.process_definition_version

        tenant_id = self.tenant_id

        include_process_instances = self.include_process_instances

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "processDefinitionId": process_definition_id,
            }
        )
        if process_definition_version is not UNSET:
            field_dict["processDefinitionVersion"] = process_definition_version
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if include_process_instances is not UNSET:
            field_dict["includeProcessInstances"] = include_process_instances

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        process_definition_id = ProcessDefinitionId(
            d.pop_required("processDefinitionId")
        )

        process_definition_version = d.pop("processDefinitionVersion", UNSET)

        tenant_id = (
            TenantId(_val) if (_val := d.pop("tenantId", UNSET)) is not UNSET else UNSET
        )

        include_process_instances = d.pop("includeProcessInstances", UNSET)

        process_definition_resumption_by_id = cls(
            process_definition_id=process_definition_id,
            process_definition_version=process_definition_version,
            tenant_id=tenant_id,
            include_process_instances=include_process_instances,
        )

        return process_definition_resumption_by_id
