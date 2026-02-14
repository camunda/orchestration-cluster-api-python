from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.element_instance_state_exact_match import ElementInstanceStateExactMatch
from ..models.process_instance_state_exact_match import ProcessInstanceStateExactMatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
    from ..models.advanced_element_instance_key_filter import (
        AdvancedElementInstanceKeyFilter,
    )
    from ..models.advanced_element_instance_state_filter import (
        AdvancedElementInstanceStateFilter,
    )
    from ..models.advanced_integer_filter import AdvancedIntegerFilter
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )
    from ..models.advanced_process_instance_state_filter import (
        AdvancedProcessInstanceStateFilter,
    )
    from ..models.advanced_string_filter import AdvancedStringFilter
    from ..models.base_process_instance_filter_fields import (
        BaseProcessInstanceFilterFields,
    )
    from ..models.variable_value_filter_property import VariableValueFilterProperty


T = TypeVar("T", bound="ProcessDefinitionElementStatisticsQueryFilter")


@_attrs_define
class ProcessDefinitionElementStatisticsQueryFilter:
    """The process definition statistics search filters.

    Attributes:
        start_date (AdvancedDateTimeFilter | datetime.datetime | Unset):
        end_date (AdvancedDateTimeFilter | datetime.datetime | Unset):
        state (AdvancedProcessInstanceStateFilter | ProcessInstanceStateExactMatch | Unset):
        has_incident (bool | Unset): Whether this process instance has a related incident or not.
        tenant_id (AdvancedStringFilter | str | Unset):
        variables (list[VariableValueFilterProperty] | Unset): The process instance variables.
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset):
        parent_process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset):
        parent_element_instance_key (AdvancedElementInstanceKeyFilter | str | Unset):
        batch_operation_id (AdvancedStringFilter | str | Unset):
        error_message (AdvancedStringFilter | str | Unset):
        has_retries_left (bool | Unset): Whether the process has failed jobs with retries left.
        element_instance_state (AdvancedElementInstanceStateFilter | ElementInstanceStateExactMatch | Unset):
        element_id (AdvancedStringFilter | str | Unset):
        has_element_instance_incident (bool | Unset): Whether the element instance has an incident or not.
        incident_error_hash_code (AdvancedIntegerFilter | int | Unset):
        tags (list[str] | Unset): List of tags. Tags need to start with a letter; then alphanumerics, `_`, `-`, `:`, or
            `.`; length ≤ 100. Example: ['high-touch', 'remediation'].
        or_ (list[BaseProcessInstanceFilterFields] | Unset): Defines a list of alternative filter groups combined using
            OR logic. Each object in the array is evaluated independently, and the filter matches if any one of them is
            satisfied.

            Top-level fields and the `$or` clause are combined using AND logic — meaning: (top-level filters) AND (any of
            the `$or` filters) must match.
            <br>
            <em>Example:</em>

            ```json
            {
              "state": "ACTIVE",
              "tenantId": 123,
              "$or": [
                { "processDefinitionId": "process_v1" },
                { "processDefinitionId": "process_v2", "hasIncident": true }
              ]
            }
            ```
            This matches process instances that:

            <ul style="padding-left: 20px; margin-left: 20px;">
              <li style="list-style-type: disc;">are in <em>ACTIVE</em> state</li>
              <li style="list-style-type: disc;">have tenant id equal to <em>123</em></li>
              <li style="list-style-type: disc;">and match either:
                <ul style="padding-left: 20px; margin-left: 20px;">
                  <li style="list-style-type: circle;"><code>processDefinitionId</code> is <em>process_v1</em>, or</li>
                  <li style="list-style-type: circle;"><code>processDefinitionId</code> is <em>process_v2</em> and
            <code>hasIncident</code> is <em>true</em></li>
                </ul>
              </li>
            </ul>
            <br>
            <p>Note: Using complex <code>$or</code> conditions may impact performance, use with caution in high-volume
            environments.
    """

    start_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    end_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    state: (
        AdvancedProcessInstanceStateFilter | ProcessInstanceStateExactMatch | Unset
    ) = UNSET
    has_incident: bool | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    variables: list[VariableValueFilterProperty] | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    parent_process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    parent_element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    batch_operation_id: AdvancedStringFilter | str | Unset = UNSET
    error_message: AdvancedStringFilter | str | Unset = UNSET
    has_retries_left: bool | Unset = UNSET
    element_instance_state: (
        AdvancedElementInstanceStateFilter | ElementInstanceStateExactMatch | Unset
    ) = UNSET
    element_id: AdvancedStringFilter | str | Unset = UNSET
    has_element_instance_incident: bool | Unset = UNSET
    incident_error_hash_code: AdvancedIntegerFilter | int | Unset = UNSET
    tags: list[str] | Unset = UNSET
    or_: list[BaseProcessInstanceFilterFields] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter

        start_date: dict[str, Any] | str | Unset
        if isinstance(self.start_date, Unset):
            start_date = UNSET
        elif isinstance(self.start_date, datetime.datetime):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date.to_dict()

        end_date: dict[str, Any] | str | Unset
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.datetime):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date.to_dict()

        state: dict[str, Any] | str | Unset
        if isinstance(self.state, Unset):
            state = UNSET
        elif isinstance(self.state, ProcessInstanceStateExactMatch):
            state = self.state.value
        else:
            state = self.state.to_dict()

        has_incident = self.has_incident

        tenant_id: dict[str, Any] | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        elif isinstance(self.tenant_id, AdvancedStringFilter):
            tenant_id = self.tenant_id.to_dict()
        else:
            tenant_id = self.tenant_id

        variables: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.variables, Unset):
            variables = []
            for variables_item_data in self.variables:
                variables_item = variables_item_data.to_dict()
                variables.append(variables_item)

        process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.process_instance_key, Unset):
            process_instance_key = UNSET
        elif isinstance(self.process_instance_key, AdvancedProcessInstanceKeyFilter):
            process_instance_key = self.process_instance_key.to_dict()
        else:
            process_instance_key = self.process_instance_key

        parent_process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.parent_process_instance_key, Unset):
            parent_process_instance_key = UNSET
        elif isinstance(
            self.parent_process_instance_key, AdvancedProcessInstanceKeyFilter
        ):
            parent_process_instance_key = self.parent_process_instance_key.to_dict()
        else:
            parent_process_instance_key = self.parent_process_instance_key

        parent_element_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.parent_element_instance_key, Unset):
            parent_element_instance_key = UNSET
        elif isinstance(
            self.parent_element_instance_key, AdvancedElementInstanceKeyFilter
        ):
            parent_element_instance_key = self.parent_element_instance_key.to_dict()
        else:
            parent_element_instance_key = self.parent_element_instance_key

        batch_operation_id: dict[str, Any] | str | Unset
        if isinstance(self.batch_operation_id, Unset):
            batch_operation_id = UNSET
        elif isinstance(self.batch_operation_id, AdvancedStringFilter):
            batch_operation_id = self.batch_operation_id.to_dict()
        else:
            batch_operation_id = self.batch_operation_id

        error_message: dict[str, Any] | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        elif isinstance(self.error_message, AdvancedStringFilter):
            error_message = self.error_message.to_dict()
        else:
            error_message = self.error_message

        has_retries_left = self.has_retries_left

        element_instance_state: dict[str, Any] | str | Unset
        if isinstance(self.element_instance_state, Unset):
            element_instance_state = UNSET
        elif isinstance(self.element_instance_state, ElementInstanceStateExactMatch):
            element_instance_state = self.element_instance_state.value
        else:
            element_instance_state = self.element_instance_state.to_dict()

        element_id: dict[str, Any] | str | Unset
        if isinstance(self.element_id, Unset):
            element_id = UNSET
        elif isinstance(self.element_id, AdvancedStringFilter):
            element_id = self.element_id.to_dict()
        else:
            element_id = self.element_id

        has_element_instance_incident = self.has_element_instance_incident

        incident_error_hash_code: dict[str, Any] | int | Unset
        if isinstance(self.incident_error_hash_code, Unset):
            incident_error_hash_code = UNSET
        elif isinstance(self.incident_error_hash_code, AdvancedIntegerFilter):
            incident_error_hash_code = self.incident_error_hash_code.to_dict()
        else:
            incident_error_hash_code = self.incident_error_hash_code

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        or_: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.or_, Unset):
            or_ = []
            for or_item_data in self.or_:
                or_item = or_item_data.to_dict()
                or_.append(or_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if state is not UNSET:
            field_dict["state"] = state
        if has_incident is not UNSET:
            field_dict["hasIncident"] = has_incident
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if variables is not UNSET:
            field_dict["variables"] = variables
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if parent_process_instance_key is not UNSET:
            field_dict["parentProcessInstanceKey"] = parent_process_instance_key
        if parent_element_instance_key is not UNSET:
            field_dict["parentElementInstanceKey"] = parent_element_instance_key
        if batch_operation_id is not UNSET:
            field_dict["batchOperationId"] = batch_operation_id
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if has_retries_left is not UNSET:
            field_dict["hasRetriesLeft"] = has_retries_left
        if element_instance_state is not UNSET:
            field_dict["elementInstanceState"] = element_instance_state
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if has_element_instance_incident is not UNSET:
            field_dict["hasElementInstanceIncident"] = has_element_instance_incident
        if incident_error_hash_code is not UNSET:
            field_dict["incidentErrorHashCode"] = incident_error_hash_code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if or_ is not UNSET:
            field_dict["$or"] = or_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_element_instance_state_filter import (
            AdvancedElementInstanceStateFilter,
        )
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_process_instance_state_filter import (
            AdvancedProcessInstanceStateFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.base_process_instance_filter_fields import (
            BaseProcessInstanceFilterFields,
        )
        from ..models.variable_value_filter_property import VariableValueFilterProperty

        d = dict(src_dict)

        def _parse_start_date(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data)

                return start_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            start_date_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return start_date_type_1

        start_date = _parse_start_date(d.pop("startDate", UNSET))

        def _parse_end_date(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data)

                return end_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            end_date_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return end_date_type_1

        end_date = _parse_end_date(d.pop("endDate", UNSET))

        def _parse_state(
            data: object,
        ) -> (
            AdvancedProcessInstanceStateFilter | ProcessInstanceStateExactMatch | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_type_0 = ProcessInstanceStateExactMatch(data)

                return state_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            state_type_1 = AdvancedProcessInstanceStateFilter.from_dict(data)

            return state_type_1

        state = _parse_state(d.pop("state", UNSET))

        has_incident = d.pop("hasIncident", UNSET)

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

        _variables = d.pop("variables", UNSET)
        variables: list[VariableValueFilterProperty] | Unset = UNSET
        if _variables is not UNSET:
            variables = []
            for variables_item_data in _variables:
                variables_item = VariableValueFilterProperty.from_dict(
                    variables_item_data
                )

                variables.append(variables_item)

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

        def _parse_parent_process_instance_key(
            data: object,
        ) -> AdvancedProcessInstanceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                parent_process_instance_key_type_1 = (
                    AdvancedProcessInstanceKeyFilter.from_dict(data)
                )

                return parent_process_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedProcessInstanceKeyFilter | str | Unset, data)

        parent_process_instance_key = _parse_parent_process_instance_key(
            d.pop("parentProcessInstanceKey", UNSET)
        )

        def _parse_parent_element_instance_key(
            data: object,
        ) -> AdvancedElementInstanceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                parent_element_instance_key_type_1 = (
                    AdvancedElementInstanceKeyFilter.from_dict(data)
                )

                return parent_element_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedElementInstanceKeyFilter | str | Unset, data)

        parent_element_instance_key = _parse_parent_element_instance_key(
            d.pop("parentElementInstanceKey", UNSET)
        )

        def _parse_batch_operation_id(
            data: object,
        ) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                batch_operation_id_type_1 = AdvancedStringFilter.from_dict(data)

                return batch_operation_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        batch_operation_id = _parse_batch_operation_id(d.pop("batchOperationId", UNSET))

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

        has_retries_left = d.pop("hasRetriesLeft", UNSET)

        def _parse_element_instance_state(
            data: object,
        ) -> (
            AdvancedElementInstanceStateFilter | ElementInstanceStateExactMatch | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                element_instance_state_type_0 = ElementInstanceStateExactMatch(data)

                return element_instance_state_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            element_instance_state_type_1 = (
                AdvancedElementInstanceStateFilter.from_dict(data)
            )

            return element_instance_state_type_1

        element_instance_state = _parse_element_instance_state(
            d.pop("elementInstanceState", UNSET)
        )

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

        has_element_instance_incident = d.pop("hasElementInstanceIncident", UNSET)

        def _parse_incident_error_hash_code(
            data: object,
        ) -> AdvancedIntegerFilter | int | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                incident_error_hash_code_type_1 = AdvancedIntegerFilter.from_dict(data)

                return incident_error_hash_code_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedIntegerFilter | int | Unset, data)

        incident_error_hash_code = _parse_incident_error_hash_code(
            d.pop("incidentErrorHashCode", UNSET)
        )

        tags = cast(list[str], d.pop("tags", UNSET))

        _or_ = d.pop("$or", UNSET)
        or_: list[BaseProcessInstanceFilterFields] | Unset = UNSET
        if _or_ is not UNSET:
            or_ = []
            for or_item_data in _or_:
                or_item = BaseProcessInstanceFilterFields.from_dict(or_item_data)

                or_.append(or_item)

        process_definition_element_statistics_query_filter = cls(
            start_date=start_date,
            end_date=end_date,
            state=state,
            has_incident=has_incident,
            tenant_id=tenant_id,
            variables=variables,
            process_instance_key=process_instance_key,
            parent_process_instance_key=parent_process_instance_key,
            parent_element_instance_key=parent_element_instance_key,
            batch_operation_id=batch_operation_id,
            error_message=error_message,
            has_retries_left=has_retries_left,
            element_instance_state=element_instance_state,
            element_id=element_id,
            has_element_instance_incident=has_element_instance_incident,
            incident_error_hash_code=incident_error_hash_code,
            tags=tags,
            or_=or_,
        )

        process_definition_element_statistics_query_filter.additional_properties = d
        return process_definition_element_statistics_query_filter

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
