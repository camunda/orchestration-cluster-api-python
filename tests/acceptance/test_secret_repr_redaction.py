"""Credentials must not render in ``repr()`` / ``str()`` of config and token objects.

Scoped to the class of defect rather than the fields that happened to leak: the secret
set is derived from the model's own field names, so a credential field added later is
covered here without anyone remembering to extend this file.
"""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from camunda_orchestration_sdk.runtime.configuration_resolver import (
    CamundaSdkConfigPartial,
    CamundaSdkConfiguration,
    ConfigurationResolver,
)


#: Name fragments that mark a configuration field as credential-bearing. ``*_PATH``
#: fields name a file on disk rather than carrying its contents, so they are not secret.
_SECRET_NAME_MARKERS = ("SECRET", "PASSWORD", "PASSPHRASE", "KEY")


def _is_secret_field_name(name: str) -> bool:
    if name.endswith("_PATH"):
        return False
    return any(marker in name for marker in _SECRET_NAME_MARKERS)


def _secret_field_names() -> list[str]:
    return [n for n in CamundaSdkConfiguration.model_fields if _is_secret_field_name(n)]


def _sentinel_for(name: str) -> str:
    return f"SENTINEL-{name}-8c41f2"


def _configuration_with_sentinel_secrets() -> tuple[CamundaSdkConfiguration, dict[str, str]]:
    sentinels = {name: _sentinel_for(name) for name in _secret_field_names()}
    values: dict[str, Any] = dict(sentinels)
    # A client key without a client certificate is rejected by the model's own
    # validation, so pair it with a (non-secret) certificate.
    values["CAMUNDA_MTLS_CERT"] = "-----BEGIN CERTIFICATE-----not-a-secret"
    values["CAMUNDA_CLIENT_ID"] = "visible-client-id"
    return CamundaSdkConfiguration(**values), sentinels


def test_the_secret_field_set_is_not_empty() -> None:
    """Guards the guard: a renamed field must not silently empty the sweep below."""

    assert set(_secret_field_names()) == {
        "CAMUNDA_CLIENT_SECRET",
        "CAMUNDA_CLIENT_AUTH_CLIENTSECRET",
        "CAMUNDA_BASIC_AUTH_PASSWORD",
        "CAMUNDA_MTLS_KEY",
        "CAMUNDA_MTLS_KEY_PASSPHRASE",
    }


def test_every_secret_bearing_field_is_declared_repr_false() -> None:
    offenders = [
        name
        for name, info in CamundaSdkConfiguration.model_fields.items()
        if _is_secret_field_name(name) and info.repr
    ]
    assert offenders == [], (
        f"credential-bearing fields render their value in repr(): {offenders}"
    )


def test_no_secret_value_appears_in_configuration_repr_or_str() -> None:
    config, sentinels = _configuration_with_sentinel_secrets()
    rendered = f"{config!r}\n{config!s}\n{config}"

    leaked = [name for name, value in sentinels.items() if value in rendered]
    assert leaked == [], f"secret value rendered for: {leaked}"


def test_non_secret_fields_still_render_so_the_config_stays_debuggable() -> None:
    config, _ = _configuration_with_sentinel_secrets()
    rendered = repr(config)

    assert "visible-client-id" in rendered
    assert "CAMUNDA_AUTH_STRATEGY" in rendered


def test_secret_values_are_still_readable_through_the_model() -> None:
    """``repr=False`` hides the value from rendering only — nothing else changes."""

    config, sentinels = _configuration_with_sentinel_secrets()

    for name, value in sentinels.items():
        assert getattr(config, name) == value
        assert config.model_dump()[name] == value


def test_resolved_configuration_repr_does_not_echo_the_raw_partials() -> None:
    environment: CamundaSdkConfigPartial = {
        "CAMUNDA_REST_ADDRESS": "http://api.local/v2",
        "CAMUNDA_BASIC_AUTH_PASSWORD": "SENTINEL-ENV-PASSWORD-8c41f2",
    }
    explicit: CamundaSdkConfigPartial = {
        "CAMUNDA_CLIENT_SECRET": "SENTINEL-EXPLICIT-SECRET-8c41f2",
        "CAMUNDA_CLIENT_ID": "visible-client-id",
    }

    resolved = ConfigurationResolver(environment, explicit).resolve()
    rendered = f"{resolved!r}\n{resolved!s}"

    assert "SENTINEL-ENV-PASSWORD-8c41f2" not in rendered
    assert "SENTINEL-EXPLICIT-SECRET-8c41f2" not in rendered
    # The raw partials are still there to read, just not to render.
    assert resolved.explicit is not None
    assert resolved.explicit["CAMUNDA_CLIENT_SECRET"] == "SENTINEL-EXPLICIT-SECRET-8c41f2"


def test_oauth_token_repr_does_not_render_the_access_token() -> None:
    from camunda_orchestration_sdk.runtime.auth import _OAuthToken

    token = _OAuthToken(
        access_token="SENTINEL-ACCESS-TOKEN-8c41f2", expires_at_epoch_s=12.0
    )
    rendered = f"{token!r}\n{token!s}"

    assert "SENTINEL-ACCESS-TOKEN-8c41f2" not in rendered
    assert "12.0" in rendered
    assert token.access_token == "SENTINEL-ACCESS-TOKEN-8c41f2"


def _oauth_client_config() -> CamundaSdkConfigPartial:
    config: CamundaSdkConfigPartial = {
        "CAMUNDA_REST_ADDRESS": "http://api.local/v2",
        "CAMUNDA_AUTH_STRATEGY": "OAUTH",
        "CAMUNDA_OAUTH_URL": "http://auth.local/oauth/token",
        "CAMUNDA_TOKEN_AUDIENCE": "aud",
        "CAMUNDA_CLIENT_ID": "visible-client-id",
        "CAMUNDA_CLIENT_SECRET": "SENTINEL-CLIENT-SECRET-8c41f2",
    }
    return config


def _handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"ok": True}, request=request)


def test_sync_client_and_its_configuration_do_not_render_the_secret() -> None:
    from camunda_orchestration_sdk import CamundaClient

    client = CamundaClient(
        configuration=_oauth_client_config(),
        httpx_args={"transport": httpx.MockTransport(_handler)},
    )

    rendered = f"{client!r}\n{client.configuration!r}\n{client.configuration!s}"
    assert "SENTINEL-CLIENT-SECRET-8c41f2" not in rendered


@pytest.mark.asyncio
async def test_async_client_and_its_configuration_do_not_render_the_secret() -> None:
    from camunda_orchestration_sdk import CamundaAsyncClient

    client = CamundaAsyncClient(
        configuration=_oauth_client_config(),
        httpx_args={"transport": httpx.MockTransport(_handler)},
    )

    rendered = f"{client!r}\n{client.configuration!r}\n{client.configuration!s}"
    assert "SENTINEL-CLIENT-SECRET-8c41f2" not in rendered
