"""Configuration errors must not echo credentials.

These errors fire at client construction -- process start-up -- so their text lands in
application logs and crash reporters. The sweep below is driven from the model's own
field names, so a credential field added later is covered without this file being
edited.
"""

from __future__ import annotations

from typing import Any, cast

import pytest
from pydantic import ValidationError

from camunda_orchestration_sdk.runtime.configuration_resolver import (
    SECRET_CONFIG_KEYS,
    CamundaSdkConfigPartial,
    CamundaSdkConfiguration,
    ConfigurationResolver,
)


_SECRET_NAME_MARKERS = ("SECRET", "PASSWORD", "PASSPHRASE", "KEY")


def _sentinel_for(key: str) -> str:
    return f"SENTINEL-{key}-4d7b19"


def _rendered(exc: Exception) -> str:
    """Everything a caller can read off the exception.

    ``str()`` of a pydantic ``ValidationError`` elides the middle of a long
    ``input_value``, so asserting on it alone would pass or fail according to where a
    value happened to land in the dict. ``errors()`` carries the input untruncated, and
    is what a structured error handler reads, so it is included here.
    """

    rendered = f"{exc}\n{exc!r}"
    errors = getattr(exc, "errors", None)
    if callable(errors):
        rendered += "\n" + "\n".join(repr(error) for error in errors())
    return rendered


# --- the set itself -----------------------------------------------------------------


def test_every_credential_shaped_field_is_listed_as_a_secret() -> None:
    """A credential field added to the model must be added to the redaction set."""

    credential_shaped = {
        name
        for name in CamundaSdkConfiguration.model_fields
        # ``*_PATH`` names a file on disk rather than carrying its contents.
        if not name.endswith("_PATH")
        and any(marker in name for marker in _SECRET_NAME_MARKERS)
    }

    assert credential_shaped == set(SECRET_CONFIG_KEYS)


# --- alias conflicts ----------------------------------------------------------------


def test_explicit_alias_conflict_on_the_client_secret_does_not_echo_the_values() -> None:
    explicit: CamundaSdkConfigPartial = {
        "CAMUNDA_CLIENT_SECRET": "SENTINEL-LEFT-4d7b19",
        "CAMUNDA_CLIENT_AUTH_CLIENTSECRET": "SENTINEL-RIGHT-4d7b19",
    }

    with pytest.raises(ValueError) as caught:
        ConfigurationResolver({}, explicit).resolve()

    rendered = _rendered(caught.value)
    assert "SENTINEL-LEFT-4d7b19" not in rendered
    assert "SENTINEL-RIGHT-4d7b19" not in rendered
    # The diagnosis survives: the user is told which two keys disagree.
    assert "CAMUNDA_CLIENT_SECRET" in rendered
    assert "CAMUNDA_CLIENT_AUTH_CLIENTSECRET" in rendered


def test_environment_alias_conflict_on_the_client_secret_does_not_echo_the_values() -> (
    None
):
    environment: CamundaSdkConfigPartial = {
        "CAMUNDA_CLIENT_SECRET": "SENTINEL-ENV-LEFT-4d7b19",
        "CAMUNDA_CLIENT_AUTH_CLIENTSECRET": "SENTINEL-ENV-RIGHT-4d7b19",
    }

    with pytest.raises(ValueError) as caught:
        ConfigurationResolver(environment).resolve()

    rendered = _rendered(caught.value)
    assert "SENTINEL-ENV-LEFT-4d7b19" not in rendered
    assert "SENTINEL-ENV-RIGHT-4d7b19" not in rendered
    assert "CAMUNDA_CLIENT_SECRET" in rendered


def test_alias_conflict_on_a_non_secret_key_still_shows_the_values() -> None:
    """Redaction is limited to credentials; other conflicts stay diagnosable."""

    explicit: CamundaSdkConfigPartial = {
        "ZEEBE_REST_ADDRESS": "http://left.local/v2",
        "CAMUNDA_REST_ADDRESS": "http://right.local/v2",
    }

    with pytest.raises(ValueError) as caught:
        ConfigurationResolver({}, explicit).resolve()

    rendered = _rendered(caught.value)
    assert "http://left.local/v2" in rendered
    assert "http://right.local/v2" in rendered


# --- pydantic validation errors -----------------------------------------------------


