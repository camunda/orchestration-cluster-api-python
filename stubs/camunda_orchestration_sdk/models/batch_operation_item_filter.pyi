from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.batch_operation_item_state_exact_match import BatchOperationItemStateExactMatch
from ..models.batch_operation_type_exact_match import BatchOperationTypeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_batch_operation_item_state_filter import AdvancedBatchOperationItemStateFilter
from ..models.advanced_batch_operation_type_filter import AdvancedBatchOperationTypeFilter
from ..models.advanced_process_instance_key_filter import AdvancedProcessInstanceKeyFilter
from ..models.basic_string_filter import BasicStringFilter
T = TypeVar("T", bound="BatchOperationItemFilter")
@_attrs_define
class BatchOperationItemFilter:
    batch_operation_key: BasicStringFilter | str | Unset = UNSET
    item_key: BasicStringFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    state: (
            AdvancedBatchOperationItemStateFilter
            | BatchOperationItemStateExactMatch
            | Unset
        ) = UNSET
    operation_type: (
            AdvancedBatchOperationTypeFilter | BatchOperationTypeExactMatch | Unset
        ) = UNSET
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
