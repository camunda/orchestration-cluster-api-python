# Job Worker Benchmark Guide

Comprehensive benchmarking system for testing Camunda job worker performance across different execution strategies, workload types, and configurations.

## Quick Start

### 1. Generate Scenarios

```bash
# Minimal suite (3 scenarios, ~1 minute)
python demo/v2/generate_benchmark_scenarios.py --suite minimal --output scenarios_minimal.json

# Quick suite (11 scenarios, ~5 minutes)
python demo/v2/generate_benchmark_scenarios.py --suite quick --output scenarios_quick.json

# Full suite (71 scenarios, ~2-3 hours)
python demo/v2/generate_benchmark_scenarios.py --suite full --output scenarios_full.json

# Full suite with CSV export
python demo/v2/generate_benchmark_scenarios.py --suite full --output scenarios.json --csv scenarios.csv
```

### 2. Run Benchmarks

```bash
# Run all scenarios
python demo/v2/run_benchmark_scenarios.py scenarios.json --output results.json

# Run only first 5 scenarios (for testing)
python demo/v2/run_benchmark_scenarios.py scenarios.json --limit 5

# Run only specific phase
python demo/v2/run_benchmark_scenarios.py scenarios.json --phase 1_baseline

# Continue on errors
python demo/v2/run_benchmark_scenarios.py scenarios.json --continue-on-error
```

### 3. Run Individual Tests

You can also run individual tests directly:

```bash
# Run a single test
uv run demo/v2/job_worker_benchmark.py test \
  --process_instances 20 \
  --worker_strategy async \
  --workload_type cpu \
  --work_duration_seconds 1.0 \
  --max_concurrent_jobs 10

# Run pre-defined benchmark suites
uv run demo/v2/job_worker_benchmark.py benchmark-workloads --process_instances 20
uv run demo/v2/job_worker_benchmark.py benchmark --process_instances 20
```

## Benchmark Suite Structure

The full benchmark suite is organized into 8 phases:

### Phase 1: Baseline (3 scenarios)
- Tests all strategies (async, thread, auto) with standard CPU workload
- **Purpose**: Establish baseline performance for each strategy

### Phase 2: Workload Types (6 scenarios)
- Tests CPU, I/O, and subprocess workloads with async and thread strategies
- **Purpose**: Identify which strategy handles which workload type best

### Phase 3: Concurrency Scaling (15 scenarios)
- Tests all strategies with 1, 5, 10, 20, 50 concurrent jobs
- **Purpose**: Understand how strategies scale with concurrency

### Phase 4: Load Scaling (15 scenarios)
- Tests all strategies with 10, 20, 50, 100, 200 process instances
- **Purpose**: Find breaking points and optimal load handling

### Phase 5: Work Duration (10 scenarios)
- Tests async and thread with work durations: 0.1s, 0.5s, 1.0s, 2.0s, 5.0s
- **Purpose**: Determine if work duration affects strategy performance

### Phase 6: Interaction Effects (12 scenarios)
- Tests combinations of: workload type × concurrency × strategy
- **Purpose**: Identify important interaction effects

### Phase 7: Edge Cases (6 scenarios)
- Single job, massive load (500 jobs), bottleneck, long duration, subprocess stress, high async concurrency
- **Purpose**: Test extreme conditions and edge cases

### Phase 8: Subprocess Threading (4 scenarios)
- Tests the problematic subprocess_threaded workload
- **Purpose**: Expose fork-safety issues with subprocess + threading

## Key Parameters

### Execution Strategies
- **`async`**: Pure async/await, best for I/O-bound work
- **`thread`**: ThreadPoolExecutor, good for mixed workloads
- **`auto`**: Automatic strategy selection based on hints
- **`process`**: ProcessPoolExecutor (currently broken due to pickling issues)

### Workload Types
- **`cpu`**: CPU-intensive busy loop
- **`io`**: I/O-bound file operations
- **`subprocess`**: External subprocess calls (sleep command)
- **`subprocess_threaded`**: Subprocess with internal threading (tests fork safety)

### Configuration Parameters
- **`num_instances`**: Number of process instances to create (= number of jobs)
- **`max_concurrent_jobs`**: Maximum number of jobs executing concurrently
- **`work_duration`**: Duration of simulated work in seconds
- **`repeats`**: Number of times to repeat test (for statistical significance)
- **`timeout`**: Maximum time to wait for all jobs to complete

## Performance Metrics

Each benchmark scenario captures:

