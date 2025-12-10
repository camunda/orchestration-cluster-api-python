from camunda_orchestration_sdk.models.complete_job_data_variables_type_0 import CompleteJobDataVariablesType0
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from camunda_orchestration_sdk.runtime.job_worker import (
    JobWorker, 
    WorkerConfig, 
    ActivatedJob, 
    JobFinalized,
    ExecutionHint
)
from camunda_orchestration_sdk.models.activate_jobs_response_200_jobs_item import ActivateJobsResponse200JobsItem
from camunda_orchestration_sdk.models.complete_job_data import CompleteJobData
from camunda_orchestration_sdk.models.activate_jobs_response_200 import ActivateJobsResponse200

@pytest.fixture
def mock_client():
    client = MagicMock()
    client.complete_job_async = AsyncMock()
    client.fail_job_async = AsyncMock()
    client.throw_job_error_async = AsyncMock()
    client.complete_job = MagicMock()
    client.fail_job = MagicMock()
    client.throw_job_error = MagicMock()
    client.activate_jobs_async = AsyncMock(return_value=ActivateJobsResponse200(jobs=[]))
    return client

@pytest.fixture
def mock_worker():
    worker = MagicMock()
    worker._strategy = "async"
    worker._decrement_active_jobs = MagicMock()
    return worker

@pytest.fixture
def mock_job_item():
    job = MagicMock(spec=ActivateJobsResponse200JobsItem)
    job.job_key = 12345
    return job

@pytest.mark.asyncio
async def test_activated_job_complete_async(mock_client, mock_worker, mock_job_item):
    activated_job = ActivatedJob(mock_job_item, mock_client, mock_worker)
    
    # Test complete
    variables = CompleteJobDataVariablesType0.from_dict({})
    result = await activated_job.complete(CompleteJobData(variables=variables))
    
    assert isinstance(result, JobFinalized)
    mock_client.complete_job_async.assert_called_once()
    mock_worker._decrement_active_jobs.assert_called_once()

@pytest.mark.asyncio
async def test_activated_job_complete_with_dict(mock_client, mock_worker, mock_job_item):
    activated_job = ActivatedJob(mock_job_item, mock_client, mock_worker)
    
    # Test complete with dict
    result = await activated_job.complete({"foo": "bar"})
    
    assert isinstance(result, JobFinalized)
    mock_client.complete_job_async.assert_called_once()
    
    # Verify the dict was converted to CompleteJobData
    call_args = mock_client.complete_job_async.call_args
    assert isinstance(call_args.kwargs['data'], CompleteJobData)
    # Note: checking the inner variables structure depends on how CompleteJobDataVariablesType0 works,
    # but we verified it was converted to the correct model type.
    
    mock_worker._decrement_active_jobs.assert_called_once()

@pytest.mark.asyncio
async def test_activated_job_complete_no_args(mock_client, mock_worker, mock_job_item):
    activated_job = ActivatedJob(mock_job_item, mock_client, mock_worker)
    
    # Test complete with no args
    result = await activated_job.complete()
    
    assert isinstance(result, JobFinalized)
    mock_client.complete_job_async.assert_called_once()
    
    # Verify data is CompleteJobData (empty)
    call_args = mock_client.complete_job_async.call_args
    assert isinstance(call_args.kwargs['data'], CompleteJobData)
    
    mock_worker._decrement_active_jobs.assert_called_once()

@pytest.mark.asyncio
async def test_activated_job_ignore(mock_client, mock_worker, mock_job_item):
    activated_job = ActivatedJob(mock_job_item, mock_client, mock_worker)
    
    # Test ignore
    result = activated_job.ignore()
    
    assert isinstance(result, JobFinalized)
    mock_client.complete_job_async.assert_not_called()
    mock_client.fail_job_async.assert_not_called()
    mock_worker._decrement_active_jobs.assert_called_once()

@pytest.mark.asyncio
async def test_activated_job_double_finalization(mock_client, mock_worker, mock_job_item):
    activated_job = ActivatedJob(mock_job_item, mock_client, mock_worker)
    
    variables = CompleteJobDataVariablesType0.from_dict({})
    await activated_job.complete(CompleteJobData(variables=variables))
    
    with pytest.raises(RuntimeError, match="has already been finalized"):
        await activated_job.fail("oops", 0)
        
    # Ensure decrement was only called once
    mock_worker._decrement_active_jobs.assert_called_once()

