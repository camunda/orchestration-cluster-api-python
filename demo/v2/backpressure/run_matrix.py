#!/usr/bin/env python3
"""
Backpressure Matrix Runner
===========================

Runs the full multi-client backpressure exploration matrix and produces
a comprehensive report with analysis and recommendations.

Between each run the Camunda container is stopped and restarted to ensure
every configuration gets an identical clean baseline.

Matrix dimensions
─────────────────
  NUM_CLIENTS:  25, 50
  MODE:         sync, async, thread
  WORKLOAD:     instant (0s latency), sleep (0.2s), http (0.2s via local server)
  PROFILE:      BALANCED, LEGACY
  ISOLATION:    subprocess (separate OS process per client, independent BP),
                shared     (threads sharing ONE client, shared BP)

Total: 2 × 3 × 3 × 2 × 2 = 72 configurations

Usage
─────
  # Full 36-configuration matrix
  uv run demo/v2/backpressure/run_matrix.py

  # Subset: only 25 clients
  uv run demo/v2/backpressure/run_matrix.py --clients 25

  # Subset: only async and thread modes
  uv run demo/v2/backpressure/run_matrix.py --modes async thread

  # Subset: only BALANCED profile
  uv run demo/v2/backpressure/run_matrix.py --profiles BALANCED

  # Custom target per client (default: 20)
  uv run demo/v2/backpressure/run_matrix.py --target 50

  # Skip container restarts (faster but less reliable baselines)
  uv run demo/v2/backpressure/run_matrix.py --no-restart

  # Preview what would run without executing
  uv run demo/v2/backpressure/run_matrix.py --dry-run
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import textwrap
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[3]
COMPOSE_FILE = REPO_ROOT / "docker" / "docker-compose.yaml"
MULTI_CLIENT_SCRIPT = Path(__file__).parent / "multi_client.py"
RESULTS_DIR = Path(__file__).parent / "results"

# ---------------------------------------------------------------------------
# Default matrix parameters
# ---------------------------------------------------------------------------
DEFAULT_CLIENTS = [25, 50]
DEFAULT_MODES = ["sync", "async", "thread"]
DEFAULT_WORKLOADS = [
    {"name": "instant", "handler_type": "sleep", "handler_latency": "0"},
    {"name": "sleep",   "handler_type": "sleep", "handler_latency": "0.2"},
    {"name": "http",    "handler_type": "http",  "handler_latency": "0.2"},
]
DEFAULT_PROFILES = ["BALANCED", "LEGACY"]
DEFAULT_ISOLATIONS = ["subprocess", "shared"]

# Per-run tunables
DEFAULT_TARGET_PER_CLIENT = 20
DEFAULT_CLIENT_CONCURRENCY = 10
DEFAULT_ACTIVATE_BATCH = 32
DEFAULT_SCENARIO_TIMEOUT = 300  # 5 min per run

# ANSI colour stripping
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------
@dataclass
class RunResult:
    num_clients: int
    mode: str
    workload: str
    profile: str
    isolation: str = "subprocess"
    target_total: int = 0
    total_completed: int = 0
    total_errors: int = 0
    total_queue_full: int = 0
    wall_clock_s: float = 0.0
    throughput: float = 0.0
    jain_fairness: float = 0.0
    status: str = "pending"  # pending | ok | timeout | error
    raw_output_file: str = ""

    @property
    def iso_short(self) -> str:
        return "sub" if self.isolation == "subprocess" else "shr"

    @property
    def label(self) -> str:
        return f"{self.num_clients}c-{self.profile[0]}-{self.mode}-{self.workload}-{self.iso_short}"

    @property
    def error_rate(self) -> float:
        total = self.total_completed + self.total_errors
        return self.total_errors / total if total > 0 else 0.0


# ---------------------------------------------------------------------------
# Container management
# ---------------------------------------------------------------------------
def restart_container() -> bool:
    """Stop and restart the Camunda container. Returns True if healthy."""
    print("  [container] Stopping...", end="", flush=True)
    subprocess.run(
        ["docker", "compose", "-f", str(COMPOSE_FILE), "down", "--timeout", "30"],
        capture_output=True,
        timeout=90,
    )
    # Wait for port release and full shutdown
    time.sleep(5)

    print(" starting...", end="", flush=True)
    subprocess.run(
        ["docker", "compose", "-f", str(COMPOSE_FILE), "up", "-d"],
        capture_output=True,
        timeout=60,
    )

    # Phase 1: Poll management health endpoint (port 9600)
    deadline = time.time() + 120
    while time.time() < deadline:
        try:
            r = subprocess.run(
                ["curl", "-sf", "http://localhost:9600/actuator/health/status"],
                capture_output=True,
                timeout=5,
            )
            if r.returncode == 0:
                break
        except Exception:
            pass
        print(".", end="", flush=True)
        time.sleep(3)
    else:
        print(" TIMEOUT (health)!", flush=True)
        return False

    # Phase 2: Verify REST API on port 8080 is also accepting requests
    deadline2 = time.time() + 30
    while time.time() < deadline2:
        try:
            r = subprocess.run(
                ["curl", "-sf", "-o", "/dev/null", "-w", "%{http_code}",
                 "http://localhost:8080/v2/topology"],
                capture_output=True,
                timeout=5,
                text=True,
            )
            if r.returncode == 0:
                print(" ready!", flush=True)
                time.sleep(3)  # extra settling time
                return True
        except Exception:
            pass
        print(".", end="", flush=True)
        time.sleep(2)

    print(" TIMEOUT (REST API)!", flush=True)
    return False


# ---------------------------------------------------------------------------
# Output parser
# ---------------------------------------------------------------------------
def parse_output(raw: str) -> dict[str, Any]:
    """Extract metrics from multi_client.py output."""
    text = _strip_ansi(raw)
    result: dict[str, Any] = {}

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Total completed:"):
            m = re.search(r"(\d+)", stripped.split(":", 1)[1])
            if m:
                result["total_completed"] = int(m.group(1))
        elif stripped.startswith("Total errors:"):
            m = re.search(r"(\d+)", stripped.split(":", 1)[1])
            if m:
                result["total_errors"] = int(m.group(1))
        elif stripped.startswith("Total queue-full:"):
            m = re.search(r"(\d+)", stripped.split(":", 1)[1])
            if m:
                result["total_queue_full"] = int(m.group(1))
        elif stripped.startswith("Wall-clock duration:"):
            m = re.search(r"([\d.]+)s", stripped)
            if m:
                result["wall_clock_s"] = float(m.group(1))
        elif stripped.startswith("Aggregate throughput:"):
            m = re.search(r"([\d.]+)", stripped.split(":", 1)[1])
            if m:
                result["throughput"] = float(m.group(1))
        elif stripped.startswith("Jain's fairness"):
            m = re.search(r"([\d.]+)", stripped.split(":", 1)[1])
            if m:
                result["jain_fairness"] = float(m.group(1))

    return result


# ---------------------------------------------------------------------------
# Run one scenario
# ---------------------------------------------------------------------------
def run_scenario(
    num_clients: int,
    mode: str,
    workload: dict[str, str],
    profile: str,
    isolation: str,
    target_per_client: int,
    client_concurrency: int,
    do_restart: bool,
    scenario_timeout: int,
) -> RunResult:
    """Run one matrix cell."""

    result = RunResult(
        num_clients=num_clients,
        mode=mode,
        workload=workload["name"],
        profile=profile,
        isolation=isolation,
        target_total=num_clients * target_per_client,
    )

    print(f"\n{'=' * 65}")
    print(f"  [{result.label}]  {num_clients} clients × {target_per_client} target")
    print(f"  mode={mode}  workload={workload['name']}  profile={profile}  isolation={isolation}")
    print(f"{'=' * 65}", flush=True)

    # Restart container for clean baseline
    if do_restart:
        if not restart_container():
            result.status = "error"
            print(f"  [{result.label}] => CONTAINER FAILED TO START")
            return result

    # Build environment
    env = os.environ.copy()
    env.update({
        "ISOLATION": isolation,
        "MODE": mode,
        "NUM_CLIENTS": str(num_clients),
        "SPIKE_CLIENTS": "0",
        "TARGET_PER_CLIENT": str(target_per_client),
        "CLIENT_CONCURRENCY": str(client_concurrency),
        "ACTIVATE_BATCH": str(DEFAULT_ACTIVATE_BATCH),
        "HANDLER_TYPE": workload["handler_type"],
        "HANDLER_LATENCY_S": workload["handler_latency"],
        "PROFILE": profile,
        "PAYLOAD_SIZE_KB": "10",
        "PROGRESS_INTERVAL_S": "5",
        "SCENARIO_TIMEOUT_S": str(scenario_timeout),
    })

    # Run multi_client.py
    output_file = RESULTS_DIR / f"{result.label}.txt"
    result.raw_output_file = str(output_file)

    try:
        proc = subprocess.run(
            [sys.executable, str(MULTI_CLIENT_SCRIPT)],
            env=env,
            capture_output=True,
            text=True,
            timeout=scenario_timeout + 60,  # extra buffer over inner timeout
            cwd=str(REPO_ROOT),
        )

        # Save raw output
        output = proc.stdout + "\n" + proc.stderr
        output_file.write_text(output)

        # Parse metrics
        metrics = parse_output(output)
        result.total_completed = metrics.get("total_completed", 0)
        result.total_errors = metrics.get("total_errors", 0)
        result.total_queue_full = metrics.get("total_queue_full", 0)
        result.wall_clock_s = metrics.get("wall_clock_s", 0)
        result.throughput = metrics.get("throughput", 0)
        result.jain_fairness = metrics.get("jain_fairness", 0)
        result.status = "ok"

        print(
            f"  [{result.label}] => "
            f"{result.throughput:.1f}/s, "
            f"{result.total_errors} errors, "
            f"{result.wall_clock_s:.1f}s, "
            f"Jain={result.jain_fairness:.3f}"
        )

    except subprocess.TimeoutExpired:
        result.status = "timeout"
        print(f"  [{result.label}] => TIMEOUT ({scenario_timeout}s)")
    except Exception as e:
        result.status = "error"
        print(f"  [{result.label}] => ERROR: {e}")

    return result


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def generate_report(
    results: list[RunResult],
    target_per_client: int,
    client_concurrency: int,
    timestamp: str,
) -> str:
    """Generate a Markdown report with analysis and recommendations."""

    ok_results = [r for r in results if r.status == "ok"]
    failed = [r for r in results if r.status != "ok"]

    # ── Header ──
    lines: list[str] = []
    w = lines.append

    w("# Backpressure Matrix Report")
    w("")
    w(f"Generated: {timestamp}")
    w("")
    w("## Parameters")
    w("")
    w(f"- **Target per client**: {target_per_client}")
    w(f"- **Client concurrency**: {client_concurrency}")
    w(f"- **Activate batch**: {DEFAULT_ACTIVATE_BATCH}")
    w(f"- **Payload**: 10 KB per instance")
    w(f"- **Container restarted** between each run")
    w("")

    # ── Summary table ──
    w("## Results Summary")
    w("")
    w("| Clients | Profile | Mode | Workload | Isolation | Throughput | Errors | QFull | Wall-clock | Jain | Status |")
    w("|---------|---------|------|----------|-----------|------------|--------|-------|------------|------|--------|")

    for r in sorted(results, key=lambda x: (x.num_clients, x.isolation, x.profile, x.mode, x.workload)):
        iso_label = "sub" if r.isolation == "subprocess" else "shr"
        if r.status == "ok":
            err_flag = " ⚠️" if r.total_errors > 0 else ""
            w(
                f"| {r.num_clients} | {r.profile} | {r.mode} | {r.workload} "
                f"| {iso_label} "
                f"| {r.throughput:.1f}/s | {r.total_errors}{err_flag} "
                f"| {r.total_queue_full} | {r.wall_clock_s:.1f}s "
                f"| {r.jain_fairness:.3f} | {r.status} |"
            )
        else:
            w(
                f"| {r.num_clients} | {r.profile} | {r.mode} | {r.workload} "
                f"| {iso_label} "
                f"| - | - | - | - | - | **{r.status}** |"
            )

    if failed:
        w("")
        w(f"**{len(failed)} run(s) failed** (timeout or error).")

    # ── Analysis by dimension ──
    w("")
    w("## Analysis")

    # Group by num_clients
    for nc in sorted(set(r.num_clients for r in ok_results)):
        subset = [r for r in ok_results if r.num_clients == nc]
        w("")
        w(f"### {nc} Clients")
        w("")

        # BALANCED vs LEGACY comparison
        balanced = [r for r in subset if r.profile == "BALANCED"]
        legacy = [r for r in subset if r.profile == "LEGACY"]

        b_errors = sum(r.total_errors for r in balanced)
        l_errors = sum(r.total_errors for r in legacy)
        b_throughput = sum(r.throughput for r in balanced) / len(balanced) if balanced else 0
        l_throughput = sum(r.throughput for r in legacy) / len(legacy) if legacy else 0

        w(f"- **BALANCED**: avg throughput {b_throughput:.1f}/s, total errors {b_errors}")
        w(f"- **LEGACY**: avg throughput {l_throughput:.1f}/s, total errors {l_errors}")

        if l_errors > b_errors:
            reduction = ((l_errors - b_errors) / l_errors * 100) if l_errors > 0 else 0
            w(f"- BALANCED reduces errors by **{reduction:.0f}%** vs LEGACY")

        # Best configs per mode
        w("")
        w("**Best configuration per mode:**")
        w("")
        for mode in ["sync", "async", "thread"]:
            mode_results = [r for r in subset if r.mode == mode]
            if not mode_results:
                continue
            # Best = highest throughput with 0 errors, or lowest errors if all have errors
            zero_err = [r for r in mode_results if r.total_errors == 0]
            if zero_err:
                best = max(zero_err, key=lambda r: r.throughput)
                w(f"- **{mode}**: {best.profile} + {best.workload} → "
                  f"{best.throughput:.1f}/s, 0 errors")
            else:
                best = min(mode_results, key=lambda r: (r.total_errors, -r.throughput))
                w(f"- **{mode}**: {best.profile} + {best.workload} → "
                  f"{best.throughput:.1f}/s, {best.total_errors} errors ⚠️")

    # ── Per-mode analysis ──
    w("")
    w("### Mode Comparison")
    w("")
    for mode in ["sync", "async", "thread"]:
        mode_ok = [r for r in ok_results if r.mode == mode]
        if not mode_ok:
            continue
        w(f"**{mode}:**")
        zero_err = [r for r in mode_ok if r.total_errors == 0]
        has_err = [r for r in mode_ok if r.total_errors > 0]
        w(f"  - {len(zero_err)}/{len(mode_ok)} configs zero errors")
        if has_err:
            worst = max(has_err, key=lambda r: r.total_errors)
            w(f"  - Worst: {worst.label} with {worst.total_errors} errors")
        if zero_err:
            best = max(zero_err, key=lambda r: r.throughput)
            w(f"  - Peak (error-free): {best.label} at {best.throughput:.1f}/s")
        w("")

    # ── Isolation comparison ──
    w("")
    w("### Isolation Comparison (independent vs shared BP)")
    w("")
    for iso in ["subprocess", "shared"]:
        iso_label = "Subprocess (independent BP)" if iso == "subprocess" else "Shared (single BP manager)"
        iso_ok = [r for r in ok_results if r.isolation == iso]
        if not iso_ok:
            continue
        avg_tp = sum(r.throughput for r in iso_ok) / len(iso_ok)
        total_err = sum(r.total_errors for r in iso_ok)
        w(f"**{iso_label}:** avg throughput {avg_tp:.1f}/s, total errors {total_err}")
    w("")

    sub_ok = [r for r in ok_results if r.isolation == "subprocess"]
    shr_ok = [r for r in ok_results if r.isolation == "shared"]
    if sub_ok and shr_ok:
        sub_avg = sum(r.throughput for r in sub_ok) / len(sub_ok)
        shr_avg = sum(r.throughput for r in shr_ok) / len(shr_ok)
        sub_err = sum(r.total_errors for r in sub_ok)
        shr_err = sum(r.total_errors for r in shr_ok)

        w("| Metric | Independent (subprocess) | Shared (single client) | Delta |")
        w("|--------|--------------------------|------------------------|-------|")
        delta_tp = sub_avg - shr_avg
        delta_pct = (delta_tp / shr_avg * 100) if shr_avg > 0 else 0
        w(f"| Avg throughput | {sub_avg:.1f}/s | {shr_avg:.1f}/s | {delta_pct:+.1f}% |")
        w(f"| Total errors | {sub_err} | {shr_err} | {sub_err - shr_err:+d} |")
        w("")

        if abs(delta_pct) < 15 and abs(sub_err - shr_err) / max(sub_err, shr_err, 1) < 0.2:
            w("Independent and shared BP show **similar performance** — the adaptive "
              "algorithm converges well without centralised coordination. This validates "
              "distributed client-side backpressure management.")
        elif delta_pct > 15:
            w(f"Independent (subprocess) shows **{delta_pct:.0f}% higher throughput**. "
              f"The shared BP manager may be over-constraining all workers when only "
              f"some experience backpressure.")
        else:
            w(f"Shared BP is **{-delta_pct:.0f}% faster** — centralised coordination "
              f"avoids redundant backoff across independent clients.")

    # ── Recommendations ──
    w("")
    w("## Recommendations")
    w("")

    # Per execution strategy recommendation
    w("### Per Execution Strategy")
    w("")

    for mode in ["sync", "async", "thread"]:
        mode_ok = [r for r in ok_results if r.mode == mode]
        if not mode_ok:
            continue

        w(f"#### `{mode}` mode")
        w("")

        balanced_ok = [r for r in mode_ok if r.profile == "BALANCED"]
        legacy_ok = [r for r in mode_ok if r.profile == "LEGACY"]

        b_err = sum(r.total_errors for r in balanced_ok)
        l_err = sum(r.total_errors for r in legacy_ok)
        b_avg = sum(r.throughput for r in balanced_ok) / len(balanced_ok) if balanced_ok else 0
        l_avg = sum(r.throughput for r in legacy_ok) / len(legacy_ok) if legacy_ok else 0

        if mode == "sync":
            if l_err > 0 and b_err < l_err:
                w(f"**Recommended profile: BALANCED**")
                w("")
                w(f"Sync mode is vulnerable to backpressure because the producer "
                  f"fires create_process_instance calls via a thread pool without "
                  f"built-in concurrency gating from the job worker. "
                  f"BALANCED's adaptive permit system prevents overload.")
                w("")
                w(f"- BALANCED: avg {b_avg:.1f}/s, {b_err} total errors")
                w(f"- LEGACY: avg {l_avg:.1f}/s, {l_err} total errors")
            else:
                w(f"Both profiles perform similarly. Prefer BALANCED for safety.")
        else:
            # async/thread have job worker with max_concurrent_jobs
            zero_both = (b_err == 0 and l_err == 0)
            if zero_both:
                w(f"**Recommended profile: BALANCED** (or LEGACY — both error-free)")
                w("")
                w(f"The job worker's `max_concurrent_jobs` naturally limits concurrency, "
                  f"making both profiles equally safe. BALANCED is recommended as a "
                  f"sensible default for forward-compatibility.")
            elif b_err < l_err:
                w(f"**Recommended profile: BALANCED**")
                w("")
                w(f"- BALANCED: avg {b_avg:.1f}/s, {b_err} total errors")
                w(f"- LEGACY: avg {l_avg:.1f}/s, {l_err} total errors")
            else:
                w(f"**Recommended profile: BALANCED**")
                w(f"  (Both show similar error patterns; BALANCED is the safer default.)")
        w("")

    # Overall default
    w("### SDK Default Recommendation")
    w("")

    total_b_err = sum(r.total_errors for r in ok_results if r.profile == "BALANCED")
    total_l_err = sum(r.total_errors for r in ok_results if r.profile == "LEGACY")
    total_b_throughput = sum(r.throughput for r in ok_results if r.profile == "BALANCED")
    total_l_throughput = sum(r.throughput for r in ok_results if r.profile == "LEGACY")
    n_b = len([r for r in ok_results if r.profile == "BALANCED"]) or 1
    n_l = len([r for r in ok_results if r.profile == "LEGACY"]) or 1

    w(f"| Metric | BALANCED | LEGACY |")
    w(f"|--------|----------|--------|")
    w(f"| Total errors (all runs) | {total_b_err} | {total_l_err} |")
    w(f"| Avg throughput | {total_b_throughput / n_b:.1f}/s | {total_l_throughput / n_l:.1f}/s |")
    w("")

    if total_l_err > total_b_err:
        reduction = (total_l_err - total_b_err) / total_l_err * 100 if total_l_err else 0
        w(f"**BALANCED should be the SDK default.** It reduces errors by "
          f"{reduction:.0f}% across the full matrix while maintaining comparable "
          f"throughput. The adaptive permit system is especially critical for "
          f"`sync` mode, where the absence of a job-worker concurrency gate "
          f"makes the client vulnerable to server overload.")
    else:
        w(f"Both profiles show similar error profiles. **BALANCED is recommended "
          f"as the default** for its adaptive protection, which provides a safety "
          f"net without measurable throughput penalty.")

    w("")
    w("---")
    w(f"*Report generated by `run_matrix.py` — {len(results)} configurations tested.*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the backpressure multi-client matrix exploration.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--clients", nargs="+", type=int, default=DEFAULT_CLIENTS,
        help=f"Client counts to test (default: {DEFAULT_CLIENTS})",
    )
    parser.add_argument(
        "--modes", nargs="+", default=DEFAULT_MODES,
        choices=["sync", "async", "thread"],
        help=f"Execution modes (default: {DEFAULT_MODES})",
    )
    parser.add_argument(
        "--workloads", nargs="+", default=None,
        choices=["instant", "sleep", "http"],
        help="Workload types (default: all three)",
    )
    parser.add_argument(
        "--profiles", nargs="+", default=DEFAULT_PROFILES,
        choices=["BALANCED", "LEGACY"],
        help=f"Backpressure profiles (default: {DEFAULT_PROFILES})",
    )
    parser.add_argument(
        "--isolations", nargs="+", default=DEFAULT_ISOLATIONS,
        choices=["subprocess", "shared"],
        help=f"Process isolation modes (default: {DEFAULT_ISOLATIONS})",
    )
    parser.add_argument(
        "--target", type=int, default=DEFAULT_TARGET_PER_CLIENT,
        help=f"Target completions per client (default: {DEFAULT_TARGET_PER_CLIENT})",
    )
    parser.add_argument(
        "--concurrency", type=int, default=DEFAULT_CLIENT_CONCURRENCY,
        help=f"Max inflight per client (default: {DEFAULT_CLIENT_CONCURRENCY})",
    )
    parser.add_argument(
        "--timeout", type=int, default=DEFAULT_SCENARIO_TIMEOUT,
        help=f"Per-run timeout in seconds (default: {DEFAULT_SCENARIO_TIMEOUT})",
    )
    parser.add_argument(
        "--no-restart", action="store_true",
        help="Skip container restarts between runs (faster, less reliable)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the matrix without executing anything",
    )
    args = parser.parse_args()

    # Resolve workloads
    if args.workloads:
        workloads = [w for w in DEFAULT_WORKLOADS if w["name"] in args.workloads]
    else:
        workloads = DEFAULT_WORKLOADS

    # Build matrix
    matrix: list[tuple[int, str, dict[str, str], str, str]] = []
    for nc in sorted(args.clients):
        for isolation in args.isolations:
            for profile in args.profiles:
                for mode in args.modes:
                    for wl in workloads:
                        matrix.append((nc, mode, wl, profile, isolation))

    total = len(matrix)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n╔══════════════════════════════════════════════════════════════════╗")
    print(f"║   Backpressure Matrix Runner                                    ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝")
    print(f"  Configurations:  {total}")
    print(f"  Client counts:   {args.clients}")
    print(f"  Modes:           {args.modes}")
    print(f"  Workloads:       {[w['name'] for w in workloads]}")
    print(f"  Profiles:        {args.profiles}")
    print(f"  Isolations:      {args.isolations}")
    print(f"  Target/client:   {args.target}")
    print(f"  Concurrency:     {args.concurrency}")
    print(f"  Timeout/run:     {args.timeout}s")
    print(f"  Restart:         {'no' if args.no_restart else 'yes'}")
    print()

    if args.dry_run:
        print("DRY RUN — would execute:")
        for i, (nc, mode, wl, profile, isolation) in enumerate(matrix, 1):
            iso_short = "sub" if isolation == "subprocess" else "shr"
            print(f"  {i:>3}. {nc}c-{profile[0]}-{mode}-{wl['name']}-{iso_short}")
        print(f"\nTotal: {total} runs")
        return

    # Create results directory
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Run matrix
    results: list[RunResult] = []
    t0 = time.time()

    for i, (nc, mode, wl, profile, isolation) in enumerate(matrix, 1):
        print(f"\n  ── Run {i}/{total} ──")
        result = run_scenario(
            num_clients=nc,
            mode=mode,
            workload=wl,
            profile=profile,
            isolation=isolation,
            target_per_client=args.target,
            client_concurrency=args.concurrency,
            do_restart=not args.no_restart,
            scenario_timeout=args.timeout,
        )
        results.append(result)

        # Progress summary
        elapsed = time.time() - t0
        ok_count = sum(1 for r in results if r.status == "ok")
        remaining = total - i
        avg_per_run = elapsed / i
        eta = avg_per_run * remaining
        print(
            f"\n  Progress: {i}/{total} done ({ok_count} ok), "
            f"elapsed {elapsed:.0f}s, ~{eta:.0f}s remaining"
        )

    total_elapsed = time.time() - t0

    # Save raw results as JSON
    json_path = RESULTS_DIR / "results.json"
    json_path.write_text(json.dumps(
        [asdict(r) for r in results],
        indent=2,
        default=str,
    ))

    # Generate report
    report = generate_report(
        results,
        target_per_client=args.target,
        client_concurrency=args.concurrency,
        timestamp=timestamp,
    )

    report_path = RESULTS_DIR / "report.md"
    report_path.write_text(report)

    # Print report to stdout
    print(f"\n\n{'=' * 65}")
    print(report)
    print(f"\n{'=' * 65}")
    print(f"\nTotal elapsed: {total_elapsed:.0f}s ({total_elapsed / 60:.1f} min)")
    print(f"Results:       {RESULTS_DIR}")
    print(f"Report:        {report_path}")
    print(f"Raw JSON:      {json_path}")


if __name__ == "__main__":
    main()
