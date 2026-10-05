from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="HistoryBackupSnapshotInfo")


@_attrs_define
class HistoryBackupSnapshotInfo:
    """Detailed info of a single snapshot making up a history backup.

    Attributes:
        snapshot_name (str): The name of the snapshot. Example: camunda_webapps_1_8.10.0_part_1_of_6.
        state (None | str): The state of the snapshot, reported verbatim by the secondary storage (for example
            'SUCCESS', 'IN_PROGRESS' or 'PARTIAL'). Deliberately not a closed set: Elasticsearch
            and OpenSearch report different vocabularies. Not reported when the backup was
            listed without snapshot detail.
             Example: SUCCESS.
        start_time (datetime.datetime | None): The timestamp at which the snapshot was started. Not reported when the
            backup was
            listed without snapshot detail.
             Example: 2022-09-15T13:10:38.176514094Z.
        failures (list[str]): The failures reported for this snapshot. Empty if there were none.
    """

    snapshot_name: str
    state: None | str
    start_time: datetime.datetime | None
    failures: list[str]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        snapshot_name = self.snapshot_name

        state: None | str
        state = self.state

        start_time: None | str
        if isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        failures = self.failures

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "snapshotName": snapshot_name,
                "state": state,
                "startTime": start_time,
                "failures": failures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        snapshot_name = d.pop("snapshotName")

        def _parse_state(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        state = _parse_state(d.pop("state"))

        def _parse_start_time(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        start_time = _parse_start_time(d.pop("startTime"))

        failures = cast(list[str], d.pop("failures"))

        history_backup_snapshot_info = cls(
            snapshot_name=snapshot_name,
            state=state,
            start_time=start_time,
            failures=failures,
        )

        history_backup_snapshot_info.additional_properties = d
        return history_backup_snapshot_info

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
