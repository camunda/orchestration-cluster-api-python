from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from .. import types
from ..types import UNSET, File, Unset
from ..models.document_metadata import DocumentMetadata

T = TypeVar("T", bound="CreateDocumentData")

@_attrs_define
class CreateDocumentData:
    file: File
    metadata: DocumentMetadata | Unset = UNSET
    def to_dict(self) -> dict[str, Any]: ...
    def to_multipart(self) -> types.RequestFiles: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
