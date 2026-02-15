from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import BatchOperationKey, ProcessInstanceKey
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.batch_operation_item_response_state import BatchOperationItemResponseState
from ..models.batch_operation_type_enum import BatchOperationTypeEnum
from ..types import UNSET, Unset, str_any_dict_factory
T = TypeVar("T", bound="BatchOperationItemResponse")
@_attrs_define
class BatchOperationItemResponse:
    operation_type: BatchOperationTypeEnum | Unset = UNSET
    batch_operation_key: BatchOperationKey | Unset = UNSET
    item_key: str | Unset = UNSET
    process_instance_key: ProcessInstanceKey | Unset = UNSET
    state: BatchOperationItemResponseState | Unset = UNSET
    processed_date: datetime.datetime | Unset = UNSET
    error_message: str | Unset = UNSET
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
