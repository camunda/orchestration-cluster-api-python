"""Quick analysis of matrix results — bimodal distribution & Jain comparison."""
import re
import sys
from pathlib import Path

results_dir = Path("demo/v2/backpressure/results")

for f in sorted(results_dir.glob("25c-B-*-sub.txt")):
    data = f.read_text()
    tag = f.stem

    # Parse per-client lines (first occurrence block)
    thrpts = re.findall(r"throughput=([\d.]+)/s", data)
    durations = re.findall(r"elapsed=([\d.]+)s", data)
    errors_list = re.findall(r"errors=(\d+)", data)
    completed_list = re.findall(r"completed=(\d+)", data)
    permits_list = re.findall(r"permits_max=(\d+)", data)

    if not thrpts:
        continue

    t = [float(x) for x in thrpts[:25]]
    d = [float(x) for x in durations[:25]]
    e = [int(x) for x in errors_list[:25]]
    c = [int(x) for x in completed_list[:25]]

    fast = [i for i, dur in enumerate(d) if dur < 60]
    slow = [i for i, dur in enumerate(d) if dur >= 60]

    total_errors = sum(e)
    total_completed = sum(c)

    # Jain fairness on throughput
    if len(t) > 0 and sum(x**2 for x in t) > 0:
        jain = (sum(t) ** 2) / (len(t) * sum(x**2 for x in t))
    else:
        jain = 0

    print(f"\n{'='*60}")
    print(f"  {tag}")
    print(f"{'='*60}")
    print(f"  Clients: {len(t)}")
    print(f"  Fast (<60s): {len(fast)}  Slow (>=60s): {len(slow)}")
    if fast:
        print(f"  Fast avg throughput: {sum(t[i] for i in fast)/len(fast):.1f}/s, avg errors: {sum(e[i] for i in fast)/len(fast):.0f}")
    if slow:
        print(f"  Slow avg throughput: {sum(t[i] for i in slow)/len(slow):.2f}/s, avg errors: {sum(e[i] for i in slow)/len(slow):.0f}")
    print(f"  Total completed: {total_completed}  Total errors: {total_errors}")
    print(f"  Jain (throughput): {jain:.3f}")
    if slow:
        print(f"  Slow clients:")
        for i in slow:
            p = permits_list[i] if i < len(permits_list) else "?"
            print(f"    client-{i+1}: {d[i]:.0f}s, {c[i]} done, {e[i]} errors, permits={p}")
