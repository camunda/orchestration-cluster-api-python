from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UnsupportedProbeAnswer")


@_attrs_define
class UnsupportedProbeAnswer:
    """The worker does not support this probe.

    Attributes:
        outcome (str): The outcome of the probe, `UNSUPPORTED`. Example: UNSUPPORTED.
    """

    outcome: str

    def to_dict(self) -> dict[str, Any]:
        outcome = self.outcome

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "outcome": outcome,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        outcome = d.pop_required("outcome")

        unsupported_probe_answer = cls(
            outcome=outcome,
        )

        return unsupported_probe_answer
