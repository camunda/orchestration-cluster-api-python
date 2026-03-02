from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import TenantId, lift_tenant_id

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.cluster_variable_scope_enum import ClusterVariableScopeEnum
from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="ClusterVariableResult")


@_attrs_define
class ClusterVariableResult:
    """
    Attributes:
        name (str): The name of the cluster variable. Unique within its scope (global or tenant-specific).
        scope (ClusterVariableScopeEnum): The scope of a cluster variable.
        value (str | Unset): Full value of this cluster variable.
        tenant_id (None | str | Unset): Only provided if the cluster variable scope is TENANT. Null for global scope
            variables.
    """

    name: str
    scope: ClusterVariableScopeEnum
    value: str | Unset = UNSET
    tenant_id: None | TenantId | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        scope = self.scope.value

        value = self.value

        tenant_id: None | TenantId | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        else:
            tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "scope": scope,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        scope = ClusterVariableScopeEnum(d.pop("scope"))

        value = d.pop("value", UNSET)

        def _parse_tenant_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        _raw_tenant_id = _parse_tenant_id(d.pop("tenantId", UNSET))

        tenant_id = (
            lift_tenant_id(_raw_tenant_id)
            if isinstance(_raw_tenant_id, str)
            else _raw_tenant_id
        )

        cluster_variable_result = cls(
            name=name,
            scope=scope,
            value=value,
            tenant_id=tenant_id,
        )

        cluster_variable_result.additional_properties = d
        return cluster_variable_result

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
