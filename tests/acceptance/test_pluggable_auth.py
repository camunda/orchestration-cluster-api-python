import base64
import json

from collections.abc import Callable
from pathlib import Path
from typing import Any

import httpx
import pytest

from camunda_orchestration_sdk.runtime.auth import (
    AsyncOAuthClientCredentialsAuthProvider,
    OAuthClientCredentialsAuthProvider,
)
from camunda_orchestration_sdk.runtime.clock import Clock, ManualClock
from camunda_orchestration_sdk.runtime.configuration_resolver import (
    CamundaSdkConfigPartial,
)


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
    config: CamundaSdkConfigPartial = {
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
    config: CamundaSdkConfigPartial = {
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
    from camunda_orchestration_sdk.runtime.auth import (
        OAuthClientCredentialsAuthProvider,
    )

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


def test_oauth_401_tarpit_file_prevents_subsequent_requests_when_file_cache_enabled_sync(
    tmp_path: Path,
) -> None:
    from camunda_orchestration_sdk.runtime.auth import (
        OAuthClientCredentialsAuthProvider,
    )

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

    tarpit_files: list[Path] = list(tmp_path.glob("oauth-401-tarpit-*.json"))
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


def test_oauth_token_is_cached_to_disk_and_reused_sync(tmp_path: Path) -> None:
    from camunda_orchestration_sdk.runtime.auth import (
        OAuthClientCredentialsAuthProvider,
    )

    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(
            200, json={"access_token": "t1", "expires_in": 3600}, request=request
        )

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


def test_oauth_disk_cache_is_disabled_when_cache_dir_cannot_be_created_sync(
    tmp_path: Path,
) -> None:
    """If cache_dir can't be created, file cache should disable and not crash."""

    from camunda_orchestration_sdk.runtime.auth import (
        OAuthClientCredentialsAuthProvider,
    )

    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(
            200,
            json={"access_token": f"t{calls['count']}", "expires_in": 3600},
            request=request,
        )

    # Make a non-directory path so mkdir(parents=True) fails.
    not_a_dir = tmp_path / "not-a-dir"
    not_a_dir.write_text("x", encoding="utf-8")
    cache_dir = not_a_dir / "child"

    provider = OAuthClientCredentialsAuthProvider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(cache_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(handler),
    )

    assert provider.get_headers()["Authorization"].startswith("Bearer t")
    assert calls["count"] == 1

    # A second provider should NOT reuse file cache (since it was disabled).
    provider2 = OAuthClientCredentialsAuthProvider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(cache_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(handler),
    )

    assert provider2.get_headers()["Authorization"].startswith("Bearer t")
    assert calls["count"] == 2

    provider.close()
    provider2.close()


def test_oauth_disk_cache_is_disabled_when_cache_dir_is_not_writable_sync(
    tmp_path: Path,
) -> None:
    """If cache_dir isn't writable, file cache should disable and not crash."""

    from camunda_orchestration_sdk.runtime.auth import (
        OAuthClientCredentialsAuthProvider,
    )

    readonly_dir = tmp_path / "readonly"
    readonly_dir.mkdir()

    # Make it non-writable. If the environment still allows writing (e.g. running as root), skip.
    readonly_dir.chmod(0o555)
    try:
        (readonly_dir / ".probe").write_text("x", encoding="utf-8")
    except Exception:
        pass
    else:
        pytest.skip(
            "Environment allows writing to chmod 0555 directory; cannot reliably test permissions"
        )

    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(
            200,
            json={"access_token": f"t{calls['count']}", "expires_in": 3600},
            request=request,
        )

    provider = OAuthClientCredentialsAuthProvider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(readonly_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(handler),
    )

    assert provider.get_headers()["Authorization"].startswith("Bearer t")
    assert calls["count"] == 1

    provider2 = OAuthClientCredentialsAuthProvider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(readonly_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(handler),
    )

    assert provider2.get_headers()["Authorization"].startswith("Bearer t")
    assert calls["count"] == 2

    provider.close()
    provider2.close()


def test_oauth_disk_cache_tolerates_corrupt_cache_file_sync(tmp_path: Path) -> None:
    """Simulate a race/partial write by seeding an invalid JSON cache file."""

    from camunda_orchestration_sdk.runtime.auth import (
        OAuthClientCredentialsAuthProvider,
    )

    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        return httpx.Response(
            200, json={"access_token": "t1", "expires_in": 3600}, request=request
        )

    # Pre-create a corrupt cache file at the expected path.
    token_file = Path(tmp_path) / "oauth-token-id-aud-auth.local.json"
    token_file.write_text("{", encoding="utf-8")

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

    provider.close()


def test_basic_auth_provider_encodes_credentials_correctly():
    from camunda_orchestration_sdk.runtime.auth import BasicAuthProvider

    provider = BasicAuthProvider(username="admin", password="secret")
    headers = provider.get_headers()

    token = base64.b64encode(b"admin:secret").decode("ascii")
    assert headers["Authorization"] == f"Basic {token}"


def test_basic_auth_provider_rejects_empty_username():
    from camunda_orchestration_sdk.runtime.auth import BasicAuthProvider

    with pytest.raises(ValueError, match="non-empty"):
        BasicAuthProvider(username="", password="secret")


def test_basic_auth_provider_rejects_empty_password():
    from camunda_orchestration_sdk.runtime.auth import BasicAuthProvider

    with pytest.raises(ValueError, match="non-empty"):
        BasicAuthProvider(username="admin", password="")


def test_basic_auth_provider_rejects_whitespace_only_credentials():
    from camunda_orchestration_sdk.runtime.auth import BasicAuthProvider

    with pytest.raises(ValueError, match="non-empty"):
        BasicAuthProvider(username="  ", password="  ")


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
    config: CamundaSdkConfigPartial = {
        "CAMUNDA_REST_ADDRESS": "http://api.local/v2",
        "CAMUNDA_AUTH_STRATEGY": "OAUTH",
        "CAMUNDA_OAUTH_URL": "http://auth.local/oauth/token",
        "CAMUNDA_TOKEN_AUDIENCE": "aud",
        "CAMUNDA_CLIENT_ID": "id",
        "CAMUNDA_CLIENT_SECRET": "secret",
    }

    client = CamundaAsyncClient(
        configuration=config, httpx_args={"transport": transport}
    )
    response = await client.client.get_async_httpx_client().get("/ping")

    assert response.status_code == 200
    assert seen["authorization"] == "Bearer t1"
    assert token_calls["count"] == 1


# ---------------------------------------------------------------------------------
# Token-endpoint failures other than 401, and token expiry boundaries.
#
# The 401 path is covered above. Everything below drives a failure the provider has
# never been asked about -- a 5xx, a transport error, a 200 whose body is unusable --
# and asserts what the provider does next, not merely that something was raised. The
# distinction that matters for a non-401 is what must *not* happen: no memoization and
# no tarpit file, so a transient outage does not lock the process out of its own
# credentials.
#
# Expiry is driven through the injected clock, so these are deterministic: no sleeping
# and no dependence on wall-clock time.
# ---------------------------------------------------------------------------------


_SAAS_OAUTH_URL = "https://login.cloud.camunda.io/oauth/token"
_LOCAL_OAUTH_URL = "http://auth.local/oauth/token"


def _counting_handler(
    response_factory: "Callable[[int, httpx.Request], httpx.Response]",
    calls: list[int],
) -> "Callable[[httpx.Request], httpx.Response]":
    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(1)
        return response_factory(len(calls), request)

    return handler


def _make_sync_provider(
    *,
    oauth_url: str,
    transport: httpx.BaseTransport,
    client_id: str = "id",
    client_secret: str = "secret",
    audience: str = "aud",
    cache_dir: str | None = None,
    disk_cache_disable: bool = True,
    saas_401_cooldown_s: float = 30.0,
    clock: Clock | None = None,
) -> "OAuthClientCredentialsAuthProvider":
    return OAuthClientCredentialsAuthProvider(
        oauth_url=oauth_url,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
        cache_dir=cache_dir,
        disk_cache_disable=disk_cache_disable,
        saas_401_cooldown_s=saas_401_cooldown_s,
        transport=transport,
        clock=clock,
    )


def _make_async_provider(
    *,
    oauth_url: str,
    transport: httpx.AsyncBaseTransport,
    client_id: str = "id",
    client_secret: str = "secret",
    audience: str = "aud",
    cache_dir: str | None = None,
    disk_cache_disable: bool = True,
    saas_401_cooldown_s: float = 30.0,
    clock: Clock | None = None,
) -> "AsyncOAuthClientCredentialsAuthProvider":
    return AsyncOAuthClientCredentialsAuthProvider(
        oauth_url=oauth_url,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
        cache_dir=cache_dir,
        disk_cache_disable=disk_cache_disable,
        saas_401_cooldown_s=saas_401_cooldown_s,
        transport=transport,
        clock=clock,
    )


def _ok(token: str, expires_in: int = 3600) -> "Callable[[int, httpx.Request], httpx.Response]":
    def factory(_n: int, request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json={"access_token": token, "expires_in": expires_in}, request=request
        )

    return factory


# --- non-401 token-endpoint failures ------------------------------------------------


def test_non_401_token_error_is_not_memoized_and_writes_no_tarpit_sync(
    tmp_path: Path,
) -> None:
    calls: list[int] = []
    provider = _make_sync_provider(
        oauth_url=_SAAS_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(
            _counting_handler(
                lambda _n, request: httpx.Response(
                    500, json={"error": "server_error"}, request=request
                ),
                calls,
            )
        ),
    )
    try:
        with pytest.raises(httpx.HTTPStatusError):
            provider.get_headers()
        with pytest.raises(httpx.HTTPStatusError):
            provider.get_headers()
    finally:
        provider.close()

    # Retried rather than memoized: a 500 is the server's problem, not the credential's.
    assert len(calls) == 2
    assert list(tmp_path.glob("oauth-401-tarpit-*.json")) == []


@pytest.mark.asyncio
async def test_non_401_token_error_is_not_memoized_and_writes_no_tarpit_async(
    tmp_path: Path,
) -> None:
    calls: list[int] = []
    provider = _make_async_provider(
        oauth_url=_SAAS_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(
            _counting_handler(
                lambda _n, request: httpx.Response(
                    503, json={"error": "unavailable"}, request=request
                ),
                calls,
            )
        ),
    )
    try:
        with pytest.raises(httpx.HTTPStatusError):
            await provider.aget_headers()
        with pytest.raises(httpx.HTTPStatusError):
            await provider.aget_headers()
    finally:
        await provider.aclose()

    assert len(calls) == 2
    assert list(tmp_path.glob("oauth-401-tarpit-*.json")) == []


def test_transport_error_from_the_token_endpoint_is_not_memoized_sync(
    tmp_path: Path,
) -> None:
    calls: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(1)
        raise httpx.ConnectError("simulated transport failure", request=request)

    provider = _make_sync_provider(
        oauth_url=_SAAS_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(handler),
    )
    try:
        with pytest.raises(httpx.ConnectError):
            provider.get_headers()
        with pytest.raises(httpx.ConnectError):
            provider.get_headers()
    finally:
        provider.close()

    assert len(calls) == 2
    assert list(tmp_path.glob("oauth-401-tarpit-*.json")) == []


@pytest.mark.asyncio
async def test_transport_error_from_the_token_endpoint_is_not_memoized_async(
    tmp_path: Path,
) -> None:
    calls: list[int] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(1)
        raise httpx.ConnectError("simulated transport failure", request=request)

    provider = _make_async_provider(
        oauth_url=_SAAS_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(handler),
    )
    try:
        with pytest.raises(httpx.ConnectError):
            await provider.aget_headers()
        with pytest.raises(httpx.ConnectError):
            await provider.aget_headers()
    finally:
        await provider.aclose()

    assert len(calls) == 2
    assert list(tmp_path.glob("oauth-401-tarpit-*.json")) == []


# --- malformed 200 responses --------------------------------------------------------


_MALFORMED_TOKEN_PAYLOADS: list[dict[str, Any]] = [
    {"access_token": "t"},
    {"expires_in": 3600},
    {},
    {"access_token": "", "expires_in": 3600},
    {"access_token": "t", "expires_in": 0},
]


@pytest.mark.parametrize("payload", _MALFORMED_TOKEN_PAYLOADS)
def test_malformed_token_response_is_rejected_sync(
    payload: dict[str, Any], tmp_path: Path
) -> None:
    calls: list[int] = []
    provider = _make_sync_provider(
        oauth_url=_SAAS_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(
            _counting_handler(
                lambda _n, request: httpx.Response(200, json=payload, request=request),
                calls,
            )
        ),
    )
    try:
        with pytest.raises(ValueError, match="missing access_token or expires_in"):
            provider.get_headers()
        with pytest.raises(ValueError, match="missing access_token or expires_in"):
            provider.get_headers()
    finally:
        provider.close()

    # Nothing usable came back, so nothing is cached, in memory or on disk.
    assert len(calls) == 2
    assert list(tmp_path.glob("oauth-token-*.json")) == []
    assert list(tmp_path.glob("oauth-401-tarpit-*.json")) == []


@pytest.mark.parametrize("payload", _MALFORMED_TOKEN_PAYLOADS)
@pytest.mark.asyncio
async def test_malformed_token_response_is_rejected_async(
    payload: dict[str, Any], tmp_path: Path
) -> None:
    calls: list[int] = []
    provider = _make_async_provider(
        oauth_url=_SAAS_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(
            _counting_handler(
                lambda _n, request: httpx.Response(200, json=payload, request=request),
                calls,
            )
        ),
    )
    try:
        with pytest.raises(ValueError, match="missing access_token or expires_in"):
            await provider.aget_headers()
        with pytest.raises(ValueError, match="missing access_token or expires_in"):
            await provider.aget_headers()
    finally:
        await provider.aclose()

    assert len(calls) == 2
    assert list(tmp_path.glob("oauth-token-*.json")) == []
    assert list(tmp_path.glob("oauth-401-tarpit-*.json")) == []


# --- expiry and skew boundaries -----------------------------------------------------


def test_token_is_reused_until_the_skew_adjusted_expiry_then_refetched_sync() -> None:
    clock = ManualClock(start=1_000_000.0)
    calls: list[int] = []
    provider = _make_sync_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        disk_cache_disable=True,
        clock=clock,
        transport=httpx.MockTransport(
            _counting_handler(
                lambda n, request: httpx.Response(
                    200,
                    json={"access_token": f"t{n}", "expires_in": 3600},
                    request=request,
                ),
                calls,
            )
        ),
    )
    try:
        assert provider.get_headers()["Authorization"] == "Bearer t1"

        # expires_at = now + 3600 - max(30, 5% of 3600) = now + 3420.
        clock.advance_sync(3419.0)
        assert provider.get_headers()["Authorization"] == "Bearer t1"
        assert len(calls) == 1

        clock.advance_sync(2.0)
        assert provider.get_headers()["Authorization"] == "Bearer t2"
        assert len(calls) == 2
    finally:
        provider.close()


@pytest.mark.asyncio
async def test_token_is_reused_until_the_skew_adjusted_expiry_then_refetched_async() -> (
    None
):
    clock = ManualClock(start=1_000_000.0)
    calls: list[int] = []
    provider = _make_async_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        disk_cache_disable=True,
        clock=clock,
        transport=httpx.MockTransport(
            _counting_handler(
                lambda n, request: httpx.Response(
                    200,
                    json={"access_token": f"t{n}", "expires_in": 3600},
                    request=request,
                ),
                calls,
            )
        ),
    )
    try:
        assert (await provider.aget_headers())["Authorization"] == "Bearer t1"

        clock.advance_sync(3419.0)
        assert (await provider.aget_headers())["Authorization"] == "Bearer t1"
        assert len(calls) == 1

        clock.advance_sync(2.0)
        assert (await provider.aget_headers())["Authorization"] == "Bearer t2"
        assert len(calls) == 2
    finally:
        await provider.aclose()


