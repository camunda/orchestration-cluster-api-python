from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import ClusterVariableName
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..models.create_cluster_variable_request_kind import (
    CreateClusterVariableRequestKind,
)
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.create_cluster_variable_request_metadata import (
    CreateClusterVariableRequestMetadata,
)
from ..models.create_cluster_variable_request_value import (
    CreateClusterVariableRequestValue,
)

T = TypeVar("T", bound="CreateClusterVariableRequest")

@_attrs_define
class CreateClusterVariableRequest:
    name: ClusterVariableName
    value: CreateClusterVariableRequestValue
    metadata: CreateClusterVariableRequestMetadata | Unset = UNSET
    kind: CreateClusterVariableRequestKind | Unset = UNSET
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
