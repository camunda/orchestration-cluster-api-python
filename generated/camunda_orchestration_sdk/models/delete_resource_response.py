from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

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
        batch_operation (DeleteResourceResponseBatchOperation | None): The batch operation created for asynchronously
            deleting the historic data.

            Populated when `deleteHistory` is `true` and either the resource is a decision
            requirements definition, or the resource is a process definition that is already fully
            deleted from the runtime state (its history is purged directly by a batch operation).

            For a process definition that still exists in the runtime state, deletion first drains
            the definition and its history is removed asynchronously as part of that lifecycle, so no
            batch operation is returned and this field is `null`. It is also `null` for forms and
            generic resources.
    """

    resource_key: str
    batch_operation: DeleteResourceResponseBatchOperation | None
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.delete_resource_response_batch_operation import (
            DeleteResourceResponseBatchOperation,
        )

        resource_key: str
        resource_key = self.resource_key

        batch_operation: dict[str, Any] | None
        if isinstance(self.batch_operation, DeleteResourceResponseBatchOperation):
            batch_operation = self.batch_operation.to_dict()
        else:
            batch_operation = self.batch_operation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resourceKey": resource_key,
                "batchOperation": batch_operation,
            }
        )

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
        ) -> DeleteResourceResponseBatchOperation | None:
            if data is None:
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
            return cast(DeleteResourceResponseBatchOperation | None, data)

        batch_operation = _parse_batch_operation(d.pop("batchOperation"))

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
