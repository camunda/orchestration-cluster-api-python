"""Tests for default ``tenantIds[]`` injection.

Mirrors the structural / class-of-defect coverage applied by the JS SDK
(`camunda/orchestration-cluster-api-js#171`): every operation whose request
body exposes an *optional* plural ``tenantIds`` array must have the default
tenant injection block emitted by the post-gen flatten-client hook, so
multi-tenant workers don't silently poll without a tenant filter when
``CAMUNDA_TENANT_ID`` / ``CAMUNDA_TENANT_IDS`` is configured.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import httpx
import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_METADATA = REPO_ROOT / "external-spec" / "bundled" / "spec-metadata.json"
GENERATED_CLIENT = REPO_ROOT / "generated" / "camunda_orchestration_sdk" / "client.py"


@pytest.fixture(autouse=True)
def _clear_camunda_env(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    for key in ("CAMUNDA_TENANT_ID", "CAMUNDA_TENANT_IDS"):
        monkeypatch.delenv(key, raising=False)


def _snake(op_id: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", op_id)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _ops_with_optional_tenant_ids_body() -> list[str]:
    """Operations whose request body has an optional plural ``tenantIds`` array,
    per the bundler's spec-metadata.json (``optionalTenantIdsInBody``, issue #489)."""
    metadata = json.loads(SPEC_METADATA.read_text(encoding="utf-8"))
    found = {
        _snake(op["operationId"])
        for op in metadata.get("operations", [])
        if op.get("optionalTenantIdsInBody") and op.get("operationId")
    }
    return sorted(found)


def test_spec_has_at_least_one_op_with_optional_tenant_ids():
    """Guard: if upstream removes every op with optional tenantIds[],
    the structural test below would vacuously pass — fail loudly instead."""
    assert _ops_with_optional_tenant_ids_body(), (
        "Expected at least one operation with optional tenantIds[] in body. "
        "If the upstream spec genuinely removed every such operation, delete "
        "this guard and the injection logic; otherwise the metadata scanner is broken."
    )


def test_every_optional_tenant_ids_op_has_injection_block():
    """Class-of-defect guard: every operation with optional tenantIds[] must
    have the default-tenant-ids injection block in both sync and async impls."""
    client_src = GENERATED_CLIENT.read_text(encoding="utf-8")
    missing: list[str] = []
    for method in _ops_with_optional_tenant_ids_body():
        # Match the def + signature + (closely following) the injection block.
        # We assert each method's body contains the CAMUNDA_TENANT_IDS sentinel,
        # and that the sentinel appears at least twice in the file (sync + async).
        sync_pat = re.compile(
            rf"    def {re.escape(method)}\(.*?(?=\n    (?:def|async def) |\Z)",
            re.DOTALL,
        )
        async_pat = re.compile(
            rf"    async def {re.escape(method)}\(.*?(?=\n    (?:def|async def) |\Z)",
            re.DOTALL,
        )
        for kind, pat in (("sync", sync_pat), ("async", async_pat)):
            match = pat.search(client_src)
            if not match or "self.configuration.CAMUNDA_TENANT_IDS" not in match.group(0):
                missing.append(f"{kind}:{method}")
    assert not missing, (
        f"Missing default-tenant-ids injection block in: {missing}. "
        "The post-gen flatten-client hook (hooks/post_gen/0900_flatten_client.py) "
        "must inject _BODY_TENANT_IDS_INJECTION for every op with optional tenantIds[]."
    )


# --- Behavioral tests for activate_jobs ---------------------------------------


def _capture_handler(captured: dict[str, Any]):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.content:
            try:
                captured["body"] = json.loads(request.content)
            except json.JSONDecodeError:
                captured["body"] = None
        captured["url"] = str(request.url)
        return httpx.Response(
            200,
            json={"jobs": []},
            headers={"content-type": "application/json"},
        )

    return handler


def test_activate_jobs_injects_default_tenant_ids_from_singular_env(monkeypatch: pytest.MonkeyPatch):
    from camunda_orchestration_sdk import CamundaClient
    from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest

    monkeypatch.setenv("CAMUNDA_TENANT_ID", "tenant-a")
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_capture_handler(captured))})

    client.activate_jobs(data=JobActivationRequest(type_="payment", timeout=30000, max_jobs_to_activate=5))

    assert captured.get("body", {}).get("tenantIds") == ["tenant-a"]


