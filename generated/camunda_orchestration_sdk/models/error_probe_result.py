from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ErrorProbeResult")


@_attrs_define
class ErrorProbeResult:
    """The worker failed to produce an answer.

    Attributes:
        outcome (str): The outcome of the probe, `ERROR`. Example: ERROR.
        worker (str): The name of the worker that answered. Example: connectors-runtime.
        message (str): Why the worker failed, at most 500 characters.
    """

    outcome: str
    worker: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        outcome = self.outcome

        worker = self.worker

        message = self.message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "outcome": outcome,
                "worker": worker,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = RequiredFields(src_dict, cls.__name__)
        outcome = d.pop_required("outcome")

        worker = d.pop_required("worker")

        message = d.pop_required("message")

        error_probe_result = cls(
            outcome=outcome,
            worker=worker,
            message=message,
        )

        return error_probe_result
