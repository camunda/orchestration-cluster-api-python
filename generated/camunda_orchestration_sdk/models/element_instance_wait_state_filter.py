from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_element_id_filter import AdvancedElementIdFilter
    from ..models.advanced_element_instance_key_filter import (
        AdvancedElementInstanceKeyFilter,
    )
    from ..models.advanced_process_instance_key_filter import (
        AdvancedProcessInstanceKeyFilter,
    )


T = TypeVar("T", bound="ElementInstanceWaitStateFilter")


@_attrs_define
class ElementInstanceWaitStateFilter:
    """Filters for the element instance inspection.

    Attributes:
        element_instance_key (AdvancedElementInstanceKeyFilter | str | Unset): Filter by element instance key.
        process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset): Filter by process instance key.
        root_process_instance_key (AdvancedProcessInstanceKeyFilter | str | Unset): Filter by root process instance key.
        element_id (AdvancedElementIdFilter | str | Unset): Filter by element ID.
    """

    element_instance_key: AdvancedElementInstanceKeyFilter | str | Unset = UNSET
    process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    root_process_instance_key: AdvancedProcessInstanceKeyFilter | str | Unset = UNSET
    element_id: AdvancedElementIdFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_element_id_filter import AdvancedElementIdFilter
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )

        element_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.element_instance_key, Unset):
            element_instance_key = UNSET
        elif isinstance(self.element_instance_key, AdvancedElementInstanceKeyFilter):
            element_instance_key = self.element_instance_key.to_dict()
        else:
            element_instance_key = self.element_instance_key

        process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.process_instance_key, Unset):
            process_instance_key = UNSET
        elif isinstance(self.process_instance_key, AdvancedProcessInstanceKeyFilter):
            process_instance_key = self.process_instance_key.to_dict()
        else:
            process_instance_key = self.process_instance_key

        root_process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.root_process_instance_key, Unset):
            root_process_instance_key = UNSET
        elif isinstance(
            self.root_process_instance_key, AdvancedProcessInstanceKeyFilter
        ):
            root_process_instance_key = self.root_process_instance_key.to_dict()
        else:
            root_process_instance_key = self.root_process_instance_key

        element_id: dict[str, Any] | str | Unset
        if isinstance(self.element_id, Unset):
            element_id = UNSET
        elif isinstance(self.element_id, AdvancedElementIdFilter):
            element_id = self.element_id.to_dict()
        else:
            element_id = self.element_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if element_instance_key is not UNSET:
            field_dict["elementInstanceKey"] = element_instance_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if root_process_instance_key is not UNSET:
            field_dict["rootProcessInstanceKey"] = root_process_instance_key
        if element_id is not UNSET:
            field_dict["elementId"] = element_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_element_id_filter import AdvancedElementIdFilter
        from ..models.advanced_element_instance_key_filter import (
            AdvancedElementInstanceKeyFilter,
        )
        from ..models.advanced_process_instance_key_filter import (
            AdvancedProcessInstanceKeyFilter,
        )

        d = dict(src_dict)

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

        def _parse_root_process_instance_key(
            data: object,
        ) -> AdvancedProcessInstanceKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                root_process_instance_key_type_1 = (
                    AdvancedProcessInstanceKeyFilter.from_dict(data)
                )

                return root_process_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedProcessInstanceKeyFilter | str | Unset, data)

        root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey", UNSET)
        )

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

        element_instance_wait_state_filter = cls(
            element_instance_key=element_instance_key,
            process_instance_key=process_instance_key,
            root_process_instance_key=root_process_instance_key,
            element_id=element_id,
        )

        element_instance_wait_state_filter.additional_properties = d
        return element_instance_wait_state_filter

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
