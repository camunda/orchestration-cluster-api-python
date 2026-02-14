from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_kind_exact_match import JobKindExactMatch
from ..models.job_listener_event_type_exact_match import JobListenerEventTypeExactMatch
from ..models.job_state_exact_match import JobStateExactMatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
    from ..models.advanced_element_instance_key_filter import (
        AdvancedElementInstanceKeyFilter,
    )
    from ..models.advanced_integer_filter import AdvancedIntegerFilter
    from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
    from ..models.advanced_job_kind_filter import AdvancedJobKindFilter
    from ..models.advanced_job_listener_event_type_filter import (
        AdvancedJobListenerEventTypeFilter,
    )
    from ..models.advanced_job_state_filter import AdvancedJobStateFilter
    from ..models.advanced_process_definition_key_filter import (
        AdvancedProcessDefinitionKeyFilter,
    )
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="JobSearchQueryFilter")


@_attrs_define
class JobSearchQueryFilter:
    """The job search filters.

    Attributes:
        deadline (AdvancedDateTimeFilter | datetime.datetime | None | Unset):
        denied_reason (AdvancedStringFilter | str | Unset):
        element_id (AdvancedStringFilter | str | Unset):
        element_instance_key (AdvancedElementInstanceKeyFilter | str | Unset):
        end_time (AdvancedDateTimeFilter | datetime.datetime | Unset):
        error_code (AdvancedStringFilter | str | Unset):
        error_message (AdvancedStringFilter | str | Unset):
        has_failed_with_retries_left (bool | Unset): Indicates whether the job has failed with retries left.
        is_denied (bool | None | Unset): Indicates whether the user task listener denies the work.
        job_key (AdvancedJobKeyFilter | str | Unset):
        kind (AdvancedJobKindFilter | JobKindExactMatch | Unset):
        listener_event_type (AdvancedJobListenerEventTypeFilter | JobListenerEventTypeExactMatch | Unset):
        process_definition_id (AdvancedStringFilter | str | Unset):
        process_definition_key (AdvancedProcessDefinitionKeyFilter | str | Unset):
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset):
        retries (AdvancedIntegerFilter | int | Unset):
        state (AdvancedJobStateFilter | JobStateExactMatch | Unset):
        tenant_id (AdvancedStringFilter | str | Unset):
        type_ (AdvancedStringFilter | str | Unset):
        worker (AdvancedStringFilter | str | Unset):
        creation_time (AdvancedDateTimeFilter | datetime.datetime | Unset):
        last_update_time (AdvancedDateTimeFilter | datetime.datetime | Unset):
    """

    deadline: AdvancedDateTimeFilter | datetime.datetime | None | Unset = UNSET
    denied_reason: AdvancedStringFilter | str | Unset = UNSET
    element_id: AdvancedStringFilter | str | Unset = UNSET
    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    end_time: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    error_code: AdvancedStringFilter | str | Unset = UNSET
    error_message: AdvancedStringFilter | str | Unset = UNSET
    has_failed_with_retries_left: bool | Unset = UNSET
    is_denied: bool | None | Unset = UNSET
    job_key: AdvancedJobKeyFilter | str | Unset = UNSET
    kind: AdvancedJobKindFilter | JobKindExactMatch | Unset = UNSET
    listener_event_type: (
        AdvancedJobListenerEventTypeFilter | JobListenerEventTypeExactMatch | Unset
    ) = UNSET
    process_definition_id: AdvancedStringFilter | str | Unset = UNSET
    process_definition_key: AdvancedProcessDefinitionKeyFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    retries: AdvancedIntegerFilter | int | Unset = UNSET
    state: AdvancedJobStateFilter | JobStateExactMatch | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    type_: AdvancedStringFilter | str | Unset = UNSET
    worker: AdvancedStringFilter | str | Unset = UNSET
    creation_time: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    last_update_time: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter

        deadline: dict[str, Any] | None | str | Unset
        if isinstance(self.deadline, Unset):
            deadline = UNSET
        elif isinstance(self.deadline, datetime.datetime):
            deadline = self.deadline.isoformat()
        elif isinstance(self.deadline, AdvancedDateTimeFilter):
            deadline = self.deadline.to_dict()
        else:
            deadline = self.deadline

        denied_reason: dict[str, Any] | str | Unset
        if isinstance(self.denied_reason, Unset):
            denied_reason = UNSET
        elif isinstance(self.denied_reason, AdvancedStringFilter):
            denied_reason = self.denied_reason.to_dict()
        else:
            denied_reason = self.denied_reason

        element_id: dict[str, Any] | str | Unset
        if isinstance(self.element_id, Unset):
            element_id = UNSET
        elif isinstance(self.element_id, AdvancedStringFilter):
            element_id = self.element_id.to_dict()
        else:
            element_id = self.element_id

        element_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.element_instance_key, Unset):
            element_instance_key = UNSET
        elif isinstance(self.element_instance_key, AdvancedElementInstanceKeyFilter):
            element_instance_key = self.element_instance_key.to_dict()
        else:
            element_instance_key = self.element_instance_key

        end_time: dict[str, Any] | str | Unset
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        elif isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time.to_dict()

        error_code: dict[str, Any] | str | Unset
        if isinstance(self.error_code, Unset):
            error_code = UNSET
        elif isinstance(self.error_code, AdvancedStringFilter):
            error_code = self.error_code.to_dict()
        else:
            error_code = self.error_code

        error_message: dict[str, Any] | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        elif isinstance(self.error_message, AdvancedStringFilter):
            error_message = self.error_message.to_dict()
        else:
            error_message = self.error_message

        has_failed_with_retries_left = self.has_failed_with_retries_left

        is_denied: bool | None | Unset
        if isinstance(self.is_denied, Unset):
            is_denied = UNSET
        else:
            is_denied = self.is_denied

        job_key: dict[str, Any] | str | Unset
        if isinstance(self.job_key, Unset):
            job_key = UNSET
        elif isinstance(self.job_key, AdvancedJobKeyFilter):
            job_key = self.job_key.to_dict()
        else:
            job_key = self.job_key

        kind: dict[str, Any] | str | Unset
        if isinstance(self.kind, Unset):
            kind = UNSET
        elif isinstance(self.kind, JobKindExactMatch):
            kind = self.kind.value
        else:
            kind = self.kind.to_dict()

        listener_event_type: dict[str, Any] | str | Unset
        if isinstance(self.listener_event_type, Unset):
            listener_event_type = UNSET
        elif isinstance(self.listener_event_type, JobListenerEventTypeExactMatch):
            listener_event_type = self.listener_event_type.value
        else:
            listener_event_type = self.listener_event_type.to_dict()

        process_definition_id: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_id, Unset):
            process_definition_id = UNSET
        elif isinstance(self.process_definition_id, AdvancedStringFilter):
            process_definition_id = self.process_definition_id.to_dict()
        else:
            process_definition_id = self.process_definition_id

        process_definition_key: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_key, Unset):
            process_definition_key = UNSET
        elif isinstance(
            self.process_definition_key, AdvancedProcessDefinitionKeyFilter
        ):
            process_definition_key = self.process_definition_key.to_dict()
        else:
            process_definition_key = self.process_definition_key

        process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.process_instance_key, Unset):
            process_instance_key = UNSET
        elif isinstance(self.process_instance_key, AdvancedProcessInstanceKeyFilter):
            process_instance_key = self.process_instance_key.to_dict()
        else:
            process_instance_key = self.process_instance_key

        retries: dict[str, Any] | int | Unset
        if isinstance(self.retries, Unset):
            retries = UNSET
        elif isinstance(self.retries, AdvancedIntegerFilter):
            retries = self.retries.to_dict()
        else:
            retries = self.retries

        state: dict[str, Any] | str | Unset
        if isinstance(self.state, Unset):
            state = UNSET
        elif isinstance(self.state, JobStateExactMatch):
            state = self.state.value
        else:
            state = self.state.to_dict()

        tenant_id: dict[str, Any] | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        elif isinstance(self.tenant_id, AdvancedStringFilter):
            tenant_id = self.tenant_id.to_dict()
        else:
            tenant_id = self.tenant_id

        type_: dict[str, Any] | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        elif isinstance(self.type_, AdvancedStringFilter):
            type_ = self.type_.to_dict()
        else:
            type_ = self.type_

        worker: dict[str, Any] | str | Unset
        if isinstance(self.worker, Unset):
            worker = UNSET
        elif isinstance(self.worker, AdvancedStringFilter):
            worker = self.worker.to_dict()
        else:
            worker = self.worker

        creation_time: dict[str, Any] | str | Unset
        if isinstance(self.creation_time, Unset):
            creation_time = UNSET
        elif isinstance(self.creation_time, datetime.datetime):
            creation_time = self.creation_time.isoformat()
        else:
            creation_time = self.creation_time.to_dict()

        last_update_time: dict[str, Any] | str | Unset
        if isinstance(self.last_update_time, Unset):
            last_update_time = UNSET
        elif isinstance(self.last_update_time, datetime.datetime):
            last_update_time = self.last_update_time.isoformat()
        else:
            last_update_time = self.last_update_time.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deadline is not UNSET:
            field_dict["deadline"] = deadline
        if denied_reason is not UNSET:
            field_dict["deniedReason"] = denied_reason
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if has_failed_with_retries_left is not UNSET:
            field_dict["hasFailedWithRetriesLeft"] = has_failed_with_retries_left
        if is_denied is not UNSET:
            field_dict["isDenied"] = is_denied
        if job_key is not UNSET:
            field_dict["jobKey"] = job_key
        if kind is not UNSET:
            field_dict["kind"] = kind
        if listener_event_type is not UNSET:
            field_dict["listenerEventType"] = listener_event_type
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if retries is not UNSET:
            field_dict["retries"] = retries
        if state is not UNSET:
            field_dict["state"] = state
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if worker is not UNSET:
            field_dict["worker"] = worker
        if creation_time is not UNSET:
            field_dict["creationTime"] = creation_time
        if last_update_time is not UNSET:
            field_dict["lastUpdateTime"] = last_update_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
        from ..models.advanced_job_kind_filter import AdvancedJobKindFilter
        from ..models.advanced_job_listener_event_type_filter import (
            AdvancedJobListenerEventTypeFilter,
        )
        from ..models.advanced_job_state_filter import AdvancedJobStateFilter
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)

        def _parse_deadline(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deadline_type_0 = isoparse(data)

                return deadline_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                deadline_type_1 = AdvancedDateTimeFilter.from_dict(data)

                return deadline_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedDateTimeFilter | datetime.datetime | None | Unset, data)

        deadline = _parse_deadline(d.pop("deadline", UNSET))

        def _parse_denied_reason(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                denied_reason_type_1 = AdvancedStringFilter.from_dict(data)

                return denied_reason_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        denied_reason = _parse_denied_reason(d.pop("deniedReason", UNSET))

        def _parse_element_id(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                element_id_type_1 = AdvancedStringFilter.from_dict(data)

                return element_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        element_id = _parse_element_id(d.pop("elementId", UNSET))

        def _parse_element_instance_key(
            data: object,
        ) -> AdvancedElementInstanceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                element_instance_key_type_1 = (
                    AdvancedElementInstanceKeyFilter.from_dict(data)
                )

                return element_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedElementInstanceKeyFilter | str | Unset, data)

        element_instance_key = _parse_element_instance_key(
            d.pop("elementInstanceKey", UNSET)
        )

        def _parse_end_time(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0 = isoparse(data)

                return end_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            end_time_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return end_time_type_1

        end_time = _parse_end_time(d.pop("endTime", UNSET))

        def _parse_error_code(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                error_code_type_1 = AdvancedStringFilter.from_dict(data)

                return error_code_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        error_code = _parse_error_code(d.pop("errorCode", UNSET))

        def _parse_error_message(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                error_message_type_1 = AdvancedStringFilter.from_dict(data)

                return error_message_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        error_message = _parse_error_message(d.pop("errorMessage", UNSET))

        has_failed_with_retries_left = d.pop("hasFailedWithRetriesLeft", UNSET)

        def _parse_is_denied(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_denied = _parse_is_denied(d.pop("isDenied", UNSET))

        def _parse_job_key(data: object) -> AdvancedJobKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                job_key_type_1 = AdvancedJobKeyFilter.from_dict(data)

                return job_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedJobKeyFilter | str | Unset, data)

        job_key = _parse_job_key(d.pop("jobKey", UNSET))

        def _parse_kind(
            data: object,
        ) -> AdvancedJobKindFilter | JobKindExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                kind_type_0 = JobKindExactMatch(data)

                return kind_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            kind_type_1 = AdvancedJobKindFilter.from_dict(data)

            return kind_type_1

        kind = _parse_kind(d.pop("kind", UNSET))

        def _parse_listener_event_type(
            data: object,
        ) -> (
            AdvancedJobListenerEventTypeFilter | JobListenerEventTypeExactMatch | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                listener_event_type_type_0 = JobListenerEventTypeExactMatch(data)

                return listener_event_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            listener_event_type_type_1 = AdvancedJobListenerEventTypeFilter.from_dict(
                data
            )

            return listener_event_type_type_1

        listener_event_type = _parse_listener_event_type(
            d.pop("listenerEventType", UNSET)
        )

        def _parse_process_definition_id(
            data: object,
        ) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_id_type_1 = AdvancedStringFilter.from_dict(data)

                return process_definition_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        process_definition_id = _parse_process_definition_id(
            d.pop("processDefinitionId", UNSET)
        )

        def _parse_process_definition_key(
            data: object,
        ) -> AdvancedProcessDefinitionKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_key_type_1 = (
                    AdvancedProcessDefinitionKeyFilter.from_dict(data)
                )

                return process_definition_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedProcessDefinitionKeyFilter | str | Unset, data)

        process_definition_key = _parse_process_definition_key(
            d.pop("processDefinitionKey", UNSET)
        )

        def _parse_process_instance_key(
            data: object,
        ) -> AdvancedProcessInstanceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_instance_key_type_1 = (
                    AdvancedProcessInstanceKeyFilter.from_dict(data)
                )

                return process_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedProcessInstanceKeyFilter | str | Unset, data)

        process_instance_key = _parse_process_instance_key(
            d.pop("processInstanceKey", UNSET)
        )

        def _parse_retries(data: object) -> AdvancedIntegerFilter | int | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                retries_type_1 = AdvancedIntegerFilter.from_dict(data)

                return retries_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedIntegerFilter | int | Unset, data)

        retries = _parse_retries(d.pop("retries", UNSET))

        def _parse_state(
            data: object,
        ) -> AdvancedJobStateFilter | JobStateExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_type_0 = JobStateExactMatch(data)

                return state_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            state_type_1 = AdvancedJobStateFilter.from_dict(data)

            return state_type_1

        state = _parse_state(d.pop("state", UNSET))

        def _parse_tenant_id(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                tenant_id_type_1 = AdvancedStringFilter.from_dict(data)

                return tenant_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        tenant_id = _parse_tenant_id(d.pop("tenantId", UNSET))

        def _parse_type_(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                type_type_1 = AdvancedStringFilter.from_dict(data)

                return type_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_worker(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                worker_type_1 = AdvancedStringFilter.from_dict(data)

                return worker_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        worker = _parse_worker(d.pop("worker", UNSET))

        def _parse_creation_time(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                creation_time_type_0 = isoparse(data)

                return creation_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            creation_time_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return creation_time_type_1

        creation_time = _parse_creation_time(d.pop("creationTime", UNSET))

        def _parse_last_update_time(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_update_time_type_0 = isoparse(data)

                return last_update_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            last_update_time_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return last_update_time_type_1

        last_update_time = _parse_last_update_time(d.pop("lastUpdateTime", UNSET))

        job_search_query_filter = cls(
            deadline=deadline,
            denied_reason=denied_reason,
            element_id=element_id,
            element_instance_key=element_instance_key,
            end_time=end_time,
            error_code=error_code,
            error_message=error_message,
            has_failed_with_retries_left=has_failed_with_retries_left,
            is_denied=is_denied,
            job_key=job_key,
            kind=kind,
            listener_event_type=listener_event_type,
            process_definition_id=process_definition_id,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            retries=retries,
            state=state,
            tenant_id=tenant_id,
            type_=type_,
            worker=worker,
            creation_time=creation_time,
            last_update_time=last_update_time,
        )

        job_search_query_filter.additional_properties = d
        return job_search_query_filter

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
