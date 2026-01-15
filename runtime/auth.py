from __future__ import annotations

from typing import Any, Mapping, Protocol, runtime_checkable

import httpx


@runtime_checkable
class AuthProvider(Protocol):
    """Provides per-request authentication headers.

    Implementations are expected to be lightweight and safe to call for every request.

    The preferred Python method name is ``get_headers``.
    """

    def get_headers(self) -> Mapping[str, str]:
        ...


class NullAuthProvider:
    """Default auth provider that adds no headers."""

    def get_headers(self) -> dict[str, str]:
        return {}
def _resolve_auth_headers(provider: object) -> Mapping[str, str]:
    get_headers = getattr(provider, "get_headers", None)
    if callable(get_headers):
        headers = get_headers()
        if not isinstance(headers, Mapping):
            raise TypeError("auth_provider.get_headers() must return a mapping")
        return headers
    
    raise TypeError(
        "auth_provider must implement get_headers() -> Mapping[str, str]"
    )


def inject_auth_event_hooks(
    httpx_args: dict[str, Any] | None,
    auth_provider: object,
    *,
    async_client: bool = False,
) -> dict[str, Any]:
    """Return a copy of httpx_args with a request hook that applies auth headers.

    This uses httpx event hooks so we don't have to inject headers in every generated API call.
    """

    if async_client:
        async def _request_hook(request: httpx.Request) -> None:
            headers = _resolve_auth_headers(auth_provider)
            if headers:
                request.headers.update(headers)
    else:
        def _request_hook(request: httpx.Request) -> None:
            headers = _resolve_auth_headers(auth_provider)
            if headers:
                request.headers.update(headers)

    out: dict[str, Any] = dict(httpx_args or {})

    # Normalize event_hooks to a writable dict.
    existing_event_hooks = out.get("event_hooks")
    event_hooks: dict[str, Any]
    if existing_event_hooks is None:
        event_hooks = {}
    elif isinstance(existing_event_hooks, dict):
        event_hooks = dict(existing_event_hooks)
    else:
        raise TypeError("httpx_args['event_hooks'] must be a dict")

    # Normalize request hooks to a list.
    existing_request_hooks = event_hooks.get("request")
    if existing_request_hooks is None:
        request_hooks: list[Any] = []
    elif isinstance(existing_request_hooks, list):
        request_hooks = list(existing_request_hooks)
    elif isinstance(existing_request_hooks, tuple):
        request_hooks = list(existing_request_hooks)
    else:
        raise TypeError("httpx_args['event_hooks']['request'] must be a list or tuple")

    request_hooks.append(_request_hook)
    event_hooks["request"] = request_hooks
    out["event_hooks"] = event_hooks

    return out
