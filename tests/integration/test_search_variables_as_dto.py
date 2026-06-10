"""Integration tests for the DTO-driven variable search (issue #144).

Mirrors the TypeScript SDK's ``searchVariablesAsDto`` integration coverage:
exercises the eventual-consistency wait against a live cluster, where a
freshly-created process instance's variables are not immediately visible to the
variable index.
"""

import os
from typing import cast

import pytest
from pydantic import BaseModel, ValidationError

from camunda_orchestration_sdk import (
    CamundaAsyncClient,
    ConsistencyOptions,
    CreateDeploymentData,
    DeploymentProcessResult,
    File,
    ProcessCreationByKey,
    ProcessInstanceCreationInstructionByKeyVariables,
)

pytestmark = pytest.mark.skipif(
    os.environ.get("CAMUNDA_INTEGRATION") != "1",
    reason="Integration tests are disabled unless CAMUNDA_INTEGRATION=1",
)

_BPMN_PATH = "./tests/integration/resources/typed_variables_test_process.bpmn"


def _make_client() -> CamundaAsyncClient:
    return CamundaAsyncClient()


async def _deploy_process_definition_key(camunda: CamundaAsyncClient) -> str:
    with open(_BPMN_PATH, "rb") as f:
        process_file = File(payload=f, file_name="typed_variables_test_process.bpmn")
        deployed = await camunda.create_deployment(
            data=CreateDeploymentData(resources=[process_file])
        )
    process_definition = cast(
        DeploymentProcessResult, deployed.deployments[0].process_definition
    )
    return str(process_definition.process_definition_key)


@pytest.mark.asyncio
async def test_search_variables_as_dto_finds_declared_variables() -> None:
    async with _make_client() as camunda:
        process_definition_key = await _deploy_process_definition_key(camunda)

        # The process waits at a service task, so its variables persist on the
        # running instance for the duration of the search.
        variables = ProcessInstanceCreationInstructionByKeyVariables()
        variables["order_id"] = "ord-1"
        variables["amount"] = 42
        # An extra variable that is not declared on the DTO and must be ignored.
        variables["internal_secret"] = "do-not-leak"

        instance = await camunda.create_process_instance(
            data=ProcessCreationByKey(
                process_definition_key=process_definition_key,
                variables=variables,
            )
        )
        process_instance_key = instance.process_instance_key

        try:

            class OrderVars(BaseModel):
                order_id: str
                amount: float | None = None

            # Variables are eventually consistent on a freshly-created instance,
            # so wait until every declared variable is visible.
            result = await camunda.search_variables_as_dto(
                OrderVars,
                process_instance_key=str(process_instance_key),
                consistency=ConsistencyOptions(wait_up_to_ms=10_000),
            )

            assert "order_id" in result
            assert "amount" in result
            assert result.get("order_id") == "ord-1"
            assert result.get("amount") == 42

            # Only the declared variables are queried — the extra one is never
            # fetched.
            assert "internal_secret" not in result
            assert sorted(result.raw.keys()) == ["amount", "order_id"]

            # Strict access returns a fully-typed, validated model.
            order = result.validate()
            assert order.order_id == "ord-1"
            assert order.amount == 42
        finally:
            await camunda.cancel_process_instance(
                data=None, process_instance_key=process_instance_key
            )


@pytest.mark.asyncio
async def test_search_variables_as_dto_validate_raises_on_missing_required() -> None:
    async with _make_client() as camunda:
        process_definition_key = await _deploy_process_definition_key(camunda)

        variables = ProcessInstanceCreationInstructionByKeyVariables()
        variables["order_id"] = "ord-1"

        instance = await camunda.create_process_instance(
            data=ProcessCreationByKey(
                process_definition_key=process_definition_key,
                variables=variables,
            )
        )
        process_instance_key = instance.process_instance_key

        try:

            class OrderVars(BaseModel):
                order_id: str
                # Declared but never set on the instance, so absent at runtime.
                customer_id: str

            result = await camunda.search_variables_as_dto(
                OrderVars,
                process_instance_key=str(process_instance_key),
                consistency=ConsistencyOptions(wait_up_to_ms=10_000),
            )

            # The declared-but-absent variable is simply missing — lenient
            # access never raises.
            assert "order_id" in result
            assert "customer_id" not in result

            # Strict validation fails because a required variable is missing.
            with pytest.raises(ValidationError):
                result.validate()
        finally:
            await camunda.cancel_process_instance(
                data=None, process_instance_key=process_instance_key
            )
