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
import re
from pathlib import Path
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
from camunda_orchestration_sdk.models.process_definition_resumption_by_id import (
    ProcessDefinitionResumptionByID,
)
from camunda_orchestration_sdk.models.process_definition_resumption_by_key import (
    ProcessDefinitionResumptionByKey,
)
from camunda_orchestration_sdk.models.process_definition_suspension_by_id import (
    ProcessDefinitionSuspensionByID,
)
from camunda_orchestration_sdk.models.process_definition_suspension_by_key import (
    ProcessDefinitionSuspensionByKey,
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

TENANT_SCOPED.update(
    {
        "resume_process_definitions_by_id": lambda t: (
            "resume_process_definitions",
            ProcessDefinitionResumptionByID(process_definition_id=ProcessDefinitionId("p"), tenant_id=_t(t)),
        ),
        "suspend_process_definitions_by_id": lambda t: (
            "suspend_process_definitions",
            ProcessDefinitionSuspensionByID(process_definition_id=ProcessDefinitionId("p"), tenant_id=_t(t)),
        ),
    }
)


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


# --- caller requests are never mutated by default-tenant injection --------------
# Class guard: injecting the default must not write into the caller's request
# object, otherwise reusing it with a differently-configured client sends the
# first client's default instead of the second one's.


def _client_for(captured: dict[str, Any], monkeypatch: pytest.MonkeyPatch, tenant: str | None) -> CamundaClient:
    if tenant is None:
        monkeypatch.delenv("CAMUNDA_TENANT_ID", raising=False)
    else:
        monkeypatch.setenv("CAMUNDA_TENANT_ID", tenant)
    return CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})


@pytest.mark.parametrize("case", sorted(TENANT_SCOPED))
def test_injection_does_not_mutate_caller_request(case: str, monkeypatch: pytest.MonkeyPatch) -> None:
    method, data = TENANT_SCOPED[case](None)
    first: dict[str, Any] = {}
    _call_sync(_client_for(first, monkeypatch, None), method, data)
    assert _sent_tenant(first) == DEFAULT
    assert data.tenant_id is UNSET
    second: dict[str, Any] = {}
    _call_sync(_client_for(second, monkeypatch, "tenant-a"), method, data)
    assert _sent_tenant(second) == "tenant-a"


@pytest.mark.asyncio
@pytest.mark.parametrize("case", sorted(TENANT_SCOPED))
async def test_async_injection_does_not_mutate_caller_request(case: str, monkeypatch: pytest.MonkeyPatch) -> None:
    method, data = TENANT_SCOPED[case](None)
    first: dict[str, Any] = {}
    await _call_async(
        CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(_handler(first))}), method, data
    )
    assert _sent_tenant(first) == DEFAULT
    assert data.tenant_id is UNSET
    monkeypatch.setenv("CAMUNDA_TENANT_ID", "tenant-a")
    second: dict[str, Any] = {}
    await _call_async(
        CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(_handler(second))}), method, data
    )
    assert _sent_tenant(second) == "tenant-a"


def test_activate_jobs_injection_does_not_mutate_caller_request(monkeypatch: pytest.MonkeyPatch) -> None:
    req = JobActivationRequest(type_="t", timeout=1000, max_jobs_to_activate=1)
    first: dict[str, Any] = {}
    _call_sync(_client_for(first, monkeypatch, None), "activate_jobs", req)
    assert first["body"]["tenantIds"] == [DEFAULT]
    assert req.tenant_ids is UNSET
    second: dict[str, Any] = {}
    _call_sync(_client_for(second, monkeypatch, "tenant-a"), "activate_jobs", req)
    assert second["body"]["tenantIds"] == ["tenant-a"]


@pytest.mark.asyncio
async def test_async_activate_jobs_injection_does_not_mutate_caller_request(monkeypatch: pytest.MonkeyPatch) -> None:
    req = JobActivationRequest(type_="t", timeout=1000, max_jobs_to_activate=1)
    first: dict[str, Any] = {}
    await _call_async(
        CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(_handler(first))}), "activate_jobs", req
    )
    assert first["body"]["tenantIds"] == [DEFAULT]
    assert req.tenant_ids is UNSET
    monkeypatch.setenv("CAMUNDA_TENANT_ID", "tenant-a")
    second: dict[str, Any] = {}
    await _call_async(
        CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(_handler(second))}), "activate_jobs", req
    )
    assert second["body"]["tenantIds"] == ["tenant-a"]


