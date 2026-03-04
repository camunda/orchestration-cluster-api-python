from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    MessageKey,
    ProcessInstanceKey,
    TenantId,
    lift_message_key,
    lift_process_instance_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="MessageCorrelationResult")


@_attrs_define
class MessageCorrelationResult:
    """The message key of the correlated message, as well as the first process instance key it
    correlated with.

        Attributes:
            tenant_id (str): The tenant ID of the correlated message Example: customer-service.
            message_key (str): The key of the correlated message. Example: 2251799813683467.
            process_instance_key (str): The key of the first process instance the message correlated with Example:
                2251799813690746.
    """

    tenant_id: TenantId
    message_key: MessageKey
    process_instance_key: ProcessInstanceKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        tenant_id = self.tenant_id

        message_key = self.message_key

        process_instance_key = self.process_instance_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tenantId": tenant_id,
                "messageKey": message_key,
                "processInstanceKey": process_instance_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tenant_id = lift_tenant_id(d.pop("tenantId"))

        message_key = lift_message_key(d.pop("messageKey"))

        process_instance_key = lift_process_instance_key(d.pop("processInstanceKey"))

        message_correlation_result = cls(
            tenant_id=tenant_id,
            message_key=message_key,
            process_instance_key=process_instance_key,
        )

        message_correlation_result.additional_properties = d
        return message_correlation_result

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
