from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_definition_type_exact_match import AgentDefinitionTypeExactMatch
from ..types import UNSET, Unset, str_any_dict_factory

if TYPE_CHECKING:
    from ..models.advanced_agent_definition_key_filter import (
        AdvancedAgentDefinitionKeyFilter,
    )
    from ..models.advanced_agent_definition_type_filter import (
        AdvancedAgentDefinitionTypeFilter,
    )
    from ..models.advanced_element_id_filter import AdvancedElementIdFilter
    from ..models.advanced_integer_filter import AdvancedIntegerFilter
    from ..models.advanced_process_definition_id_filter import (
        AdvancedProcessDefinitionIdFilter,
    )
    from ..models.advanced_process_definition_key_filter import (
        AdvancedProcessDefinitionKeyFilter,
    )
    from ..models.advanced_string_filter import AdvancedStringFilter


T = TypeVar("T", bound="AgentDefinitionFilter")


@_attrs_define
class AgentDefinitionFilter:
    """Agent definition search filter.

    Attributes:
        agent_definition_key (AdvancedAgentDefinitionKeyFilter | str | Unset): The unique key of the agent definition.
        agent_type (AdvancedAgentDefinitionTypeFilter | AgentDefinitionTypeExactMatch | Unset): The kind of agent this
            agent definition describes.
        name (AdvancedStringFilter | str | Unset): The human-readable name of the process element that owns the agent
            definition.
        element_id (AdvancedElementIdFilter | str | Unset): The BPMN element ID of the process element that owns the
            agent definition.
        process_definition_id (AdvancedProcessDefinitionIdFilter | str | Unset): The BPMN process ID of the process
            definition that owns the agent definition.
        process_definition_key (AdvancedProcessDefinitionKeyFilter | str | Unset): The key of the process definition
            that owns the agent definition.
        process_definition_version (AdvancedIntegerFilter | int | Unset): The version of the process definition that
            owns the agent definition.
        process_definition_version_tag (AdvancedStringFilter | str | Unset): The version tag of the process definition
            that owns the agent definition.
        tenant_id (AdvancedStringFilter | str | Unset): The tenant ID of the agent definition.
    """

    agent_definition_key: AdvancedAgentDefinitionKeyFilter | str | Unset = UNSET
    agent_type: (
        AdvancedAgentDefinitionTypeFilter | AgentDefinitionTypeExactMatch | Unset
    ) = UNSET
    name: AdvancedStringFilter | str | Unset = UNSET
    element_id: AdvancedElementIdFilter | str | Unset = UNSET
    process_definition_id: AdvancedProcessDefinitionIdFilter | str | Unset = UNSET
    process_definition_key: AdvancedProcessDefinitionKeyFilter | str | Unset = UNSET
    process_definition_version: AdvancedIntegerFilter | int | Unset = UNSET
    process_definition_version_tag: AdvancedStringFilter | str | Unset = UNSET
    tenant_id: AdvancedStringFilter | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.advanced_agent_definition_key_filter import (
            AdvancedAgentDefinitionKeyFilter,
        )
        from ..models.advanced_element_id_filter import AdvancedElementIdFilter
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_process_definition_id_filter import (
            AdvancedProcessDefinitionIdFilter,
        )
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter

        agent_definition_key: dict[str, Any] | str | Unset
        if isinstance(self.agent_definition_key, Unset):
            agent_definition_key = UNSET
        elif isinstance(self.agent_definition_key, AdvancedAgentDefinitionKeyFilter):
            agent_definition_key = self.agent_definition_key.to_dict()
        else:
            agent_definition_key = self.agent_definition_key

        agent_type: dict[str, Any] | str | Unset
        if isinstance(self.agent_type, Unset):
            agent_type = UNSET
        elif isinstance(self.agent_type, AgentDefinitionTypeExactMatch):
            agent_type = self.agent_type.value
        else:
            agent_type = self.agent_type.to_dict()

        name: dict[str, Any] | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, AdvancedStringFilter):
            name = self.name.to_dict()
        else:
            name = self.name

        element_id: dict[str, Any] | str | Unset
        if isinstance(self.element_id, Unset):
            element_id = UNSET
        elif isinstance(self.element_id, AdvancedElementIdFilter):
            element_id = self.element_id.to_dict()
        else:
            element_id = self.element_id

        process_definition_id: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_id, Unset):
            process_definition_id = UNSET
        elif isinstance(self.process_definition_id, AdvancedProcessDefinitionIdFilter):
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

        process_definition_version: dict[str, Any] | int | Unset
        if isinstance(self.process_definition_version, Unset):
            process_definition_version = UNSET
        elif isinstance(self.process_definition_version, AdvancedIntegerFilter):
            process_definition_version = self.process_definition_version.to_dict()
        else:
            process_definition_version = self.process_definition_version

        process_definition_version_tag: dict[str, Any] | str | Unset
        if isinstance(self.process_definition_version_tag, Unset):
            process_definition_version_tag = UNSET
        elif isinstance(self.process_definition_version_tag, AdvancedStringFilter):
            process_definition_version_tag = (
                self.process_definition_version_tag.to_dict()
            )
        else:
            process_definition_version_tag = self.process_definition_version_tag

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
        if agent_definition_key is not UNSET:
            field_dict["agentDefinitionKey"] = agent_definition_key
        if agent_type is not UNSET:
            field_dict["agentType"] = agent_type
        if name is not UNSET:
            field_dict["name"] = name
        if element_id is not UNSET:
            field_dict["elementId"] = element_id
        if process_definition_id is not UNSET:
            field_dict["processDefinitionId"] = process_definition_id
        if process_definition_key is not UNSET:
            field_dict["processDefinitionKey"] = process_definition_key
        if process_definition_version is not UNSET:
            field_dict["processDefinitionVersion"] = process_definition_version
        if process_definition_version_tag is not UNSET:
            field_dict["processDefinitionVersionTag"] = process_definition_version_tag
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advanced_agent_definition_key_filter import (
            AdvancedAgentDefinitionKeyFilter,
        )
        from ..models.advanced_agent_definition_type_filter import (
            AdvancedAgentDefinitionTypeFilter,
        )
        from ..models.advanced_element_id_filter import AdvancedElementIdFilter
        from ..models.advanced_integer_filter import AdvancedIntegerFilter
        from ..models.advanced_process_definition_id_filter import (
            AdvancedProcessDefinitionIdFilter,
        )
        from ..models.advanced_process_definition_key_filter import (
            AdvancedProcessDefinitionKeyFilter,
        )
        from ..models.advanced_string_filter import AdvancedStringFilter

        d = dict(src_dict)

        def _parse_agent_definition_key(
            data: object,
        ) -> AdvancedAgentDefinitionKeyFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                agent_definition_key_type_1 = (
                    AdvancedAgentDefinitionKeyFilter.from_dict(data)
                )

                return agent_definition_key_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedAgentDefinitionKeyFilter | str | Unset, data)

        agent_definition_key = _parse_agent_definition_key(
            d.pop("agentDefinitionKey", UNSET)
        )

        def _parse_agent_type(
            data: object,
        ) -> AdvancedAgentDefinitionTypeFilter | AgentDefinitionTypeExactMatch | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                agent_type_type_0 = AgentDefinitionTypeExactMatch(data)

                return agent_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()

            data = cast(dict[str, Any], data)
            agent_type_type_1 = AdvancedAgentDefinitionTypeFilter.from_dict(data)

            return agent_type_type_1

        agent_type = _parse_agent_type(d.pop("agentType", UNSET))

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

        def _parse_process_definition_id(
            data: object,
        ) -> AdvancedProcessDefinitionIdFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_id_type_1 = (
                    AdvancedProcessDefinitionIdFilter.from_dict(data)
                )

                return process_definition_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedProcessDefinitionIdFilter | str | Unset, data)

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

        def _parse_process_definition_version_tag(
            data: object,
        ) -> AdvancedStringFilter | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()

                data = cast(dict[str, Any], data)
                process_definition_version_tag_type_1 = AdvancedStringFilter.from_dict(
                    data
                )

                return process_definition_version_tag_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AdvancedStringFilter | str | Unset, data)

        process_definition_version_tag = _parse_process_definition_version_tag(
            d.pop("processDefinitionVersionTag", UNSET)
        )

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

        agent_definition_filter = cls(
            agent_definition_key=agent_definition_key,
            agent_type=agent_type,
            name=name,
            element_id=element_id,
            process_definition_id=process_definition_id,
            process_definition_key=process_definition_key,
            process_definition_version=process_definition_version,
            process_definition_version_tag=process_definition_version_tag,
            tenant_id=tenant_id,
        )

        agent_definition_filter.additional_properties = d
        return agent_definition_filter

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
