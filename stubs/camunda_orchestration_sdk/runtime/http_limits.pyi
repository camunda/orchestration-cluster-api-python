from __future__ import annotations

from typing import Any

def apply_http_max_connections(
    httpx_args: dict[str, Any] | None, max_connections: int | None
) -> dict[str, Any]: ...
