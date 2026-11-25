from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.probe_ok_result_data import ProbeOkResultData


T = TypeVar("T", bound="OKProbeAnswer")


@_attrs_define
class OKProbeAnswer:
    """The worker produced an answer.

    Attributes:
        outcome (str): The outcome of the probe, `OK`. Example: OK.
        data (ProbeOkResultData): The answer, whose shape the worker of the probe ID defines.
    """

    outcome: str
    data: ProbeOkResultData

    def to_dict(self) -> dict[str, Any]:
        outcome = self.outcome

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "outcome": outcome,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.probe_ok_result_data import ProbeOkResultData  # noqa: PLC0415

        d = RequiredFields(src_dict, cls.__name__)
        outcome = d.pop_required("outcome")

        data = ProbeOkResultData.from_dict(d.pop_required("data"))

        ok_probe_answer = cls(
            outcome=outcome,
            data=data,
        )

        return ok_probe_answer
