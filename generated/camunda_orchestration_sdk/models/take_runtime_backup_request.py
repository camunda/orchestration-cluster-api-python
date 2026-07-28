from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

T = TypeVar("T", bound="TakeRuntimeBackupRequest")


@_attrs_define
class TakeRuntimeBackupRequest:
    """Request body for taking a runtime backup.

    Attributes:
        backup_id (int | None | Unset): The id of the backup to take. Must be omitted if continuous backups and/or a
            backup or checkpoint schedule is enabled for the physical tenant.
             Example: 1.
    """

    backup_id: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        backup_id: int | None | Unset
        if isinstance(self.backup_id, Unset):
            backup_id = UNSET
        else:
            backup_id = self.backup_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if backup_id is not UNSET:
            field_dict["backupId"] = backup_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_backup_id(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        backup_id = _parse_backup_id(d.pop("backupId", UNSET))

        take_runtime_backup_request = cls(
            backup_id=backup_id,
        )

        take_runtime_backup_request.additional_properties = d
        return take_runtime_backup_request

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
