from __future__ import annotations

from typing import Any
import httpx

_CLUSTER_ADMIN_PREFIX = "/cluster/v2/"
_DOUBLED_PREFIX = "/v2" + _CLUSTER_ADMIN_PREFIX

def rewrite_cluster_admin_url(url: httpx.URL) -> httpx.URL: ...
def inject_cluster_admin_url_hook(
    httpx_args: dict[str, Any] | None, *, async_client: bool = False
) -> dict[str, Any]: ...
