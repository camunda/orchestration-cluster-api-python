from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.probe_ok_result_data import ProbeOkResultData


T = TypeVar("T", bound="OKProbeResult")


@_attrs_define
class OKProbeResult:
    """The worker produced an answer.

    Attributes:
        outcome (str): The outcome of the probe, `OK`. Example: OK.
        worker (str): The name of the worker that answered. Example: connectors-runtime.
        data (ProbeOkResultData): The answer, whose shape the worker of the probe ID defines.
    """

    outcome: str
    worker: str
    data: ProbeOkResultData

    def to_dict(self) -> dict[str, Any]:
        outcome = self.outcome

        worker = self.worker

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "outcome": outcome,
                "worker": worker,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.probe_ok_result_data import ProbeOkResultData  # noqa: PLC0415

        d = RequiredFields(src_dict, cls.__name__)
        outcome = d.pop_required("outcome")

        worker = d.pop_required("worker")

        data = ProbeOkResultData.from_dict(d.pop_required("data"))

        ok_probe_result = cls(
            outcome=outcome,
            worker=worker,
            data=data,
        )

        return ok_probe_result
