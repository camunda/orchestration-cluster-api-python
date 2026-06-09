from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..models.agent_instance_document_content_document_reference import (
    AgentInstanceDocumentContentDocumentReference,
)

T = TypeVar("T", bound="DocumentContent")

@_attrs_define
class DocumentContent:
    content_type: str
    document_reference: AgentInstanceDocumentContentDocumentReference
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
