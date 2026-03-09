#!/usr/bin/env python3
"""Compare error counts between LEGACY and BALANCED from the same run."""
import re, os

def extract(path):
    if not os.path.exists(path):
        return None, None
    txt = open(path).read()
    comp = re.search(r'Total completed:\s+(\d+)', txt)
    err = re.search(r'Total errors:\s+(\d+)', txt)
    return (int(comp.group(1)) if comp else None, int(err.group(1)) if err else None)

configs = [
    'sync-instant-sub', 'sync-sleep-sub', 'sync-http-sub',
    'thread-instant-sub', 'thread-sleep-sub', 'thread-http-sub',
    'async-instant-sub', 'async-sleep-sub', 'async-http-sub',
]

print(f"{'Config':<22} {'LEG Err':>8} {'BAL Err':>8} {'Change':>10}")
print('-' * 52)
tl = tb = 0
for c in configs:
    _, ne = extract(f'results/25c-B-{c}.txt')
    _, le = extract(f'results/25c-L-{c}.txt')
    # fallback to baseline if current-run LEGACY missing
    if le is None:
        _, le = extract(f'results-baseline-no-backoff/25c-L-{c}.txt')
    if ne is not None and le is not None:
        if le > 0:
            change = f'{(ne - le) / le * 100:+.0f}%'
        else:
            change = '0' if ne == 0 else f'+{ne}'
        label = c.replace('-sub', '')
        print(f'{label:<22} {le:>8} {ne:>8} {change:>10}')
        tl += le
        tb += ne

print('-' * 52)
if tl > 0:
    print(f"{'TOTALS':<22} {tl:>8} {tb:>8} {(tb - tl) / tl * 100:+.0f}%")
else:
    print(f"{'TOTALS':<22} {tl:>8} {tb:>8}")
