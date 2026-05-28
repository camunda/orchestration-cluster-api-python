from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    ProcessInstanceKey,
    TenantId,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.element_instance_wait_state_message_result_element_type import (
    ElementInstanceWaitStateMessageResultElementType,
)
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.message_wait_state_details import MessageWaitStateDetails


T = TypeVar("T", bound="ElementInstanceWaitStateMessageResult")


@_attrs_define
class ElementInstanceWaitStateMessageResult:
    """Inspection result for an element instance waiting on a message.

    Attributes:
        wait_state_type (str): The type of waiting state an element instance is in.
        process_instance_key (str): The process instance key associated to this element instance. Example:
            2251799813690746.
        element_instance_key (str): The element instance key associated to this element instance. Example:
            2251799813686789.
        element_id (str): The element ID for this element instance. Example: Activity_106kosb.
        element_type (ElementInstanceWaitStateMessageResultElementType): The BPMN element type of this element instance.
        tenant_id (str): The tenant ID of the element instance. Example: customer-service.
        details (MessageWaitStateDetails):
        root_process_instance_key (None | str | Unset): Key of the root process instance. Example: 2251799813690746.
    """

    wait_state_type: str
    process_instance_key: ProcessInstanceKey
    element_instance_key: ElementInstanceKey
    element_id: ElementId
    element_type: ElementInstanceWaitStateMessageResultElementType
    tenant_id: TenantId
    details: MessageWaitStateDetails
    root_process_instance_key: None | ProcessInstanceKey | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        wait_state_type = self.wait_state_type

        process_instance_key = self.process_instance_key

        element_instance_key = self.element_instance_key

        element_id = self.element_id

        element_type = self.element_type.value

        tenant_id = self.tenant_id

        details = self.details.to_dict()

        root_process_instance_key: None | ProcessInstanceKey | Unset
        if isinstance(self.root_process_instance_key, Unset):
            root_process_instance_key = UNSET
        else:
            root_process_instance_key = self.root_process_instance_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "waitStateType": wait_state_type,
                "processInstanceKey": process_instance_key,
                "elementInstanceKey": element_instance_key,
                "elementId": element_id,
                "elementType": element_type,
                "tenantId": tenant_id,
                "details": details,
            }
        )
        if root_process_instance_key is not UNSET:
            field_dict["rootProcessInstanceKey"] = root_process_instance_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message_wait_state_details import MessageWaitStateDetails

        d = dict(src_dict)
        wait_state_type = d.pop("waitStateType")

        process_instance_key = ProcessInstanceKey(d.pop("processInstanceKey"))

        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        element_id = ElementId(d.pop("elementId"))

        element_type = ElementInstanceWaitStateMessageResultElementType(
            d.pop("elementType")
        )

        tenant_id = TenantId(d.pop("tenantId"))

        details = MessageWaitStateDetails.from_dict(d.pop("details"))

        def _parse_root_process_instance_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey", UNSET)
        )

        root_process_instance_key = (
            ProcessInstanceKey(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        element_instance_wait_state_message_result = cls(
            wait_state_type=wait_state_type,
            process_instance_key=process_instance_key,
            element_instance_key=element_instance_key,
            element_id=element_id,
            element_type=element_type,
            tenant_id=tenant_id,
            details=details,
            root_process_instance_key=root_process_instance_key,
        )

        element_instance_wait_state_message_result.additional_properties = d
        return element_instance_wait_state_message_result

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
