from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.variable_history_item_actor_type_exact_match import (
    VariableHistoryItemActorTypeExactMatch,
)
from ..models.variable_history_item_operation_type_exact_match import (
    VariableHistoryItemOperationTypeExactMatch,
)
from ..models.variable_history_item_variable_operation_type_exact_match import (
    VariableHistoryItemVariableOperationTypeExactMatch,
)
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
    from ..models.advanced_element_id_filter import AdvancedElementIdFilter
    from ..models.advanced_element_instance_key_filter import (
        AdvancedElementInstanceKeyFilter,
    )
    from ..models.advanced_process_definition_id_filter import (
        AdvancedProcessDefinitionIdFilter,
    )
    from ..models.advanced_process_definition_key_filter import (
        AdvancedProcessDefinitionKeyFilter,
    )
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )
    from ..models.advanced_scope_key_filter import AdvancedScopeKeyFilter
    from ..models.advanced_string_filter import AdvancedStringFilter
    from ..models.advanced_variable_history_item_actor_type_filter import (
        AdvancedVariableHistoryItemActorTypeFilter,
    )
    from ..models.advanced_variable_history_item_key_filter import (
        AdvancedVariableHistoryItemKeyFilter,
    )
    from ..models.advanced_variable_history_item_operation_type_filter import (
        AdvancedVariableHistoryItemOperationTypeFilter,
    )
    from ..models.advanced_variable_history_item_variable_operation_type_filter import (
        AdvancedVariableHistoryItemVariableOperationTypeFilter,
    )
    from ..models.advanced_variable_key_filter import AdvancedVariableKeyFilter


T = TypeVar("T", bound="VariableHistoryItemSearchQueryFilter")


