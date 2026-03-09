"""Recompute Jain fairness index on completions (not throughput) for all results."""
import re
import os

results_dir = "demo/v2/backpressure/results"
rows = []

for fname in sorted(os.listdir(results_dir)):
    if not fname.endswith(".txt"):
        continue
    path = os.path.join(results_dir, fname)
    text = open(path).read()

    completions = [int(m) for m in re.findall(r"completed=(\d+)", text)]
    if not completions:
        print(f"SKIP {fname}: no completions found")
        continue

    n = len(completions)
    s = sum(float(c) for c in completions)
    s2 = sum(float(c) ** 2 for c in completions)
    jain_c = (s * s) / (n * s2) if s2 > 0 else 0.0

    throughputs = [float(m) for m in re.findall(r"throughput=([\d.]+)/s", text)]
    if throughputs:
        st = sum(throughputs)
        st2 = sum(t * t for t in throughputs)
        jain_t = (st * st) / (n * st2) if st2 > 0 else 0.0
    else:
        jain_t = 0.0

    errors_m = re.findall(r"Total errors:\s*(\d+)", text)
    total_errors = int(errors_m[0]) if errors_m else 0

    label = fname.replace(".txt", "")
    rows.append((label, jain_t, jain_c, total_errors, min(completions), max(completions), sum(completions)))

header = f"{'Label':<35} {'Old(tput)':>10} {'New(comp)':>10} {'Delta':>8} {'Errors':>8} {'Min':>5} {'Max':>5} {'Total':>6}"
print(header)
print("-" * len(header))
for label, jt, jc, err, mn, mx, tot in rows:
    delta = jc - jt
    print(f"{label:<35} {jt:>10.3f} {jc:>10.3f} {delta:>+8.3f} {err:>8} {mn:>5} {mx:>5} {tot:>6}")

# Summary by profile
print("\n\n=== SUMMARY BY PROFILE x ISOLATION ===")
from collections import defaultdict

groups = defaultdict(list)
for label, jt, jc, err, mn, mx, tot in rows:
    parts = label.split("-", 2)
    profile = "BALANCED" if "-B-" in label else "LEGACY"
    isolation = "subprocess" if label.endswith("-sub") else "shared"
    groups[(profile, isolation)].append((jc, err))

for (profile, iso), vals in sorted(groups.items()):
    jains = [v[0] for v in vals]
    errs = [v[1] for v in vals]
    avg_j = sum(jains) / len(jains)
    avg_e = sum(errs) / len(errs)
    print(f"  {profile:>10} {iso:>12}: n={len(vals):>2}  avgJain={avg_j:.3f}  avgErrors={int(avg_e):>8}")

# BALANCED vs LEGACY comparison
print("\n\n=== BALANCED vs LEGACY (subprocess, corrected Jain) ===")
by_config = defaultdict(dict)
for label, jt, jc, err, mn, mx, tot in rows:
    if not label.endswith("-sub"):
        continue
    profile = "B" if "-B-" in label else "L"
    # label: 25c-B-async-http-sub -> extract "25c" and "async-http"
    parts = label.replace("-sub", "").split("-")
    clients = parts[0]
    p = parts[1]
    mode_workload = "-".join(parts[2:])
    by_config[(clients, mode_workload)][profile] = (jc, err, tot)

hdr = f"  {'clients':<8} {'config':<20} {'B-Jain':>8} {'L-Jain':>8} {'delta':>8} {'B-err':>10} {'L-err':>10} {'err-red':>10} {'B-tot':>7} {'L-tot':>7}"
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for (clients, config) in sorted(by_config):
    d = by_config[(clients, config)]
    if "B" in d and "L" in d:
        bj, be, bt = d["B"]
        lj, le, lt = d["L"]
        delta = bj - lj
        err_red = ((le - be) / le * 100) if le > 0 else (0 if be == 0 else -999)
        print(f"  {clients:<8} {config:<20} {bj:>8.3f} {lj:>8.3f} {delta:>+8.3f} {be:>10} {le:>10} {err_red:>9.0f}% {bt:>7} {lt:>7}")
