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
from attrs import field as _attrs_field
from ..models.element_instance_wait_state_job_result_element_type import (
    ElementInstanceWaitStateJobResultElementType,
)
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.job_wait_state_details import JobWaitStateDetails

T = TypeVar("T", bound="ElementInstanceWaitStateJobResult")

@_attrs_define
class ElementInstanceWaitStateJobResult:
    wait_state_type: str
    process_instance_key: ProcessInstanceKey
    element_instance_key: ElementInstanceKey
    element_id: ElementId
    element_type: ElementInstanceWaitStateJobResultElementType
    tenant_id: TenantId
    details: JobWaitStateDetails
    root_process_instance_key: None | ProcessInstanceKey | Unset = UNSET
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
