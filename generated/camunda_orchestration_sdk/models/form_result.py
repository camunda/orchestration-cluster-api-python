from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    FormId,
    FormKey,
    TenantId,
    lift_form_id,
    lift_form_key,
    lift_tenant_id,
)

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="FormResult")


@_attrs_define
class FormResult:
    """
    Attributes:
        tenant_id (str): The tenant ID of the form. Example: customer-service.
        form_id (str): The user-provided identifier of the form. Example: Form_1nx5hav.
        schema (str): The form schema as a JSON document serialized as a string.
        version (int): The version of the the deployed form.
        form_key (str): The assigned key, which acts as a unique identifier for this form. Example: 2251799813684365.
    """

    tenant_id: TenantId
    form_id: FormId
    schema: str
    version: int
    form_key: FormKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        tenant_id = self.tenant_id

        form_id = self.form_id

        schema = self.schema

        version = self.version

        form_key = self.form_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tenantId": tenant_id,
                "formId": form_id,
                "schema": schema,
                "version": version,
                "formKey": form_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tenant_id = lift_tenant_id(d.pop("tenantId"))

        form_id = lift_form_id(d.pop("formId"))

        schema = d.pop("schema")

        version = d.pop("version")

        form_key = lift_form_key(d.pop("formKey"))

        form_result = cls(
            tenant_id=tenant_id,
            form_id=form_id,
            schema=schema,
            version=version,
            form_key=form_key,
        )

        form_result.additional_properties = d
        return form_result

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
