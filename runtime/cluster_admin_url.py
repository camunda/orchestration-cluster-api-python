"""Honour the operation-level ``servers`` override for cluster-admin endpoints.

The OpenAPI spec serves every ordinary operation under the document-level server
base ``{schema}://{host}:{port}/v2``, so the SDK bakes the ``/v2`` suffix into the
httpx ``base_url``. The cluster-wide ``/cluster/v2/...`` operations are different:
each path item overrides ``servers`` with the bare root ``{schema}://{host}:{port}``
(no ``/v2``). Their path key already carries the ``/cluster/v2`` prefix, so the
correct request is ``GET /cluster/v2/topology`` — **not** ``GET /v2/cluster/v2/topology``.

``openapi-python-client`` does not model per-operation servers, so every generated
cluster-admin operation emits a root-relative ``/cluster/v2/...`` URL that httpx then
concatenates onto the ``/v2`` base, producing the doubled ``/v2/cluster/v2/...`` path.

This module installs an httpx request event hook that undoes the doubling: whenever a
request path carries the document ``/v2`` base immediately in front of the
``/cluster/v2/`` prefix, the hook drops that one ``/v2`` segment. This mirrors the
Camunda gateway's own ``OpenApiYamlLoader.KNOWN_ROOTS`` logic, which matches the literal
``/cluster/v2/`` prefix to skip the runtime ``/v2`` prefixing that every other path gets.

Any host prefix in front of the ``/v2`` suffix (e.g. a gateway cluster-id segment) is
preserved — only the single ``/v2`` suffix declared by the document server is dropped.
When the base URL carries no ``/v2`` suffix (``CAMUNDA_REST_ADDRESS_EXACT``), there is
nothing to drop and the path is left untouched.
"""

from __future__ import annotations

from typing import Any

import httpx

# The literal the Camunda gateway matches on to serve cluster-wide operations at the
# bare root instead of under the document's ``/v2`` base.
_CLUSTER_ADMIN_PREFIX = "/cluster/v2/"

# The doubled segment produced when the ``/v2`` document base is concatenated in front
# of a ``/cluster/v2/...`` path key.
_DOUBLED_PREFIX = "/v2" + _CLUSTER_ADMIN_PREFIX


def rewrite_cluster_admin_url(url: httpx.URL) -> httpx.URL:
    """Drop the document ``/v2`` base that precedes a ``/cluster/v2/`` path.

    Returns the URL unchanged when it is not a doubled cluster-admin path.
    """
    raw_path = url.raw_path.decode("ascii")
    if _DOUBLED_PREFIX not in raw_path:
        return url
    fixed = raw_path.replace(_DOUBLED_PREFIX, _CLUSTER_ADMIN_PREFIX, 1)
    return url.copy_with(raw_path=fixed.encode("ascii"))


def inject_cluster_admin_url_hook(
    httpx_args: dict[str, Any] | None,
    *,
    async_client: bool = False,
) -> dict[str, Any]:
    """Return a copy of ``httpx_args`` with a request hook that fixes cluster-admin URLs.

    The hook is appended after any existing request hooks (including the auth hook), so
    header injection still sees the original request before the path is normalised. The
    URL rewrite is independent of headers, so ordering relative to auth does not matter.
    """

    request_hook: Any
    if async_client:

        async def _request_hook_async(request: httpx.Request) -> None:
            request.url = rewrite_cluster_admin_url(request.url)

        request_hook = _request_hook_async
    else:

        def _request_hook_sync(request: httpx.Request) -> None:
            request.url = rewrite_cluster_admin_url(request.url)

        request_hook = _request_hook_sync

    out: dict[str, Any] = dict(httpx_args or {})

    existing_event_hooks = out.get("event_hooks")
    event_hooks: dict[str, Any]
    if existing_event_hooks is None:
        event_hooks = {}
    elif isinstance(existing_event_hooks, dict):
        event_hooks = dict(existing_event_hooks)  # type: ignore[arg-type]
    else:
        raise TypeError("httpx_args['event_hooks'] must be a dict")

    existing_request_hooks = event_hooks.get("request")
    if existing_request_hooks is None:
        request_hooks: list[Any] = []
    elif isinstance(existing_request_hooks, (list, tuple)):
        request_hooks = list(existing_request_hooks)  # type: ignore[arg-type]
    else:
        raise TypeError("httpx_args['event_hooks']['request'] must be a list or tuple")

    request_hooks.append(request_hook)
    event_hooks["request"] = request_hooks
    out["event_hooks"] = event_hooks
    return out
