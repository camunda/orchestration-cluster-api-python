import os
import pytest
from camunda_orchestration_sdk import Client
from camunda_orchestration_sdk.models.search_process_instances_body import SearchProcessInstancesBody
from camunda_orchestration_sdk.models.search_process_instances_body_page import SearchProcessInstancesBodyPage

pytestmark = pytest.mark.skipif(
    os.environ.get("CAMUNDA_INTEGRATION") != "1",
    reason="Integration tests are disabled unless CAMUNDA_INTEGRATION=1",
)

def _make_client():
    host = os.environ.get("CAMUNDA_BASE_URL", "http://localhost:8080/v2")
    return Client(base_url=host)


@pytest.mark.asyncio
async def test_searchProcessInstances_smoke():
    async with _make_client() as api_client:
        # Construct the query
        # Note: 'from' is aliased to 'var_from' in Python because 'from' is a reserved keyword
        # But since SearchProcessInstancesBodyPage is a dict wrapper, we use dict assignment.
        
        page = SearchProcessInstancesBodyPage()
        page["from"] = 0
        page["limit"] = 50
        
        query = SearchProcessInstancesBody(
            page=page
        )        
        resp = await api_client.search_process_instances_async(body=query)
        print(resp)
        assert resp is not None
        # Check for expected fields in SearchProcessInstancesResponse200
        assert hasattr(resp, "items")
        assert hasattr(resp, "page")

