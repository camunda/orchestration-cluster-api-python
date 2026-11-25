from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..models.probe_activation_request_tenant_filter import (
    ProbeActivationRequestTenantFilter,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProbeActivationRequest")

@_attrs_define
class ProbeActivationRequest:
    probe_ids: list[str]
    max_probes_to_activate: int
    worker: str | Unset = UNSET
    request_timeout: int | Unset = UNSET
    tenant_ids: list[str] | Unset = UNSET
    tenant_filter: ProbeActivationRequestTenantFilter | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
