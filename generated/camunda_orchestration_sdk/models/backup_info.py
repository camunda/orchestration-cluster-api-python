from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.backup_info_runtime_backup_state import BackupInfoRuntimeBackupState

if TYPE_CHECKING:
    from ..models.partition_backup_info import PartitionBackupInfo


T = TypeVar("T", bound="BackupInfo")


@_attrs_define
class BackupInfo:
    """Detailed status of a runtime backup. The aggregated state is computed from the backup
    state of each partition as:
    - If the backup of all partitions is 'COMPLETED', the overall state is 'COMPLETED'.
    - If one partition is 'FAILED', the overall state is 'FAILED'.
    - Otherwise, if one partition is 'DOES_NOT_EXIST', the overall state is 'INCOMPLETE'.
    - Otherwise, if one partition is 'IN_PROGRESS', the overall state is 'IN_PROGRESS'.

        Attributes:
            backup_id (int): The id of the backup. Example: 1.
            state (BackupInfoRuntimeBackupState): The aggregated state of the backup. Example: IN_PROGRESS.
            failure_reason (None | str): Reason for failure if the state is 'FAILED'.
            details (list[PartitionBackupInfo]): Detailed status of the backup per partition. Always contains every
                partition of
                the physical tenant.
    """

    backup_id: int
    state: BackupInfoRuntimeBackupState
    failure_reason: None | str
    details: list[PartitionBackupInfo]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        backup_id = self.backup_id

        state = self.state.value

        failure_reason: None | str
        failure_reason = self.failure_reason

        details: list[dict[str, Any]] = []
        for details_item_data in self.details:
            details_item = details_item_data.to_dict()
            details.append(details_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backupId": backup_id,
                "state": state,
                "failureReason": failure_reason,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.partition_backup_info import PartitionBackupInfo

        d = dict(src_dict)
        backup_id = d.pop("backupId")

        state = BackupInfoRuntimeBackupState(d.pop("state"))

        def _parse_failure_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        failure_reason = _parse_failure_reason(d.pop("failureReason"))

        details: list[PartitionBackupInfo] = []
        _details = d.pop("details")
        for details_item_data in _details:
            details_item = PartitionBackupInfo.from_dict(details_item_data)

            details.append(details_item)

        backup_info = cls(
            backup_id=backup_id,
            state=state,
            failure_reason=failure_reason,
            details=details,
        )

        backup_info.additional_properties = d
        return backup_info

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
