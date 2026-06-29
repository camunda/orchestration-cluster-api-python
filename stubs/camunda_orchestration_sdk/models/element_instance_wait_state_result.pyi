from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    ProcessInstanceKey,
    TenantId,
)
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.element_instance_wait_state_result_element_type import (
    ElementInstanceWaitStateResultElementType,
)
from ..models.condition_wait_state_details import ConditionWaitStateDetails
from ..models.job_wait_state_details import JobWaitStateDetails
from ..models.message_wait_state_details import MessageWaitStateDetails
from ..models.signal_wait_state_details import SignalWaitStateDetails
from ..models.timer_wait_state_details import TimerWaitStateDetails
from ..models.user_task_wait_state_details import UserTaskWaitStateDetails

T = TypeVar("T", bound="ElementInstanceWaitStateResult")

@_attrs_define
class ElementInstanceWaitStateResult:
    root_process_instance_key: None | ProcessInstanceKey
    process_instance_key: ProcessInstanceKey
    element_instance_key: ElementInstanceKey
    element_id: ElementId
    element_type: ElementInstanceWaitStateResultElementType
    tenant_id: TenantId
    bpmn_process_id: str
    details: (
        ConditionWaitStateDetails
        | JobWaitStateDetails
        | MessageWaitStateDetails
        | SignalWaitStateDetails
        | TimerWaitStateDetails
        | UserTaskWaitStateDetails
    )
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
