from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.probe_activation_request_tenant_filter import (
    ProbeActivationRequestTenantFilter,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProbeActivationRequest")


@_attrs_define
class ProbeActivationRequest:
    """
    Attributes:
        probe_ids (list[str]): The probe IDs to collect probes for: 1 to 100 distinct values, each 1 to 256
            characters, without whitespace, and not `*`. Probe IDs on which the caller lacks the
            `ANSWER` permission are skipped.
             Example: ['validate-configuration/io.camunda:aws-credential:1', 'validate-configuration/io.camunda:slack:1'].
        max_probes_to_activate (int): The maximum number of probes to collect with this request, at least 1. Example:
            10.
        worker (str | Unset): The name of the worker, returned to the client in the answer. Example: connectors-runtime.
        request_timeout (int | Unset): How long to hold the request until a probe is collected, in milliseconds. With
            `0` or
            absent, the cluster's long polling timeout is used. With a value below `0`, long
            polling is off and the request returns at once, also when it collected no probe.
             Example: 60000.
        tenant_ids (list[str] | Unset): A list of IDs of tenants for which to collect probes.
        tenant_filter (ProbeActivationRequestTenantFilter | Unset): The tenant filtering strategy - determines whether
            to use provided tenant IDs or assigned tenant IDs from the authenticated principal's authorized tenants.
             Server default: PROVIDED.
    """

    probe_ids: list[str]
    max_probes_to_activate: int
    worker: str | Unset = UNSET
    request_timeout: int | Unset = UNSET
    tenant_ids: list[str] | Unset = UNSET
    tenant_filter: ProbeActivationRequestTenantFilter | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        probe_ids = self.probe_ids

        max_probes_to_activate = self.max_probes_to_activate

        worker = self.worker

        request_timeout = self.request_timeout

        tenant_ids: list[str] | Unset = UNSET
        if not isinstance(self.tenant_ids, Unset):
            tenant_ids = self.tenant_ids

        tenant_filter: str | Unset = UNSET
        if not isinstance(self.tenant_filter, Unset):
            tenant_filter = self.tenant_filter.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "probeIds": probe_ids,
                "maxProbesToActivate": max_probes_to_activate,
            }
        )
        if worker is not UNSET:
            field_dict["worker"] = worker
        if request_timeout is not UNSET:
            field_dict["requestTimeout"] = request_timeout
        if tenant_ids is not UNSET:
            field_dict["tenantIds"] = tenant_ids
        if tenant_filter is not UNSET:
            field_dict["tenantFilter"] = tenant_filter

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        probe_ids = cast(list[str], d.pop_required("probeIds"))

        max_probes_to_activate = d.pop_required("maxProbesToActivate")

        worker = d.pop("worker", UNSET)

        request_timeout = d.pop("requestTimeout", UNSET)

        tenant_ids = cast(list[str], d.pop("tenantIds", UNSET))

        _tenant_filter = d.pop("tenantFilter", UNSET)
        tenant_filter: ProbeActivationRequestTenantFilter | Unset
        if isinstance(_tenant_filter, Unset):
            tenant_filter = UNSET
        else:
            tenant_filter = ProbeActivationRequestTenantFilter(_tenant_filter)

        probe_activation_request = cls(
            probe_ids=probe_ids,
            max_probes_to_activate=max_probes_to_activate,
            worker=worker,
            request_timeout=request_timeout,
            tenant_ids=tenant_ids,
            tenant_filter=tenant_filter,
        )

        return probe_activation_request
