from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import Username, lift_username

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.camunda_user_result_c8_links import CamundaUserResultC8Links
    from ..models.tenant_result import TenantResult


T = TypeVar("T", bound="CamundaUserResult")


@_attrs_define
class CamundaUserResult:
    """
    Attributes:
        username (str): The username of the user. Example: swillis.
        display_name (None | str): The display name of the user. Example: Samantha Willis.
        email (None | str): The email of the user. Example: swillis@acme.com.
        authorized_components (list[str]): The web components the user is authorized to use. Example: ['*'].
        tenants (list[TenantResult]): The tenants the user is a member of.
        groups (list[str]): The groups assigned to the user. Example: ['customer-service'].
        roles (list[str]): The roles assigned to the user. Example: ['frontline-support'].
        sales_plan_type (None | str): The plan of the user.
        c_8_links (CamundaUserResultC8Links): The links to the components in the C8 stack.
        can_logout (bool): Flag for understanding if the user is able to perform logout.
    """

    username: Username
    display_name: None | str
    email: None | str
    authorized_components: list[str]
    tenants: list[TenantResult]
    groups: list[str]
    roles: list[str]
    sales_plan_type: None | str
    c_8_links: CamundaUserResultC8Links
    can_logout: bool
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        display_name: None | str
        display_name = self.display_name

        email: None | str
        email = self.email

        authorized_components = self.authorized_components

        tenants: list[dict[str, Any]] = []
        for tenants_item_data in self.tenants:
            tenants_item = tenants_item_data.to_dict()
            tenants.append(tenants_item)

        groups = self.groups

        roles = self.roles

        sales_plan_type: None | str
        sales_plan_type = self.sales_plan_type

        c_8_links = self.c_8_links.to_dict()

        can_logout = self.can_logout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "displayName": display_name,
                "email": email,
                "authorizedComponents": authorized_components,
                "tenants": tenants,
                "groups": groups,
                "roles": roles,
                "salesPlanType": sales_plan_type,
                "c8Links": c_8_links,
                "canLogout": can_logout,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.camunda_user_result_c8_links import CamundaUserResultC8Links
        from ..models.tenant_result import TenantResult

        d = dict(src_dict)
        username = lift_username(d.pop("username"))

        def _parse_display_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        display_name = _parse_display_name(d.pop("displayName"))

        def _parse_email(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        email = _parse_email(d.pop("email"))

        authorized_components = cast(list[str], d.pop("authorizedComponents"))

        tenants: list[TenantResult] = []
        _tenants = d.pop("tenants")
        for tenants_item_data in _tenants:
            tenants_item = TenantResult.from_dict(tenants_item_data)

            tenants.append(tenants_item)

        groups = cast(list[str], d.pop("groups"))

        roles = cast(list[str], d.pop("roles"))

        def _parse_sales_plan_type(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        sales_plan_type = _parse_sales_plan_type(d.pop("salesPlanType"))

        c_8_links = CamundaUserResultC8Links.from_dict(d.pop("c8Links"))

        can_logout = d.pop("canLogout")

        camunda_user_result = cls(
            username=username,
            display_name=display_name,
            email=email,
            authorized_components=authorized_components,
            tenants=tenants,
            groups=groups,
            roles=roles,
            sales_plan_type=sales_plan_type,
            c_8_links=c_8_links,
            can_logout=can_logout,
        )

        camunda_user_result.additional_properties = d
        return camunda_user_result

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
