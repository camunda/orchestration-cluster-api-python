from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ClusterVariableName

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.cluster_variable_kind_enum import ClusterVariableKindEnum
from ..models.cluster_variable_scope_enum import ClusterVariableScopeEnum

if TYPE_CHECKING:
    from ..models.cluster_variable_result_metadata import ClusterVariableResultMetadata


T = TypeVar("T", bound="ClusterVariableResult")


@_attrs_define
class ClusterVariableResult:
    """
    Attributes:
        value (str): Full value of this cluster variable.
        name (str): The name of the cluster variable. Unique within its scope (global or tenant-specific). Example:
            feature-flag-checkout.
        scope (ClusterVariableScopeEnum): The scope of a cluster variable.
        tenant_id (None | str): Only provided if the cluster variable scope is TENANT. Null for global scope variables.
        metadata (ClusterVariableResultMetadata): A generic key-value metadata bag attached to the cluster variable.
            Values are strings or numbers.
        kind (ClusterVariableKindEnum): The kind of a cluster variable. JSON is the default. SECRET_REFERENCE allows the
            value to contain camunda.secrets.X references that are resolved at job activation time.
    """

    value: str
    name: ClusterVariableName
    scope: ClusterVariableScopeEnum
    tenant_id: None | str
    metadata: ClusterVariableResultMetadata
    kind: ClusterVariableKindEnum
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        name = self.name

        scope = self.scope.value

        tenant_id: None | str
        tenant_id = self.tenant_id

        metadata = self.metadata.to_dict()

        kind = self.kind.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "name": name,
                "scope": scope,
                "tenantId": tenant_id,
                "metadata": metadata,
                "kind": kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_variable_result_metadata import (
            ClusterVariableResultMetadata,
        )

        d = dict(src_dict)
        value = d.pop("value")

        name = ClusterVariableName(d.pop("name"))

        scope = ClusterVariableScopeEnum(d.pop("scope"))

        def _parse_tenant_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        tenant_id = _parse_tenant_id(d.pop("tenantId"))

        metadata = ClusterVariableResultMetadata.from_dict(d.pop("metadata"))

        kind = ClusterVariableKindEnum(d.pop("kind"))

        cluster_variable_result = cls(
            value=value,
            name=name,
            scope=scope,
            tenant_id=tenant_id,
            metadata=metadata,
            kind=kind,
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
