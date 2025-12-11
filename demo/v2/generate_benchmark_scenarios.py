#!/usr/bin/env python3
"""
Benchmark Scenario Generator

Generates a comprehensive suite of benchmark scenarios to explore performance tradeoffs
across different execution strategies, workload types, and configuration parameters.

Uses a hybrid approach combining:
1. Baseline comparisons
2. Systematic parameter sweeps
3. Key interaction effects
4. Edge case testing

Usage:
    python generate_benchmark_scenarios.py --output scenarios.json
    python generate_benchmark_scenarios.py --suite quick --output quick_scenarios.json
    python generate_benchmark_scenarios.py --suite full --csv scenarios.csv
"""

import argparse
import json
import csv
from pathlib import Path
from typing import Literal, TypedDict
from dataclasses import dataclass, asdict


class Scenario(TypedDict):
    """Type definition for a benchmark scenario."""
    name: str
    num_instances: int
    strategy: str
    workload_type: str
    work_duration: float
    max_concurrent_jobs: int
    repeats: int
    timeout: int
    job_timeout_ms: int
    description: str
    phase: str


@dataclass
class ScenarioParams:
    """Default parameters for scenario generation."""
    default_num_instances: int = 20
    default_work_duration: float = 1.0
    default_max_concurrent: int = 10
    default_repeats: int = 3
    default_timeout: int = 120
    default_job_timeout_ms: int = 30000