def test_a_lifetime_shorter_than_the_skew_is_clamped_not_negative_sync() -> None:
    """``expires_in`` below the 30s skew floor clamps to zero, never to the past."""

    clock = ManualClock(start=1_000_000.0)
    calls: list[int] = []
    provider = _make_sync_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        disk_cache_disable=True,
        clock=clock,
        transport=httpx.MockTransport(
            _counting_handler(
                lambda n, request: httpx.Response(
                    200,
                    json={"access_token": f"t{n}", "expires_in": 20},
                    request=request,
                ),
                calls,
            )
        ),
    )
    try:
        assert provider.get_headers()["Authorization"] == "Bearer t1"
        # Pinned exactly, not merely "in the past": without the max(0.0, ...) the
        # expiry would land 10s before now and every assertion below would still
        # pass, so the clamp itself would go untested.
        held = provider._token  # pyright: ignore[reportPrivateUsage]
        assert held is not None
        assert held.expires_at_epoch_s == clock.now()

        assert provider.get_headers()["Authorization"] == "Bearer t2"
        assert len(calls) == 2
    finally:
        provider.close()


# --- the on-disk cache at the expiry boundary ---------------------------------------


def _seed_cache_entry(tmp_path: Path, access_token: str, expires_at: float) -> Path:
    token_file = tmp_path / "oauth-token-id-aud-auth.local.json"
    token_file.write_text(
        json.dumps(
            {"access_token": access_token, "expires_at_epoch_s": expires_at},
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return token_file


def test_an_expired_file_cached_token_is_replaced_sync(tmp_path: Path) -> None:
    token_file = _seed_cache_entry(tmp_path, "stale", expires_at=500.0)
    calls: list[int] = []
    provider = _make_sync_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        clock=ManualClock(start=1000.0),
        transport=httpx.MockTransport(_counting_handler(_ok("fresh"), calls)),
    )
    try:
        assert provider.get_headers()["Authorization"] == "Bearer fresh"
    finally:
        provider.close()

    assert len(calls) == 1
    assert json.loads(token_file.read_text(encoding="utf-8"))["access_token"] == "fresh"


def test_an_expired_file_cached_token_is_unlinked_even_when_the_refetch_fails_sync(
    tmp_path: Path,
) -> None:
    token_file = _seed_cache_entry(tmp_path, "stale", expires_at=500.0)
    provider = _make_sync_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        clock=ManualClock(start=1000.0),
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                500, json={"error": "server_error"}, request=request
            )
        ),
    )
    try:
        with pytest.raises(httpx.HTTPStatusError):
            provider.get_headers()
    finally:
        provider.close()

    # The stale entry is gone rather than left to be served after a later restart.
    assert not token_file.exists()


