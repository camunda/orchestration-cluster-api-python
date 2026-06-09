from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent_instance_object_content_object import (
        AgentInstanceObjectContentObject,
    )


T = TypeVar("T", bound="ObjectContent")


@_attrs_define
class ObjectContent:
    """An arbitrary structured content block.

    Attributes:
        content_type (str): The content type discriminator. Example: OBJECT.
        object_ (AgentInstanceObjectContentObject): Arbitrary structured content.
    """

    content_type: str
    object_: AgentInstanceObjectContentObject

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        object_ = self.object_.to_dict()

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
        from ..models.agent_instance_object_content_object import (
            AgentInstanceObjectContentObject,
        )

        d = dict(src_dict)
        content_type = d.pop("contentType")

        object_ = AgentInstanceObjectContentObject.from_dict(d.pop("object"))

        object_content = cls(
            content_type=content_type,
            object_=object_,
        )

        return object_content
