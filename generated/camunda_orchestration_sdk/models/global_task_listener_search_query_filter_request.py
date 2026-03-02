from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.global_listener_source_exact_match import GlobalListenerSourceExactMatch
from ..models.global_task_listener_event_type_exact_match import (
    GlobalTaskListenerEventTypeExactMatch,
)
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_global_listener_source_filter import (
        AdvancedGlobalListenerSourceFilter,
    )
    from ..models.advanced_global_task_listener_event_type_filter import (
        AdvancedGlobalTaskListenerEventTypeFilter,
    )
    from ..models.advanced_integer_filter import AdvancedIntegerFilter
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="GlobalTaskListenerSearchQueryFilterRequest")


@_attrs_define
class GlobalTaskListenerSearchQueryFilterRequest:
    """Global listener filter request.

    Attributes:
        id (AdvancedStringFilter | str | Unset):
        type_ (AdvancedStringFilter | str | Unset):
        retries (AdvancedIntegerFilter | int | Unset):
        event_types (list[AdvancedGlobalTaskListenerEventTypeFilter | GlobalTaskListenerEventTypeExactMatch] | Unset):
            Event types of the global listener.
        after_non_global (bool | Unset): Whether the listener runs after model-level listeners.
        priority (AdvancedIntegerFilter | int | Unset):
        source (AdvancedGlobalListenerSourceFilter | GlobalListenerSourceExactMatch | Unset):
    """

    id: AdvancedStringFilter | str | Unset = UNSET
    type_: AdvancedStringFilter | str | Unset = UNSET
    retries: AdvancedIntegerFilter | int | Unset = UNSET
    event_types: (
        list[
            AdvancedGlobalTaskListenerEventTypeFilter
            | GlobalTaskListenerEventTypeExactMatch
        ]
        | Unset
    ) = UNSET
    after_non_global: bool | Unset = UNSET
    priority: AdvancedIntegerFilter | int | Unset = UNSET
    source: (
        AdvancedGlobalListenerSourceFilter | GlobalListenerSourceExactMatch | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_string_filter import AdvancedStringFilter

        id: dict[str, Any] | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, AdvancedStringFilter):
            id = self.id.to_dict()
        else:
            id = self.id

        type_: dict[str, Any] | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        elif isinstance(self.type_, AdvancedStringFilter):
            type_ = self.type_.to_dict()
        else:
            type_ = self.type_

        retries: dict[str, Any] | int | Unset
        if isinstance(self.retries, Unset):
            retries = UNSET
        elif isinstance(self.retries, AdvancedIntegerFilter):
            retries = self.retries.to_dict()
        else:
            retries = self.retries

        event_types: list[dict[str, Any] | str] | Unset = UNSET
        if not isinstance(self.event_types, Unset):
            event_types = []
            for event_types_item_data in self.event_types:
                event_types_item: dict[str, Any] | str
                if isinstance(
                    event_types_item_data, GlobalTaskListenerEventTypeExactMatch
                ):
                    event_types_item = event_types_item_data.value
                else:
                    event_types_item = event_types_item_data.to_dict()

                event_types.append(event_types_item)

        after_non_global = self.after_non_global

        priority: dict[str, Any] | int | Unset
        if isinstance(self.priority, Unset):
            priority = UNSET
        elif isinstance(self.priority, AdvancedIntegerFilter):
            priority = self.priority.to_dict()
        else:
            priority = self.priority

        source: dict[str, Any] | str | Unset
        if isinstance(self.source, Unset):
            source = UNSET
        elif isinstance(self.source, GlobalListenerSourceExactMatch):
            source = self.source.value
        else:
            source = self.source.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if retries is not UNSET:
            field_dict["retries"] = retries
        if event_types is not UNSET:
            field_dict["eventTypes"] = event_types
        if after_non_global is not UNSET:
            field_dict["afterNonGlobal"] = after_non_global
        if priority is not UNSET:
            field_dict["priority"] = priority
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_global_listener_source_filter import (
            AdvancedGlobalListenerSourceFilter,
        )
        from ..models.advanced_global_task_listener_event_type_filter import (
            AdvancedGlobalTaskListenerEventTypeFilter,
        )
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)

        def _parse_id(data: object) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                id_type_1 = AdvancedStringFilter.from_dict(data)

                return id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

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

        _event_types = d.pop("eventTypes", UNSET)
        event_types: (
            list[
                AdvancedGlobalTaskListenerEventTypeFilter
                | GlobalTaskListenerEventTypeExactMatch
            ]
            | Unset
        ) = UNSET
        if _event_types is not UNSET:
            event_types = []
            for event_types_item_data in _event_types:

                def _parse_event_types_item(
                    data: object,
                ) -> (
                    AdvancedGlobalTaskListenerEventTypeFilter
                    | GlobalTaskListenerEventTypeExactMatch
                ):
                    try:
                        if not isinstance(data, str):
                            raise TypeError()
                        event_types_item_type_0 = GlobalTaskListenerEventTypeExactMatch(
                            data
                        )

                        return event_types_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()

                    data = cast(dict[str, Any], data)
                    event_types_item_type_1 = (
                        AdvancedGlobalTaskListenerEventTypeFilter.from_dict(data)
                    )

                    return event_types_item_type_1

                event_types_item = _parse_event_types_item(event_types_item_data)

                event_types.append(event_types_item)

        after_non_global = d.pop("afterNonGlobal", UNSET)

        def _parse_priority(data: object) -> AdvancedIntegerFilter | int | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                priority_type_1 = AdvancedIntegerFilter.from_dict(data)

                return priority_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedIntegerFilter | int | Unset, data)

        priority = _parse_priority(d.pop("priority", UNSET))

        def _parse_source(
            data: object,
        ) -> (
            AdvancedGlobalListenerSourceFilter | GlobalListenerSourceExactMatch | Unset
        ):
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                source_type_0 = GlobalListenerSourceExactMatch(data)

                return source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            source_type_1 = AdvancedGlobalListenerSourceFilter.from_dict(data)

            return source_type_1

        source = _parse_source(d.pop("source", UNSET))

        global_task_listener_search_query_filter_request = cls(
            id=id,
            type_=type_,
            retries=retries,
            event_types=event_types,
            after_non_global=after_non_global,
            priority=priority,
            source=source,
        )

        global_task_listener_search_query_filter_request.additional_properties = d
        return global_task_listener_search_query_filter_request

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