- **`jobs_per_second`**: Throughput (jobs completed per second)
- **`total_time`**: Total time to complete all jobs
- **`jobs_completed`**: Number of jobs successfully completed
- **`memory_peak_mb`**: Peak Python memory usage
- **`max_rss_mb`**: Maximum resident set size (total process memory)
- **`rss_delta_mb`**: Change in RSS memory during test

## Analyzing Results

### View Summary Report

The runner automatically generates a summary report showing:
- Results grouped by phase
- Top performers by throughput
- Best strategy for each workload type

### Manual Analysis

Results are saved in JSON format:

```python
import json
import pandas as pd

# Load results
with open('results.json') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data['results'])

# Filter successful runs
success = df[df['status'] == 'success']

# Compare strategies
success.pivot_table(
    values='jobs_per_second_avg',
    index='workload_type',
    columns='strategy',
    aggfunc='mean'
)

# Find best configuration for high load
high_load = success[success['num_instances'] >= 100]
high_load.nlargest(5, 'jobs_per_second_avg')[['name', 'strategy', 'jobs_per_second_avg']]
```

## Key Questions Answered

The benchmark suite helps answer:

1. **Which strategy is fastest for CPU-bound work?**
   - Look at Phase 1 baseline + Phase 2 CPU workload results

2. **How does concurrency affect throughput?**
   - Analyze Phase 3 concurrency scaling results

3. **What's the optimal max_concurrent_jobs setting?**
   - Find the "knee" in the concurrency curve (diminishing returns)

4. **Does async or thread handle I/O better?**
   - Compare Phase 2 results for I/O workload

5. **What happens under extreme load?**
   - Check Phase 7 edge cases (especially massive_load scenario)

6. **Are there subprocess threading issues?**
   - Review Phase 8 subprocess_threaded results for errors/warnings

## Custom Scenarios

You can create custom scenario files:

```json
[
  {
    "name": "custom_test",
    "num_instances": 50,
    "strategy": "async",
    "workload_type": "cpu",
    "work_duration": 2.0,
    "max_concurrent_jobs": 25,
    "repeats": 3,
    "timeout": 120,
    "job_timeout_ms": 30000,
    "description": "Custom scenario for testing X",
    "phase": "custom"
  }
]
```

Then run:
```bash
python demo/v2/run_benchmark_scenarios.py custom_scenarios.json
```

## Performance Tips

1. **Use `--limit` for quick testing**: Test your setup with `--limit 3` before running full suite
2. **Run overnight**: Full suite takes 2-3 hours
3. **Use `--continue-on-error`**: Don't let one failure stop the entire suite
4. **Save intermediate results**: Runner saves after each scenario
5. **Filter by phase**: Use `--phase` to run specific sections

## Troubleshooting

### Camunda Connection Issues
```bash
# Set Camunda URL
export CAMUNDA_BASE_URL="http://localhost:8080/v2"
```

### Timeouts
- Increase `timeout` in scenario files for slow environments
- Check Camunda broker health

### Memory Issues
- Reduce `num_instances` or `max_concurrent_jobs`
- Monitor with `top` or `htop` during runs

### Process Strategy Errors
The `process` strategy currently doesn't work due to pickling issues with the `ActivatedJob` containing unpicklable `CamundaClient`. Stick with `async`, `thread`, or `auto`.

## Example Workflow

```bash
# 1. Generate scenarios
python demo/v2/generate_benchmark_scenarios.py --suite full --output scenarios.json --csv scenarios.csv

# 2. Test with first 5 scenarios
python demo/v2/run_benchmark_scenarios.py scenarios.json --limit 5 --output test_results.json

# 3. If successful, run full suite
python demo/v2/run_benchmark_scenarios.py scenarios.json --output full_results.json --continue-on-error

# 4. Analyze specific phase
python demo/v2/run_benchmark_scenarios.py scenarios.json --phase 3_concurrency_scaling --output concurrency_results.json

# 5. Review results
cat full_results.json | jq '.results[] | select(.status == "success") | {name, strategy, jobs_per_second_avg}'
```

## Contributing

To add new phases or scenarios:

1. Edit `generate_benchmark_scenarios.py`
2. Add a new `generate_phaseX_xxx()` method
3. Call it from `generate_full_suite()`
4. Test with `--suite full`

## References

- Main benchmark script: [`job_worker_benchmark.py`](job_worker_benchmark.py)
- Scenario generator: [`generate_benchmark_scenarios.py`](generate_benchmark_scenarios.py)
- Scenario runner: [`run_benchmark_scenarios.py`](run_benchmark_scenarios.py)
