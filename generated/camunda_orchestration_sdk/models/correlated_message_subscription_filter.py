from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

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
    from ..models.advanced_process_definition_key_filter import (
        AdvancedProcessDefinitionKeyFilter,
    )
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )
    from ..models.advanced_string_filter import AdvancedStringFilter
    from ..models.basic_string_filter import BasicStringFilter


T = TypeVar("T", bound="CorrelatedMessageSubscriptionFilter")


@_attrs_define
class CorrelatedMessageSubscriptionFilter:
    """Correlated message subscriptions search filter.

    Attributes:
        correlation_key (AdvancedStringFilter | str | Unset):
        correlation_time (AdvancedDateTimeFilter | datetime.datetime | Unset):
        element_id (AdvancedStringFilter | str | Unset):
        element_instance_key (AdvancedElementInstanceKeyFilter | str | Unset):
        message_key (BasicStringFilter | str | Unset):
        message_name (AdvancedStringFilter | str | Unset):
        partition_id (AdvancedIntegerFilter | int | Unset):
        process_definition_id (AdvancedStringFilter | str | Unset):
        process_definition_key (AdvancedProcessDefinitionKeyFilter | str | Unset):
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset):
        subscription_key (AdvancedMessageSubscriptionKeyFilter | str | Unset):
        tenant_id (AdvancedStringFilter | str | Unset):
    """

    correlation_key: AdvancedStringFilter | str | Unset = UNSET
    correlation_time: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    element_id: AdvancedStringFilter | str | Unset = UNSET
    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    message_key: BasicStringFilter | str | Unset = UNSET
    message_name: AdvancedStringFilter | str | Unset = UNSET
    partition_id: AdvancedIntegerFilter | int | Unset = UNSET
    process_definition_id: AdvancedStringFilter | str | Unset = UNSET
    process_definition_key: AdvancedProcessDefinitionKeyFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    subscription_key: AdvancedMessageSubscriptionKeyFilter | str | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
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
        from ..models.basic_string_filter import BasicStringFilter

        correlation_key: dict[str, Any] | str | Unset
        if isinstance(self.correlation_key, Unset):
            correlation_key = UNSET
        elif isinstance(self.correlation_key, AdvancedStringFilter):
            correlation_key = self.correlation_key.to_dict()
        else:
            correlation_key = self.correlation_key

        correlation_time: dict[str, Any] | str | Unset
        if isinstance(self.correlation_time, Unset):
            correlation_time = UNSET
        elif isinstance(self.correlation_time, datetime.datetime):
            correlation_time = self.correlation_time.isoformat()
        else:
            correlation_time = self.correlation_time.to_dict()

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

        message_key: dict[str, Any] | str | Unset
        if isinstance(self.message_key, Unset):
            message_key = UNSET
        elif isinstance(self.message_key, BasicStringFilter):
            message_key = self.message_key.to_dict()
        else:
            message_key = self.message_key

        message_name: dict[str, Any] | str | Unset
        if isinstance(self.message_name, Unset):
            message_name = UNSET
        elif isinstance(self.message_name, AdvancedStringFilter):
            message_name = self.message_name.to_dict()
        else:
            message_name = self.message_name

        partition_id: dict[str, Any] | int | Unset
        if isinstance(self.partition_id, Unset):
            partition_id = UNSET
        elif isinstance(self.partition_id, AdvancedIntegerFilter):
            partition_id = self.partition_id.to_dict()
        else:
            partition_id = self.partition_id

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

        subscription_key: dict[str, Any] | str | Unset
        if isinstance(self.subscription_key, Unset):
            subscription_key = UNSET
        elif isinstance(self.subscription_key, AdvancedMessageSubscriptionKeyFilter):
            subscription_key = self.subscription_key.to_dict()
        else:
            subscription_key = self.subscription_key

        tenant_id: dict[str, Any] | str | Unset
        if isinstance(self.tenant_id, Unset):
            tenant_id = UNSET
        elif isinstance(self.tenant_id, AdvancedStringFilter):
            tenant_id = self.tenant_id.to_dict()
        else:
            tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if correlation_key is not UNSET:
            field_dict["correlationKey"] = correlation_key
        if correlation_time is not UNSET:
            field_dict["correlationTime"] = correlation_time
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key
        if message_key is not UNSET:
            field_dict["messageKey"] = message_key
        if message_name is not UNSET:
            field_dict["messageName"] = message_name
        if partition_id is not UNSET:
            field_dict["partitionId"] = partition_id
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if subscription_key is not UNSET:
            field_dict["subscriptionKey"] = subscription_key
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id

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
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter
        from ..models.basic_string_filter import BasicStringFilter

        d = dict(src_dict)

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

        def _parse_correlation_time(
            data: object,
        ) -> AdvancedDateTimeFilter | datetime.datetime | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                correlation_time_type_0 = isoparse(data)

                return correlation_time_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            correlation_time_type_1 = AdvancedDateTimeFilter.from_dict(data)

            return correlation_time_type_1

        correlation_time = _parse_correlation_time(d.pop("correlationTime", UNSET))

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

        def _parse_message_key(data: object) -> BasicStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                message_key_type_1 = BasicStringFilter.from_dict(data)

                return message_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BasicStringFilter | str | Unset, data)

        message_key = _parse_message_key(d.pop("messageKey", UNSET))

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

        def _parse_partition_id(data: object) -> AdvancedIntegerFilter | int | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                partition_id_type_1 = AdvancedIntegerFilter.from_dict(data)

                return partition_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedIntegerFilter | int | Unset, data)

        partition_id = _parse_partition_id(d.pop("partitionId", UNSET))

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

        def _parse_subscription_key(
            data: object,
        ) -> AdvancedMessageSubscriptionKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                subscription_key_type_1 = (
                    AdvancedMessageSubscriptionKeyFilter.from_dict(data)
                )

                return subscription_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedMessageSubscriptionKeyFilter | str | Unset, data)

        subscription_key = _parse_subscription_key(d.pop("subscriptionKey", UNSET))

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

        correlated_message_subscription_filter = cls(
            correlation_key=correlation_key,
            correlation_time=correlation_time,
            element_id=element_id,
            element_instance_key=element_instance_key,
            message_key=message_key,
            message_name=message_name,
            partition_id=partition_id,
            process_definition_id=process_definition_id,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            subscription_key=subscription_key,
            tenant_id=tenant_id,
        )

        correlated_message_subscription_filter.additional_properties = d
        return correlated_message_subscription_filter

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
