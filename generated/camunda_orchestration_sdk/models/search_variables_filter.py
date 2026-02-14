from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import TenantId, lift_tenant_id

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )
    from ..models.advanced_variable_key_filter import AdvancedVariableKeyFilter
    from ..models.name_advanced_filter import NameAdvancedFilter
    from ..models.scope_key_advanced_filter import ScopeKeyAdvancedFilter


T = TypeVar("T", bound="SearchVariablesFilter")


@_attrs_define
class SearchVariablesFilter:
    """The variable search filters.

    Attributes:
        name (NameAdvancedFilter | str | Unset):
        value (NameAdvancedFilter | str | Unset):
        tenant_id (str | Unset): Tenant ID of this variable. Example: customer-service.
        is_truncated (bool | Unset): Whether the value is truncated or not.
        variable_key (AdvancedVariableKeyFilter | str | Unset):
        scope_key (ScopeKeyAdvancedFilter | str | Unset):
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset):
    """

    name: NameAdvancedFilter | str | Unset = UNSET
    value: NameAdvancedFilter | str | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    is_truncated: bool | Unset = UNSET
    variable_key: AdvancedVariableKeyFilter | str | Unset = UNSET
    scope_key: ScopeKeyAdvancedFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_variable_key_filter import AdvancedVariableKeyFilter
        from ..models.name_advanced_filter import NameAdvancedFilter
        from ..models.scope_key_advanced_filter import ScopeKeyAdvancedFilter

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, NameAdvancedFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        value: dict[str, Any] | str | Unset
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, NameAdvancedFilter):
            value = self.value.to_dict()
        else:
            value = self.value

        tenant_id = self.tenant_id

        is_truncated = self.is_truncated

        variable_key: dict[str, Any] | str | Unset
        if isinstance(self.variable_key, Unset):
            variable_key = UNSET
        elif isinstance(self.variable_key, AdvancedVariableKeyFilter):
            variable_key = self.variable_key.to_dict()
        else:
            variable_key = self.variable_key

        scope_key: dict[str, Any] | str | Unset
        if isinstance(self.scope_key, Unset):
            scope_key = UNSET
        elif isinstance(self.scope_key, ScopeKeyAdvancedFilter):
            scope_key = self.scope_key.to_dict()
        else:
            scope_key = self.scope_key

        process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.process_instance_key, Unset):
            process_instance_key = UNSET
        elif isinstance(self.process_instance_key, AdvancedProcessInstanceKeyFilter):
            process_instance_key = self.process_instance_key.to_dict()
        else:
            process_instance_key = self.process_instance_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if value is not UNSET:
            field_dict["value"] = value
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if is_truncated is not UNSET:
            field_dict["isTruncated"] = is_truncated
        if variable_key is not UNSET:
            field_dict["variableKey"] = variable_key
        if scope_key is not UNSET:
            field_dict["scopeKey"] = scope_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_variable_key_filter import AdvancedVariableKeyFilter
        from ..models.name_advanced_filter import NameAdvancedFilter
        from ..models.scope_key_advanced_filter import ScopeKeyAdvancedFilter

        d = dict(src_dict)

        def _parse_name(data: object) -> NameAdvancedFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                name_type_1 = NameAdvancedFilter.from_dict(data)

                return name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(NameAdvancedFilter | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_value(data: object) -> NameAdvancedFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                value_type_1 = NameAdvancedFilter.from_dict(data)

                return value_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(NameAdvancedFilter | str | Unset, data)

        value = _parse_value(d.pop("value", UNSET))

        tenant_id = (
            lift_tenant_id(_val)
            if (_val := d.pop("tenantId", UNSET)) is not UNSET
            else UNSET
        )

        is_truncated = d.pop("isTruncated", UNSET)

        def _parse_variable_key(
            data: object,
        ) -> AdvancedVariableKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                variable_key_type_1 = AdvancedVariableKeyFilter.from_dict(data)

                return variable_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedVariableKeyFilter | str | Unset, data)

        variable_key = _parse_variable_key(d.pop("variableKey", UNSET))

        def _parse_scope_key(data: object) -> ScopeKeyAdvancedFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                scope_key_type_1 = ScopeKeyAdvancedFilter.from_dict(data)

                return scope_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ScopeKeyAdvancedFilter | str | Unset, data)

        scope_key = _parse_scope_key(d.pop("scopeKey", UNSET))

        def _parse_process_instance_key(
            data: object,
        ) -> AdvancedProcessInstanceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_instance_key_type_1 = (
                    AdvancedProcessInstanceKeyFilter.from_dict(data)
                )

                return process_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedProcessInstanceKeyFilter | str | Unset, data)

        process_instance_key = _parse_process_instance_key(
            d.pop("processInstanceKey", UNSET)
        )

        search_variables_filter = cls(
            name=name,
            value=value,
            tenant_id=tenant_id,
            is_truncated=is_truncated,
            variable_key=variable_key,
            scope_key=scope_key,
            process_instance_key=process_instance_key,
        )

        search_variables_filter.additional_properties = d
        return search_variables_filter

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
