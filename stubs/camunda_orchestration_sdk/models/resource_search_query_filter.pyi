from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import TenantId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
from ..models.advanced_deployment_key_filter import AdvancedDeploymentKeyFilter
from ..models.advanced_integer_filter import AdvancedIntegerFilter
from ..models.advanced_resource_key_filter import AdvancedResourceKeyFilter
from ..models.advanced_string_filter import AdvancedStringFilter
T = TypeVar("T", bound="ResourceSearchQueryFilter")
@_attrs_define
class ResourceSearchQueryFilter:
    resource_key: AdvancedResourceKeyFilter | str | Unset = UNSET
    resource_name: AdvancedStringFilter | str | Unset = UNSET
    resource_id: AdvancedStringFilter | str | Unset = UNSET
    version: AdvancedIntegerFilter | int | Unset = UNSET
    version_tag: AdvancedStringFilter | str | Unset = UNSET
    deployment_key: AdvancedDeploymentKeyFilter | str | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
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
