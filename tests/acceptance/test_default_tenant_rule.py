"""Cross-SDK default-tenant rule (camunda/orchestration-cluster-api-python#449).

Mirrors the Camunda Java client:

1. Tenant-scoped commands send ``tenantId`` = effective default tenant
   (``CAMUNDA_TENANT_ID`` or ``"<default>"``) when the caller omits it.
2. ``activate_jobs`` sends ``tenantIds: [<effective default>]`` when
   ``tenantFilter`` is ``PROVIDED`` or unset and no tenant ids are passed;
   ``ASSIGNED`` leaves ``tenantIds`` alone.
3. An explicit per-call tenant always wins.
4. Searches never get a tenant added.

The behavioural tests run against *every* tenant-scoped command (sync and
async), so a newly added command that misses the rule is caught.
"""

from __future__ import annotations

import io
import json
from collections.abc import Callable
from typing import Any

import httpx
import pytest

from camunda_orchestration_sdk import CamundaAsyncClient, CamundaClient
from camunda_orchestration_sdk.models.signal_broadcast_request import (
    SignalBroadcastRequest,
)
from camunda_orchestration_sdk.models.conditional_evaluation_instruction import (
    ConditionalEvaluationInstruction,
)
from camunda_orchestration_sdk.models.conditional_evaluation_instruction_variables import (
    ConditionalEvaluationInstructionVariables,
)
from camunda_orchestration_sdk.models.create_deployment_data import (
    CreateDeploymentData,
)
from camunda_orchestration_sdk.models.decision_evaluation_by_id import (
    DecisionEvaluationByID,
)
from camunda_orchestration_sdk.models.decision_evaluation_by_key import (
    DecisionEvaluationByKey,
)
from camunda_orchestration_sdk.models.expression_evaluation_request import (
    ExpressionEvaluationRequest,
)
from camunda_orchestration_sdk.models.job_activation_request import (
    JobActivationRequest,
)
from camunda_orchestration_sdk.models.job_activation_request_tenant_filter import (
    JobActivationRequestTenantFilter,
)
from camunda_orchestration_sdk.models.message_correlation_request import (
    MessageCorrelationRequest,
)
from camunda_orchestration_sdk.models.message_publication_request import (
    MessagePublicationRequest,
)
from camunda_orchestration_sdk.models.process_creation_by_id import (
    ProcessCreationById,
)
from camunda_orchestration_sdk.models.process_creation_by_key import (
    ProcessCreationByKey,
)
from camunda_orchestration_sdk.models.process_creation_by_version_tag import (
    ProcessCreationByVersionTag,
)
from camunda_orchestration_sdk.models.process_instance_search_query import (
    ProcessInstanceSearchQuery,
)
from camunda_orchestration_sdk.semantic_types import (
    DecisionDefinitionId,
    DecisionDefinitionKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    TenantId,
)
from camunda_orchestration_sdk.types import UNSET, File

DEFAULT = "<default>"


