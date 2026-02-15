from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ElementInstanceKey, ProcessDefinitionId, ProcessDefinitionKey, ProcessInstanceKey, TenantId
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.process_instance_state_enum import ProcessInstanceStateEnum
from ..types import UNSET, Unset, str_any_dict_factory
T = TypeVar("T", bound="SearchProcessInstancesItemsItem")
@_attrs_define
class SearchProcessInstancesItemsItem:
    process_definition_id: ProcessDefinitionId
    process_definition_name: str
    process_definition_version: int
    start_date: datetime.datetime
    state: ProcessInstanceStateEnum
    has_incident: bool
    tenant_id: TenantId
    process_instance_key: ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    process_definition_version_tag: str | Unset = UNSET
    end_date: datetime.datetime | Unset = UNSET
    parent_process_instance_key: ProcessInstanceKey | Unset = UNSET
    parent_element_instance_key: ElementInstanceKey | Unset = UNSET
    tags: list[str] | Unset = UNSET
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
