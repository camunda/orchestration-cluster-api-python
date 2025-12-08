import os
import pytest
from camunda_orchestration_sdk import CamundaClient

pytestmark = pytest.mark.skipif(
    os.environ.get("CAMUNDA_INTEGRATION") != "1",
    reason="Integration tests are disabled unless CAMUNDA_INTEGRATION=1",
)

def _make_client():
    host = os.environ.get("CAMUNDA_BASE_URL", "http://localhost:8080/v2")
    return CamundaClient(base_url=host)


@pytest.mark.asyncio
async def test_get_topology_smoke():
    async with _make_client() as api_client:
        resp = await api_client.get_topology_async()
        print(resp)
        assert resp is not None
        # Basic shape checks if available
        # TopologyResponse fields are spec-defined; we only smoke-check here
        assert hasattr(resp, "brokers") or hasattr(resp, "clusterSize") or hasattr(resp, "gatewayVersion")

