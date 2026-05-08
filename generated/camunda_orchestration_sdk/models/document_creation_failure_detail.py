from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="DocumentCreationFailureDetail")


@_attrs_define
class DocumentCreationFailureDetail:
    """
    Attributes:
        file_name (str): The name of the file that failed to upload.
        status (int): The HTTP status code of the failure.
        title (str): A short, human-readable summary of the problem type.
        detail (str): A human-readable explanation specific to this occurrence of the problem.
    """

    file_name: str
    status: int
    title: str
    detail: str
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        file_name = self.file_name

        status = self.status

        title = self.title

        detail = self.detail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fileName": file_name,
                "status": status,
                "title": title,
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_name = d.pop("fileName")

        status = d.pop("status")

        title = d.pop("title")

        detail = d.pop("detail")

        document_creation_failure_detail = cls(
            file_name=file_name,
            status=status,
            title=title,
            detail=detail,
        )

        document_creation_failure_detail.additional_properties = d
        return document_creation_failure_detail

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
