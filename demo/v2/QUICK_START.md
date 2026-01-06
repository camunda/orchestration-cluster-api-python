# Quick Start: Fast Validation Run

To validate that everything is working before running longer benchmarks:

## 1. Generate Fast Suite (15 scenarios)

```bash
python demo/v2/generate_benchmark_scenarios.py --suite fast --output scenarios_fast.json
```

**What it includes:**
- ✅ Baseline tests (3 strategies)
- ✅ Workload types (cpu, io, subprocess)
- ✅ Concurrency scaling (3 levels)
- ✅ Load scaling (3 levels)
- ✅ One interaction test
- ✅ One edge case
- ✅ One subprocess threading test

**Expected runtime: ~10-15 minutes**

## 2. Run Fast Suite

```bash
uv run demo/v2/run_benchmark_scenarios.py scenarios_fast.json \
  --output results_fast.json \
  --continue-on-error
```

## 3. Check Results

The runner will automatically show a summary. Look for:

```
✓ Completed: fast_baseline_async
  Duration: 15.2s
  Throughput: 0.33 jobs/sec

✓ Completed: fast_baseline_thread
  Duration: 14.8s
  Throughput: 0.34 jobs/sec
...

======================================================================
ALL SCENARIOS COMPLETE
======================================================================
Total scenarios: 15
Successful: 15
Failed: 0
```

## Suite Comparison

| Suite | Scenarios | Time | Use Case |
|-------|-----------|------|----------|
| **minimal** | 3 | ~1-2 min | Smoke test |
| **fast** | 15 | ~10-15 min | **Validation before long runs** |
| **quick** | 11 | ~5-10 min | Rapid iteration |
| **full** | 71 | ~2-4 hrs | Comprehensive analysis |

## Fast Suite Details

### Phase Breakdown

```
fast_baseline (3):        All strategies with CPU workload
fast_workload (3):        CPU, IO, subprocess with async
fast_concurrency (3):     1, 5, 20 concurrent jobs
fast_load (3):            5, 20, 50 instances
fast_interaction (1):     async + io + high concurrency
fast_edge (1):            100 instances stress test
fast_subprocess (1):      Threading safety test
```

### Key Parameters

All scenarios use:
- **Short work duration**: 0.2-0.5 seconds
- **No repeats**: `repeats=1` (single run)
- **Small instance counts**: 5-100 instances
- **Quick timeouts**: 30-60 seconds

## Troubleshooting

### If it fails immediately:
```bash
# Check Camunda connection
export CAMUNDA_BASE_URL="http://localhost:8080/v2"

# Test with just one scenario
uv run demo/v2/run_benchmark_scenarios.py scenarios_fast.json --limit 1
```

### If some scenarios fail:
```bash
# Continue running despite errors
uv run demo/v2/run_benchmark_scenarios.py scenarios_fast.json --continue-on-error
```

### If you want to test specific parts:
```bash
# Just baseline tests (~3 min)
uv run demo/v2/run_benchmark_scenarios.py scenarios_fast.json --phase fast_baseline

# Just workload tests (~3 min)
uv run demo/v2/run_benchmark_scenarios.py scenarios_fast.json --phase fast_workload
```

## Next Steps

Once the fast suite passes:

### Option 1: Run full suite
```bash
python demo/v2/generate_benchmark_scenarios.py --suite full --output scenarios.json
uv run demo/v2/run_benchmark_scenarios.py scenarios.json --continue-on-error
```

### Option 2: Target specific insights
```bash
# Deep dive into concurrency
uv run demo/v2/run_benchmark_scenarios.py scenarios.json --phase 3_concurrency_scaling

# Test edge cases
uv run demo/v2/run_benchmark_scenarios.py scenarios.json --phase 7_edge_cases
```

### Option 3: Create custom scenarios
Edit `scenarios_fast.json` to adjust parameters and re-run.

## Expected Output

Successful fast suite run shows:
- All 15 scenarios completed
- Mix of throughput values (0.1 - 5.0 jobs/sec depending on config)
- Memory usage tracked
- No errors or timeouts
- Results saved to JSON

This validates:
- ✅ Camunda connection works
- ✅ All strategies can execute jobs
- ✅ All workload types function
- ✅ Concurrency scaling works
- ✅ High load handling works
- ✅ Subprocess calls succeed
- ✅ No pickling errors
- ✅ Results collection works

You're now ready for longer benchmark runs!
