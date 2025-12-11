# Job Worker Demo & Benchmark

This directory contains a comprehensive demonstration and benchmarking tool for the Camunda Python SDK's `JobWorker`. The `job_worker_benchmark.py` script allows you to test different execution strategies (`async`, `thread`, `process`) under various simulated workloads (`cpu`, `io`, `subprocess`).

## Prerequisites

*   Python 3.10+
*   A running Camunda 8 instance (Self-Managed or SaaS).
*   The `camunda-orchestration-sdk` package installed.
*   Environment variables configured for Camunda connection (e.g., `CAMUNDA_BASE_URL` or `ZEEBE_ADDRESS`, `ZEEBE_CLIENT_ID`, etc.).

## Usage

The script is a command-line tool that supports several modes of operation. We recommend using `uv` to run the script.

### Default Run

Runs a simple scenario with 1 process instance and the `auto` execution strategy.

```bash
uv run demo/v2/job_worker_benchmark.py
```

### Quick Test

Runs a quick test with 5 instances.

```bash
uv run demo/v2/job_worker_benchmark.py quick
```

### Benchmarking Strategies

Compares all execution strategies (`async`, `thread`, `process`, `auto`) using a CPU-bound workload.

```bash
uv run demo/v2/job_worker_benchmark.py benchmark --process_instances 50 --work_duration_seconds 3.0 --job_timeout_milliseconds 30000
```

*   `--process_instances`: Number of process instances to start (default: 20).
*   `--work_duration_seconds`: Duration of simulated work in seconds (default: 3.0).
*   `--job_timeout_milliseconds`: Job timeout in milliseconds (default: 30000).

### Benchmarking Workloads

Compares strategies across both CPU-bound and I/O-bound workloads.

```bash
uv run demo/v2/job_worker_benchmark.py benchmark-workloads --process_instances 20 --work_duration_seconds 3.0 --job_timeout_milliseconds 30000
```

*   `--process_instances`: Number of process instances to start (default: 20).
*   `--work_duration_seconds`: Duration of simulated work in seconds (default: 3.0).
*   `--job_timeout_milliseconds`: Job timeout in milliseconds (default: 30000).

### Benchmarking Subprocess Calls

Specifically tests `subprocess.call()` behavior across strategies to check for deadlocks or issues.

```bash
uv run demo/v2/job_worker_benchmark.py benchmark-subprocess --process_instances 20 --work_duration_seconds 3.0 --job_timeout_milliseconds 30000
```

*   `--process_instances`: Number of process instances to start (default: 20).
*   `--work_duration_seconds`: Duration of simulated work in seconds (default: 3.0).
*   `--job_timeout_milliseconds`: Job timeout in milliseconds (default: 30000).

### Custom Test Run

Run a fully customizable test with specific parameters.

```bash
uv run demo/v2/job_worker_benchmark.py test --process_instances 20 --worker_strategy process --workload_type cpu --repeat_runs 3 --max_concurrent_jobs 10 --work_duration_seconds 3.0 --job_timeout_milliseconds 30000
```

*   `--process_instances`: Number of process instances to start (default: 10).
*   `--worker_strategy`: `auto`, `async`, `thread`, or `process` (default: auto).
*   `--workload_type`: `cpu`, `io`, or `subprocess` (default: cpu).
*   `--repeat_runs`: Number of times to repeat the test (results are averaged) (default: 1).
*   `--max_concurrent_jobs`: Maximum concurrent jobs for the worker (default: 10).
*   `--work_duration_seconds`: Duration of simulated work in seconds (default: 3.0).
*   `--job_timeout_milliseconds`: Job timeout in milliseconds (default: 30000).

### Other Scenarios

*   `stress`: Runs a heavy load test (100 instances, 50 concurrent jobs).
*   `load`: Similar to stress but with different defaults.
*   `multi`: Runs a comparison of all strategies with a single run each.

```bash
uv run demo/v2/job_worker_benchmark.py stress
```

## Key Concepts Demonstrated

*   **`JobWorker`**: The core class for processing jobs.
*   **Execution Strategies**:
    *   `async`: Uses Python's `asyncio` event loop. Best for I/O-bound tasks that use `async/await`.
    *   `thread`: Uses a `ThreadPoolExecutor`. Good for blocking I/O operations. **Note**: Subject to the Global Interpreter Lock (GIL), so not suitable for heavy CPU tasks.
    *   **`process`**: Uses a `ProcessPoolExecutor`. Essential for CPU-bound tasks to bypass the GIL. This benchmark demonstrates the "detached execution" pattern where the subprocess returns a result tuple instead of calling the client directly (which isn't picklable).
    *   `auto`: Automatically selects the best strategy based on the callback signature and hints.
*   **`ExecutionHint`**: Decorators (`@ExecutionHint.cpu_bound`, `@ExecutionHint.io_bound`) to guide the `auto` strategy.
*   **Workload Simulation**:
    *   `cpu`: Performs heavy arithmetic operations (list comprehensions) to hold the GIL and simulate real CPU-bound work.
    *   `io`: Simulates blocking file I/O.
    *   `subprocess`: Simulates calling external commands.
*   **Memory Tracking**: Monitoring memory usage during worker execution.

## Performance Notes

Recent benchmarks (Python 3.11 on macOS) comparing `process` vs `thread` strategies for CPU-bound workloads (3s duration, 50 instances) showed:

*   **Process Strategy**: ~30% faster throughput (2.35 jobs/s) and significantly lower memory usage (~96 MB). It successfully bypasses the GIL, allowing true parallelism across cores.
*   **Thread Strategy**: Slower throughput (1.79 jobs/s) and much higher memory usage (~1.3 GB). The GIL forces threads to execute sequentially for CPU tasks, and high object churn on a shared heap can lead to memory fragmentation.

**Recommendation**: Use `execution_strategy="process"` for any CPU-intensive job workers in Python.
