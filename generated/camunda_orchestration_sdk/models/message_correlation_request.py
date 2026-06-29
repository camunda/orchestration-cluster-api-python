from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import BusinessId, TenantId

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.message_correlation_request_variables import (
        MessageCorrelationRequestVariables,
    )


T = TypeVar("T", bound="MessageCorrelationRequest")


@_attrs_define
class MessageCorrelationRequest:
    """
    Attributes:
        name (str): The message name as defined in the BPMN process
        correlation_key (str | Unset): The correlation key of the message. Server default: . Example: customer-43421.
        variables (MessageCorrelationRequestVariables | Unset): The message variables as JSON document
        tenant_id (str | Unset): the tenant for which the message is published Example: customer-service.
        business_id (str | Unset): An optional business id used to enforce uniqueness of the process instance that a
            message start event would create. If provided and uniqueness enforcement is enabled,
            the engine rejects starting a new process instance when another root process instance
            with the same business id is already active for the same process definition. It has no
            effect when the message correlates to a catch, boundary, or intermediate event.
             Example: order-12345.
    """

    name: str
    correlation_key: str | Unset = UNSET
    variables: MessageCorrelationRequestVariables | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    business_id: BusinessId | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        correlation_key = self.correlation_key

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        tenant_id = self.tenant_id

        business_id = self.business_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
            }
        )
        if correlation_key is not UNSET:
            field_dict["correlationKey"] = correlation_key
        if variables is not UNSET:
            field_dict["variables"] = variables
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if business_id is not UNSET:
            field_dict["businessId"] = business_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message_correlation_request_variables import (
            MessageCorrelationRequestVariables,
        )

        d = dict(src_dict)
        name = d.pop("name")

        correlation_key = d.pop("correlationKey", UNSET)

        _variables = d.pop("variables", UNSET)
        variables: MessageCorrelationRequestVariables | Unset
        if isinstance(_variables, Unset):
            variables = UNSET
        else:
            variables = MessageCorrelationRequestVariables.from_dict(_variables)

        tenant_id = (
            TenantId(_val) if (_val := d.pop("tenantId", UNSET)) is not UNSET else UNSET
        )

        business_id = (
            BusinessId(_val)
            if (_val := d.pop("businessId", UNSET)) is not UNSET
            else UNSET
        )

        message_correlation_request = cls(
            name=name,
            correlation_key=correlation_key,
            variables=variables,
            tenant_id=tenant_id,
            business_id=business_id,
        )

        return message_correlation_request
