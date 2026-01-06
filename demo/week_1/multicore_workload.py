import time
import multiprocessing
from functools import partial
from camunda_orchestration_sdk.runtime.job_worker import JobContext

def _heavy_calculation_chunk(start: int, end: int) -> int:
    """
    A pure Python function that burns CPU.
    This will run in a separate process.
    """
    total = 0
    for i in range(start, end):
        total += i * i
    return total

def simulate_multicore_work(job: JobContext, total_items: int = 10_000_000):
    """
    Splits a massive calculation across all available CPU cores.
    """
    print(f"Starting multicore work for job {job.job_key}")
    start_time = time.time()

    # Determine number of cores
    num_cores = multiprocessing.cpu_count()
    chunk_size = total_items // num_cores
    
    # Create ranges for each core
    ranges: list[tuple[int, int]] = []
    for i in range(num_cores):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_cores - 1 else total_items
        ranges.append((start, end))

    print(f"Spawning {num_cores} processes to calculate sum of squares for {total_items} items...")

    # Create a pool of workers
    # Note: We use 'spawn' or 'fork' depending on OS, Pool handles this.
    with multiprocessing.Pool(processes=num_cores) as pool:
        # Map the work to the processes
        results = pool.starmap(_heavy_calculation_chunk, ranges)
    
    final_result = sum(results)
    
    duration = time.time() - start_time
    print(f"Completed in {duration:.2f}s. Result: {final_result}")
    
    return {"result": final_result, "duration_seconds": duration}