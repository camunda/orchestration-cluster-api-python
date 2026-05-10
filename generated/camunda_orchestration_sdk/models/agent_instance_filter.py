from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_instance_status_exact_match import AgentInstanceStatusExactMatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_agent_instance_key_filter import (
        AdvancedAgentInstanceKeyFilter,
    )
    from ..models.advanced_agent_instance_status_filter import (
        AdvancedAgentInstanceStatusFilter,
    )
    from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
    from ..models.advanced_element_id_filter import AdvancedElementIdFilter
    from ..models.advanced_process_definition_key_filter import (
        AdvancedProcessDefinitionKeyFilter,
    )
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="AgentInstanceFilter")


@_attrs_define
class AgentInstanceFilter:
    """Agent instance search filter.

    Attributes:
        agent_instance_key (AdvancedAgentInstanceKeyFilter | str | Unset): The unique key of the agent instance.
        status (AdvancedAgentInstanceStatusFilter | AgentInstanceStatusExactMatch | Unset): The current status of the
            agent instance.
        element_id (AdvancedElementIdFilter | str | Unset): The BPMN element ID of the agent task.
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset): The key of the process instance that owns
            this agent instance.
        process_definition_key (AdvancedProcessDefinitionKeyFilter | str | Unset): The key of the process definition
            associated with this agent instance.
        tenant_id (AdvancedStringFilter | str | Unset): The tenant ID of the agent instance.
        creation_date (AdvancedDateTimeFilter | datetime.datetime | Unset): The creation date of the agent instance.
        last_updated_date (AdvancedDateTimeFilter | datetime.datetime | Unset): The date the agent instance was last
            updated.
        completion_date (AdvancedDateTimeFilter | datetime.datetime | Unset): The completion date of the agent instance.
    """

    agent_instance_key: AdvancedAgentInstanceKeyFilter | str | Unset = UNSET
    status: (
        AdvancedAgentInstanceStatusFilter | AgentInstanceStatusExactMatch | Unset
    ) = UNSET
    element_id: AdvancedElementIdFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    process_definition_key: AdvancedProcessDefinitionKeyFilter | str | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    creation_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    last_updated_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    completion_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_agent_instance_key_filter import (
            AdvancedAgentInstanceKeyFilter,
        )
        from ..models.advanced_element_id_filter import AdvancedElementIdFilter
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter

        agent_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.agent_instance_key, Unset):
            agent_instance_key = UNSET
        elif isinstance(self.agent_instance_key, AdvancedAgentInstanceKeyFilter):
            agent_instance_key = self.agent_instance_key.to_dict()
        else:
            agent_instance_key = self.agent_instance_key

        status: dict[str, Any] | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, AgentInstanceStatusExactMatch):
            status = self.status.value
        else:
            status = self.status.to_dict()

        element_id: dict[str, Any] | str | Unset
        if isinstance(self.element_id, Unset):
            element_id = UNSET
        elif isinstance(self.element_id, AdvancedElementIdFilter):
            element_id = self.element_id.to_dict()
        else:
            element_id = self.element_id

        process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.process_instance_key, Unset):
            process_instance_key = UNSET
        elif isinstance(self.process_instance_key, AdvancedProcessInstanceKeyFilter):
            process_instance_key = self.process_instance_key.to_dict()
        else:
            process_instance_key = self.process_instance_key

        process_definition_key: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_key, Unset):
            process_definition_key = UNSET
        elif isinstance(
            self.process_definition_key, AdvancedProcessDefinitionKeyFilter
        ):
            process_definition_key = self.process_definition_key.to_dict()
        else:
            process_definition_key = self.process_definition_key

        tenant_id: dict[str, Any] | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        elif isinstance(self.tenant_id, AdvancedStringFilter):
            tenant_id = self.tenant_id.to_dict()
        else:
            tenant_id = self.tenant_id

        creation_date: dict[str, Any] | str | Unset
        if isinstance(self.creation_date, Unset):
            creation_date = UNSET
        elif isinstance(self.creation_date, datetime.datetime):
            creation_date = self.creation_date.isoformat()
        else:
            creation_date = self.creation_date.to_dict()

        last_updated_date: dict[str, Any] | str | Unset
        if isinstance(self.last_updated_date, Unset):
            last_updated_date = UNSET
        elif isinstance(self.last_updated_date, datetime.datetime):
            last_updated_date = self.last_updated_date.isoformat()
        else:
            last_updated_date = self.last_updated_date.to_dict()

        completion_date: dict[str, Any] | str | Unset
        if isinstance(self.completion_date, Unset):
            completion_date = UNSET
        elif isinstance(self.completion_date, datetime.datetime):
            completion_date = self.completion_date.isoformat()
        else:
            completion_date = self.completion_date.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_instance_key is not UNSET:
            field_dict["agentInstanceKey"] = agent_instance_key
        if status is not UNSET:
            field_dict["status"] = status
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if last_updated_date is not UNSET:
            field_dict["lastUpdatedDate"] = last_updated_date
        if completion_date is not UNSET:
            field_dict["completionDate"] = completion_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_agent_instance_key_filter import (
            AdvancedAgentInstanceKeyFilter,
        )
        from ..models.advanced_agent_instance_status_filter import (
            AdvancedAgentInstanceStatusFilter,
        )
        from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
        from ..models.advanced_element_id_filter import AdvancedElementIdFilter
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)

        def _parse_agent_instance_key(
            data: object,
        ) -> AdvancedAgentInstanceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                agent_instance_key_type_1 = AdvancedAgentInstanceKeyFilter.from_dict(
                    data
                )

                return agent_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedAgentInstanceKeyFilter | str | Unset, data)

        agent_instance_key = _parse_agent_instance_key(d.pop("agentInstanceKey", UNSET))

        def _parse_status(
            data: object,
        ) -> AdvancedAgentInstanceStatusFilter | AgentInstanceStatusExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = AgentInstanceStatusExactMatch(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            status_type_1 = AdvancedAgentInstanceStatusFilter.from_dict(data)

            return status_type_1

        status = _parse_status(d.pop("status", UNSET))

        def _parse_element_id(data: object) -> AdvancedElementIdFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                element_id_type_1 = AdvancedElementIdFilter.from_dict(data)

                return element_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedElementIdFilter | str | Unset, data)

        element_id = _parse_element_id(d.pop("elementId", UNSET))

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

        def _parse_creation_date(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                creation_date_type_0 = isoparse(data)

                return creation_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            creation_date_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return creation_date_type_1

        creation_date = _parse_creation_date(d.pop("creationDate", UNSET))

        def _parse_last_updated_date(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_updated_date_type_0 = isoparse(data)

                return last_updated_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            last_updated_date_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return last_updated_date_type_1

        last_updated_date = _parse_last_updated_date(d.pop("lastUpdatedDate", UNSET))

        def _parse_completion_date(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completion_date_type_0 = isoparse(data)

                return completion_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            completion_date_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return completion_date_type_1

        completion_date = _parse_completion_date(d.pop("completionDate", UNSET))

        agent_instance_filter = cls(
            agent_instance_key=agent_instance_key,
            status=status,
            element_id=element_id,
            process_instance_key=process_instance_key,
            process_definition_key=process_definition_key,
            tenant_id=tenant_id,
            creation_date=creation_date,
            last_updated_date=last_updated_date,
            completion_date=completion_date,
        )

        agent_instance_filter.additional_properties = d
        return agent_instance_filter

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
