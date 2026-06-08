"""Typed variable maps with DTO-driven queries (issue #144).

This runtime helper lets a caller declare a Pydantic model describing the
variables they care about and have the SDK:

1. **Derive the query** — the declared field names (honouring Pydantic aliases)
   are turned into a ``name $in [...]`` filter, so only the declared variables
   are fetched. Memory is bounded by the DTO shape, not by the total number of
   variables on the process instance.
2. **Map the response onto the DTO** — values (returned as serialized JSON
   strings) are parsed and exposed through a :class:`VariableMap`:

   * :meth:`VariableMap.get` — lenient access; missing variables read as
     ``None``.
   * :meth:`VariableMap.validate` — strict access; constructs the Pydantic
     model, raising :class:`pydantic.ValidationError` if required fields are
     absent or values fail validation.

Design notes (see issue #144):

* **Pagination** is driven to exhaustion over the ``$in``-filtered result set.
  Because the server-side filter already bounds the result to the declared
  names, this stays memory-bounded even on the unhappy path (a declared
  variable simply does not appear). There is no "stop early once all names are
  found" optimisation — that would require an ordering guarantee the API does
  not make.
* **Scope collisions** are surfaced, not guessed. BPMN variables are scoped
  (process-level vs. local element scopes); the DTO is a flat map. If the same
  variable name is returned at more than one scope, a
  :class:`VariableScopeCollisionError` is raised instructing the caller to pass
  ``scope_key`` to disambiguate. This follows the repo's no-silent-failure rule.
* **No silent failure on malformed values.** A *missing* variable is legitimate
  (read as ``None`` via :meth:`VariableMap.get`). A variable that is *present*
  but whose value is not parseable JSON raises
  :class:`VariableDeserializationError` rather than silently becoming ``None``.
  Full (untruncated) values are always requested so values are never truncated
  mid-parse.
"""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Iterable, ItemsView, Iterator, KeysView, ValuesView
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic import BaseModel

from camunda_orchestration_sdk.models.advanced_string_filter import AdvancedStringFilter
from camunda_orchestration_sdk.models.cursor_based_forward_pagination import (
    CursorBasedForwardPagination,
)
from camunda_orchestration_sdk.models.limit_based_pagination import LimitBasedPagination
from camunda_orchestration_sdk.models.variable_search_query import VariableSearchQuery
from camunda_orchestration_sdk.models.variable_search_query_filter import (
    VariableSearchQueryFilter,
)
from camunda_orchestration_sdk.runtime.eventual import ConsistencyOptions
from camunda_orchestration_sdk.semantic_types import EndCursor, TenantId

if TYPE_CHECKING:
    from camunda_orchestration_sdk import CamundaAsyncClient, CamundaClient
    from camunda_orchestration_sdk.models.variable_search_result import (
        VariableSearchResult,
    )

T = TypeVar("T", bound=BaseModel)

__all__ = [
    "TypedVariablesError",
    "VariableDeserializationError",
    "VariableMap",
    "VariableScopeCollisionError",
    "search_variables_as_dto_async",
    "search_variables_as_dto_sync",
]


class TypedVariablesError(Exception):
    """Base class for typed-variable-map errors."""


class VariableScopeCollisionError(TypedVariablesError):
    """Raised when a variable name is returned at more than one scope.

    The DTO is a flat name->value map, but BPMN variables are scoped. When a
    declared variable resolves to multiple scopes, the SDK cannot deterministically
    choose one, so it raises rather than guessing. Pass ``scope_key`` to the
    search call to disambiguate.
    """

    def __init__(self, name: str, scope_keys: list[str]) -> None:
        self.name = name
        self.scope_keys = scope_keys
        super().__init__(
            f"Variable {name!r} was found at multiple scopes ({', '.join(scope_keys)}). "
            "Pass scope_key=... to the search to select a single scope."
        )


class VariableDeserializationError(TypedVariablesError):
    """Raised when a present variable value is not parseable as JSON.

    A *missing* variable is not an error (it reads as ``None`` via
    :meth:`VariableMap.get`); a *present but malformed* value is, and is surfaced
    here rather than silently dropped.
    """

    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value
        super().__init__(
            f"Variable {name!r} has a value that is not valid JSON and cannot be deserialized."
        )


