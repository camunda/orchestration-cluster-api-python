from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..models.job_activation_request_tenant_filter import JobActivationRequestTenantFilter
from ..types import UNSET, Unset
T = TypeVar("T", bound="JobActivationRequest")
@_attrs_define
class JobActivationRequest:
    type_: str
    timeout: int
    max_jobs_to_activate: int
    worker: str | Unset = UNSET
    fetch_variable: list[str] | Unset = UNSET
    request_timeout: int | Unset = UNSET
    tenant_ids: list[str] | Unset = UNSET
    tenant_filter: JobActivationRequestTenantFilter | Unset = (
            JobActivationRequestTenantFilter.PROVIDED
        )
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
