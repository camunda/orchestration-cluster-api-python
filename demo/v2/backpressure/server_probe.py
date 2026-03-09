"""Server recovery probe — measures actual backpressure/recovery dynamics.

Fires bursts of requests, timestamps every 429 and 200, then computes:
  - How long the server stays in backpressure after a burst
  - How quickly it recovers (first success after last 429)
  - The sustained rate at which it can handle requests without 429s
"""
import httpx
import time
import json
import os
import statistics

BASE_URL = os.environ.get("CAMUNDA_BASE_URL", "http://localhost:8080")
PROCESS_KEY = os.environ.get("PROCESS_DEFINITION_KEY", "")

# Generate 10KB payload to match matrix test workload
import random as _rng
_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
PAYLOAD_10KB = "".join(_rng.Random(42).choice(_alphabet) for _ in range(10 * 1024))


def deploy_and_get_key(client: httpx.Client) -> str:
    """Deploy a minimal process and return its definition key."""
    bpmn = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:zeebe="http://camunda.org/schema/zeebe/1.0"
  targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn:process id="bp-probe" isExecutable="true">
    <bpmn:startEvent id="start"/>
  </bpmn:process>
</bpmn:definitions>"""
    resp = client.post(
        f"{BASE_URL}/v2/deployments",
        files={"resources": ("probe.bpmn", bpmn.encode(), "application/xml")},
    )
    resp.raise_for_status()
    data = resp.json()
    # Handle various response shapes
    for item in data.get("deployedProcesses", data.get("processes", [])):
        return str(item["processDefinitionKey"])
    for item in data.get("deployments", []):
        pd = item.get("processDefinition")
        if pd and pd.get("processDefinitionKey"):
            return str(pd["processDefinitionKey"])
    raise RuntimeError(f"No process in deployment response: {data}")


def create_instance(client: httpx.Client, key: str) -> tuple[int, float]:
    """Send one create-instance request with 10KB payload. Returns (status_code, latency_s)."""
    t0 = time.monotonic()
    try:
        resp = client.post(
            f"{BASE_URL}/v2/process-instances",
            json={
                "processDefinitionKey": key,
                "variables": {"data": PAYLOAD_10KB},
            },
            timeout=10.0,
        )
        return resp.status_code, time.monotonic() - t0
    except Exception:
        return 0, time.monotonic() - t0


def probe_burst(client: httpx.Client, key: str, burst_size: int) -> list[dict]:
    """Fire a burst of requests, recording timestamp + status for each."""
    results = []
    for i in range(burst_size):
        t = time.monotonic()
        status, latency = create_instance(client, key)
        results.append({
            "t": t,
            "status": status,
            "latency": latency,
            "seq": i,
        })
    return results


def probe_steady(client: httpx.Client, key: str, rps: float, duration_s: float) -> list[dict]:
    """Send requests at a steady rate, recording status codes."""
    interval = 1.0 / rps
    results = []
    t_start = time.monotonic()
    while time.monotonic() - t_start < duration_s:
        t = time.monotonic()
        status, latency = create_instance(client, key)
        results.append({
            "t_rel": t - t_start,
            "status": status,
            "latency": latency,
        })
        elapsed = time.monotonic() - t
        sleep_for = interval - elapsed
        if sleep_for > 0:
            time.sleep(sleep_for)
    return results


def analyze_burst(results: list[dict]) -> dict:
    """Analyze a burst for recovery timing."""
    if not results:
        return {}
    t0 = results[0]["t"]
    successes = [r for r in results if r["status"] in (200, 201)]
    errors = [r for r in results if r["status"] == 429]
    other = [r for r in results if r["status"] not in (200, 201, 429)]

    last_429_t = max((r["t"] for r in errors), default=0) - t0 if errors else 0
    first_success_after_429 = None
    if errors:
        last_429_abs = max(r["t"] for r in errors)
        for r in results:
            if r["t"] > last_429_abs and r["status"] in (200, 201):
                first_success_after_429 = r["t"] - last_429_abs
                break

    return {
        "total": len(results),
        "successes": len(successes),
        "errors_429": len(errors),
        "other_errors": len(other),
        "duration_s": results[-1]["t"] - t0,
        "last_429_at_s": last_429_t,
        "recovery_gap_s": first_success_after_429,
        "avg_latency_success": statistics.mean(r["latency"] for r in successes) if successes else 0,
        "avg_latency_429": statistics.mean(r["latency"] for r in errors) if errors else 0,
    }


def analyze_steady(results: list[dict]) -> dict:
    """Analyze steady-state for 429 windows."""
    if not results:
        return {}
    successes = [r for r in results if r["status"] in (200, 201)]
    errors = [r for r in results if r["status"] == 429]

    # Find contiguous 429 windows
    windows = []
    in_window = False
    window_start = 0
    for r in results:
        if r["status"] == 429:
            if not in_window:
                in_window = True
                window_start = r["t_rel"]
        else:
            if in_window:
                windows.append({"start": window_start, "end": r["t_rel"], "duration": r["t_rel"] - window_start})
                in_window = False
    if in_window:
        windows.append({"start": window_start, "end": results[-1]["t_rel"], "duration": results[-1]["t_rel"] - window_start})

    return {
        "total": len(results),
        "successes": len(successes),
        "errors_429": len(errors),
        "error_rate": len(errors) / len(results) if results else 0,
        "bp_windows": len(windows),
        "avg_window_duration_s": statistics.mean(w["duration"] for w in windows) if windows else 0,
        "max_window_duration_s": max((w["duration"] for w in windows), default=0),
        "windows": windows[:10],  # first 10 for inspection
    }


def main():
    client = httpx.Client()

    # Deploy or use existing key
    key = PROCESS_KEY
    if not key:
        print("Deploying probe process...")
        key = deploy_and_get_key(client)
        print(f"  Key: {key}")

    print(f"\n=== Phase 1: Concurrent burst to trigger backpressure ===")
    import concurrent.futures
    import threading

    results_lock = threading.Lock()

    def timed_create(seq: int) -> dict:
        # Each thread gets its own client to avoid connection pool contention
        with httpx.Client() as c:
            t = time.monotonic()
            status, latency = create_instance(c, key)
            return {"t": t, "status": status, "latency": latency, "seq": seq}

    for concurrency in [10, 25, 50, 100, 200]:
        total_reqs = concurrency * 5  # 5 requests per "client"
        print(f"\n  {concurrency} concurrent threads, {total_reqs} total requests...")
        time.sleep(3)  # let server recover

        all_results = []
        t_start = time.monotonic()
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = [pool.submit(timed_create, i) for i in range(total_reqs)]
            for f in concurrent.futures.as_completed(futures):
                all_results.append(f.result())
        t_end = time.monotonic()

        all_results.sort(key=lambda r: r["t"])
        successes = sum(1 for r in all_results if r["status"] in (200, 201))
        errors_429 = sum(1 for r in all_results if r["status"] == 429)
        errors_other = sum(1 for r in all_results if r["status"] not in (200, 201, 429))
        duration = t_end - t_start

        # Find 429 timing windows
        first_429 = None
        last_429 = None
        first_ok_after_429 = None
        for r in all_results:
            if r["status"] == 429:
                if first_429 is None:
                    first_429 = r["t"] - t_start
                last_429 = r["t"] - t_start
        if last_429 is not None:
            last_429_abs = t_start + last_429
            for r in all_results:
                if r["t"] > last_429_abs and r["status"] in (200, 201):
                    first_ok_after_429 = r["t"] - last_429_abs
                    break

        avg_ok = statistics.mean(r["latency"] for r in all_results if r["status"] in (200, 201)) if successes else 0
        avg_429 = statistics.mean(r["latency"] for r in all_results if r["status"] == 429) if errors_429 else 0

        print(f"    Duration: {duration:.2f}s")
        print(f"    {successes} ok, {errors_429} x429, {errors_other} other")
        print(f"    Error rate: {errors_429/len(all_results):.1%}")
        print(f"    Avg latency OK: {avg_ok*1000:.0f}ms, 429: {avg_429*1000:.0f}ms")
        if first_429 is not None:
            print(f"    First 429 at: {first_429:.3f}s")
            print(f"    Last 429 at: {last_429:.3f}s")
            print(f"    429 window: {last_429 - first_429:.3f}s")
            if first_ok_after_429 is not None:
                print(f"    Recovery gap (last 429 → first OK): {first_ok_after_429*1000:.0f}ms")

    print(f"\n=== Phase 2: Sustained concurrent load with recovery probing ===")
    # Run 25 concurrent threads continuously for 30s, tracking 429s per second
    concurrency = 25
    run_duration = 30.0
    print(f"\n  {concurrency} threads, {run_duration}s sustained, tracking per-second error rates...")
    time.sleep(5)

    events = []
    events_lock = threading.Lock()
    stop_event = threading.Event()

    def sustained_worker():
        with httpx.Client() as c:
            while not stop_event.is_set():
                t = time.monotonic()
                status, latency = create_instance(c, key)
                with events_lock:
                    events.append({"t": t, "status": status, "latency": latency})

    t_start = time.monotonic()
    threads = []
    for _ in range(concurrency):
        t = threading.Thread(target=sustained_worker, daemon=True)
        t.start()
        threads.append(t)

    time.sleep(run_duration)
    stop_event.set()
    for t in threads:
        t.join(timeout=5)

    # Analyze per-second buckets
    events.sort(key=lambda e: e["t"])
    if events:
        bucket_size = 1.0
        buckets = {}
        for e in events:
            bucket = int((e["t"] - t_start) / bucket_size)
            if bucket not in buckets:
                buckets[bucket] = {"ok": 0, "err429": 0, "other": 0}
            if e["status"] in (200, 201):
                buckets[bucket]["ok"] += 1
            elif e["status"] == 429:
                buckets[bucket]["err429"] += 1
            else:
                buckets[bucket]["other"] += 1

        print(f"\n  Per-second breakdown (first 30s):")
        print(f"  {'Sec':>4}  {'OK':>5}  {'429':>5}  {'Err%':>6}  {'Bar'}")
        for sec in sorted(buckets.keys()):
            b = buckets[sec]
            total = b["ok"] + b["err429"] + b["other"]
            err_pct = b["err429"] / total * 100 if total else 0
            bar_ok = "█" * min(b["ok"], 80)
            bar_err = "░" * min(b["err429"], 80)
            print(f"  {sec:>4}  {b['ok']:>5}  {b['err429']:>5}  {err_pct:>5.1f}%  {bar_ok}{bar_err}")

        total_ok = sum(b["ok"] for b in buckets.values())
        total_429 = sum(b["err429"] for b in buckets.values())
        print(f"\n  Totals: {total_ok} ok, {total_429} x429 ({total_429/(total_ok+total_429)*100:.1f}% error rate)")

        # Find backpressure episode durations
        in_bp = False
        bp_start = 0
        bp_episodes = []
        for sec in sorted(buckets.keys()):
            has_429 = buckets[sec]["err429"] > 0
            if has_429 and not in_bp:
                bp_start = sec
                in_bp = True
            elif not has_429 and in_bp:
                bp_episodes.append(sec - bp_start)
                in_bp = False
        if in_bp:
            bp_episodes.append(max(buckets.keys()) - bp_start + 1)

        if bp_episodes:
            print(f"\n  Backpressure episodes: {len(bp_episodes)}")
            print(f"  Episode durations (seconds): {bp_episodes}")
            print(f"  Avg episode: {statistics.mean(bp_episodes):.1f}s")

    client.close()


if __name__ == "__main__":
    main()
