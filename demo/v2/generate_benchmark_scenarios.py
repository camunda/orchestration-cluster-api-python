#!/usr/bin/env python3
"""
Benchmark Scenario Generator

Generates a comprehensive suite of benchmark scenarios to explore performance tradeoffs
across different execution strategies, workload types, and configuration parameters.

Refactored to focus on three key goals:
1. Baselines: Establish performance baselines for regression testing.
2. Envelope: Evaluate the performance envelope across strategies and workloads.
3. Safety: Discover gotchas and deadlocks (e.g., fork safety).

Usage:
    python generate_benchmark_scenarios.py --suite full --output scenarios.json
    python generate_benchmark_scenarios.py --suite baseline --output baseline.json
    python generate_benchmark_scenarios.py --suite envelope --output envelope.json
    python generate_benchmark_scenarios.py --suite safety --output safety.json
"""

import argparse
import json
import csv
import itertools
from pathlib import Path
from typing import Literal, TypedDict, List, Any
from dataclasses import dataclass


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

    # Updated to include 'process' strategy and 'subprocess_threaded' workload
    STRATEGIES = ["async", "thread", "process"]
    WORKLOAD_TYPES = ["cpu", "io", "subprocess", "subprocess_threaded"]
    
    # Parameter ranges for Envelope Suite
    CONCURRENCY_LEVELS = [1, 10, 50]
    LOAD_SIZES = [20, 100]
    DURATIONS = [0.1, 1.0, 5.0]

    def __init__(self, params: ScenarioParams = None):
        self.params = params or ScenarioParams()
        self.scenarios: List[Scenario] = []

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

    def generate_baseline_suite(self):
        """
        Goal 1: Establish performance baselines.
        
        A static set of "golden path" scenarios to measure the effect of refactoring.
        These should be stable and representative of common usage.
        """
        phase = "1_baseline"
        
        # 1. Async CPU (Standard high-throughput baseline)
        self._add_scenario(
            name="baseline_async_cpu",
            phase=phase,
            description="Baseline: Async strategy with CPU workload",
            strategy="async",
            workload_type="cpu",
            num_instances=50,
            max_concurrent_jobs=20,
            work_duration=0.5,
            repeats=5  # More repeats for stable baseline
        )

        # 2. Thread IO (Standard blocking I/O baseline)
        self._add_scenario(
            name="baseline_thread_io",
            phase=phase,
            description="Baseline: Thread strategy with IO workload",
            strategy="thread",
            workload_type="io",
            num_instances=50,
            max_concurrent_jobs=20,
            work_duration=0.5,
            repeats=5
        )

        # 3. Process CPU (Standard parallelism baseline)
        self._add_scenario(
            name="baseline_process_cpu",
            phase=phase,
            description="Baseline: Process strategy with CPU workload",
            strategy="process",
            workload_type="cpu",
            num_instances=50,
            max_concurrent_jobs=10, # Lower concurrency for processes
            work_duration=0.5,
            repeats=5
        )

    def generate_envelope_suite(self):
        """
        Goal 2: Evaluate the performance envelope.
        
        Sweep across strategies, workloads, and parameters to guide default design
        and user configuration.
        """
        phase = "2_envelope"
        
        # Cartesian product of main factors
        # We limit the combinations to avoid explosion, but cover the edges
        
        for strategy in self.STRATEGIES:
            for workload in self.WORKLOAD_TYPES:
                
                # Skip nonsensical/redundant combinations if necessary
                # e.g., async + cpu is known to block, but useful to measure HOW BAD it is.
                
                # Sweep Concurrency
                for concurrency in self.CONCURRENCY_LEVELS:
                    self._add_scenario(
                        name=f"env_{strategy}_{workload}_c{concurrency}",
                        phase=f"{phase}_concurrency",
                        description=f"Envelope: {strategy}/{workload} at {concurrency} concurrency",
                        strategy=strategy,
                        workload_type=workload,
                        max_concurrent_jobs=concurrency,
                        num_instances=max(20, concurrency * 2), # Ensure enough work
                        work_duration=1.0,
                        repeats=3
                    )

                # Sweep Duration (at fixed concurrency)
                for duration in self.DURATIONS:
                    if duration == 1.0: continue # Already covered above
                    self._add_scenario(
                        name=f"env_{strategy}_{workload}_d{duration}s",
                        phase=f"{phase}_duration",
                        description=f"Envelope: {strategy}/{workload} with {duration}s duration",
                        strategy=strategy,
                        workload_type=workload,
                        max_concurrent_jobs=10,
                        num_instances=20,
                        work_duration=duration,
                        repeats=3,
                        timeout=max(120, int(duration * 30))
                    )

    def generate_safety_suite(self):
        """
        Goal 3: Discover gotchas and deadlocks.
        
        Targeted scenarios for known or suspected issues, like fork safety
        with threads and subprocesses.
        """
        phase = "3_safety"
        
        # 1. The "Fork Safety" Trap
        # Mixing threads (in the worker) with subprocesses (in the workload)
        # especially when the subprocess itself uses threads/locks.
        for strategy in ["thread", "process"]:
            self._add_scenario(
                name=f"safety_deadlock_{strategy}_subprocess_threaded",
                phase=phase,
                description=f"Safety: {strategy} worker spawning threaded subprocesses (Deadlock Risk)",
                strategy=strategy,
                workload_type="subprocess_threaded",
                num_instances=50,
                max_concurrent_jobs=20, # High concurrency increases race condition probability
                work_duration=0.5,
                repeats=3,
                timeout=60 # Should fail/hang quickly if broken
            )

        # 2. Async Blocking
        # Confirm that CPU work in async strategy blocks the loop (and thus heartbeats?)
        self._add_scenario(
            name="safety_async_blocking_cpu",
            phase=phase,
            description="Safety: Async worker with heavy CPU load (Loop Blocking Risk)",
            strategy="async",
            workload_type="cpu",
            num_instances=10,
            max_concurrent_jobs=1, # Serial execution
            work_duration=5.0, # Long blocking duration
            repeats=1,
            job_timeout_ms=2000 # Job timeout < Work duration -> Should fail if heartbeats are blocked?
            # Note: SDK might not heartbeat during user callback execution anyway, but this tests the behavior.
        )

        # 3. Resource Exhaustion
        # High concurrency with Process strategy (Memory pressure)
        self._add_scenario(
            name="safety_process_exhaustion",
            phase=phase,
            description="Safety: Process strategy with high concurrency (Memory Risk)",
            strategy="process",
            workload_type="cpu",
            num_instances=100,
            max_concurrent_jobs=50, # 50 processes!
            work_duration=1.0,
            repeats=1,
            timeout=300
        )

    def generate_minimal_suite(self):
        """Smoke tests only."""
        self._add_scenario(
            name="smoke_async_cpu",
            phase="0_smoke",
            description="Smoke Test: Async CPU",
            strategy="async",
            workload_type="cpu",
            num_instances=5,
            work_duration=0.1,
            max_concurrent_jobs=5,
            repeats=1
        )

    def generate_fast_suite(self):
        """Fast validation (subset of baseline + safety)."""
        self.generate_baseline_suite()
        # Add one safety case
        self._add_scenario(
            name="fast_safety_check",
            phase="3_safety",
            description="Fast Safety Check: Threaded Subprocess",
            strategy="thread",
            workload_type="subprocess_threaded",
            num_instances=10,
            max_concurrent_jobs=5,
            work_duration=0.5,
            repeats=1
        )

    def generate_full_suite(self):
        """Generate everything."""
        self.generate_baseline_suite()
        self.generate_envelope_suite()
        self.generate_safety_suite()

    def get_scenarios(self) -> List[Scenario]:
        return self.scenarios

    def get_summary(self) -> dict:
        phases = {}
        strategies = {}
        workloads = {}
        
        for s in self.scenarios:
            phases[s["phase"]] = phases.get(s["phase"], 0) + 1
            strategies[s["strategy"]] = strategies.get(s["strategy"], 0) + 1
            workloads[s["workload_type"]] = workloads.get(s["workload_type"], 0) + 1

        return {
            "total": len(self.scenarios),
            "by_phase": phases,
            "by_strategy": strategies,
            "by_workload": workloads
        }


