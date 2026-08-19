from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.cluster_restore_request_overrides import (
        ClusterRestoreRequestOverrides,
    )


T = TypeVar("T", bound="ClusterRestoreRequest")


@_attrs_define
class ClusterRestoreRequest:
    """Describes a restore request issued by a cluster admin. The backup selection at the top level applies to every
    targeted physical tenant, except for the ones listed in `overrides`.

        Attributes:
            overrides (ClusterRestoreRequestOverrides | None | Unset): The backup selection to apply to individual physical
                tenants, keyed by physical tenant id. Only allowed for a cluster-wide restore, that is when no
                `physicalTenantId` parameter is given. Example: {'tenant-a': {'backupIds': [55]}}.
            from_ (datetime.datetime | None | Unset): The start of the time range to restore from, as an ISO 8601 timestamp.
                Example: 2024-01-01T10:00:00Z.
            to (datetime.datetime | None | Unset): The end of the time range to restore from, as an ISO 8601 timestamp.
                Example: 2024-01-01T12:00:00Z.
            backup_ids (list[int] | None | Unset): The IDs of the backups to restore from, one per partition. Example: [100,
                101].
    """

    overrides: ClusterRestoreRequestOverrides | None | Unset = UNSET
    from_: datetime.datetime | None | Unset = UNSET
    to: datetime.datetime | None | Unset = UNSET
    backup_ids: list[int] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.cluster_restore_request_overrides import (
            ClusterRestoreRequestOverrides,
        )

        overrides: dict[str, Any] | None | Unset
        if isinstance(self.overrides, Unset):
            overrides = UNSET
        elif isinstance(self.overrides, ClusterRestoreRequestOverrides):
            overrides = self.overrides.to_dict()
        else:
            overrides = self.overrides

        from_: None | str | Unset
        if isinstance(self.from_, Unset):
            from_ = UNSET
        elif isinstance(self.from_, datetime.datetime):
            from_ = self.from_.isoformat()
        else:
            from_ = self.from_

        to: None | str | Unset
        if isinstance(self.to, Unset):
            to = UNSET
        elif isinstance(self.to, datetime.datetime):
            to = self.to.isoformat()
        else:
            to = self.to

        backup_ids: list[int] | None | Unset
        if isinstance(self.backup_ids, Unset):
            backup_ids = UNSET
        elif isinstance(self.backup_ids, list):
            backup_ids = self.backup_ids

        else:
            backup_ids = self.backup_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if overrides is not UNSET:
            field_dict["overrides"] = overrides
        if from_ is not UNSET:
            field_dict["from"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if backup_ids is not UNSET:
            field_dict["backupIds"] = backup_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cluster_restore_request_overrides import (
            ClusterRestoreRequestOverrides,
        )

        d = dict(src_dict)

        def _parse_overrides(
            data: object,
        ) -> ClusterRestoreRequestOverrides | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_cluster_restore_request_overrides_type_0 = (
                    ClusterRestoreRequestOverrides.from_dict(data)
                )

                return componentsschemas_cluster_restore_request_overrides_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ClusterRestoreRequestOverrides | None | Unset, data)

        overrides = _parse_overrides(d.pop("overrides", UNSET))

        def _parse_from_(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                from_type_0 = isoparse(data)

                return from_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        from_ = _parse_from_(d.pop("from", UNSET))

        def _parse_to(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                to_type_0 = isoparse(data)

                return to_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        to = _parse_to(d.pop("to", UNSET))

        def _parse_backup_ids(data: object) -> list[int] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                backup_ids_type_0 = cast(list[int], data)

                return backup_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[int] | None | Unset, data)

        backup_ids = _parse_backup_ids(d.pop("backupIds", UNSET))

        cluster_restore_request = cls(
            overrides=overrides,
            from_=from_,
            to=to,
            backup_ids=backup_ids,
        )

        cluster_restore_request.additional_properties = d
        return cluster_restore_request

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
