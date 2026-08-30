"""The job context exposes the worker's clock -- where it safely can.

Slice 3 of the injected-clock contract. Slices 1 and 2 put the SDK's own cadence on the
injected clock; this puts it within reach of handler code, so a handler that waits waits on
engine time too. Without it a handler still has to reach for `asyncio.sleep`, and the
process it is participating in stalls on the real clock the moment the engine is pinned.

The interesting constraint is that this cannot be uniform across the three strategies: the
`process` context crosses a process boundary, and a clock does not survive pickling. That
asymmetry is deliberate and is pinned by the tests below.

See camunda/orchestration-cluster-api-js#450.
"""

from __future__ import annotations

import pickle
import time as real_time
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import attrs
import pytest

from camunda_orchestration_sdk.models.activated_job_result import ActivatedJobResult
from camunda_orchestration_sdk.models.activated_job_result_custom_headers import (
    ActivatedJobResultCustomHeaders,
)
from camunda_orchestration_sdk.models.activated_job_result_variables import (
    ActivatedJobResultVariables,
)
from camunda_orchestration_sdk.models.job_activation_result import JobActivationResult
from camunda_orchestration_sdk.models.job_kind_enum import JobKindEnum
from camunda_orchestration_sdk.models.job_listener_event_type_enum import (
    JobListenerEventTypeEnum,
)
from camunda_orchestration_sdk.runtime.clock import Clock, ManualClock, live_clock
from camunda_orchestration_sdk.runtime.job_worker import (
    ConnectedJobContext,
    JobContext,
    JobWorker,
    SyncJobContext,
    WorkerConfig,
)
from camunda_orchestration_sdk.semantic_types import (
    ElementId,
    ElementInstanceKey,
    JobKey,
    ProcessDefinitionId,
    ProcessDefinitionKey,
    ProcessInstanceKey,
    TenantId,
)

#: Real seconds a virtualised wait is allowed to take. A safety net, not a timing assertion.
REAL_BUDGET_S = 5.0

#: Long enough that doing it for real would be unmistakable in the test run.
VIRTUAL_WAIT_S = 30.0


def _real_job() -> ActivatedJobResult:
    """A genuinely picklable job. A MagicMock would not be, so the pickling guard below
    would pass or fail for reasons that have nothing to do with the context."""
    return ActivatedJobResult(
        job_key=JobKey("99"),
        business_id=None,
        type_="my-job",
        process_instance_key=ProcessInstanceKey("1"),
        process_definition_id=ProcessDefinitionId("proc"),
        process_definition_version=3,
        process_definition_key=ProcessDefinitionKey("2"),
        element_id=ElementId("elem"),
        element_instance_key=ElementInstanceKey("3"),
        custom_headers=ActivatedJobResultCustomHeaders(),
        worker="w1",
        retries=5,
        deadline=9999,
        variables=ActivatedJobResultVariables(),
        tenant_id=TenantId("t1"),
        physical_tenant_id="t1",
        lease_token=None,
        kind=JobKindEnum("BPMN_ELEMENT"),
        listener_event_type=JobListenerEventTypeEnum("UNSPECIFIED"),
        tags=[],
        root_process_instance_key=None,
        user_task=None,
        priority=0,
    )


def _job() -> Any:
    job = MagicMock(spec=ActivatedJobResult)
    job.job_key = 1
    job.type_ = "test-job"
    job.process_instance_key = 1
    job.bpmn_process_id = "p"
    job.process_definition_version = 1
    job.process_definition_key = 2
    job.element_id = "e"
    job.element_instance_key = 3
    job.custom_headers = {}
    job.worker = "w"
    job.retries = 3
    job.deadline = 0
    job.variables = None
    return job


def _client() -> MagicMock:
    client = MagicMock()
    client.complete_job = AsyncMock()
    client.fail_job = AsyncMock()
    client.throw_job_error = AsyncMock()
    client.activate_jobs = AsyncMock(return_value=JobActivationResult(jobs=[]))
    return client


def _config() -> WorkerConfig:
    return WorkerConfig(job_type="test", job_timeout_milliseconds=1000)


