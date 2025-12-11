#!/usr/bin/env python3
"""
Benchmark Scenario Runner

Executes benchmark scenarios from a JSON file and collects results.

Usage:
    uv run demo/v2/run_benchmark_scenarios.py scenarios.json
    uv run demo/v2/run_benchmark_scenarios.py scenarios.json --output results.json
    uv run demo/v2/run_benchmark_scenarios.py scenarios.json --continue-on-error
"""

import argparse
import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Import from the benchmark module
try:
    from job_worker_benchmark import run_test, make_client
except ImportError:
    # If running as script, add parent directory to path
    sys.path.insert(0, str(Path(__file__).parent))
    from job_worker_benchmark import run_test, make_client


class BenchmarkRunner:
    """Runs benchmark scenarios and collects results."""

    def __init__(self, scenarios_file: str, output_file: str = None, continue_on_error: bool = False):
        self.scenarios_file = scenarios_file

        # Default output file based on input file if not specified
        if output_file:
            self.output_file = output_file
        else:
            # If input is scenarios/<suite>.json, output to scenarios/results_<suite>.json
            scenarios_path = Path(scenarios_file)
            if scenarios_path.parent.name == "scenarios":
                self.output_file = str(scenarios_path.parent / f"results_{scenarios_path.name}")
            else:
                self.output_file = "benchmark_results.json"
        self.continue_on_error = continue_on_error
        self.results = []
        self.failed_scenarios = []

    def load_scenarios(self) -> list[dict]:
        """Load scenarios from JSON file."""
        with open(self.scenarios_file, 'r') as f:
            scenarios = json.load(f)
        print(f"✓ Loaded {len(scenarios)} scenarios from {self.scenarios_file}")
        return scenarios

    async def run_scenario(self, scenario: dict) -> dict:
        """Run a single benchmark scenario."""
        start_time = time.time()

        print(f"\n{'='*70}")
        print(f"Running: {scenario['name']}")
        print(f"Phase: {scenario['phase']}")
        print(f"Description: {scenario['description']}")
        print(f"{'='*70}")

        try:
            # Run the benchmark test
            result = await run_test(
                num_instances=scenario['num_instances'],
                strategy=scenario['strategy'],
                workload_type=scenario['workload_type'],
                repeats=scenario['repeats'],
                max_concurrent_jobs=scenario['max_concurrent_jobs'],
                timeout=scenario['timeout'],
                work_duration=scenario['work_duration'],
                job_timeout_ms=scenario['job_timeout_ms'],
            )

            elapsed_time = time.time() - start_time

            # Combine scenario config with results
            full_result = {
                **scenario,
                **result,
                "status": "success",
                "elapsed_time": elapsed_time,
                "timestamp": datetime.now().isoformat(),
            }

            print(f"\n✓ Completed: {scenario['name']}")
            print(f"  Duration: {elapsed_time:.1f}s")

            if 'jobs_per_second_avg' in result:
                print(f"  Throughput: {result['jobs_per_second_avg']:.2f} jobs/sec")
            elif 'jobs_per_second' in result:
                print(f"  Throughput: {result['jobs_per_second']:.2f} jobs/sec")

            return full_result

        except Exception as e:
            elapsed_time = time.time() - start_time

            error_result = {
                **scenario,
                "status": "failed",
                "error": str(e),
                "error_type": type(e).__name__,
                "elapsed_time": elapsed_time,
                "timestamp": datetime.now().isoformat(),
            }

            print(f"\n✗ Failed: {scenario['name']}")
            print(f"  Error: {e}")

            if not self.continue_on_error:
                raise

            self.failed_scenarios.append(scenario['name'])
            return error_result

    async def run_all_scenarios(self, scenarios: list[dict]):
        """Run all scenarios sequentially."""
        total = len(scenarios)

        for i, scenario in enumerate(scenarios, 1):
            print(f"\n\n{'#'*70}")
            print(f"# Scenario {i}/{total}")
            print(f"{'#'*70}")

            result = await self.run_scenario(scenario)
            self.results.append(result)

            # Save intermediate results
            self.save_results()

        print(f"\n\n{'='*70}")
        print("ALL SCENARIOS COMPLETE")
        print(f"{'='*70}")
        print(f"Total scenarios: {total}")
        print(f"Successful: {total - len(self.failed_scenarios)}")
        print(f"Failed: {len(self.failed_scenarios)}")

        if self.failed_scenarios:
            print(f"\nFailed scenarios:")
            for name in self.failed_scenarios:
                print(f"  - {name}")

    def save_results(self):
        """Save results to JSON file."""
        with open(self.output_file, 'w') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "scenarios_file": self.scenarios_file,
                "total_scenarios": len(self.results),
                "failed_count": len(self.failed_scenarios),
                "failed_scenarios": self.failed_scenarios,
                "results": self.results,
            }, f, indent=2)

        print(f"✓ Saved results to {self.output_file}")

    def generate_summary_report(self):
        """Generate a comprehensive performance comparison across strategies."""
        if not self.results:
            print("No results to summarize")
            return

        print(f"\n\n{'='*120}")
        print("STRATEGY COMPARISON: HEAD-TO-HEAD PERFORMANCE")
        print(f"{'='*120}\n")

        success_results = [r for r in self.results if r['status'] == 'success' and ('jobs_per_second' in r or 'jobs_per_second_avg' in r)]

        if not success_results:
            print("No successful results to analyze")
            return

        # Group by unique test conditions (workload + instances + concurrency)
        test_conditions = {}
        for result in success_results:
            # Create a key for unique test condition
            workload = result.get('workload_type', 'cpu')
            instances = result.get('num_instances', 0)
            concurrency = result.get('max_concurrent_jobs', 0)
            duration = result.get('work_duration', 0)

            key = (workload, instances, concurrency, duration)

            if key not in test_conditions:
                test_conditions[key] = []

            test_conditions[key].append(result)

        # Print comparison for each test condition
        print(f"{'Workload':12} {'Instances':>10} {'Concurrency':>12} {'Duration':>10} | {'async':>12} {'thread':>12} | {'Winner':>10} {'Margin':>10}")
        print("-" * 120)

        summary_stats = {'async': {'wins': 0, 'total': 0}, 'thread': {'wins': 0, 'total': 0}}

        for (workload, instances, concurrency, duration), results in sorted(test_conditions.items()):
            # Group by strategy
            by_strategy = {}
            for r in results:
                strategy = r['strategy']
                throughput = r.get('jobs_per_second_avg', r.get('jobs_per_second', 0))

                if strategy not in by_strategy:
                    by_strategy[strategy] = []
                by_strategy[strategy].append(throughput)

            # Calculate average for each strategy
            strategy_avgs = {}
            for strategy, throughputs in by_strategy.items():
                strategy_avgs[strategy] = sum(throughputs) / len(throughputs) if throughputs else 0

            # Determine winner
            async_val = strategy_avgs.get('async', 0)
            thread_val = strategy_avgs.get('thread', 0)

            winner = ""
            margin = ""

            if async_val > 0 and thread_val > 0:
                if async_val > thread_val:
                    winner = "async"
                    margin_pct = ((async_val - thread_val) / thread_val) * 100
                    margin = f"+{margin_pct:.1f}%"
                    summary_stats['async']['wins'] += 1
                elif thread_val > async_val:
                    winner = "thread"
                    margin_pct = ((thread_val - async_val) / async_val) * 100
                    margin = f"+{margin_pct:.1f}%"
                    summary_stats['thread']['wins'] += 1
                else:
                    winner = "tie"
                    margin = "0%"

                summary_stats['async']['total'] += 1
                summary_stats['thread']['total'] += 1
            elif async_val > 0:
                winner = "async"
                margin = "only"
                summary_stats['async']['total'] += 1
            elif thread_val > 0:
                winner = "thread"
                margin = "only"
                summary_stats['thread']['total'] += 1

            # Format values
            async_str = f"{async_val:.2f} j/s" if async_val > 0 else "-"
            thread_str = f"{thread_val:.2f} j/s" if thread_val > 0 else "-"

            print(f"{workload:12} {instances:10} {concurrency:12} {duration:10.1f}s | {async_str:>12} {thread_str:>12} | {winner:>10} {margin:>10}")

        # Print summary
        print(f"\n{'='*120}")
        print("OVERALL SUMMARY")
        print(f"{'='*120}\n")

        for strategy in ['async', 'thread']:
            stats = summary_stats[strategy]
            if stats['total'] > 0:
                win_rate = (stats['wins'] / stats['total']) * 100
                print(f"{strategy:8} - {stats['wins']}/{stats['total']} wins ({win_rate:.1f}% win rate)")



