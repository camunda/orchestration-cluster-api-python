from __future__ import annotations

from collections.abc import Iterable, ItemsView, Iterator, KeysView, ValuesView
from typing import Any, Generic, TypeVar
from pydantic import BaseModel
from camunda_orchestration_sdk.models.variable_search_query import VariableSearchQuery
from camunda_orchestration_sdk.runtime.eventual import ConsistencyOptions
from camunda_orchestration_sdk import CamundaAsyncClient, CamundaClient
from camunda_orchestration_sdk.models.variable_search_result import VariableSearchResult

T = TypeVar("T", bound=BaseModel)
__all__ = [
    "TypedVariablesError",
    "VariableDeserializationError",
    "VariableMap",
    "VariableScopeCollisionError",
    "search_variables_as_dto_async",
    "search_variables_as_dto_sync",
]

class TypedVariablesError(Exception): ...

class VariableScopeCollisionError(TypedVariablesError):
    def __init__(self, name: str, scope_keys: list[str]) -> None: ...

class VariableDeserializationError(TypedVariablesError):
    def __init__(self, name: str, value: str) -> None: ...

class VariableMap(Generic[T]):
    def __init__(self, model: type[T], raw: dict[str, Any]) -> None: ...
    def get(self, name: str, default: Any = None) -> Any: ...
    def validate(self) -> T: ...
    @property
    def raw(self) -> dict[str, Any]: ...
    def __getitem__(self, name: str) -> Any: ...
    def __contains__(self, name: object) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def keys(self) -> KeysView[str]: ...
    def values(self) -> ValuesView[Any]: ...
    def items(self) -> ItemsView[str, Any]: ...
    def __repr__(self) -> str: ...

def _extract_query_names(dto: type[BaseModel]) -> list[str]: ...
def _build_query(
    *,
    names: list[str],
    page_size: int,
    process_instance_key: str,
    scope_key: str | None,
    tenant_id: str | None,
    after: str | None,
) -> VariableSearchQuery: ...
def _parse_value(name: str, value: str) -> Any: ...

class _VariableCollector:
    def __init__(self, query_names: set[str]) -> None: ...
    def ingest(self, items: Iterable[VariableSearchResult]) -> None: ...
    def finalize(self) -> dict[str, Any]: ...
    @property
    def found_names(self) -> set[str]: ...

_MIN_POLL_INTERVAL_MS: int = 10

def _validate_page_size(page_size: int) -> None: ...
def _collect_one_pass_sync(
    client: CamundaClient,
    *,
    query_names: list[str],
    page_size: int,
    process_instance_key: str,
    scope_key: str | None,
    tenant_id: str | None,
) -> _VariableCollector: ...
def search_variables_as_dto_sync(
    client: CamundaClient,
    dto: type[T],
    *,
    process_instance_key: str,
    scope_key: str | None = None,
    tenant_id: str | None = None,
    page_size: int = 100,
    consistency: ConsistencyOptions | None = None,
) -> VariableMap[T]: ...
async def _collect_one_pass_async(
    client: CamundaAsyncClient,
    *,
    query_names: list[str],
    page_size: int,
    process_instance_key: str,
    scope_key: str | None,
    tenant_id: str | None,
) -> _VariableCollector: ...
async def search_variables_as_dto_async(
    client: CamundaAsyncClient,
    dto: type[T],
    *,
    process_instance_key: str,
    scope_key: str | None = None,
    tenant_id: str | None = None,
    page_size: int = 100,
    consistency: ConsistencyOptions | None = None,
) -> VariableMap[T]: ...
