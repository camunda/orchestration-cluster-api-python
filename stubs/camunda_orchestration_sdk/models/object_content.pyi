from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..models.agent_instance_object_content_object import (
    AgentInstanceObjectContentObject,
)

T = TypeVar("T", bound="ObjectContent")

@_attrs_define
class ObjectContent:
    content_type: str
    object_: AgentInstanceObjectContentObject
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
