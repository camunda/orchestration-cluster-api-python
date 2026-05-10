from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset
from ..models.signal_broadcast_request_variables import SignalBroadcastRequestVariables

T = TypeVar("T", bound="SignalBroadcastRequest")

@_attrs_define
class SignalBroadcastRequest:
    signal_name: str
    variables: SignalBroadcastRequestVariables | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
