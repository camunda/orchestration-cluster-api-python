from __future__ import annotations

from camunda_orchestration_sdk.semantic_types import DocumentId
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from ..models.document_reference_camunda_document_type import DocumentReferenceCamundaDocumentType
from ..models.document_metadata_response import DocumentMetadataResponse
T = TypeVar("T", bound="DocumentReference")
@_attrs_define
class DocumentReference:
    camunda_document_type: DocumentReferenceCamundaDocumentType
    store_id: str
    document_id: DocumentId
    content_hash: None | str
    metadata: DocumentMetadataResponse
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
