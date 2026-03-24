from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import TenantId, lift_tenant_id

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.cluster_variable_scope_enum import ClusterVariableScopeEnum

T = TypeVar("T", bound="ClusterVariableSearchResult")


@_attrs_define
class ClusterVariableSearchResult:
    """Cluster variable search response item.

    Attributes:
        value (str): Value of this cluster variable. Can be truncated.
        is_truncated (bool): Whether the value is truncated or not.
        name (str): The name of the cluster variable. Unique within its scope (global or tenant-specific).
        scope (ClusterVariableScopeEnum): The scope of a cluster variable.
        tenant_id (None | str): Only provided if the cluster variable scope is TENANT. Null for global scope variables.
    """

    value: str
    is_truncated: bool
    name: str
    scope: ClusterVariableScopeEnum
    tenant_id: None | TenantId
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        is_truncated = self.is_truncated

        name = self.name

        scope = self.scope.value

        tenant_id: None | TenantId
        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "isTruncated": is_truncated,
                "name": name,
                "scope": scope,
                "tenantId": tenant_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        is_truncated = d.pop("isTruncated")

        name = d.pop("name")

        scope = ClusterVariableScopeEnum(d.pop("scope"))

        def _parse_tenant_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_tenant_id = _parse_tenant_id(d.pop("tenantId"))

        tenant_id = lift_tenant_id(_raw_tenant_id)

        cluster_variable_search_result = cls(
            value=value,
            is_truncated=is_truncated,
            name=name,
            scope=scope,
            tenant_id=tenant_id,
        )

        cluster_variable_search_result.additional_properties = d
        return cluster_variable_search_result

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
