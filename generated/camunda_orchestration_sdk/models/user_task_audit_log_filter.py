from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.audit_log_actor_type_exact_match import AuditLogActorTypeExactMatch
from ..models.audit_log_result_exact_match import AuditLogResultExactMatch
from ..models.operation_type_exact_match import OperationTypeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_actor_type_filter import AdvancedActorTypeFilter
    from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
    from ..models.advanced_operation_type_filter import AdvancedOperationTypeFilter
    from ..models.advanced_result_filter import AdvancedResultFilter
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="UserTaskAuditLogFilter")


@_attrs_define
class UserTaskAuditLogFilter:
    """The user task audit log search filters.

    Attributes:
        operation_type (AdvancedOperationTypeFilter | OperationTypeExactMatch | Unset):
        result (AdvancedResultFilter | AuditLogResultExactMatch | Unset):
        timestamp (AdvancedDateTimeFilter | datetime.datetime | Unset):
        actor_type (AdvancedActorTypeFilter | AuditLogActorTypeExactMatch | Unset):
        actor_id (AdvancedStringFilter | str | Unset):
    """

    operation_type: AdvancedOperationTypeFilter | OperationTypeExactMatch | Unset = (
        UNSET
    )
    result: AdvancedResultFilter | AuditLogResultExactMatch | Unset = UNSET
    timestamp: AdvancedDateTimeFilter | datetime.datetime | Unset = UNSET
    actor_type: AdvancedActorTypeFilter | AuditLogActorTypeExactMatch | Unset = UNSET
    actor_id: AdvancedStringFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_string_filter import AdvancedStringFilter

        operation_type: dict[str, Any] | str | Unset
        if isinstance(self.operation_type, Unset):
            operation_type = UNSET
        elif isinstance(self.operation_type, OperationTypeExactMatch):
            operation_type = self.operation_type.value
        else:
            operation_type = self.operation_type.to_dict()

        result: dict[str, Any] | str | Unset
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, AuditLogResultExactMatch):
            result = self.result.value
        else:
            result = self.result.to_dict()

        timestamp: dict[str, Any] | str | Unset
        if isinstance(self.timestamp, Unset):
            timestamp = UNSET
        elif isinstance(self.timestamp, datetime.datetime):
            timestamp = self.timestamp.isoformat()
        else:
            timestamp = self.timestamp.to_dict()

        actor_type: dict[str, Any] | str | Unset
        if isinstance(self.actor_type, Unset):
            actor_type = UNSET
        elif isinstance(self.actor_type, AuditLogActorTypeExactMatch):
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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if operation_type is not UNSET:
            field_dict["operationType"] = operation_type
        if result is not UNSET:
            field_dict["result"] = result
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if actor_type is not UNSET:
            field_dict["actorType"] = actor_type
        if actor_id is not UNSET:
            field_dict["actorId"] = actor_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_actor_type_filter import AdvancedActorTypeFilter
        from ..models.advanced_date_time_filter import AdvancedDateTimeFilter
        from ..models.advanced_operation_type_filter import AdvancedOperationTypeFilter
        from ..models.advanced_result_filter import AdvancedResultFilter
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)

        def _parse_operation_type(
            data: object,
        ) -> AdvancedOperationTypeFilter | OperationTypeExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                operation_type_type_0 = OperationTypeExactMatch(data)

                return operation_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            operation_type_type_1 = AdvancedOperationTypeFilter.from_dict(data)

            return operation_type_type_1

        operation_type = _parse_operation_type(d.pop("operationType", UNSET))

        def _parse_result(
            data: object,
        ) -> AdvancedResultFilter | AuditLogResultExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                result_type_0 = AuditLogResultExactMatch(data)

                return result_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            result_type_1 = AdvancedResultFilter.from_dict(data)

            return result_type_1

        result = _parse_result(d.pop("result", UNSET))

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

        def _parse_actor_type(
            data: object,
        ) -> AdvancedActorTypeFilter | AuditLogActorTypeExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                actor_type_type_0 = AuditLogActorTypeExactMatch(data)

                return actor_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            actor_type_type_1 = AdvancedActorTypeFilter.from_dict(data)

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

        user_task_audit_log_filter = cls(
            operation_type=operation_type,
            result=result,
            timestamp=timestamp,
            actor_type=actor_type,
            actor_id=actor_id,
        )

        user_task_audit_log_filter.additional_properties = d
        return user_task_audit_log_filter

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
