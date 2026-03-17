from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import BatchOperationKey, ProcessInstanceKey
import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.batch_operation_item_response_state import BatchOperationItemResponseState
from ..models.batch_operation_type_enum import BatchOperationTypeEnum
T = TypeVar("T", bound="BatchOperationItemResponse")
@_attrs_define
class BatchOperationItemResponse:
    operation_type: BatchOperationTypeEnum
    batch_operation_key: BatchOperationKey
    item_key: str
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    state: BatchOperationItemResponseState
    processed_date: datetime.datetime | None
    error_message: None | str
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
