from typing import Any
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from camunda_orchestration_sdk.runtime.job_worker import (
    JobWorker,
    WorkerConfig,
    JobContext,
    JobError,
    JobFailure,
    ConnectedJobContext,
)
from camunda_orchestration_sdk.models.activated_job_result import (
    ActivatedJobResult,
)
from camunda_orchestration_sdk.models.job_completion_request import JobCompletionRequest
from camunda_orchestration_sdk.models.job_result_user_task import JobResultUserTask
from camunda_orchestration_sdk.models.job_result_corrections import JobResultCorrections
from camunda_orchestration_sdk.models.job_activation_result import (
    JobActivationResult,
)
from camunda_orchestration_sdk.models.job_fail_request import JobFailRequest
from camunda_orchestration_sdk.models.job_error_request import JobErrorRequest


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.complete_job = AsyncMock()
    client.fail_job = AsyncMock()
    client.throw_job_error = AsyncMock()
    client.activate_jobs = AsyncMock(return_value=JobActivationResult(jobs=[]))
    return client


@pytest.fixture
def mock_worker():
    worker = MagicMock()
    worker._strategy = "async"
    worker._decrement_active_jobs = MagicMock()
    return worker


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


@pytest.mark.asyncio
async def test_job_completion(mock_client: MagicMock, mock_job_item: JobContext):
    async def callback(job: JobContext):
        return {"foo": "bar"}

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    mock_client.complete_job.assert_called_once()
    call_args = mock_client.complete_job.call_args
    assert call_args.kwargs["job_key"] == 12345
    assert isinstance(call_args.kwargs["data"], JobCompletionRequest)


@pytest.mark.asyncio
async def test_job_completion_with_corrections(mock_client: MagicMock, mock_job_item: JobContext):
    """Sync-style handler can return a JobCompletionRequest with corrections."""

    def callback(job: JobContext) -> JobCompletionRequest:
        return JobCompletionRequest(
            result=JobResultUserTask(
                type_="userTask",
                corrections=JobResultCorrections(
                    assignee="corrected-user",
                    priority=80,
                ),
            ),
        )

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    mock_client.complete_job.assert_called_once()
    call_args = mock_client.complete_job.call_args
    assert call_args.kwargs["job_key"] == 12345
    data = call_args.kwargs["data"]
    assert isinstance(data, JobCompletionRequest)
    assert isinstance(data.result, JobResultUserTask)
    assert data.result.type_ == "userTask"
    assert isinstance(data.result.corrections, JobResultCorrections)
    assert data.result.corrections.assignee == "corrected-user"
    assert data.result.corrections.priority == 80


@pytest.mark.asyncio
async def test_job_failure(mock_client: MagicMock, mock_job_item: JobContext):
    async def callback(job: JobContext):
        raise JobFailure("Something failed", retries=2, retry_back_off=100)

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    mock_client.fail_job.assert_called_once()
    call_args = mock_client.fail_job.call_args
    assert call_args.kwargs["job_key"] == 12345
    assert isinstance(call_args.kwargs["data"], JobFailRequest)
    assert call_args.kwargs["data"].error_message == "Something failed"
    assert call_args.kwargs["data"].retries == 2
    assert call_args.kwargs["data"].retry_back_off == 100


@pytest.mark.asyncio
async def test_job_error(mock_client: MagicMock, mock_job_item: JobContext):
    async def callback(job: JobContext):
        raise JobError("ERR_CODE", "Business error")

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    mock_client.throw_job_error.assert_called_once()
    call_args = mock_client.throw_job_error.call_args
    assert call_args.kwargs["job_key"] == 12345
    assert isinstance(call_args.kwargs["data"], JobErrorRequest)
    assert call_args.kwargs["data"].error_code == "ERR_CODE"
    assert call_args.kwargs["data"].error_message == "Business error"


@pytest.mark.asyncio
async def test_job_exception(mock_client: MagicMock, mock_job_item: JobContext):
    async def callback(job: JobContext):
        raise ValueError("Unexpected error")

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    mock_client.fail_job.assert_called_once()
    call_args = mock_client.fail_job.call_args
    assert call_args.kwargs["job_key"] == 12345
    assert "Unexpected error" in call_args.kwargs["data"].error_message
    assert call_args.kwargs["data"].retries == 2  # Decremented from 3


def test_strategy_detection_async():
    async def async_callback(job: JobContext):
        result: dict[str, Any] = {}
        return result

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(MagicMock(), async_callback, config)

    assert worker._strategy == "async"  # pyright: ignore[reportPrivateUsage]


def test_strategy_detection_sync():
    def sync_callback(job: JobContext):
        result: dict[str, Any] = {}
        return result

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(MagicMock(), sync_callback, config)

    assert worker._strategy == "thread"  # pyright: ignore[reportPrivateUsage]