def test_a_file_cached_token_is_served_while_it_is_still_valid_sync(
    tmp_path: Path,
) -> None:
    _seed_cache_entry(tmp_path, "from-disk", expires_at=2000.0)
    calls: list[int] = []
    provider = _make_sync_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        clock=ManualClock(start=1999.0),
        transport=httpx.MockTransport(_counting_handler(_ok("from-network"), calls)),
    )
    try:
        assert provider.get_headers()["Authorization"] == "Bearer from-disk"
    finally:
        provider.close()

    assert calls == []


# --- the 401 cooldown boundary ------------------------------------------------------


def test_the_401_memoization_expires_after_the_cooldown_sync() -> None:
    clock = ManualClock(start=1_000.0)
    calls: list[int] = []
    provider = _make_sync_provider(
        # Not the SaaS endpoint: this is about the in-memory cooldown, and a tarpit
        # file would end the test at the first call instead.
        oauth_url=_LOCAL_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        disk_cache_disable=True,
        saas_401_cooldown_s=30.0,
        clock=clock,
        transport=httpx.MockTransport(
            _counting_handler(
                lambda _n, request: httpx.Response(
                    401, json={"error": "invalid_client"}, request=request
                ),
                calls,
            )
        ),
    )
    try:
        with pytest.raises(httpx.HTTPStatusError):
            provider.get_headers()
        assert len(calls) == 1

        clock.advance_sync(29.0)
        with pytest.raises(httpx.HTTPStatusError):
            provider.get_headers()
        assert len(calls) == 1, "still inside the cooldown"

        clock.advance_sync(2.0)
        with pytest.raises(httpx.HTTPStatusError):
            provider.get_headers()
        assert len(calls) == 2, "cooldown elapsed, so the endpoint is tried again"
    finally:
        provider.close()


