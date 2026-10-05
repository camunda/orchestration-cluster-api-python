from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.restore_status_response_status import RestoreStatusResponseStatus

if TYPE_CHECKING:
    from ..models.restore_broker_status import RestoreBrokerStatus


T = TypeVar("T", bound="RestoreStatusResponse")


@_attrs_define
class RestoreStatusResponse:
    """The status of the restore that is currently in progress.

    Attributes:
        status (RestoreStatusResponseStatus): The overall status of the restore. Example: IN_PROGRESS.
        change_id (str): The ID of the cluster change that performs the restore. Example: -2.
        started_at (datetime.datetime | None): The time the restore started, as an ISO 8601 timestamp. Example:
            2024-01-01T10:00:00Z.
        brokers (list[RestoreBrokerStatus]): The per-broker restore status.
    """

    status: RestoreStatusResponseStatus
    change_id: str
    started_at: datetime.datetime | None
    brokers: list[RestoreBrokerStatus]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        change_id = self.change_id

        started_at: None | str
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        brokers: list[dict[str, Any]] = []
        for brokers_item_data in self.brokers:
            brokers_item = brokers_item_data.to_dict()
            brokers.append(brokers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "changeId": change_id,
                "startedAt": started_at,
                "brokers": brokers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.restore_broker_status import RestoreBrokerStatus

        d = dict(src_dict)
        status = RestoreStatusResponseStatus(d.pop("status"))

        change_id = d.pop("changeId")

        def _parse_started_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        started_at = _parse_started_at(d.pop("startedAt"))

        brokers: list[RestoreBrokerStatus] = []
        _brokers = d.pop("brokers")
        for brokers_item_data in _brokers:
            brokers_item = RestoreBrokerStatus.from_dict(brokers_item_data)

            brokers.append(brokers_item)

        restore_status_response = cls(
            status=status,
            change_id=change_id,
            started_at=started_at,
            brokers=brokers,
        )

        restore_status_response.additional_properties = d
        return restore_status_response

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
