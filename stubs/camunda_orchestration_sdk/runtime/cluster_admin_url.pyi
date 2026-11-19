from __future__ import annotations

from collections.abc import Callable
from typing import Any
import httpx

HttpxArgs = dict[str, Any]
RequestHook = Callable[[httpx.Request], object]
_CLUSTER_ADMIN_PREFIX = "/cluster/v2/"
_DOCUMENT_V2_SUFFIX = "/v2"

def _normalise_base_path(base_url: str | httpx.URL | None) -> str: ...
def rewrite_cluster_admin_url(url: httpx.URL, base_path: str = "/v2") -> httpx.URL: ...
def inject_cluster_admin_url_hook(
    httpx_args: dict[str, Any] | None,
    *,
    base_url: str | httpx.URL | None = None,
    async_client: bool = False,
) -> dict[str, Any]: ...
def append_request_hook(
    httpx_args: HttpxArgs | None, request_hook: RequestHook
) -> HttpxArgs: ...