@pytest.mark.asyncio
async def test_worker_concurrency_limit(mock_client: MagicMock):
    # Setup
    mock_client.activate_jobs = AsyncMock()

    # Create a callback that holds the job for a bit
    active_jobs_in_callback = 0
    max_observed_concurrency = 0

    async def slow_callback(job: JobContext):
        nonlocal active_jobs_in_callback, max_observed_concurrency
        active_jobs_in_callback += 1
        max_observed_concurrency = max(
            max_observed_concurrency, active_jobs_in_callback
        )
        await asyncio.sleep(0.1)
        active_jobs_in_callback -= 1
        result: dict[str, Any] = {}
        return result

    config = WorkerConfig(
        job_type="test", job_timeout_milliseconds=1000, max_concurrent_jobs=2
    )

    worker = JobWorker(mock_client, slow_callback, config)

    # Mock poll response to return 2 jobs each time
    job1 = MagicMock(spec=ActivatedJobResult)
    job1.job_key = 1
    job2 = MagicMock(spec=ActivatedJobResult)
    job2.job_key = 2
    job3 = MagicMock(spec=ActivatedJobResult)
    job3.job_key = 3

    # First poll returns 2 jobs (filling capacity)
    # Second poll should be skipped or return empty if capacity is full
    # But we can't easily control the timing of the poll loop vs the callback execution in this simple test without more complex mocking.

    # Instead, let's test _poll_for_jobs directly

    # 1. Initial state: 0 active jobs
    worker.active_jobs = 0
    mock_client.activate_jobs.return_value = JobActivationResult(jobs=[job1, job2])

    jobs = await worker._poll_for_jobs()  # pyright: ignore[reportPrivateUsage]
    assert len(jobs) == 2
    assert worker.active_jobs == 2

    # 2. Capacity full: should skip poll
    mock_client.activate_jobs.reset_mock()
    jobs = await worker._poll_for_jobs()  # pyright: ignore[reportPrivateUsage]
    assert len(jobs) == 0
    mock_client.activate_jobs.assert_not_called()

    # 3. One job finishes
    worker._decrement_active_jobs()  # pyright: ignore[reportPrivateUsage]
    assert worker.active_jobs == 1

    # 4. Capacity available: should poll again
    mock_client.activate_jobs.return_value = JobActivationResult(jobs=[job3])
    jobs = await worker._poll_for_jobs()  # pyright: ignore[reportPrivateUsage]
    assert len(jobs) == 1
    assert worker.active_jobs == 2
    mock_client.activate_jobs.assert_called_once()

    # Verify call args for capacity
    call_args = mock_client.activate_jobs.call_args
    assert call_args.kwargs["data"].max_jobs_to_activate == 1


# ---------------------------------------------------------------------------
# Autocomplete suppression when handler explicitly handles the job
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_autocomplete_suppressed_when_handler_calls_fail_job(
    mock_client: MagicMock, mock_job_item: JobContext
):
    """When the handler calls job.client.fail_job() and returns normally,
    the worker must NOT auto-complete the job."""

    async def callback(job: ConnectedJobContext):
        await job.client.fail_job(
            job_key=job.job_key,
            data=JobFailRequest(error_message="handled by handler", retries=1),
        )
        return {"should": "be ignored"}

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    # fail_job should have been called (through the wrapper -> mock)
    mock_client.fail_job.assert_called_once()
    # complete_job must NOT be called (auto-complete suppressed)
    mock_client.complete_job.assert_not_called()


@pytest.mark.asyncio
async def test_autocomplete_suppressed_when_handler_calls_throw_job_error(
    mock_client: MagicMock, mock_job_item: JobContext
):
    """When the handler calls job.client.throw_job_error() and returns normally,
    the worker must NOT auto-complete the job."""

    async def callback(job: ConnectedJobContext):
        await job.client.throw_job_error(
            job_key=job.job_key,
            data=JobErrorRequest(error_code="ERR_HANDLED", error_message="handled"),
        )
        return None

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    mock_client.throw_job_error.assert_called_once()
    mock_client.complete_job.assert_not_called()


@pytest.mark.asyncio
async def test_autocomplete_suppressed_when_handler_calls_complete_job(
    mock_client: MagicMock, mock_job_item: JobContext
):
    """When the handler calls job.client.complete_job() explicitly,
    the worker must NOT auto-complete a second time."""

    async def callback(job: ConnectedJobContext):
        await job.client.complete_job(
            job_key=job.job_key,
            data=JobCompletionRequest(),
        )
        return {"extra": "data"}

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    # complete_job should only be called once (by the handler, NOT by auto-complete)
    mock_client.complete_job.assert_called_once()


