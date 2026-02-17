import os
import pytest
from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.models.process_instance_search_query import (
    ProcessInstanceSearchQuery,
)
from camunda_orchestration_sdk.models.offset_based_pagination import (
    OffsetBasedPagination,
)

pytestmark = pytest.mark.skipif(
    os.environ.get("CAMUNDA_INTEGRATION") != "1",
    reason="Integration tests are disabled unless CAMUNDA_INTEGRATION=1",
)


def _make_client():
    return CamundaAsyncClient()


@pytest.mark.asyncio
async def test_searchProcessInstances_smoke():
    async with _make_client() as camunda:
        # Construct the query
        # Note: 'from' is aliased to 'var_from' in Python because 'from' is a reserved keyword
        # But since SearchProcessInstancesDataPage is a dict wrapper, we use dict assignment.

        page = OffsetBasedPagination(from_=0, limit=50)

        query = ProcessInstanceSearchQuery(page=page)
        resp = await camunda.search_process_instances(data=query)

        print(resp)
        assert resp is not None
        # Check for expected fields in SearchProcessInstancesResponse200
        assert hasattr(resp, "items")
        assert hasattr(resp, "page")
