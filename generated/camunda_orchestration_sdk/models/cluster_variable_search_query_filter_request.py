from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.cluster_variable_scope_exact_match import ClusterVariableScopeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_cluster_variable_scope_filter import (
        AdvancedClusterVariableScopeFilter,
    )
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="ClusterVariableSearchQueryFilterRequest")


@_attrs_define
class ClusterVariableSearchQueryFilterRequest:
    """Cluster variable filter request.

    Attributes:
        name (AdvancedStringFilter | str | Unset):
        value (AdvancedStringFilter | str | Unset):
        scope (AdvancedClusterVariableScopeFilter | ClusterVariableScopeExactMatch | Unset):
        tenant_id (AdvancedStringFilter | str | Unset):
        is_truncated (bool | Unset): Filter cluster variables by truncation status of their stored values. When true,
            returns only variables whose stored values are truncated (i.e., the value exceeds the storage size limit and is
            truncated in storage). When false, returns only variables with non-truncated stored values. This filter is based
            on the underlying storage characteristic, not the response format.
    """

    name: AdvancedStringFilter | str | Unset = UNSET
    value: AdvancedStringFilter | str | Unset = UNSET
    scope: (
        AdvancedClusterVariableScopeFilter | ClusterVariableScopeExactMatch | Unset
    ) = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    is_truncated: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_string_filter import AdvancedStringFilter

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, AdvancedStringFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        value: dict[str, Any] | str | Unset
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, AdvancedStringFilter):
            value = self.value.to_dict()
        else:
            value = self.value

        scope: dict[str, Any] | str | Unset
        if isinstance(self.scope, Unset):
            scope = UNSET
        elif isinstance(self.scope, ClusterVariableScopeExactMatch):
            scope = self.scope.value
        else:
            scope = self.scope.to_dict()

        tenant_id: dict[str, Any] | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        elif isinstance(self.tenant_id, AdvancedStringFilter):
            tenant_id = self.tenant_id.to_dict()
        else:
            tenant_id = self.tenant_id

        is_truncated = self.is_truncated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if value is not UNSET:
            field_dict["value"] = value
        if scope is not UNSET:
            field_dict["scope"] = scope
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if is_truncated is not UNSET:
            field_dict["isTruncated"] = is_truncated

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_cluster_variable_scope_filter import (
            AdvancedClusterVariableScopeFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)

        def _parse_name(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                name_type_1 = AdvancedStringFilter.from_dict(data)

                return name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_value(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                value_type_1 = AdvancedStringFilter.from_dict(data)

                return value_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        value = _parse_value(d.pop("value", UNSET))

        def _parse_scope(
            data: object,
        ) -> (
            AdvancedClusterVariableScopeFilter | ClusterVariableScopeExactMatch | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_type_0 = ClusterVariableScopeExactMatch(data)

                return scope_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            scope_type_1 = AdvancedClusterVariableScopeFilter.from_dict(data)

            return scope_type_1

        scope = _parse_scope(d.pop("scope", UNSET))

        def _parse_tenant_id(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                tenant_id_type_1 = AdvancedStringFilter.from_dict(data)

                return tenant_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        tenant_id = _parse_tenant_id(d.pop("tenantId", UNSET))

        is_truncated = d.pop("isTruncated", UNSET)

        cluster_variable_search_query_filter_request = cls(
            name=name,
            value=value,
            scope=scope,
            tenant_id=tenant_id,
            is_truncated=is_truncated,
        )

        cluster_variable_search_query_filter_request.additional_properties = d
        return cluster_variable_search_query_filter_request

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
