"""The seeded randomness seam (camunda/sdk-infra#50).

Pinning the clock makes SDK cadence virtual; injecting a seeded random source as well makes
it reproducible. The generator must produce the cross-SDK SplitMix64 sequence exactly, or
the same seed would mean different jitter in each SDK.
"""

from __future__ import annotations

import asyncio
import threading
from typing import Any

import pytest

from camunda_orchestration_sdk.runtime.clock import ManualClock
from camunda_orchestration_sdk.runtime.configuration_resolver import CamundaSdkConfigPartial
from camunda_orchestration_sdk.runtime.job_worker import WorkerConfig
from camunda_orchestration_sdk.runtime.random_source import (
    SEED_ENV_VAR,
    LiveRandom,
    SeededRandom,
    live_random,
)

#: Seed 42's first draws, pinned by the cross-SDK contract.
SEED_42 = [
    0.7415648787718233,
    0.1599103928769201,
    0.27860113025513866,
    0.34419071652363753,
    0.03803016854024621,
]


class TestSeededRandom:
    def test_matches_the_published_splitmix64_reference(self) -> None:
        # SplitMix64 with seed 0 emits 0xE220A8397B1DCDAF first (Vigna's reference).
        assert SeededRandom(0).next() == (0xE220A8397B1DCDAF >> 11) * 2.0**-53

    def test_matches_the_cross_sdk_conformance_vector(self) -> None:
        random = SeededRandom(42)
        assert [random.next() for _ in SEED_42] == SEED_42

    def test_accepts_the_full_unsigned_64_bit_range(self) -> None:
        assert SeededRandom(2**64 - 1).seed == 2**64 - 1

    @pytest.mark.parametrize("seed", [-1, 2**64])
    def test_rejects_an_out_of_range_seed(self, seed: int) -> None:
        with pytest.raises(ValueError, match="unsigned 64-bit"):
            SeededRandom(seed)

    def test_the_same_seed_replays_the_same_sequence(self) -> None:
        random = SeededRandom.from_env()
        replay = SeededRandom(random.seed)
        for i in range(1_000):
            assert random.next() == replay.next(), f"draw {i} diverged ({random!r})"

    def test_draws_stay_in_the_unit_interval(self) -> None:
        random = SeededRandom.from_env()
        for i in range(100_000):
            u = random.next()
            assert 0.0 <= u < 1.0, f"draw {i} = {u} is outside [0, 1) ({random!r})"

    def test_concurrent_draws_consume_the_sequence_exactly_once(self) -> None:
        """A lost or repeated state step would change the multiset of values drawn."""
        random = SeededRandom.from_env()
        threads, per_thread = 8, 5_000
        drawn: list[float] = []
        lock = threading.Lock()

        def draw() -> None:
            values = [random.next() for _ in range(per_thread)]
            with lock:
                drawn.extend(values)

        workers = [threading.Thread(target=draw) for _ in range(threads)]
        for w in workers:
            w.start()
        for w in workers:
            w.join()

        replay = SeededRandom(random.seed)
        expected = sorted(replay.next() for _ in range(threads * per_thread))
        assert sorted(drawn) == expected, f"concurrent draws diverged ({random!r})"

    def test_names_the_seed_and_how_to_replay_it(self) -> None:
        assert repr(SeededRandom(12345)) == (
            "SeededRandom(seed=12345; replay with CAMUNDA_TEST_SEED=12345)"
        )


class TestFromEnv:
    def test_replays_the_seed_from_the_environment(self) -> None:
        random = SeededRandom.from_env({SEED_ENV_VAR: "42"})
        assert random.seed == 42
        assert random.next() == SEED_42[0]

    def test_draws_a_fresh_seed_only_when_the_variable_is_unset(self) -> None:
        assert 0 <= SeededRandom.from_env({}).seed < 2**53

    @pytest.mark.parametrize(
        "raw", ["", " ", " 42", "42\n", "-1", "0x2A", "abc", "١٢", str(2**64)]
    )
    def test_rejects_a_malformed_seed_rather_than_silently_picking_another(
        self, raw: str
    ) -> None:
        with pytest.raises(ValueError, match=SEED_ENV_VAR):
            SeededRandom.from_env({SEED_ENV_VAR: raw})


