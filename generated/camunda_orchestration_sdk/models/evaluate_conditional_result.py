from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ConditionalEvaluationKey,
    TenantId,
    lift_conditional_evaluation_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.process_instance_reference import ProcessInstanceReference


T = TypeVar("T", bound="EvaluateConditionalResult")


@_attrs_define
class EvaluateConditionalResult:
    """
    Attributes:
        conditional_evaluation_key (str): The unique key of the conditional evaluation operation. Example:
            2251799813687654.
        tenant_id (str): The tenant ID of the conditional evaluation operation. Example: customer-service.
        process_instances (list[ProcessInstanceReference]): List of process instances created. If no root-level
            conditional start events evaluated to true, the list will be empty.
    """

    conditional_evaluation_key: ConditionalEvaluationKey
    tenant_id: TenantId
    process_instances: list[ProcessInstanceReference]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        conditional_evaluation_key = self.conditional_evaluation_key

        tenant_id = self.tenant_id

        process_instances: list[dict[str, Any]] = []
        for process_instances_item_data in self.process_instances:
            process_instances_item = process_instances_item_data.to_dict()
            process_instances.append(process_instances_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "conditionalEvaluationKey": conditional_evaluation_key,
                "tenantId": tenant_id,
                "processInstances": process_instances,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_instance_reference import ProcessInstanceReference

        d = dict(src_dict)
        conditional_evaluation_key = lift_conditional_evaluation_key(
            d.pop("conditionalEvaluationKey")
        )

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        process_instances: list[ProcessInstanceReference] = []
        _process_instances = d.pop("processInstances")
        for process_instances_item_data in _process_instances:
            process_instances_item = ProcessInstanceReference.from_dict(
                process_instances_item_data
            )

            process_instances.append(process_instances_item)

        evaluate_conditional_result = cls(
            conditional_evaluation_key=conditional_evaluation_key,
            tenant_id=tenant_id,
            process_instances=process_instances,
        )

        evaluate_conditional_result.additional_properties = d
        return evaluate_conditional_result

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