def test_strategy_detection_async():
    async def async_callback(job: ActivatedJob) -> JobFinalized: 
        return await job.complete()
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(MagicMock(), async_callback, config) # type: ignore
    
    assert worker._strategy == "async"

def test_strategy_detection_sync():
    def sync_callback(job: ActivatedJob) -> JobFinalized: 
        return job.complete()
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(MagicMock(), sync_callback, config)
    
    assert worker._strategy == "thread"

def test_strategy_detection_hint():
    @ExecutionHint.cpu_bound
    def cpu_callback(job): pass
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    worker = JobWorker(MagicMock(), cpu_callback, config)
    
    assert worker._strategy == "process"

def test_strategy_validation_async_mismatch():
    # Strategy is async, but callback is sync
    def sync_callback(job): pass
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000, execution_strategy="async")
    
    with pytest.raises(ValueError, match="Execution strategy is 'async' but callback .* is synchronous"):
        JobWorker(MagicMock(), sync_callback, config)

def test_strategy_validation_thread_mismatch():
    # Strategy is thread, but callback is async
    async def async_callback(job): pass
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000, execution_strategy="thread")
    
    with pytest.raises(ValueError, match="Execution strategy is 'thread' but callback .* is asynchronous"):
        JobWorker(MagicMock(), async_callback, config)

def test_strategy_validation_hint_mismatch():
    # Hint says io_bound (thread), but callback is async
    @ExecutionHint.io_bound
    async def async_callback(job): pass
    
    config = WorkerConfig(job_type="test", job_timeout_milliseconds=1000)
    
    with pytest.raises(ValueError, match="Execution strategy is 'thread' but callback .* is asynchronous"):
        JobWorker(MagicMock(), async_callback, config)

@pytest.mark.asyncio
async def test_worker_concurrency_limit(mock_client):
    # Setup
    mock_client.activate_jobs_async = AsyncMock()
    
    # Create a callback that holds the job for a bit
    active_jobs_in_callback = 0
    max_observed_concurrency = 0
    
    async def slow_callback(job: ActivatedJob):
        nonlocal active_jobs_in_callback, max_observed_concurrency
        active_jobs_in_callback += 1
        max_observed_concurrency = max(max_observed_concurrency, active_jobs_in_callback)
        await asyncio.sleep(0.1)
        job.ignore()
        active_jobs_in_callback -= 1
        return JobFinalized()

    config = WorkerConfig(
        job_type="test", 
        job_timeout_milliseconds=1000,
        max_concurrent_jobs=2
    )
    
    worker = JobWorker(mock_client, slow_callback, config)
    
    # Mock poll response to return 2 jobs each time
    job1 = MagicMock(spec=ActivateJobsResponse200JobsItem); job1.job_key = 1
    job2 = MagicMock(spec=ActivateJobsResponse200JobsItem); job2.job_key = 2
    job3 = MagicMock(spec=ActivateJobsResponse200JobsItem); job3.job_key = 3
    
    # First poll returns 2 jobs (filling capacity)
    # Second poll should be skipped or return empty if capacity is full
    # But we can't easily control the timing of the poll loop vs the callback execution in this simple test without more complex mocking.
    
    # Instead, let's test _poll_for_jobs directly
    
    # 1. Initial state: 0 active jobs
    worker.active_jobs = 0
    mock_client.activate_jobs_async.return_value = ActivateJobsResponse200(jobs=[job1, job2])
    
    jobs = await worker._poll_for_jobs()
    assert len(jobs) == 2
    assert worker.active_jobs == 2
    
    # 2. Capacity full: should skip poll
    mock_client.activate_jobs_async.reset_mock()
    jobs = await worker._poll_for_jobs()
    assert len(jobs) == 0
    mock_client.activate_jobs_async.assert_not_called()
    
    # 3. One job finishes
    worker._decrement_active_jobs()
    assert worker.active_jobs == 1
    
    # 4. Capacity available: should poll again
    mock_client.activate_jobs_async.return_value = ActivateJobsResponse200(jobs=[job3])
    jobs = await worker._poll_for_jobs()
    assert len(jobs) == 1
    assert worker.active_jobs == 2
    mock_client.activate_jobs_async.assert_called_once()
    
    # Verify call args for capacity
    call_args = mock_client.activate_jobs_async.call_args
    assert call_args.kwargs['data'].max_jobs_to_activate == 1

