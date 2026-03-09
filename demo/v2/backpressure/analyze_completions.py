#!/usr/bin/env python3
"""Full matrix analysis using COMPLETIONS as primary metric."""
import re, os

RESULTS = 'results'

def extract(path):
    if not os.path.exists(path):
        return None
    txt = open(path).read()
    comp = re.search(r'Total completed:\s+(\d+)', txt)
    err = re.search(r'Total errors:\s+(\d+)', txt)
    wall = re.search(r'Wall-clock duration:\s+([\d.]+)s', txt)
    jain = re.search(r"Jain's fairness index:\s+([\d.]+)", txt)
    return {
        'completed': int(comp.group(1)) if comp else 0,
        'errors': int(err.group(1)) if err else 0,
        'wall': float(wall.group(1)) if wall else 0,
        'jain': float(jain.group(1)) if jain else 0,
    }

modes = ['sync', 'async', 'thread']
workloads = ['instant', 'sleep', 'http']
isolations = ['sub', 'shr']
scales = ['25c', '50c']

def section(title):
    print(f'\n{"=" * 90}')
    print(f'  {title}')
    print(f'{"=" * 90}')

def show_table(scale, iso):
    header = f"{'Config':<18} {'L comp':>7} {'B comp':>7} {'comp%':>6} {'L err':>8} {'B err':>8} {'err%':>8} {'B jain':>6}"
    print(header)
    print('-' * len(header))

    t_lc = t_bc = t_le = t_be = 0
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

            lc, bc = l['completed'], b['completed']
            le, be = l['errors'], b['errors']
            bj = b['jain']

            if lc > 0:
                cd = (bc - lc) / lc * 100
                cds = f'{cd:+.0f}%'
            elif bc > 0:
                cd = 100
                cds = f'+{bc}'
            else:
                cd = 0
                cds = '0'

            if le > 0:
                eds = f'{(be - le) / le * 100:+.0f}%'
            elif be == 0:
                eds = '0'
            else:
                eds = f'+{be}'

            marker = ''
            if cd >= 2:
                wins += 1
                marker = ' WIN'
            elif cd <= -2:
                losses += 1
                marker = ' LOSS'
            else:
                ties += 1

            print(f'{label:<18} {lc:>7} {bc:>7} {cds:>6} {le:>8} {be:>8} {eds:>8} {bj:>6.3f}{marker}')
            t_lc += lc; t_bc += bc; t_le += le; t_be += be
            pairs += 1

    print('-' * len(header))
    if t_lc > 0:
        cds = f'{(t_bc - t_lc) / t_lc * 100:+.0f}%'
    else:
        cds = 'N/A'
    if t_le > 0:
        eds = f'{(t_be - t_le) / t_le * 100:+.0f}%'
    elif t_be == 0:
        eds = '0'
    else:
        eds = f'+{t_be}'
    print(f"{'TOTALS':<18} {t_lc:>7} {t_bc:>7} {cds:>6} {t_le:>8} {t_be:>8} {eds:>8}")
    print(f'  Wins: {wins}  Ties: {ties}  Losses: {losses}  (of {pairs})')
    return wins, ties, losses, t_lc, t_bc, t_le, t_be

# Run all four quadrants
all_wins = all_ties = all_losses = 0
all_lc = all_bc = all_le = all_be = 0

for scale in scales:
    for iso_label, iso in [('Subprocess (independent BP)', 'sub'), ('Shared (single BP)', 'shr')]:
        section(f'{scale} — {iso_label}')
        w, t, lo, lc, bc, le, be = show_table(scale, iso)
        all_wins += w; all_ties += t; all_losses += lo
        all_lc += lc; all_bc += bc; all_le += le; all_be += be

# Grand summary
section('GRAND SUMMARY (all 36 pairs)')
print(f'  Completions — LEGACY: {all_lc:,}  BALANCED: {all_bc:,}  ({(all_bc-all_lc)/all_lc*100:+.1f}%)')
print(f'  Errors      — LEGACY: {all_le:,}  BALANCED: {all_be:,}  ({(all_be-all_le)/all_le*100:+.1f}%)')
print(f'  Record      — Wins: {all_wins}  Ties: {all_ties}  Losses: {all_losses}  (of {all_wins+all_ties+all_losses})')
print()

# Per-mode rollup
section('PER-MODE ROLLUP')
for mode in modes:
    m_lc = m_bc = m_le = m_be = 0
    for scale in scales:
        for iso in isolations:
            for wl in workloads:
                b = extract(f'{RESULTS}/{scale}-B-{mode}-{wl}-{iso}.txt')
                l = extract(f'{RESULTS}/{scale}-L-{mode}-{wl}-{iso}.txt')
                if b and l:
                    m_lc += l['completed']; m_bc += b['completed']
                    m_le += l['errors']; m_be += b['errors']
    cd = f'{(m_bc-m_lc)/m_lc*100:+.1f}%' if m_lc else 'N/A'
    ed = f'{(m_be-m_le)/m_le*100:+.0f}%' if m_le else ('0' if m_be==0 else f'+{m_be}')
    print(f'  {mode:<8}  completions: {cd:>8}  errors: {ed:>8}  (L:{m_lc:,} B:{m_bc:,})')

# Per-scale rollup
section('PER-SCALE ROLLUP')
for scale in scales:
    s_lc = s_bc = s_le = s_be = 0
    for iso in isolations:
        for mode in modes:
            for wl in workloads:
                b = extract(f'{RESULTS}/{scale}-B-{mode}-{wl}-{iso}.txt')
                l = extract(f'{RESULTS}/{scale}-L-{mode}-{wl}-{iso}.txt')
                if b and l:
                    s_lc += l['completed']; s_bc += b['completed']
                    s_le += l['errors']; s_be += b['errors']
    cd = f'{(s_bc-s_lc)/s_lc*100:+.1f}%' if s_lc else 'N/A'
    ed = f'{(s_be-s_le)/s_le*100:+.0f}%' if s_le else ('0' if s_be==0 else f'+{s_be}')
    print(f'  {scale}  completions: {cd:>8}  errors: {ed:>8}  (L:{s_lc:,} B:{s_bc:,})')

# Per-isolation rollup
section('PER-ISOLATION ROLLUP')
for iso_label, iso in [('subprocess', 'sub'), ('shared', 'shr')]:
    i_lc = i_bc = i_le = i_be = 0
    for scale in scales:
        for mode in modes:
            for wl in workloads:
                b = extract(f'{RESULTS}/{scale}-B-{mode}-{wl}-{iso}.txt')
                l = extract(f'{RESULTS}/{scale}-L-{mode}-{wl}-{iso}.txt')
                if b and l:
                    i_lc += l['completed']; i_bc += b['completed']
                    i_le += l['errors']; i_be += b['errors']
    cd = f'{(i_bc-i_lc)/i_lc*100:+.1f}%' if i_lc else 'N/A'
    ed = f'{(i_be-i_le)/i_le*100:+.0f}%' if i_le else ('0' if i_be==0 else f'+{i_be}')
    print(f'  {iso_label:<12}  completions: {cd:>8}  errors: {ed:>8}  (L:{i_lc:,} B:{i_bc:,})')
