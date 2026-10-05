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

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

from ..models.element_instance_wait_state_result_element_type import (
    ElementInstanceWaitStateResultElementType,
)

if TYPE_CHECKING:
    from ..models.condition_wait_state_details import ConditionWaitStateDetails
    from ..models.job_wait_state_details import JobWaitStateDetails
    from ..models.message_wait_state_details import MessageWaitStateDetails
    from ..models.signal_wait_state_details import SignalWaitStateDetails
    from ..models.timer_wait_state_details import TimerWaitStateDetails
    from ..models.user_task_wait_state_details import UserTaskWaitStateDetails


T = TypeVar("T", bound="ElementInstanceWaitStateResult")


@_attrs_define
class ElementInstanceWaitStateResult:
    """An element instance waiting state.

    Attributes:
        root_process_instance_key (None | str): Key of the root process instance. Example: 2251799813690746.
        process_instance_key (str): The process instance key associated to this element instance. Example:
            2251799813690746.
        element_instance_key (str): The element instance key associated to this element instance. Example:
            2251799813686789.
        element_id (str): The element ID for this element instance. Example: Activity_106kosb.
        element_type (ElementInstanceWaitStateResultElementType): The BPMN element type of this element instance.
        tenant_id (str): The tenant ID of the element instance. Example: customer-service.
        bpmn_process_id (str): The BPMN process ID of the process definition associated to this element instance.
        details (ConditionWaitStateDetails | JobWaitStateDetails | MessageWaitStateDetails | SignalWaitStateDetails |
            TimerWaitStateDetails | UserTaskWaitStateDetails): Wait-state-specific details, resolved by waitStateType.
    """

    root_process_instance_key: None | ProcessInstanceKey
    process_instance_key: ProcessInstanceKey
    element_instance_key: ElementInstanceKey
    element_id: ElementId
    element_type: ElementInstanceWaitStateResultElementType
    tenant_id: TenantId
    bpmn_process_id: str
    details: (
        ConditionWaitStateDetails
        | JobWaitStateDetails
        | MessageWaitStateDetails
        | SignalWaitStateDetails
        | TimerWaitStateDetails
        | UserTaskWaitStateDetails
    )
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.job_wait_state_details import JobWaitStateDetails
        from ..models.message_wait_state_details import MessageWaitStateDetails
        from ..models.signal_wait_state_details import SignalWaitStateDetails
        from ..models.timer_wait_state_details import TimerWaitStateDetails
        from ..models.user_task_wait_state_details import UserTaskWaitStateDetails

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        process_instance_key = self.process_instance_key

        element_instance_key = self.element_instance_key

        element_id = self.element_id

        element_type = self.element_type.value

        tenant_id = self.tenant_id

        bpmn_process_id = self.bpmn_process_id

        details: dict[str, Any]
        if isinstance(self.details, JobWaitStateDetails):
            details = self.details.to_dict()
        elif isinstance(self.details, MessageWaitStateDetails):
            details = self.details.to_dict()
        elif isinstance(self.details, UserTaskWaitStateDetails):
            details = self.details.to_dict()
        elif isinstance(self.details, TimerWaitStateDetails):
            details = self.details.to_dict()
        elif isinstance(self.details, SignalWaitStateDetails):
            details = self.details.to_dict()
        else:
            details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rootProcessInstanceKey": root_process_instance_key,
                "processInstanceKey": process_instance_key,
                "elementInstanceKey": element_instance_key,
                "elementId": element_id,
                "elementType": element_type,
                "tenantId": tenant_id,
                "bpmnProcessId": bpmn_process_id,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.condition_wait_state_details import ConditionWaitStateDetails
        from ..models.job_wait_state_details import JobWaitStateDetails
        from ..models.message_wait_state_details import MessageWaitStateDetails
        from ..models.signal_wait_state_details import SignalWaitStateDetails
        from ..models.timer_wait_state_details import TimerWaitStateDetails
        from ..models.user_task_wait_state_details import UserTaskWaitStateDetails

        d = dict(src_dict)

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = (
            ProcessInstanceKey(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        process_instance_key = ProcessInstanceKey(d.pop("processInstanceKey"))

        element_instance_key = ElementInstanceKey(d.pop("elementInstanceKey"))

        element_id = ElementId(d.pop("elementId"))

        element_type = ElementInstanceWaitStateResultElementType(d.pop("elementType"))

        tenant_id = TenantId(d.pop("tenantId"))

        bpmn_process_id = d.pop("bpmnProcessId")

        def _parse_details(
            data: object,
        ) -> (
            ConditionWaitStateDetails
            | JobWaitStateDetails
            | MessageWaitStateDetails
            | SignalWaitStateDetails
            | TimerWaitStateDetails
            | UserTaskWaitStateDetails
        ):
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                details_type_0 = JobWaitStateDetails.from_dict(data)

                return details_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                details_type_1 = MessageWaitStateDetails.from_dict(data)

                return details_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                details_type_2 = UserTaskWaitStateDetails.from_dict(data)

                return details_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                details_type_3 = TimerWaitStateDetails.from_dict(data)

                return details_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                details_type_4 = SignalWaitStateDetails.from_dict(data)

                return details_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            details_type_5 = ConditionWaitStateDetails.from_dict(data)

            return details_type_5

        details = _parse_details(d.pop("details"))

        element_instance_wait_state_result = cls(
            root_process_instance_key=root_process_instance_key,
            process_instance_key=process_instance_key,
            element_instance_key=element_instance_key,
            element_id=element_id,
            element_type=element_type,
            tenant_id=tenant_id,
            bpmn_process_id=bpmn_process_id,
            details=details,
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
