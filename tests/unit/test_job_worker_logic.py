import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from camunda_orchestration_sdk.runtime.job_worker import JobWorker, WorkerConfig, ActivatedJob, SyncActivatedJob
from camunda_orchestration_sdk.models.activate_jobs_response_200_jobs_item import ActivateJobsResponse200JobsItem

@pytest.mark.asyncio
async def test_worker_decrements_active_jobs_on_success():
    # Mock client
    mock_client = MagicMock()
    mock_client.activate_jobs_async = AsyncMock(return_value=None) # Don't return jobs in poll loop
    mock_client.complete_job_async = AsyncMock()

    # Mock job
    mock_job_item = MagicMock(spec=ActivateJobsResponse200JobsItem)
    mock_job_item.job_key = 123
    
    # Config
    config = WorkerConfig(
        job_type="test-job",
        job_timeout_milliseconds=1000,
        max_concurrent_jobs=5,
        execution_strategy="async"
    )

    # Callback
    async def success_callback(job: ActivatedJob):
        return await job.complete()

    worker = JobWorker(client=mock_client, callback=success_callback, config=config)
    
    # Manually simulate job execution logic to test the internal state
    # We bypass the poll loop to control the execution flow
    
    # 1. Simulate receiving a job (increment counter)
    with worker.lock:
        worker.active_jobs += 1
    
    assert worker.active_jobs == 1

    # 2. Execute the job
    await worker._execute_job(mock_job_item)

    # 3. Verify counter is decremented
    assert worker.active_jobs == 0
    
    # 4. Verify complete was called
    mock_client.complete_job_async.assert_called_once()


@pytest.mark.asyncio
async def test_worker_handles_exception_and_decrements_counter():
    # Mock client
    mock_client = MagicMock()
    mock_client.activate_jobs_async = AsyncMock(return_value=None)
    mock_client.fail_job_async = AsyncMock()

    # Mock job
    mock_job_item = MagicMock(spec=ActivateJobsResponse200JobsItem)
    mock_job_item.job_key = 456
    mock_job_item.retries = 3
    
    # Config
    config = WorkerConfig(
        job_type="test-job",
        job_timeout_milliseconds=1000,
        max_concurrent_jobs=5,
        execution_strategy="async"
    )

    # Callback that raises exception
    async def failing_callback(job: ActivatedJob):
        raise ValueError("Something went wrong!")

    worker = JobWorker(client=mock_client, callback=failing_callback, config=config)
    
    # 1. Simulate receiving a job
    with worker.lock:
        worker.active_jobs += 1
    
    assert worker.active_jobs == 1

    # 2. Execute the job
    await worker._execute_job(mock_job_item)

    # 3. Verify counter is decremented
    assert worker.active_jobs == 0
    
    # 4. Verify fail_job_async was called with correct error message
    mock_client.fail_job_async.assert_called_once()
    call_args = mock_client.fail_job_async.call_args
    assert call_args.kwargs['job_key'] == 456
    assert call_args.kwargs['data'].error_message == "Something went wrong!"
    assert call_args.kwargs['data'].retries == 2 # Should be decremented


@pytest.mark.asyncio
async def test_worker_thread_strategy_exception_handling():
    # Mock client
    mock_client = MagicMock()
    mock_client.fail_job_async = AsyncMock()

    # Mock job
    mock_job_item = MagicMock(spec=ActivateJobsResponse200JobsItem)
    mock_job_item.job_key = 789
    mock_job_item.retries = 3
    
    # Config
    config = WorkerConfig(
        job_type="test-job",
        job_timeout_milliseconds=1000,
        max_concurrent_jobs=5,
        execution_strategy="thread"
    )

    # Sync Callback that raises exception
    def failing_sync_callback(job: SyncActivatedJob):
        raise RuntimeError("Thread failure!")

    worker = JobWorker(client=mock_client, callback=failing_sync_callback, config=config)
    
    # 1. Simulate receiving a job
    with worker.lock:
        worker.active_jobs += 1
    
    # 2. Execute the job
    await worker._execute_job(mock_job_item)

    # 3. Verify counter is decremented
    assert worker.active_jobs == 0
    
    # 4. Verify fail_job_async was called
    mock_client.fail_job_async.assert_called_once()
    assert "Thread failure!" in mock_client.fail_job_async.call_args.kwargs['data'].error_message
