from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define
from attrs import field as _attrs_field
from ..types import UNSET, Unset, str_any_dict_factory
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
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
    @property
    def additional_keys(self) -> list[str]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
