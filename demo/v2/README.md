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

## Advanced: Systematic Benchmarking

For comprehensive performance analysis, use the scenario generator and runner:

### 1. Generate Benchmark Scenarios

```bash
# Minimal suite (2 scenarios, ~1 minute) - smoke test
python demo/v2/generate_benchmark_scenarios.py --suite minimal

# Fast suite (16 scenarios, ~15-20 minutes) - RECOMMENDED for validation
python demo/v2/generate_benchmark_scenarios.py --suite fast

# Quick suite (10 scenarios, ~5-10 minutes) - rapid iteration
python demo/v2/generate_benchmark_scenarios.py --suite quick

# Full suite (60 scenarios, ~2-4 hours) - comprehensive analysis
python demo/v2/generate_benchmark_scenarios.py --suite full

# Custom output location
python demo/v2/generate_benchmark_scenarios.py --suite fast --output custom_path.json
```

Scenarios are saved to `demo/v2/scenarios/<suite>.json` by default.

**First time?** Use the **fast** suite to validate everything works! See [QUICK_START.md](QUICK_START.md).

### 2. Run Benchmark Suite

```bash
# Run scenarios (results saved to demo/v2/results/<suite>_<timestamp>.json)
uv run demo/v2/run_benchmark_scenarios.py demo/v2/scenarios/fast.json

# Custom output location
uv run demo/v2/run_benchmark_scenarios.py demo/v2/scenarios/fast.json --output custom_results.json

# Continue on errors (recommended for full suite)
uv run demo/v2/run_benchmark_scenarios.py demo/v2/scenarios/fast.json --continue-on-error

# Prevent sleep during long runs
# macOS:
caffeinate -i uv run demo/v2/run_benchmark_scenarios.py demo/v2/scenarios/full.json

# Linux:
systemd-inhibit uv run demo/v2/run_benchmark_scenarios.py demo/v2/scenarios/full.json
```

See [BENCHMARK_GUIDE.md](BENCHMARK_GUIDE.md) for complete documentation on systematic benchmarking.

### Benchmark Suite Structure

The scenario generator creates 8 phases of tests:

| Phase | Scenarios | Purpose |
|-------|-----------|---------|
| Baseline | 3 | Establish baseline performance |
| Workload Types | 6 | Best strategy for each workload |
| Concurrency Scaling | 15 | How strategies scale |
| Load Scaling | 15 | Breaking points under load |
| Work Duration | 10 | Duration sensitivity |
| Interactions | 12 | Combined effects |
| Edge Cases | 6 | Extreme conditions |
| Subprocess Threading | 4 | Fork-safety testing |

### Files

- `job_worker_benchmark.py` - Core benchmark tool
- `generate_benchmark_scenarios.py` - Scenario generator (**Strategy 4: Hybrid Approach**)
- `run_benchmark_scenarios.py` - Scenario execution runner
- `BENCHMARK_GUIDE.md` - Detailed benchmarking documentation

## Performance Notes

Recent benchmarks (Python 3.11 on macOS) comparing `process` vs `thread` strategies for CPU-bound workloads (3s duration, 50 instances) showed:

*   **Process Strategy**: ~30% faster throughput (2.35 jobs/s) and significantly lower memory usage (~96 MB). It successfully bypasses the GIL, allowing true parallelism across cores.
*   **Thread Strategy**: Slower throughput (1.79 jobs/s) and much higher memory usage (~1.3 GB). The GIL forces threads to execute sequentially for CPU tasks, and high object churn on a shared heap can lead to memory fragmentation.

**Recommendation**: Use `execution_strategy="process"` for any CPU-intensive job workers in Python.
