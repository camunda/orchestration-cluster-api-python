from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.document_creation_failure_detail import DocumentCreationFailureDetail
    from ..models.document_reference import DocumentReference


T = TypeVar("T", bound="DocumentCreationBatchResponse")


@_attrs_define
class DocumentCreationBatchResponse:
    """
    Attributes:
        failed_documents (list[DocumentCreationFailureDetail]): Documents that were successfully created.
        created_documents (list[DocumentReference]): Documents that failed creation.
    """

    failed_documents: list[DocumentCreationFailureDetail]
    created_documents: list[DocumentReference]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        failed_documents: list[dict[str, Any]] = []
        for failed_documents_item_data in self.failed_documents:
            failed_documents_item = failed_documents_item_data.to_dict()
            failed_documents.append(failed_documents_item)

        created_documents: list[dict[str, Any]] = []
        for created_documents_item_data in self.created_documents:
            created_documents_item = created_documents_item_data.to_dict()
            created_documents.append(created_documents_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "failedDocuments": failed_documents,
                "createdDocuments": created_documents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document_creation_failure_detail import (
            DocumentCreationFailureDetail,
        )
        from ..models.document_reference import DocumentReference

        d = dict(src_dict)
        failed_documents: list[DocumentCreationFailureDetail] = []
        _failed_documents = d.pop("failedDocuments")
        for failed_documents_item_data in _failed_documents:
            failed_documents_item = DocumentCreationFailureDetail.from_dict(
                failed_documents_item_data
            )

            failed_documents.append(failed_documents_item)

        created_documents: list[DocumentReference] = []
        _created_documents = d.pop("createdDocuments")
        for created_documents_item_data in _created_documents:
            created_documents_item = DocumentReference.from_dict(
                created_documents_item_data
            )

            created_documents.append(created_documents_item)

        document_creation_batch_response = cls(
            failed_documents=failed_documents,
            created_documents=created_documents,
        )

        document_creation_batch_response.additional_properties = d
        return document_creation_batch_response

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
