import pytest


@pytest.fixture(autouse=True)
def _clear_sdk_env(monkeypatch: pytest.MonkeyPatch) -> None:  # pyright: ignore[reportUnusedFunction]
    """Acceptance tests must not depend on the developer shell environment.

    This clears any SDK-related env vars so defaults are deterministic.
    Individual tests can opt-in to env configuration with monkeypatch.setenv.
    """

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
        "CAMUNDA_SDK_LOG_LEVEL",
        "CAMUNDA_TOKEN_CACHE_DIR",
        "CAMUNDA_TOKEN_DISK_CACHE_DISABLE",
    ):
        monkeypatch.delenv(key, raising=False)
