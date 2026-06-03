from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import Username
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.camunda_user_result_c8_links import CamundaUserResultC8Links
from ..models.tenant_result import TenantResult
T = TypeVar("T", bound="CamundaUserResult")
@_attrs_define
class CamundaUserResult:
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
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
