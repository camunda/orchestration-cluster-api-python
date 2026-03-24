from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ProcessInstanceKey,
    ScopeKey,
    TenantId,
    VariableKey,
    lift_process_instance_key,
    lift_scope_key,
    lift_tenant_id,
    lift_variable_key,
)

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="VariableSearchResult")


@_attrs_define
class VariableSearchResult:
    """Variable search response item.

    Attributes:
        value (str): Value of this variable. Can be truncated.
        is_truncated (bool): Whether the value is truncated or not.
        name (str): Name of this variable.
        tenant_id (str): Tenant ID of this variable. Example: customer-service.
        variable_key (str): The key for this variable. Example: 2251799813683287.
        scope_key (str): The key of the scope where this variable is directly defined. For process-level
            variables, this is the process instance key. For local variables, this is the key of the
            specific element instance (task, subprocess, gateway, event, etc.) where the variable is
            directly defined.
             Example: 2251799813683890.
        process_instance_key (str): The key of the process instance of this variable. Example: 2251799813690746.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
    """

    value: str
    is_truncated: bool
    name: str
    tenant_id: TenantId
    variable_key: VariableKey
    scope_key: ScopeKey
    process_instance_key: ProcessInstanceKey
    root_process_instance_key: None | ProcessInstanceKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        is_truncated = self.is_truncated

        name = self.name

        tenant_id = self.tenant_id

        variable_key = self.variable_key

        scope_key: ScopeKey
        scope_key = self.scope_key

        process_instance_key = self.process_instance_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "isTruncated": is_truncated,
                "name": name,
                "tenantId": tenant_id,
                "variableKey": variable_key,
                "scopeKey": scope_key,
                "processInstanceKey": process_instance_key,
                "rootProcessInstanceKey": root_process_instance_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        is_truncated = d.pop("isTruncated")

        name = d.pop("name")

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        variable_key = lift_variable_key(d.pop("variableKey"))

        def _parse_scope_key(data: object) -> str:
            return cast(str, data)

        _raw_scope_key = _parse_scope_key(d.pop("scopeKey"))

        scope_key = lift_scope_key(_raw_scope_key)

        process_instance_key = lift_process_instance_key(d.pop("processInstanceKey"))

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = lift_process_instance_key(
            _raw_root_process_instance_key
        )

        variable_search_result = cls(
            value=value,
            is_truncated=is_truncated,
            name=name,
            tenant_id=tenant_id,
            variable_key=variable_key,
            scope_key=scope_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
        )

        variable_search_result.additional_properties = d
        return variable_search_result

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
