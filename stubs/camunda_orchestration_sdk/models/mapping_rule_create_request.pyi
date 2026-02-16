from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from attrs import define as _attrs_define

T = TypeVar("T", bound="MappingRuleCreateRequest")

@_attrs_define
class MappingRuleCreateRequest:
    mapping_rule_id: str
    claim_name: str
    claim_value: str
    name: str
    def to_dict(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T: ...