def _configuration_missing_the_client_id() -> dict[str, Any]:
    """A configuration that fails validation while carrying every credential."""

    values: dict[str, Any] = {
        "CAMUNDA_AUTH_STRATEGY": "OAUTH",
        "CAMUNDA_MTLS_CERT": "-----BEGIN CERTIFICATE-----not-a-secret",
    }
    for key in SECRET_CONFIG_KEYS:
        values[key] = _sentinel_for(key)
    # The alias pair must agree, or the alias check fires before validation.
    values["CAMUNDA_CLIENT_AUTH_CLIENTSECRET"] = values["CAMUNDA_CLIENT_SECRET"]
    return values


def test_no_credential_appears_in_a_validation_error() -> None:
    environment = _configuration_missing_the_client_id()

    with pytest.raises(ValueError) as caught:
        ConfigurationResolver(environment).resolve()

    rendered = _rendered(caught.value)

    leaked = [key for key in SECRET_CONFIG_KEYS if _sentinel_for(key) in rendered]
    assert leaked == [], f"credential value echoed in the error for: {leaked}"
    # The diagnosis survives.
    assert "CAMUNDA_CLIENT_ID" in rendered


def test_no_credential_appears_in_a_validation_error_raised_at_client_construction() -> (
    None
):
    from camunda_orchestration_sdk import CamundaClient

    configuration = _configuration_missing_the_client_id()

    with pytest.raises(ValueError) as caught:
        CamundaClient(configuration=cast(CamundaSdkConfigPartial, configuration))

    rendered = _rendered(caught.value)
    leaked = [key for key in SECRET_CONFIG_KEYS if _sentinel_for(key) in rendered]
    assert leaked == [], f"credential value echoed in the error for: {leaked}"


def test_an_invalid_non_secret_value_is_still_shown() -> None:
    """Redaction must not blind the user to the value that was actually rejected."""

    environment: dict[str, Any] = {"CAMUNDA_WORKER_TIMEOUT": "not-a-number"}

    with pytest.raises(ValueError) as caught:
        ConfigurationResolver(environment).resolve()

    assert "not-a-number" in _rendered(caught.value)


def test_a_rejected_credential_value_is_reported_without_echoing_it() -> None:
    """The one case where the rejected value *is* the credential."""

    environment: dict[str, Any] = {
        "CAMUNDA_AUTH_STRATEGY": "OAUTH",
        "CAMUNDA_CLIENT_ID": "visible-client-id",
        "CAMUNDA_CLIENT_SECRET": 1234567890123,
        "CAMUNDA_CLIENT_AUTH_CLIENTSECRET": 1234567890123,
    }

    try:
        ConfigurationResolver(environment).resolve()
    except ValueError as exc:
        assert "1234567890123" not in _rendered(exc)
    else:  # pragma: no cover - documents the alternative outcome
        pytest.fail("expected a non-string client secret to be rejected")


def test_an_empty_credential_still_produces_its_own_validation_error() -> None:
    """Redaction must not make an absent credential look present.

    A placeholder is non-empty, so redacting ``""`` would let the redacted copy pass
    the presence check the real configuration failed — and the user would lose the
    diagnosis.
    """

    environment: dict[str, Any] = {
        "CAMUNDA_AUTH_STRATEGY": "BASIC",
        "CAMUNDA_BASIC_AUTH_USERNAME": "admin",
        "CAMUNDA_BASIC_AUTH_PASSWORD": "",
    }

    with pytest.raises(ValidationError) as caught:
        ConfigurationResolver(environment).resolve()

    assert "CAMUNDA_BASIC_AUTH_PASSWORD" in _rendered(caught.value)


def test_an_empty_credential_alongside_another_error_keeps_both_diagnoses() -> None:
    environment: dict[str, Any] = {
        "CAMUNDA_AUTH_STRATEGY": "BASIC",
        "CAMUNDA_BASIC_AUTH_USERNAME": "admin",
        "CAMUNDA_BASIC_AUTH_PASSWORD": "",
        "CAMUNDA_WORKER_TIMEOUT": "not-a-number",
    }

    with pytest.raises(ValidationError) as caught:
        ConfigurationResolver(environment).resolve()

    rendered = _rendered(caught.value)
    assert "CAMUNDA_WORKER_TIMEOUT" in rendered
