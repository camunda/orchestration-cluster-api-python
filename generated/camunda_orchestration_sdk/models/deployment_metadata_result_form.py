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

T = TypeVar("T", bound="DeploymentMetadataResultForm")


@_attrs_define
class DeploymentMetadataResultForm:
    """Deployed form.

    Attributes:
        form_id (str): The form ID, as parsed during deployment, together with the version forms a
            unique identifier for a specific form.
             Example: Form_1nx5hav.
        version (int): The version of the deployed form.
        resource_name (str): The name of the resource.
        tenant_id (str): The unique identifier of the tenant. Example: customer-service.
        form_key (str): The assigned key, which acts as a unique identifier for this form. Example: 2251799813684365.
    """

    form_id: FormId
    version: int
    resource_name: str
    tenant_id: TenantId
    form_key: FormKey
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        form_id = self.form_id

        version = self.version

        resource_name = self.resource_name

        tenant_id = self.tenant_id

        form_key = self.form_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "formId": form_id,
                "version": version,
                "resourceName": resource_name,
                "tenantId": tenant_id,
                "formKey": form_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        form_id = lift_form_id(d.pop("formId"))

        version = d.pop("version")

        resource_name = d.pop("resourceName")

        tenant_id = lift_tenant_id(d.pop("tenantId"))

        form_key = lift_form_key(d.pop("formKey"))

        deployment_metadata_result_form = cls(
            form_id=form_id,
            version=version,
            resource_name=resource_name,
            tenant_id=tenant_id,
            form_key=form_key,
        )

        deployment_metadata_result_form.additional_properties = d
        return deployment_metadata_result_form

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
