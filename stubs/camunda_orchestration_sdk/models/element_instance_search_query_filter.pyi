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
from ..models.element_instance_search_query_filter_type import (
    ElementInstanceSearchQueryFilterType,
)
from ..models.element_instance_state_exact_match import ElementInstanceStateExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
from ..models.advanced_element_instance_state_filter import (
    AdvancedElementInstanceStateFilter,
)

T = TypeVar("T", bound="ElementInstanceSearchQueryFilter")

@_attrs_define
class ElementInstanceSearchQueryFilter:
    process_definition_id: ProcessDefinitionId | Unset = UNSET
    state: (
        AdvancedElementInstanceStateFilter | ElementInstanceStateExactMatch | Unset
    ) = UNSET
    type_: ElementInstanceSearchQueryFilterType | Unset = UNSET
    element_id: ElementId | Unset = UNSET
    element_name: str | Unset = UNSET
    has_incident: bool | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    element_instance_key: ElementInstanceKey | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    process_definition_key: ProcessDefinitionKey | Unset = UNSET
    incident_key: IncidentKey | Unset = UNSET
    start_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    end_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    element_instance_scope_key: str | Unset = UNSET
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
