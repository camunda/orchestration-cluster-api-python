from __future__ import annotations
from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionId,
    DecisionDefinitionKey,
    DecisionEvaluationInstanceKey,
    DecisionEvaluationKey,
    ElementInstanceKey,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
)

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import str_any_dict_factory
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.decision_definition_type_enum import DecisionDefinitionTypeEnum
from ..models.decision_instance_state_enum import DecisionInstanceStateEnum

T = TypeVar("T", bound="DecisionInstanceResult")


@_attrs_define
class DecisionInstanceResult:
    """
    Attributes:
        decision_definition_id (str): The ID of the DMN decision. Example: new-hire-onboarding-workflow.
        decision_definition_key (str): The key of the decision. Example: 2251799813326547.
        decision_definition_name (str): The name of the DMN decision.
        decision_definition_type (DecisionDefinitionTypeEnum): The type of the decision. UNSPECIFIED is deprecated and
            should not be used anymore, for removal in 8.10
        decision_definition_version (int): The version of the decision.
        decision_evaluation_instance_key (str): System-generated key for a decision evaluation instance. Example:
            2251799813684367.
        decision_evaluation_key (str): The key of the decision evaluation where this instance was created. Example:
            2251792362345323.
        element_instance_key (None | str): The key of the element instance this decision instance is linked to. Example:
            2251799813686789.
        evaluation_date (datetime.datetime): The evaluation date of the decision instance.
        evaluation_failure (None | str): The evaluation failure of the decision instance.
        process_definition_key (None | str): The key of the process definition. Example: 2251799813686749.
        process_instance_key (None | str): The key of the process instance. Example: 2251799813690746.
        result (str): The result of the decision instance.
        root_decision_definition_key (str): The key of the root decision definition. Example: 2251799813326547.
        root_process_instance_key (None | str): The key of the root process instance. The root process instance is the
            top-level
            ancestor in the process instance hierarchy. This field is only present for data
            belonging to process instance hierarchies created in version 8.9 or later.
             Example: 2251799813690746.
        state (DecisionInstanceStateEnum): The state of the decision instance. UNSPECIFIED and UNKNOWN are deprecated
            and should not be used anymore, for removal in 8.10
        tenant_id (str): The tenant ID of the decision instance. Example: customer-service.
    """

    decision_definition_id: DecisionDefinitionId
    decision_definition_key: DecisionDefinitionKey
    decision_definition_name: str
    decision_definition_type: DecisionDefinitionTypeEnum
    decision_definition_version: int
    decision_evaluation_instance_key: DecisionEvaluationInstanceKey
    decision_evaluation_key: DecisionEvaluationKey
    element_instance_key: None | ElementInstanceKey
    evaluation_date: datetime.datetime
    evaluation_failure: None | str
    process_definition_key: None | ProcessDefinitionKey
    process_instance_key: None | ProcessInstanceKey
    result: str
    root_decision_definition_key: DecisionDefinitionKey
    root_process_instance_key: None | ProcessInstanceKey
    state: DecisionInstanceStateEnum
    tenant_id: TenantId
    additional_properties: dict[str, Any] = _attrs_field(
        init=False, factory=str_any_dict_factory
    )

    def to_dict(self) -> dict[str, Any]:
        decision_definition_id = self.decision_definition_id

        decision_definition_key = self.decision_definition_key

        decision_definition_name = self.decision_definition_name

        decision_definition_type = self.decision_definition_type.value

        decision_definition_version = self.decision_definition_version

        decision_evaluation_instance_key = self.decision_evaluation_instance_key

        decision_evaluation_key = self.decision_evaluation_key

        element_instance_key: None | ElementInstanceKey
        element_instance_key = self.element_instance_key

        evaluation_date = self.evaluation_date.isoformat()

        evaluation_failure: None | str
        evaluation_failure = self.evaluation_failure

        process_definition_key: None | ProcessDefinitionKey
        process_definition_key = self.process_definition_key

        process_instance_key: None | ProcessInstanceKey
        process_instance_key = self.process_instance_key

        result = self.result

        root_decision_definition_key = self.root_decision_definition_key

        root_process_instance_key: None | ProcessInstanceKey
        root_process_instance_key = self.root_process_instance_key

        state = self.state.value

        tenant_id = self.tenant_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "decisionDefinitionId": decision_definition_id,
                "decisionDefinitionKey": decision_definition_key,
                "decisionDefinitionName": decision_definition_name,
                "decisionDefinitionType": decision_definition_type,
                "decisionDefinitionVersion": decision_definition_version,
                "decisionEvaluationInstanceKey": decision_evaluation_instance_key,
                "decisionEvaluationKey": decision_evaluation_key,
                "elementInstanceKey": element_instance_key,
                "evaluationDate": evaluation_date,
                "evaluationFailure": evaluation_failure,
                "processDefinitionKey": process_definition_key,
                "processInstanceKey": process_instance_key,
                "result": result,
                "rootDecisionDefinitionKey": root_decision_definition_key,
                "rootProcessInstanceKey": root_process_instance_key,
                "state": state,
                "tenantId": tenant_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        decision_definition_id = DecisionDefinitionId(d.pop("decisionDefinitionId"))

        decision_definition_key = DecisionDefinitionKey(d.pop("decisionDefinitionKey"))

        decision_definition_name = d.pop("decisionDefinitionName")

        decision_definition_type = DecisionDefinitionTypeEnum(
            d.pop("decisionDefinitionType")
        )

        decision_definition_version = d.pop("decisionDefinitionVersion")

        decision_evaluation_instance_key = DecisionEvaluationInstanceKey(
            d.pop("decisionEvaluationInstanceKey")
        )

        decision_evaluation_key = DecisionEvaluationKey(d.pop("decisionEvaluationKey"))

        def _parse_element_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_element_instance_key = _parse_element_instance_key(
            d.pop("elementInstanceKey")
        )

        element_instance_key = (
            ElementInstanceKey(_raw_element_instance_key)
            if isinstance(_raw_element_instance_key, str)
            else _raw_element_instance_key
        )

        evaluation_date = isoparse(d.pop("evaluationDate"))

        def _parse_evaluation_failure(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        evaluation_failure = _parse_evaluation_failure(d.pop("evaluationFailure"))

        def _parse_process_definition_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_definition_key = _parse_process_definition_key(
            d.pop("processDefinitionKey")
        )

        process_definition_key = (
            ProcessDefinitionKey(_raw_process_definition_key)
            if isinstance(_raw_process_definition_key, str)
            else _raw_process_definition_key
        )

        def _parse_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_process_instance_key = _parse_process_instance_key(
            d.pop("processInstanceKey")
        )

        process_instance_key = (
            ProcessInstanceKey(_raw_process_instance_key)
            if isinstance(_raw_process_instance_key, str)
            else _raw_process_instance_key
        )

        result = d.pop("result")

        root_decision_definition_key = d.pop("rootDecisionDefinitionKey")

        def _parse_root_process_instance_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        _raw_root_process_instance_key = _parse_root_process_instance_key(
            d.pop("rootProcessInstanceKey")
        )

        root_process_instance_key = (
            ProcessInstanceKey(_raw_root_process_instance_key)
            if isinstance(_raw_root_process_instance_key, str)
            else _raw_root_process_instance_key
        )

        state = DecisionInstanceStateEnum(d.pop("state"))

        tenant_id = TenantId(d.pop("tenantId"))

        decision_instance_result = cls(
            decision_definition_id=decision_definition_id,
            decision_definition_key=decision_definition_key,
            decision_definition_name=decision_definition_name,
            decision_definition_type=decision_definition_type,
            decision_definition_version=decision_definition_version,
            decision_evaluation_instance_key=decision_evaluation_instance_key,
            decision_evaluation_key=decision_evaluation_key,
            element_instance_key=element_instance_key,
            evaluation_date=evaluation_date,
            evaluation_failure=evaluation_failure,
            process_definition_key=process_definition_key,
            process_instance_key=process_instance_key,
            result=result,
            root_decision_definition_key=root_decision_definition_key,
            root_process_instance_key=root_process_instance_key,
            state=state,
            tenant_id=tenant_id,
        )

        decision_instance_result.additional_properties = d
        return decision_instance_result

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
