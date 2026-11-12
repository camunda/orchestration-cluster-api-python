from __future__ import annotations

from typing import Any

import httpx


def apply_http_max_connections(
    httpx_args: dict[str, Any] | None,
    max_connections: int | None,
) -> dict[str, Any]:
    """Apply the ``CAMUNDA_HTTP_MAX_CONNECTIONS`` pool limit to ``httpx_args``.

    When ``max_connections`` is set and the caller did not already supply an
    explicit ``limits`` entry in ``httpx_args``, an
    ``httpx.Limits(max_connections=N, max_keepalive_connections=N)`` is injected
    so both sync and async httpx clients cap their connection pool.

    Precedence: an explicit ``limits`` entry in ``httpx_args`` always wins over
    the configuration value. When ``max_connections`` is ``None`` the arguments
    are returned unchanged.
    """

    args = dict(httpx_args) if httpx_args else {}
    if max_connections is None:
        return args
    if "limits" in args:
        return args
    args["limits"] = httpx.Limits(
        max_connections=max_connections,
        max_keepalive_connections=max_connections,
    )
    return args
