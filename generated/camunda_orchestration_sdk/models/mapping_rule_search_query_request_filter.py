from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import MappingRuleId

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="MappingRuleSearchQueryRequestFilter")


@_attrs_define
class MappingRuleSearchQueryRequestFilter:
    """The mapping rule search filters.

    Attributes:
        claim_name (str | Unset): The claim name to match against a token.
        claim_value (str | Unset): The value of the claim to match.
        name (AdvancedStringFilter | str | Unset): The name of the mapping rule.
        mapping_rule_id (str | Unset): The ID of the mapping rule. Example: my-mapping-rule.
    """

    claim_name: str | Unset = UNSET
    claim_value: str | Unset = UNSET
    name: AdvancedStringFilter | str | Unset = UNSET
    mapping_rule_id: MappingRuleId | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_string_filter import AdvancedStringFilter

        claim_name = self.claim_name

        claim_value = self.claim_value

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, AdvancedStringFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        mapping_rule_id = self.mapping_rule_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if claim_name is not UNSET:
            field_dict["claimName"] = claim_name
        if claim_value is not UNSET:
            field_dict["claimValue"] = claim_value
        if name is not UNSET:
            field_dict["name"] = name
        if mapping_rule_id is not UNSET:
            field_dict["mappingRuleId"] = mapping_rule_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)
        claim_name = d.pop("claimName", UNSET)

        claim_value = d.pop("claimValue", UNSET)

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

        mapping_rule_id = (
            MappingRuleId(_val)
            if (_val := d.pop("mappingRuleId", UNSET)) is not UNSET
            else UNSET
        )

        mapping_rule_search_query_request_filter = cls(
            claim_name=claim_name,
            claim_value=claim_value,
            name=name,
            mapping_rule_id=mapping_rule_id,
        )

        mapping_rule_search_query_request_filter.additional_properties = d
        return mapping_rule_search_query_request_filter

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
