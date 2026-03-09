#!/usr/bin/env python3
"""Full matrix analysis: BALANCED vs LEGACY across all 72 configs."""
import re, os

RESULTS = 'results'

def extract(path):
    if not os.path.exists(path):
        return None
    txt = open(path).read()
    comp = re.search(r'Total completed:\s+(\d+)', txt)
    err = re.search(r'Total errors:\s+(\d+)', txt)
    thr = re.search(r'Aggregate throughput:\s+([\d.]+)', txt)
    wall = re.search(r'Wall-clock duration:\s+([\d.]+)s', txt)
    jain = re.search(r"Jain's fairness index:\s+([\d.]+)", txt)
    return {
        'completed': int(comp.group(1)) if comp else 0,
        'errors': int(err.group(1)) if err else 0,
        'throughput': float(thr.group(1)) if thr else 0,
        'wall': float(wall.group(1)) if wall else 0,
        'jain': float(jain.group(1)) if jain else 0,
    }

modes = ['sync', 'async', 'thread']
workloads = ['instant', 'sleep', 'http']
isolations = ['sub', 'shr']
scales = ['25c', '50c']

def section(title):
    print(f'\n{"=" * 80}')
    print(f'  {title}')
    print(f'{"=" * 80}')

def show_table(scale, iso):
    header = f"{'Config':<18} {'L thr':>7} {'B thr':>7} {'thr%':>6} {'L err':>7} {'B err':>7} {'err%':>8} {'L jain':>6} {'B jain':>6}"
    print(header)
    print('-' * len(header))

    t_lt = t_bt = t_le = t_be = 0
    wins = ties = losses = 0
    pairs = 0

    for mode in modes:
        for wl in workloads:
            label = f'{mode}-{wl}'
            b = extract(f'{RESULTS}/{scale}-B-{mode}-{wl}-{iso}.txt')
            l = extract(f'{RESULTS}/{scale}-L-{mode}-{wl}-{iso}.txt')
            if b is None or l is None:
                print(f'{label:<18} {"(missing)":>50}')
                continue

            lt, bt = l['throughput'], b['throughput']
            le, be = l['errors'], b['errors']
            lj, bj = l['jain'], b['jain']

            if lt > 0:
                td = (bt - lt) / lt * 100
                tds = f'{td:+.0f}%'
            else:
                td = 0
                tds = 'N/A'

            if le > 0:
                eds = f'{(be - le) / le * 100:+.0f}%'
            elif be == 0:
                eds = '0'
            else:
                eds = f'+{be}'

            marker = ''
            if td >= 2:
                wins += 1
                marker = ' *'
            elif td <= -2:
                losses += 1
                marker = ' !'
            else:
                ties += 1

            print(f'{label:<18} {lt:>7.0f} {bt:>7.0f} {tds:>6} {le:>7} {be:>7} {eds:>8} {lj:>6.3f} {bj:>6.3f}{marker}')
            t_lt += lt; t_bt += bt; t_le += le; t_be += be
            pairs += 1

    print('-' * len(header))
    if t_lt > 0:
        tds = f'{(t_bt - t_lt) / t_lt * 100:+.0f}%'
    else:
        tds = 'N/A'
    if t_le > 0:
        eds = f'{(t_be - t_le) / t_le * 100:+.0f}%'
    elif t_be == 0:
        eds = '0'
    else:
        eds = f'+{t_be}'
    print(f"{'TOTALS':<18} {t_lt:>7.0f} {t_bt:>7.0f} {tds:>6} {t_le:>7} {t_be:>7} {eds:>8}")
    print(f'  Wins: {wins}  Ties: {ties}  Losses: {losses}  (of {pairs})')
    print(f'  (* = BALANCED wins >=2%, ! = BALANCED loses >=-2%)')
    return wins, ties, losses, t_lt, t_bt, t_le, t_be

