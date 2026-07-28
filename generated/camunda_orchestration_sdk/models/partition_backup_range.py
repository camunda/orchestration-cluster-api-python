from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.partition_backup_range_end import PartitionBackupRangeEnd
    from ..models.partition_backup_range_start import PartitionBackupRangeStart


T = TypeVar("T", bound="PartitionBackupRange")


@_attrs_define
class PartitionBackupRange:
    """Information about one backup range for a partition.

    Attributes:
        partition_id (int): The id of the partition. Example: 3.
        start (None | PartitionBackupRangeStart): The oldest backup in the range.
        end (None | PartitionBackupRangeEnd): The newest backup in the range.
    """

    partition_id: int
    start: None | PartitionBackupRangeStart
    end: None | PartitionBackupRangeEnd
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.partition_backup_range_end import PartitionBackupRangeEnd
        from ..models.partition_backup_range_start import PartitionBackupRangeStart

        partition_id = self.partition_id

        start: dict[str, Any] | None
        if isinstance(self.start, PartitionBackupRangeStart):
            start = self.start.to_dict()
        else:
            start = self.start

        end: dict[str, Any] | None
        if isinstance(self.end, PartitionBackupRangeEnd):
            end = self.end.to_dict()
        else:
            end = self.end

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "partitionId": partition_id,
                "start": start,
                "end": end,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.partition_backup_range_end import PartitionBackupRangeEnd
        from ..models.partition_backup_range_start import PartitionBackupRangeStart

        d = dict(src_dict)
        partition_id = d.pop("partitionId")

        def _parse_start(data: object) -> None | PartitionBackupRangeStart:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_partition_backup_range_start_type_0 = (
                    PartitionBackupRangeStart.from_dict(data)
                )

                return componentsschemas_partition_backup_range_start_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PartitionBackupRangeStart, data)

        start = _parse_start(d.pop("start"))

        def _parse_end(data: object) -> None | PartitionBackupRangeEnd:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_partition_backup_range_end_type_0 = (
                    PartitionBackupRangeEnd.from_dict(data)
                )

                return componentsschemas_partition_backup_range_end_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PartitionBackupRangeEnd, data)

        end = _parse_end(d.pop("end"))

        partition_backup_range = cls(
            partition_id=partition_id,
            start=start,
            end=end,
        )

        partition_backup_range.additional_properties = d
        return partition_backup_range

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
