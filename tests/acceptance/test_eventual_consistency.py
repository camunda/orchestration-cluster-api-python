"""Acceptance tests for eventual consistency polling runtime."""

from __future__ import annotations

from typing import Any

import pytest

from camunda_orchestration_sdk.runtime.eventual import (
    ConsistencyOptions,
    EventualConsistencyTimeoutError,
    _default_predicate,  # pyright: ignore[reportPrivateUsage]
    eventual_poll,
    eventual_poll_async,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class FakeHttpError(Exception):
    """Fake HTTP error with a status_code attribute."""

    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}")


class FakeResult:
    """Fake API result with an optional ``items`` attribute."""

    def __init__(self, items: list[Any] | None = None):
        self.items = items


# ---------------------------------------------------------------------------
# _default_predicate
# ---------------------------------------------------------------------------


class TestDefaultPredicate:
    def test_get_accepts_any_non_none(self):
        assert _default_predicate({"id": 1}, is_get=True) is True

    def test_get_rejects_none(self):
        assert _default_predicate(None, is_get=True) is False

    def test_non_get_accepts_non_empty_items_attr(self):
        result = FakeResult(items=[{"id": 1}])
        assert _default_predicate(result, is_get=False) is True

    def test_non_get_rejects_empty_items_attr(self):
        result = FakeResult(items=[])
        assert _default_predicate(result, is_get=False) is False

    def test_non_get_accepts_non_empty_items_dict(self):
        result: dict[str, list[Any]] = {"items": [{"id": 1}]}
        assert _default_predicate(result, is_get=False) is True

    def test_non_get_rejects_empty_items_dict(self):
        result: dict[str, list[Any]] = {"items": []}
        assert _default_predicate(result, is_get=False) is False

    def test_non_get_no_items_accepts_non_none(self):
        assert _default_predicate("something", is_get=False) is True

    def test_non_get_no_items_rejects_none(self):
        assert _default_predicate(None, is_get=False) is False


# ---------------------------------------------------------------------------
# ConsistencyOptions
# ---------------------------------------------------------------------------


class TestConsistencyOptions:
    def test_defaults(self):
        opts = ConsistencyOptions(wait_up_to_ms=5000)
        assert opts.wait_up_to_ms == 5000
        assert opts.poll_interval_ms == 500
        assert opts.predicate is None

    def test_custom_predicate(self):
        def pred(x: Any) -> bool:
            return x == 42

        opts = ConsistencyOptions(wait_up_to_ms=1000, predicate=pred)
        assert opts.predicate is pred


# ---------------------------------------------------------------------------
# EventualConsistencyTimeoutError
# ---------------------------------------------------------------------------


class TestTimeoutError:
    def test_attributes(self):
        err = EventualConsistencyTimeoutError(
            attempts=3,
            elapsed_ms=1500,
            last_status=404,
            operation_id="get_process",
        )
        assert err.attempts == 3
        assert err.elapsed_ms == 1500
        assert err.last_status == 404
        assert err.operation_id == "get_process"
        assert "get_process" in str(err)
        assert "1500ms" in str(err)

    def test_without_operation_id(self):
        err = EventualConsistencyTimeoutError(attempts=1, elapsed_ms=100)
        assert err.operation_id is None
        assert "100ms" in str(err)


# ---------------------------------------------------------------------------
# eventual_poll (sync)
# ---------------------------------------------------------------------------


