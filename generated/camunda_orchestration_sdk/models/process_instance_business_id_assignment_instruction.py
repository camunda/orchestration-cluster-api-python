from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ProcessInstanceBusinessIdAssignmentInstruction")


@_attrs_define
class ProcessInstanceBusinessIdAssignmentInstruction:
    """The instruction describing the business id to assign to a running process instance.

    Attributes:
        business_id (str): An optional, user-defined string identifier that identifies the process instance
            within the scope of a process definition (scoped by tenant). If provided and uniqueness
            enforcement is enabled, the engine will reject creation if another root process instance
            with the same business id is already active for the same process definition.
            Note that any active child process instances with the same business id are not taken into account.
             Example: order-12345.
    """

    business_id: str

    def to_dict(self) -> dict[str, Any]:
        business_id = self.business_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "businessId": business_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        business_id = d.pop("businessId")

        process_instance_business_id_assignment_instruction = cls(
            business_id=business_id,
        )

        return process_instance_business_id_assignment_instruction
