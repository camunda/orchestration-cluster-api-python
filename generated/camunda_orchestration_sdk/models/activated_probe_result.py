from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields
from camunda_orchestration_sdk.semantic_types import ProbeId, ProbeKey, TenantId

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.activated_probe_result_input import ActivatedProbeResultInput


T = TypeVar("T", bound="ActivatedProbeResult")


@_attrs_define
class ActivatedProbeResult:
    """
    Attributes:
        probe_key (str): The key to answer the probe with. Example: 2251799813685464.
        probe_id (str): The probe ID, to pick the handler when the worker polls several probe IDs. Example: validate-
            configuration/io.camunda:aws-credential:1.
        worker (str): The name of the worker that collected the probe. Example: connectors-runtime.
        deadline (int): The deadline of the probe, as a UNIX epoch timestamp in milliseconds. An answer after
            it gets 404.
             Example: 1794232249291.
        tenant_id (str): The ID of the tenant of the probe. Example: customer-service.
        physical_tenant_id (str): The ID of the physical tenant that the activation request was routed to;
            the default physical tenant when the request did not specify one.
        input_ (ActivatedProbeResultInput): The evaluated input, with the values of its secrets injected.
        secret_pointers (list[str]): The JSON pointers (RFC 6901) of the `input` values into which the engine injected a
            secret value; empty when none. Remove these values from logs and error messages.
             Example: ['/accessKey'].
    """

    probe_key: ProbeKey
    probe_id: ProbeId
    worker: str
    deadline: int
    tenant_id: TenantId
    physical_tenant_id: str
    input_: ActivatedProbeResultInput
    secret_pointers: list[str]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        probe_key = self.probe_key

        probe_id = self.probe_id

        worker = self.worker

        deadline = self.deadline

        tenant_id = self.tenant_id

        physical_tenant_id = self.physical_tenant_id

        input_ = self.input_.to_dict()

        secret_pointers = self.secret_pointers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "probeKey": probe_key,
                "probeId": probe_id,
                "worker": worker,
                "deadline": deadline,
                "tenantId": tenant_id,
                "physicalTenantId": physical_tenant_id,
                "input": input_,
                "secretPointers": secret_pointers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.activated_probe_result_input import (
            ActivatedProbeResultInput,  # noqa: PLC0415
        )

        d = RequiredFields(src_dict, cls.__name__)
        probe_key = ProbeKey(d.pop_required("probeKey"))

        probe_id = ProbeId(d.pop_required("probeId"))

        worker = d.pop_required("worker")

        deadline = d.pop_required("deadline")

        tenant_id = TenantId(d.pop_required("tenantId"))

        physical_tenant_id = d.pop_required("physicalTenantId")

        input_ = ActivatedProbeResultInput.from_dict(d.pop_required("input"))

        secret_pointers = cast(list[str], d.pop_required("secretPointers"))

        activated_probe_result = cls(
            probe_key=probe_key,
            probe_id=probe_id,
            worker=worker,
            deadline=deadline,
            tenant_id=tenant_id,
            physical_tenant_id=physical_tenant_id,
            input_=input_,
            secret_pointers=secret_pointers,
        )

        activated_probe_result.additional_properties = d
        return activated_probe_result

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
