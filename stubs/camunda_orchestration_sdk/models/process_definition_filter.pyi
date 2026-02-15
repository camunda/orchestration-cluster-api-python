from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ProcessDefinitionKey, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_string_filter import AdvancedStringFilter
T = TypeVar("T", bound="ProcessDefinitionFilter")
@_attrs_define
class ProcessDefinitionFilter:
    name: AdvancedStringFilter | str | Unset = UNSET
    is_latest_version: bool | Unset = UNSET
    resource_name: str | Unset = UNSET
    version: int | Unset = UNSET
    version_tag: str | Unset = UNSET
    process_definition_id: AdvancedStringFilter | str | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    has_start_form: bool | Unset = UNSET
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
