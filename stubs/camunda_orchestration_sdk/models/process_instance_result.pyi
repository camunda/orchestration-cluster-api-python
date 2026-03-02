from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import BusinessId, ElementInstanceKey, ProcessDefinitionId, ProcessDefinitionKey, ProcessInstanceKey, TenantId
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.process_instance_state_enum import ProcessInstanceStateEnum
T = TypeVar("T", bound="ProcessInstanceResult")
@_attrs_define
class ProcessInstanceResult:
    process_definition_id: ProcessDefinitionId
    process_definition_name: None | str
    process_definition_version: int
    process_definition_version_tag: None | str
    start_date: datetime.datetime
    end_date: datetime.datetime | None
    state: ProcessInstanceStateEnum
    has_incident: bool
    tenant_id: TenantId
    process_instance_key: ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    parent_process_instance_key: None | ProcessInstanceKey
    parent_element_instance_key: None | ElementInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    tags: list[str]
    business_id: None | BusinessId
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
