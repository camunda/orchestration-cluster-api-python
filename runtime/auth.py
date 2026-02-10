from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import os
from pathlib import Path
import re
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


_SAAS_OAUTH_HOST = "login.cloud.camunda.io"
_SAAS_401_COOLDOWN_S_DEFAULT = 30.0
_TARPIT_FILENAME_SALT = "camunda-oauth-tarpit-filename-salt-v1"


def _is_saas_oauth_url(oauth_url: str) -> bool:
    try:
        return httpx.URL(oauth_url).host == _SAAS_OAUTH_HOST
    except Exception:
        return False


def _safe_filename_component(value: str) -> str:
    # Keep filenames readable and portable.
    value = value.strip()
    if not value:
        return "empty"
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    return value[:120]


def _hash_secret_for_filename(secret: str) -> str:
    # Deterministic, computationally expensive derivation.
    # This is NOT for secure storage; it's only to avoid writing the raw secret
    # into tarpit filenames.
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        secret.encode("utf-8"),
        _TARPIT_FILENAME_SALT.encode("utf-8"),
        100_000,
        dklen=32,
    )
    return derived.hex()[:16]


def _ensure_dir(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        # Best-effort writeability check.
        test_file = path / f".write-test-{os.getpid()}.tmp"
        test_file.write_text("test", encoding="utf-8")
        test_file.unlink(missing_ok=True)
        return True
    except Exception as e:
        _log_warning("OAuth cache dir is not writable; disabling file cache: dir={dir} err={err}", dir=str(path), err=str(e))
        return False


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
    from collections.abc import Callable
    from typing import cast

    get_headers = getattr(provider, "get_headers", None)
    if not callable(get_headers):
        raise TypeError("auth_provider must implement get_headers() -> Mapping[str, str]")

    typed_get_headers = cast(Callable[[], object], get_headers)
    headers = typed_get_headers()
    if not isinstance(headers, Mapping):
        raise TypeError("auth_provider.get_headers() must return a mapping")
    return cast(Mapping[str, str], headers)


async def _resolve_async_auth_headers(provider: object) -> Mapping[str, str]:
    from collections.abc import Awaitable, Callable
    from typing import cast

    aget_headers = getattr(provider, "aget_headers", None)
    if callable(aget_headers):
        typed_aget_headers = cast(Callable[[], Awaitable[object]], aget_headers)
        headers = await typed_aget_headers()
        if not isinstance(headers, Mapping):
            raise TypeError("auth_provider.aget_headers() must return a mapping")
        return cast(Mapping[str, str], headers)

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
        cache_dir: str | None = None,
        disk_cache_disable: bool = False,
        saas_401_cooldown_s: float = _SAAS_401_COOLDOWN_S_DEFAULT,
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
        self._is_saas = _is_saas_oauth_url(oauth_url)
        self._saas_401_cooldown_s = float(saas_401_cooldown_s)
        self._memoized_401: tuple[float, Exception] | None = None

        self._cache_dir = Path(cache_dir).expanduser() if cache_dir else None
        self._use_file_cache = bool(self._cache_dir) and (not disk_cache_disable)
        if self._use_file_cache and self._cache_dir is not None:
            self._use_file_cache = _ensure_dir(self._cache_dir)

    def close(self) -> None:
        """Close the underlying HTTP client used for token requests.

        Call this when the application is shutting down if you created a provider
        instance yourself (or if you want deterministic cleanup in tests).
        """

        try:
            self._client.close()
        except Exception:
            # Best-effort cleanup.
            return

    def __enter__(self) -> "OAuthClientCredentialsAuthProvider":
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.close()

    def _token_cache_file(self) -> Path | None:
        if not self._use_file_cache or self._cache_dir is None:
            return None
        try:
            host = httpx.URL(self._oauth_url).host or "unknown"
        except Exception:
            host = "unknown"
        filename = "oauth-token-{client_id}-{audience}-{host}.json".format(
            client_id=_safe_filename_component(self._client_id),
            audience=_safe_filename_component(self._audience),
            host=_safe_filename_component(host),
        )
        return self._cache_dir / filename

    def _tarpit_file(self) -> Path | None:
        if not (self._use_file_cache and self._cache_dir and self._is_saas):
            return None
        filename = "oauth-401-tarpit-{client_id}-{audience}-{secret_hash}.json".format(
            client_id=_safe_filename_component(self._client_id),
            audience=_safe_filename_component(self._audience),
            secret_hash=_hash_secret_for_filename(self._client_secret),
        )
        return self._cache_dir / filename

    def _now(self) -> float:
        return time.time()

    def _is_valid(self, token: _OAuthToken) -> bool:
        return self._now() < token.expires_at_epoch_s

    def _try_load_file_cached_token(self) -> _OAuthToken | None:
        token_file = self._token_cache_file()
        if token_file is None:
            return None
        try:
            if not token_file.exists():
                return None
            payload = json.loads(token_file.read_text(encoding="utf-8"))
            access_token = payload.get("access_token")
            expires_at = payload.get("expires_at_epoch_s")
            if not access_token or expires_at is None:
                return None
            token = _OAuthToken(access_token=str(access_token), expires_at_epoch_s=float(expires_at))
            if not self._is_valid(token):
                try:
                    token_file.unlink(missing_ok=True)
                except Exception:
                    pass
                return None
            return token
        except Exception:
            return None

    def _try_save_file_cached_token(self, token: _OAuthToken) -> None:
        token_file = self._token_cache_file()
        if token_file is None:
            return
        try:
            token_file.write_text(
                json.dumps(
                    {
                        "access_token": token.access_token,
                        "expires_at_epoch_s": token.expires_at_epoch_s,
                        "client_id": self._client_id,
                        "audience": self._audience,
                        "oauth_url": self._oauth_url,
                    },
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            try:
                os.chmod(token_file, 0o600)
            except Exception:
                pass
        except Exception:
            # Best-effort only.
            return

    def _is_tarpitted(self) -> bool:
        tarpit = self._tarpit_file()
        return bool(tarpit and tarpit.exists())

    def _create_tarpit_file(self, *, reason: str) -> None:
        tarpit = self._tarpit_file()
        if tarpit is None:
            return
        if tarpit.exists():
            return
        try:
            tarpit.write_text(
                json.dumps(
                    {
                        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "clientId": self._client_id,
                        "audience": self._audience,
                        "reason": reason,
                        "message": "Persistent 401 tarpit – clear manually to retry",
                    },
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            try:
                os.chmod(tarpit, 0o600)
            except Exception:
                # Best-effort permission hardening; ignore chmod failures (e.g. on non-POSIX
                # filesystems or when permissions cannot be changed). The tarpit file
                # still serves its purpose even without strict mode.
                pass
        except Exception:
            return

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
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                # SaaS token endpoint has a 30s cooldown on repeated invalid credentials.
                # Memoize the error to avoid repeatedly hitting the endpoint.
                self._memoized_401 = (self._now(), e)
                if self._is_saas:
                    self._create_tarpit_file(reason=str(e))
            raise
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
            # Persistent SaaS tarpit check (if enabled).
            if self._is_tarpitted():
                raise RuntimeError(
                    "OAuth token requests are tarpitted due to a previous 401 Unauthorized for this client_id/audience/secret. "
                    "Delete the tarpit file in the configured cache_dir (or rotate credentials) to retry."
                )

            # In-memory SaaS 401 cooldown memoization.
            if self._memoized_401 is not None:
                ts, err = self._memoized_401
                if (self._now() - ts) < self._saas_401_cooldown_s:
                    raise err
                self._memoized_401 = None

            if self._token is None or not self._is_valid(self._token):
                # Try file cache first (if enabled).
                cached = self._try_load_file_cached_token()
                if cached is not None:
                    self._token = cached
                else:
                    self._token = self._fetch_token()
                    self._try_save_file_cached_token(self._token)
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
        cache_dir: str | None = None,
        disk_cache_disable: bool = False,
        saas_401_cooldown_s: float = _SAAS_401_COOLDOWN_S_DEFAULT,
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
        self._is_saas = _is_saas_oauth_url(oauth_url)
        self._saas_401_cooldown_s = float(saas_401_cooldown_s)
        self._memoized_401: tuple[float, Exception] | None = None

        self._cache_dir = Path(cache_dir).expanduser() if cache_dir else None
        self._use_file_cache = bool(self._cache_dir) and (not disk_cache_disable)
        if self._use_file_cache and self._cache_dir is not None:
            self._use_file_cache = _ensure_dir(self._cache_dir)

    async def aclose(self) -> None:
        """Close the underlying async HTTP client used for token requests."""

        try:
            await self._client.aclose()
        except Exception:
            # Best-effort cleanup.
            return

    async def __aenter__(self) -> "AsyncOAuthClientCredentialsAuthProvider":
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        await self.aclose()

    def _token_cache_file(self) -> Path | None:
        if not self._use_file_cache or self._cache_dir is None:
            return None
        host = "unknown"
        try:
            host = httpx.URL(self._oauth_url).host or "unknown"
        except Exception:
            host = "unknown"
        filename = "oauth-token-{client_id}-{audience}-{host}.json".format(
            client_id=_safe_filename_component(self._client_id),
            audience=_safe_filename_component(self._audience),
            host=_safe_filename_component(host),
        )
        return self._cache_dir / filename

    def _tarpit_file(self) -> Path | None:
        if not (self._use_file_cache and self._cache_dir and self._is_saas):
            return None
        filename = "oauth-401-tarpit-{client_id}-{audience}-{secret_hash}.json".format(
            client_id=_safe_filename_component(self._client_id),
            audience=_safe_filename_component(self._audience),
            secret_hash=_hash_secret_for_filename(self._client_secret),
        )
        return self._cache_dir / filename

    def _now(self) -> float:
        return time.time()

    def _is_valid(self, token: _OAuthToken) -> bool:
        return self._now() < token.expires_at_epoch_s

    def _try_load_file_cached_token(self) -> _OAuthToken | None:
        token_file = self._token_cache_file()
        if token_file is None:
            return None
        try:
            if not token_file.exists():
                return None
            payload = json.loads(token_file.read_text(encoding="utf-8"))
            access_token = payload.get("access_token")
            expires_at = payload.get("expires_at_epoch_s")
            if not access_token or expires_at is None:
                return None
            token = _OAuthToken(access_token=str(access_token), expires_at_epoch_s=float(expires_at))
            if not self._is_valid(token):
                try:
                    token_file.unlink(missing_ok=True)
                except Exception:
                    pass
                return None
            return token
        except Exception:
            return None

    def _try_save_file_cached_token(self, token: _OAuthToken) -> None:
        token_file = self._token_cache_file()
        if token_file is None:
            return
        try:
            token_file.write_text(
                json.dumps(
                    {
                        "access_token": token.access_token,
                        "expires_at_epoch_s": token.expires_at_epoch_s,
                        "client_id": self._client_id,
                        "audience": self._audience,
                        "oauth_url": self._oauth_url,
                    },
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            try:
                os.chmod(token_file, 0o600)
            except Exception:
                pass
        except Exception:
            return

    def _is_tarpitted(self) -> bool:
        tarpit = self._tarpit_file()
        return bool(tarpit and tarpit.exists())

    def _create_tarpit_file(self, *, reason: str) -> None:
        tarpit = self._tarpit_file()
        if tarpit is None:
            return
        if tarpit.exists():
            return
        try:
            tarpit.write_text(
                json.dumps(
                    {
                        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "clientId": self._client_id,
                        "audience": self._audience,
                        "reason": reason,
                        "message": "Persistent 401 tarpit – clear manually to retry",
                    },
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            try:
                os.chmod(tarpit, 0o600)
            except Exception:
                pass
        except Exception:
            return

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
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                self._memoized_401 = (self._now(), e)
                if self._is_saas:
                    self._create_tarpit_file(reason=str(e))
            raise
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
            if self._is_tarpitted():
                raise RuntimeError(
                    "OAuth token requests are tarpitted due to a previous 401 Unauthorized for this client_id/audience/secret. "
                    "Delete the tarpit file in the configured cache_dir (or rotate credentials) to retry."
                )

            if self._memoized_401 is not None:
                ts, err = self._memoized_401
                if (self._now() - ts) < self._saas_401_cooldown_s:
                    raise err
                self._memoized_401 = None

            if self._token is None or not self._is_valid(self._token):
                cached = self._try_load_file_cached_token()
                if cached is not None:
                    self._token = cached
                else:
                    self._token = await self._fetch_token()
                    self._try_save_file_cached_token(self._token)
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

    request_hook: Any
    response_hook: Any

    if async_client:

        async def _request_hook_async(request: httpx.Request) -> None:
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

        async def _response_hook_async(response: httpx.Response) -> None:
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

        request_hook = _request_hook_async
        response_hook = _response_hook_async

    else:

        def _request_hook_sync(request: httpx.Request) -> None:
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

        def _response_hook_sync(response: httpx.Response) -> None:
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

        request_hook = _request_hook_sync
        response_hook = _response_hook_sync

    out: dict[str, Any] = dict(httpx_args or {})

    # Normalize event_hooks to a writable dict.
    existing_event_hooks = out.get("event_hooks")
    event_hooks: dict[str, Any]
    if existing_event_hooks is None:
        event_hooks = {}
    elif isinstance(existing_event_hooks, dict):
        event_hooks = dict(existing_event_hooks)  # type: ignore[arg-type]
    else:
        raise TypeError("httpx_args['event_hooks'] must be a dict")

    # Normalize request hooks to a list.
    existing_request_hooks = event_hooks.get("request")
    if existing_request_hooks is None:
        request_hooks: list[Any] = []
    elif isinstance(existing_request_hooks, list):
        request_hooks = list(existing_request_hooks)  # type: ignore[arg-type]
    elif isinstance(existing_request_hooks, tuple):
        request_hooks = list(existing_request_hooks)  # type: ignore[arg-type]
    else:
        raise TypeError("httpx_args['event_hooks']['request'] must be a list or tuple")

    request_hooks.append(request_hook)
    event_hooks["request"] = request_hooks

    # Normalize response hooks to a list.
    existing_response_hooks = event_hooks.get("response")
    if existing_response_hooks is None:
        response_hooks: list[Any] = []
    elif isinstance(existing_response_hooks, list):
        response_hooks = list(existing_response_hooks)  # type: ignore[arg-type]
    elif isinstance(existing_response_hooks, tuple):
        response_hooks = list(existing_response_hooks)  # type: ignore[arg-type]
    else:
        raise TypeError("httpx_args['event_hooks']['response'] must be a list or tuple")

    response_hooks.append(response_hook)
    event_hooks["response"] = response_hooks
    out["event_hooks"] = event_hooks

    return out