class VariableMap(Generic[T]):
    """Result of a DTO-driven variable search.

    Holds the parsed variable values keyed by their query name (the Pydantic
    field name, or its alias when one is declared). Provides lenient dict-style
    access and a strict :meth:`validate` that constructs the declared model.
    """

    def __init__(self, model: type[T], raw: dict[str, Any]) -> None:
        self._model = model
        self._raw = raw

    def get(self, name: str, default: Any = None) -> Any:
        """Lenient access. Returns the parsed value, or ``default`` if absent."""
        return self._raw.get(name, default)

    def validate(self) -> T:
        """Strict access. Construct and return the declared model.

        Raises:
            pydantic.ValidationError: If required fields are missing or any value
                fails the model's validation.
        """
        return self._model.model_validate(self._raw)

    @property
    def raw(self) -> dict[str, Any]:
        """A copy of the parsed name->value map."""
        return dict(self._raw)

    def __getitem__(self, name: str) -> Any:
        return self._raw[name]

    def __contains__(self, name: object) -> bool:
        return name in self._raw

    def __iter__(self) -> Iterator[str]:
        return iter(self._raw)

    def __len__(self) -> int:
        return len(self._raw)

    def keys(self) -> KeysView[str]:
        return self._raw.keys()

    def values(self) -> ValuesView[Any]:
        return self._raw.values()

    def items(self) -> ItemsView[str, Any]:
        return self._raw.items()

    def __repr__(self) -> str:
        return f"VariableMap(model={self._model.__name__}, keys={list(self._raw)})"


def _extract_query_names(dto: type[BaseModel]) -> list[str]:
    """Return the variable names to query for, derived from the DTO fields.

    The query name is the field's alias when one is declared, otherwise the field
    name. This is the same key :meth:`pydantic.BaseModel.model_validate` expects,
    so the parsed map can be validated directly.
    """
    if not (isinstance(dto, type) and issubclass(dto, BaseModel)):
        raise TypeError(
            "search_variables_as_dto requires a pydantic BaseModel subclass; "
            f"got {dto!r}."
        )
    names: list[str] = []
    for field_name, info in dto.model_fields.items():
        alias = info.alias
        names.append(alias if isinstance(alias, str) and alias else field_name)
    return names


def _build_query(
    *,
    names: list[str],
    page_size: int,
    process_instance_key: str,
    scope_key: str | None,
    tenant_id: str | None,
    after: str | None,
) -> VariableSearchQuery:
    filter_ = VariableSearchQueryFilter(
        name=AdvancedStringFilter(in_=list(names)),
        process_instance_key=process_instance_key,
    )
    if scope_key is not None:
        filter_.scope_key = scope_key
    if tenant_id is not None:
        filter_.tenant_id = TenantId(tenant_id)

    page: LimitBasedPagination | CursorBasedForwardPagination
    if after is not None:
        page = CursorBasedForwardPagination(after=EndCursor(after), limit=page_size)
    else:
        page = LimitBasedPagination(limit=page_size)

    return VariableSearchQuery(filter_=filter_, page=page)


def _parse_value(name: str, value: str) -> Any:
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError) as exc:
        raise VariableDeserializationError(name=name, value=value) from exc


class _VariableCollector:
    """Incrementally collapses paged variable items into a parsed map.

    Memory stays bounded by the DTO shape rather than the total number of paged
    items: only the first value seen per requested name is retained, alongside the
    set of scope keys observed for that name (used for collision detection). Pages
    are ingested as they arrive and discarded, so large ``value`` strings for
    undeclared variables are never accumulated.
    """

    def __init__(self, query_names: set[str]) -> None:
        self._query_names = query_names
        self._chosen: dict[str, VariableSearchResult] = {}
        self._scopes_seen: dict[str, set[str]] = {}

    def ingest(self, items: Iterable[VariableSearchResult]) -> None:
        """Fold one page of results into the retained per-name state."""
        for item in items:
            name = item.name
            if name not in self._query_names:
                continue
            self._scopes_seen.setdefault(name, set()).add(str(item.scope_key))
            self._chosen.setdefault(name, item)

    def finalize(self) -> dict[str, Any]:
        """Parse retained values, raising on scope collisions or malformed JSON.

        Detects scope collisions (same name at multiple scope keys) and raises
        rather than choosing arbitrarily. Parses each value as JSON, raising on
        malformed present values.
        """
        raw: dict[str, Any] = {}
        for name, item in self._chosen.items():
            scopes = self._scopes_seen[name]
            if len(scopes) > 1:
                raise VariableScopeCollisionError(name=name, scope_keys=sorted(scopes))
            raw[name] = _parse_value(name, item.value)
        return raw

    @property
    def found_names(self) -> set[str]:
        """The declared names for which a value has been collected so far."""
        return set(self._chosen.keys())


# Minimum delay between consistency re-reads, to prevent busy-looping.
_MIN_POLL_INTERVAL_MS: int = 10


def _validate_page_size(page_size: int) -> None:
    if page_size < 1:
        raise ValueError(f"page_size must be >= 1, got {page_size}.")


def _collect_one_pass_sync(
    client: CamundaClient,
    *,
    query_names: list[str],
    page_size: int,
    process_instance_key: str,
    scope_key: str | None,
    tenant_id: str | None,
) -> _VariableCollector:
    """Run one full pagination pass and return the collected state (sync)."""
    collector = _VariableCollector(set(query_names))
    after: str | None = None
    seen_cursors: set[str] = set()
    while True:
        query = _build_query(
            names=query_names,
            page_size=page_size,
            process_instance_key=process_instance_key,
            scope_key=scope_key,
            tenant_id=tenant_id,
            after=after,
        )
        result = client.search_variables(data=query, truncate_values=False)
        collector.ingest(result.items)
        end_cursor = result.page.end_cursor
        if not end_cursor or not result.items or end_cursor in seen_cursors:
            break
        seen_cursors.add(end_cursor)
        after = end_cursor
    return collector


