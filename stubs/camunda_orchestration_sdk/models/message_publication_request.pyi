from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.message_publication_request_variables import MessagePublicationRequestVariables
T = TypeVar("T", bound="MessagePublicationRequest")
@_attrs_define
class MessagePublicationRequest:
    name: str
    correlation_key: str | Unset = UNSET
    time_to_live: int | Unset = UNSET
    message_id: str | Unset = UNSET
    variables: MessagePublicationRequestVariables | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
