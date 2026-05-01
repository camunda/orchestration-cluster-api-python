"""Eventual consistency polling runtime.

Provides transparent retry for endpoints annotated with
``x-eventually-consistent: true`` in the OpenAPI spec.  Both synchronous
and asynchronous polling helpers are included.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, TypeVar, cast

T = TypeVar("T")

# HTTP status codes that should abort polling immediately.
_ABORT_STATUSES: frozenset[int] = frozenset({400, 401, 403, 409, 422})

# Default poll interval when none is configured.
_DEFAULT_POLL_INTERVAL_MS: int = 500

# Minimum poll interval to prevent busy-looping.
_MIN_POLL_INTERVAL_MS: int = 10


class EventualConsistencyTimeoutError(Exception):
    """Raised when an eventually consistent endpoint times out.

    Attributes:
        attempts: Number of polling attempts made.
        elapsed_ms: Total elapsed time in milliseconds.
        last_status: HTTP status code of the last response (if available).
        operation_id: The SDK operation that timed out.
    """

    def __init__(
        self,
        *,
        attempts: int,
        elapsed_ms: int,
        last_status: int | None = None,
        operation_id: str | None = None,
    ) -> None:
        self.attempts = attempts
        self.elapsed_ms = elapsed_ms
        self.last_status = last_status
        self.operation_id = operation_id
        op = f" [{operation_id}]" if operation_id else ""
        super().__init__(
            f"Eventual consistency timeout{op} after {elapsed_ms}ms ({attempts} attempts)"
        )


@dataclass
class ConsistencyOptions:
    """Options for eventual consistency polling.

    Attributes:
        wait_up_to_ms: Maximum time to wait in milliseconds.
            Set to ``0`` to skip polling and return the first response.
        poll_interval_ms: Delay between poll attempts (default 500ms, minimum 10ms).
        predicate: Optional callable that receives the result and returns ``True``
            when the data is considered consistent.  For non-GET endpoints the
            default predicate checks that an ``items`` attribute is non-empty.
    """

    wait_up_to_ms: int
    poll_interval_ms: int = _DEFAULT_POLL_INTERVAL_MS
    predicate: Callable[[Any], bool] | None = None


def _effective_interval(options: ConsistencyOptions) -> float:
    """Return the poll interval in seconds, clamped to the minimum."""
    return max(_MIN_POLL_INTERVAL_MS, options.poll_interval_ms) / 1000.0


def _should_abort(exc: Exception) -> bool:
    """Return True if the error should stop polling immediately."""
    status = getattr(exc, "status_code", None)
    if status is None:
        return True  # not an HTTP error — don't swallow
    if status in _ABORT_STATUSES or status >= 500:
        return True
    return False


def _default_predicate(result: Any, is_get: bool) -> bool:
    """Default success check when no user predicate is provided.

    * GET endpoints: any non-None result is accepted.
    * Non-GET endpoints (search/list): require ``items`` to be non-empty.
    """
    if is_get:
        return result is not None
    if isinstance(result, dict):
        items = cast(dict[str, Any], result).get("items")
    else:
        items = getattr(result, "items", None)
    if isinstance(items, list):
        return len(cast(list[Any], items)) > 0
    return result is not None


def eventual_poll(
    operation_id: str,
    is_get: bool,
    invoke: Callable[[], T],
    options: ConsistencyOptions,
    on_retry: Callable[[int], None] | None = None,
) -> T:
    """Synchronous eventual consistency poller.

    Calls *invoke* repeatedly until the result satisfies the consistency
    predicate or the timeout expires.

    Args:
        operation_id: Name of the SDK operation (for diagnostics).
        is_get: Whether this is a GET endpoint (affects 404 retry).
        invoke: Zero-argument callable that performs the API call.
        options: Polling configuration.
        on_retry: Optional callback invoked with the HTTP status code each
            time the poller swallows an error and retries (e.g. 404 on a GET
            or 429 with backoff).  This lets callers observe retry-worthy
            backpressure signals (such as 429) that would otherwise be hidden
            from the outer wrapper, so they can update backpressure state.

    Returns:
        The result from *invoke* once consistent.

    Raises:
        EventualConsistencyTimeoutError: If the timeout expires.
    """
    if options.wait_up_to_ms <= 0:
        return invoke()

    interval = _effective_interval(options)
    predicate = options.predicate
    start = time.monotonic()
    attempts = 0
    last_status: int | None = None

    while True:
        attempts += 1
        try:
            result = invoke()
            last_status = 200

            ok = predicate(result) if predicate else _default_predicate(result, is_get)
            if ok:
                return result

            elapsed_ms = int((time.monotonic() - start) * 1000)
            if elapsed_ms >= options.wait_up_to_ms:
                raise EventualConsistencyTimeoutError(
                    attempts=attempts,
                    elapsed_ms=elapsed_ms,
                    last_status=last_status,
                    operation_id=operation_id,
                )

            remaining_s = (options.wait_up_to_ms - elapsed_ms) / 1000.0
            time.sleep(min(interval, remaining_s))

        except EventualConsistencyTimeoutError:
            raise

        except Exception as exc:
            status = getattr(exc, "status_code", None)
            last_status = status
            elapsed_ms = int((time.monotonic() - start) * 1000)
            remaining_ms = options.wait_up_to_ms - elapsed_ms

            # GET + 404 → resource not yet visible, retry
            if status == 404 and is_get and remaining_ms > 0:
                if on_retry is not None:
                    on_retry(404)
                remaining_s = remaining_ms / 1000.0
                time.sleep(min(interval, remaining_s))
                continue

            # 429 → rate limited, back off.  Notify the caller so backpressure
            # state can be updated even though the exception is swallowed here.
            if status == 429 and remaining_ms > 0:
                if on_retry is not None:
                    on_retry(429)
                delay = interval * 2
                delay = min(delay, interval * 5, 2.0, remaining_ms / 1000.0)
                time.sleep(delay)
                continue

            if _should_abort(exc):
                raise

            if remaining_ms <= 0:
                raise EventualConsistencyTimeoutError(
                    attempts=attempts,
                    elapsed_ms=elapsed_ms,
                    last_status=status,
                    operation_id=operation_id,
                ) from exc

            raise


async def eventual_poll_async(
    operation_id: str,
    is_get: bool,
    invoke: Callable[[], Awaitable[T]],
    options: ConsistencyOptions,
    on_retry: Callable[[int], None] | None = None,
) -> T:
    """Asynchronous eventual consistency poller.

    Same logic as :func:`eventual_poll` but uses ``asyncio.sleep`` and
    ``await`` for the invoke callable.

    Args:
        operation_id: Name of the SDK operation (for diagnostics).
        is_get: Whether this is a GET endpoint (affects 404 retry).
        invoke: Zero-argument async callable that performs the API call.
        options: Polling configuration.
        on_retry: Optional callback invoked with the HTTP status code each
            time the poller swallows an error and retries (e.g. 404 on a GET
            or 429 with backoff).  This lets callers observe retry-worthy
            backpressure signals (such as 429) that would otherwise be hidden
            from the outer wrapper.

    Returns:
        The result from *invoke* once consistent.

    Raises:
        EventualConsistencyTimeoutError: If the timeout expires.
    """
    if options.wait_up_to_ms <= 0:
        return await invoke()

    interval = _effective_interval(options)
    predicate = options.predicate
    start = time.monotonic()
    attempts = 0
    last_status: int | None = None

    while True:
        attempts += 1
        try:
            result = await invoke()
            last_status = 200

            ok = predicate(result) if predicate else _default_predicate(result, is_get)
            if ok:
                return result

            elapsed_ms = int((time.monotonic() - start) * 1000)
            if elapsed_ms >= options.wait_up_to_ms:
                raise EventualConsistencyTimeoutError(
                    attempts=attempts,
                    elapsed_ms=elapsed_ms,
                    last_status=last_status,
                    operation_id=operation_id,
                )

            remaining_s = (options.wait_up_to_ms - elapsed_ms) / 1000.0
            await asyncio.sleep(min(interval, remaining_s))

        except EventualConsistencyTimeoutError:
            raise

        except Exception as exc:
            status = getattr(exc, "status_code", None)
            last_status = status
            elapsed_ms = int((time.monotonic() - start) * 1000)
            remaining_ms = options.wait_up_to_ms - elapsed_ms

            # GET + 404 → resource not yet visible, retry
            if status == 404 and is_get and remaining_ms > 0:
                if on_retry is not None:
                    on_retry(404)
                remaining_s = remaining_ms / 1000.0
                await asyncio.sleep(min(interval, remaining_s))
                continue

            # 429 → rate limited, back off.  Notify the caller so backpressure
            # state can be updated even though the exception is swallowed here.
            if status == 429 and remaining_ms > 0:
                if on_retry is not None:
                    on_retry(429)
                delay = interval * 2
                delay = min(delay, interval * 5, 2.0, remaining_ms / 1000.0)
                await asyncio.sleep(delay)
                continue

            if _should_abort(exc):
                raise

            if remaining_ms <= 0:
                raise EventualConsistencyTimeoutError(
                    attempts=attempts,
                    elapsed_ms=elapsed_ms,
                    last_status=status,
                    operation_id=operation_id,
                ) from exc

            raise
