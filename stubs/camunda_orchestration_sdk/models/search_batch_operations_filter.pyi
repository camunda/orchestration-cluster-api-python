from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.batch_operation_state_exact_match import BatchOperationStateExactMatch
from ..models.batch_operation_type_exact_match import BatchOperationTypeExactMatch
from ..models.search_batch_operations_filter_actor_type import SearchBatchOperationsFilterActorType
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_batch_operation_state_filter import AdvancedBatchOperationStateFilter
from ..models.advanced_string_filter import AdvancedStringFilter
from ..models.basic_string_filter import BasicStringFilter
from ..models.operation_type_advanced_filter import OperationTypeAdvancedFilter
T = TypeVar("T", bound="SearchBatchOperationsFilter")
@_attrs_define
class SearchBatchOperationsFilter:
    batch_operation_key: BasicStringFilter | str | Unset = UNSET
    operation_type: (
            BatchOperationTypeExactMatch | OperationTypeAdvancedFilter | Unset
        ) = UNSET
    state: AdvancedBatchOperationStateFilter | BatchOperationStateExactMatch | Unset = (
            UNSET
        )
    actor_type: SearchBatchOperationsFilterActorType | Unset = UNSET
    actor_id: AdvancedStringFilter | str | Unset = UNSET
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
