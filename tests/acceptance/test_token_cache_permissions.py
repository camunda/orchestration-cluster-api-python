"""The OAuth token cache must never be readable by other local users.

Regression guard for the write-then-``chmod`` shape: a file created by
``Path.write_text`` exists at the process umask until the ``chmod`` lands, and on
Windows the ``chmod`` never narrows it at all. These tests therefore assert the mode
the *creating* call produces, with ``os.chmod`` neutralised so nothing after the fact
can rescue it, and they sweep every file the cache writes rather than only the token
file -- the tarpit record names the client_id and the token-endpoint error too.
"""

from __future__ import annotations

import json
import os
import stat
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import httpx
import pytest


SAAS_OAUTH_URL = "https://login.cloud.camunda.io/oauth/token"

requires_posix_modes = pytest.mark.skipif(
    os.name != "posix",
    reason=(
        "Asserts POSIX permission bits. A mode argument does not become an access-control "
        "list on Windows; that platform needs its own handling."
    ),
)


@pytest.fixture
def open_umask() -> Iterator[None]:
    """Run with umask 0, so any mode observed came from the SDK, not from the umask."""

    previous = os.umask(0o000)
    try:
        yield
    finally:
        os.umask(previous)


@pytest.fixture
def no_chmod(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Make ``os.chmod`` a no-op, as it effectively is for this purpose on Windows."""

    monkeypatch.setattr(os, "chmod", lambda *args, **kwargs: None)
    yield


def _success_handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        200,
        json={"access_token": "cached-access-token", "expires_in": 3600},
        request=request,
    )


def _unauthorized_handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(401, json={"error": "invalid_client"}, request=request)


def _mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


def _cache_files(cache_dir: Path) -> list[Path]:
    return sorted(p for p in cache_dir.iterdir() if p.is_file())


def _leftover_temp_files(cache_dir: Path) -> list[Path]:
    return [p for p in cache_dir.iterdir() if p.name.endswith(".tmp")]


def _sync_provider(**kwargs: Any) -> Any:
    from camunda_orchestration_sdk.runtime.auth import (
        OAuthClientCredentialsAuthProvider,
    )

    return OAuthClientCredentialsAuthProvider(**kwargs)


def _async_provider(**kwargs: Any) -> Any:
    from camunda_orchestration_sdk.runtime.auth import (
        AsyncOAuthClientCredentialsAuthProvider,
    )

    return AsyncOAuthClientCredentialsAuthProvider(**kwargs)


# --- the cache directory ------------------------------------------------------------


@requires_posix_modes
def test_sync_token_cache_directory_is_created_private(
    tmp_path: Path, open_umask: None, no_chmod: None
) -> None:
    cache_dir = tmp_path / "cache"

    provider = _sync_provider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(cache_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(_success_handler),
    )
    try:
        provider.get_headers()
    finally:
        provider.close()

    assert _mode(cache_dir) == 0o700


@requires_posix_modes
@pytest.mark.asyncio
async def test_async_token_cache_directory_is_created_private(
    tmp_path: Path, open_umask: None, no_chmod: None
) -> None:
    cache_dir = tmp_path / "cache"

    provider = _async_provider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(cache_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(_success_handler),
    )
    try:
        await provider.aget_headers()
    finally:
        await provider.aclose()

    assert _mode(cache_dir) == 0o700


# --- every file the cache writes ----------------------------------------------------


@requires_posix_modes
def test_sync_every_cache_file_is_created_private_without_chmod(
    tmp_path: Path, open_umask: None, no_chmod: None
) -> None:
    """Class-scoped: whatever the cache writes, not just the token file."""

    cache_dir = tmp_path / "cache"

    token_provider = _sync_provider(
        oauth_url=SAAS_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(cache_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(_success_handler),
    )
    try:
        token_provider.get_headers()
    finally:
        token_provider.close()

    tarpit_provider = _sync_provider(
        oauth_url=SAAS_OAUTH_URL,
        # A different client_id, so this provider cannot reuse the token entry the
        # first one cached: the token filename keys on client_id, audience and host.
        client_id="rejected-id",
        client_secret="wrong-secret",
        audience="aud",
        cache_dir=str(cache_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(_unauthorized_handler),
    )
    try:
        with pytest.raises(httpx.HTTPStatusError):
            tarpit_provider.get_headers()
    finally:
        tarpit_provider.close()

    files = _cache_files(cache_dir)
    assert [p.name for p in files if p.name.startswith("oauth-token-")], (
        "expected a token cache file to have been written"
    )
    assert [p.name for p in files if p.name.startswith("oauth-401-tarpit-")], (
        "expected a tarpit file to have been written"
    )
    assert {p.name: _mode(p) for p in files} == {p.name: 0o600 for p in files}


@requires_posix_modes
@pytest.mark.asyncio
async def test_async_every_cache_file_is_created_private_without_chmod(
    tmp_path: Path, open_umask: None, no_chmod: None
) -> None:
    cache_dir = tmp_path / "cache"

    token_provider = _async_provider(
        oauth_url=SAAS_OAUTH_URL,
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(cache_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(_success_handler),
    )
    try:
        await token_provider.aget_headers()
    finally:
        await token_provider.aclose()

    tarpit_provider = _async_provider(
        oauth_url=SAAS_OAUTH_URL,
        # A different client_id, so this provider cannot reuse the token entry the
        # first one cached: the token filename keys on client_id, audience and host.
        client_id="rejected-id",
        client_secret="wrong-secret",
        audience="aud",
        cache_dir=str(cache_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(_unauthorized_handler),
    )
    try:
        with pytest.raises(httpx.HTTPStatusError):
            await tarpit_provider.aget_headers()
    finally:
        await tarpit_provider.aclose()

    files = _cache_files(cache_dir)
    assert [p.name for p in files if p.name.startswith("oauth-token-")], (
        "expected a token cache file to have been written"
    )
    assert [p.name for p in files if p.name.startswith("oauth-401-tarpit-")], (
        "expected a tarpit file to have been written"
    )
    assert {p.name: _mode(p) for p in files} == {p.name: 0o600 for p in files}


# --- atomicity ----------------------------------------------------------------------


def test_sync_cache_write_leaves_no_temporary_file_behind(tmp_path: Path) -> None:
    provider = _sync_provider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(_success_handler),
    )
    try:
        provider.get_headers()
    finally:
        provider.close()

    assert _leftover_temp_files(tmp_path) == []
    token_file = next(tmp_path.glob("oauth-token-*.json"))
    assert json.loads(token_file.read_text(encoding="utf-8"))["access_token"] == (
        "cached-access-token"
    )


def test_sync_a_failed_cache_write_leaves_the_previous_entry_intact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A write that dies part-way must not destroy the entry already on disk.

    Driven through the save method directly: going through ``get_headers`` would first
    take the *load* path, which unlinks an entry it considers expired, so the state
    this test is about could not be set up through the public surface.
    """

    from camunda_orchestration_sdk.runtime.auth import _OAuthToken

    provider = _sync_provider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(_success_handler),
    )
    try:
        provider.get_headers()
        token_file = next(tmp_path.glob("oauth-token-*.json"))
        original = token_file.read_text(encoding="utf-8")

        def _fail(*args: Any, **kwargs: Any) -> None:
            raise OSError("simulated failure before the entry is in place")

        monkeypatch.setattr(os, "replace", _fail)
        provider._try_save_file_cached_token(  # pyright: ignore[reportPrivateUsage]
            _OAuthToken(access_token="replacement-token", expires_at_epoch_s=1.0)
        )
    finally:
        provider.close()

    assert token_file.read_text(encoding="utf-8") == original
    assert _leftover_temp_files(tmp_path) == []


