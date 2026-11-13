"""The sentinel-secret regression test required by the shared SDK policy.

A recognisable sentinel is configured as the credential, the auth success and auth
failure paths are driven with it, and the sentinel is then looked for in everything an
operator or a crash reporter can see: every log record emitted at ``trace``, every
exception raised along the way, the rendered client and auth provider, and the name and
contents of every file the SDK wrote.

Extend it when a credential gains a new place to flow. The guard at the top fails if a
credential-shaped configuration field appears that this file neither drives nor
explicitly excludes, so that is not left to memory.
"""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, cast

import httpx
import pytest

from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.runtime.configuration_resolver import (
    CamundaSdkConfigPartial,
    CamundaSdkConfiguration,
    ConfigurationResolver,
)


SENTINEL = "CAMUNDA-SENTINEL-SECRET-DO-NOT-LOG"

_OAUTH_URL = "http://auth.local/oauth/token"
_REST_ADDRESS = "http://api.local/v2"

#: Credential fields this file drives end to end.
_DRIVEN_CREDENTIAL_FIELDS = frozenset(
    {
        "CAMUNDA_CLIENT_SECRET",
        "CAMUNDA_CLIENT_AUTH_CLIENTSECRET",
        "CAMUNDA_BASIC_AUTH_PASSWORD",
    }
)

#: Credential fields that cannot be driven with an arbitrary sentinel: they must be
#: real PEM key material or the TLS context cannot be built at all. Their handling is
#: covered by the mTLS tests instead.
_UNDRIVABLE_CREDENTIAL_FIELDS = frozenset(
    {
        "CAMUNDA_MTLS_KEY",
        "CAMUNDA_MTLS_KEY_PASSPHRASE",
    }
)


