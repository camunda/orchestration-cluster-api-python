from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import ElementId, ElementInstanceKey, ProcessInstanceKey, TenantId

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.element_instance_wait_state_result_element_type import (
    ElementInstanceWaitStateResultElementType,
)
from ..models.element_instance_wait_state_result_wait_state_type import (
    ElementInstanceWaitStateResultWaitStateType,
)

if TYPE_CHECKING:
    from ..models.element_instance_wait_state_result_job_details import (
        ElementInstanceWaitStateResultJobDetails,
    )
    from ..models.element_instance_wait_state_result_message_details import (
        ElementInstanceWaitStateResultMessageDetails,
    )


T = TypeVar("T", bound="ElementInstanceWaitStateResult")


@_attrs_define
class ElementInstanceWaitStateResult:
    """An element instance waiting state.

    Attributes:
        wait_state_type (ElementInstanceWaitStateResultWaitStateType): The type of waiting state an element instance is
            in.
        root_process_instance_key (None | str): Key of the root process instance. Example: 2251799813690746.
        process_instance_key (str): The process instance key associated to this element instance. Example:
            2251799813690746.
        element_instance_key (str): The element instance key associated to this element instance. Example:
            2251799813686789.
        element_id (str): The element ID for this element instance. Example: Activity_106kosb.
        element_type (ElementInstanceWaitStateResultElementType): The BPMN element type of this element instance.
        tenant_id (str): The tenant ID of the element instance. Example: customer-service.
        job_details (ElementInstanceWaitStateResultJobDetails | None): Job details, present when waitStateType is JOB.
        message_details (ElementInstanceWaitStateResultMessageDetails | None): Message details, present when
            waitStateType is MESSAGE.
    """

    wait_state_type: ElementInstanceWaitStateResultWaitStateType
    root_process_instance_key: None | ProcessInstanceKey
    process_instance_key: ProcessInstanceKey
    element_instance_key: ElementInstanceKey
    element_id: ElementId
    element_type: ElementInstanceWaitStateResultElementType
    tenant_id: TenantId
    job_details: ElementInstanceWaitStateResultJobDetails | None
    message_details: ElementInstanceWaitStateResultMessageDetails | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=str_any_dict_factory)

    def to_dict(self) -> dict[str, Any]:
        from ..models.element_instance_wait_state_result_job_details import (
            ElementInstanceWaitStateResultJobDetails,
        )
        from ..models.element_instance_wait_state_result_message_details import (
            ElementInstanceWaitStateResultMessageDetails,
        )

        wait_state_type = self.wait_state_type.value

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        process_instance_key = self.process_instance_key

        element_instance_key = self.element_instance_key

        element_id = self.element_id

        element_type = self.element_type.value

        tenant_id = self.tenant_id

        job_details: dict[str, Any] | None
        if isinstance(self.job_details, ElementInstanceWaitStateResultJobDetails):
            job_details = self.job_details.to_dict()
        else:
            job_details = self.job_details

        message_details: dict[str, Any] | None
        if isinstance(
            self.message_details, ElementInstanceWaitStateResultMessageDetails
        ):
            message_details = self.message_details.to_dict()
        else:
            message_details = self.message_details

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "waitStateType": wait_state_type,
                "rootProcessInstanceKey": root_process_instance_key,
                "processInstanceKey": process_instance_key,
                "elementInstanceKey": element_instance_key,
                "elementId": element_id,
                "elementType": element_type,
                "tenantId": tenant_id,
                "jobDetails": job_details,
                "messageDetails": message_details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.element_instance_wait_state_result_job_details import (
            ElementInstanceWaitStateResultJobDetails,
        )
        from ..models.element_instance_wait_state_result_message_details import (
            ElementInstanceWaitStateResultMessageDetails,
        )

        d = dict(src_dict)
        wait_state_type = ElementInstanceWaitStateResultWaitStateType(
            d.pop("waitStateType")
        )

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )


        root_process_instance_key = ProcessInstanceKey(_raw_root_process_instance_key) if isinstance(_raw_root_process_instance_key, str) else _raw_root_process_instance_key

        process_instance_key = ProcessInstanceKey(d.pop("processInstanceKey"))

        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        element_id = ElementId(d.pop("elementId"))

        element_type = ElementInstanceWaitStateResultElementType(d.pop("elementType"))

        tenant_id = TenantId(d.pop("tenantId"))

        def _parse_job_details(
            data: object,
        ) -> ElementInstanceWaitStateResultJobDetails | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_element_instance_wait_state_result_job_details_type_0 = ElementInstanceWaitStateResultJobDetails.from_dict(
                    data
                )

                return componentsschemas_element_instance_wait_state_result_job_details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ElementInstanceWaitStateResultJobDetails | None, data)

        job_details = _parse_job_details(d.pop("jobDetails"))

        def _parse_message_details(
            data: object,
        ) -> ElementInstanceWaitStateResultMessageDetails | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                componentsschemas_element_instance_wait_state_result_message_details_type_0 = ElementInstanceWaitStateResultMessageDetails.from_dict(
                    data
                )

                return componentsschemas_element_instance_wait_state_result_message_details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ElementInstanceWaitStateResultMessageDetails | None, data)

        message_details = _parse_message_details(d.pop("messageDetails"))

        element_instance_wait_state_result = cls(
            wait_state_type=wait_state_type,
            root_process_instance_key=root_process_instance_key,
            process_instance_key=process_instance_key,
            element_instance_key=element_instance_key,
            element_id=element_id,
            element_type=element_type,
            tenant_id=tenant_id,
            job_details=job_details,
            message_details=message_details,
        )

        element_instance_wait_state_result.additional_properties = d
        return element_instance_wait_state_result

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
