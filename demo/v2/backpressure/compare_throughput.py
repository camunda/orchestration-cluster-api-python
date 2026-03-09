"""Throughput-focused comparison: New BALANCED vs LEGACY (the competitor)."""

import re
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
BASELINE_DIR = os.path.join(BASE, "results-baseline-no-backoff")
NEW_DIR = os.path.join(BASE, "results")


def extract(path):
    if not os.path.exists(path):
        return None, None, None
    txt = open(path).read()
    comp = re.search(r"Total completed:\s+(\d+)", txt)
    err = re.search(r"Total errors:\s+(\d+)", txt)
    jain = re.search(r"Jain's fairness index:\s+([0-9.]+)", txt)
    return (
        int(comp.group(1)) if comp else None,
        int(err.group(1)) if err else None,
        float(jain.group(1)) if jain else None,
    )


configs_25 = [
    "sync-instant-sub", "sync-sleep-sub", "sync-http-sub",
    "thread-instant-sub", "thread-sleep-sub", "thread-http-sub",
    "async-instant-sub", "async-sleep-sub", "async-http-sub",
]

print("=" * 90)
print("THROUGHPUT COMPARISON: New BALANCED vs LEGACY (completions)")
print("=" * 90)
print(f"{'Config':<28} {'LEGACY':>7} {'NewBAL':>7} {'vs LEG':>7} {'OldBAL':>7} {'vs Old':>7}")
print("-" * 90)

wins = 0
losses = 0
total_new = 0
total_leg = 0
total_old = 0

for c in configs_25:
    # New BALANCED from current run
    nc, ne, nj = extract(os.path.join(NEW_DIR, f"25c-B-{c}.txt"))
    # LEGACY - prefer current run, fall back to baseline
    lc, le, lj = extract(os.path.join(NEW_DIR, f"25c-L-{c}.txt"))
    if lc is None:
        lc, le, lj = extract(os.path.join(BASELINE_DIR, f"25c-L-{c}.txt"))
    # Old BALANCED from baseline
    oc, oe, oj = extract(os.path.join(BASELINE_DIR, f"25c-B-{c}.txt"))

    if nc is not None and lc is not None:
        vs_leg = f"{(nc - lc) / lc * 100:+.0f}%"
        vs_old = f"{(nc - oc) / oc * 100:+.0f}%" if oc else "?"
        marker = " <-- WINS" if nc >= lc else ""
        print(f"25c-B-{c:<22} {lc:>7} {nc:>7} {vs_leg:>7} {oc:>7} {vs_old:>7}{marker}")
        total_new += nc
        total_leg += lc
        if oc:
            total_old += oc
        if nc >= lc:
            wins += 1
        else:
            losses += 1
    elif nc is not None:
        print(f"25c-B-{c:<22} {'?':>7} {nc:>7}")

print("-" * 90)
if total_leg:
    print(f"{'TOTALS':<28} {total_leg:>7} {total_new:>7} {(total_new-total_leg)/total_leg*100:+.0f}% {total_old:>7} {(total_new-total_old)/total_old*100:+.0f}%")
print(f"\nNew BALANCED wins {wins}/{wins+losses} configs vs LEGACY")
