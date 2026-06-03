from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import DecisionRequirementsKey, TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
T = TypeVar("T", bound="DecisionRequirementsResult")
@_attrs_define
class DecisionRequirementsResult:
    decision_requirements_id: str
    decision_requirements_key: DecisionRequirementsKey
    decision_requirements_name: str
    resource_name: str
    tenant_id: TenantId
    version: int
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