@_attrs_define
class VariableHistoryItemSearchQueryFilter:
    """The variable history item search filters.

    Attributes:
        variable_key (AdvancedVariableKeyFilter | str | Unset): The key of the variable this history item belongs to.
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset): The key of the process instance of this
            variable.
        name (AdvancedStringFilter | str | Unset): Name of the variable.
        scope_key (AdvancedScopeKeyFilter | str | Unset): The key of the scope that defines where this variable is
            directly defined. This can
            be a process instance key (for process-level variables) or an element instance key
            (for local variables scoped to tasks, sub-processes, gateways, events, etc.).
        element_id (AdvancedElementIdFilter | str | Unset): The model-defined id of the element that caused this change,
            if any.
        element_instance_key (AdvancedElementInstanceKeyFilter | str | Unset): The key of the element instance that
            caused this change, if any.
        variable_history_item_key (AdvancedVariableHistoryItemKeyFilter | str | Unset): The unique key of this variable
            history item.
        process_definition_key (AdvancedProcessDefinitionKeyFilter | str | Unset): The key of the process definition.
        process_definition_id (AdvancedProcessDefinitionIdFilter | str | Unset): The id of the process definition.
        tenant_id (AdvancedStringFilter | str | Unset): The tenant id of this variable.
        timestamp (AdvancedDateTimeFilter | datetime.datetime | Unset): The timestamp when this change occurred.
        operation_type (AdvancedVariableHistoryItemOperationTypeFilter | Unset |
            VariableHistoryItemOperationTypeExactMatch): The type of operation that produced this variable change.
        variable_operation_type (AdvancedVariableHistoryItemVariableOperationTypeFilter | Unset |
            VariableHistoryItemVariableOperationTypeExactMatch): What wrote this variable value.
        actor_type (AdvancedVariableHistoryItemActorTypeFilter | Unset | VariableHistoryItemActorTypeExactMatch): The
            type of the actor who performed the operation.
        actor_id (AdvancedStringFilter | str | Unset): The id of the user or client that caused this change, if known.
        agent_element_id (AdvancedElementIdFilter | str | Unset): The element id of the agent that caused this change,
            for example the element id
            of an ad-hoc sub-process, if any.
    """

    variable_key: AdvancedVariableKeyFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    name: AdvancedStringFilter | str | Unset = UNSET
    scope_key: AdvancedScopeKeyFilter | str | Unset = UNSET
    element_id: AdvancedElementIdFilter | str | Unset = UNSET
    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    variable_history_item_key: AdvancedVariableHistoryItemKeyFilter | str | Unset = (
        UNSET
    )
    process_definition_key: AdvancedProcessDefinitionKeyFilter | str | Unset = UNSET
    process_definition_id: AdvancedProcessDefinitionIdFilter | str | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    timestamp: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    operation_type: (
        AdvancedVariableHistoryItemOperationTypeFilter
        | Unset
        | VariableHistoryItemOperationTypeExactMatch
    ) = UNSET
    variable_operation_type: (
        AdvancedVariableHistoryItemVariableOperationTypeFilter
        | Unset
        | VariableHistoryItemVariableOperationTypeExactMatch
    ) = UNSET
    actor_type: (
        AdvancedVariableHistoryItemActorTypeFilter
        | Unset
        | VariableHistoryItemActorTypeExactMatch
    ) = UNSET
    actor_id: AdvancedStringFilter | str | Unset = UNSET
    agent_element_id: AdvancedElementIdFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_element_id_filter import (
            AdvancedElementIdFilter,  # noqa: PLC0415
        )
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,  # noqa: PLC0415
        )
        from ..models.advanced_process_definition_id_filter import (
            AdvancedProcessDefinitionIdFilter,  # noqa: PLC0415
        )
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,  # noqa: PLC0415
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,  # noqa: PLC0415
        )
        from ..models.advanced_scope_key_filter import (
            AdvancedScopeKeyFilter,  # noqa: PLC0415
        )
        from ..models.advanced_string_filter import (
            AdvancedStringFilter,  # noqa: PLC0415
        )
        from ..models.advanced_variable_history_item_key_filter import (
            AdvancedVariableHistoryItemKeyFilter,  # noqa: PLC0415
        )
        from ..models.advanced_variable_key_filter import (
            AdvancedVariableKeyFilter,  # noqa: PLC0415
        )

        variable_key: dict[str, Any] | str | Unset
        if isinstance(self.variable_key, Unset):
            variable_key = UNSET
        elif isinstance(self.variable_key, AdvancedVariableKeyFilter):
            variable_key = self.variable_key.to_dict()
        else:
            variable_key = self.variable_key

        process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.process_instance_key, Unset):
            process_instance_key = UNSET
        elif isinstance(self.process_instance_key, AdvancedProcessInstanceKeyFilter):
            process_instance_key = self.process_instance_key.to_dict()
        else:
            process_instance_key = self.process_instance_key

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, AdvancedStringFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        scope_key: dict[str, Any] | str | Unset
        if isinstance(self.scope_key, Unset):
            scope_key = UNSET
        elif isinstance(self.scope_key, AdvancedScopeKeyFilter):
            scope_key = self.scope_key.to_dict()
        else:
            scope_key = self.scope_key

        element_id: dict[str, Any] | str | Unset
        if isinstance(self.element_id, Unset):
            element_id = UNSET
        elif isinstance(self.element_id, AdvancedElementIdFilter):
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

        variable_history_item_key: dict[str, Any] | str | Unset
        if isinstance(self.variable_history_item_key, Unset):
            variable_history_item_key = UNSET
        elif isinstance(
            self.variable_history_item_key, AdvancedVariableHistoryItemKeyFilter
        ):
            variable_history_item_key = self.variable_history_item_key.to_dict()
        else:
            variable_history_item_key = self.variable_history_item_key

        process_definition_key: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_key, Unset):
            process_definition_key = UNSET
        elif isinstance(
            self.process_definition_key, AdvancedProcessDefinitionKeyFilter
        ):
            process_definition_key = self.process_definition_key.to_dict()
        else:
            process_definition_key = self.process_definition_key

        process_definition_id: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_id, Unset):
            process_definition_id = UNSET
        elif isinstance(self.process_definition_id, AdvancedProcessDefinitionIdFilter):
            process_definition_id = self.process_definition_id.to_dict()
        else:
            process_definition_id = self.process_definition_id

        tenant_id: dict[str, Any] | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        elif isinstance(self.tenant_id, AdvancedStringFilter):
            tenant_id = self.tenant_id.to_dict()
        else:
            tenant_id = self.tenant_id

        timestamp: dict[str, Any] | str | Unset
        if isinstance(self.timestamp, Unset):
            timestamp = UNSET
        elif isinstance(self.timestamp, datetime.datetime):
            timestamp = self.timestamp.isoformat()
        else:
            timestamp = self.timestamp.to_dict()

        operation_type: dict[str, Any] | str | Unset
        if isinstance(self.operation_type, Unset):
            operation_type = UNSET
        elif isinstance(
            self.operation_type, VariableHistoryItemOperationTypeExactMatch
        ):
            operation_type = self.operation_type.value
        else:
            operation_type = self.operation_type.to_dict()

        variable_operation_type: dict[str, Any] | str | Unset
        if isinstance(self.variable_operation_type, Unset):
            variable_operation_type = UNSET
        elif isinstance(
            self.variable_operation_type,
            VariableHistoryItemVariableOperationTypeExactMatch,
        ):
            variable_operation_type = self.variable_operation_type.value
        else:
            variable_operation_type = self.variable_operation_type.to_dict()

        actor_type: dict[str, Any] | str | Unset
        if isinstance(self.actor_type, Unset):
            actor_type = UNSET
        elif isinstance(self.actor_type, VariableHistoryItemActorTypeExactMatch):
            actor_type = self.actor_type.value
        else:
            actor_type = self.actor_type.to_dict()

        actor_id: dict[str, Any] | str | Unset
        if isinstance(self.actor_id, Unset):
            actor_id = UNSET
        elif isinstance(self.actor_id, AdvancedStringFilter):
            actor_id = self.actor_id.to_dict()
        else:
            actor_id = self.actor_id

        agent_element_id: dict[str, Any] | str | Unset
        if isinstance(self.agent_element_id, Unset):
            agent_element_id = UNSET
        elif isinstance(self.agent_element_id, AdvancedElementIdFilter):
            agent_element_id = self.agent_element_id.to_dict()
        else:
            agent_element_id = self.agent_element_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if variable_key is not UNSET:
            field_dict["variableKey"] = variable_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if name is not UNSET:
            field_dict["name"] = name
        if scope_key is not UNSET:
            field_dict["scopeKey"] = scope_key
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key
        if variable_history_item_key is not UNSET:
            field_dict["variableHistoryItemKey"] = variable_history_item_key
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if operation_type is not UNSET:
            field_dict["operationType"] = operation_type
        if variable_operation_type is not UNSET:
            field_dict["variableOperationType"] = variable_operation_type
        if actor_type is not UNSET:
            field_dict["actorType"] = actor_type
        if actor_id is not UNSET:
            field_dict["actorId"] = actor_id
        if agent_element_id is not UNSET:
            field_dict["agentElementId"] = agent_element_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_date_time_filter import (
            AdvancedDateTimeFilter,  # noqa: PLC0415
        )
        from ..models.advanced_element_id_filter import (
            AdvancedElementIdFilter,  # noqa: PLC0415
        )
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,  # noqa: PLC0415
        )
        from ..models.advanced_process_definition_id_filter import (
            AdvancedProcessDefinitionIdFilter,  # noqa: PLC0415
        )
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,  # noqa: PLC0415
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,  # noqa: PLC0415
        )
        from ..models.advanced_scope_key_filter import (
            AdvancedScopeKeyFilter,  # noqa: PLC0415
        )
        from ..models.advanced_string_filter import (
            AdvancedStringFilter,  # noqa: PLC0415
        )
        from ..models.advanced_variable_history_item_actor_type_filter import (
            AdvancedVariableHistoryItemActorTypeFilter,  # noqa: PLC0415
        )
        from ..models.advanced_variable_history_item_key_filter import (
            AdvancedVariableHistoryItemKeyFilter,  # noqa: PLC0415
        )
        from ..models.advanced_variable_history_item_operation_type_filter import (
            AdvancedVariableHistoryItemOperationTypeFilter,  # noqa: PLC0415
        )
        from ..models.advanced_variable_history_item_variable_operation_type_filter import (
            AdvancedVariableHistoryItemVariableOperationTypeFilter,  # noqa: PLC0415
        )
        from ..models.advanced_variable_key_filter import (
            AdvancedVariableKeyFilter,  # noqa: PLC0415
        )

        d = dict(src_dict)

        def _parse_variable_key(
            data: object,
        ) -> AdvancedVariableKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                variable_key_type_1 = AdvancedVariableKeyFilter.from_dict(data)

                return variable_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedVariableKeyFilter | str | Unset, data)

        variable_key = _parse_variable_key(d.pop("variableKey", UNSET))

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

        def _parse_name(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                name_type_1 = AdvancedStringFilter.from_dict(data)

                return name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_scope_key(data: object) -> AdvancedScopeKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                scope_key_type_1 = AdvancedScopeKeyFilter.from_dict(data)

                return scope_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedScopeKeyFilter | str | Unset, data)

        scope_key = _parse_scope_key(d.pop("scopeKey", UNSET))

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

        def _parse_variable_history_item_key(
            data: object,
        ) -> AdvancedVariableHistoryItemKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                variable_history_item_key_type_1 = (
                    AdvancedVariableHistoryItemKeyFilter.from_dict(data)
                )

                return variable_history_item_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedVariableHistoryItemKeyFilter | str | Unset, data)

        variable_history_item_key = _parse_variable_history_item_key(
            d.pop("variableHistoryItemKey", UNSET)
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

        def _parse_process_definition_id(
            data: object,
        ) -> AdvancedProcessDefinitionIdFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_id_type_1 = (
                    AdvancedProcessDefinitionIdFilter.from_dict(data)
                )

                return process_definition_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedProcessDefinitionIdFilter | str | Unset, data)

        process_definition_id = _parse_process_definition_id(
            d.pop("processDefinitionId", UNSET)
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

        def _parse_timestamp(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                timestamp_type_0 = isoparse(data)

                return timestamp_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            timestamp_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return timestamp_type_1

        timestamp = _parse_timestamp(d.pop("timestamp", UNSET))

        def _parse_operation_type(
            data: object,
        ) -> (
            AdvancedVariableHistoryItemOperationTypeFilter
            | Unset
            | VariableHistoryItemOperationTypeExactMatch
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                operation_type_type_0 = VariableHistoryItemOperationTypeExactMatch(data)

                return operation_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            operation_type_type_1 = (
                AdvancedVariableHistoryItemOperationTypeFilter.from_dict(data)
            )

            return operation_type_type_1

        operation_type = _parse_operation_type(d.pop("operationType", UNSET))

        def _parse_variable_operation_type(
            data: object,
        ) -> (
            AdvancedVariableHistoryItemVariableOperationTypeFilter
            | Unset
            | VariableHistoryItemVariableOperationTypeExactMatch
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                variable_operation_type_type_0 = (
                    VariableHistoryItemVariableOperationTypeExactMatch(data)
                )

                return variable_operation_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            variable_operation_type_type_1 = (
                AdvancedVariableHistoryItemVariableOperationTypeFilter.from_dict(data)
            )

            return variable_operation_type_type_1

        variable_operation_type = _parse_variable_operation_type(
            d.pop("variableOperationType", UNSET)
        )

        def _parse_actor_type(
            data: object,
        ) -> (
            AdvancedVariableHistoryItemActorTypeFilter
            | Unset
            | VariableHistoryItemActorTypeExactMatch
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                actor_type_type_0 = VariableHistoryItemActorTypeExactMatch(data)

                return actor_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            actor_type_type_1 = AdvancedVariableHistoryItemActorTypeFilter.from_dict(
                data
            )

            return actor_type_type_1

        actor_type = _parse_actor_type(d.pop("actorType", UNSET))

        def _parse_actor_id(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                actor_id_type_1 = AdvancedStringFilter.from_dict(data)

                return actor_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        actor_id = _parse_actor_id(d.pop("actorId", UNSET))

        def _parse_agent_element_id(
            data: object,
        ) -> AdvancedElementIdFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                agent_element_id_type_1 = AdvancedElementIdFilter.from_dict(data)

                return agent_element_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedElementIdFilter | str | Unset, data)

        agent_element_id = _parse_agent_element_id(d.pop("agentElementId", UNSET))

        variable_history_item_search_query_filter = cls(
            variable_key=variable_key,
            process_instance_key=process_instance_key,
            name=name,
            scope_key=scope_key,
            element_id=element_id,
            element_instance_key=element_instance_key,
            variable_history_item_key=variable_history_item_key,
            process_definition_key=process_definition_key,
            process_definition_id=process_definition_id,
            tenant_id=tenant_id,
            timestamp=timestamp,
            operation_type=operation_type,
            variable_operation_type=variable_operation_type,
            actor_type=actor_type,
            actor_id=actor_id,
            agent_element_id=agent_element_id,
        )

        variable_history_item_search_query_filter.additional_properties = d
        return variable_history_item_search_query_filter

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