# --- suspend/resume process definitions (issue #482) -------------------------
# By-id bodies carry an optional tenantId and get the effective default; by-key
# bodies have no tenantId and must get nothing.

BY_KEY: dict[str, Callable[[], tuple[str, Any]]] = {
    "resume_process_definitions_by_key": lambda: (
        "resume_process_definitions",
        ProcessDefinitionResumptionByKey(process_definition_key=ProcessDefinitionKey("1")),
    ),
    "suspend_process_definitions_by_key": lambda: (
        "suspend_process_definitions",
        ProcessDefinitionSuspensionByKey(process_definition_key=ProcessDefinitionKey("1")),
    ),
}


@pytest.mark.parametrize("tenant", [None, "tenant-a"])
@pytest.mark.parametrize("case", sorted(BY_KEY))
def test_by_key_variant_gets_no_tenant(case: str, tenant: str | None, monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}
    method, data = BY_KEY[case]()
    _call_sync(_client_for(captured, monkeypatch, tenant), method, data)
    assert captured.get("body") is not None
    assert "tenantId" not in captured["body"]


# --- spec-derived class guard ------------------------------------------------
# Every operation whose request body (any union variant) has an optional
# top-level tenantId must fall back to the effective default tenant, in both
# clients. Derived from the bundled spec, not a list, so a new tenant-scoped
# operation that misses injection fails here.

_SPEC = Path(__file__).resolve().parents[2] / "external-spec" / "bundled" / "rest-api.bundle.json"


def _ops_with_optional_body_tenant(spec: dict[str, Any] | None = None) -> set[str]:
    if spec is None:
        spec = json.loads(_SPEC.read_text())
    assert spec is not None

    def resolve(schema: dict[str, Any]) -> dict[str, Any]:
        while "$ref" in schema:
            node: Any = spec
            for p in schema["$ref"].lstrip("#/").split("/"):
                node = node[p]
            schema = node
        return schema

    def variants(schema: dict[str, Any], depth: int = 0) -> list[dict[str, Any]]:
        schema = resolve(schema)
        nested = schema.get("oneOf", []) + schema.get("anyOf", [])
        if not nested or depth > 5:
            return [schema]
        out = [schema]
        for v in nested:
            out += variants(v, depth + 1)
        return out

    def collect_all_of(schema: dict[str, Any], props: dict[str, Any], required: set[str], depth: int = 0) -> None:
        # Walk every allOf ancestor, not just direct parents (Body -> Mid -> Base).
        schema = resolve(schema)
        if depth > 10:
            return
        for part in schema.get("allOf", []):
            collect_all_of(part, props, required, depth + 1)
        props.update(schema.get("properties", {}))
        required.update(schema.get("required", []))

    ops: set[str] = set()
    for methods in spec.get("paths", {}).values():
        for op in methods.values():
            if not isinstance(op, dict) or "operationId" not in op:
                continue
            for ct in op.get("requestBody", {}).get("content", {}).values():
                for v in variants(ct.get("schema", {})):
                    props: dict[str, Any] = {}
                    required: set[str] = set()
                    collect_all_of(v, props, required)
                    if "tenantId" in props and "tenantId" not in required:
                        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", op["operationId"])
                        ops.add(re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower())
    return ops


