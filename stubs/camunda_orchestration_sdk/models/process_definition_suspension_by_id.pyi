from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ProcessDefinitionId, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessDefinitionSuspensionByID")

@_attrs_define
class ProcessDefinitionSuspensionByID:
    process_definition_id: ProcessDefinitionId
    process_definition_version: int | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    include_process_instances: bool | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