@pytest.mark.asyncio
async def test_the_401_memoization_expires_after_the_cooldown_async() -> None:
    clock = ManualClock(start=1_000.0)
    calls: list[int] = []
    provider = _make_async_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        disk_cache_disable=True,
        saas_401_cooldown_s=30.0,
        clock=clock,
        transport=httpx.MockTransport(
            _counting_handler(
                lambda _n, request: httpx.Response(
                    401, json={"error": "invalid_client"}, request=request
                ),
                calls,
            )
        ),
    )
    try:
        with pytest.raises(httpx.HTTPStatusError):
            await provider.aget_headers()
        assert len(calls) == 1

        clock.advance_sync(29.0)
        with pytest.raises(httpx.HTTPStatusError):
            await provider.aget_headers()
        assert len(calls) == 1, "still inside the cooldown"

        clock.advance_sync(2.0)
        with pytest.raises(httpx.HTTPStatusError):
            await provider.aget_headers()
        assert len(calls) == 2, "cooldown elapsed, so the endpoint is tried again"
    finally:
        await provider.aclose()


@pytest.mark.asyncio
async def test_a_lifetime_shorter_than_the_skew_is_clamped_not_negative_async() -> None:
    clock = ManualClock(start=1_000_000.0)
    calls: list[int] = []
    provider = _make_async_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        disk_cache_disable=True,
        clock=clock,
        transport=httpx.MockTransport(
            _counting_handler(
                lambda n, request: httpx.Response(
                    200,
                    json={"access_token": f"t{n}", "expires_in": 20},
                    request=request,
                ),
                calls,
            )
        ),
    )
    try:
        assert (await provider.aget_headers())["Authorization"] == "Bearer t1"
        held = provider._token  # pyright: ignore[reportPrivateUsage]
        assert held is not None
        assert held.expires_at_epoch_s == clock.now()

        assert (await provider.aget_headers())["Authorization"] == "Bearer t2"
        assert len(calls) == 2
    finally:
        await provider.aclose()


