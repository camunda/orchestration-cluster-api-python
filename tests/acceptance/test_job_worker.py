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
)
from camunda_orchestration_sdk.models.activate_jobs_jobs_item import ActivateJobsJobsItem
from camunda_orchestration_sdk.models.complete_job_data import CompleteJobData
from camunda_orchestration_sdk.models.activate_jobs_response_200 import ActivateJobsResponse200
from camunda_orchestration_sdk.models.job_fail_request import JobFailRequest
from camunda_orchestration_sdk.models.job_error_request import JobErrorRequest

@pytest.fixture
def mock_client():
    client = MagicMock()
    client.complete_job = AsyncMock()
    client.fail_job = AsyncMock()
    client.throw_job_error = AsyncMock()
    client.activate_jobs = AsyncMock(return_value=ActivateJobsResponse200(jobs=[]))
    return client

@pytest.fixture
def mock_worker():
    worker = MagicMock()
    worker._strategy = "async"
    worker._decrement_active_jobs = MagicMock()
    return worker

@pytest.fixture
def mock_job_item():
    job = MagicMock(spec=ActivateJobsJobsItem)
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
    
    await worker._execute_job(mock_job_item) # pyright: ignore[reportPrivateUsage]
    
    mock_client.complete_job.assert_called_once()
    call_args = mock_client.complete_job.call_args
    assert call_args.kwargs['job_key'] == 12345
    assert isinstance(call_args.kwargs['data'], CompleteJobData)

@pytest.mark.asyncio
async def test_job_failure(mock_client: MagicMock, mock_job_item: JobContext):
    async def callback(job: JobContext):
        raise JobFailure("Something failed", retries=2, retry_back_off=100)
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)
    
    await worker._execute_job(mock_job_item) # pyright: ignore[reportPrivateUsage]
    
    mock_client.fail_job.assert_called_once()
    call_args = mock_client.fail_job.call_args
    assert call_args.kwargs['job_key'] == 12345
    assert isinstance(call_args.kwargs['data'], JobFailRequest)
    assert call_args.kwargs['data'].error_message == "Something failed"
    assert call_args.kwargs['data'].retries == 2
    assert call_args.kwargs['data'].retry_back_off == 100

@pytest.mark.asyncio
async def test_job_error(mock_client: MagicMock, mock_job_item: JobContext):
    async def callback(job: JobContext):
        raise JobError("ERR_CODE", "Business error")
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)
    
    await worker._execute_job(mock_job_item) # pyright: ignore[reportPrivateUsage]
    
    mock_client.throw_job_error.assert_called_once()
    call_args = mock_client.throw_job_error.call_args
    assert call_args.kwargs['job_key'] == 12345
    assert isinstance(call_args.kwargs['data'], JobErrorRequest)
    assert call_args.kwargs['data'].error_code == "ERR_CODE"
    assert call_args.kwargs['data'].error_message == "Business error"

@pytest.mark.asyncio
async def test_job_exception(mock_client: MagicMock, mock_job_item: JobContext):
    async def callback(job: JobContext):
        raise ValueError("Unexpected error")
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(mock_client, callback, config)
    
    await worker._execute_job(mock_job_item) # pyright: ignore[reportPrivateUsage]
    
    mock_client.fail_job.assert_called_once()
    call_args = mock_client.fail_job.call_args
    assert call_args.kwargs['job_key'] == 12345
    assert "Unexpected error" in call_args.kwargs['data'].error_message
    assert call_args.kwargs['data'].retries == 2 # Decremented from 3

def test_strategy_detection_async():
    async def async_callback(job: JobContext): 
        result: dict[str, Any] = {}
        return result
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(MagicMock(), async_callback, config) # type: ignore
    
    assert worker._strategy == "async" # pyright: ignore[reportPrivateUsage]

def test_strategy_detection_sync():
    def sync_callback(job: JobContext): 
        result: dict[str, Any] = {}
        return result
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(MagicMock(), sync_callback, config)
    
    assert worker._strategy == "thread" # pyright: ignore[reportPrivateUsage]

# def test_strategy_detection_hint():
#     @ExecutionHint.cpu_bound
#     def cpu_callback(job): pass
    
#     config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
#     worker = JobWorker(MagicMock(), cpu_callback, config)
    
#     assert worker._strategy == "process" # pyright: ignore[reportPrivateUsage]

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
        max_observed_concurrency = max(max_observed_concurrency, active_jobs_in_callback)
        await asyncio.sleep(0.1)
        active_jobs_in_callback -= 1
        result: dict[str, Any] = {}
        return result

    config = WorkerConfig(
        job_type="test", 
        job_timeout_milliseconds=1000,
        max_concurrent_jobs=2
    )
    
    worker = JobWorker(mock_client, slow_callback, config)
    
    # Mock poll response to return 2 jobs each time
    job1 = MagicMock(spec=ActivateJobsJobsItem)
    job1.job_key = 1
    job2 = MagicMock(spec=ActivateJobsJobsItem)
    job2.job_key = 2
    job3 = MagicMock(spec=ActivateJobsJobsItem)
    job3.job_key = 3
    
    # First poll returns 2 jobs (filling capacity)
    # Second poll should be skipped or return empty if capacity is full
    # But we can't easily control the timing of the poll loop vs the callback execution in this simple test without more complex mocking.
    
    # Instead, let's test _poll_for_jobs directly
    
    # 1. Initial state: 0 active jobs
    worker.active_jobs = 0
    mock_client.activate_jobs.return_value = ActivateJobsResponse200(jobs=[job1, job2])
    
    jobs = await worker._poll_for_jobs() # pyright: ignore[reportPrivateUsage]
    assert len(jobs) == 2
    assert worker.active_jobs == 2
    
    # 2. Capacity full: should skip poll
    mock_client.activate_jobs.reset_mock()
    jobs = await worker._poll_for_jobs() # pyright: ignore[reportPrivateUsage]
    assert len(jobs) == 0
    mock_client.activate_jobs.assert_not_called()
    
    # 3. One job finishes
    worker._decrement_active_jobs() # pyright: ignore[reportPrivateUsage]
    assert worker.active_jobs == 1
    
    # 4. Capacity available: should poll again
    mock_client.activate_jobs.return_value = ActivateJobsResponse200(jobs=[job3])
    jobs = await worker._poll_for_jobs() # pyright: ignore[reportPrivateUsage]
    assert len(jobs) == 1
    assert worker.active_jobs == 2
    mock_client.activate_jobs.assert_called_once()
    
    # Verify call args for capacity
    call_args = mock_client.activate_jobs.call_args
    assert call_args.kwargs['data'].max_jobs_to_activate == 1