class BenchmarkScenarioGenerator:
    """Generator for comprehensive benchmark scenarios."""

    # Available parameter values
    STRATEGIES = ["async", "thread"]  # Skip "process" (broken) and "auto" (redundant)
    WORKLOAD_TYPES = ["cpu", "io", "subprocess"]
    CONCURRENCY_LEVELS = [1, 5, 10, 20, 50]
    LOAD_SIZES = [10, 20, 50, 100, 200]
    DURATIONS = [0.1, 0.5, 1.0, 2.0, 5.0]

    def __init__(self, params: ScenarioParams = None):
        self.params = params or ScenarioParams()
        self.scenarios = []

    def _add_scenario(
        self,
        name: str,
        phase: str,
        description: str,
        num_instances: int = None,
        strategy: str = "auto",
        workload_type: str = "cpu",
        work_duration: float = None,
        max_concurrent_jobs: int = None,
        repeats: int = None,
        timeout: int = None,
        job_timeout_ms: int = None,
    ):
        """Add a scenario with defaults filled in."""
        scenario: Scenario = {
            "name": name,
            "num_instances": num_instances or self.params.default_num_instances,
            "strategy": strategy,
            "workload_type": workload_type,
            "work_duration": work_duration or self.params.default_work_duration,
            "max_concurrent_jobs": max_concurrent_jobs or self.params.default_max_concurrent,
            "repeats": repeats or self.params.default_repeats,
            "timeout": timeout or self.params.default_timeout,
            "job_timeout_ms": job_timeout_ms or self.params.default_job_timeout_ms,
            "description": description,
            "phase": phase,
        }
        self.scenarios.append(scenario)

    def generate_phase1_baseline(self):
        """Phase 1: Baseline comparisons for all strategies with standard settings."""
        for strategy in self.STRATEGIES:
            self._add_scenario(
                name=f"baseline_{strategy}",
                phase="1_baseline",
                description=f"Baseline test for {strategy} strategy with standard CPU workload",
                strategy=strategy,
                workload_type="cpu",
                num_instances=10,
            )

    def generate_phase2_workload_matrix(self):
        """Phase 2: Test all workload types across key strategies."""
        for strategy in ["async", "thread"]:  # Focus on most viable strategies
            for workload in self.WORKLOAD_TYPES:
                self._add_scenario(
                    name=f"workload_{strategy}_{workload}",
                    phase="2_workload_types",
                    description=f"Test {workload} workload with {strategy} strategy",
                    strategy=strategy,
                    workload_type=workload,
                    num_instances=20,
                    work_duration=2.0,
                )

    def generate_phase3_concurrency_sweep(self):
        """Phase 3: How does each strategy scale with concurrency?"""
        for strategy in self.STRATEGIES:
            for concurrency in self.CONCURRENCY_LEVELS:
                self._add_scenario(
                    name=f"concurrency_{strategy}_{concurrency}",
                    phase="3_concurrency_scaling",
                    description=f"Test {strategy} with {concurrency} concurrent jobs",
                    strategy=strategy,
                    workload_type="cpu",
                    num_instances=50,
                    max_concurrent_jobs=concurrency,
                    timeout=180,  # More time for high concurrency
                )

    def generate_phase4_load_scaling(self):
        """Phase 4: How does each strategy handle increasing load?"""
        for strategy in self.STRATEGIES:
            for load in self.LOAD_SIZES:
                # Adjust timeout based on load
                timeout = 120 if load <= 50 else 240

                self._add_scenario(
                    name=f"load_{strategy}_{load}",
                    phase="4_load_scaling",
                    description=f"Test {strategy} with {load} process instances",
                    strategy=strategy,
                    workload_type="cpu",
                    num_instances=load,
                    max_concurrent_jobs=20,
                    timeout=timeout,
                )

    def generate_phase5_duration_impact(self):
        """Phase 5: Does work duration affect strategies differently?"""
        for strategy in ["async", "thread"]:
            for duration in self.DURATIONS:
                # Adjust timeout based on duration
                timeout = max(120, int(duration * 30))

                self._add_scenario(
                    name=f"duration_{strategy}_{duration}s",
                    phase="5_work_duration",
                    description=f"Test {strategy} with {duration}s work duration",
                    strategy=strategy,
                    workload_type="cpu",
                    num_instances=20,
                    work_duration=duration,
                    timeout=timeout,
                )

    def generate_phase6_interaction_effects(self):
        """Phase 6: Test key interactions (workload × concurrency × strategy)."""
        # Focus on meaningful interactions
        workloads = ["cpu", "io"]
        concurrency_levels = [1, 10, 50]
        strategies = ["async", "thread"]

        for workload in workloads:
            for concurrency in concurrency_levels:
                for strategy in strategies:
                    self._add_scenario(
                        name=f"interaction_{strategy}_{workload}_c{concurrency}",
                        phase="6_interactions",
                        description=f"Test interaction: {strategy} + {workload} workload + {concurrency} concurrent",
                        strategy=strategy,
                        workload_type=workload,
                        num_instances=30,
                        max_concurrent_jobs=concurrency,
                        work_duration=1.0,
                        timeout=180,
                    )

    def generate_phase7_edge_cases(self):
        """Phase 7: Edge cases and stress tests."""
        edge_cases = [
            {
                "name": "edge_single_job",
                "description": "Minimal case: single job with minimal concurrency",
                "num_instances": 1,
                "strategy": "async",
                "workload_type": "cpu",
                "work_duration": 1.0,
                "max_concurrent_jobs": 1,
                "repeats": 3,
            },
            {
                "name": "edge_massive_load",
                "description": "Stress test: 500 jobs with high concurrency",
                "num_instances": 500,
                "strategy": "auto",
                "workload_type": "cpu",
                "work_duration": 0.5,
                "max_concurrent_jobs": 50,
                "repeats": 1,  # Single run for stress test
                "timeout": 300,
            },
            {
                "name": "edge_bottleneck",
                "description": "Bottleneck test: high load with very low concurrency",
                "num_instances": 100,
                "strategy": "thread",
                "workload_type": "cpu",
                "work_duration": 1.0,
                "max_concurrent_jobs": 2,
                "timeout": 360,
            },
            {
                "name": "edge_long_duration",
                "description": "Long-running jobs test",
                "num_instances": 10,
                "strategy": "async",
                "workload_type": "io",
                "work_duration": 10.0,
                "max_concurrent_jobs": 5,
                "timeout": 240,
            },
            {
                "name": "edge_subprocess_stress",
                "description": "Stress test with subprocess workload",
                "num_instances": 50,
                "strategy": "thread",
                "workload_type": "subprocess",
                "work_duration": 2.0,
                "max_concurrent_jobs": 20,
                "timeout": 180,
            },
            {
                "name": "edge_high_concurrency_async",
                "description": "Async with very high concurrency",
                "num_instances": 100,
                "strategy": "async",
                "workload_type": "cpu",
                "work_duration": 0.5,
                "max_concurrent_jobs": 100,
                "timeout": 180,
            },
        ]

        for edge_case in edge_cases:
            self._add_scenario(
                phase="7_edge_cases",
                **edge_case
            )

    def generate_phase8_problematic_subprocess(self):
        """Phase 8: Test problematic subprocess workload (threading issues)."""
        for strategy in ["async", "thread"]:
            for concurrency in [5, 20]:
                self._add_scenario(
                    name=f"subprocess_threaded_{strategy}_c{concurrency}",
                    phase="8_subprocess_threading",
                    description=f"Test subprocess with threading issues: {strategy} with {concurrency} concurrent",
                    strategy=strategy,
                    workload_type="subprocess_threaded",
                    num_instances=20,
                    work_duration=1.0,
                    max_concurrent_jobs=concurrency,
                    timeout=180,
                )

    def generate_quick_suite(self):
        """Generate a quick test suite for rapid iteration (~10 scenarios)."""
        # Just baseline + one sweep
        self.generate_phase1_baseline()

        # Quick concurrency sweep with fewer data points
        for strategy in self.STRATEGIES:
            for concurrency in [1, 10, 50]:
                self._add_scenario(
                    name=f"quick_conc_{strategy}_{concurrency}",
                    phase="quick_concurrency",
                    description=f"Quick concurrency test: {strategy} with {concurrency} jobs",
                    strategy=strategy,
                    num_instances=20,
                    max_concurrent_jobs=concurrency,
                    repeats=1,  # Single run for speed
                )

        # Quick workload comparison
        for workload in ["cpu", "io"]:
            self._add_scenario(
                name=f"quick_workload_{workload}",
                phase="quick_workload",
                description=f"Quick workload test: {workload}",
                strategy="async",
                workload_type=workload,
                num_instances=10,
                repeats=1,
            )

    def generate_full_suite(self):
        """Generate the complete benchmark suite (~150-200 scenarios)."""
        self.generate_phase1_baseline()
        self.generate_phase2_workload_matrix()
        self.generate_phase3_concurrency_sweep()
        self.generate_phase4_load_scaling()
        self.generate_phase5_duration_impact()
        self.generate_phase6_interaction_effects()
        self.generate_phase7_edge_cases()
        self.generate_phase8_problematic_subprocess()

    def generate_minimal_suite(self):
        """Generate a minimal test suite for smoke testing (~2 scenarios)."""
        for strategy in self.STRATEGIES:
            self._add_scenario(
                name=f"smoke_{strategy}",
                phase="smoke_test",
                description=f"Smoke test for {strategy}",
                strategy=strategy,
                num_instances=5,
                work_duration=0.5,
                max_concurrent_jobs=5,
                repeats=1,
                timeout=30,
            )

    def generate_fast_suite(self):
        """Generate a fast validation suite with head-to-head comparisons (~20 scenarios, ~15-20 minutes).

        Tests key dimensions with both strategies for direct comparison.
        Perfect for validating that everything works before longer runs.
        """
        # Baseline - both strategies for cpu workload (2 scenarios)
        for strategy in self.STRATEGIES:
            self._add_scenario(
                name=f"fast_baseline_{strategy}",
                phase="fast_baseline",
                description=f"Fast baseline for {strategy}",
                strategy=strategy,
                workload_type="cpu",
                num_instances=5,
                work_duration=0.5,
                max_concurrent_jobs=5,
                repeats=1,
                timeout=30,
            )

        # IO workload - both strategies (2 scenarios)
        for strategy in self.STRATEGIES:
            self._add_scenario(
                name=f"fast_workload_io_{strategy}",
                phase="fast_workload",
                description=f"Fast test of io workload with {strategy}",
                strategy=strategy,
                workload_type="io",
                num_instances=5,
                work_duration=0.5,
                max_concurrent_jobs=5,
                repeats=1,
                timeout=30,
            )

        # Concurrency - both strategies with 2 levels for direct comparison (4 scenarios)
        for concurrency in [1, 20]:
            for strategy in self.STRATEGIES:
                self._add_scenario(
                    name=f"fast_conc_{concurrency}_{strategy}",
                    phase="fast_concurrency",
                    description=f"Fast concurrency test: {concurrency} jobs with {strategy}",
                    strategy=strategy,
                    workload_type="cpu",
                    num_instances=10,
                    work_duration=0.3,
                    max_concurrent_jobs=concurrency,
                    repeats=1,
                    timeout=30,
                )

        # Load scaling - both strategies with 2 levels (4 scenarios)
        for load in [20, 50]:
            for strategy in self.STRATEGIES:
                self._add_scenario(
                    name=f"fast_load_{load}_{strategy}",
                    phase="fast_load",
                    description=f"Fast load test: {load} instances with {strategy}",
                    strategy=strategy,
                    workload_type="cpu",
                    num_instances=load,
                    work_duration=0.3,
                    max_concurrent_jobs=10,
                    repeats=1,
                    timeout=60,
                )

        # High concurrency with high load - both strategies (2 scenarios)
        for strategy in self.STRATEGIES:
            self._add_scenario(
                name=f"fast_interaction_{strategy}",
                phase="fast_interaction",
                description=f"Fast interaction: high concurrency + high load with {strategy}",
                strategy=strategy,
                workload_type="cpu",
                num_instances=50,
                work_duration=0.2,
                max_concurrent_jobs=20,
                repeats=1,
                timeout=60,
            )

        # Subprocess workload - async only (1 scenario)
        self._add_scenario(
            name="fast_subprocess",
            phase="fast_subprocess",
            description="Fast subprocess workload test",
            strategy="async",
            workload_type="subprocess",
            num_instances=5,
            work_duration=0.5,
            max_concurrent_jobs=5,
            repeats=1,
            timeout=30,
        )

        # Subprocess threading - thread only (1 scenario)
        self._add_scenario(
            name="fast_subprocess_threaded",
            phase="fast_subprocess",
            description="Fast subprocess threading test",
            strategy="thread",
            workload_type="subprocess_threaded",
            num_instances=5,
            work_duration=0.5,
            max_concurrent_jobs=5,
            repeats=1,
            timeout=30,
        )

    def get_scenarios(self) -> list[Scenario]:
        """Get all generated scenarios."""
        return self.scenarios

    def get_summary(self) -> dict:
        """Get a summary of generated scenarios."""
        phases = {}
        for scenario in self.scenarios:
            phase = scenario["phase"]
            if phase not in phases:
                phases[phase] = 0
            phases[phase] += 1

        strategies = {}
        for scenario in self.scenarios:
            strategy = scenario["strategy"]
            if strategy not in strategies:
                strategies[strategy] = 0
            strategies[strategy] += 1

        return {
            "total_scenarios": len(self.scenarios),
            "scenarios_by_phase": phases,
            "scenarios_by_strategy": strategies,
        }


