"""
Integration tests for search_process_instances — filter and pagination shape coverage.

The purpose of these tests is typechecking: each test constructs a query using a
specific filter variant or pagination type and calls the API.  We only assert that
we get a valid response with zero or more items; correctness of the filter semantics
is not tested here.

Tests are skipped unless CAMUNDA_INTEGRATION=1 is set in the environment.
"""

from __future__ import annotations

import datetime
import os

import pytest

from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.models import (
    AdvancedDateTimeFilter,
    AdvancedElementInstanceKeyFilter,
    AdvancedElementInstanceStateFilter,
    AdvancedIntegerFilter,
    AdvancedProcessDefinitionKeyFilter,
    AdvancedProcessInstanceKeyFilter,
    AdvancedProcessInstanceStateFilter,
    AdvancedStringFilter,
    CursorBasedBackwardPagination,
    CursorBasedForwardPagination,
    ElementInstanceStateEnum,
    LimitBasedPagination,
    OffsetBasedPagination,
    ProcessInstanceFilterFields,
    ProcessInstanceSearchQuery,
    ProcessInstanceSearchQueryFilter,
    ProcessInstanceSearchQuerySortRequest,
    ProcessInstanceSearchQuerySortRequestField,
    ProcessInstanceStateEnum,
    ProcessInstanceStateExactMatch,
    SortOrderEnum,
    VariableValueFilterProperty,
)
from camunda_orchestration_sdk.semantic_types import EndCursor, StartCursor

pytestmark = pytest.mark.skipif(
    os.environ.get("CAMUNDA_INTEGRATION") != "1",
    reason="Integration tests are disabled unless CAMUNDA_INTEGRATION=1",
)


def _client() -> CamundaAsyncClient:
    return CamundaAsyncClient()


def _assert_valid_response(resp: object) -> None:
    assert resp is not None
    assert hasattr(resp, "items")
    assert isinstance(resp.items, list)  # type: ignore[union-attr]


# =============================================================================
# Pagination variants
# =============================================================================


@pytest.mark.asyncio
async def test_pagination_unset() -> None:
    """No pagination — server applies its default."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(data=ProcessInstanceSearchQuery())
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_pagination_offset_based() -> None:
    """OffsetBasedPagination with from_ and limit."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                page=OffsetBasedPagination(from_=0, limit=10)
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_pagination_offset_based_limit_only() -> None:
    """OffsetBasedPagination with only limit (from_ omitted)."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                page=OffsetBasedPagination(limit=5)
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_pagination_limit_based() -> None:
    """LimitBasedPagination — limit only, no offset."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                page=LimitBasedPagination(limit=20)
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_pagination_cursor_forward() -> None:
    """CursorBasedForwardPagination — fetch first page then advance via endCursor."""
    async with _client() as camunda:
        first = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(page=LimitBasedPagination(limit=1))
        )
        _assert_valid_response(first)
        if first.page is None or not hasattr(first.page, "end_cursor"):  # type: ignore[union-attr]
            pytest.skip("No endCursor in response — cannot test forward cursor pagination")
        cursor = EndCursor(first.page.end_cursor)  # type: ignore[union-attr]
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                page=CursorBasedForwardPagination(after=cursor, limit=5)
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_pagination_cursor_backward() -> None:
    """CursorBasedBackwardPagination — fetch first page then go back via startCursor."""
    async with _client() as camunda:
        first = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(page=OffsetBasedPagination(from_=1, limit=1))
        )
        _assert_valid_response(first)
        if first.page is None or not hasattr(first.page, "start_cursor"):  # type: ignore[union-attr]
            pytest.skip("No startCursor in response — cannot test backward cursor pagination")
        cursor = StartCursor(first.page.start_cursor)  # type: ignore[union-attr]
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                page=CursorBasedBackwardPagination(before=cursor, limit=5)
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# Simple (scalar) filters — exact-match shorthand
# =============================================================================


