from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cluster_mode_change_operation import ClusterModeChangeOperation


T = TypeVar("T", bound="ClusterModeChangePlannedChange")


@_attrs_define
class ClusterModeChangePlannedChange:
    """The operations of a cluster mode change that apply to one physical tenant.

    Attributes:
        physical_tenant_id (None | str): The physical tenant the operations apply to; null for operations that are not
            scoped to a single physical tenant, such as broker lifecycle operations. Example: default.
        operations (list[ClusterModeChangeOperation]): The ordered list of operations that will be applied to the
            physical tenant.
    """

    physical_tenant_id: None | str
    operations: list[ClusterModeChangeOperation]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        physical_tenant_id: None | str
        physical_tenant_id = self.physical_tenant_id

        operations: list[dict[str, Any]] = []
        for operations_item_data in self.operations:
            operations_item = operations_item_data.to_dict()
            operations.append(operations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "physicalTenantId": physical_tenant_id,
                "operations": operations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_mode_change_operation import ClusterModeChangeOperation

        d = dict(src_dict)

        def _parse_physical_tenant_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        physical_tenant_id = _parse_physical_tenant_id(d.pop("physicalTenantId"))

        operations: list[ClusterModeChangeOperation] = []
        _operations = d.pop("operations")
        for operations_item_data in _operations:
            operations_item = ClusterModeChangeOperation.from_dict(operations_item_data)

            operations.append(operations_item)

        cluster_mode_change_planned_change = cls(
            physical_tenant_id=physical_tenant_id,
            operations=operations,
        )

        cluster_mode_change_planned_change.additional_properties = d
        return cluster_mode_change_planned_change

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
