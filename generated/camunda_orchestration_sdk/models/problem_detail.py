from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProblemDetail")


@_attrs_define
class ProblemDetail:
    """A Problem detail object as described in [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457). There may be additional
    properties specific to the problem type.

        Attributes:
            type_ (str): A URI identifying the problem type. Default: 'about:blank'. Example:
                https://docs.camunda.io/api/v2.0/problem-types/bad-request.
            title (str): A summary of the problem type. Example: Bad Request.
            status (int): The HTTP status code for this problem. Example: 400.
            detail (str): An explanation of the problem in more detail. Example: Request property [maxJobsToActivates]
                cannot be parsed.
            instance (str): A URI path identifying the origin of the problem. Example: /v2/jobs/activation.
    """

    title: str
    status: int
    detail: str
    instance: str
    type_: str = "about:blank"
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        title = self.title

        status = self.status

        detail = self.detail

        instance = self.instance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "title": title,
                "status": status,
                "detail": detail,
                "instance": instance,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        title = d.pop("title")

        status = d.pop("status")

        detail = d.pop("detail")

        instance = d.pop("instance")

        problem_detail = cls(
            type_=type_,
            title=title,
            status=status,
            detail=detail,
            instance=instance,
        )

        problem_detail.additional_properties = d
        return problem_detail

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