class TestEventualPoll:
    def test_returns_immediately_when_consistent(self):
        result = eventual_poll(
            "test_op",
            is_get=True,
            invoke=lambda: {"id": 1},
            options=ConsistencyOptions(wait_up_to_ms=5000),
        )
        assert result == {"id": 1}

    def test_skips_polling_when_wait_is_zero(self):
        result = eventual_poll(
            "test_op",
            is_get=True,
            invoke=lambda: None,
            options=ConsistencyOptions(wait_up_to_ms=0),
        )
        assert result is None

    def test_retries_on_404_for_get(self):
        call_count = 0

        def invoke():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise FakeHttpError(404)
            return {"id": 1}

        result = eventual_poll(
            "test_op",
            is_get=True,
            invoke=invoke,
            options=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
        )
        assert result == {"id": 1}
        assert call_count == 3

    def test_aborts_on_404_for_non_get(self):
        def invoke():
            raise FakeHttpError(404)

        with pytest.raises(FakeHttpError):
            eventual_poll(
                "test_op",
                is_get=False,
                invoke=invoke,
                options=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
            )

    def test_aborts_on_400(self):
        def invoke():
            raise FakeHttpError(400)

        with pytest.raises(FakeHttpError):
            eventual_poll(
                "test_op",
                is_get=True,
                invoke=invoke,
                options=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
            )

    def test_aborts_on_401(self):
        def invoke():
            raise FakeHttpError(401)

        with pytest.raises(FakeHttpError):
            eventual_poll(
                "test_op",
                is_get=True,
                invoke=invoke,
                options=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
            )

    def test_aborts_on_403(self):
        def invoke():
            raise FakeHttpError(403)

        with pytest.raises(FakeHttpError):
            eventual_poll(
                "test_op",
                is_get=True,
                invoke=invoke,
                options=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
            )

    def test_aborts_on_500(self):
        def invoke():
            raise FakeHttpError(500)

        with pytest.raises(FakeHttpError):
            eventual_poll(
                "test_op",
                is_get=True,
                invoke=invoke,
                options=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
            )

    def test_retries_on_429(self):
        call_count = 0

        def invoke():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise FakeHttpError(429)
            return {"id": 1}

        result = eventual_poll(
            "test_op",
            is_get=True,
            invoke=invoke,
            options=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
        )
        assert result == {"id": 1}
        assert call_count == 3

    def test_timeout_with_unsatisfied_predicate(self):
        def invoke():
            return FakeResult(items=[])

        with pytest.raises(EventualConsistencyTimeoutError) as exc_info:
            eventual_poll(
                "search_things",
                is_get=False,
                invoke=invoke,
                options=ConsistencyOptions(wait_up_to_ms=50, poll_interval_ms=10),
            )
        err = exc_info.value
        assert err.operation_id == "search_things"
        assert err.attempts > 0
        assert err.last_status == 200

    def test_custom_predicate(self):
        call_count = 0

        def invoke():
            nonlocal call_count
            call_count += 1
            return {"count": call_count}

        result = eventual_poll(
            "test_op",
            is_get=True,
            invoke=invoke,
            options=ConsistencyOptions(
                wait_up_to_ms=5000,
                poll_interval_ms=10,
                predicate=lambda r: r["count"] >= 3,
            ),
        )
        assert result == {"count": 3}
        assert call_count == 3


# ---------------------------------------------------------------------------
# eventual_poll_async
# ---------------------------------------------------------------------------


