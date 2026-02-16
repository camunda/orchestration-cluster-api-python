import pytest
from unittest.mock import MagicMock, AsyncMock
from camunda_orchestration_sdk.runtime.job_worker import (
    JobWorker,
    WorkerConfig,
    JobContext,
)
from camunda_orchestration_sdk.models.activate_jobs_jobs_item import (
    ActivateJobsJobsItem,
)


@pytest.mark.asyncio
async def test_worker_decrements_active_jobs_on_success():
    # Mock client
    mock_client = MagicMock()
    mock_client.activate_jobs = AsyncMock(
        return_value=None
    )  # Don't return jobs in poll loop
    mock_client.complete_job = AsyncMock()

    # Mock job
    mock_job_item = MagicMock(spec=ActivateJobsJobsItem)
    mock_job_item.job_key = 123
    mock_job_item.type_ = "test-job"
    mock_job_item.process_instance_key = 1
    mock_job_item.bpmn_process_id = "process"
    mock_job_item.process_definition_version = 1
    mock_job_item.process_definition_key = 2
    mock_job_item.element_id = "element"
    mock_job_item.element_instance_key = 3
    mock_job_item.custom_headers = {}
    mock_job_item.worker = "worker"
    mock_job_item.retries = 3
    mock_job_item.deadline = 1234567890
    mock_job_item.variables = None

    # Config
    config = WorkerConfig(
        job_type="test-job",
        job_timeout_milliseconds=1000,
        max_concurrent_jobs=5,
        execution_strategy="async",
    )

    # Callback
    async def success_callback(job: JobContext) -> dict[str, str]:
        return {}

    worker = JobWorker(client=mock_client, callback=success_callback, config=config)

    # Manually simulate job execution logic to test the internal state
    # We bypass the poll loop to control the execution flow

    # 1. Simulate receiving a job (increment counter)
    with worker.lock:
        worker.active_jobs += 1

    assert worker.active_jobs == 1

    # 2. Execute the job
    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    # 3. Verify counter is decremented
    assert worker.active_jobs == 0

    # 4. Verify complete was called
    mock_client.complete_job.assert_called_once()


@pytest.mark.asyncio
async def test_worker_handles_exception_and_decrements_counter():
    # Mock client
    mock_client = MagicMock()
    mock_client.activate_jobs = AsyncMock(return_value=None)
    mock_client.fail_job = AsyncMock()

    # Mock job
    mock_job_item = MagicMock(spec=ActivateJobsJobsItem)
    mock_job_item.job_key = 456
    mock_job_item.type_ = "test-job"
    mock_job_item.process_instance_key = 1
    mock_job_item.bpmn_process_id = "process"
    mock_job_item.process_definition_version = 1
    mock_job_item.process_definition_key = 2
    mock_job_item.element_id = "element"
    mock_job_item.element_instance_key = 3
    mock_job_item.custom_headers = {}
    mock_job_item.worker = "worker"
    mock_job_item.retries = 3
    mock_job_item.deadline = 1234567890
    mock_job_item.variables = None

    # Config
    config = WorkerConfig(
        job_type="test-job",
        job_timeout_milliseconds=1000,
        max_concurrent_jobs=5,
        execution_strategy="async",
    )

    # Callback that raises exception
    async def failing_callback(job: JobContext):
        raise ValueError("Something went wrong!")

    worker = JobWorker(client=mock_client, callback=failing_callback, config=config)

    # 1. Simulate receiving a job
    with worker.lock:
        worker.active_jobs += 1

    assert worker.active_jobs == 1

    # 2. Execute the job
    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    # 3. Verify counter is decremented
    assert worker.active_jobs == 0

    # 4. Verify fail_job_async was called with correct error message
    mock_client.fail_job.assert_called_once()
    call_args = mock_client.fail_job.call_args
    assert call_args.kwargs["job_key"] == 456
    assert call_args.kwargs["data"].error_message == "Something went wrong!"
    assert call_args.kwargs["data"].retries == 2  # Should be decremented


@pytest.mark.asyncio
async def test_worker_thread_strategy_exception_handling():
    # Mock client
    mock_client = MagicMock()
    mock_client.fail_job = AsyncMock()

    # Mock job
    mock_job_item = MagicMock(spec=ActivateJobsJobsItem)
    mock_job_item.job_key = 789
    mock_job_item.type_ = "test-job"
    mock_job_item.process_instance_key = 1
    mock_job_item.bpmn_process_id = "process"
    mock_job_item.process_definition_version = 1
    mock_job_item.process_definition_key = 2
    mock_job_item.element_id = "element"
    mock_job_item.element_instance_key = 3
    mock_job_item.custom_headers = {}
    mock_job_item.worker = "worker"
    mock_job_item.retries = 3
    mock_job_item.deadline = 1234567890
    mock_job_item.variables = None

    # Config
    config = WorkerConfig(
        job_type="test-job",
        job_timeout_milliseconds=1000,
        max_concurrent_jobs=5,
        execution_strategy="thread",
    )

    # Sync Callback that raises exception
    def failing_sync_callback(job: JobContext):
        raise RuntimeError("Thread failure!")

    worker = JobWorker(
        client=mock_client, callback=failing_sync_callback, config=config
    )

    # 1. Simulate receiving a job
    with worker.lock:
        worker.active_jobs += 1

    # 2. Execute the job
    await worker._execute_job(mock_job_item)  # pyright: ignore[reportPrivateUsage]

    # 3. Verify counter is decremented
    assert worker.active_jobs == 0

    # 4. Verify fail_job_async was called
    mock_client.fail_job.assert_called_once()
    assert (
        "Thread failure!" in mock_client.fail_job.call_args.kwargs["data"].error_message
    )
