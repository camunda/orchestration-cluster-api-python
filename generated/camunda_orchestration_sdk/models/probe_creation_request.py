from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields
from camunda_orchestration_sdk.semantic_types import ProbeId, TenantId

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProbeCreationRequest")


@_attrs_define
class ProbeCreationRequest:
    """
    Attributes:
        probe_id (str): The probe ID, as the worker registered it: 1 to 256 characters, without whitespace, and
            not `*`. The engine matches it to the probe IDs of polling workers by exact equality.
             Example: validate-configuration/io.camunda:aws-credential:1.
        input_ (str): A FEEL expression that evaluates to a context: the question for the worker, whose shape
            the worker of the probe ID defines. References to `camunda.vars` and
            `camunda.secrets` follow the rules of input mappings.
             Example: ={region: "eu-west-1", accessKey: camunda.secrets.awsKey}.
        tenant_id (str | Unset): The tenant of the probe. Required with multi-tenancy. Example: customer-service.
        request_timeout (int | Unset): How long to wait for an answer, in milliseconds, from 0 to 30000. With `0` or
            absent,
            the cluster's request timeout is used, capped at 30000.
             Example: 10000.
    """

    probe_id: ProbeId
    input_: str
    tenant_id: TenantId | Unset = UNSET
    request_timeout: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        probe_id = self.probe_id

        input_ = self.input_

        tenant_id = self.tenant_id

        request_timeout = self.request_timeout

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "probeId": probe_id,
                "input": input_,
            }
        )
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if request_timeout is not UNSET:
            field_dict["requestTimeout"] = request_timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        probe_id = ProbeId(d.pop_required("probeId"))

        input_ = d.pop_required("input")

        tenant_id = (
            TenantId(_val) if (_val := d.pop("tenantId", UNSET)) is not UNSET else UNSET
        )

        request_timeout = d.pop("requestTimeout", UNSET)

        probe_creation_request = cls(
            probe_id=probe_id,
            input_=input_,
            tenant_id=tenant_id,
            request_timeout=request_timeout,
        )

        return probe_creation_request
