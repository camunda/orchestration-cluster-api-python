from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import TenantId

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.protection_mode_exact_match import ProtectionModeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )
    from ..models.advanced_protection_mode_filter import AdvancedProtectionModeFilter
    from ..models.advanced_scope_key_filter import AdvancedScopeKeyFilter
    from ..models.advanced_string_filter import AdvancedStringFilter
    from ..models.advanced_variable_key_filter import AdvancedVariableKeyFilter


T = TypeVar("T", bound="VariableFilter")


@_attrs_define
class VariableFilter:
    """Variable filter request.

    Attributes:
        name (AdvancedStringFilter | str | Unset): Name of the variable.
        value (AdvancedStringFilter | str | Unset): The value of the variable.
            Variable values in filters need to be in serialized JSON format. For example, a variable
            with string value `myValue` can be found with the filter value `"myValue"`. Consider
            appropriate escaping for special characters in JSON strings when constructing filter values.
        tenant_id (str | Unset): Tenant ID of this variable. Example: customer-service.
        is_truncated (bool | Unset): Whether the value is truncated or not.
        variable_key (AdvancedVariableKeyFilter | str | Unset): The key for this variable.
        scope_key (AdvancedScopeKeyFilter | str | Unset): The key of the scope that defines where this variable is
            directly defined. This can be a
            process instance key (for process-level variables) or an element instance key (for local
            variables scoped to tasks, subprocesses, gateways, events, etc.). Use this filter to
            find variables directly defined in specific scopes. Note that this does not include
            variables from parent scopes that would be visible through the scope hierarchy.
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset): The key of the process instance of this
            variable.
        protection_mode (AdvancedProtectionModeFilter | ProtectionModeExactMatch | Unset): The protection modes applied
            to the variable.
    """

    name: AdvancedStringFilter | str | Unset = UNSET
    value: AdvancedStringFilter | str | Unset = UNSET
    tenant_id: TenantId | Unset = UNSET
    is_truncated: bool | Unset = UNSET
    variable_key: AdvancedVariableKeyFilter | str | Unset = UNSET
    scope_key: AdvancedScopeKeyFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    protection_mode: AdvancedProtectionModeFilter | ProtectionModeExactMatch | Unset = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_scope_key_filter import AdvancedScopeKeyFilter
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.advanced_variable_key_filter import AdvancedVariableKeyFilter

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
        elif isinstance(self.scope_key, AdvancedScopeKeyFilter):
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

        protection_mode: dict[str, Any] | str | Unset
        if isinstance(self.protection_mode, Unset):
            protection_mode = UNSET
        elif isinstance(self.protection_mode, ProtectionModeExactMatch):
            protection_mode = self.protection_mode.value
        else:
            protection_mode = self.protection_mode.to_dict()

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
        if protection_mode is not UNSET:
            field_dict["protectionMode"] = protection_mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_protection_mode_filter import (
            AdvancedProtectionModeFilter,
        )
        from ..models.advanced_scope_key_filter import AdvancedScopeKeyFilter
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.advanced_variable_key_filter import AdvancedVariableKeyFilter

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

        tenant_id = (
            TenantId(_val) if (_val := d.pop("tenantId", UNSET)) is not UNSET else UNSET
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

        def _parse_scope_key(data: object) -> AdvancedScopeKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                scope_key_type_1 = AdvancedScopeKeyFilter.from_dict(data)

                return scope_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedScopeKeyFilter | str | Unset, data)

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

        def _parse_protection_mode(
            data: object,
        ) -> AdvancedProtectionModeFilter | ProtectionModeExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                protection_mode_type_0 = ProtectionModeExactMatch(data)

                return protection_mode_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            protection_mode_type_1 = AdvancedProtectionModeFilter.from_dict(data)

            return protection_mode_type_1

        protection_mode = _parse_protection_mode(d.pop("protectionMode", UNSET))

        variable_filter = cls(
            name=name,
            value=value,
            tenant_id=tenant_id,
            is_truncated=is_truncated,
            variable_key=variable_key,
            scope_key=scope_key,
            process_instance_key=process_instance_key,
            protection_mode=protection_mode,
        )

        variable_filter.additional_properties = d
        return variable_filter

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
