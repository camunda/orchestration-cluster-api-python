from __future__ import annotations

import asyncio
import base64
import threading
import time
from dataclasses import dataclass
from typing import Any, Mapping, Protocol, runtime_checkable

import httpx

try:
    from loguru import logger as _logger
except Exception:  # pragma: no cover
    _logger = None  # type: ignore[assignment]


_LOG_LEVEL_ORDER: dict[str, int] = {
    "silent": 0,
    "error": 1,
    "warn": 2,
    "info": 3,
    "debug": 4,
    "trace": 5,
    "silly": 6,
}


def _should_log_http(log_level: str | None) -> bool:
    if not log_level:
        return False
    return _LOG_LEVEL_ORDER.get(str(log_level).lower(), 0) >= _LOG_LEVEL_ORDER["debug"]


def _should_log_http_body(log_level: str | None) -> bool:
    if not log_level:
        return False
    return _LOG_LEVEL_ORDER.get(str(log_level).lower(), 0) >= _LOG_LEVEL_ORDER["trace"]


def _log_debug(message: str, **kwargs: Any) -> None:
    if _logger is None:
        return
    _logger.debug(message, **kwargs)


def _log_warning(message: str, **kwargs: Any) -> None:
    if _logger is None:
        return
    _logger.warning(message, **kwargs)


@runtime_checkable
class AuthProvider(Protocol):
    """Provides per-request authentication headers.

    Implementations are expected to be lightweight and safe to call for every request.
    """

    def get_headers(self) -> Mapping[str, str]:
        ...


@runtime_checkable
class AsyncAuthProvider(Protocol):
    """Async auth provider variant.

    If an auth provider implements this protocol, async clients will prefer it.
    """

    async def aget_headers(self) -> Mapping[str, str]:
        ...


class NullAuthProvider:
    """Default auth provider that adds no headers."""

    def get_headers(self) -> dict[str, str]:
        return {}


def _resolve_auth_headers(provider: object) -> Mapping[str, str]:
    get_headers = getattr(provider, "get_headers", None)
    if not callable(get_headers):
        raise TypeError("auth_provider must implement get_headers() -> Mapping[str, str]")

    headers = get_headers()
    if not isinstance(headers, Mapping):
        raise TypeError("auth_provider.get_headers() must return a mapping")
    return headers


async def _resolve_async_auth_headers(provider: object) -> Mapping[str, str]:
    aget_headers = getattr(provider, "aget_headers", None)
    if callable(aget_headers):
        headers = await aget_headers()
        if not isinstance(headers, Mapping):
            raise TypeError("auth_provider.aget_headers() must return a mapping")
        return headers

    return _resolve_auth_headers(provider)


class BasicAuthProvider:
    """HTTP Basic auth provider."""

    def __init__(self, *, username: str, password: str):
        username = username.strip()
        password = password.strip()
        if not username or not password:
            raise ValueError("Basic auth username and password must be non-empty")
        token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
        self._header_value = f"Basic {token}"

    def get_headers(self) -> Mapping[str, str]:
        return {"Authorization": self._header_value}


@dataclass
class _OAuthToken:
    access_token: str
    expires_at_epoch_s: float


