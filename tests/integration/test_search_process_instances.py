import os
import pytest
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk.models.search_process_instances_data import SearchProcessInstancesData
from camunda_orchestration_sdk.models.search_process_instances_data_page import SearchProcessInstancesDataPage

pytestmark = pytest.mark.skipif(
    os.environ.get("CAMUNDA_INTEGRATION") != "1",
    reason="Integration tests are disabled unless CAMUNDA_INTEGRATION=1",
)

def _make_client():
    host = os.environ.get("CAMUNDA_BASE_URL", "http://localhost:8080/v2")
    return CamundaClient(base_url=host)


@pytest.mark.asyncio
async def test_searchProcessInstances_smoke():
    async with _make_client() as camunda:
        # Construct the query
        # Note: 'from' is aliased to 'var_from' in Python because 'from' is a reserved keyword
        # But since SearchProcessInstancesDataPage is a dict wrapper, we use dict assignment.
        
        page = SearchProcessInstancesDataPage()
        page["from"] = 0
        page["limit"] = 50
        
        query = SearchProcessInstancesData(
            page=page
        )        
        resp = await camunda.search_process_instances_async(data=query)

        print(resp)
        assert resp is not None
        # Check for expected fields in SearchProcessInstancesResponse200
        assert hasattr(resp, "items")
        assert hasattr(resp, "page")

