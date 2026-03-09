#!/usr/bin/env python3
"""Compare 50-client scale results: throughput + errors."""
import re, os

def extract(path):
    if not os.path.exists(path):
        return None, None, None
    txt = open(path).read()
    comp = re.search(r'Total completed:\s+(\d+)', txt)
    err = re.search(r'Total errors:\s+(\d+)', txt)
    thr = re.search(r'Aggregate throughput:\s+([\d.]+)', txt)
    return (
        int(comp.group(1)) if comp else None,
        int(err.group(1)) if err else None,
        float(thr.group(1)) if thr else None,
    )

files_50 = sorted(f for f in os.listdir('results') if f.startswith('50c-'))
print(f'50c files available: {len(files_50)}')
for f in files_50:
    print(f'  {f}')
print()

configs = [
    'sync-instant-sub', 'sync-sleep-sub', 'sync-http-sub',
    'thread-instant-sub', 'thread-sleep-sub', 'thread-http-sub',
    'async-instant-sub', 'async-sleep-sub', 'async-http-sub',
]

header = f"{'Config':<22} {'LEG thr':>8} {'BAL thr':>8} {'thr %':>7} {'LEG err':>8} {'BAL err':>8} {'err %':>8}"
print(header)
print('-' * len(header))

t_lt = t_bt = t_le = t_be = 0
pairs = 0

for c in configs:
    bc, be, bt = extract(f'results/50c-B-{c}.txt')
    lc, le, lt = extract(f'results/50c-L-{c}.txt')
    label = c.replace('-sub', '')

    if bt is not None and lt is not None:
        td = f'{(bt - lt) / lt * 100:+.0f}%'
        if le and le > 0:
            ed = f'{(be - le) / le * 100:+.0f}%'
        elif be == 0:
            ed = '0'
        else:
            ed = f'+{be}'
        print(f'{label:<22} {lt:>8.0f} {bt:>8.0f} {td:>7} {le:>8} {be:>8} {ed:>8}')
        t_lt += lt; t_bt += bt; t_le += le; t_be += be
        pairs += 1
    elif bt is not None:
        print(f'{label:<22} {"---":>8} {bt:>8.0f} {"wait":>7} {"---":>8} {be:>8} {"wait":>8}')

if pairs > 0:
    print('-' * len(header))
    td = f'{(t_bt - t_lt) / t_lt * 100:+.0f}%' if t_lt else 'N/A'
    ed = f'{(t_be - t_le) / t_le * 100:+.0f}%' if t_le else ('0' if t_be == 0 else f'+{t_be}')
    print(f"{'TOTALS':<22} {t_lt:>8.0f} {t_bt:>8.0f} {td:>7} {t_le:>8} {t_be:>8} {ed:>8}")
    print(f'\n{pairs} paired configs available out of 9')
