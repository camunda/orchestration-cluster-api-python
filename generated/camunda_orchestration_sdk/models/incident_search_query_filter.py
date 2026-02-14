from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.incident_error_type_exact_match import IncidentErrorTypeExactMatch
from ..models.incident_state_exact_match import IncidentStateExactMatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
    from ..models.advanced_element_instance_key_filter import (
        AdvancedElementInstanceKeyFilter,
    )
    from ..models.advanced_incident_error_type_filter import (
        AdvancedIncidentErrorTypeFilter,
    )
    from ..models.advanced_incident_state_filter import AdvancedIncidentStateFilter
    from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
    from ..models.advanced_process_definition_key_filter import (
        AdvancedProcessDefinitionKeyFilter,
    )
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )
    from ..models.advanced_string_filter import AdvancedStringFilter
    from ..models.basic_string_filter import BasicStringFilter


T = TypeVar("T", bound="IncidentSearchQueryFilter")


@_attrs_define
class IncidentSearchQueryFilter:
    """The incident search filters.

    Attributes:
        process_definition_id (AdvancedStringFilter | str | Unset):
        error_type (AdvancedIncidentErrorTypeFilter | IncidentErrorTypeExactMatch | Unset):
        error_message (AdvancedStringFilter | str | Unset):
        element_id (AdvancedStringFilter | str | Unset):
        creation_time (AdvancedDateTimeFilter | datetime.datetime | Unset):
        state (AdvancedIncidentStateFilter | IncidentStateExactMatch | Unset):
        tenant_id (AdvancedStringFilter | str | Unset):
        incident_key (BasicStringFilter | str | Unset):
        process_definition_key (AdvancedProcessDefinitionKeyFilter | str | Unset):
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset):
        element_instance_key (AdvancedElementInstanceKeyFilter | str | Unset):
        job_key (AdvancedJobKeyFilter | str | Unset):
    """

    process_definition_id: AdvancedStringFilter | str | Unset = UNSET
    error_type: (
        AdvancedIncidentErrorTypeFilter | IncidentErrorTypeExactMatch | Unset
    ) = UNSET
    error_message: AdvancedStringFilter | str | Unset = UNSET
    element_id: AdvancedStringFilter | str | Unset = UNSET
    creation_time: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    state: AdvancedIncidentStateFilter | IncidentStateExactMatch | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    incident_key: BasicStringFilter | str | Unset = UNSET
    process_definition_key: AdvancedProcessDefinitionKeyFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    job_key: AdvancedJobKeyFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.basic_string_filter import BasicStringFilter

        process_definition_id: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_id, Unset):
            process_definition_id = UNSET
        elif isinstance(self.process_definition_id, AdvancedStringFilter):
            process_definition_id = self.process_definition_id.to_dict()
        else:
            process_definition_id = self.process_definition_id

        error_type: dict[str, Any] | str | Unset
        if isinstance(self.error_type, Unset):
            error_type = UNSET
        elif isinstance(self.error_type, IncidentErrorTypeExactMatch):
            error_type = self.error_type.value
        else:
            error_type = self.error_type.to_dict()

        error_message: dict[str, Any] | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        elif isinstance(self.error_message, AdvancedStringFilter):
            error_message = self.error_message.to_dict()
        else:
            error_message = self.error_message

        element_id: dict[str, Any] | str | Unset
        if isinstance(self.element_id, Unset):
            element_id = UNSET
        elif isinstance(self.element_id, AdvancedStringFilter):
            element_id = self.element_id.to_dict()
        else:
            element_id = self.element_id

        creation_time: dict[str, Any] | str | Unset
        if isinstance(self.creation_time, Unset):
            creation_time = UNSET
        elif isinstance(self.creation_time, datetime.datetime):
            creation_time = self.creation_time.isoformat()
        else:
            creation_time = self.creation_time.to_dict()

        state: dict[str, Any] | str | Unset
        if isinstance(self.state, Unset):
            state = UNSET
        elif isinstance(self.state, IncidentStateExactMatch):
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

        incident_key: dict[str, Any] | str | Unset
        if isinstance(self.incident_key, Unset):
            incident_key = UNSET
        elif isinstance(self.incident_key, BasicStringFilter):
            incident_key = self.incident_key.to_dict()
        else:
            incident_key = self.incident_key

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

        element_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.element_instance_key, Unset):
            element_instance_key = UNSET
        elif isinstance(self.element_instance_key, AdvancedElementInstanceKeyFilter):
            element_instance_key = self.element_instance_key.to_dict()
        else:
            element_instance_key = self.element_instance_key

        job_key: dict[str, Any] | str | Unset
        if isinstance(self.job_key, Unset):
            job_key = UNSET
        elif isinstance(self.job_key, AdvancedJobKeyFilter):
            job_key = self.job_key.to_dict()
        else:
            job_key = self.job_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if error_type is not UNSET:
            field_dict["errorType"] = error_type
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if creation_time is not UNSET:
            field_dict["creationTime"] = creation_time
        if state is not UNSET:
            field_dict["state"] = state
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if incident_key is not UNSET:
            field_dict["incidentKey"] = incident_key
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key
        if job_key is not UNSET:
            field_dict["jobKey"] = job_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_incident_error_type_filter import (
            AdvancedIncidentErrorTypeFilter,
        )
        from ..models.advanced_incident_state_filter import AdvancedIncidentStateFilter
        from ..models.advanced_job_key_filter import AdvancedJobKeyFilter
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.basic_string_filter import BasicStringFilter

        d = dict(src_dict)

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

        def _parse_error_type(
            data: object,
        ) -> AdvancedIncidentErrorTypeFilter | IncidentErrorTypeExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                error_type_type_0 = IncidentErrorTypeExactMatch(data)

                return error_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            error_type_type_1 = AdvancedIncidentErrorTypeFilter.from_dict(data)

            return error_type_type_1

        error_type = _parse_error_type(d.pop("errorType", UNSET))

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

        def _parse_state(
            data: object,
        ) -> AdvancedIncidentStateFilter | IncidentStateExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_type_0 = IncidentStateExactMatch(data)

                return state_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            state_type_1 = AdvancedIncidentStateFilter.from_dict(data)

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

        def _parse_incident_key(data: object) -> BasicStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                incident_key_type_1 = BasicStringFilter.from_dict(data)

                return incident_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BasicStringFilter | str | Unset, data)

        incident_key = _parse_incident_key(d.pop("incidentKey", UNSET))

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

        incident_search_query_filter = cls(
            process_definition_id=process_definition_id,
            error_type=error_type,
            error_message=error_message,
            element_id=element_id,
            creation_time=creation_time,
            state=state,
            tenant_id=tenant_id,
            incident_key=incident_key,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            element_instance_key=element_instance_key,
            job_key=job_key,
        )

        incident_search_query_filter.additional_properties = d
        return incident_search_query_filter

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
