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

This module installs an httpx request event hook that undoes the doubling. The hook
is anchored to the *configured* base path: only when the request path starts with the
configured base path immediately followed by the ``/cluster/v2/`` prefix is the base
path's trailing ``/v2`` segment dropped. This mirrors the Camunda gateway's own
``OpenApiYamlLoader.KNOWN_ROOTS`` logic, which matches the literal ``/cluster/v2/``
prefix to skip the runtime ``/v2`` prefixing that every other path gets.

Anchoring to the configured base (rather than replacing the literal ``/v2`` substring
anywhere in the path) is what keeps gateway deployments safe: with
``CAMUNDA_REST_ADDRESS_EXACT=true`` and a base such as
``https://host/v2/cluster/v2/proxy``, an ordinary ``GET /topology`` request resolves
to ``/v2/cluster/v2/proxy/topology`` — a path that merely *contains* ``/v2/cluster/v2/``
inside the gateway prefix. A substring rewrite would eat the first segment of that
prefix and reroute the request; the anchored rewrite only ever strips the configured
base path's trailing ``/v2`` segment when a cluster-admin path follows it, and leaves
every other path untouched. When the base URL carries no ``/v2`` suffix at all, there
is nothing to drop and paths are left untouched.
"""

from __future__ import annotations

from typing import Any

import httpx

# The literal the Camunda gateway matches on to serve cluster-wide operations at the
# bare root instead of under the document's ``/v2`` base.
_CLUSTER_ADMIN_PREFIX = "/cluster/v2/"

# The path suffix the spec's document-level server adds to every ordinary operation.
_DOCUMENT_V2_SUFFIX = "/v2"


def _normalise_base_path(base_url: str | httpx.URL | None) -> str:
    """Return the configured base path, without any trailing slash.

    An empty or root-only base path normalises to ``""`` so that ``base_path + suffix``
    comparisons degenerate to a plain ``startswith`` on the suffix.
    """
    if base_url is None:
        return ""
    path = httpx.URL(str(base_url)).path
    if path == "/":
        return ""
    return path.rstrip("/")


def rewrite_cluster_admin_url(url: httpx.URL, base_path: str = "/v2") -> httpx.URL:
    """Drop the configured base path's trailing ``/v2`` before a ``/cluster/v2/`` path.

    ``base_path`` is the path component of the SDK's configured REST address
    (``CAMUNDA_REST_ADDRESS``), e.g. ``/v2`` or ``/clusterA/v2``; a trailing slash is
    ignored. The rewrite applies only when the request path starts with ``base_path``
    immediately followed by the ``/cluster/v2/`` prefix — i.e. exactly the doubling
    produced by concatenating the configured base onto a cluster-admin path key — and
    only the base path's trailing ``/v2`` segment is removed, so any gateway prefix in
    front of it is preserved. When the configured base does not end with the document
    ``/v2`` suffix (e.g. ``CAMUNDA_REST_ADDRESS_EXACT``), there is no doubling to undo
    and the URL is returned unchanged.
    """
    base_path = base_path.rstrip("/")
    if not base_path.endswith(_DOCUMENT_V2_SUFFIX):
        return url
    doubled_prefix = base_path + _CLUSTER_ADMIN_PREFIX
    raw_path = url.raw_path.decode("ascii")
    if not raw_path.startswith(doubled_prefix):
        return url
    keep = len(base_path) - len(_DOCUMENT_V2_SUFFIX)
    fixed = raw_path[:keep] + raw_path[len(base_path) :]
    return url.copy_with(raw_path=fixed.encode("ascii"))


def inject_cluster_admin_url_hook(
    httpx_args: dict[str, Any] | None,
    *,
    base_url: str | httpx.URL | None = None,
    async_client: bool = False,
) -> dict[str, Any]:
    """Return a copy of ``httpx_args`` with a request hook that fixes cluster-admin URLs.

    ``base_url`` is the SDK's configured REST address; its path component anchors the
    rewrite so only the configured base is ever stripped from a request path. When
    omitted it defaults to the spec's document server suffix ``/v2``.

    The hook is appended after any existing request hooks (including the auth hook), so
    header injection still sees the original request before the path is normalised. The
    URL rewrite is independent of headers, so ordering relative to auth does not matter.
    """

    base_path = _normalise_base_path(base_url)

    request_hook: Any
    if async_client:

        async def _request_hook_async(request: httpx.Request) -> None:
            request.url = rewrite_cluster_admin_url(request.url, base_path)

        request_hook = _request_hook_async
    else:

        def _request_hook_sync(request: httpx.Request) -> None:
            request.url = rewrite_cluster_admin_url(request.url, base_path)

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