@pytest.fixture(autouse=True)
def _clear_camunda_env(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    for key in ("CAMUNDA_TENANT_ID", "CAMUNDA_TENANT_IDS"):
        monkeypatch.delenv(key, raising=False)


def _handler(captured: dict[str, Any]) -> Callable[[httpx.Request], httpx.Response]:
    def handler(request: httpx.Request) -> httpx.Response:
        captured["content_type"] = request.headers.get("content-type", "")
        captured["raw"] = request.content
        try:
            captured["body"] = json.loads(request.content) if request.content else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            captured["body"] = None
        return httpx.Response(
            400,
            json={"type": "about:blank", "title": "x", "status": 400, "detail": "x"},
            headers={"content-type": "application/problem+json"},
        )

    return handler


def _sent_tenant(captured: dict[str, Any]) -> Any:
    body = captured.get("body")
    if body is not None:
        return body.get("tenantId")
    # multipart (create_deployment)
    raw: bytes = captured["raw"]
    marker = b'name="tenantId"'
    if marker not in raw:
        return None
    after = raw.split(marker, 1)[1].split(b"\r\n\r\n", 1)[1]
    return after.split(b"\r\n", 1)[0].decode()


# Each factory takes an optional explicit tenant and returns (method, data).
_Factory = Callable[[str | None], tuple[str, Any]]


def _t(tenant: str | None) -> Any:
    return TenantId(tenant) if tenant is not None else UNSET


TENANT_SCOPED: dict[str, _Factory] = {
    "create_deployment": lambda t: (
        "create_deployment",
        CreateDeploymentData(
            resources=[File(payload=io.BytesIO(b"<x/>"), file_name="a.bpmn")], tenant_id=_t(t)
        ),
    ),
    "create_process_instance_by_id": lambda t: (
        "create_process_instance",
        ProcessCreationById(process_definition_id=ProcessDefinitionId("p"), tenant_id=_t(t)),
    ),
    "create_process_instance_by_key": lambda t: (
        "create_process_instance",
        ProcessCreationByKey(process_definition_key=ProcessDefinitionKey("1"), tenant_id=_t(t)),
    ),
    "create_process_instance_by_version_tag": lambda t: (
        "create_process_instance",
        ProcessCreationByVersionTag(
            process_definition_id=ProcessDefinitionId("p"),
            process_definition_version_tag="v1",
            tenant_id=_t(t),
        ),
    ),
    "publish_message": lambda t: (
        "publish_message",
        MessagePublicationRequest(name="m", tenant_id=_t(t)),
    ),
    "correlate_message": lambda t: (
        "correlate_message",
        MessageCorrelationRequest(name="m", tenant_id=_t(t)),
    ),
    "broadcast_signal": lambda t: (
        "broadcast_signal",
        SignalBroadcastRequest(signal_name="s", tenant_id=_t(t)),
    ),
    "evaluate_decision_by_id": lambda t: (
        "evaluate_decision",
        DecisionEvaluationByID(decision_definition_id=DecisionDefinitionId("d"), tenant_id=_t(t)),
    ),
    "evaluate_decision_by_key": lambda t: (
        "evaluate_decision",
        DecisionEvaluationByKey(decision_definition_key=DecisionDefinitionKey("1"), tenant_id=_t(t)),
    ),
    "evaluate_expression": lambda t: (
        "evaluate_expression",
        ExpressionEvaluationRequest(expression="=1", tenant_id=_t(t)),
    ),
    "evaluate_conditionals": lambda t: (
        "evaluate_conditionals",
        ConditionalEvaluationInstruction(
            variables=ConditionalEvaluationInstructionVariables(), tenant_id=_t(t)
        ),
    ),
}


def _call_sync(client: CamundaClient, method: str, data: Any) -> None:
    try:
        getattr(client, method)(data=data)
    except Exception:
        pass


async def _call_async(client: CamundaAsyncClient, method: str, data: Any) -> None:
    try:
        await getattr(client, method)(data=data)
    except Exception:
        pass


@pytest.mark.parametrize("case", sorted(TENANT_SCOPED))
def test_unconfigured_sends_default_tenant(case: str) -> None:
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    method, data = TENANT_SCOPED[case](None)
    _call_sync(client, method, data)
    assert _sent_tenant(captured) == DEFAULT


@pytest.mark.parametrize("case", sorted(TENANT_SCOPED))
def test_configured_default_tenant_is_sent(case: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CAMUNDA_TENANT_ID", "tenant-a")
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    method, data = TENANT_SCOPED[case](None)
    _call_sync(client, method, data)
    assert _sent_tenant(captured) == "tenant-a"


@pytest.mark.parametrize("case", sorted(TENANT_SCOPED))
def test_explicit_tenant_wins(case: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CAMUNDA_TENANT_ID", "tenant-a")
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    method, data = TENANT_SCOPED[case]("explicit")
    _call_sync(client, method, data)
    assert _sent_tenant(captured) == "explicit"


@pytest.mark.asyncio
@pytest.mark.parametrize("case", sorted(TENANT_SCOPED))
async def test_async_unconfigured_sends_default_tenant(case: str) -> None:
    captured: dict[str, Any] = {}
    client = CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    method, data = TENANT_SCOPED[case](None)
    await _call_async(client, method, data)
    assert _sent_tenant(captured) == DEFAULT


def test_deploy_resources_from_files_unconfigured_sends_default(tmp_path: Any) -> None:
    f = tmp_path / "a.bpmn"
    f.write_text("<x/>")
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    try:
        client.deploy_resources_from_files([str(f)])
    except Exception:
        pass
    assert _sent_tenant(captured) == DEFAULT


# --- activate_jobs -------------------------------------------------------------


def _activate(client: CamundaClient, **kw: Any) -> None:
    _call_sync(
        client,
        "activate_jobs",
        JobActivationRequest(type_="t", timeout=1000, max_jobs_to_activate=1, **kw),
    )


@pytest.mark.parametrize(
    "kw",
    [
        {},
        {"tenant_ids": []},
        {"tenant_filter": JobActivationRequestTenantFilter.PROVIDED},
        {"tenant_filter": JobActivationRequestTenantFilter.PROVIDED, "tenant_ids": []},
    ],
)
def test_activate_jobs_unconfigured_sends_default_tenant_ids(kw: dict[str, Any]) -> None:
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    _activate(client, **kw)
    assert captured["body"]["tenantIds"] == [DEFAULT]


def test_activate_jobs_configured_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CAMUNDA_TENANT_ID", "tenant-a")
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    _activate(client)
    assert captured["body"]["tenantIds"] == ["tenant-a"]


def test_activate_jobs_explicit_wins() -> None:
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    _activate(client, tenant_ids=["x"])
    assert captured["body"]["tenantIds"] == ["x"]


def test_activate_jobs_assigned_filter_leaves_tenant_ids_alone() -> None:
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    _activate(client, tenant_filter=JobActivationRequestTenantFilter.ASSIGNED)
    assert "tenantIds" not in captured["body"]


# --- searches ------------------------------------------------------------------


def test_search_sends_no_tenant() -> None:
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    _call_sync(client, "search_process_instances", ProcessInstanceSearchQuery())
    assert "tenant" not in json.dumps(captured.get("body") or {}).lower()
