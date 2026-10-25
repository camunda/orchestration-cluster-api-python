"""Regression tests for issue #324: cluster-admin operations are served at the bare
root (``/cluster/v2/...``), honouring their operation-level ``servers`` override,
instead of being double-prefixed to ``/v2/cluster/v2/...``.

The cluster-wide operations declare an operation-level ``servers`` entry without the
document ``/v2`` base, so the correct request is ``GET /cluster/v2/topology`` — not
``GET /v2/cluster/v2/topology``. ``openapi-python-client`` does not model per-operation
servers, so the SDK installs an httpx request hook (``inject_cluster_admin_url_hook``)
that drops the ``/v2`` the base URL would otherwise prepend.

These tests target the *class* of defect — every generated operation whose path starts
with ``/cluster/v2/`` — rather than a single instance, so a future operation added under
that prefix is covered automatically.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import httpx
import pytest

import camunda_orchestration_sdk
from camunda_orchestration_sdk import CamundaAsyncClient, CamundaClient, errors
from camunda_orchestration_sdk.runtime.cluster_admin_url import (
    inject_cluster_admin_url_hook,
    rewrite_cluster_admin_url,
)

_BASE_URL = "http://host:8080/v2"
_CLUSTER_ADMIN_PREFIX = "/cluster/v2/"


def _api_package_dir() -> Path:
    return Path(camunda_orchestration_sdk.__file__).parent / "api"


def _url_template(value: ast.expr) -> str | None:
    """Return the ``url`` template string for a ``_get_kwargs`` dict value.

    Static paths are plain ``ast.Constant`` strings. Paths with path parameters are
    emitted as ``"/cluster/v2/backups/runtime/{backup_id}".format(...)`` — a method call
    whose receiver is the template string constant. Both forms are recognised; the
    ``{placeholder}`` tokens are left intact for the caller to concretise.
    """
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return value.value
    if (
        isinstance(value, ast.Call)
        and isinstance(value.func, ast.Attribute)
        and value.func.attr == "format"
        and isinstance(value.func.value, ast.Constant)
        and isinstance(value.func.value.value, str)
    ):
        return value.func.value.value
    return None


def _operation_urls() -> list[str]:
    """Extract the ``url`` template from every generated ``_get_kwargs`` in the api package."""
    urls: list[str] = []
    api_dir = _api_package_dir()
    for path in sorted(api_dir.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.FunctionDef) and node.name == "_get_kwargs"):
                continue
            for sub in ast.walk(node):
                if not isinstance(sub, ast.Dict):
                    continue
                for key, value in zip(sub.keys, sub.values, strict=False):
                    if (
                        isinstance(key, ast.Constant)
                        and key.value == "url"
                        and value is not None
                    ):
                        template = _url_template(value)
                        if template is not None:
                            urls.append(template)
    return urls


def _concretise(url_template: str) -> str:
    """Replace ``{placeholder}`` path tokens with a dummy value for request building."""
    return re.sub(r"\{[^}]+\}", "x", url_template)


def _cluster_admin_urls() -> list[str]:
    return [u for u in _operation_urls() if u.startswith(_CLUSTER_ADMIN_PREFIX)]


def _client_with_hook(
    base_url: str = _BASE_URL,
) -> tuple[httpx.Client, list[httpx.URL]]:
    """Build an httpx client wired exactly like CamundaClient does for cluster-admin URLs."""
    httpx_args = inject_cluster_admin_url_hook({}, base_url=base_url, async_client=False)
    captured: list[httpx.URL] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request.url)
        return httpx.Response(200, json={})

    httpx_args["transport"] = httpx.MockTransport(handler)
    client = httpx.Client(base_url=base_url, **httpx_args)
    return client, captured


# ---------------------------------------------------------------------------
# The generated SDK must expose cluster-admin operations under /cluster/v2/.
# ---------------------------------------------------------------------------


def test_cluster_admin_operations_are_discovered():
    """Guard the discovery itself: the 22 known cluster-admin operations must exist.

    If generation ever drops the /cluster/v2 prefix (e.g. regressing to bare keys),
    this catches it before the URL assertions silently pass on an empty set.
    """
    cluster_urls = _cluster_admin_urls()
    assert len(cluster_urls) >= 22, (
        f"expected at least 22 /cluster/v2/* operations, found {len(cluster_urls)}: "
        f"{sorted(set(cluster_urls))}"
    )


# ---------------------------------------------------------------------------
# Class-scoped: EVERY /cluster/v2/* operation lands at the bare root, and every
# ordinary operation keeps the /v2 base.
# ---------------------------------------------------------------------------


def test_every_cluster_admin_url_is_served_at_bare_root():
    """No /cluster/v2/* operation may be double-prefixed to /v2/cluster/v2/*."""
    client, captured = _client_with_hook()
    for template in _cluster_admin_urls():
        url = _concretise(template)
        client.get(url)
        actual = captured[-1].raw_path.decode("ascii")
        assert actual == url, (
            f"cluster-admin op {template!r} resolved to {actual!r}; "
            f"expected the bare-root path {url!r}"
        )
        assert "/v2/cluster/v2/" not in actual


def test_ordinary_operations_keep_the_v2_base():
    """The hook must not disturb ordinary operations, which stay under /v2."""
    client, captured = _client_with_hook()
    ordinary = [u for u in _operation_urls() if not u.startswith(_CLUSTER_ADMIN_PREFIX)]
    assert ordinary, "expected at least one ordinary (non cluster-admin) operation"
    for template in ordinary:
        url = _concretise(template)
        client.get(url)
        actual = captured[-1].raw_path.decode("ascii")
        assert actual == "/v2" + url, (
            f"ordinary op {template!r} resolved to {actual!r}; expected {'/v2' + url!r}"
        )


def test_gateway_prefix_containing_doubled_segment_is_not_eaten():
    """Regression: a gateway prefix that itself contains /v2/cluster/v2/ is preserved.

    With CAMUNDA_REST_ADDRESS_EXACT=true and base https://host/v2/cluster/v2/proxy,
    an ordinary get_topology() must stay at /v2/cluster/v2/proxy/topology, and a
    cluster-admin call under the same prefix is left alone too: the configured base
    does not end with the document /v2 suffix, so there is no doubling to undo.
    """
    gateway_base = "http://host:8080/v2/cluster/v2/proxy"
    client, captured = _client_with_hook(base_url=gateway_base)

    client.get("/topology")
    assert captured[-1].raw_path.decode("ascii") == "/v2/cluster/v2/proxy/topology"

    client.get("/cluster/v2/topology")
    assert (
        captured[-1].raw_path.decode("ascii") == "/v2/cluster/v2/proxy/cluster/v2/topology"
    )


# ---------------------------------------------------------------------------
# Unit: the rewrite is surgical and prefix-preserving.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw_path", "base_path", "expected"),
    [
        ("/v2/cluster/v2/topology", "/v2", "/cluster/v2/topology"),
        ("/v2/cluster/v2/backups/runtime/42", "/v2", "/cluster/v2/backups/runtime/42"),
        # Gateway cluster-id prefix is preserved; only the base's trailing /v2 is dropped.
        ("/clusterA/v2/cluster/v2/mode", "/clusterA/v2", "/clusterA/cluster/v2/mode"),
        # No /v2 base (CAMUNDA_REST_ADDRESS_EXACT) → nothing to drop.
        ("/cluster/v2/topology", "", "/cluster/v2/topology"),
        # Ordinary paths are untouched.
        ("/v2/deployments", "/v2", "/v2/deployments"),
        # Regression for the review finding: a gateway prefix that itself contains
        # /v2/cluster/v2/ must not be eaten by the rewrite. With
        # CAMUNDA_REST_ADDRESS_EXACT=true and base https://host/v2/cluster/v2/proxy,
        # ordinary get_topology() resolves to /v2/cluster/v2/proxy/topology and must
        # stay exactly there — only the configured base path may ever be stripped.
        (
            "/v2/cluster/v2/proxy/topology",
            "/v2/cluster/v2/proxy",
            "/v2/cluster/v2/proxy/topology",
        ),
        # A base without the document /v2 suffix never doubles, so nothing is dropped
        # even when a cluster-admin path follows it.
        (
            "/v2/cluster/v2/proxy/cluster/v2/topology",
            "/v2/cluster/v2/proxy",
            "/v2/cluster/v2/proxy/cluster/v2/topology",
        ),
        # A path that merely contains /v2/cluster/v2/ beyond the configured base's
        # trailing /v2 segment is a gateway prefix, not a doubling: only the suffix
        # is stripped, the gateway prefix is preserved.
        ("/v2/cluster/v2/proxy/topology", "/v2", "/cluster/v2/proxy/topology"),
        # A trailing slash on the configured base address must not disable the rewrite.
        ("/v2/cluster/v2/topology", "/v2/", "/cluster/v2/topology"),
    ],
)
def test_rewrite_cluster_admin_url(raw_path: str, base_path: str, expected: str):
    url = httpx.URL("http://host:8080").copy_with(raw_path=raw_path.encode("ascii"))
    assert rewrite_cluster_admin_url(url, base_path).raw_path.decode("ascii") == expected


# ---------------------------------------------------------------------------
# End-to-end: the flattened CamundaClient actually installs the hook.
# ---------------------------------------------------------------------------


def _capture_client(sync: bool, captured: list[httpx.URL]):
    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request.url)
        return httpx.Response(
            500,
            json={
                "type": "about:blank",
                "title": "boom",
                "status": 500,
                "detail": "boom",
                "instance": "/cluster/v2/topology",
            },
        )

    transport = httpx.MockTransport(handler)
    cls = CamundaClient if sync else CamundaAsyncClient
    return cls(httpx_args={"transport": transport})


def test_camunda_client_sends_cluster_topology_to_bare_root():
    captured: list[httpx.URL] = []
    client = _capture_client(sync=True, captured=captured)
    # A documented 500 response proves the request reached the transport at the
    # bare root and the facade parsed it; the captured URL is the real assertion.
    with pytest.raises(errors.InternalServerErrorError):
        client.get_cluster_topology()  # pyright: ignore[reportAttributeAccessIssue]
    assert captured, "no request was sent"
    assert captured[0].raw_path == b"/cluster/v2/topology"


@pytest.mark.asyncio
async def test_async_camunda_client_sends_cluster_topology_to_bare_root():
    captured: list[httpx.URL] = []
    client = _capture_client(sync=False, captured=captured)
    with pytest.raises(errors.InternalServerErrorError):
        await client.get_cluster_topology()  # pyright: ignore[reportAttributeAccessIssue]
    assert captured, "no request was sent"
    assert captured[0].raw_path == b"/cluster/v2/topology"
