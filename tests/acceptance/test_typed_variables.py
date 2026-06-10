"""Acceptance tests for the typed variable map / DTO-driven query helper (issue #144)."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import BaseModel, Field, ValidationError

from camunda_orchestration_sdk.models.advanced_string_filter import AdvancedStringFilter
from camunda_orchestration_sdk.models.search_query_page_response import (
    SearchQueryPageResponse,
)
from camunda_orchestration_sdk.models.variable_search_query import VariableSearchQuery
from camunda_orchestration_sdk.models.variable_search_query_result import (
    VariableSearchQueryResult,
)
from camunda_orchestration_sdk.models.variable_search_result import VariableSearchResult
from camunda_orchestration_sdk.runtime.eventual import ConsistencyOptions
from camunda_orchestration_sdk.runtime.typed_variables import (
    VariableDeserializationError,
    VariableMap,
    VariableScopeCollisionError,
    search_variables_as_dto_async,
    search_variables_as_dto_sync,
)
from camunda_orchestration_sdk.semantic_types import EndCursor


class OrderVars(BaseModel):
    order_id: str
    amount: float | None = None


class AliasVars(BaseModel):
    order_id: str = Field(alias="orderId")


def _item(
    name: str,
    value: str,
    *,
    scope_key: str = "100",
    process_instance_key: str = "100",
) -> VariableSearchResult:
    return VariableSearchResult.from_dict(
        {
            "value": value,
            "isTruncated": False,
            "name": name,
            "tenantId": "<default>",
            "variableKey": "1",
            "scopeKey": scope_key,
            "processInstanceKey": process_instance_key,
            "rootProcessInstanceKey": None,
        }
    )


def _page(
    items: list[VariableSearchResult], *, end_cursor: str | None = None
) -> VariableSearchQueryResult:
    return VariableSearchQueryResult(
        items=items,
        page=SearchQueryPageResponse(
            total_items=len(items),
            has_more_total_items=False,
            start_cursor=None,
            end_cursor=EndCursor(end_cursor) if end_cursor is not None else None,
        ),
    )


def _sync_client(*pages: VariableSearchQueryResult) -> MagicMock:
    client = MagicMock()
    client.search_variables = MagicMock(side_effect=list(pages))
    return client


# --- query derivation -------------------------------------------------------


def test_derives_in_filter_from_dto_fields() -> None:
    client = _sync_client(
        _page([_item("order_id", json.dumps("ord-1")), _item("amount", "42.5")])
    )

    search_variables_as_dto_sync(client, OrderVars, process_instance_key="100")

    call = client.search_variables.call_args
    query = call.kwargs["data"]
    assert isinstance(query, VariableSearchQuery)
    assert isinstance(query.filter_.name, AdvancedStringFilter)
    # $in is derived from the declared field names.
    assert query.filter_.name.in_ == ["order_id", "amount"]
    assert query.filter_.process_instance_key == "100"
    # Full values are requested so values are never truncated mid-parse.
    assert call.kwargs["truncate_values"] is False


def test_query_name_honours_pydantic_alias() -> None:
    client = _sync_client(_page([_item("orderId", json.dumps("ord-1"))]))

    result = search_variables_as_dto_sync(client, AliasVars, process_instance_key="100")

    query = client.search_variables.call_args.kwargs["data"]
    assert query.filter_.name.in_ == ["orderId"]
    # The alias is also the validation key, so the model constructs cleanly.
    assert result.validate().order_id == "ord-1"


def test_scope_key_and_tenant_id_are_applied() -> None:
    client = _sync_client(_page([_item("order_id", json.dumps("ord-1"))]))

    search_variables_as_dto_sync(
        client,
        OrderVars,
        process_instance_key="100",
        scope_key="200",
        tenant_id="acme",
    )

    filter_ = client.search_variables.call_args.kwargs["data"].filter_
    assert filter_.scope_key == "200"
    assert filter_.tenant_id == "acme"


# --- pagination -------------------------------------------------------------


def test_paginates_to_exhaustion() -> None:
    client = _sync_client(
        _page([_item("order_id", json.dumps("ord-1"))], end_cursor="c1"),
        _page([_item("amount", "42.5")], end_cursor=None),
    )

    result = search_variables_as_dto_sync(client, OrderVars, process_instance_key="100")

    assert client.search_variables.call_count == 2
    # The second page's cursor was threaded into the follow-up request.
    second_query = client.search_variables.call_args_list[1].kwargs["data"]
    assert second_query.page.after == "c1"
    assert result.get("order_id") == "ord-1"
    assert result.get("amount") == 42.5


def test_pagination_stops_on_repeated_cursor() -> None:
    # A server that keeps returning the same cursor must not loop forever.
    client = _sync_client(
        _page([_item("order_id", json.dumps("ord-1"))], end_cursor="loop"),
        _page([_item("amount", "42.5")], end_cursor="loop"),
    )

    result = search_variables_as_dto_sync(client, OrderVars, process_instance_key="100")

    assert client.search_variables.call_count == 2
    assert result.get("amount") == 42.5


# --- collapse / scope collisions -------------------------------------------


def test_scope_collision_raises() -> None:
    client = _sync_client(
        _page(
            [
                _item("order_id", json.dumps("a"), scope_key="100"),
                _item("order_id", json.dumps("b"), scope_key="200"),
            ]
        )
    )

    with pytest.raises(VariableScopeCollisionError) as exc:
        search_variables_as_dto_sync(client, OrderVars, process_instance_key="100")

    assert exc.value.name == "order_id"
    assert exc.value.scope_keys == ["100", "200"]


def test_same_name_same_scope_is_not_a_collision() -> None:
    client = _sync_client(
        _page(
            [
                _item("order_id", json.dumps("a"), scope_key="100"),
                _item("order_id", json.dumps("a"), scope_key="100"),
            ]
        )
    )

    result = search_variables_as_dto_sync(client, OrderVars, process_instance_key="100")

    assert result.get("order_id") == "a"


# --- value deserialization / no silent failure ------------------------------


def test_malformed_value_raises_not_silently_dropped() -> None:
    client = _sync_client(_page([_item("order_id", "not-valid-json")]))

    with pytest.raises(VariableDeserializationError) as exc:
        search_variables_as_dto_sync(client, OrderVars, process_instance_key="100")

    assert exc.value.name == "order_id"


def test_missing_variable_is_none_via_get() -> None:
    # order_id absent from the response; amount present.
    client = _sync_client(_page([_item("amount", "42.5")]))

    result = search_variables_as_dto_sync(client, OrderVars, process_instance_key="100")

    assert result.get("order_id") is None
    assert result.get("amount") == 42.5


# --- VariableMap access modes ----------------------------------------------


def test_validate_returns_typed_model() -> None:
    client = _sync_client(
        _page([_item("order_id", json.dumps("ord-1")), _item("amount", "42.5")])
    )

    result = search_variables_as_dto_sync(client, OrderVars, process_instance_key="100")

    validated = result.validate()
    assert isinstance(validated, OrderVars)
    assert validated.order_id == "ord-1"
    assert validated.amount == 42.5


def test_validate_raises_when_required_field_missing() -> None:
    # Required order_id is absent.
    client = _sync_client(_page([_item("amount", "42.5")]))

    result = search_variables_as_dto_sync(client, OrderVars, process_instance_key="100")

    with pytest.raises(ValidationError):
        result.validate()


def test_variable_map_is_mapping_like() -> None:
    vm: VariableMap[OrderVars] = VariableMap(
        OrderVars, {"order_id": "x", "amount": 1.0}
    )
    assert "order_id" in vm
    assert vm["order_id"] == "x"
    assert len(vm) == 2
    assert set(vm.keys()) == {"order_id", "amount"}
    assert dict(vm.items()) == {"order_id": "x", "amount": 1.0}
    assert vm.raw == {"order_id": "x", "amount": 1.0}


# --- input validation -------------------------------------------------------


def test_non_basemodel_dto_raises_type_error() -> None:
    client = _sync_client(_page([]))

    class NotAModel:
        order_id: str

    with pytest.raises(TypeError):
        search_variables_as_dto_sync(client, NotAModel, process_instance_key="100")  # ty: ignore[invalid-argument-type]


def test_invalid_page_size_raises_value_error() -> None:
    client = _sync_client(_page([]))

    with pytest.raises(ValueError):
        search_variables_as_dto_sync(
            client, OrderVars, process_instance_key="100", page_size=0
        )


# --- async variant ----------------------------------------------------------


@pytest.mark.asyncio
async def test_async_variant_collects_and_validates() -> None:
    client = MagicMock()
    client.search_variables = AsyncMock(
        side_effect=[
            _page([_item("order_id", json.dumps("ord-1"))], end_cursor="c1"),
            _page([_item("amount", "42.5")], end_cursor=None),
        ]
    )

    result = await search_variables_as_dto_async(
        client, OrderVars, process_instance_key="100"
    )

    assert client.search_variables.await_count == 2
    validated = result.validate()
    assert validated.order_id == "ord-1"
    assert validated.amount == 42.5


# --- eventual consistency ---------------------------------------------------
#
# Variable indexes update asynchronously, so a freshly written variable may not
# be visible immediately — and different declared variables can become visible
# at different times. The consistency budget must therefore wait until *every*
# declared variable is visible, not settle as soon as the first one appears.


def test_consistency_rereads_until_all_declared_variables_are_visible() -> None:
    # The first two reads only see order_id; amount appears on the third. A
    # naive "settle once any item is present" check would stop after read 1 and
    # never observe amount.
    order_only = _page([_item("order_id", json.dumps("ord-1"))])
    both = _page(
        [_item("order_id", json.dumps("ord-1")), _item("amount", "42.5")]
    )
    client = _sync_client(order_only, order_only, both)

    result = search_variables_as_dto_sync(
        client,
        OrderVars,
        process_instance_key="100",
        consistency=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
    )

    assert client.search_variables.call_count == 3
    assert "order_id" in result
    assert "amount" in result
    assert result.validate().amount == 42.5


def test_consistency_returns_partial_snapshot_when_budget_expires() -> None:
    # amount never becomes visible. The call must terminate within the budget
    # and return the best snapshot rather than hanging; the genuinely-absent
    # variable then surfaces via validate(), not by blocking forever.
    client = MagicMock()
    client.search_variables = MagicMock(
        return_value=_page([_item("order_id", json.dumps("ord-1"))])
    )

    result = search_variables_as_dto_sync(
        client,
        OrderVars,
        process_instance_key="100",
        consistency=ConsistencyOptions(wait_up_to_ms=30, poll_interval_ms=10),
    )

    assert "order_id" in result
    assert "amount" not in result
    assert result.get("amount") is None


def test_reads_exactly_once_when_no_consistency_is_requested() -> None:
    # Without a consistency budget the variables are read exactly once, even if
    # a declared variable is missing — no polling, no waiting.
    client = _sync_client(_page([_item("order_id", json.dumps("ord-1"))]))

    result = search_variables_as_dto_sync(
        client, OrderVars, process_instance_key="100"
    )

    assert client.search_variables.call_count == 1
    assert "order_id" in result
    assert "amount" not in result


@pytest.mark.asyncio
async def test_consistency_rereads_until_all_visible_async() -> None:
    order_only = _page([_item("order_id", json.dumps("ord-1"))])
    both = _page(
        [_item("order_id", json.dumps("ord-1")), _item("amount", "42.5")]
    )
    client = MagicMock()
    client.search_variables = AsyncMock(side_effect=[order_only, order_only, both])

    result = await search_variables_as_dto_async(
        client,
        OrderVars,
        process_instance_key="100",
        consistency=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
    )

    assert client.search_variables.await_count == 3
    assert "order_id" in result
    assert "amount" in result
    assert result.validate().amount == 42.5
