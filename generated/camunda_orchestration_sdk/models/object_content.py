from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ObjectContent")


@_attrs_define
class ObjectContent:
    """An arbitrary structured content block. Accepts any valid JSON value:
    objects, arrays, numbers, booleans, or strings.
    Use TEXT content for human-readable natural language;
    use OBJECT content for machine-readable structured data.

        Attributes:
            content_type (str): The content type discriminator. Example: OBJECT.
            object_ (Any): Arbitrary structured content — any valid JSON value (object, array, number, boolean, or string).
    """

    content_type: str
    object_: Any

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        object_ = self.object_

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "contentType": content_type,
                "object": object_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_type = d.pop("contentType")

        object_ = d.pop("object")

        object_content = cls(
            content_type=content_type,
            object_=object_,
        )

        return object_content
