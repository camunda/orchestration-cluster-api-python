"""Acceptance tests for the SDK ``User-Agent`` header (issue #476).

Gateway usage reports attribute traffic by the *first* product token in the
``User-Agent`` header. Every request the SDK sends -- generated REST
operations, raw requests through the underlying httpx client, and OAuth token
requests, for both the sync and the async client -- must therefore lead with
``camunda-orchestration-sdk-python/<version>``. An application-supplied user
agent (``CAMUNDA_USER_AGENT``) is appended, never replacing the SDK token.
"""

from __future__ import annotations

import importlib.metadata
from pathlib import Path
from typing import Any, cast

import httpx
import pytest

from camunda_orchestration_sdk.runtime.configuration_resolver import (
    CamundaSdkConfigPartial,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SDK_UA = "camunda-orchestration-sdk-python/" + importlib.metadata.version(
    "camunda-orchestration-sdk"
)

_TOPOLOGY = {
    "brokers": [],
    "clusterSize": 1,
    "partitionsCount": 1,
    "replicationFactor": 1,
    "gatewayVersion": "8.9.0",
    "lastCompletedChangeId": "-1",
    "clusterId": None,
}


@pytest.fixture(autouse=True)
def _clear_camunda_env(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    for key in (
        "CAMUNDA_REST_ADDRESS",
        "ZEEBE_REST_ADDRESS",
        "CAMUNDA_AUTH_STRATEGY",
        "CAMUNDA_CLIENT_ID",
        "CAMUNDA_CLIENT_SECRET",
        "CAMUNDA_OAUTH_URL",
        "CAMUNDA_TOKEN_AUDIENCE",
        "CAMUNDA_USER_AGENT",
        "CAMUNDA_LOAD_ENVFILE",
    ):
        monkeypatch.delenv(key, raising=False)


def _oauth_config(**extra: str) -> CamundaSdkConfigPartial:
    cfg: dict[str, Any] = {
        "CAMUNDA_REST_ADDRESS": "http://api.local/v2",
        "CAMUNDA_AUTH_STRATEGY": "OAUTH",
        "CAMUNDA_OAUTH_URL": "http://auth.local/oauth/token",
        "CAMUNDA_TOKEN_AUDIENCE": "aud",
        "CAMUNDA_CLIENT_ID": "id",
        "CAMUNDA_CLIENT_SECRET": "secret",
        "CAMUNDA_TOKEN_DISK_CACHE_DISABLE": "true",
    }
    cfg.update(extra)
    return cast(CamundaSdkConfigPartial, cfg)


def _recording_handler(seen: dict[str, list[str | None]]):
    def handler(request: httpx.Request) -> httpx.Response:
        ua = request.headers.get("User-Agent")
        if request.url.path == "/oauth/token":
            seen["token"].append(ua)
            return httpx.Response(200, json={"access_token": "t1", "expires_in": 3600})
        seen["rest"].append(ua)
        if request.url.path.endswith("/topology"):
            return httpx.Response(200, json=_TOPOLOGY)
        return httpx.Response(200, json={"ok": True})

    return handler


def _new_seen() -> dict[str, list[str | None]]:
    return {"token": [], "rest": []}


def test_sdk_user_agent_helper_uses_released_version() -> None:
    from camunda_orchestration_sdk.runtime.user_agent import (
        build_user_agent,
        sdk_user_agent,
    )

    assert sdk_user_agent() == SDK_UA
    assert build_user_agent(None) == SDK_UA
    assert build_user_agent("") == SDK_UA
    assert build_user_agent("  ") == SDK_UA
    assert build_user_agent("my-app/1.2") == f"{SDK_UA} my-app/1.2"


def test_sync_client_sends_sdk_user_agent_on_rest_and_token_requests() -> None:
    from camunda_orchestration_sdk import CamundaClient

    seen = _new_seen()
    transport = httpx.MockTransport(_recording_handler(seen))
    client = CamundaClient(
        configuration=_oauth_config(),
        httpx_args={"transport": transport},
    )

    client.get_topology()
    client.client.get_httpx_client().get("/ping")

    assert seen["token"] == [SDK_UA]
    assert seen["rest"] == [SDK_UA, SDK_UA]


@pytest.mark.asyncio
async def test_async_client_sends_sdk_user_agent_on_rest_and_token_requests() -> None:
    from camunda_orchestration_sdk import CamundaAsyncClient

    seen = _new_seen()
    transport = httpx.MockTransport(_recording_handler(seen))
    client = CamundaAsyncClient(
        configuration=_oauth_config(),
        httpx_args={"transport": transport},
    )

    await client.get_topology()
    await client.client.get_async_httpx_client().get("/ping")

    assert seen["token"] == [SDK_UA]
    assert seen["rest"] == [SDK_UA, SDK_UA]


def test_application_user_agent_from_env_is_appended(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from camunda_orchestration_sdk import CamundaClient

    monkeypatch.setenv("CAMUNDA_USER_AGENT", "my-app/1.2")
    seen = _new_seen()
    client = CamundaClient(
        configuration=_oauth_config(),
        httpx_args={"transport": httpx.MockTransport(_recording_handler(seen))},
    )

    assert client.configuration.CAMUNDA_USER_AGENT == "my-app/1.2"
    client.get_topology()

    assert seen["token"] == [f"{SDK_UA} my-app/1.2"]
    assert seen["rest"] == [f"{SDK_UA} my-app/1.2"]


@pytest.mark.asyncio
async def test_application_user_agent_from_configuration_is_appended_async() -> None:
    from camunda_orchestration_sdk import CamundaAsyncClient

    seen = _new_seen()
    client = CamundaAsyncClient(
        configuration=_oauth_config(CAMUNDA_USER_AGENT="my-app/1.2"),
        httpx_args={"transport": httpx.MockTransport(_recording_handler(seen))},
    )

    await client.get_topology()

    assert seen["token"] == [f"{SDK_UA} my-app/1.2"]
    assert seen["rest"] == [f"{SDK_UA} my-app/1.2"]


@pytest.mark.parametrize("header_name", ["User-Agent", "user-agent"])
def test_caller_supplied_user_agent_header_cannot_replace_sdk_token(
    header_name: str,
) -> None:
    from camunda_orchestration_sdk import CamundaClient

    seen = _new_seen()
    client = CamundaClient(
        configuration={
            "CAMUNDA_REST_ADDRESS": "http://api.local/v2",
            "CAMUNDA_AUTH_STRATEGY": "NONE",
        },
        headers={header_name: "custom/9"},
        httpx_args={"transport": httpx.MockTransport(_recording_handler(seen))},
    )

    client.get_topology()

    assert seen["rest"] == [f"{SDK_UA} custom/9"]


def test_dead_http_user_agent_generator_setting_removed() -> None:
    """openapi-python-client ignores ``httpUserAgent``; it must not mislead."""

    text = (REPO_ROOT / "generator-config.yaml").read_text()
    assert "httpUserAgent" not in text
