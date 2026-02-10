import pytest
from pydantic import ValidationError
@pytest.fixture(autouse=True)
def _clear_camunda_env(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    """Acceptance tests must not depend on the developer shell environment."""

    for key in (
        "CAMUNDA_REST_ADDRESS",
        "ZEEBE_REST_ADDRESS",
        "CAMUNDA_AUTH_STRATEGY",
        "CAMUNDA_OAUTH_URL",
        "CAMUNDA_TOKEN_AUDIENCE",
        "CAMUNDA_CLIENT_ID",
        "CAMUNDA_CLIENT_SECRET",
        "CAMUNDA_CLIENT_AUTH_CLIENTID",
        "CAMUNDA_CLIENT_AUTH_CLIENTSECRET",
        "CAMUNDA_BASIC_AUTH_USERNAME",
        "CAMUNDA_BASIC_AUTH_PASSWORD",
    ):
        monkeypatch.delenv(key, raising=False)


def test_camunda_client_resolves_defaults():
    from camunda_orchestration_sdk import CamundaClient

    client = CamundaClient()

    assert client.configuration.ZEEBE_REST_ADDRESS == "http://localhost:8080/v2"
    assert client.configuration.CAMUNDA_REST_ADDRESS == "http://localhost:8080/v2"
    assert client.configuration.CAMUNDA_AUTH_STRATEGY == "NONE"

    httpx_client = client.client.get_httpx_client()
    assert str(httpx_client.base_url).rstrip("/") == "http://localhost:8080/v2"


def test_camunda_client_explicit_overrides_environment(monkeypatch: pytest.MonkeyPatch):
    from camunda_orchestration_sdk import CamundaClient

    monkeypatch.setenv("ZEEBE_REST_ADDRESS", "http://env:8080/v2")

    client = CamundaClient(configuration={"CAMUNDA_REST_ADDRESS": "http://explicit:8080/v2"})

    # Explicit should win even across alias keys, and effective config should populate both.
    assert client.configuration.ZEEBE_REST_ADDRESS == "http://explicit:8080/v2"
    assert client.configuration.CAMUNDA_REST_ADDRESS == "http://explicit:8080/v2"

    httpx_client = client.client.get_httpx_client()
    assert str(httpx_client.base_url).rstrip("/") == "http://explicit:8080/v2"


def test_camunda_client_conflicting_alias_values_raises():
    from camunda_orchestration_sdk import CamundaClient

    with pytest.raises(ValueError, match="Conflicting explicit configuration"):
        CamundaClient(
            configuration={
                "ZEEBE_REST_ADDRESS": "http://a:8080/v2",
                "CAMUNDA_REST_ADDRESS": "http://b:8080/v2",
            }
        )


def test_rest_address_normalization_appends_v2():
    from camunda_orchestration_sdk.runtime.configuration_resolver import ConfigurationResolver

    resolved = ConfigurationResolver(
        environment={
            # Simulate SaaS env exports that provide the cluster base URL without /v2.
            "ZEEBE_REST_ADDRESS": "https://example.invalid/cluster",
        },
        explicit_configuration=None,
    ).resolve()

    assert resolved.effective.CAMUNDA_REST_ADDRESS == "https://example.invalid/cluster/v2"
    assert resolved.effective.ZEEBE_REST_ADDRESS == "https://example.invalid/cluster/v2"


def test_rest_address_normalization_preserves_existing_v2():
    from camunda_orchestration_sdk.runtime.configuration_resolver import ConfigurationResolver

    resolved = ConfigurationResolver(
        environment={
            "CAMUNDA_REST_ADDRESS": "http://localhost:8080/v2",
        },
        explicit_configuration=None,
    ).resolve()

    assert resolved.effective.CAMUNDA_REST_ADDRESS == "http://localhost:8080/v2"


def test_auth_strategy_infers_oauth_when_credentials_present():
    from camunda_orchestration_sdk.runtime.configuration_resolver import ConfigurationResolver

    resolved = ConfigurationResolver(
        environment={
            "CAMUNDA_CLIENT_ID": "id",
            "CAMUNDA_CLIENT_SECRET": "secret",
        },
        explicit_configuration=None,
    ).resolve()

    assert resolved.effective.CAMUNDA_AUTH_STRATEGY == "OAUTH"

def test_auth_strategy_is_not_inferred_when_explicitly_set_none_even_if_oauth_credentials_present() -> None:
    from camunda_orchestration_sdk.runtime.configuration_resolver import ConfigurationResolver

    resolver = ConfigurationResolver(
        environment={
            "CAMUNDA_AUTH_STRATEGY": "NONE",
            "CAMUNDA_CLIENT_ID": "my-client-id",
            "CAMUNDA_CLIENT_SECRET": "my-client-secret",
        }
    )
    resolved = resolver.resolve()
    assert resolved.effective.CAMUNDA_AUTH_STRATEGY == "NONE"

def test_auth_strategy_infers_basic_when_credentials_present():
    from camunda_orchestration_sdk.runtime.configuration_resolver import ConfigurationResolver

    resolved = ConfigurationResolver(
        environment={
            "CAMUNDA_BASIC_AUTH_USERNAME": "u",
            "CAMUNDA_BASIC_AUTH_PASSWORD": "p",
        },
        explicit_configuration=None,
    ).resolve()

    assert resolved.effective.CAMUNDA_AUTH_STRATEGY == "BASIC"


def test_camunda_client_oauth_requires_client_credentials():
    from camunda_orchestration_sdk import CamundaClient

    with pytest.raises(ValidationError):
        CamundaClient(configuration={"CAMUNDA_AUTH_STRATEGY": "OAUTH"})