class TestEventualPollAsync:
    @pytest.mark.asyncio
    async def test_returns_immediately_when_consistent(self):
        async def invoke():
            return {"id": 1}

        result = await eventual_poll_async(
            "test_op",
            is_get=True,
            invoke=invoke,
            options=ConsistencyOptions(wait_up_to_ms=5000),
        )
        assert result == {"id": 1}

    @pytest.mark.asyncio
    async def test_skips_polling_when_wait_is_zero(self):
        async def invoke():
            return None

        result = await eventual_poll_async(
            "test_op",
            is_get=True,
            invoke=invoke,
            options=ConsistencyOptions(wait_up_to_ms=0),
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_retries_on_404_for_get(self):
        call_count = 0

        async def invoke():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise FakeHttpError(404)
            return {"id": 1}

        result = await eventual_poll_async(
            "test_op",
            is_get=True,
            invoke=invoke,
            options=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
        )
        assert result == {"id": 1}
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_aborts_on_400(self):
        async def invoke():
            raise FakeHttpError(400)

        with pytest.raises(FakeHttpError):
            await eventual_poll_async(
                "test_op",
                is_get=True,
                invoke=invoke,
                options=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
            )

    @pytest.mark.asyncio
    async def test_timeout_with_404(self):
        async def invoke():
            raise FakeHttpError(404)

        with pytest.raises(EventualConsistencyTimeoutError):
            await eventual_poll_async(
                "test_op",
                is_get=True,
                invoke=invoke,
                options=ConsistencyOptions(wait_up_to_ms=50, poll_interval_ms=10),
            )

    @pytest.mark.asyncio
    async def test_retries_on_429(self):
        call_count = 0

        async def invoke():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise FakeHttpError(429)
            return {"id": 1}

        result = await eventual_poll_async(
            "test_op",
            is_get=True,
            invoke=invoke,
            options=ConsistencyOptions(wait_up_to_ms=5000, poll_interval_ms=10),
        )
        assert result == {"id": 1}
        assert call_count == 3


# ---------------------------------------------------------------------------
# Generated client integration — verify eventual ops annotation
# ---------------------------------------------------------------------------


class TestGeneratedClientHasConsistencyParam:
    """Verify that eventually consistent methods in the generated client
    accept a ``consistency`` parameter, and non-eventual methods do not."""

    def _get_client_source(self) -> str:
        import importlib.resources

        # Read the generated client.py source
        import camunda_orchestration_sdk

        client_path = (
            importlib.resources.files(camunda_orchestration_sdk) / "client.py"
        )
        return client_path.read_text()

    def _get_eventual_methods(self) -> set[str]:
        """Read spec-metadata.json and return the set of eventually consistent
        method names (snake_case)."""
        import json
        import re
        from pathlib import Path

        metadata_path = (
            Path(__file__).parent.parent.parent
            / "external-spec"
            / "bundled"
            / "spec-metadata.json"
        )
        if not metadata_path.exists():
            pytest.skip("spec-metadata.json not found")

        with open(metadata_path) as f:
            metadata = json.load(f)

        def to_snake(name: str) -> str:
            s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
            s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
            return s.lower()

        methods: set[str] = set()
        for op in metadata.get("operations", []):
            if op.get("eventuallyConsistent"):
                methods.add(to_snake(op["operationId"]))
        return methods

    def test_eventual_methods_have_consistency_param(self):
        """Every eventually consistent method must accept a ``consistency``
        parameter."""
        source = self._get_client_source()
        eventual_methods = self._get_eventual_methods()
        if not eventual_methods:
            pytest.skip("No eventually consistent methods found in metadata")

        missing: list[str] = []
        for method in sorted(eventual_methods):
            # Match: def <method>(... consistency: ConsistencyOptions
            # in both sync and async classes
            if f"def {method}(" in source:
                # Find the def line(s) and check for consistency param
                import re

                pattern = rf"def {method}\([^)]*consistency:\s*ConsistencyOptions"
                if not re.search(pattern, source, re.DOTALL):
                    missing.append(method)

        assert not missing, (
            f"Eventually consistent methods missing 'consistency' parameter: {missing}"
        )

    def test_non_eventual_methods_lack_consistency_param(self):
        """Non-eventual methods must NOT have a ``consistency`` parameter."""
        import re

        source = self._get_client_source()
        eventual_methods = self._get_eventual_methods()

        # Find all method definitions with consistency param
        pattern = r"def (\w+)\([^)]*consistency:\s*ConsistencyOptions"
        matches = set(re.findall(pattern, source, re.DOTALL))

        unexpected = matches - eventual_methods
        assert not unexpected, (
            f"Non-eventual methods unexpectedly have 'consistency' parameter: {sorted(unexpected)}"
        )

    def test_consistency_import_in_client(self):
        """Generated client.py must import ConsistencyOptions."""
        source = self._get_client_source()
        assert "ConsistencyOptions" in source, (
            "client.py does not import ConsistencyOptions"
        )

    def test_eventual_poll_import_in_client(self):
        """Generated client.py must import eventual_poll functions."""
        source = self._get_client_source()
        assert "eventual_poll" in source, (
            "client.py does not import eventual_poll"
        )
