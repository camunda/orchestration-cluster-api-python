from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import DocumentId

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.document_reference_camunda_document_type import (
    DocumentReferenceCamundaDocumentType,
)

if TYPE_CHECKING:
    from ..models.document_metadata_response import DocumentMetadataResponse


T = TypeVar("T", bound="DocumentReference")


@_attrs_define
class DocumentReference:
    """
    Attributes:
        camunda_document_type (DocumentReferenceCamundaDocumentType): Document discriminator. Always set to "camunda".
        store_id (str): The ID of the document store.
        document_id (str): The ID of the document.
        content_hash (None | str): The hash of the document.
        metadata (DocumentMetadataResponse): Information about the document that is returned in responses.
    """

    camunda_document_type: DocumentReferenceCamundaDocumentType
    store_id: str
    document_id: DocumentId
    content_hash: None | str
    metadata: DocumentMetadataResponse
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        camunda_document_type = self.camunda_document_type.value

        store_id = self.store_id

        document_id = self.document_id

        content_hash: None | str
        content_hash = self.content_hash

        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "camunda.document.type": camunda_document_type,
                "storeId": store_id,
                "documentId": document_id,
                "contentHash": content_hash,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document_metadata_response import DocumentMetadataResponse

        d = dict(src_dict)
        camunda_document_type = DocumentReferenceCamundaDocumentType(
            d.pop("camunda.document.type")
        )

        store_id = d.pop("storeId")

        document_id = DocumentId(d.pop("documentId"))

        def _parse_content_hash(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        content_hash = _parse_content_hash(d.pop("contentHash"))

        metadata = DocumentMetadataResponse.from_dict(d.pop("metadata"))

        document_reference = cls(
            camunda_document_type=camunda_document_type,
            store_id=store_id,
            document_id=document_id,
            content_hash=content_hash,
            metadata=metadata,
        )

        document_reference.additional_properties = d
        return document_reference

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
