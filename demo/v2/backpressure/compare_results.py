"""Compare baseline (no backoff) vs new (backoff-at-floor) matrix results."""

import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OLD_DIR = os.path.join(BASE, "results-baseline-no-backoff")
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


configs = [
    "sync-instant-sub", "sync-sleep-sub", "sync-http-sub",
    "async-instant-sub", "async-sleep-sub", "async-http-sub",
]

print(f"{'Config':<28} {'OldComp':>7} {'NewComp':>7} {'Comp%':>6} {'OldErr':>7} {'NewErr':>7} {'Err%':>7} {'OldJ':>5} {'NewJ':>5} {'LegComp':>7} {'LegErr':>7}")
print("-" * 120)

for c in configs:
    oc, oe, oj = extract(os.path.join(OLD_DIR, f"25c-B-{c}.txt"))
    nc, ne, nj = extract(os.path.join(NEW_DIR, f"25c-B-{c}.txt"))
    lc, le, lj = extract(os.path.join(OLD_DIR, f"25c-L-{c}.txt"))

    if oc is not None and nc is not None:
        comp_delta = f"{(nc - oc) / oc * 100:+.0f}%" if oc > 0 else "N/A"
        err_delta = f"{(ne - oe) / oe * 100:+.0f}%" if oe and oe > 0 else ("0" if ne == 0 else "N/A")
        leg_comp = str(lc) if lc else "?"
        leg_err = str(le) if le else "?"
        print(
            f"25c-B-{c:<22} {oc:>7} {nc:>7} {comp_delta:>6} "
            f"{oe:>7} {ne:>7} {err_delta:>7} "
            f"{oj:>5.3f} {nj:>5.3f} "
            f"{leg_comp:>7} {leg_err:>7}"
        )
    elif oc is not None:
        print(f"25c-B-{c:<22} {oc:>7} {'...':>7}")

print()
print("OldComp/OldErr = baseline BALANCED (no backoff)")
print("NewComp/NewErr = new BALANCED (backoff-at-floor)")
print("LegComp/LegErr = LEGACY baseline (for throughput reference)")
print()

# Summaries
old_comp_total = sum(extract(os.path.join(OLD_DIR, f"25c-B-{c}.txt"))[0] or 0 for c in configs)
new_comp_total = sum(extract(os.path.join(NEW_DIR, f"25c-B-{c}.txt"))[0] or 0 for c in configs)
old_err_total = sum(extract(os.path.join(OLD_DIR, f"25c-B-{c}.txt"))[1] or 0 for c in configs)
new_err_total = sum(extract(os.path.join(NEW_DIR, f"25c-B-{c}.txt"))[1] or 0 for c in configs)
leg_comp_total = sum(extract(os.path.join(OLD_DIR, f"25c-L-{c}.txt"))[0] or 0 for c in configs)
leg_err_total = sum(extract(os.path.join(OLD_DIR, f"25c-L-{c}.txt"))[1] or 0 for c in configs)

available = sum(1 for c in configs if extract(os.path.join(NEW_DIR, f"25c-B-{c}.txt"))[0] is not None)
print(f"Totals ({available} configs):")
print(f"  Old BALANCED:  completions={old_comp_total}  errors={old_err_total}")
print(f"  New BALANCED:  completions={new_comp_total}  errors={new_err_total}")
print(f"  LEGACY:        completions={leg_comp_total}  errors={leg_err_total}")
if old_comp_total:
    print(f"  Completion delta: {(new_comp_total - old_comp_total) / old_comp_total * 100:+.1f}%")
if old_err_total:
    print(f"  Error delta:      {(new_err_total - old_err_total) / old_err_total * 100:+.1f}%")
