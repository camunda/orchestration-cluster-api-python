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
import httpx

from .cluster_admin_url import HttpxArgs, append_request_hook

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

    user_agent = build_user_agent(application_user_agent)

    if async_client:

        async def _request_hook_async(request: httpx.Request) -> None:
            _apply_user_agent(request, user_agent)

        return append_request_hook(httpx_args, _request_hook_async)

    def _request_hook_sync(request: httpx.Request) -> None:
        _apply_user_agent(request, user_agent)

    return append_request_hook(httpx_args, _request_hook_sync)