def save_to_json(scenarios: list[Scenario], filepath: str):
    """Save scenarios to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(scenarios, f, indent=2)
    print(f"✓ Saved {len(scenarios)} scenarios to {filepath}")


def save_to_csv(scenarios: list[Scenario], filepath: str):
    """Save scenarios to CSV file."""
    if not scenarios:
        print("No scenarios to save")
        return

    fieldnames = scenarios[0].keys()
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scenarios)
    print(f"✓ Saved {len(scenarios)} scenarios to {filepath}")


def print_summary(generator: BenchmarkScenarioGenerator):
    """Print a summary of generated scenarios."""
    summary = generator.get_summary()

    print("\n" + "="*70)
    print("BENCHMARK SCENARIO SUITE SUMMARY")
    print("="*70)
    print(f"Total Scenarios: {summary['total_scenarios']}")

    print("\nScenarios by Phase:")
    for phase, count in sorted(summary['scenarios_by_phase'].items()):
        print(f"  {phase:30} {count:4} scenarios")

    print("\nScenarios by Strategy:")
    for strategy, count in sorted(summary['scenarios_by_strategy'].items()):
        print(f"  {strategy:30} {count:4} scenarios")

    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate benchmark scenarios for Camunda job worker testing"
    )
    parser.add_argument(
        "--suite",
        choices=["minimal", "fast", "quick", "full"],
        default="full",
        help="Suite size to generate (default: full)"
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: scenarios/<suite>.json)"
    )
    parser.add_argument(
        "--csv",
        help="Also save as CSV to this file path"
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress summary output"
    )

    args = parser.parse_args()

    # Generate scenarios
    generator = BenchmarkScenarioGenerator()

    if args.suite == "minimal":
        generator.generate_minimal_suite()
    elif args.suite == "fast":
        generator.generate_fast_suite()
    elif args.suite == "quick":
        generator.generate_quick_suite()
    else:  # full
        generator.generate_full_suite()

    scenarios = generator.get_scenarios()

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        # Default to scenarios/<suite>.json
        script_dir = Path(__file__).parent
        scenarios_dir = script_dir / "scenarios"
        scenarios_dir.mkdir(exist_ok=True)
        output_path = str(scenarios_dir / f"{args.suite}.json")

    # Save to JSON
    save_to_json(scenarios, output_path)

    # Optionally save to CSV
    if args.csv:
        save_to_csv(scenarios, args.csv)

    # Print summary
    if not args.quiet:
        print_summary(generator)


if __name__ == "__main__":
    main()
