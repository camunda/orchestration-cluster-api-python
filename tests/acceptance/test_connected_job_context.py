"""Tests for polymorphic job context based on execution strategy.

Verifies that:
- async/thread strategies provide ConnectedJobContext (with client)
- process strategy provides plain JobContext (no client)
- ConnectedJobContext.create() correctly copies fields from ActivatedJobResult
- execution_strategy override on JobWorker controls context type
"""

from typing import Any
import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock
from camunda_orchestration_sdk.runtime.job_worker import (
    ConnectedJobContext,
    JobContext,
    JobWorker,
    WorkerConfig,
)
from camunda_orchestration_sdk.models.activated_job_result import ActivatedJobResult
from camunda_orchestration_sdk.models.job_activation_result import JobActivationResult


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.complete_job = AsyncMock()
    client.fail_job = AsyncMock()
    client.throw_job_error = AsyncMock()
    client.activate_jobs = AsyncMock(return_value=JobActivationResult(jobs=[]))
    return client


@pytest.fixture
def mock_job_item():
    job = MagicMock(spec=ActivatedJobResult)
    job.job_key = 12345
    job.type_ = "test-job"
    job.process_instance_key = 1
    job.bpmn_process_id = "process"
    job.process_definition_version = 1
    job.process_definition_key = 2
    job.element_id = "element"
    job.element_instance_key = 3
    job.custom_headers = {}
    job.worker = "worker"
    job.retries = 3
    job.deadline = 1234567890
    job.variables = None
    return job


CONFIG = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)


# ---------------------------------------------------------------------------
# Context type depends on strategy
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_strategy_provides_connected_context(
    mock_client: MagicMock, mock_job_item: MagicMock
):
    """async strategy should pass ConnectedJobContext with client to the handler."""
    received_context = None

    async def handler(job: ConnectedJobContext) -> None:
        nonlocal received_context
        received_context = job

    worker = JobWorker(mock_client, handler, CONFIG, execution_strategy="async")
    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    assert isinstance(received_context, ConnectedJobContext)
    assert received_context.client is mock_client


@pytest.mark.asyncio
async def test_thread_strategy_provides_connected_context(
    mock_client: MagicMock, mock_job_item: MagicMock
):
    """thread strategy should pass ConnectedJobContext with client to the handler."""
    received_context = None

    def handler(job: ConnectedJobContext) -> None:
        nonlocal received_context
        received_context = job

    worker = JobWorker(mock_client, handler, CONFIG, execution_strategy="thread")
    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    assert isinstance(received_context, ConnectedJobContext)
    assert received_context.client is mock_client


@pytest.mark.asyncio
async def test_process_strategy_provides_plain_context(
    mock_client: MagicMock, mock_job_item: MagicMock
):
    """process strategy should create plain JobContext (no client) for the handler."""
    from unittest.mock import patch

    def handler(job: JobContext) -> None:
        pass

    worker = JobWorker(mock_client, handler, CONFIG, execution_strategy="process")

    # Capture the job_context passed to _execute_task_isolated without actually
    # running through ProcessPoolExecutor (local functions aren't picklable).
    captured_context = None

    async def fake_run_in_executor(
        pool: Any, fn: Any, *args: Any
    ) -> tuple[str, dict[str, Any] | None]:
        nonlocal captured_context
        # args are (callback, job_context)
        if len(args) >= 2:
            captured_context = args[1]
        return ("complete", None)

    with patch.object(
        asyncio.get_event_loop(),
        "run_in_executor",
        side_effect=fake_run_in_executor,
    ):
        await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    assert isinstance(captured_context, JobContext)
    assert not isinstance(captured_context, ConnectedJobContext)


@pytest.mark.asyncio
async def test_auto_strategy_async_callback_provides_connected_context(
    mock_client: MagicMock, mock_job_item: MagicMock
):
    """auto strategy with async callback → async → ConnectedJobContext."""
    received_context = None

    async def handler(job: ConnectedJobContext) -> None:
        nonlocal received_context
        received_context = job

    worker = JobWorker(
        mock_client, handler, CONFIG
    )  # default execution_strategy="auto"
    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    assert isinstance(received_context, ConnectedJobContext)


@pytest.mark.asyncio
async def test_auto_strategy_sync_callback_provides_connected_context(
    mock_client: MagicMock, mock_job_item: MagicMock
):
    """auto strategy with sync callback → thread → ConnectedJobContext."""
    received_context = None

    def handler(job: ConnectedJobContext) -> None:
        nonlocal received_context
        received_context = job

    worker = JobWorker(
        mock_client, handler, CONFIG
    )  # default execution_strategy="auto"
    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    assert isinstance(received_context, ConnectedJobContext)


# ---------------------------------------------------------------------------
# ConnectedJobContext.create() copies fields correctly
# ---------------------------------------------------------------------------


