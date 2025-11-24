import os
from camunda_orchestration_sdk.api.process_instance_api import ProcessInstanceSearchQuery
from camunda_orchestration_sdk.models.process_instance_search_query import ProcessInstanceSearchQuery
from camunda_orchestration_sdk.models.search_query_page_request import SearchQueryPageRequest
from camunda_orchestration_sdk.models.offset_pagination import OffsetPagination
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
async def test_searchProcessInstances_smoke():
    import camunda_orchestration_sdk
    async with _make_client() as api_client:
        api = camunda_orchestration_sdk.ProcessInstanceApi(api_client)
        # Construct the query
        # Note: 'from' is aliased to 'var_from' in Python because 'from' is a reserved keyword
        pagination = OffsetPagination(var_from=0, limit=50)
        query = ProcessInstanceSearchQuery(
            page=SearchQueryPageRequest(pagination)
        )        
        resp = await api.search_process_instances(process_instance_search_query=query)
        print(resp)
        assert resp is not None
        # Check for expected fields in ProcessInstanceSearchQueryResult
        assert hasattr(resp, "items")
        assert hasattr(resp, "page")

