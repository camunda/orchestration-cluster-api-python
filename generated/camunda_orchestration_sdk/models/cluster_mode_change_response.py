from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cluster_mode_change_planned_change import (
        ClusterModeChangePlannedChange,
    )


T = TypeVar("T", bound="ClusterModeChangeResponse")


@_attrs_define
class ClusterModeChangeResponse:
    """The planned changes resulting from a cluster mode transition request.

    Attributes:
        change_id (str): The ID of the cluster change that was triggered by the request. Example: 7.
        planned_changes (list[ClusterModeChangePlannedChange]): The operations that will be applied to complete the
            change, grouped by the physical tenant they belong to. Groups are transitioned in parallel; the operations
            within a group are applied in the given order.
    """

    change_id: str
    planned_changes: list[ClusterModeChangePlannedChange]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        change_id = self.change_id

        planned_changes: list[dict[str, Any]] = []
        for planned_changes_item_data in self.planned_changes:
            planned_changes_item = planned_changes_item_data.to_dict()
            planned_changes.append(planned_changes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "changeId": change_id,
                "plannedChanges": planned_changes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_mode_change_planned_change import (
            ClusterModeChangePlannedChange,
        )

        d = dict(src_dict)
        change_id = d.pop("changeId")

        planned_changes: list[ClusterModeChangePlannedChange] = []
        _planned_changes = d.pop("plannedChanges")
        for planned_changes_item_data in _planned_changes:
            planned_changes_item = ClusterModeChangePlannedChange.from_dict(
                planned_changes_item_data
            )

            planned_changes.append(planned_changes_item)

        cluster_mode_change_response = cls(
            change_id=change_id,
            planned_changes=planned_changes,
        )

        cluster_mode_change_response.additional_properties = d
        return cluster_mode_change_response

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