def search_variables_as_dto_sync(
    client: CamundaClient,
    dto: type[T],
    *,
    process_instance_key: str,
    scope_key: str | None = None,
    tenant_id: str | None = None,
    page_size: int = 100,
    consistency: ConsistencyOptions | None = None,
) -> VariableMap[T]:
    """Fetch the variables declared by ``dto`` for a process instance (sync).

    See the module docstring for the full design. The query is derived from the
    DTO fields, paginated to exhaustion over the filtered result set, collapsed
    by name (raising on scope collisions), and parsed into a :class:`VariableMap`.

    Eventual consistency: variable indexes update asynchronously, so a freshly
    written variable may not be visible immediately. When ``consistency`` is
    supplied, the *whole* collection is re-read until **every** declared variable
    is visible or the ``wait_up_to_ms`` budget expires — waiting is applied at the
    collection level, not per page, so a declared variable that indexes later than
    its siblings is still awaited. On expiry the best snapshot collected so far is
    returned (it is *not* an error); :meth:`VariableMap.validate` is where a
    genuinely-absent required variable surfaces. Without ``consistency`` the
    variables are read exactly once.
    """
    _validate_page_size(page_size)
    query_names = _extract_query_names(dto)
    if not query_names:
        return VariableMap(dto, {})

    wait_up_to_ms = consistency.wait_up_to_ms if consistency is not None else 0
    poll_interval_s = (
        max(_MIN_POLL_INTERVAL_MS, consistency.poll_interval_ms) / 1000.0
        if consistency is not None
        else 0.0
    )
    declared = set(query_names)
    deadline = time.monotonic() + wait_up_to_ms / 1000.0

    while True:
        collector = _collect_one_pass_sync(
            client,
            query_names=query_names,
            page_size=page_size,
            process_instance_key=process_instance_key,
            scope_key=scope_key,
            tenant_id=tenant_id,
        )
        remaining = declared - collector.found_names
        if not remaining or wait_up_to_ms <= 0 or time.monotonic() >= deadline:
            return VariableMap(dto, collector.finalize())
        time.sleep(min(poll_interval_s, max(0.0, deadline - time.monotonic())))


async def _collect_one_pass_async(
    client: CamundaAsyncClient,
    *,
    query_names: list[str],
    page_size: int,
    process_instance_key: str,
    scope_key: str | None,
    tenant_id: str | None,
) -> _VariableCollector:
    """Run one full pagination pass and return the collected state (async)."""
    collector = _VariableCollector(set(query_names))
    after: str | None = None
    seen_cursors: set[str] = set()
    while True:
        query = _build_query(
            names=query_names,
            page_size=page_size,
            process_instance_key=process_instance_key,
            scope_key=scope_key,
            tenant_id=tenant_id,
            after=after,
        )
        result = await client.search_variables(data=query, truncate_values=False)
        collector.ingest(result.items)
        end_cursor = result.page.end_cursor
        if not end_cursor or not result.items or end_cursor in seen_cursors:
            break
        seen_cursors.add(end_cursor)
        after = end_cursor
    return collector


async def search_variables_as_dto_async(
    client: CamundaAsyncClient,
    dto: type[T],
    *,
    process_instance_key: str,
    scope_key: str | None = None,
    tenant_id: str | None = None,
    page_size: int = 100,
    consistency: ConsistencyOptions | None = None,
) -> VariableMap[T]:
    """Fetch the variables declared by ``dto`` for a process instance (async).

    Async variant of :func:`search_variables_as_dto_sync`; see it for the
    eventual-consistency semantics of ``consistency``.
    """
    _validate_page_size(page_size)
    query_names = _extract_query_names(dto)
    if not query_names:
        return VariableMap(dto, {})

    wait_up_to_ms = consistency.wait_up_to_ms if consistency is not None else 0
    poll_interval_s = (
        max(_MIN_POLL_INTERVAL_MS, consistency.poll_interval_ms) / 1000.0
        if consistency is not None
        else 0.0
    )
    declared = set(query_names)
    deadline = time.monotonic() + wait_up_to_ms / 1000.0

    while True:
        collector = await _collect_one_pass_async(
            client,
            query_names=query_names,
            page_size=page_size,
            process_instance_key=process_instance_key,
            scope_key=scope_key,
            tenant_id=tenant_id,
        )
        remaining = declared - collector.found_names
        if not remaining or wait_up_to_ms <= 0 or time.monotonic() >= deadline:
            return VariableMap(dto, collector.finalize())
        await asyncio.sleep(min(poll_interval_s, max(0.0, deadline - time.monotonic())))
