from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields
from camunda_orchestration_sdk.semantic_types import ProcessDefinitionKey

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessDefinitionSuspensionByKey")


@_attrs_define
class ProcessDefinitionSuspensionByKey:
    """
    Attributes:
        process_definition_key (str): The key of the process definition version to suspend. Example: 2251799813686749.
        include_process_instances (bool | Unset): Whether to also suspend the process instances of the affected
            process definition versions. The instances are changed by a batch operation.
             Server default: False.
    """

    process_definition_key: ProcessDefinitionKey
    include_process_instances: bool | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        process_definition_key = self.process_definition_key

        include_process_instances = self.include_process_instances

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "processDefinitionKey": process_definition_key,
            }
        )
        if include_process_instances is not UNSET:
            field_dict["includeProcessInstances"] = include_process_instances

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        process_definition_key = ProcessDefinitionKey(
            d.pop_required("processDefinitionKey")
        )

        include_process_instances = d.pop("includeProcessInstances", UNSET)

        process_definition_suspension_by_key = cls(
            process_definition_key=process_definition_key,
            include_process_instances=include_process_instances,
        )

        return process_definition_suspension_by_key
