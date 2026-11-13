"""Property-based redaction invariants (a pilot of sdk-infra#87).

The example-based redaction tests pin the fields and values their authors thought of.
These state the invariant instead -- *whatever* a credential's value, it never reaches
a rendering of the configuration or an error raised for it, while the non-secret fields
still do -- and let Hypothesis look for a value that breaks it.

Deterministic by construction: ``derandomize=True`` derives every example from the
test's own source, so a given revision always runs the same examples, and the example
database is switched off so nothing is carried between runs.
"""

from __future__ import annotations

from typing import Any, Callable, cast

from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
import pytest

from camunda_orchestration_sdk.runtime.configuration_resolver import (
    SECRET_CONFIG_KEYS,
    CamundaSdkConfigPartial,
    CamundaSdkConfiguration,
    ConfigurationResolver,
)

_PROPERTY = settings(
    derandomize=True,
    database=None,
    max_examples=100,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)

#: Long enough that an accidental overlap with the surrounding (non-secret) text is
#: rare; the rare overlap that remains is filtered out per example below, not ignored.
_secret = st.text(min_size=8, max_size=64)
_client_id = st.text(min_size=1, max_size=32)

_PLACEHOLDER = "placeholder-secret"


def _credential_fields() -> list[str]:
    return sorted(
        name
        for name in CamundaSdkConfiguration.model_fields
        if not name.endswith("_PATH")
        and any(m in name for m in ("SECRET", "PASSWORD", "PASSPHRASE", "KEY"))
    )


def _configuration(secret: str, client_id: str, **extra: Any) -> dict[str, Any]:
    """Every credential field set to ``secret``, with a valid non-secret remainder."""

    values: dict[str, Any] = {name: secret for name in _credential_fields()}
    values.update(
        CAMUNDA_AUTH_STRATEGY="OAUTH",
        CAMUNDA_CLIENT_ID=client_id,
        # A client key without a certificate is rejected by the model's own validation.
        CAMUNDA_MTLS_CERT="-----BEGIN CERTIFICATE-----not-a-secret",
    )
    values.update(extra)
    return values


def _renderings(config: CamundaSdkConfiguration) -> str:
    return f"{config!r}\n{config!s}"


def test_the_property_sweep_covers_every_secret_the_redaction_knows_about() -> None:
    """Guards the guard: the credential set below must be the one redaction uses."""

    assert set(_credential_fields()) == set(SECRET_CONFIG_KEYS)


@_PROPERTY
@given(secret=_secret, client_id=_client_id)
def test_no_secret_value_reaches_a_configuration_rendering(
    secret: str, client_id: str
) -> None:
    baseline = _renderings(
        CamundaSdkConfiguration(**_configuration(_PLACEHOLDER, client_id))
    )
    # A secret that occurs in the non-secret text is not a leak when it shows up there.
    assume(secret not in baseline)

    rendered = _renderings(CamundaSdkConfiguration(**_configuration(secret, client_id)))

    assert secret not in rendered


@_PROPERTY
@given(secret=_secret, client_id=_client_id)
def test_non_secret_fields_are_preserved_by_redaction(
    secret: str, client_id: str
) -> None:
    config = CamundaSdkConfiguration(**_configuration(secret, client_id))
    rendered = _renderings(config)

    # Rendered by ``repr``, as pydantic does for every field; redaction removes the
    # credentials and nothing else.
    assert f"CAMUNDA_CLIENT_ID={client_id!r}" in rendered
    assert "CAMUNDA_AUTH_STRATEGY='OAUTH'" in rendered
    # And the value is still there to be used.
    assert config.CAMUNDA_CLIENT_SECRET == secret


def _error_text(raise_it: Callable[[], object]) -> str:
    with pytest.raises(ValueError) as caught:
        raise_it()
    exc = caught.value
    rendered = f"{exc}\n{exc!r}"
    errors = getattr(exc, "errors", None)
    if callable(errors):
        rendered += "\n" + "\n".join(repr(error) for error in errors())
    return rendered


@_PROPERTY
@given(secret=_secret)
def test_no_secret_value_reaches_a_validation_error(secret: str) -> None:
    def resolve(value: str) -> object:
        # Rejected: OAuth needs a client id, so the error carries the whole input.
        values = _configuration(value, "unused")
        del values["CAMUNDA_CLIENT_ID"]
        return ConfigurationResolver(cast(CamundaSdkConfigPartial, values)).resolve()

    baseline = _error_text(lambda: resolve(_PLACEHOLDER))
    assume(secret not in baseline)

    rendered = _error_text(lambda: resolve(secret))

    assert secret not in rendered
    # The diagnosis survives redaction.
    assert "CAMUNDA_CLIENT_ID" in rendered


@_PROPERTY
@given(left=_secret, right=_secret)
def test_no_secret_value_reaches_an_alias_conflict_error(left: str, right: str) -> None:
    assume(left != right)

    def resolve(first: str, second: str) -> object:
        explicit = cast(
            CamundaSdkConfigPartial,
            {
                "CAMUNDA_CLIENT_SECRET": first,
                "CAMUNDA_CLIENT_AUTH_CLIENTSECRET": second,
            },
        )
        return ConfigurationResolver({}, explicit).resolve()

    baseline = _error_text(lambda: resolve(_PLACEHOLDER, _PLACEHOLDER + "-2"))
    assume(left not in baseline and right not in baseline)

    rendered = _error_text(lambda: resolve(left, right))

    assert left not in rendered
    assert right not in rendered
    assert "CAMUNDA_CLIENT_SECRET" in rendered