@pytest.mark.asyncio
async def test_an_expired_file_cached_token_is_replaced_async(tmp_path: Path) -> None:
    token_file = _seed_cache_entry(tmp_path, "stale", expires_at=500.0)
    calls: list[int] = []
    provider = _make_async_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        clock=ManualClock(start=1000.0),
        transport=httpx.MockTransport(_counting_handler(_ok("fresh"), calls)),
    )
    try:
        assert (await provider.aget_headers())["Authorization"] == "Bearer fresh"
    finally:
        await provider.aclose()

    assert len(calls) == 1
    assert json.loads(token_file.read_text(encoding="utf-8"))["access_token"] == "fresh"


@pytest.mark.asyncio
async def test_an_expired_file_cached_token_is_unlinked_even_when_the_refetch_fails_async(
    tmp_path: Path,
) -> None:
    token_file = _seed_cache_entry(tmp_path, "stale", expires_at=500.0)
    provider = _make_async_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        clock=ManualClock(start=1000.0),
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                500, json={"error": "server_error"}, request=request
            )
        ),
    )
    try:
        with pytest.raises(httpx.HTTPStatusError):
            await provider.aget_headers()
    finally:
        await provider.aclose()

    assert not token_file.exists()


@pytest.mark.asyncio
async def test_a_file_cached_token_is_served_while_it_is_still_valid_async(
    tmp_path: Path,
) -> None:
    _seed_cache_entry(tmp_path, "from-disk", expires_at=2000.0)
    calls: list[int] = []
    provider = _make_async_provider(
        oauth_url=_LOCAL_OAUTH_URL,
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        clock=ManualClock(start=1999.0),
        transport=httpx.MockTransport(_counting_handler(_ok("from-network"), calls)),
    )
    try:
        assert (await provider.aget_headers())["Authorization"] == "Bearer from-disk"
    finally:
        await provider.aclose()

    assert calls == []
