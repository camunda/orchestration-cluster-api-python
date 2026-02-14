from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementId, lift_element_id

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.ad_hoc_sub_process_activate_activity_reference_variables import (
        AdHocSubProcessActivateActivityReferenceVariables,
    )


T = TypeVar("T", bound="AdHocSubProcessActivateActivityReference")


@_attrs_define
class AdHocSubProcessActivateActivityReference:
    """
    Attributes:
        element_id (str): The ID of the element that should be activated. Example: Activity_106kosb.
        variables (AdHocSubProcessActivateActivityReferenceVariables | Unset): Variables to be set when activating the
            element.
    """

    element_id: ElementId
    variables: AdHocSubProcessActivateActivityReferenceVariables | Unset = UNSET
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
        field_dict.update(
            {
                "elementId": element_id,
            }
        )
        if variables is not UNSET:
            field_dict["variables"] = variables

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ad_hoc_sub_process_activate_activity_reference_variables import (
            AdHocSubProcessActivateActivityReferenceVariables,
        )

        d = dict(src_dict)
        element_id = lift_element_id(d.pop("elementId"))

        _variables = d.pop("variables", UNSET)
        variables: AdHocSubProcessActivateActivityReferenceVariables | Unset
        if isinstance(_variables, Unset):
            variables = UNSET
        else:
            variables = AdHocSubProcessActivateActivityReferenceVariables.from_dict(
                _variables
            )

        ad_hoc_sub_process_activate_activity_reference = cls(
            element_id=element_id,
            variables=variables,
        )

        ad_hoc_sub_process_activate_activity_reference.additional_properties = d
        return ad_hoc_sub_process_activate_activity_reference

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