@pytest.mark.asyncio
async def test_filter_state_active_shorthand() -> None:
    """Filter by state using ProcessInstanceStateExactMatch (the shorthand enum for state)."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    state=ProcessInstanceStateExactMatch.ACTIVE
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_state_completed_shorthand() -> None:
    """Filter by COMPLETED state using ProcessInstanceStateExactMatch."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    state=ProcessInstanceStateExactMatch.COMPLETED
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_has_incident_true() -> None:
    """Filter to process instances that have an active incident."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(has_incident=True)
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_has_incident_false() -> None:
    """Filter to process instances without incidents."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(has_incident=False)
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_has_retries_left() -> None:
    """Filter by has_retries_left boolean."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(has_retries_left=True)
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_has_element_instance_incident() -> None:
    """Filter by has_element_instance_incident boolean."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    has_element_instance_incident=False
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_id_shorthand() -> None:
    """Filter by process_definition_id using a plain string."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_id="non-existent-process"
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_name_shorthand() -> None:
    """Filter by process_definition_name using a plain string."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_name="my-process"
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_version_shorthand() -> None:
    """Filter by process_definition_version using a plain int."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_version=1
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_version_tag_shorthand() -> None:
    """Filter by process_definition_version_tag using a plain string."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_version_tag="v1.0.0"
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_tenant_id_shorthand() -> None:
    """Filter by tenant_id using a plain string."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(tenant_id="<default>")
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_element_id_shorthand() -> None:
    """Filter by element_id using a plain string."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(element_id="StartEvent_1")
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_business_id_shorthand() -> None:
    """Filter by business_id using a plain string."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(business_id="order-123")
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_tags() -> None:
    """Filter by tags list."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(tags=["env:prod", "team:core"])
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_batch_operation_key_shorthand() -> None:
    """Filter by batch_operation_key using a plain string."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    batch_operation_key="non-existent-batch"
                )
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# AdvancedStringFilter — all operators
# =============================================================================


@pytest.mark.asyncio
async def test_filter_process_definition_name_advanced_eq() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_name=AdvancedStringFilter(eq="my-process")
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_name_advanced_neq() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_name=AdvancedStringFilter(neq="excluded-process")
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_name_advanced_like() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_name=AdvancedStringFilter(like="order-*")
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_name_advanced_in() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_name=AdvancedStringFilter(
                        in_=["process-a", "process-b"]
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_name_advanced_not_in() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_name=AdvancedStringFilter(
                        not_in=["excluded-a", "excluded-b"]
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_tenant_id_advanced_eq() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    tenant_id=AdvancedStringFilter(eq="<default>")
                )
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# Key filters (AdvancedProcessDefinitionKeyFilter, etc.)
# =============================================================================


@pytest.mark.asyncio
async def test_filter_process_definition_key_advanced_eq() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_key=AdvancedProcessDefinitionKeyFilter(
                        eq="2251799813686749"
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_key_advanced_in() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_key=AdvancedProcessDefinitionKeyFilter(
                        in_=["2251799813686749", "2251799813686750"]
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_key_advanced_not_in() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_key=AdvancedProcessDefinitionKeyFilter(
                        not_in=["2251799813686749"]
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_key_advanced_exists() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_key=AdvancedProcessDefinitionKeyFilter(
                        exists=True
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_instance_key_advanced_eq() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_instance_key=AdvancedProcessInstanceKeyFilter(
                        eq="2251799813690746"
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_instance_key_advanced_in() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_instance_key=AdvancedProcessInstanceKeyFilter(
                        in_=["2251799813690746", "2251799813690747"]
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_parent_process_instance_key_advanced() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    parent_process_instance_key=AdvancedProcessInstanceKeyFilter(
                        exists=True
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_parent_element_instance_key_advanced() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    parent_element_instance_key=AdvancedElementInstanceKeyFilter(
                        exists=True
                    )
                )
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# AdvancedIntegerFilter — all operators
# =============================================================================


@pytest.mark.asyncio
async def test_filter_process_definition_version_advanced_eq() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_version=AdvancedIntegerFilter(eq=1)
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_version_advanced_gte() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_version=AdvancedIntegerFilter(gte=1)
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_version_advanced_range() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_version=AdvancedIntegerFilter(gte=1, lte=5)
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_version_advanced_in() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_version=AdvancedIntegerFilter(in_=[1, 2, 3])
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_process_definition_version_advanced_exists() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_version=AdvancedIntegerFilter(exists=True)
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_incident_error_hash_code_advanced_eq() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    incident_error_hash_code=AdvancedIntegerFilter(eq=12345)
                )
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# AdvancedDateTimeFilter — all operators
# =============================================================================


@pytest.mark.asyncio
async def test_filter_start_date_advanced_gte() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    start_date=AdvancedDateTimeFilter(
                        gte=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_start_date_advanced_range() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    start_date=AdvancedDateTimeFilter(
                        gte=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
                        lte=datetime.datetime(2030, 1, 1, tzinfo=datetime.timezone.utc),
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_start_date_advanced_exists() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    start_date=AdvancedDateTimeFilter(exists=True)
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_end_date_advanced_exists_false() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    end_date=AdvancedDateTimeFilter(exists=False)
                )
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# AdvancedProcessInstanceStateFilter
# =============================================================================


@pytest.mark.asyncio
async def test_filter_state_advanced_eq() -> None:
    from camunda_orchestration_sdk.models import AdvancedProcessInstanceStateFilterEq

    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    state=AdvancedProcessInstanceStateFilter(
                        eq=AdvancedProcessInstanceStateFilterEq.ACTIVE
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_state_advanced_neq() -> None:
    from camunda_orchestration_sdk.models import AdvancedProcessInstanceStateFilterNeq

    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    state=AdvancedProcessInstanceStateFilter(
                        neq=AdvancedProcessInstanceStateFilterNeq.COMPLETED
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_state_advanced_in() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    state=AdvancedProcessInstanceStateFilter(
                        in_=[ProcessInstanceStateEnum.ACTIVE]
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_state_advanced_exists() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    state=AdvancedProcessInstanceStateFilter(exists=True)
                )
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# AdvancedElementInstanceStateFilter
# =============================================================================


@pytest.mark.asyncio
async def test_filter_element_instance_state_advanced_in() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    element_instance_state=AdvancedElementInstanceStateFilter(
                        in_=[ElementInstanceStateEnum.ACTIVE]
                    )
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_element_instance_state_advanced_exists() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    element_instance_state=AdvancedElementInstanceStateFilter(
                        exists=True
                    )
                )
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# VariableValueFilterProperty — variable value filters
# =============================================================================


@pytest.mark.asyncio
async def test_filter_variables_plain_string_value() -> None:
    """Filter by variable with an exact string value."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    variables=[
                        VariableValueFilterProperty(
                            name="orderId", value='"order-123"'
                        )
                    ]
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_variables_advanced_string_filter() -> None:
    """Filter by variable with an AdvancedStringFilter for like-matching."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    variables=[
                        VariableValueFilterProperty(
                            name="orderId",
                            value=AdvancedStringFilter(like='"order-*"'),
                        )
                    ]
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_variables_multiple() -> None:
    """Filter by multiple variables."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    variables=[
                        VariableValueFilterProperty(
                            name="status", value='"active"'
                        ),
                        VariableValueFilterProperty(
                            name="amount", value=AdvancedStringFilter(like="1*")
                        ),
                    ]
                )
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# OR compound filter
# =============================================================================


