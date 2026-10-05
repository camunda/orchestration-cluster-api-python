from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.history_backup_info_history_backup_state import (
    HistoryBackupInfoHistoryBackupState,
)

if TYPE_CHECKING:
    from ..models.history_backup_snapshot_info import HistoryBackupSnapshotInfo


T = TypeVar("T", bound="HistoryBackupInfo")


@_attrs_define
class HistoryBackupInfo:
    """Detailed status of a history backup. The aggregated state is computed from the state of
    each of its snapshots as:
    - If every expected snapshot exists and all are complete, the overall state is
      'COMPLETED'.
    - If one snapshot failed or is partial, the overall state is 'FAILED'.
    - Otherwise, if one snapshot is incompatible, the overall state is 'INCOMPATIBLE'.
    - Otherwise, if one snapshot is still running, the overall state is 'IN_PROGRESS'.
    - Otherwise, if snapshots are missing and the backup has not progressed within the
      configured timeout, the overall state is 'INCOMPLETE'.

        Attributes:
            backup_id (int): The id of the backup. Example: 1.
            state (HistoryBackupInfoHistoryBackupState): The aggregated state of the backup. Example: IN_PROGRESS.
            failure_reason (None | str): Reason for failure if the state is 'FAILED'.
            details (list[HistoryBackupSnapshotInfo]): Detailed status of the backup per snapshot. Always lists every
                snapshot found for
                the backup; when the backup was read without snapshot detail, each entry carries
                only its name.
    """

    backup_id: int
    state: HistoryBackupInfoHistoryBackupState
    failure_reason: None | str
    details: list[HistoryBackupSnapshotInfo]
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
        from ..models.history_backup_snapshot_info import HistoryBackupSnapshotInfo

        d = dict(src_dict)
        backup_id = d.pop("backupId")

        state = HistoryBackupInfoHistoryBackupState(d.pop("state"))

        def _parse_failure_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        failure_reason = _parse_failure_reason(d.pop("failureReason"))

        details: list[HistoryBackupSnapshotInfo] = []
        _details = d.pop("details")
        for details_item_data in _details:
            details_item = HistoryBackupSnapshotInfo.from_dict(details_item_data)

            details.append(details_item)

        history_backup_info = cls(
            backup_id=backup_id,
            state=state,
            failure_reason=failure_reason,
            details=details,
        )

        history_backup_info.additional_properties = d
        return history_backup_info

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
