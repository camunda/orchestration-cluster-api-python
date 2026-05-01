from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, TypeVar
T = TypeVar("T")
_ABORT_STATUSES: frozenset[int] = frozenset({400, 401, 403, 409, 422})
_DEFAULT_POLL_INTERVAL_MS: int = 500
_MIN_POLL_INTERVAL_MS: int = 10
class EventualConsistencyTimeoutError(Exception):
    def __init__(self, *, attempts: int, elapsed_ms: int, last_status: int | None = None, operation_id: str | None = None) -> None: ...
@dataclass
class ConsistencyOptions:
    wait_up_to_ms: int
    poll_interval_ms: int = _DEFAULT_POLL_INTERVAL_MS
    predicate: Callable[[Any], bool] | None = None
def _effective_interval(options: ConsistencyOptions) -> float: ...
def _should_abort(exc: Exception) -> bool: ...
def _default_predicate(result: Any, is_get: bool) -> bool: ...
def eventual_poll(operation_id: str, is_get: bool, invoke: Callable[[], T], options: ConsistencyOptions, on_retry: Callable[[int], None] | None = None) -> T: ...
async def eventual_poll_async(operation_id: str, is_get: bool, invoke: Callable[[], Awaitable[T]], options: ConsistencyOptions, on_retry: Callable[[int], None] | None = None) -> T: ...