class _CapturingLogger:
    """A ``CamundaLogger`` that keeps everything, including ``trace``."""

    def __init__(self) -> None:
        self.records: list[str] = []

    def _record(self, level: str, msg: str, *args: Any, **kwargs: Any) -> None:
        self.records.append(f"{level}: {msg} args={args!r} kwargs={kwargs!r}")

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._record("debug", msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._record("info", msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._record("warning", msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._record("error", msg, *args, **kwargs)

    def trace(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._record("trace", msg, *args, **kwargs)


def _credential_shaped_fields() -> set[str]:
    return {
        name
        for name in CamundaSdkConfiguration.model_fields
        # ``*_PATH`` names a file on disk rather than carrying its contents.
        if not name.endswith("_PATH")
        and any(
            marker in name for marker in ("SECRET", "PASSWORD", "PASSPHRASE", "KEY")
        )
    }


def test_every_credential_field_is_either_driven_here_or_explicitly_excluded() -> None:
    assert _credential_shaped_fields() == (
        _DRIVEN_CREDENTIAL_FIELDS | _UNDRIVABLE_CREDENTIAL_FIELDS
    ), (
        "a credential field was added: drive it in this file, or add it to "
        "_UNDRIVABLE_CREDENTIAL_FIELDS with the reason"
    )


class _Surfaces:
    """Everything the sentinel is asserted not to appear in."""

    def __init__(self) -> None:
        self.logger = _CapturingLogger()
        self.exceptions: list[BaseException] = []
        self.rendered: list[str] = []

    def record(self, obj: object) -> None:
        # Both renderings: a separate ``__str__`` can disclose what ``__repr__`` hides.
        self.rendered.append(f"{obj!r}")
        self.rendered.append(f"{obj!s}")
        # A client carries its effective configuration: it is a separate object with its
        # own repr, and the one ``print(client.configuration)`` or a traceback renders.
        configuration = getattr(obj, "configuration", None)
        if isinstance(configuration, CamundaSdkConfiguration):
            self.rendered.append(f"{configuration!r}")
            self.rendered.append(f"{configuration!s}")

    def drive(self, action: Any) -> None:
        try:
            action()
        except BaseException as exc:  # every error raised is itself a surface to check
            self.exceptions.append(exc)

    def text(self, cache_dir: Path | None) -> str:
        parts = list(self.logger.records) + list(self.rendered)
        for exc in self.exceptions:
            parts.append(f"{exc}")
            parts.append(f"{exc!r}")
            errors = getattr(exc, "errors", None)
            if callable(errors):
                parts.extend(repr(error) for error in errors())
        if cache_dir is not None and cache_dir.exists():
            # Recursive: a nested cache directory is still a place a credential can land.
            for path in sorted(cache_dir.rglob("*")):
                parts.append(path.name)
                if path.is_file():
                    parts.append(path.read_text(encoding="utf-8", errors="replace"))
        return "\n".join(parts)


def _assert_absent(surfaces: _Surfaces, cache_dir: Path | None, *values: str) -> None:
    haystack = surfaces.text(cache_dir)
    leaked = [value for value in values if value in haystack]
    assert leaked == [], f"a credential reached an observable surface: {leaked!r}"


def _oauth_config(
    cache_dir: Path, oauth_url: str = _OAUTH_URL
) -> CamundaSdkConfigPartial:
    return {
        "CAMUNDA_REST_ADDRESS": _REST_ADDRESS,
        "CAMUNDA_AUTH_STRATEGY": "OAUTH",
        "CAMUNDA_OAUTH_URL": oauth_url,
        "CAMUNDA_TOKEN_AUDIENCE": "aud",
        "CAMUNDA_CLIENT_ID": "sentinel-client-id",
        "CAMUNDA_CLIENT_SECRET": SENTINEL,
        "CAMUNDA_SDK_LOG_LEVEL": "trace",
        "CAMUNDA_TOKEN_CACHE_DIR": str(cache_dir),
    }


_SAAS_OAUTH_URL = "https://login.cloud.camunda.io/oauth/token"


def _token_endpoint(status: int, body: dict[str, Any]) -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/oauth/token":
            return httpx.Response(status, json=body, request=request)
        return httpx.Response(200, json={"ok": True}, request=request)

    return handler


def test_the_sentinel_survives_the_oauth_success_path(tmp_path: Path) -> None:
    """A token is fetched, cached to disk and used for an API call."""

    cache_dir = tmp_path / "cache"
    surfaces = _Surfaces()

    client = CamundaClient(
        configuration=_oauth_config(cache_dir),
        logger=surfaces.logger,
        httpx_args={
            "transport": httpx.MockTransport(
                _token_endpoint(
                    200, {"access_token": "issued-token", "expires_in": 3600}
                )
            )
        },
    )
    surfaces.record(client)
    surfaces.record(client.auth_provider)

    surfaces.drive(lambda: client.client.get_httpx_client().get("/ping"))

    assert surfaces.logger.records, "the trace-level logger captured nothing to check"
    assert list(cache_dir.glob("oauth-token-*.json")), "no token was cached"
    _assert_absent(surfaces, cache_dir, SENTINEL)


def test_the_sentinel_survives_the_oauth_401_path(tmp_path: Path) -> None:
    cache_dir = tmp_path / "cache"
    surfaces = _Surfaces()

    client = CamundaClient(
        configuration=_oauth_config(cache_dir),
        logger=surfaces.logger,
        httpx_args={
            "transport": httpx.MockTransport(
                _token_endpoint(401, {"error": "invalid_client"})
            )
        },
    )
    surfaces.record(client)
    surfaces.record(client.auth_provider)

    surfaces.drive(lambda: client.client.get_httpx_client().get("/ping"))
    # Again, to drive the memoized-401 branch as well as the first failure.
    surfaces.drive(lambda: client.client.get_httpx_client().get("/ping"))

    assert surfaces.exceptions, "the 401 path raised nothing to inspect"
    _assert_absent(surfaces, cache_dir, SENTINEL)


def test_the_sentinel_survives_a_non_401_token_endpoint_failure(tmp_path: Path) -> None:
    cache_dir = tmp_path / "cache"
    surfaces = _Surfaces()

    client = CamundaClient(
        configuration=_oauth_config(cache_dir),
        logger=surfaces.logger,
        httpx_args={
            "transport": httpx.MockTransport(
                _token_endpoint(500, {"error": "server_error"})
            )
        },
    )
    surfaces.record(client)
    surfaces.record(client.auth_provider)

    surfaces.drive(lambda: client.client.get_httpx_client().get("/ping"))

    assert surfaces.exceptions
    _assert_absent(surfaces, cache_dir, SENTINEL)


def test_the_sentinel_survives_a_failing_api_call_with_body_logging(
    tmp_path: Path,
) -> None:
    """At ``trace`` the response hook logs error bodies; a hostile body is still a body."""

    cache_dir = tmp_path / "cache"
    surfaces = _Surfaces()

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/oauth/token":
            return httpx.Response(
                200,
                json={"access_token": "issued-token", "expires_in": 3600},
                request=request,
            )
        return httpx.Response(500, json={"title": "INTERNAL"}, request=request)

    client = CamundaClient(
        configuration=_oauth_config(cache_dir),
        logger=surfaces.logger,
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    surfaces.record(client)

    surfaces.drive(lambda: client.client.get_httpx_client().get("/ping"))
    surfaces.drive(client.get_topology)

    assert surfaces.exceptions
    _assert_absent(surfaces, cache_dir, SENTINEL)


def test_the_sentinel_survives_the_basic_auth_paths() -> None:
    """Basic auth has no token endpoint: success and a 401 from the API itself."""

    surfaces = _Surfaces()
    encoded = base64.b64encode(f"sentinel-user:{SENTINEL}".encode("utf-8")).decode(
        "ascii"
    )

    responses = iter([200, 401])

    def handler(request: httpx.Request) -> httpx.Response:
        status = next(responses, 401)
        return httpx.Response(status, json={"title": "NOPE"}, request=request)

    config: CamundaSdkConfigPartial = {
        "CAMUNDA_REST_ADDRESS": _REST_ADDRESS,
        "CAMUNDA_AUTH_STRATEGY": "BASIC",
        "CAMUNDA_BASIC_AUTH_USERNAME": "sentinel-user",
        "CAMUNDA_BASIC_AUTH_PASSWORD": SENTINEL,
        "CAMUNDA_SDK_LOG_LEVEL": "trace",
    }

    client = CamundaClient(
        configuration=config,
        logger=surfaces.logger,
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    surfaces.record(client)
    surfaces.record(client.auth_provider)

    surfaces.drive(lambda: client.client.get_httpx_client().get("/ping"))
    surfaces.drive(client.get_topology)

    assert surfaces.logger.records
    # Neither the password nor the Authorization header that carries it.
    _assert_absent(surfaces, None, SENTINEL, encoded)


@pytest.mark.asyncio
async def test_the_sentinel_survives_the_async_oauth_paths(tmp_path: Path) -> None:
    from camunda_orchestration_sdk import CamundaAsyncClient

    cache_dir = tmp_path / "cache"
    surfaces = _Surfaces()

    client = CamundaAsyncClient(
        configuration=_oauth_config(cache_dir),
        logger=surfaces.logger,
        httpx_args={
            "transport": httpx.MockTransport(
                _token_endpoint(
                    200, {"access_token": "issued-token", "expires_in": 3600}
                )
            )
        },
    )
    surfaces.record(client)
    surfaces.record(client.auth_provider)

    # The success path must actually succeed, or the failure path below would be the
    # only thing this test proves.
    response = await client.client.get_async_httpx_client().get("/ping")
    assert response.status_code == 200
    assert list(cache_dir.glob("oauth-token-*.json")), "no token was cached"

    failing = CamundaAsyncClient(
        configuration=_oauth_config(cache_dir / "failing"),
        logger=surfaces.logger,
        httpx_args={
            "transport": httpx.MockTransport(
                _token_endpoint(401, {"error": "invalid_client"})
            )
        },
    )
    surfaces.record(failing)
    with pytest.raises(httpx.HTTPStatusError) as caught:
        await failing.client.get_async_httpx_client().get("/ping")
    surfaces.exceptions.append(caught.value)

    _assert_absent(surfaces, cache_dir, SENTINEL)


def test_the_sentinel_survives_the_saas_401_tarpit(tmp_path: Path) -> None:
    """The SaaS 401 writes a persistent file keyed on the secret; check it by name."""

    cache_dir = tmp_path / "cache"
    surfaces = _Surfaces()

    client = CamundaClient(
        configuration=_oauth_config(cache_dir, _SAAS_OAUTH_URL),
        logger=surfaces.logger,
        httpx_args={
            "transport": httpx.MockTransport(
                _token_endpoint(401, {"error": "invalid_client"})
            )
        },
    )
    surfaces.record(client)
    surfaces.record(client.auth_provider)

    surfaces.drive(lambda: client.client.get_httpx_client().get("/ping"))
    # Again: the second call raises from the persistent tarpit rather than the endpoint.
    surfaces.drive(lambda: client.client.get_httpx_client().get("/ping"))

    tarpits = list(cache_dir.glob("oauth-401-tarpit-*.json"))
    assert tarpits, "the SaaS 401 should have written a tarpit file"
    assert surfaces.exceptions
    _assert_absent(surfaces, cache_dir, SENTINEL)


@pytest.mark.asyncio
async def test_the_sentinel_survives_the_async_saas_401_tarpit(tmp_path: Path) -> None:
    from camunda_orchestration_sdk import CamundaAsyncClient

    cache_dir = tmp_path / "cache"
    surfaces = _Surfaces()

    client = CamundaAsyncClient(
        configuration=_oauth_config(cache_dir, _SAAS_OAUTH_URL),
        logger=surfaces.logger,
        httpx_args={
            "transport": httpx.MockTransport(
                _token_endpoint(401, {"error": "invalid_client"})
            )
        },
    )
    surfaces.record(client)
    surfaces.record(client.auth_provider)

    with pytest.raises(httpx.HTTPStatusError) as caught:
        await client.client.get_async_httpx_client().get("/ping")
    surfaces.exceptions.append(caught.value)

    tarpits = list(cache_dir.glob("oauth-401-tarpit-*.json"))
    assert tarpits, "the SaaS 401 should have written a tarpit file"
    _assert_absent(surfaces, cache_dir, SENTINEL)


# --- repr()/str() of the configuration itself ----------------------------------------


def _every_credential_field() -> frozenset[str]:
    """Driven and undriven alike: rendering needs no working TLS context or key."""

    return _DRIVEN_CREDENTIAL_FIELDS | _UNDRIVABLE_CREDENTIAL_FIELDS


def _sentinel_for(field: str) -> str:
    # Prefixed with the shared sentinel so one substring check covers every field, and
    # suffixed with the field so a leak names where it came from.
    return f"{SENTINEL}-{field}"


def _all_credentials_configured() -> dict[str, Any]:
    """A configuration that sets every credential field to its own sentinel."""

    values: dict[str, Any] = {
        field: _sentinel_for(field) for field in _every_credential_field()
    }
    # The alias pair must agree, or the alias check fires before validation.
    values["CAMUNDA_CLIENT_AUTH_CLIENTSECRET"] = values["CAMUNDA_CLIENT_SECRET"]
    # A client key without a client certificate is rejected by the model's validation.
    values["CAMUNDA_MTLS_CERT"] = "-----BEGIN CERTIFICATE-----not-a-secret"
    values["CAMUNDA_CLIENT_ID"] = "sentinel-client-id"
    return values


def test_the_sentinel_survives_repr_and_str_of_the_configuration() -> None:
    """Every credential field, rendered through every configuration object."""

    surfaces = _Surfaces()
    configured = _all_credentials_configured()

    resolved = ConfigurationResolver(configured).resolve()
    surfaces.record(resolved)
    surfaces.record(resolved.effective)
    # The explicit path keeps a second raw copy of the values on the resolved object.
    explicit = ConfigurationResolver({}, cast(CamundaSdkConfigPartial, configured))
    surfaces.record(explicit.resolve())
    surfaces.record(CamundaSdkConfiguration(**configured))

    assert "sentinel-client-id" in surfaces.text(None), (
        "non-secret fields should still render, or the check proves nothing"
    )
    _assert_absent(surfaces, None, SENTINEL)


def test_the_sentinel_survives_repr_and_str_of_the_oauth_token() -> None:
    from camunda_orchestration_sdk.runtime.auth import _OAuthToken

    surfaces = _Surfaces()
    surfaces.record(_OAuthToken(access_token=SENTINEL, expires_at_epoch_s=12.0))

    _assert_absent(surfaces, None, SENTINEL)


# --- the invalid-configuration error surface -----------------------------------------


def _drive_construction(surfaces: _Surfaces, configuration: dict[str, Any]) -> None:
    """Construct both client flavours; each raise is a surface to check."""

    from camunda_orchestration_sdk import CamundaAsyncClient

    partial = cast(CamundaSdkConfigPartial, configuration)
    surfaces.drive(lambda: CamundaClient(configuration=partial, logger=surfaces.logger))
    surfaces.drive(
        lambda: CamundaAsyncClient(configuration=partial, logger=surfaces.logger)
    )


def test_the_sentinel_survives_a_configuration_rejected_at_construction() -> None:
    """Fires at start-up, so its text lands in application logs and crash reporters."""

    surfaces = _Surfaces()
    configured = _all_credentials_configured()
    # Rejected: OAuth needs a client id.
    del configured["CAMUNDA_CLIENT_ID"]
    configured["CAMUNDA_AUTH_STRATEGY"] = "OAUTH"

    _drive_construction(surfaces, configured)

    assert len(surfaces.exceptions) == 2, "both clients should reject the configuration"
    # The diagnosis survives redaction: the user is still told what is missing.
    assert all("CAMUNDA_CLIENT_ID" in f"{exc}" for exc in surfaces.exceptions)
    _assert_absent(surfaces, None, SENTINEL)


@pytest.mark.parametrize("source", ["explicit", "environment"])
def test_the_sentinel_survives_a_configuration_rejected_by_the_resolver(
    source: str,
) -> None:
    """The resolver raises its own errors (alias conflicts) before validation runs."""

    surfaces = _Surfaces()
    conflicting = cast(
        CamundaSdkConfigPartial,
        {
            "CAMUNDA_CLIENT_SECRET": _sentinel_for("LEFT"),
            "CAMUNDA_CLIENT_AUTH_CLIENTSECRET": _sentinel_for("RIGHT"),
        },
    )
    if source == "explicit":
        surfaces.drive(lambda: ConfigurationResolver({}, conflicting).resolve())
    else:
        surfaces.drive(lambda: ConfigurationResolver(conflicting).resolve())

    assert surfaces.exceptions, f"the {source} alias conflict raised nothing"
    assert "CAMUNDA_CLIENT_SECRET" in f"{surfaces.exceptions[0]}"
    _assert_absent(surfaces, None, SENTINEL)


def test_the_sentinel_survives_a_credential_rejected_for_its_type() -> None:
    """The rejected value *is* the credential: the error cannot quote it back."""

    surfaces = _Surfaces()
    configured = {
        "CAMUNDA_AUTH_STRATEGY": "OAUTH",
        "CAMUNDA_CLIENT_ID": "sentinel-client-id",
        # Not a string, so validation rejects it; the digits stand in for the sentinel.
        "CAMUNDA_CLIENT_SECRET": 424242424242,
        "CAMUNDA_CLIENT_AUTH_CLIENTSECRET": 424242424242,
    }

    surfaces.drive(
        lambda: ConfigurationResolver(
            {}, cast(CamundaSdkConfigPartial, configured)
        ).resolve()
    )

    assert surfaces.exceptions, "a non-string credential should be rejected"
    _assert_absent(surfaces, None, "424242424242")