@pytest.mark.asyncio
async def test_filter_or_state_combinations() -> None:
    """Combine two state filters with OR logic."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    or_=[
                        ProcessInstanceFilterFields(
                            state=ProcessInstanceStateExactMatch.ACTIVE
                        ),
                        ProcessInstanceFilterFields(
                            state=ProcessInstanceStateExactMatch.COMPLETED,
                            has_incident=True,
                        ),
                    ]
                )
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_filter_or_with_advanced_filters() -> None:
    """OR filter using advanced filter types in each branch."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    or_=[
                        ProcessInstanceFilterFields(
                            process_definition_name=AdvancedStringFilter(
                                like="order-*"
                            )
                        ),
                        ProcessInstanceFilterFields(
                            process_definition_name=AdvancedStringFilter(
                                like="invoice-*"
                            )
                        ),
                    ]
                )
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# Sort variants — all sort fields, both orders
# =============================================================================


@pytest.mark.asyncio
async def test_sort_by_start_date_desc() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.STARTDATE,
                        order=SortOrderEnum.DESC,
                    )
                ]
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_sort_by_start_date_asc() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.STARTDATE,
                        order=SortOrderEnum.ASC,
                    )
                ]
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_sort_by_process_instance_key() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.PROCESSINSTANCEKEY,
                        order=SortOrderEnum.ASC,
                    )
                ]
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_sort_by_state() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.STATE,
                    )
                ]
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_sort_by_process_definition_key() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.PROCESSDEFINITIONKEY,
                        order=SortOrderEnum.DESC,
                    )
                ]
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_sort_by_process_definition_name() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.PROCESSDEFINITIONNAME,
                        order=SortOrderEnum.ASC,
                    )
                ]
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_sort_by_process_definition_version() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.PROCESSDEFINITIONVERSION,
                        order=SortOrderEnum.DESC,
                    )
                ]
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_sort_by_end_date() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.ENDDATE,
                        order=SortOrderEnum.DESC,
                    )
                ]
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_sort_by_tenant_id() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.TENANTID,
                        order=SortOrderEnum.ASC,
                    )
                ]
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_sort_by_business_id() -> None:
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.BUSINESSID,
                        order=SortOrderEnum.ASC,
                    )
                ]
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_sort_multiple_fields() -> None:
    """Multiple sort criteria — primary by state, secondary by start date."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.STATE,
                        order=SortOrderEnum.ASC,
                    ),
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.STARTDATE,
                        order=SortOrderEnum.DESC,
                    ),
                ]
            )
        )
        _assert_valid_response(resp)


# =============================================================================
# Combined filter + pagination + sort
# =============================================================================


@pytest.mark.asyncio
async def test_combined_filter_pagination_sort() -> None:
    """Exercise filter, pagination and sort together."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    state=ProcessInstanceStateExactMatch.ACTIVE,
                    has_incident=False,
                ),
                page=OffsetBasedPagination(from_=0, limit=20),
                sort=[
                    ProcessInstanceSearchQuerySortRequest(
                        field=ProcessInstanceSearchQuerySortRequestField.STARTDATE,
                        order=SortOrderEnum.DESC,
                    )
                ],
            )
        )
        _assert_valid_response(resp)


@pytest.mark.asyncio
async def test_combined_advanced_filter_limit_based_pagination() -> None:
    """Advanced filter operators with LimitBasedPagination."""
    async with _client() as camunda:
        resp = await camunda.search_process_instances(
            data=ProcessInstanceSearchQuery(
                filter_=ProcessInstanceSearchQueryFilter(
                    process_definition_version=AdvancedIntegerFilter(gte=1),
                    start_date=AdvancedDateTimeFilter(
                        gte=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
                    ),
                ),
                page=LimitBasedPagination(limit=10),
            )
        )
        _assert_valid_response(resp)