def _config() -> CamundaSdkConfigPartial:
    return {
        "CAMUNDA_REST_ADDRESS": "http://example:8080/v2",
        "CAMUNDA_AUTH_STRATEGY": "NONE",
    }


class TestClientInjection:
    def test_live_random_is_the_live_implementation(self) -> None:
        assert isinstance(live_random, LiveRandom)

    def test_sync_client_defaults_to_the_live_source(self) -> None:
        from camunda_orchestration_sdk import CamundaClient

        assert CamundaClient(configuration=_config()).random is live_random

    def test_async_client_defaults_to_the_live_source(self) -> None:
        from camunda_orchestration_sdk import CamundaAsyncClient

        assert CamundaAsyncClient(configuration=_config()).random is live_random

    def test_sync_client_exposes_the_injected_source(self) -> None:
        from camunda_orchestration_sdk import CamundaClient

        injected = SeededRandom(1)
        assert CamundaClient(configuration=_config(), random=injected).random is injected

    def test_async_client_exposes_the_injected_source(self) -> None:
        from camunda_orchestration_sdk import CamundaAsyncClient

        injected = SeededRandom(1)
        assert CamundaAsyncClient(configuration=_config(), random=injected).random is injected

    def test_the_thread_strategy_sync_client_inherits_the_worker_clock_and_source(
        self,
    ) -> None:
        """Thread-strategy handlers get a lazily built sync client. Built from configuration
        alone it fell back to the live clock and source, so handler-side cadence escaped
        both injections."""
        from camunda_orchestration_sdk import CamundaAsyncClient

        clock, random = ManualClock(), SeededRandom(1)
        client = CamundaAsyncClient(configuration=_config(), clock=clock, random=random)
        worker = client.create_job_worker(
            WorkerConfig(job_type="sync", job_timeout_milliseconds=1_000),
            lambda job: None,
            auto_start=False,
        )

        sync_client = worker._get_sync_client()

        assert sync_client.clock is clock
        assert sync_client.random is random


async def _wait_for_sleeps(clock: ManualClock, count: int) -> None:
    for _ in range(1_000):
        if len(clock.sleeps) >= count:
            return
        await asyncio.sleep(0)
    raise AssertionError(f"expected {count} sleeps, saw {clock.sleeps}")


class TestWorkerStartupJitter:
    @pytest.mark.asyncio
    async def test_draws_from_the_client_source(self) -> None:
        """Seed 42 draws 0.7415... of a 10s maximum."""
        from camunda_orchestration_sdk import CamundaAsyncClient

        clock = ManualClock(auto_advance=False)
        client = CamundaAsyncClient(configuration=_config(), clock=clock, random=SeededRandom(42))
        worker = client.create_job_worker(
            WorkerConfig(job_type="jitter", job_timeout_milliseconds=1_000),
            _noop,
            auto_start=False,
            startup_jitter_max_seconds=10,
        )
        try:
            worker.start()
            await _wait_for_sleeps(clock, 1)
            assert clock.sleeps == (pytest.approx(7.415648787718233),)
        finally:
            worker.stop()

    @pytest.mark.asyncio
    async def test_draws_in_start_order(self) -> None:
        """The two workers have different maxima, so the pair of delays identifies which draw
        each received: start order gives {1.599..., 74.156...}; the reverse would give
        {7.415..., 15.991...}."""
        from camunda_orchestration_sdk import CamundaAsyncClient

        clock = ManualClock(auto_advance=False)
        client = CamundaAsyncClient(configuration=_config(), clock=clock, random=SeededRandom(42))

        def create(job_type: str, maximum: float) -> Any:
            return client.create_job_worker(
                WorkerConfig(job_type=job_type, job_timeout_milliseconds=1_000),
                _noop,
                auto_start=False,
                startup_jitter_max_seconds=maximum,
            )

        short, long = create("short", 10), create("long", 100)
        try:
            long.start()
            short.start()
            await _wait_for_sleeps(clock, 2)
            assert sorted(clock.sleeps) == [
                pytest.approx(1.599103928769201),
                pytest.approx(74.15648787718233),
            ]
        finally:
            long.stop()
            short.stop()


async def _noop(job: Any) -> None:
    return None
