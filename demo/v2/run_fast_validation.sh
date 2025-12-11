#!/bin/bash
# Quick validation run - tests that everything works in ~10-15 minutes

set -e

echo "=================================================="
echo "Fast Validation Run"
echo "=================================================="
echo ""
echo "This will:"
echo "  1. Generate 15 test scenarios"
echo "  2. Run them against your Camunda instance"
echo "  3. Take ~10-15 minutes"
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
echo "Results saved to: demo/v2/scenarios/results_fast.json"
echo ""
echo "Next steps:"
echo "  - Review demo/v2/scenarios/results_fast.json for performance metrics"
echo "  - If successful, run full suite: python demo/v2/generate_benchmark_scenarios.py --suite full"
echo ""
