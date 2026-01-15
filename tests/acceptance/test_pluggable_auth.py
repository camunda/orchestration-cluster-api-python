import httpx
import pytest


class _StaticAuthProvider:
    def __init__(self, header_value: str):
        self.header_value = header_value
        self.calls = 0

    def get_headers(self) -> dict[str, str]:
        self.calls += 1
        return {"X-Test-Auth": self.header_value}


class _CamelCaseAuthProvider:
    def __init__(self, header_value: str):
        self.header_value = header_value
        self.calls = 0

    def get_headers(self) -> dict[str, str]:  # noqa: N802
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


def test_camel_case_provider_supported():
    from camunda_orchestration_sdk import CamundaClient

    seen: dict[str, str | None] = {"x_test_auth": None}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["x_test_auth"] = request.headers.get("X-Test-Auth")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    auth = _CamelCaseAuthProvider("camel")

    client = CamundaClient(auth_provider=auth, httpx_args={"transport": transport})
    response = client.client.get_httpx_client().get("/ping")

    assert response.status_code == 200
    assert seen["x_test_auth"] == "camel"
    assert auth.calls == 1