@pytest.mark.asyncio
async def test_ack_flag_not_set_when_api_call_fails(
    mock_client: MagicMock, mock_job_item: JobContext
):
    """If the underlying complete_job API call raises, the ack flag must stay
    unset so the worker can still attempt auto-fail for the job."""

    mock_client.complete_job.side_effect = RuntimeError("API unavailable")

    async def callback(job: ConnectedJobContext):
        # Handler tries to complete but the API fails
        with pytest.raises(RuntimeError, match="API unavailable"):
            await job.client.complete_job(
                job_key=job.job_key,
                data=JobCompletionRequest(),
            )
        # Handler re-raises so the worker auto-fails
        raise RuntimeError("complete failed")

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    # complete_job was attempted once (by handler) and raised
    mock_client.complete_job.assert_called_once()
    # Worker should auto-fail because ack flag was NOT set (the API call failed)
    mock_client.fail_job.assert_called_once()


@pytest.mark.asyncio
async def test_ack_suppresses_auto_fail(
    mock_client: MagicMock, mock_job_item: JobContext
):
    """When the handler explicitly completes the job and then raises,
    the worker must NOT attempt to auto-fail — the ack flag guards
    all terminal actions, not just complete."""

    async def callback(job: ConnectedJobContext):
        # Handler successfully completes the job...
        await job.client.complete_job(
            job_key=job.job_key,
            data=JobCompletionRequest(),
        )
        # ...but then raises for some reason
        raise RuntimeError("post-complete error")

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    # complete_job called once (by handler)
    mock_client.complete_job.assert_called_once()
    # fail_job must NOT be called — ack flag suppresses all terminal actions
    mock_client.fail_job.assert_not_called()


@pytest.mark.asyncio
async def test_ack_suppresses_auto_error(
    mock_client: MagicMock, mock_job_item: JobContext
):
    """When the handler explicitly fails the job and then raises a JobError,
    the worker must NOT attempt to auto-throw-error."""

    async def callback(job: ConnectedJobContext):
        # Handler explicitly fails the job
        await job.client.fail_job(
            job_key=job.job_key,
            data=JobFailRequest(error_message="handled", retries=0),
        )
        # Then raises a JobError — worker should NOT send a second terminal op
        raise JobError("ERR", "should be ignored")

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    # fail_job called once (by handler)
    mock_client.fail_job.assert_called_once()
    # throw_job_error must NOT be called — ack flag suppresses
    mock_client.throw_job_error.assert_not_called()


# ---------------------------------------------------------------------------
# Variables support on JobFailure and JobError exceptions
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_job_failure_with_variables(mock_client: MagicMock, mock_job_item: JobContext):
    """JobFailure with variables passes them through to fail_job."""

    async def callback(job: JobContext):
        raise JobFailure(
            "Something failed",
            retries=2,
            retry_back_off=100,
            variables={"errorDetail": "bad input", "retryCount": 2},
        )

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    mock_client.fail_job.assert_called_once()
    call_args = mock_client.fail_job.call_args
    data = call_args.kwargs["data"]
    assert isinstance(data, JobFailRequest)
    assert data.error_message == "Something failed"
    assert data.retries == 2
    assert data.retry_back_off == 100
    assert data.variables.to_dict() == {"errorDetail": "bad input", "retryCount": 2}


@pytest.mark.asyncio
async def test_job_failure_without_variables_omits_field(
    mock_client: MagicMock, mock_job_item: JobContext
):
    """JobFailure without variables does not set the variables field."""

    async def callback(job: JobContext):
        raise JobFailure("Something failed", retries=1)

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    mock_client.fail_job.assert_called_once()
    call_args = mock_client.fail_job.call_args
    data = call_args.kwargs["data"]
    from camunda_orchestration_sdk.types import UNSET

    assert data.variables is UNSET


@pytest.mark.asyncio
async def test_job_error_with_variables(mock_client: MagicMock, mock_job_item: JobContext):
    """JobError with variables passes them through to throw_job_error."""

    async def callback(job: JobContext):
        raise JobError(
            "ERR_CODE",
            "Business error",
            variables={"failedItem": "order-123"},
        )

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    mock_client.throw_job_error.assert_called_once()
    call_args = mock_client.throw_job_error.call_args
    data = call_args.kwargs["data"]
    assert isinstance(data, JobErrorRequest)
    assert data.error_code == "ERR_CODE"
    assert data.error_message == "Business error"
    assert data.variables.to_dict() == {"failedItem": "order-123"}


@pytest.mark.asyncio
async def test_job_error_without_variables_omits_field(
    mock_client: MagicMock, mock_job_item: JobContext
):
    """JobError without variables does not set the variables field."""

    async def callback(job: JobContext):
        raise JobError("ERR_CODE", "Business error")

    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)

    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    mock_client.throw_job_error.assert_called_once()
    call_args = mock_client.throw_job_error.call_args
    data = call_args.kwargs["data"]
    from camunda_orchestration_sdk.types import UNSET

    assert data.variables is UNSET
