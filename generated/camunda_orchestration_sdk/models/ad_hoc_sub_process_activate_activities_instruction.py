from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.ad_hoc_sub_process_activate_activity_reference import (
        AdHocSubProcessActivateActivityReference,
    )


T = TypeVar("T", bound="AdHocSubProcessActivateActivitiesInstruction")


@_attrs_define
class AdHocSubProcessActivateActivitiesInstruction:
    """
    Attributes:
        elements (list[AdHocSubProcessActivateActivityReference]): Activities to activate.
        cancel_remaining_instances (bool | Unset): Whether to cancel remaining instances of the ad-hoc sub-process.
            Default: False.
    """

    elements: list[AdHocSubProcessActivateActivityReference]
    cancel_remaining_instances: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        elements: list[dict[str, Any]] = []
        for elements_item_data in self.elements:
            elements_item = elements_item_data.to_dict()
            elements.append(elements_item)

        cancel_remaining_instances = self.cancel_remaining_instances

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "elements": elements,
            }
        )
        if cancel_remaining_instances is not UNSET:
            field_dict["cancelRemainingInstances"] = cancel_remaining_instances

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ad_hoc_sub_process_activate_activity_reference import (
            AdHocSubProcessActivateActivityReference,
        )

        d = dict(src_dict)
        elements: list[AdHocSubProcessActivateActivityReference] = []
        _elements = d.pop("elements")
        for elements_item_data in _elements:
            elements_item = AdHocSubProcessActivateActivityReference.from_dict(
                elements_item_data
            )

            elements.append(elements_item)

        cancel_remaining_instances = d.pop("cancelRemainingInstances", UNSET)

        ad_hoc_sub_process_activate_activities_instruction = cls(
            elements=elements,
            cancel_remaining_instances=cancel_remaining_instances,
        )

        ad_hoc_sub_process_activate_activities_instruction.additional_properties = d
        return ad_hoc_sub_process_activate_activities_instruction

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
