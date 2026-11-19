"""Attributable ``User-Agent`` header for every request the SDK sends.

Gateway usage reports group traffic by the *first* product token in the
``User-Agent`` header, so every SDK request leads with
``camunda-orchestration-sdk-python/<version>``. An application-supplied user
agent (``CAMUNDA_USER_AGENT``, or a ``User-Agent`` header passed by the caller)
is appended after the SDK token -- it never replaces it.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from functools import lru_cache
from typing import Any

import httpx

from collections.abc import Callable

HttpxArgs = dict[str, Any]
RequestHook = Callable[[httpx.Request], object]


def append_request_hook(
    httpx_args: HttpxArgs | None, request_hook: RequestHook
) -> HttpxArgs:
    """Return a copy of ``httpx_args`` with ``request_hook`` appended to the request hooks."""

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

SDK_USER_AGENT_PRODUCT = "camunda-orchestration-sdk-python"
_DISTRIBUTION_NAME = "camunda-orchestration-sdk"
_HTTPX_DEFAULT_PREFIX = "python-httpx/"


@lru_cache(maxsize=1)
def sdk_version() -> str:
    """Return the installed SDK distribution version (``unknown`` if not installed)."""

    try:
        return version(_DISTRIBUTION_NAME)
    except PackageNotFoundError:
        return "unknown"


def sdk_user_agent() -> str:
    """Return the SDK product token, e.g. ``camunda-orchestration-sdk-python/11.0.0``."""

    return f"{SDK_USER_AGENT_PRODUCT}/{sdk_version()}"


def build_user_agent(application_user_agent: str | None = None) -> str:
    """Return the full ``User-Agent`` value: SDK token, then the application's, if any."""

    base = sdk_user_agent()
    extra = (application_user_agent or "").strip()
    return f"{base} {extra}" if extra else base


def _is_httpx_default(value: str) -> bool:
    """True only for httpx's bare default (``python-httpx/<version>``), nothing appended."""

    return value.startswith(_HTTPX_DEFAULT_PREFIX) and " " not in value


def _apply_user_agent(request: httpx.Request, user_agent: str) -> None:
    current = request.headers.get("User-Agent", "").strip()
    if not current or _is_httpx_default(current):
        request.headers["User-Agent"] = user_agent
    elif current == user_agent or current.startswith(user_agent + " "):
        # Already carries this client's full composed value (e.g. a retry).
        return
    else:
        # Caller-supplied header: keep it, but after the SDK token.
        request.headers["User-Agent"] = f"{user_agent} {current}"


def inject_user_agent_hook(
    httpx_args: HttpxArgs | None,
    *,
    application_user_agent: str | None = None,
    async_client: bool = False,
) -> HttpxArgs:
    """Return a copy of ``httpx_args`` with a request hook that sets ``User-Agent``."""

    return append_request_hook(
        httpx_args, _make_hook(build_user_agent(application_user_agent), async_client)
    )


def ensure_user_agent_hook(httpx_args: HttpxArgs | None) -> HttpxArgs:
    """Add the default ``User-Agent`` hook unless one is already installed.

    Used by the generated low-level clients so that direct use attributes
    traffic, while ``attrs.evolve`` (``with_headers`` etc.) and the
    ``CamundaClient`` wrapper's own injection do not stack duplicate hooks.
    """

    hooks = (dict(httpx_args or {}).get("event_hooks") or {})
    request_hooks = hooks.get("request") if isinstance(hooks, dict) else None
    if isinstance(request_hooks, (list, tuple)) and any(
        isinstance(getattr(h, "__camunda_user_agent__", None), str)
        for h in request_hooks
    ):
        return dict(httpx_args or {})
    return inject_user_agent_hook(httpx_args)


class _UserAgentHook:
    """httpx request hook that sets the SDK ``User-Agent`` header.

    Carries the composed value as a class attribute so
    ``ensure_user_agent_hook`` can detect an already-installed hook and
    ``asyncify_user_agent_hooks`` can rebuild it for the async factory.
    """

    __camunda_user_agent__: str
    __camunda_user_agent_async__: bool = False

    def __init__(self, user_agent: str) -> None:
        self.__camunda_user_agent__ = user_agent

    def __call__(self, request: httpx.Request) -> None:
        _apply_user_agent(request, self.__camunda_user_agent__)


class _AsyncUserAgentHook:
    """Async variant of ``_UserAgentHook`` for ``httpx.AsyncClient``."""

    __camunda_user_agent__: str
    __camunda_user_agent_async__: bool = True

    def __init__(self, user_agent: str) -> None:
        self.__camunda_user_agent__ = user_agent

    async def __call__(self, request: httpx.Request) -> None:
        _apply_user_agent(request, self.__camunda_user_agent__)


def _make_hook(user_agent: str, async_client: bool) -> RequestHook:
    if async_client:
        return _AsyncUserAgentHook(user_agent)
    return _UserAgentHook(user_agent)


def asyncify_user_agent_hooks(httpx_args: HttpxArgs | None) -> HttpxArgs:
    """Return a copy of ``httpx_args`` with sync ``User-Agent`` hooks made async.

    The generated low-level clients share one ``httpx_args`` dict between their
    sync and async httpx factories, and ``httpx.AsyncClient`` awaits every
    request hook. Each SDK-installed sync hook is swapped for an async hook
    composing the *same* value (so a wrapper's application suffix survives);
    caller hooks and already-async hooks are untouched, order is preserved.
    """

    out: HttpxArgs = dict(httpx_args or {})
    event_hooks = out.get("event_hooks")
    if not isinstance(event_hooks, dict):
        return out
    request_hooks = event_hooks.get("request")
    if not isinstance(request_hooks, (list, tuple)):
        return out
    converted: list[Any] = []
    for h in request_hooks:
        ua = getattr(h, "__camunda_user_agent__", None)
        is_async = getattr(h, "__camunda_user_agent_async__", False)
        if isinstance(ua, str) and not is_async:
            converted.append(_make_hook(ua, True))
        else:
            converted.append(h)
    new_hooks: dict[str, Any] = dict(event_hooks)
    new_hooks["request"] = converted
    out["event_hooks"] = new_hooks
    return out
