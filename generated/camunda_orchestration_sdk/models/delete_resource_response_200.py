from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.delete_resource_response_200_batch_operation import (
        DeleteResourceResponse200BatchOperation,
    )


T = TypeVar("T", bound="DeleteResourceResponse200")


@_attrs_define
class DeleteResourceResponse200:
    """
    Attributes:
        resource_key (str): The system-assigned key for this resource, requested to be deleted.
        batch_operation (DeleteResourceResponse200BatchOperation | Unset): The batch operation created for
            asynchronously deleting the historic data.

            This field is only populated when the request `deleteHistory` is set to `true` and the resource
            is a process definition. For other resource types (decisions, forms, generic resources),
            this field will not be present in the response.
    """

    resource_key: str
    batch_operation: DeleteResourceResponse200BatchOperation | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        resource_key: str
        resource_key = self.resource_key

        batch_operation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.batch_operation, Unset):
            batch_operation = self.batch_operation.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resourceKey": resource_key,
            }
        )
        if batch_operation is not UNSET:
            field_dict["batchOperation"] = batch_operation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delete_resource_response_200_batch_operation import (
            DeleteResourceResponse200BatchOperation,
        )

        d = dict(src_dict)

        def _parse_resource_key(data: object) -> str:
            return cast(str, data)

        resource_key = _parse_resource_key(d.pop("resourceKey"))

        _batch_operation = d.pop("batchOperation", UNSET)
        batch_operation: DeleteResourceResponse200BatchOperation | Unset
        if isinstance(_batch_operation, Unset):
            batch_operation = UNSET
        else:
            batch_operation = DeleteResourceResponse200BatchOperation.from_dict(
                _batch_operation
            )

        delete_resource_response_200 = cls(
            resource_key=resource_key,
            batch_operation=batch_operation,
        )

        delete_resource_response_200.additional_properties = d
        return delete_resource_response_200

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
