from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ClusterVariableName

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.create_cluster_variable_request_metadata import (
        CreateClusterVariableRequestMetadata,
    )
    from ..models.create_cluster_variable_request_value import (
        CreateClusterVariableRequestValue,
    )


T = TypeVar("T", bound="CreateClusterVariableRequest")


@_attrs_define
class CreateClusterVariableRequest:
    """
    Attributes:
        name (str): The name of the cluster variable. Must be unique within its scope (global or tenant-specific).
            Example: feature-flag-checkout.
        value (CreateClusterVariableRequestValue): The value of the cluster variable. Can be any JSON object or
            primitive value. Will be serialized as a JSON string in responses.
        metadata (CreateClusterVariableRequestMetadata | Unset): A generic key-value metadata bag attached to the
            cluster variable. Values must be strings or numbers. Limited to 100 entries and a configurable maximum
            serialized size (default: 100 entries at max key length of a cluster variable name (256 chars) plus the maximum
            value length, 8192 characters).
    """

    name: ClusterVariableName
    value: CreateClusterVariableRequestValue
    metadata: CreateClusterVariableRequestMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value.to_dict()

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_cluster_variable_request_metadata import (
            CreateClusterVariableRequestMetadata,
        )
        from ..models.create_cluster_variable_request_value import (
            CreateClusterVariableRequestValue,
        )

        d = dict(src_dict)
        name = ClusterVariableName(d.pop("name"))

        value = CreateClusterVariableRequestValue.from_dict(d.pop("value"))

        _metadata = d.pop("metadata", UNSET)
        metadata: CreateClusterVariableRequestMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateClusterVariableRequestMetadata.from_dict(_metadata)

        create_cluster_variable_request = cls(
            name=name,
            value=value,
            metadata=metadata,
        )

        create_cluster_variable_request.additional_properties = d
        return create_cluster_variable_request

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
