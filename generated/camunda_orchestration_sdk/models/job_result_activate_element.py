from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementId, lift_element_id

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.job_result_activate_element_variables import (
        JobResultActivateElementVariables,
    )


T = TypeVar("T", bound="JobResultActivateElement")


@_attrs_define
class JobResultActivateElement:
    """Instruction to activate a single BPMN element within an ad‑hoc sub‑process, optionally providing variables scoped to
    that element.

        Attributes:
            element_id (str | Unset): The element ID to activate. Example: Activity_106kosb.
            variables (JobResultActivateElementVariables | Unset): Variables for the element.
    """

    element_id: ElementId | Unset = UNSET
    variables: JobResultActivateElementVariables | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        element_id = self.element_id

        variables: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.job_result_activate_element_variables import (
            JobResultActivateElementVariables,
        )

        d = dict(src_dict)
        element_id = (
            lift_element_id(_val)
            if (_val := d.pop("elementId", UNSET)) is not UNSET
            else UNSET
        )

        _variables = d.pop("variables", UNSET)
        variables: JobResultActivateElementVariables | Unset
        if isinstance(_variables, Unset):
            variables = UNSET
        else:
            variables = JobResultActivateElementVariables.from_dict(_variables)

        job_result_activate_element = cls(
            element_id=element_id,
            variables=variables,
        )

        job_result_activate_element.additional_properties = d
        return job_result_activate_element

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
