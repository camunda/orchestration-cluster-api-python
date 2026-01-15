import pytest
from pydantic import ValidationError


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


def test_camunda_client_oauth_requires_client_credentials():
    from camunda_orchestration_sdk import CamundaClient

    with pytest.raises(ValidationError):
        CamundaClient(configuration={"CAMUNDA_AUTH_STRATEGY": "OAUTH"})
