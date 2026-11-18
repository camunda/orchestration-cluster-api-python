from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields
from camunda_orchestration_sdk.semantic_types import BatchOperationKey

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.process_definition_resumption_version_result import (
        ProcessDefinitionResumptionVersionResult,
    )


T = TypeVar("T", bound="ProcessDefinitionResumptionResult")


@_attrs_define
class ProcessDefinitionResumptionResult:
    """
    Attributes:
        process_definitions (list[ProcessDefinitionResumptionVersionResult]): The affected process definition versions.
        batch_operation_key (None | str): The key of the batch operation that resumes the suspended process instances.
            Null when `includeProcessInstances` is not set.
             Example: 2251799813684321.
    """

    process_definitions: list[ProcessDefinitionResumptionVersionResult]
    batch_operation_key: None | BatchOperationKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        process_definitions: list[dict[str, Any]] = []
        for process_definitions_item_data in self.process_definitions:
            process_definitions_item = process_definitions_item_data.to_dict()
            process_definitions.append(process_definitions_item)

        batch_operation_key: None | BatchOperationKey
        batch_operation_key = self.batch_operation_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "processDefinitions": process_definitions,
                "batchOperationKey": batch_operation_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_definition_resumption_version_result import (
            ProcessDefinitionResumptionVersionResult,  # noqa: PLC0415
        )

        d = RequiredFields(src_dict, cls.__name__)
        process_definitions: list[ProcessDefinitionResumptionVersionResult] = []
        _process_definitions = d.pop_required("processDefinitions")
        for process_definitions_item_data in _process_definitions:
            process_definitions_item = (
                ProcessDefinitionResumptionVersionResult.from_dict(
                    process_definitions_item_data
                )
            )

            process_definitions.append(process_definitions_item)

        def _parse_batch_operation_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_batch_operation_key = _parse_batch_operation_key(
            d.pop_required("batchOperationKey")
        )

        batch_operation_key = (
            BatchOperationKey(_raw_batch_operation_key)
            if isinstance(_raw_batch_operation_key, str)
            else _raw_batch_operation_key
        )

        process_definition_resumption_result = cls(
            process_definitions=process_definitions,
            batch_operation_key=batch_operation_key,
        )

        process_definition_resumption_result.additional_properties = d
        return process_definition_resumption_result

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
