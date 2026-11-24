from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ProbeId, ProbeKey, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.activated_probe_result_input import ActivatedProbeResultInput

T = TypeVar("T", bound="ActivatedProbeResult")

@_attrs_define
class ActivatedProbeResult:
    probe_key: ProbeKey
    probe_id: ProbeId
    worker: str
    deadline: int
    tenant_id: TenantId
    physical_tenant_id: str
    input_: ActivatedProbeResultInput
    secret_pointers: list[str]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