def test_every_optional_body_tenant_op_falls_back_to_default_tenant() -> None:
    import ast
    import inspect

    import camunda_orchestration_sdk.client as client_mod

    expected = _ops_with_optional_body_tenant()
    assert {"suspend_process_definitions", "resume_process_definitions", "create_process_instance"} <= expected
    tree = ast.parse(inspect.getsource(client_mod))
    missing: list[str] = []
    for cls in tree.body:
        if isinstance(cls, ast.ClassDef) and cls.name in ("CamundaClient", "CamundaAsyncClient"):
            fns = {
                fn.name: ast.unparse(fn)
                for fn in cls.body
                if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
            for op in sorted(expected):
                if "CAMUNDA_TENANT_ID or DEFAULT_TENANT_ID" not in fns.get(op, ""):
                    missing.append(f"{cls.name}.{op}")
    assert not missing, f"operations with optional body tenantId lack default-tenant injection: {missing}"


def _nested_all_of_spec(base_required: list[str]) -> dict[str, Any]:
    return {
        "paths": {
            "/x": {"post": {"operationId": "doNestedThing", "requestBody": {"content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Body"}}}}}}
        },
        "components": {"schemas": {
            "Body": {"allOf": [{"$ref": "#/components/schemas/Mid"}], "properties": {"a": {"type": "string"}}},
            "Mid": {"allOf": [{"$ref": "#/components/schemas/Base"}]},
            "Base": {"properties": {"tenantId": {"type": "string"}}, "required": base_required},
        }},
    }


def _hook_compute_body_tenant_ops(spec: dict[str, Any], tmp_path: Path) -> set[str]:
    import importlib.util

    hook = Path(__file__).resolve().parents[2] / "hooks" / "post_gen" / "0900_flatten_client.py"
    mod_spec = importlib.util.spec_from_file_location("_flatten_client_hook", hook)
    assert mod_spec is not None and mod_spec.loader is not None
    mod = importlib.util.module_from_spec(mod_spec)
    import sys

    sys.path.insert(0, str(hook.parent))
    try:
        mod_spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(hook.parent))
    f = tmp_path / "spec.json"
    f.write_text(json.dumps(spec))
    return set(mod._compute_body_tenant_ops(f))


@pytest.mark.parametrize("detector", ["guard", "hook"])
def test_nested_all_of_tenant_is_detected(detector: str, tmp_path: Path) -> None:
    def run(spec: dict[str, Any]) -> set[str]:
        if detector == "guard":
            return _ops_with_optional_body_tenant(spec)
        return _hook_compute_body_tenant_ops(spec, tmp_path)

    assert run(_nested_all_of_spec([])) == {"do_nested_thing"}
    assert run(_nested_all_of_spec(["tenantId"])) == set()


# --- dict-shaped bodies (issue #483) -------------------------------------------
#
# Request bodies are typed models; dict bodies are not part of the API. The
# injection must never rebuild a body into a plain ``dict`` (which lacks
# ``to_dict()`` and crashes ``_get_kwargs``). A mapping-like body that carries
# its own ``to_dict()`` must therefore reach the transport unchanged.


class _DictBody(dict[str, Any]):
    def to_dict(self) -> dict[str, Any]:
        return dict(self)


def _dict_body_cases() -> list[str]:
    return sorted(c for c in TENANT_SCOPED if c != "create_deployment")


@pytest.mark.parametrize("case", _dict_body_cases())
def test_dict_body_with_to_dict_is_not_rebuilt(case: str) -> None:
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    method, data = TENANT_SCOPED[case](None)
    try:
        getattr(client, method)(data=_DictBody(data.to_dict()))
    except AttributeError as e:  # pragma: no cover - the regression
        pytest.fail(f"{method} crashed on a dict-shaped body: {e}")
    except Exception:
        pass
    assert "body" in captured, f"{method} never reached the transport"


def test_activate_jobs_dict_body_with_to_dict_is_not_rebuilt() -> None:
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_handler(captured))})
    body = _DictBody(JobActivationRequest(type_="t", timeout=1, max_jobs_to_activate=1).to_dict())
    try:
        getattr(client, "activate_jobs")(data=body)  # noqa: B009 - bypass static typing on purpose
    except AttributeError as e:  # pragma: no cover - the regression
        pytest.fail(f"activate_jobs crashed on a dict-shaped body: {e}")
    except Exception:
        pass
    assert "body" in captured


def test_generated_client_never_rebuilds_dict_bodies() -> None:
    import inspect

    import camunda_orchestration_sdk.client as client_mod

    src = inspect.getsource(client_mod)
    assert "isinstance(_body, dict)" not in src
