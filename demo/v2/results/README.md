# Benchmark Results Directory

This directory contains timestamped benchmark results from scenario runs.

## File Naming

Results are automatically named with timestamps:
- `fast_20231215_143022.json` - Fast suite run on Dec 15, 2023 at 14:30:22
- `full_20231215_150000.json` - Full suite run on Dec 15, 2023 at 15:00:00
- `quick_20231215_120000.json` - Quick suite run on Dec 15, 2023 at 12:00:00

## Contents

Each result file contains:
- **Metadata**: Timestamp, scenarios file, total scenarios
- **Results**: Detailed metrics for each scenario (throughput, timing, memory)
- **Failed Scenarios**: List of any scenarios that failed
- **Summary Report**: Head-to-head comparison tables printed to console

## Usage

### View Latest Results
```bash
# List results by date
ls -lt demo/v2/results/

# View latest result
cat demo/v2/results/fast_*.json | jq
```

### Compare Results
```bash
# Compare two runs
diff <(jq '.results' demo/v2/results/fast_20231215_143022.json) \
     <(jq '.results' demo/v2/results/fast_20231215_150000.json)
```

## Git Tracking

All result files (`*.json`) are ignored by git to keep results local.
Share scenario definitions from `../scenarios/` instead.