def test_activate_jobs_injects_default_tenant_ids_from_plural_env(monkeypatch: pytest.MonkeyPatch):
    from camunda_orchestration_sdk import CamundaClient
    from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest

    monkeypatch.setenv("CAMUNDA_TENANT_IDS", "tenant-a,tenant-b")
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_capture_handler(captured))})

    client.activate_jobs(data=JobActivationRequest(type_="payment", timeout=30000, max_jobs_to_activate=5))

    assert captured.get("body", {}).get("tenantIds") == ["tenant-a", "tenant-b"]


def test_activate_jobs_preserves_explicit_tenant_ids(monkeypatch: pytest.MonkeyPatch):
    from camunda_orchestration_sdk import CamundaClient
    from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest

    monkeypatch.setenv("CAMUNDA_TENANT_IDS", "default-a,default-b")
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_capture_handler(captured))})

    client.activate_jobs(
        data=JobActivationRequest(
            type_="payment",
            timeout=30000,
            max_jobs_to_activate=5,
            tenant_ids=["explicit-x"],
        )
    )

    assert captured.get("body", {}).get("tenantIds") == ["explicit-x"]


def test_activate_jobs_no_default_injects_default_tenant():
    from camunda_orchestration_sdk import CamundaClient
    from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest

    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_capture_handler(captured))})

    client.activate_jobs(data=JobActivationRequest(type_="payment", timeout=30000, max_jobs_to_activate=5))

    # No tenant configured anywhere → effective default ``<default>`` (Java client parity, #449).
    assert captured.get("body", {}).get("tenantIds") == ["<default>"]


@pytest.mark.asyncio
async def test_activate_jobs_async_injects_default_tenant_ids(monkeypatch: pytest.MonkeyPatch):
    from camunda_orchestration_sdk import CamundaAsyncClient
    from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest

    monkeypatch.setenv("CAMUNDA_TENANT_IDS", "async-a,async-b")
    captured: dict[str, Any] = {}
    client = CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(_capture_handler(captured))})

    await client.activate_jobs(data=JobActivationRequest(type_="payment", timeout=30000, max_jobs_to_activate=5))

    assert captured.get("body", {}).get("tenantIds") == ["async-a", "async-b"]


# --- Blank singular tenant must not bypass the <default> fallback -----------


@pytest.mark.parametrize("blank", ["", "   "])
def test_blank_singular_tenant_id_resolves_to_unset(monkeypatch: pytest.MonkeyPatch, blank: str):
    monkeypatch.setenv("CAMUNDA_TENANT_ID", blank)
    monkeypatch.delenv("CAMUNDA_TENANT_IDS", raising=False)
    from camunda_orchestration_sdk import CamundaClient

    cfg = CamundaClient().configuration
    assert cfg.CAMUNDA_TENANT_ID is None
    assert cfg.CAMUNDA_TENANT_IDS is None


@pytest.mark.parametrize("blank", ["", "   "])
def test_activate_jobs_blank_singular_tenant_sends_default(monkeypatch: pytest.MonkeyPatch, blank: str):
    from camunda_orchestration_sdk import CamundaClient
    from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest

    monkeypatch.setenv("CAMUNDA_TENANT_ID", blank)
    monkeypatch.delenv("CAMUNDA_TENANT_IDS", raising=False)
    captured: dict[str, Any] = {}
    client = CamundaClient(httpx_args={"transport": httpx.MockTransport(_capture_handler(captured))})

    client.activate_jobs(data=JobActivationRequest(type_="payment", timeout=30000, max_jobs_to_activate=5))

    assert captured.get("body", {}).get("tenantIds") == ["<default>"]


@pytest.mark.parametrize("blank", ["", "   "])
@pytest.mark.asyncio
async def test_activate_jobs_async_blank_singular_tenant_sends_default(monkeypatch: pytest.MonkeyPatch, blank: str):
    from camunda_orchestration_sdk import CamundaAsyncClient
    from camunda_orchestration_sdk.models.job_activation_request import JobActivationRequest

    monkeypatch.setenv("CAMUNDA_TENANT_ID", blank)
    monkeypatch.delenv("CAMUNDA_TENANT_IDS", raising=False)
    captured: dict[str, Any] = {}
    client = CamundaAsyncClient(httpx_args={"transport": httpx.MockTransport(_capture_handler(captured))})

    await client.activate_jobs(data=JobActivationRequest(type_="payment", timeout=30000, max_jobs_to_activate=5))

    assert captured.get("body", {}).get("tenantIds") == ["<default>"]
