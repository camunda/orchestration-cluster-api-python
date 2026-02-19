from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="JobTypeStatisticsFilter")


@_attrs_define
class JobTypeStatisticsFilter:
    """Job type statistics search filter.

    Attributes:
        from_ (datetime.datetime): Start of the time window to filter metrics. ISO 8601 date-time format.
             Example: 2024-07-28T15:51:28.071Z.
        to (datetime.datetime): End of the time window to filter metrics. ISO 8601 date-time format.
             Example: 2024-07-29T15:51:28.071Z.
        job_type (AdvancedStringFilter | str | Unset):
    """

    from_: datetime.datetime
    to: datetime.datetime
    job_type: AdvancedStringFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_string_filter import AdvancedStringFilter

        from_ = self.from_.isoformat()

        to = self.to.isoformat()

        job_type: dict[str, Any] | str | Unset
        if isinstance(self.job_type, Unset):
            job_type = UNSET
        elif isinstance(self.job_type, AdvancedStringFilter):
            job_type = self.job_type.to_dict()
        else:
            job_type = self.job_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "to": to,
            }
        )
        if job_type is not UNSET:
            field_dict["jobType"] = job_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)
        from_ = isoparse(d.pop("from"))

        to = isoparse(d.pop("to"))

        def _parse_job_type(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                job_type_type_1 = AdvancedStringFilter.from_dict(data)

                return job_type_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        job_type = _parse_job_type(d.pop("jobType", UNSET))

        job_type_statistics_filter = cls(
            from_=from_,
            to=to,
            job_type=job_type,
        )

        job_type_statistics_filter.additional_properties = d
        return job_type_statistics_filter

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
