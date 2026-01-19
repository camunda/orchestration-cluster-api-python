import base64

import httpx
import pytest


class _StaticAuthProvider:
    def __init__(self, header_value: str):
        self.header_value = header_value
        self.calls = 0

    def get_headers(self) -> dict[str, str]:
        self.calls += 1
        return {"X-Test-Auth": self.header_value}


def test_auth_headers_applied_sync():
    from camunda_orchestration_sdk import CamundaClient

    seen: dict[str, str | None] = {"x_test_auth": None}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["x_test_auth"] = request.headers.get("X-Test-Auth")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    auth = _StaticAuthProvider("sync")

    client = CamundaClient(auth_provider=auth, httpx_args={"transport": transport})
    response = client.client.get_httpx_client().get("/ping")

    assert response.status_code == 200
    assert seen["x_test_auth"] == "sync"
    assert auth.calls == 1


def test_null_auth_provider_default_sync():
    from camunda_orchestration_sdk import CamundaClient

    seen: dict[str, str | None] = {"x_test_auth": None}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["x_test_auth"] = request.headers.get("X-Test-Auth")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)

    client = CamundaClient(httpx_args={"transport": transport})
    response = client.client.get_httpx_client().get("/ping")

    assert response.status_code == 200
    assert seen["x_test_auth"] is None


@pytest.mark.asyncio
async def test_auth_headers_applied_async():
    from camunda_orchestration_sdk import CamundaAsyncClient

    seen: dict[str, str | None] = {"x_test_auth": None}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["x_test_auth"] = request.headers.get("X-Test-Auth")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    auth = _StaticAuthProvider("async")

    client = CamundaAsyncClient(auth_provider=auth, httpx_args={"transport": transport})
    response = await client.client.get_async_httpx_client().get("/ping")

    assert response.status_code == 200
    assert seen["x_test_auth"] == "async"
    assert auth.calls == 1


def test_builtin_basic_auth_strategy_applies_authorization_header_sync():
    from camunda_orchestration_sdk import CamundaClient

    seen: dict[str, str | None] = {"authorization": None}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/ping"):
            seen["authorization"] = request.headers.get("Authorization")
            return httpx.Response(200, json={"ok": True})
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    token = base64.b64encode(b"u:p").decode("ascii")
    config = {
        "CAMUNDA_REST_ADDRESS": "http://api.local/v2",
        "CAMUNDA_AUTH_STRATEGY": "BASIC",
        "CAMUNDA_BASIC_AUTH_USERNAME": "u",
        "CAMUNDA_BASIC_AUTH_PASSWORD": "p",
    }

    client = CamundaClient(configuration=config, httpx_args={"transport": transport})
    response = client.client.get_httpx_client().get("/ping")

    assert response.status_code == 200
    assert seen["authorization"] == f"Basic {token}"


def test_builtin_oauth_strategy_applies_bearer_header_sync():
    from camunda_orchestration_sdk import CamundaClient

    seen: dict[str, str | None] = {"authorization": None}
    token_calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/oauth/token":
            token_calls["count"] += 1
            return httpx.Response(200, json={"access_token": "t1", "expires_in": 3600})
        if request.url.path.endswith("/ping"):
            seen["authorization"] = request.headers.get("Authorization")
            return httpx.Response(200, json={"ok": True})
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    config = {
        "CAMUNDA_REST_ADDRESS": "http://api.local/v2",
        "CAMUNDA_AUTH_STRATEGY": "OAUTH",
        "CAMUNDA_OAUTH_URL": "http://auth.local/oauth/token",
        "CAMUNDA_TOKEN_AUDIENCE": "aud",
        "CAMUNDA_CLIENT_ID": "id",
        "CAMUNDA_CLIENT_SECRET": "secret",
    }

    client = CamundaClient(configuration=config, httpx_args={"transport": transport})
    response = client.client.get_httpx_client().get("/ping")

    assert response.status_code == 200
    assert seen["authorization"] == "Bearer t1"
    assert token_calls["count"] == 1


def test_oauth_401_is_memoized_to_avoid_repeated_token_requests_sync() -> None:
    from camunda_orchestration_sdk.runtime.auth import OAuthClientCredentialsAuthProvider

    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(401, json={"error": "invalid_client"}, request=request)

    transport = httpx.MockTransport(handler)
    provider = OAuthClientCredentialsAuthProvider(
        oauth_url="https://login.cloud.camunda.io/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        transport=transport,
    )

    with pytest.raises(httpx.HTTPStatusError):
        provider.get_headers()
    with pytest.raises(httpx.HTTPStatusError):
        provider.get_headers()

    assert calls["count"] == 1


def test_oauth_401_tarpit_file_prevents_subsequent_requests_when_file_cache_enabled_sync(tmp_path) -> None:
    from camunda_orchestration_sdk.runtime.auth import OAuthClientCredentialsAuthProvider

    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(401, json={"error": "invalid_client"}, request=request)

    transport = httpx.MockTransport(handler)
    provider = OAuthClientCredentialsAuthProvider(
        oauth_url="https://login.cloud.camunda.io/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=transport,
    )

    with pytest.raises(httpx.HTTPStatusError):
        provider.get_headers()

    tarpit_files = list(tmp_path.glob("oauth-401-tarpit-*.json"))
    assert len(tarpit_files) >= 1

    calls["count"] = 0

    def handler_should_not_run(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(500, json={"unexpected": True}, request=request)

    provider2 = OAuthClientCredentialsAuthProvider(
        oauth_url="https://login.cloud.camunda.io/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(handler_should_not_run),
    )

    with pytest.raises(RuntimeError):
        provider2.get_headers()

    assert calls["count"] == 0


def test_oauth_token_is_cached_to_disk_and_reused_sync(tmp_path) -> None:
    from camunda_orchestration_sdk.runtime.auth import OAuthClientCredentialsAuthProvider

    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(200, json={"access_token": "t1", "expires_in": 3600}, request=request)

    provider = OAuthClientCredentialsAuthProvider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(handler),
    )

    assert provider.get_headers()["Authorization"] == "Bearer t1"
    assert calls["count"] == 1

    calls["count"] = 0

    def handler_should_not_run(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(500, json={"unexpected": True}, request=request)

    provider2 = OAuthClientCredentialsAuthProvider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(handler_should_not_run),
    )

    assert provider2.get_headers()["Authorization"] == "Bearer t1"
    assert calls["count"] == 0


@pytest.mark.asyncio
async def test_builtin_oauth_strategy_applies_bearer_header_async():
    from camunda_orchestration_sdk import CamundaAsyncClient

    seen: dict[str, str | None] = {"authorization": None}
    token_calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/oauth/token":
            token_calls["count"] += 1
            return httpx.Response(200, json={"access_token": "t1", "expires_in": 3600})
        if request.url.path.endswith("/ping"):
            seen["authorization"] = request.headers.get("Authorization")
            return httpx.Response(200, json={"ok": True})
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    config = {
        "CAMUNDA_REST_ADDRESS": "http://api.local/v2",
        "CAMUNDA_AUTH_STRATEGY": "OAUTH",
        "CAMUNDA_OAUTH_URL": "http://auth.local/oauth/token",
        "CAMUNDA_TOKEN_AUDIENCE": "aud",
        "CAMUNDA_CLIENT_ID": "id",
        "CAMUNDA_CLIENT_SECRET": "secret",
    }

    client = CamundaAsyncClient(configuration=config, httpx_args={"transport": transport})
    response = await client.client.get_async_httpx_client().get("/ping")

    assert response.status_code == 200
    assert seen["authorization"] == "Bearer t1"
    assert token_calls["count"] == 1
