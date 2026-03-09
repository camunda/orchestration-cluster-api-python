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


T = TypeVar("T", bound="JobErrorStatisticsFilter")


@_attrs_define
class JobErrorStatisticsFilter:
    """Job error statistics search filter.

    Attributes:
        from_ (datetime.datetime): Start of the time window to filter metrics. ISO 8601 date-time format.
             Example: 2024-07-28T15:51:28.071Z.
        to (datetime.datetime): End of the time window to filter metrics. ISO 8601 date-time format.
             Example: 2024-07-29T15:51:28.071Z.
        job_type (str): Job type to return error metrics for. Example: fetch-customer-data.
        error_code (AdvancedStringFilter | str | Unset): Optional error code filter with advanced search capabilities.
        error_message (AdvancedStringFilter | str | Unset): Optional error message filter with advanced search
            capabilities.
    """

    from_: datetime.datetime
    to: datetime.datetime
    job_type: str
    error_code: AdvancedStringFilter | str | Unset = UNSET
    error_message: AdvancedStringFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_string_filter import AdvancedStringFilter

        from_ = self.from_.isoformat()

        to = self.to.isoformat()

        job_type = self.job_type

        error_code: dict[str, Any] | str | Unset
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        elif isinstance(self.error_code, AdvancedStringFilter):
            error_code = self.error_code.to_dict()
        else:
            error_code = self.error_code

        error_message: dict[str, Any] | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        elif isinstance(self.error_message, AdvancedStringFilter):
            error_message = self.error_message.to_dict()
        else:
            error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "to": to,
                "jobType": job_type,
            }
        )
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)
        from_ = isoparse(d.pop("from"))

        to = isoparse(d.pop("to"))

        job_type = d.pop("jobType")

        def _parse_error_code(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                error_code_type_1 = AdvancedStringFilter.from_dict(data)

                return error_code_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        error_code = _parse_error_code(d.pop("errorCode", UNSET))

        def _parse_error_message(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                error_message_type_1 = AdvancedStringFilter.from_dict(data)

                return error_message_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        error_message = _parse_error_message(d.pop("errorMessage", UNSET))

        job_error_statistics_filter = cls(
            from_=from_,
            to=to,
            job_type=job_type,
            error_code=error_code,
            error_message=error_message,
        )

        job_error_statistics_filter.additional_properties = d
        return job_error_statistics_filter

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