# Run all four quadrants
all_wins = all_ties = all_losses = 0
all_lt = all_bt = all_le = all_be = 0

for scale in scales:
    for iso_label, iso in [('Subprocess (independent BP)', 'sub'), ('Shared (single BP)', 'shr')]:
        section(f'{scale} — {iso_label}')
        w, t, lo, lt, bt, le, be = show_table(scale, iso)
        all_wins += w; all_ties += t; all_losses += lo
        all_lt += lt; all_bt += bt; all_le += le; all_be += be

# Grand summary
section('GRAND SUMMARY (all 36 pairs)')
print(f'  Throughput — LEGACY: {all_lt:.0f}  BALANCED: {all_bt:.0f}  ({(all_bt-all_lt)/all_lt*100:+.1f}%)')
print(f'  Errors     — LEGACY: {all_le}  BALANCED: {all_be}  ({(all_be-all_le)/all_le*100:+.1f}%)')
print(f'  Record     — Wins: {all_wins}  Ties: {all_ties}  Losses: {all_losses}  (of {all_wins+all_ties+all_losses})')
print()

# Per-mode rollup
section('PER-MODE ROLLUP')
for mode in modes:
    m_lt = m_bt = m_le = m_be = 0
    for scale in scales:
        for iso in isolations:
            for wl in workloads:
                b = extract(f'{RESULTS}/{scale}-B-{mode}-{wl}-{iso}.txt')
                l = extract(f'{RESULTS}/{scale}-L-{mode}-{wl}-{iso}.txt')
                if b and l:
                    m_lt += l['throughput']; m_bt += b['throughput']
                    m_le += l['errors']; m_be += b['errors']
    td = f'{(m_bt-m_lt)/m_lt*100:+.1f}%' if m_lt else 'N/A'
    ed = f'{(m_be-m_le)/m_le*100:+.0f}%' if m_le else ('0' if m_be==0 else f'+{m_be}')
    print(f'  {mode:<8}  thr: {td:>7}  err: {ed:>8}')

# Per-scale rollup
section('PER-SCALE ROLLUP')
for scale in scales:
    s_lt = s_bt = s_le = s_be = 0
    for iso in isolations:
        for mode in modes:
            for wl in workloads:
                b = extract(f'{RESULTS}/{scale}-B-{mode}-{wl}-{iso}.txt')
                l = extract(f'{RESULTS}/{scale}-L-{mode}-{wl}-{iso}.txt')
                if b and l:
                    s_lt += l['throughput']; s_bt += b['throughput']
                    s_le += l['errors']; s_be += b['errors']
    td = f'{(s_bt-s_lt)/s_lt*100:+.1f}%' if s_lt else 'N/A'
    ed = f'{(s_be-s_le)/s_le*100:+.0f}%' if s_le else ('0' if s_be==0 else f'+{s_be}')
    print(f'  {scale}  thr: {td:>7}  err: {ed:>8}')

# Per-isolation rollup
section('PER-ISOLATION ROLLUP')
for iso_label, iso in [('subprocess', 'sub'), ('shared', 'shr')]:
    i_lt = i_bt = i_le = i_be = 0
    for scale in scales:
        for mode in modes:
            for wl in workloads:
                b = extract(f'{RESULTS}/{scale}-B-{mode}-{wl}-{iso}.txt')
                l = extract(f'{RESULTS}/{scale}-L-{mode}-{wl}-{iso}.txt')
                if b and l:
                    i_lt += l['throughput']; i_bt += b['throughput']
                    i_le += l['errors']; i_be += b['errors']
    td = f'{(i_bt-i_lt)/i_lt*100:+.1f}%' if i_lt else 'N/A'
    ed = f'{(i_be-i_le)/i_le*100:+.0f}%' if i_le else ('0' if i_be==0 else f'+{i_be}')
    print(f'  {iso_label:<12}  thr: {td:>7}  err: {ed:>8}')
