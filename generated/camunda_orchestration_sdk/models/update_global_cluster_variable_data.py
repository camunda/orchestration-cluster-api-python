from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.update_global_cluster_variable_data_value import (
        UpdateGlobalClusterVariableDataValue,
    )


T = TypeVar("T", bound="UpdateGlobalClusterVariableData")


@_attrs_define
class UpdateGlobalClusterVariableData:
    """
    Attributes:
        value (UpdateGlobalClusterVariableDataValue): The new value of the cluster variable. Can be any JSON object or
            primitive value. Will be serialized as a JSON string in responses.
    """

    value: UpdateGlobalClusterVariableDataValue
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_global_cluster_variable_data_value import (
            UpdateGlobalClusterVariableDataValue,
        )

        d = dict(src_dict)
        value = UpdateGlobalClusterVariableDataValue.from_dict(d.pop("value"))

        update_global_cluster_variable_data = cls(
            value=value,
        )

        update_global_cluster_variable_data.additional_properties = d
        return update_global_cluster_variable_data

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