async def main():
    parser = argparse.ArgumentParser(
        description="Run benchmark scenarios from a JSON file"
    )
    parser.add_argument(
        "scenarios",
        help="Path to scenarios JSON file"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="benchmark_results.json",
        help="Output file for results (default: benchmark_results.json)"
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue running even if a scenario fails"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Only run first N scenarios (for testing)"
    )
    parser.add_argument(
        "--phase",
        help="Only run scenarios from a specific phase"
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Skip summary report generation"
    )

    args = parser.parse_args()

    # Create runner
    runner = BenchmarkRunner(
        scenarios_file=args.scenarios,
        output_file=args.output,
        continue_on_error=args.continue_on_error,
    )

    # Load scenarios
    scenarios = runner.load_scenarios()

    # Filter scenarios if requested
    if args.phase:
        scenarios = [s for s in scenarios if s['phase'] == args.phase]
        print(f"✓ Filtered to {len(scenarios)} scenarios in phase '{args.phase}'")

    if args.limit:
        scenarios = scenarios[:args.limit]
        print(f"✓ Limited to first {len(scenarios)} scenarios")

    if not scenarios:
        print("No scenarios to run!")
        return

    # Run all scenarios
    start_time = time.time()
    await runner.run_all_scenarios(scenarios)
    total_time = time.time() - start_time

    # Save final results
    runner.save_results()

    # Generate summary
    if not args.no_summary:
        runner.generate_summary_report()

    print(f"\nTotal execution time: {total_time/60:.1f} minutes")


if __name__ == "__main__":
    asyncio.run(main())
