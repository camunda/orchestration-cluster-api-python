from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="TextContent")


@_attrs_define
class TextContent:
    """A plain-text content block.

    Attributes:
        content_type (str): The content type discriminator. Example: TEXT.
        text (str): The text content.
    """

    content_type: str
    text: str

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        text = self.text

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "contentType": content_type,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_type = d.pop("contentType")

        text = d.pop("text")

        text_content = cls(
            content_type=content_type,
            text=text,
        )

        return text_content
