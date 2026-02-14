from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import TenantId, lift_tenant_id

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.decision_evaluation_by_id_variables import (
        DecisionEvaluationByIdVariables,
    )


T = TypeVar("T", bound="MessagePublicationRequest")


@_attrs_define
class MessagePublicationRequest:
    """
    Attributes:
        name (str): The name of the message.
        correlation_key (str | Unset): The correlation key of the message. Default: ''. Example: customer-43421.
        time_to_live (int | Unset): Timespan (in ms) to buffer the message on the broker. Default: 0.
        message_id (str | Unset): The unique ID of the message. This is used to ensure only one message with the given
            ID
            will be published during the lifetime of the message (if `timeToLive` is set).
        variables (DecisionEvaluationByIdVariables | Unset): The message variables as JSON document.
        tenant_id (str | Unset): The tenant of the message sender. Example: customer-service.
    """

    name: str
    correlation_key: str | Unset = ""
    time_to_live: int | Unset = 0
    message_id: str | Unset = UNSET
    variables: DecisionEvaluationByIdVariables | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        correlation_key = self.correlation_key

        time_to_live = self.time_to_live

        message_id = self.message_id

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
            }
        )
        if correlation_key is not UNSET:
            field_dict["correlationKey"] = correlation_key
        if time_to_live is not UNSET:
            field_dict["timeToLive"] = time_to_live
        if message_id is not UNSET:
            field_dict["messageId"] = message_id
        if variables is not UNSET:
            field_dict["variables"] = variables
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decision_evaluation_by_id_variables import (
            DecisionEvaluationByIdVariables,
        )

        d = dict(src_dict)
        name = d.pop("name")

        correlation_key = d.pop("correlationKey", UNSET)

        time_to_live = d.pop("timeToLive", UNSET)

        message_id = d.pop("messageId", UNSET)

        _variables = d.pop("variables", UNSET)
        variables: DecisionEvaluationByIdVariables | Unset
        if isinstance(_variables, Unset):
            variables = UNSET
        else:
            variables = DecisionEvaluationByIdVariables.from_dict(_variables)

        tenant_id = (
            lift_tenant_id(_val)
            if (_val := d.pop("tenantId", UNSET)) is not UNSET
            else UNSET
        )

        message_publication_request = cls(
            name=name,
            correlation_key=correlation_key,
            time_to_live=time_to_live,
            message_id=message_id,
            variables=variables,
            tenant_id=tenant_id,
        )

        return message_publication_request
