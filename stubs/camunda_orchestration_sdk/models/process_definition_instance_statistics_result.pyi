from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ProcessDefinitionId, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
T = TypeVar("T", bound="ProcessDefinitionInstanceStatisticsResult")
@_attrs_define
class ProcessDefinitionInstanceStatisticsResult:
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    latest_process_definition_name: None | str | Unset = UNSET
    has_multiple_versions: bool | Unset = UNSET
    active_instances_without_incident_count: int | Unset = UNSET
    active_instances_with_incident_count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
