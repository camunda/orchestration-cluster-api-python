from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    BatchOperationKey,
    lift_batch_operation_key,
)

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.batchoperationtype_exactmatch import BatchoperationtypeExactmatch
from ..models.state_exactmatch import StateExactmatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.batchoperationtype_advancedfilter import (
        BatchoperationtypeAdvancedfilter,
    )
    from ..models.processinstancekey_advancedfilter import (
        ProcessinstancekeyAdvancedfilter,
    )
    from ..models.state_advancedfilter import StateAdvancedfilter
    from ..models.usertaskkey_advancedfilter import UsertaskkeyAdvancedfilter


T = TypeVar("T", bound="SearchBatchOperationItemsDataFilter")


@_attrs_define
class SearchBatchOperationItemsDataFilter:
    """The batch operation item search filters.

    Attributes:
        batch_operation_key (str | Unset | UsertaskkeyAdvancedfilter):
        item_key (str | Unset | UsertaskkeyAdvancedfilter):
        process_instance_key (ProcessinstancekeyAdvancedfilter | str | Unset):
        state (StateAdvancedfilter | StateExactmatch | Unset): The state of the batch operation.
        operation_type (BatchoperationtypeAdvancedfilter | BatchoperationtypeExactmatch | Unset):
    """

    batch_operation_key: BatchOperationKey | Unset | UsertaskkeyAdvancedfilter = UNSET
    item_key: str | Unset | UsertaskkeyAdvancedfilter = UNSET
    process_instance_key: ProcessinstancekeyAdvancedfilter | str | Unset = UNSET
    state: StateAdvancedfilter | StateExactmatch | Unset = UNSET
    operation_type: (
        BatchoperationtypeAdvancedfilter | BatchoperationtypeExactmatch | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.processinstancekey_advancedfilter import (
            ProcessinstancekeyAdvancedfilter,
        )
        from ..models.usertaskkey_advancedfilter import UsertaskkeyAdvancedfilter

        batch_operation_key: dict[str, Any] | str | Unset
        if isinstance(self.batch_operation_key, Unset):
            batch_operation_key = UNSET
        elif isinstance(self.batch_operation_key, UsertaskkeyAdvancedfilter):
            batch_operation_key = self.batch_operation_key.to_dict()
        else:
            batch_operation_key = self.batch_operation_key

        item_key: dict[str, Any] | str | Unset
        if isinstance(self.item_key, Unset):
            item_key = UNSET
        elif isinstance(self.item_key, UsertaskkeyAdvancedfilter):
            item_key = self.item_key.to_dict()
        else:
            item_key = self.item_key

        process_instance_key: dict[str, Any] | str | Unset
        if isinstance(self.process_instance_key, Unset):
            process_instance_key = UNSET
        elif isinstance(self.process_instance_key, ProcessinstancekeyAdvancedfilter):
            process_instance_key = self.process_instance_key.to_dict()
        else:
            process_instance_key = self.process_instance_key

        state: dict[str, Any] | str | Unset
        if isinstance(self.state, Unset):
            state = UNSET
        elif isinstance(self.state, StateExactmatch):
            state = self.state.value
        else:
            state = self.state.to_dict()

        operation_type: dict[str, Any] | str | Unset
        if isinstance(self.operation_type, Unset):
            operation_type = UNSET
        elif isinstance(self.operation_type, BatchoperationtypeExactmatch):
            operation_type = self.operation_type.value
        else:
            operation_type = self.operation_type.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if batch_operation_key is not UNSET:
            field_dict["batchOperationKey"] = batch_operation_key
        if item_key is not UNSET:
            field_dict["itemKey"] = item_key
        if process_instance_key is not UNSET:
            field_dict["processInstanceKey"] = process_instance_key
        if state is not UNSET:
            field_dict["state"] = state
        if operation_type is not UNSET:
            field_dict["operationType"] = operation_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batchoperationtype_advancedfilter import (
            BatchoperationtypeAdvancedfilter,
        )
        from ..models.processinstancekey_advancedfilter import (
            ProcessinstancekeyAdvancedfilter,
        )
        from ..models.state_advancedfilter import StateAdvancedfilter
        from ..models.usertaskkey_advancedfilter import UsertaskkeyAdvancedfilter

        d = dict(src_dict)

        def _parse_batch_operation_key(
            data: object,
        ) -> str | Unset | UsertaskkeyAdvancedfilter:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                batch_operation_key_type_1 = UsertaskkeyAdvancedfilter.from_dict(data)

                return batch_operation_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | Unset | UsertaskkeyAdvancedfilter, data)

        _raw_batch_operation_key = _parse_batch_operation_key(
            d.pop("batchOperationKey", UNSET)
        )

        batch_operation_key = (
            lift_batch_operation_key(_raw_batch_operation_key)
            if isinstance(_raw_batch_operation_key, str)
            else _raw_batch_operation_key
        )

        def _parse_item_key(data: object) -> str | Unset | UsertaskkeyAdvancedfilter:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                item_key_type_1 = UsertaskkeyAdvancedfilter.from_dict(data)

                return item_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | Unset | UsertaskkeyAdvancedfilter, data)

        item_key = _parse_item_key(d.pop("itemKey", UNSET))

        def _parse_process_instance_key(
            data: object,
        ) -> ProcessinstancekeyAdvancedfilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_instance_key_type_1 = (
                    ProcessinstancekeyAdvancedfilter.from_dict(data)
                )

                return process_instance_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ProcessinstancekeyAdvancedfilter | str | Unset, data)

        process_instance_key = _parse_process_instance_key(
            d.pop("processInstanceKey", UNSET)
        )

        def _parse_state(data: object) -> StateAdvancedfilter | StateExactmatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                state_type_0 = StateExactmatch(data)

                return state_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            state_type_1 = StateAdvancedfilter.from_dict(data)

            return state_type_1

        state = _parse_state(d.pop("state", UNSET))

        def _parse_operation_type(
            data: object,
        ) -> BatchoperationtypeAdvancedfilter | BatchoperationtypeExactmatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                operation_type_type_0 = BatchoperationtypeExactmatch(data)

                return operation_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            operation_type_type_1 = BatchoperationtypeAdvancedfilter.from_dict(data)

            return operation_type_type_1

        operation_type = _parse_operation_type(d.pop("operationType", UNSET))

        search_batch_operation_items_data_filter = cls(
            batch_operation_key=batch_operation_key,
            item_key=item_key,
            process_instance_key=process_instance_key,
            state=state,
            operation_type=operation_type,
        )

        search_batch_operation_items_data_filter.additional_properties = d
        return search_batch_operation_items_data_filter

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