@pytest.mark.asyncio
async def test_async_a_failed_cache_write_leaves_the_previous_entry_intact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from camunda_orchestration_sdk.runtime.auth import _OAuthToken

    provider = _async_provider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        transport=httpx.MockTransport(_success_handler),
    )
    try:
        await provider.aget_headers()
        token_file = next(tmp_path.glob("oauth-token-*.json"))
        original = token_file.read_text(encoding="utf-8")

        def _fail(*args: Any, **kwargs: Any) -> None:
            raise OSError("simulated failure before the entry is in place")

        monkeypatch.setattr(os, "replace", _fail)
        provider._try_save_file_cached_token(  # pyright: ignore[reportPrivateUsage]
            _OAuthToken(access_token="replacement-token", expires_at_epoch_s=1.0)
        )
    finally:
        await provider.aclose()

    assert token_file.read_text(encoding="utf-8") == original
    assert _leftover_temp_files(tmp_path) == []


def test_a_cache_filename_near_the_component_limit_still_persists(
    tmp_path: Path,
) -> None:
    """The temporary name must not embed the destination's, or it outgrows the limit.

    A 249-character destination is valid on its own (the limit is 255 bytes per path
    component). Were the temporary name derived from it, the temporary name would
    exceed the limit, ``ENAMETOOLONG`` would be swallowed by the best-effort callers,
    and token persistence would be silently disabled.
    """

    from camunda_orchestration_sdk.runtime.auth import (
        _write_private_file,  # pyright: ignore[reportPrivateUsage]
    )

    destination = tmp_path / ("a" * 249)

    _write_private_file(destination, "payload")

    assert destination.read_text(encoding="utf-8") == "payload"
    assert _leftover_temp_files(tmp_path) == []


class _RaisingLogger:
    """A user-supplied logger that fails on every call."""

    def debug(self, *args: Any, **kwargs: Any) -> None:
        raise RuntimeError("logger exploded")

    info = warning = error = debug


@pytest.mark.asyncio
async def test_async_a_raising_logger_does_not_fail_a_request_holding_a_valid_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A failed cache write is only a diagnostic; it must not escape the request."""

    from camunda_orchestration_sdk.runtime.auth import _OAuthToken
    from camunda_orchestration_sdk.runtime.logging import SdkLogger

    provider = _async_provider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(tmp_path),
        disk_cache_disable=False,
        logger=SdkLogger(_RaisingLogger()),  # pyright: ignore[reportArgumentType]
        transport=httpx.MockTransport(_success_handler),
    )
    try:

        def _fail(*args: Any, **kwargs: Any) -> None:
            raise OSError("simulated cache write failure")

        monkeypatch.setattr(os, "replace", _fail)
        provider._try_save_file_cached_token(  # pyright: ignore[reportPrivateUsage]
            _OAuthToken(access_token="valid-token", expires_at_epoch_s=1.0)
        )
    finally:
        await provider.aclose()


def test_existing_cache_directory_mode_is_left_alone(tmp_path: Path) -> None:
    """The SDK creates its cache dir private; it does not re-permission the user's."""

    cache_dir = tmp_path / "preexisting"
    cache_dir.mkdir(mode=0o755)
    before = _mode(cache_dir)

    provider = _sync_provider(
        oauth_url="http://auth.local/oauth/token",
        client_id="id",
        client_secret="secret",
        audience="aud",
        cache_dir=str(cache_dir),
        disk_cache_disable=False,
        transport=httpx.MockTransport(_success_handler),
    )
    try:
        provider.get_headers()
    finally:
        provider.close()

    assert _mode(cache_dir) == before