class TestContextsCarryTheClock:
    def test_async_context_exposes_it(self) -> None:
        clock = ManualClock(start=1_000.0)
        ctx = ConnectedJobContext.create(_job(), client=_client(), clock=clock)
        assert ctx.clock is clock

    def test_thread_context_exposes_it(self) -> None:
        clock = ManualClock(start=1_000.0)
        ctx = SyncJobContext.create(_job(), client=_client(), clock=clock)
        assert ctx.clock is clock

    def test_it_is_the_worker_s_own_clock(self) -> None:
        """A context carrying some *other* clock would be worse than carrying none."""
        clock = ManualClock(start=1_000.0)
        worker = JobWorker(_client(), lambda job: None, _config(), clock=clock)

        ctx = ConnectedJobContext.create(_job(), client=_client(), clock=worker._clock)  # pyright: ignore[reportPrivateUsage]

        assert ctx.clock is clock


class TestHandlersCanWaitOnEngineTime:
    """The point of the slice: a handler that waits does not burn real time."""

    @pytest.mark.asyncio
    async def test_an_async_handler_sleeps_on_the_injected_clock(self) -> None:
        clock = ManualClock(start=1_000.0)
        ctx = ConnectedJobContext.create(_job(), client=_client(), clock=clock)

        started = real_time.monotonic()
        await ctx.clock.sleep(VIRTUAL_WAIT_S)
        elapsed = real_time.monotonic() - started

        assert clock.now() == 1_000.0 + VIRTUAL_WAIT_S
        assert elapsed < REAL_BUDGET_S, (
            f"a {VIRTUAL_WAIT_S}s handler wait burned {elapsed:.1f}s of real time"
        )

    def test_a_thread_handler_sleeps_on_the_injected_clock(self) -> None:
        clock = ManualClock(start=1_000.0)
        ctx = SyncJobContext.create(_job(), client=_client(), clock=clock)

        started = real_time.monotonic()
        ctx.clock.sleep_sync(VIRTUAL_WAIT_S)
        elapsed = real_time.monotonic() - started

        assert clock.now() == 1_000.0 + VIRTUAL_WAIT_S
        assert elapsed < REAL_BUDGET_S, (
            f"a {VIRTUAL_WAIT_S}s handler wait burned {elapsed:.1f}s of real time"
        )


class TestTheProcessBoundaryIsRespected:
    """`process` handlers get no clock, and that is load-bearing rather than an oversight.

    A clock owns a lock, so adding one to the base context would break the process strategy
    at dispatch -- the failure would land in `run_in_executor`, far from the change that
    caused it.
    """

    def test_the_process_context_has_no_clock(self) -> None:
        ctx = JobContext.from_job(_real_job())
        assert not hasattr(ctx, "clock")

    def test_the_process_context_gains_nothing_but_a_logger(self) -> None:
        """Class-scoped: any live object added here breaks the process strategy, not just a
        clock. Fails on the next such field rather than only on the one foreseen."""
        inherited = {f.name for f in attrs.fields(ActivatedJobResult)}
        added = {f.name for f in attrs.fields(JobContext)} - inherited

        assert added == {"log"}, (
            f"JobContext must stay picklable for the process strategy; it gained {added}"
        )

    def test_the_process_context_is_still_picklable(self) -> None:
        ctx = JobContext.from_job(_real_job())
        assert isinstance(pickle.loads(pickle.dumps(ctx)), JobContext)

    def test_a_clock_is_what_would_have_broken_it(self) -> None:
        """Proves the constraint rather than asserting it: this is why the base has none."""
        for clock in (live_clock, ManualClock()):
            with pytest.raises((TypeError, AttributeError, pickle.PicklingError)):
                pickle.dumps(clock)

    def test_the_in_process_contexts_are_not_expected_to_pickle(self) -> None:
        """They already hold a live client, so the clock costs nothing extra here."""
        ctx = ConnectedJobContext.create(_job(), client=_client(), clock=ManualClock())
        with pytest.raises((TypeError, AttributeError, pickle.PicklingError)):
            pickle.dumps(ctx)


def test_the_clock_satisfies_the_protocol() -> None:
    ctx = ConnectedJobContext.create(_job(), client=_client(), clock=ManualClock())
    assert isinstance(ctx.clock, Clock)