def test_connected_context_create_copies_all_fields(mock_client: MagicMock):
    """ConnectedJobContext.create() should copy all ActivatedJobResult fields."""
    from camunda_orchestration_sdk.models.activated_job_result_custom_headers import (
        ActivatedJobResultCustomHeaders,
    )
    from camunda_orchestration_sdk.models.activated_job_result_variables import (
        ActivatedJobResultVariables,
    )
    from camunda_orchestration_sdk.semantic_types import (
        JobKey,
        ProcessInstanceKey,
        ProcessDefinitionId,
        ProcessDefinitionKey,
        ElementId,
        ElementInstanceKey,
        TenantId,
    )
    from camunda_orchestration_sdk.models.job_kind_enum import JobKindEnum
    from camunda_orchestration_sdk.models.job_listener_event_type_enum import (
        JobListenerEventTypeEnum,
    )

    job = ActivatedJobResult(
        job_key=JobKey("99"),
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
        kind=JobKindEnum("BPMN_ELEMENT"),
        listener_event_type=JobListenerEventTypeEnum("UNSPECIFIED"),
        tags=[],
        root_process_instance_key=None,
    )

    ctx = ConnectedJobContext.create(job, client=mock_client)

    assert ctx.job_key == JobKey("99")
    assert ctx.type_ == "my-job"
    assert ctx.process_instance_key == ProcessInstanceKey("1")
    assert ctx.process_definition_version == 3
    assert ctx.retries == 5
    assert ctx.tenant_id == TenantId("t1")
    assert ctx.client is mock_client


def test_connected_context_is_subclass_of_job_context():
    """ConnectedJobContext should be a subclass of JobContext."""
    assert issubclass(ConnectedJobContext, JobContext)


def test_connected_context_has_log(mock_client: MagicMock):
    """ConnectedJobContext.create() with a logger should set log field."""
    from camunda_orchestration_sdk.runtime.logging import create_logger
    from camunda_orchestration_sdk.models.activated_job_result_custom_headers import (
        ActivatedJobResultCustomHeaders,
    )
    from camunda_orchestration_sdk.models.activated_job_result_variables import (
        ActivatedJobResultVariables,
    )
    from camunda_orchestration_sdk.semantic_types import (
        JobKey,
        ProcessInstanceKey,
        ProcessDefinitionId,
        ProcessDefinitionKey,
        ElementId,
        ElementInstanceKey,
        TenantId,
    )
    from camunda_orchestration_sdk.models.job_kind_enum import JobKindEnum
    from camunda_orchestration_sdk.models.job_listener_event_type_enum import (
        JobListenerEventTypeEnum,
    )

    job = ActivatedJobResult(
        job_key=JobKey("1"),
        type_="t",
        process_instance_key=ProcessInstanceKey("1"),
        process_definition_id=ProcessDefinitionId("p"),
        process_definition_version=1,
        process_definition_key=ProcessDefinitionKey("1"),
        element_id=ElementId("e"),
        element_instance_key=ElementInstanceKey("1"),
        custom_headers=ActivatedJobResultCustomHeaders(),
        worker="w",
        retries=1,
        deadline=0,
        variables=ActivatedJobResultVariables(),
        tenant_id=TenantId("t"),
        kind=JobKindEnum("BPMN_ELEMENT"),
        listener_event_type=JobListenerEventTypeEnum("UNSPECIFIED"),
        tags=[],
        root_process_instance_key=None,
    )
    logger = create_logger()
    ctx = ConnectedJobContext.create(job, client=mock_client, logger=logger)

    assert ctx.log is logger


# ---------------------------------------------------------------------------
# execution_strategy override controls strategy selection
# ---------------------------------------------------------------------------


def test_explicit_async_overrides_sync_detection(mock_client: MagicMock):
    """Passing execution_strategy='async' forces async even for a sync callback."""

    def sync_handler(job: JobContext) -> None:
        pass

    worker = JobWorker(mock_client, sync_handler, CONFIG, execution_strategy="async")
    assert worker._strategy == "async"  # pyright: ignore[reportPrivateUsage]


def test_explicit_thread_overrides_async_detection(mock_client: MagicMock):
    """Passing execution_strategy='thread' forces thread even for an async callback."""

    async def async_handler(job: JobContext) -> None:
        pass

    worker = JobWorker(mock_client, async_handler, CONFIG, execution_strategy="thread")
    assert worker._strategy == "thread"  # pyright: ignore[reportPrivateUsage]


def test_explicit_process_overrides_async_detection(mock_client: MagicMock):
    """Passing execution_strategy='process' forces process even for an async callback."""

    async def async_handler(job: JobContext) -> None:
        pass

    worker = JobWorker(mock_client, async_handler, CONFIG, execution_strategy="process")
    assert worker._strategy == "process"  # pyright: ignore[reportPrivateUsage]


def test_auto_strategy_detects_async(mock_client: MagicMock):
    """auto + async callback → strategy='async'."""

    async def handler(job: JobContext) -> None:
        pass

    worker = JobWorker(mock_client, handler, CONFIG, execution_strategy="auto")
    assert worker._strategy == "async"  # pyright: ignore[reportPrivateUsage]


def test_auto_strategy_detects_sync_as_thread(mock_client: MagicMock):
    """auto + sync callback → strategy='thread'."""

    def handler(job: JobContext) -> None:
        pass

    worker = JobWorker(mock_client, handler, CONFIG, execution_strategy="auto")
    assert worker._strategy == "thread"  # pyright: ignore[reportPrivateUsage]


# ---------------------------------------------------------------------------
# Handler can use client from ConnectedJobContext
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_handler_can_call_client_methods(
    mock_client: MagicMock, mock_job_item: MagicMock
):
    """A ConnectedJobContext handler can call client API methods."""
    mock_client.get_topology = AsyncMock(return_value=MagicMock())
    called = False

    async def handler(job: ConnectedJobContext) -> None:
        nonlocal called
        await job.client.get_topology()
        called = True

    worker = JobWorker(mock_client, handler, CONFIG, execution_strategy="async")
    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    assert called
    mock_client.get_topology.assert_called_once()
