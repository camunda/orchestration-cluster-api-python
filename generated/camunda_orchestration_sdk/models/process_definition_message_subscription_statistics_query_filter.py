from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.message_subscription_state_exact_match import (
    MessageSubscriptionStateExactMatch,
)
from ..models.message_subscription_type_exact_match import (
    MessageSubscriptionTypeExactMatch,
)
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
    from ..models.advanced_element_instance_key_filter import (
        AdvancedElementInstanceKeyFilter,
    )
    from ..models.advanced_integer_filter import AdvancedIntegerFilter
    from ..models.advanced_message_subscription_key_filter import (
        AdvancedMessageSubscriptionKeyFilter,
    )
    from ..models.advanced_message_subscription_state_filter import (
        AdvancedMessageSubscriptionStateFilter,
    )
    from ..models.advanced_message_subscription_type_filter import (
        AdvancedMessageSubscriptionTypeFilter,
    )
    from ..models.advanced_process_definition_key_filter import (
        AdvancedProcessDefinitionKeyFilter,
    )
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="ProcessDefinitionMessageSubscriptionStatisticsQueryFilter")


@_attrs_define
class ProcessDefinitionMessageSubscriptionStatisticsQueryFilter:
    """The message subscription filters.

    Attributes:
        message_subscription_key (AdvancedMessageSubscriptionKeyFilter | str | Unset): The message subscription key
            associated with this message subscription.
        process_definition_key (AdvancedProcessDefinitionKeyFilter | str | Unset): The process definition key associated
            with this correlated message subscription. This only works for data created with 8.9 and later.
        process_definition_id (AdvancedStringFilter | str | Unset): The process definition ID associated with this
            message subscription.
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset): The process instance key associated with
            this message subscription.
        element_id (AdvancedStringFilter | str | Unset): The element ID associated with this message subscription.
        element_instance_key (AdvancedElementInstanceKeyFilter | str | Unset): The element instance key associated with
            this message subscription.
        message_subscription_state (AdvancedMessageSubscriptionStateFilter | MessageSubscriptionStateExactMatch |
            Unset): The message subscription state.
        last_updated_date (AdvancedDateTimeFilter | datetime.datetime | Unset): The last updated date of the message
            subscription.
        message_name (AdvancedStringFilter | str | Unset): The name of the message associated with the message
            subscription.
        correlation_key (AdvancedStringFilter | str | Unset): The correlation key of the message subscription.
        tenant_id (AdvancedStringFilter | str | Unset): The unique external tenant ID.
        message_subscription_type (AdvancedMessageSubscriptionTypeFilter | MessageSubscriptionTypeExactMatch | Unset):
            The type of message subscription to filter by. When omitted, both
            `START_EVENT` and `PROCESS_EVENT` are returned. Only available for data
            created with Camunda 8.10 or later.
        process_definition_name (AdvancedStringFilter | str | Unset): The name of the process definition associated with
            this message subscription.
        process_definition_version (AdvancedIntegerFilter | int | Unset): The version of the process definition
            associated with this message subscription.
        tool_name (AdvancedStringFilter | str | Unset): Filter by tool name extracted from the `io.camunda.tool:name`
            zeebe:property.
        inbound_connector_type (AdvancedStringFilter | str | Unset): Filter by inbound connector type extracted from the
            `inbound.type` zeebe:property.
    """

    message_subscription_key: AdvancedMessageSubscriptionKeyFilter | str | Unset = UNSET
    process_definition_key: AdvancedProcessDefinitionKeyFilter | str | Unset = UNSET
    process_definition_id: AdvancedStringFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    element_id: AdvancedStringFilter | str | Unset = UNSET
    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    message_subscription_state: (
        AdvancedMessageSubscriptionStateFilter
        | MessageSubscriptionStateExactMatch
        | Unset
    ) = UNSET
    last_updated_date: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    message_name: AdvancedStringFilter | str | Unset = UNSET
    correlation_key: AdvancedStringFilter | str | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    message_subscription_type: (
        AdvancedMessageSubscriptionTypeFilter
        | MessageSubscriptionTypeExactMatch
        | Unset
    ) = UNSET
    process_definition_name: AdvancedStringFilter | str | Unset = UNSET
    process_definition_version: AdvancedIntegerFilter | int | Unset = UNSET
    tool_name: AdvancedStringFilter | str | Unset = UNSET
    inbound_connector_type: AdvancedStringFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_message_subscription_key_filter import (
            AdvancedMessageSubscriptionKeyFilter,
        )
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter

        message_subscription_key: dict[str, Any] | str | Unset
        if isinstance(self.message_subscription_key, Unset):
            message_subscription_key = UNSET
        elif isinstance(
            self.message_subscription_key, AdvancedMessageSubscriptionKeyFilter
        ):
            message_subscription_key = self.message_subscription_key.to_dict()
        else:
            message_subscription_key = self.message_subscription_key

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
        elif isinstance(self.process_definition_id, AdvancedStringFilter):
            process_definition_id = self.process_definition_id.to_dict()
        else:
            process_definition_id = self.process_definition_id

        process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.process_instance_key, Unset):
            process_instance_key = UNSET
        elif isinstance(self.process_instance_key, AdvancedProcessInstanceKeyFilter):
            process_instance_key = self.process_instance_key.to_dict()
        else:
            process_instance_key = self.process_instance_key

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

        message_subscription_state: dict[str, Any] | str | Unset
        if isinstance(self.message_subscription_state, Unset):
            message_subscription_state = UNSET
        elif isinstance(
            self.message_subscription_state, MessageSubscriptionStateExactMatch
        ):
            message_subscription_state = self.message_subscription_state.value
        else:
            message_subscription_state = self.message_subscription_state.to_dict()

        last_updated_date: dict[str, Any] | str | Unset
        if isinstance(self.last_updated_date, Unset):
            last_updated_date = UNSET
        elif isinstance(self.last_updated_date, datetime.datetime):
            last_updated_date = self.last_updated_date.isoformat()
        else:
            last_updated_date = self.last_updated_date.to_dict()

        message_name: dict[str, Any] | str | Unset
        if isinstance(self.message_name, Unset):
            message_name = UNSET
        elif isinstance(self.message_name, AdvancedStringFilter):
            message_name = self.message_name.to_dict()
        else:
            message_name = self.message_name

        correlation_key: dict[str, Any] | str | Unset
        if isinstance(self.correlation_key, Unset):
            correlation_key = UNSET
        elif isinstance(self.correlation_key, AdvancedStringFilter):
            correlation_key = self.correlation_key.to_dict()
        else:
            correlation_key = self.correlation_key

        tenant_id: dict[str, Any] | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        elif isinstance(self.tenant_id, AdvancedStringFilter):
            tenant_id = self.tenant_id.to_dict()
        else:
            tenant_id = self.tenant_id

        message_subscription_type: dict[str, Any] | str | Unset
        if isinstance(self.message_subscription_type, Unset):
            message_subscription_type = UNSET
        elif isinstance(
            self.message_subscription_type, MessageSubscriptionTypeExactMatch
        ):
            message_subscription_type = self.message_subscription_type.value
        else:
            message_subscription_type = self.message_subscription_type.to_dict()

        process_definition_name: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_name, Unset):
            process_definition_name = UNSET
        elif isinstance(self.process_definition_name, AdvancedStringFilter):
            process_definition_name = self.process_definition_name.to_dict()
        else:
            process_definition_name = self.process_definition_name

        process_definition_version: dict[str, Any] | int | Unset
        if isinstance(self.process_definition_version, Unset):
            process_definition_version = UNSET
        elif isinstance(self.process_definition_version, AdvancedIntegerFilter):
            process_definition_version = self.process_definition_version.to_dict()
        else:
            process_definition_version = self.process_definition_version

        tool_name: dict[str, Any] | str | Unset
        if isinstance(self.tool_name, Unset):
            tool_name = UNSET
        elif isinstance(self.tool_name, AdvancedStringFilter):
            tool_name = self.tool_name.to_dict()
        else:
            tool_name = self.tool_name

        inbound_connector_type: dict[str, Any] | str | Unset
        if isinstance(self.inbound_connector_type, Unset):
            inbound_connector_type = UNSET
        elif isinstance(self.inbound_connector_type, AdvancedStringFilter):
            inbound_connector_type = self.inbound_connector_type.to_dict()
        else:
            inbound_connector_type = self.inbound_connector_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message_subscription_key is not UNSET:
            field_dict["messageSubscriptionKey"] = message_subscription_key
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key
        if message_subscription_state is not UNSET:
            field_dict["messageSubscriptionState"] = message_subscription_state
        if last_updated_date is not UNSET:
            field_dict["lastUpdatedDate"] = last_updated_date
        if message_name is not UNSET:
            field_dict["messageName"] = message_name
        if correlation_key is not UNSET:
            field_dict["correlationKey"] = correlation_key
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if message_subscription_type is not UNSET:
            field_dict["messageSubscriptionType"] = message_subscription_type
        if process_definition_name is not UNSET:
            field_dict["processDefinitionName"] = process_definition_name
        if process_definition_version is not UNSET:
            field_dict["processDefinitionVersion"] = process_definition_version
        if tool_name is not UNSET:
            field_dict["toolName"] = tool_name
        if inbound_connector_type is not UNSET:
            field_dict["inboundConnectorType"] = inbound_connector_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_message_subscription_key_filter import (
            AdvancedMessageSubscriptionKeyFilter,
        )
        from ..models.advanced_message_subscription_state_filter import (
            AdvancedMessageSubscriptionStateFilter,
        )
        from ..models.advanced_message_subscription_type_filter import (
            AdvancedMessageSubscriptionTypeFilter,
        )
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)

        def _parse_message_subscription_key(
            data: object,
        ) -> AdvancedMessageSubscriptionKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                message_subscription_key_type_1 = (
                    AdvancedMessageSubscriptionKeyFilter.from_dict(data)
                )

                return message_subscription_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedMessageSubscriptionKeyFilter | str | Unset, data)

        message_subscription_key = _parse_message_subscription_key(
            d.pop("messageSubscriptionKey", UNSET)
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

        def _parse_message_subscription_state(
            data: object,
        ) -> (
            AdvancedMessageSubscriptionStateFilter
            | MessageSubscriptionStateExactMatch
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                message_subscription_state_type_0 = MessageSubscriptionStateExactMatch(
                    data
                )

                return message_subscription_state_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            message_subscription_state_type_1 = (
                AdvancedMessageSubscriptionStateFilter.from_dict(data)
            )

            return message_subscription_state_type_1

        message_subscription_state = _parse_message_subscription_state(
            d.pop("messageSubscriptionState", UNSET)
        )

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

        def _parse_message_name(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                message_name_type_1 = AdvancedStringFilter.from_dict(data)

                return message_name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        message_name = _parse_message_name(d.pop("messageName", UNSET))

        def _parse_correlation_key(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                correlation_key_type_1 = AdvancedStringFilter.from_dict(data)

                return correlation_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        correlation_key = _parse_correlation_key(d.pop("correlationKey", UNSET))

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

        def _parse_message_subscription_type(
            data: object,
        ) -> (
            AdvancedMessageSubscriptionTypeFilter
            | MessageSubscriptionTypeExactMatch
            | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                message_subscription_type_type_0 = MessageSubscriptionTypeExactMatch(
                    data
                )

                return message_subscription_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            message_subscription_type_type_1 = (
                AdvancedMessageSubscriptionTypeFilter.from_dict(data)
            )

            return message_subscription_type_type_1

        message_subscription_type = _parse_message_subscription_type(
            d.pop("messageSubscriptionType", UNSET)
        )

        def _parse_process_definition_name(
            data: object,
        ) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_name_type_1 = AdvancedStringFilter.from_dict(data)

                return process_definition_name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        process_definition_name = _parse_process_definition_name(
            d.pop("processDefinitionName", UNSET)
        )

        def _parse_process_definition_version(
            data: object,
        ) -> AdvancedIntegerFilter | int | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_version_type_1 = AdvancedIntegerFilter.from_dict(
                    data
                )

                return process_definition_version_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedIntegerFilter | int | Unset, data)

        process_definition_version = _parse_process_definition_version(
            d.pop("processDefinitionVersion", UNSET)
        )

        def _parse_tool_name(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                tool_name_type_1 = AdvancedStringFilter.from_dict(data)

                return tool_name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        tool_name = _parse_tool_name(d.pop("toolName", UNSET))

        def _parse_inbound_connector_type(
            data: object,
        ) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                inbound_connector_type_type_1 = AdvancedStringFilter.from_dict(data)

                return inbound_connector_type_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        inbound_connector_type = _parse_inbound_connector_type(
            d.pop("inboundConnectorType", UNSET)
        )

        process_definition_message_subscription_statistics_query_filter = cls(
            message_subscription_key=message_subscription_key,
            process_definition_key=process_definition_key,
            process_definition_id=process_definition_id,
            process_instance_key=process_instance_key,
            element_id=element_id,
            element_instance_key=element_instance_key,
            message_subscription_state=message_subscription_state,
            last_updated_date=last_updated_date,
            message_name=message_name,
            correlation_key=correlation_key,
            tenant_id=tenant_id,
            message_subscription_type=message_subscription_type,
            process_definition_name=process_definition_name,
            process_definition_version=process_definition_version,
            tool_name=tool_name,
            inbound_connector_type=inbound_connector_type,
        )

        process_definition_message_subscription_statistics_query_filter.additional_properties = d
        return process_definition_message_subscription_statistics_query_filter

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
