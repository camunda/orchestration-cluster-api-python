import time
from camunda_orchestration_sdk.runtime.job_worker import JobContext

def simulate_cpu_work(job: JobContext, duration: float = 5.0):
    """Simulate CPU-bound work that heavily engages the Python interpreter (GIL-bound).

    Performs arithmetic operations and list comprehensions to ensure the
    Global Interpreter Lock (GIL) is held, preventing multi-threaded parallelism.
    """
    print(f"Working on job. Job Key: {job.job_key}")
    end_time = time.time() + duration
    while time.time() < end_time:
        # Create and destroy objects, do math
        # This is pure Python work that cannot be parallelized by threads
        _ = [x * x for x in range(500_000)]
    print(f"Completed work for {job.job_key}")
