"""Evaluate matrix results."""
import re
import sys

log_path = "demo/v2/backpressure/matrix-run.log"
lines_raw = open(log_path).read()
results = re.findall(
    r"\[([^\]]+)\] => ([\d.]+)/s, (\d+) errors, ([\d.]+)s, Jain=([\d.]+)",
    lines_raw,
)

if not results:
    print("No results found.")
    sys.exit(1)

# Parse into tuples
data = [(n, float(r), int(e), float(t), float(j)) for n, r, e, t, j in results]

# Group by isolation and profile
groups = {
    "BALANCED subprocess": [x for x in data if "sub" in x[0] and "-B-" in x[0]],
    "LEGACY subprocess": [x for x in data if "sub" in x[0] and "-L-" in x[0]],
    "BALANCED shared": [x for x in data if "shr" in x[0] and "-B-" in x[0]],
    "LEGACY shared": [x for x in data if "shr" in x[0] and "-L-" in x[0]],
}

for label, grp in groups.items():
    if not grp:
        continue
    jains = [j for _, _, _, _, j in grp]
    errs = [e for _, _, e, _, _ in grp]
    avg_j = sum(jains) / len(jains)
    avg_e = sum(errs) // len(errs)
    print(f"\n{label}: n={len(grp)}  avgJain={avg_j:.3f}  minJain={min(jains):.3f}  maxJain={max(jains):.3f}  avgErrors={avg_e}")
    for n, r, e, t, j in sorted(grp, key=lambda x: x[4], reverse=True):
        tag = n.replace("25c-", "").replace("50c-", "50-").replace("-sub", "").replace("-shr", "")
        print(f"  {tag:25s}  rate={r:5.1f}/s  errors={e:>7}  elapsed={t:>6.1f}s  Jain={j:.3f}")

# Summary comparison: BALANCED vs LEGACY for subprocess
print("\n" + "=" * 70)
print("BALANCED vs LEGACY comparison (subprocess, independent BP per client)")
print("=" * 70)
b_sub = groups["BALANCED subprocess"]
l_sub = groups["LEGACY subprocess"]
if b_sub and l_sub:
    # Match by mode+workload
    b_map = {}
    for n, r, e, t, j in b_sub:
        key = re.sub(r"25c-[BL]-", "", n).replace("-sub", "")
        b_map[key] = (r, e, t, j)
    l_map = {}
    for n, r, e, t, j in l_sub:
        key = re.sub(r"25c-[BL]-", "", n).replace("-sub", "")
        l_map[key] = (r, e, t, j)

    print(f"  {'config':25s}  {'B-Jain':>7}  {'L-Jain':>7}  {'delta':>7}  {'B-err':>8}  {'L-err':>8}  {'err-reduction':>14}")
    for key in sorted(b_map.keys()):
        if key in l_map:
            bj = b_map[key][3]
            lj = l_map[key][3]
            be = b_map[key][1]
            le = l_map[key][1]
            err_red = f"{(1 - be / le) * 100:.0f}%" if le > 0 else "N/A"
            print(f"  {key:25s}  {bj:>7.3f}  {lj:>7.3f}  {bj - lj:>+7.3f}  {be:>8}  {le:>8}  {err_red:>14}")
