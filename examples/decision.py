# Compilable usage examples for decision evaluation and search.
# These examples are type-checked during build to guard against API regressions.
from __future__ import annotations

from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.models.decision_definition_search_query import (
    DecisionDefinitionSearchQuery,
)
from camunda_orchestration_sdk.models.decision_evaluation_by_id import (
    DecisionEvaluationByID,
)
from camunda_orchestration_sdk.models.decision_evaluation_by_key import (
    DecisionEvaluationByKey,
)
from camunda_orchestration_sdk.semantic_types import DecisionDefinitionId, DecisionDefinitionKey
from camunda_orchestration_sdk.types import Unset


# region EvaluateDecisionByKey
def evaluate_decision_by_key_example() -> None:
    client = CamundaClient()

    result = client.evaluate_decision(
        data=DecisionEvaluationByKey(
            decision_definition_key=DecisionDefinitionKey("123456"),
        )
    )

    print(f"Decision key: {result.decision_definition_key}")
# endregion EvaluateDecisionByKey


# region EvaluateDecisionById
def evaluate_decision_by_id_example() -> None:
    client = CamundaClient()

    result = client.evaluate_decision(
        data=DecisionEvaluationByID(
            decision_definition_id=DecisionDefinitionId("invoice-classification"),
        )
    )

    print(f"Decision key: {result.decision_definition_key}")
# endregion EvaluateDecisionById


# region SearchDecisionDefinitions
def search_decision_definitions_example() -> None:
    client = CamundaClient()

    result = client.search_decision_definitions(
        data=DecisionDefinitionSearchQuery()
    )

    if not isinstance(result.items, Unset):
        for definition in result.items:
            print(f"Decision: {definition.decision_definition_id}")
# endregion SearchDecisionDefinitions


# region GetDecisionDefinition
def get_decision_definition_example() -> None:
    client = CamundaClient()

    definition = client.get_decision_definition(
        decision_definition_key=DecisionDefinitionKey("123456")
    )

    print(f"Decision: {definition.decision_definition_id}")
# endregion GetDecisionDefinition
