from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ProcessDefinitionId,
    ProcessInstanceKey,
    lift_process_definition_id,
    lift_process_instance_key,
)

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.document_metadata_custom_properties import (
        DocumentMetadataCustomProperties,
    )


T = TypeVar("T", bound="DocumentMetadataResponse")


@_attrs_define
class DocumentMetadataResponse:
    """Information about the document that is returned in responses.

    Attributes:
        content_type (str): The content type of the document.
        file_name (str): The name of the file.
        expires_at (datetime.datetime | None): The date and time when the document expires.
        size (int): The size of the document in bytes.
        process_definition_id (None | str): The ID of the process definition that created the document. Example: new-
            account-onboarding-workflow.
        process_instance_key (None | str): The key of the process instance that created the document. Example:
            2251799813690746.
        custom_properties (DocumentMetadataCustomProperties): Custom properties of the document.
    """

    content_type: str
    file_name: str
    expires_at: datetime.datetime | None
    size: int
    process_definition_id: None | ProcessDefinitionId
    process_instance_key: None | ProcessInstanceKey
    custom_properties: DocumentMetadataCustomProperties
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        file_name = self.file_name

        expires_at: None | str
        if isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        size = self.size

        process_definition_id: None | ProcessDefinitionId
        process_definition_id = self.process_definition_id

        process_instance_key: None | ProcessInstanceKey
        process_instance_key = self.process_instance_key

        custom_properties = self.custom_properties.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "contentType": content_type,
                "fileName": file_name,
                "expiresAt": expires_at,
                "size": size,
                "processDefinitionId": process_definition_id,
                "processInstanceKey": process_instance_key,
                "customProperties": custom_properties,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document_metadata_custom_properties import (
            DocumentMetadataCustomProperties,
        )

        d = dict(src_dict)
        content_type = d.pop("contentType")

        file_name = d.pop("fileName")

        def _parse_expires_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        expires_at = _parse_expires_at(d.pop("expiresAt"))

        size = d.pop("size")

        def _parse_process_definition_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_definition_id = _parse_process_definition_id(
            d.pop("processDefinitionId")
        )

        process_definition_id = lift_process_definition_id(_raw_process_definition_id)

        def _parse_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_instance_key = _parse_process_instance_key(
            d.pop("processInstanceKey")
        )

        process_instance_key = lift_process_instance_key(_raw_process_instance_key)

        custom_properties = DocumentMetadataCustomProperties.from_dict(
            d.pop("customProperties")
        )

        document_metadata_response = cls(
            content_type=content_type,
            file_name=file_name,
            expires_at=expires_at,
            size=size,
            process_definition_id=process_definition_id,
            process_instance_key=process_instance_key,
            custom_properties=custom_properties,
        )

        document_metadata_response.additional_properties = d
        return document_metadata_response

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
