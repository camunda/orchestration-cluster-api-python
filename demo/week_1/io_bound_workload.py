import asyncio

from camunda_orchestration_sdk.runtime.job_worker import JobContext

async def simulate_io_work_async(job: JobContext, duration: float = 5.0):
    """Simulate I/O-bound work with async network operations.

    Uses asyncio.sleep to simulate network latency (e.g. calling an external API).
    This demonstrates proper async handling where the event loop can switch to other tasks
    while waiting for the "network response".
    """
    print(f"Working on job. Job Key: {job.job_key}")
    
    # Simulate multiple network calls with latency
    steps = 5
    step_duration = duration / steps
    
    for _ in range(steps):
        # This yields control back to the event loop
        await asyncio.sleep(step_duration)
        # print(f"Job {job.job_key}: Completed step {i+1}/{steps}")
        
    print(f"Completed work for {job.job_key}")

    