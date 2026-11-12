"""Acceptance tests for the CAMUNDA_HTTP_MAX_CONNECTIONS configuration key.

Covers the full defect class: the key must resolve from the environment (and
from explicit configuration), validate as a positive integer, and be applied as
an ``httpx.Limits`` pool cap when the SDK builds its httpx clients — for both
the sync and the async client — while an explicit ``limits`` entry in
``httpx_args`` always takes precedence.
"""

import httpx
import pytest
from pydantic import ValidationError


@pytest.fixture(autouse=True)
def _clear_camunda_env(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    """Acceptance tests must not depend on the developer shell environment."""

    for key in (
        "CAMUNDA_REST_ADDRESS",
        "ZEEBE_REST_ADDRESS",
        "CAMUNDA_AUTH_STRATEGY",
        "CAMUNDA_CLIENT_ID",
        "CAMUNDA_CLIENT_SECRET",
        "CAMUNDA_BASIC_AUTH_USERNAME",
        "CAMUNDA_BASIC_AUTH_PASSWORD",
        "CAMUNDA_HTTP_MAX_CONNECTIONS",
    ):
        monkeypatch.delenv(key, raising=False)


def _pool_limits(
    httpx_client: httpx.Client | httpx.AsyncClient,
) -> tuple[int | None, int | None]:
    """Read (max_connections, max_keepalive_connections) off the httpx transport pool."""

    transport = getattr(httpx_client, "_transport", None)
    pool = getattr(transport, "_pool", None)
    if pool is None:
        return None, None
    return (
        getattr(pool, "_max_connections", None),
        getattr(pool, "_max_keepalive_connections", None),
    )


def test_max_connections_resolves_from_environment(monkeypatch: pytest.MonkeyPatch):
    from camunda_orchestration_sdk import CamundaClient

    monkeypatch.setenv("CAMUNDA_HTTP_MAX_CONNECTIONS", "25")

    client = CamundaClient()

    assert client.configuration.CAMUNDA_HTTP_MAX_CONNECTIONS == 25


def test_max_connections_resolves_from_explicit_configuration():
    from camunda_orchestration_sdk import CamundaClient

    client = CamundaClient(configuration={"CAMUNDA_HTTP_MAX_CONNECTIONS": "15"})

    assert client.configuration.CAMUNDA_HTTP_MAX_CONNECTIONS == 15


def test_max_connections_defaults_to_none():
    from camunda_orchestration_sdk import CamundaClient

    client = CamundaClient()

    assert client.configuration.CAMUNDA_HTTP_MAX_CONNECTIONS is None


@pytest.mark.parametrize("value", ["0", "-5", "not-a-number"])
def test_max_connections_rejects_invalid_values(
    monkeypatch: pytest.MonkeyPatch, value: str
):
    from camunda_orchestration_sdk import CamundaClient

    monkeypatch.setenv("CAMUNDA_HTTP_MAX_CONNECTIONS", value)

    with pytest.raises(ValidationError):
        CamundaClient()


def test_max_connections_applies_limits_to_sync_client(monkeypatch: pytest.MonkeyPatch):
    from camunda_orchestration_sdk import CamundaClient

    monkeypatch.setenv("CAMUNDA_HTTP_MAX_CONNECTIONS", "20")

    client = CamundaClient()
    httpx_client = client.client.get_httpx_client()

    assert _pool_limits(httpx_client) == (20, 20)


def test_max_connections_applies_limits_to_async_client(monkeypatch: pytest.MonkeyPatch):
    from camunda_orchestration_sdk import CamundaAsyncClient

    monkeypatch.setenv("CAMUNDA_HTTP_MAX_CONNECTIONS", "20")

    client = CamundaAsyncClient()
    httpx_client = client.client.get_async_httpx_client()

    assert _pool_limits(httpx_client) == (20, 20)


def test_explicit_httpx_args_limits_take_precedence(monkeypatch: pytest.MonkeyPatch):
    from camunda_orchestration_sdk import CamundaClient

    monkeypatch.setenv("CAMUNDA_HTTP_MAX_CONNECTIONS", "20")
    explicit_limits = httpx.Limits(max_connections=7, max_keepalive_connections=3)

    client = CamundaClient(httpx_args={"limits": explicit_limits})
    httpx_client = client.client.get_httpx_client()

    assert _pool_limits(httpx_client) == (7, 3)


def test_explicit_httpx_args_limits_take_precedence_async(
    monkeypatch: pytest.MonkeyPatch,
):
    from camunda_orchestration_sdk import CamundaAsyncClient

    monkeypatch.setenv("CAMUNDA_HTTP_MAX_CONNECTIONS", "20")
    explicit_limits = httpx.Limits(max_connections=7, max_keepalive_connections=3)

    client = CamundaAsyncClient(httpx_args={"limits": explicit_limits})
    httpx_client = client.client.get_async_httpx_client()

    assert _pool_limits(httpx_client) == (7, 3)


def test_no_limits_injected_when_unset():
    from camunda_orchestration_sdk import CamundaClient

    client = CamundaClient()
    httpx_client = client.client.get_httpx_client()

    # httpx defaults apply when the key is unset.
    assert _pool_limits(httpx_client) == (100, 20)
