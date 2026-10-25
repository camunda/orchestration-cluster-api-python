from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="CreateDeploymentData")

@_attrs_define
class CreateDeploymentData:
    resources: list[File]
    tenant_id: TenantId | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    def to_multipart(self) -> types.RequestFiles: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
