#!/bin/bash
# Quick validation run - tests that everything works in ~10-15 minutes

set -e

echo "=================================================="
echo "Fast Validation Run"
echo "=================================================="
echo ""
echo "This will:"
echo "  1. Generate 16 test scenarios"
echo "  2. Run them against your Camunda instance"
echo "  3. Take ~15-20 minutes"
echo ""
echo "Note: Ensure your computer won't sleep during the run"
echo "  macOS: caffeinate -i bash demo/v2/run_fast_validation.sh"
echo "  Linux: systemd-inhibit bash demo/v2/run_fast_validation.sh"
echo ""
echo "Press Ctrl+C to cancel, or wait 3 seconds to start..."
sleep 3

echo ""
echo "Step 1/2: Generating fast scenario suite..."
python demo/v2/generate_benchmark_scenarios.py --suite fast --quiet

echo ""
echo "Step 2/2: Running scenarios..."
uv run demo/v2/run_benchmark_scenarios.py demo/v2/scenarios/fast.json --continue-on-error

echo ""
echo "=================================================="
echo "✓ Validation Complete!"
echo "=================================================="
echo ""
echo "Results saved to: demo/v2/results/fast_<timestamp>.json"
echo ""
echo "Next steps:"
echo "  - Review the latest file in demo/v2/results/ for performance metrics"
echo "  - If successful, run full suite: python demo/v2/generate_benchmark_scenarios.py --suite full"
echo ""