class OAuthClientCredentialsAuthProvider:
    """OAuth 2.0 Client Credentials provider with in-memory caching.

    This is designed for sync clients.
    """

    def __init__(
        self,
        *,
        oauth_url: str,
        client_id: str,
        client_secret: str,
        audience: str,
        transport: httpx.BaseTransport | None = None,
        timeout: float | None = None,
    ):
        self._oauth_url = oauth_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._audience = audience
        self._client = httpx.Client(transport=transport, timeout=timeout)
        self._lock = threading.Lock()
        self._token: _OAuthToken | None = None

    def _now(self) -> float:
        return time.time()

    def _is_valid(self, token: _OAuthToken) -> bool:
        return self._now() < token.expires_at_epoch_s

    def _fetch_token(self) -> _OAuthToken:
        data = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "audience": self._audience,
        }

        if _logger is not None:
            _logger.debug(
                "OAuth token request: url={url} audience={audience} client_id={client_id}",
                url=self._oauth_url,
                audience=self._audience,
                client_id=self._client_id,
            )

        resp = self._client.post(
            self._oauth_url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()
        payload = resp.json()
        access_token = payload.get("access_token")
        expires_in = payload.get("expires_in")
        if not access_token or not expires_in:
            raise ValueError("OAuth token response missing access_token or expires_in")

        lifetime_s = float(expires_in)
        # Match TS behavior: subtract a skew buffer (>=30s or 5% of lifetime)
        skew = max(30.0, lifetime_s * 0.05)
        expires_at = self._now() + max(0.0, lifetime_s - skew)
        return _OAuthToken(access_token=str(access_token), expires_at_epoch_s=expires_at)

    def get_headers(self) -> Mapping[str, str]:
        with self._lock:
            if self._token is None or not self._is_valid(self._token):
                self._token = self._fetch_token()
            return {"Authorization": f"Bearer {self._token.access_token}"}


class AsyncOAuthClientCredentialsAuthProvider:
    """OAuth 2.0 Client Credentials provider with in-memory caching.

    This is designed for async clients.
    """

    def __init__(
        self,
        *,
        oauth_url: str,
        client_id: str,
        client_secret: str,
        audience: str,
        transport: httpx.AsyncBaseTransport | None = None,
        timeout: float | None = None,
    ):
        self._oauth_url = oauth_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._audience = audience
        self._client = httpx.AsyncClient(transport=transport, timeout=timeout)
        self._lock = asyncio.Lock()
        self._token: _OAuthToken | None = None

    def _now(self) -> float:
        return time.time()

    def _is_valid(self, token: _OAuthToken) -> bool:
        return self._now() < token.expires_at_epoch_s

    async def _fetch_token(self) -> _OAuthToken:
        data = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "audience": self._audience,
        }

        if _logger is not None:
            _logger.debug(
                "OAuth token request (async): url={url} audience={audience} client_id={client_id}",
                url=self._oauth_url,
                audience=self._audience,
                client_id=self._client_id,
            )

        resp = await self._client.post(
            self._oauth_url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()
        payload = resp.json()
        access_token = payload.get("access_token")
        expires_in = payload.get("expires_in")
        if not access_token or not expires_in:
            raise ValueError("OAuth token response missing access_token or expires_in")

        lifetime_s = float(expires_in)
        skew = max(30.0, lifetime_s * 0.05)
        expires_at = self._now() + max(0.0, lifetime_s - skew)
        return _OAuthToken(access_token=str(access_token), expires_at_epoch_s=expires_at)

    async def aget_headers(self) -> Mapping[str, str]:
        async with self._lock:
            if self._token is None or not self._is_valid(self._token):
                self._token = await self._fetch_token()
            return {"Authorization": f"Bearer {self._token.access_token}"}


def inject_auth_event_hooks(
    httpx_args: dict[str, Any] | None,
    auth_provider: object,
    *,
    async_client: bool = False,
    log_level: str | None = None,
) -> dict[str, Any]:
    """Return a copy of httpx_args with a request hook that applies auth headers.

    This uses httpx event hooks so we don't have to inject headers in every generated API call.
    """

    log_http = _should_log_http(log_level)
    log_http_body = _should_log_http_body(log_level)

    if async_client:

        async def _request_hook(request: httpx.Request) -> None:
            headers = await _resolve_async_auth_headers(auth_provider)
            if headers:
                request.headers.update(headers)

            if log_http:
                _log_debug(
                    "HTTP request: method={method} url={url} has_auth={has_auth}",
                    method=request.method,
                    url=str(request.url),
                    has_auth=("authorization" in request.headers),
                )

        async def _response_hook(response: httpx.Response) -> None:
            if not log_http:
                return

            request = response.request
            status = response.status_code

            # Keep output safe and compact; only show body at trace.
            if status >= 400:
                if log_http_body:
                    body_preview = (response.text or "").strip().replace("\n", " ")[:500]
                    _log_warning(
                        "HTTP response: status={status} method={method} url={url} body={body}",
                        status=status,
                        method=request.method,
                        url=str(request.url),
                        body=body_preview,
                    )
                else:
                    _log_warning(
                        "HTTP response: status={status} method={method} url={url}",
                        status=status,
                        method=request.method,
                        url=str(request.url),
                    )
            else:
                _log_debug(
                    "HTTP response: status={status} method={method} url={url}",
                    status=status,
                    method=request.method,
                    url=str(request.url),
                )

    else:

        def _request_hook(request: httpx.Request) -> None:
            headers = _resolve_auth_headers(auth_provider)
            if headers:
                request.headers.update(headers)

            if log_http:
                _log_debug(
                    "HTTP request: method={method} url={url} has_auth={has_auth}",
                    method=request.method,
                    url=str(request.url),
                    has_auth=("authorization" in request.headers),
                )

        def _response_hook(response: httpx.Response) -> None:
            if not log_http:
                return

            request = response.request
            status = response.status_code

            # Keep output safe and compact; only show body at trace.
            if status >= 400:
                if log_http_body:
                    body_preview = (response.text or "").strip().replace("\n", " ")[:500]
                    _log_warning(
                        "HTTP response: status={status} method={method} url={url} body={body}",
                        status=status,
                        method=request.method,
                        url=str(request.url),
                        body=body_preview,
                    )
                else:
                    _log_warning(
                        "HTTP response: status={status} method={method} url={url}",
                        status=status,
                        method=request.method,
                        url=str(request.url),
                    )
            else:
                _log_debug(
                    "HTTP response: status={status} method={method} url={url}",
                    status=status,
                    method=request.method,
                    url=str(request.url),
                )

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

    # Normalize response hooks to a list.
    existing_response_hooks = event_hooks.get("response")
    if existing_response_hooks is None:
        response_hooks: list[Any] = []
    elif isinstance(existing_response_hooks, list):
        response_hooks = list(existing_response_hooks)
    elif isinstance(existing_response_hooks, tuple):
        response_hooks = list(existing_response_hooks)
    else:
        raise TypeError("httpx_args['event_hooks']['response'] must be a list or tuple")

    response_hooks.append(_response_hook)
    event_hooks["response"] = response_hooks
    out["event_hooks"] = event_hooks

    return out
