from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cluster_restore_await_mode_change_operation import (
        ClusterRestoreAwaitModeChangeOperation,
    )
    from ..models.cluster_restore_broker_operation import ClusterRestoreBrokerOperation
    from ..models.cluster_restore_mode_change_operation import (
        ClusterRestoreModeChangeOperation,
    )
    from ..models.cluster_restore_partition_operation import (
        ClusterRestorePartitionOperation,
    )
    from ..models.cluster_restore_partition_restore_operation import (
        ClusterRestorePartitionRestoreOperation,
    )


T = TypeVar("T", bound="ClusterRestorePlannedChange")


@_attrs_define
class ClusterRestorePlannedChange:
    """The operations of a restore that apply to one physical tenant.

    Attributes:
        physical_tenant_id (None | str): The physical tenant the operations apply to; null for operations that are not
            scoped to a single physical tenant, such as broker lifecycle operations. Example: default.
        operations (list[ClusterRestoreAwaitModeChangeOperation | ClusterRestoreBrokerOperation |
            ClusterRestoreModeChangeOperation | ClusterRestorePartitionOperation |
            ClusterRestorePartitionRestoreOperation]): The ordered list of operations that will be applied to the physical
            tenant.
    """

    physical_tenant_id: None | str
    operations: list[
        ClusterRestoreAwaitModeChangeOperation
        | ClusterRestoreBrokerOperation
        | ClusterRestoreModeChangeOperation
        | ClusterRestorePartitionOperation
        | ClusterRestorePartitionRestoreOperation
    ]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.cluster_restore_broker_operation import (
            ClusterRestoreBrokerOperation,
        )
        from ..models.cluster_restore_mode_change_operation import (
            ClusterRestoreModeChangeOperation,
        )
        from ..models.cluster_restore_partition_operation import (
            ClusterRestorePartitionOperation,
        )
        from ..models.cluster_restore_partition_restore_operation import (
            ClusterRestorePartitionRestoreOperation,
        )

        physical_tenant_id: None | str
        physical_tenant_id = self.physical_tenant_id

        operations: list[dict[str, Any]] = []
        for operations_item_data in self.operations:
            operations_item: dict[str, Any]
            if isinstance(operations_item_data, ClusterRestoreBrokerOperation):
                operations_item = operations_item_data.to_dict()
            elif isinstance(operations_item_data, ClusterRestorePartitionOperation):
                operations_item = operations_item_data.to_dict()
            elif isinstance(
                operations_item_data, ClusterRestorePartitionRestoreOperation
            ):
                operations_item = operations_item_data.to_dict()
            elif isinstance(operations_item_data, ClusterRestoreModeChangeOperation):
                operations_item = operations_item_data.to_dict()
            else:
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
        from ..models.cluster_restore_await_mode_change_operation import (
            ClusterRestoreAwaitModeChangeOperation,
        )
        from ..models.cluster_restore_broker_operation import (
            ClusterRestoreBrokerOperation,
        )
        from ..models.cluster_restore_mode_change_operation import (
            ClusterRestoreModeChangeOperation,
        )
        from ..models.cluster_restore_partition_operation import (
            ClusterRestorePartitionOperation,
        )
        from ..models.cluster_restore_partition_restore_operation import (
            ClusterRestorePartitionRestoreOperation,
        )

        d = dict(src_dict)

        def _parse_physical_tenant_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        physical_tenant_id = _parse_physical_tenant_id(d.pop("physicalTenantId"))

        operations: list[
            ClusterRestoreAwaitModeChangeOperation
            | ClusterRestoreBrokerOperation
            | ClusterRestoreModeChangeOperation
            | ClusterRestorePartitionOperation
            | ClusterRestorePartitionRestoreOperation
        ] = []
        _operations = d.pop("operations")
        for operations_item_data in _operations:

            def _parse_operations_item(
                data: object,
            ) -> (
                ClusterRestoreAwaitModeChangeOperation
                | ClusterRestoreBrokerOperation
                | ClusterRestoreModeChangeOperation
                | ClusterRestorePartitionOperation
                | ClusterRestorePartitionRestoreOperation
            ):
                try:
                    if not isinstance(data, dict):
                        raise TypeError()

                    data = cast(dict[str, Any], data)
                    componentsschemas_cluster_restore_operation_type_0 = (
                        ClusterRestoreBrokerOperation.from_dict(data)
                    )

                    return componentsschemas_cluster_restore_operation_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()

                    data = cast(dict[str, Any], data)
                    componentsschemas_cluster_restore_operation_type_1 = (
                        ClusterRestorePartitionOperation.from_dict(data)
                    )

                    return componentsschemas_cluster_restore_operation_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()

                    data = cast(dict[str, Any], data)
                    componentsschemas_cluster_restore_operation_type_2 = (
                        ClusterRestorePartitionRestoreOperation.from_dict(data)
                    )

                    return componentsschemas_cluster_restore_operation_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()

                    data = cast(dict[str, Any], data)
                    componentsschemas_cluster_restore_operation_type_3 = (
                        ClusterRestoreModeChangeOperation.from_dict(data)
                    )

                    return componentsschemas_cluster_restore_operation_type_3
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_cluster_restore_operation_type_4 = (
                    ClusterRestoreAwaitModeChangeOperation.from_dict(data)
                )

                return componentsschemas_cluster_restore_operation_type_4

            operations_item = _parse_operations_item(operations_item_data)

            operations.append(operations_item)

        cluster_restore_planned_change = cls(
            physical_tenant_id=physical_tenant_id,
            operations=operations,
        )

        cluster_restore_planned_change.additional_properties = d
        return cluster_restore_planned_change

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
