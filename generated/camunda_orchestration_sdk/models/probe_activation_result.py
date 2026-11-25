from __future__ import annotations
from camunda_orchestration_sdk._required_fields import RequiredFields

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.activated_probe_result import ActivatedProbeResult


T = TypeVar("T", bound="ProbeActivationResult")


@_attrs_define
class ProbeActivationResult:
    """The collected probes.

    Attributes:
        probes (list[ActivatedProbeResult]): The collected probes, none when the request timed out.
    """

    probes: list[ActivatedProbeResult]
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        probes: list[dict[str, Any]] = []
        for probes_item_data in self.probes:
            probes_item = probes_item_data.to_dict()
            probes.append(probes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "probes": probes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.activated_probe_result import (
            ActivatedProbeResult,  # noqa: PLC0415
        )

        d = RequiredFields(src_dict, cls.__name__)
        probes: list[ActivatedProbeResult] = []
        _probes = d.pop_required("probes")
        for probes_item_data in _probes:
            probes_item = ActivatedProbeResult.from_dict(probes_item_data)

            probes.append(probes_item)

        probe_activation_result = cls(
            probes=probes,
        )

        probe_activation_result.additional_properties = d
        return probe_activation_result

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
