from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent_instance_document_content_document_reference import (
        AgentInstanceDocumentContentDocumentReference,
    )


T = TypeVar("T", bound="DocumentContent")


@_attrs_define
class DocumentContent:
    """A Camunda Document Store reference content block.

    Attributes:
        content_type (str): The content type discriminator. Example: DOCUMENT.
        document_reference (AgentInstanceDocumentContentDocumentReference): A reference to a document stored in the
            Camunda Document Store.
    """

    content_type: str
    document_reference: AgentInstanceDocumentContentDocumentReference

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        document_reference = self.document_reference.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "contentType": content_type,
                "documentReference": document_reference,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_instance_document_content_document_reference import (
            AgentInstanceDocumentContentDocumentReference,
        )

        d = dict(src_dict)
        content_type = d.pop("contentType")

        document_reference = AgentInstanceDocumentContentDocumentReference.from_dict(
            d.pop("documentReference")
        )

        document_content = cls(
            content_type=content_type,
            document_reference=document_reference,
        )

        return document_content
