from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    IncidentKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
)
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.element_instance_result_state import ElementInstanceResultState
from ..models.element_instance_result_type import ElementInstanceResultType
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="ElementInstanceResult")

@_attrs_define
class ElementInstanceResult:
    process_definition_id: ProcessDefinitionId
    start_date: datetime.datetime
    element_id: ElementId
    element_name: str
    type_: ElementInstanceResultType
    state: ElementInstanceResultState
    has_incident: bool
    tenant_id: TenantId
    element_instance_key: ElementInstanceKey
    process_instance_key: ProcessInstanceKey
    process_definition_key: ProcessDefinitionKey
    end_date: datetime.datetime | Unset = UNSET
    incident_key: IncidentKey | Unset = UNSET
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
