from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.delete_resource_response_batch_operation import (
        DeleteResourceResponseBatchOperation,
    )


T = TypeVar("T", bound="DeleteResourceResponse")


@_attrs_define
class DeleteResourceResponse:
    """
    Attributes:
        resource_key (str): The system-assigned key for this resource, requested to be deleted.
        batch_operation (DeleteResourceResponseBatchOperation | None | Unset): The batch operation created for
            asynchronously deleting the historic data.

            This field is only populated when the request `deleteHistory` is set to `true` and the resource
            is a process definition. For other resource types (decisions, forms, generic resources),
            this field will be `null`.
    """

    resource_key: str
    batch_operation: DeleteResourceResponseBatchOperation | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.delete_resource_response_batch_operation import (
            DeleteResourceResponseBatchOperation,
        )

        resource_key: str
        resource_key = self.resource_key

        batch_operation: dict[str, Any] | None | Unset
        if isinstance(self.batch_operation, Unset):
            batch_operation = UNSET
        elif isinstance(self.batch_operation, DeleteResourceResponseBatchOperation):
            batch_operation = self.batch_operation.to_dict()
        else:
            batch_operation = self.batch_operation

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
        from ..models.delete_resource_response_batch_operation import (
            DeleteResourceResponseBatchOperation,
        )

        d = dict(src_dict)

        def _parse_resource_key(data: object) -> str:
            return cast(str, data)

        resource_key = _parse_resource_key(d.pop("resourceKey"))

        def _parse_batch_operation(
            data: object,
        ) -> DeleteResourceResponseBatchOperation | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_delete_resource_response_batch_operation_type_0 = (
                    DeleteResourceResponseBatchOperation.from_dict(data)
                )

                return componentsschemas_delete_resource_response_batch_operation_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeleteResourceResponseBatchOperation | None | Unset, data)

        batch_operation = _parse_batch_operation(d.pop("batchOperation", UNSET))

        delete_resource_response = cls(
            resource_key=resource_key,
            batch_operation=batch_operation,
        )

        delete_resource_response.additional_properties = d
        return delete_resource_response

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