def save_to_json(scenarios: List[Scenario], filepath: str):
    with open(filepath, 'w') as f:
        json.dump(scenarios, f, indent=2)
    print(f"✓ Saved {len(scenarios)} scenarios to {filepath}")


def print_summary(generator: BenchmarkScenarioGenerator):
    summary = generator.get_summary()
    print("\n" + "="*70)
    print("BENCHMARK SUITE SUMMARY")
    print("="*70)
    print(f"Total Scenarios: {summary['total']}")
    
    print("\nBy Phase:")
    for k, v in sorted(summary['by_phase'].items()):
        print(f"  {k:30} {v:4}")
        
    print("\nBy Strategy:")
    for k, v in sorted(summary['by_strategy'].items()):
        print(f"  {k:30} {v:4}")

    print("\nBy Workload:")
    for k, v in sorted(summary['by_workload'].items()):
        print(f"  {k:30} {v:4}")
    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Generate benchmark scenarios")
    parser.add_argument(
        "--suite",
        choices=["minimal", "fast", "baseline", "envelope", "safety", "full"],
        default="full",
        help="Suite to generate"
    )
    parser.add_argument("--output", "-o", help="Output JSON file path")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress summary")

    args = parser.parse_args()
    generator = BenchmarkScenarioGenerator()

    if args.suite == "minimal":
        generator.generate_minimal_suite()
    elif args.suite == "fast":
        generator.generate_fast_suite()
    elif args.suite == "baseline":
        generator.generate_baseline_suite()
    elif args.suite == "envelope":
        generator.generate_envelope_suite()
    elif args.suite == "safety":
        generator.generate_safety_suite()
    elif args.suite == "full":
        generator.generate_full_suite()

    scenarios = generator.get_scenarios()
    
    # Default output path
    if args.output:
        output_path = args.output
    else:
        script_dir = Path(__file__).parent
        scenarios_dir = script_dir / "scenarios"
        scenarios_dir.mkdir(exist_ok=True)
        output_path = str(scenarios_dir / f"{args.suite}.json")

    save_to_json(scenarios, output_path)
    
    if not args.quiet:
        print_summary(generator)


if __name__ == "__main__":
    main()
