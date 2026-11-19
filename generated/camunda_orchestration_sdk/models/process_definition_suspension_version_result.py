from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields
from camunda_orchestration_sdk.semantic_types import ProcessDefinitionKey

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.process_definition_suspension_version_result_outcome import (
    ProcessDefinitionSuspensionVersionResultOutcome,
)

T = TypeVar("T", bound="ProcessDefinitionSuspensionVersionResult")


@_attrs_define
class ProcessDefinitionSuspensionVersionResult:
    """
    Attributes:
        process_definition_key (str): The key of the process definition version. Example: 2251799813686749.
        process_definition_version (int): The version of the process definition.
        outcome (ProcessDefinitionSuspensionVersionResultOutcome): `SUSPENDED` if the version was active and is now
            suspended. The suspension applies to
            all partitions shortly after the response.
            `ALREADY_SUSPENDED` if the version was already suspended, so its state is unchanged.
            With `includeProcessInstances`, its process instances are still suspended by the
            batch operation.
            `DRAINING` if it is being deleted and is left unchanged. This only occurs when the
            request selects by ID without a version; selecting a single draining version is rejected
            with 409.
    """

    process_definition_key: ProcessDefinitionKey
    process_definition_version: int
    outcome: ProcessDefinitionSuspensionVersionResultOutcome
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definition_key = self.process_definition_key

        process_definition_version = self.process_definition_version

        outcome = self.outcome.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinitionKey": process_definition_key,
                "processDefinitionVersion": process_definition_version,
                "outcome": outcome,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        process_definition_key = ProcessDefinitionKey(
            d.pop_required("processDefinitionKey")
        )

        process_definition_version = d.pop_required("processDefinitionVersion")

        outcome = ProcessDefinitionSuspensionVersionResultOutcome(
            d.pop_required("outcome")
        )

        process_definition_suspension_version_result = cls(
            process_definition_key=process_definition_key,
            process_definition_version=process_definition_version,
            outcome=outcome,
        )

        process_definition_suspension_version_result.additional_properties = d
        return process_definition_suspension_version_result

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
