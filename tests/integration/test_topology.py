import os
import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("CAMUNDA_INTEGRATION") != "1",
    reason="Integration tests are disabled unless CAMUNDA_INTEGRATION=1",
)

def _make_client():
    import camunda_orchestration_sdk

    host = os.environ.get("CAMUNDA_BASE_URL", "http://localhost:8080/v2")
    configuration = camunda_orchestration_sdk.Configuration(host=host)
    return camunda_orchestration_sdk.ApiClient(configuration)


@pytest.mark.asyncio
async def test_get_topology_smoke():
    import camunda_orchestration_sdk
    async with _make_client() as api_client:
        api = camunda_orchestration_sdk.ClusterApi(api_client)
        resp = await api.get_topology()
        print(resp)
        assert resp is not None
        # Basic shape checks if available
        # TopologyResponse fields are spec-defined; we only smoke-check here
        assert hasattr(resp, "brokers") or hasattr(resp, "clusterSize") or hasattr(resp, "gatewayVersion")

