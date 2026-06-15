# =====================================================================
# PEAK-ANALYSE
# Je Graph -> Gangzyklus in erste 50 % und letzte 50 % teilen.
# Pro Bedingung (Normal/Medial/Lateral) und Trial:
#   1. Peak  = Extremwert (groesste Auslenkung, Vorzeichen erhalten) in 0-50 %
#   2. Peak  = Extremwert in 50-100 %
# Dazu jeweils der Mittelwert ueber die 3 Trials.
# Ausgabe: Konsole + peaks.csv
# =====================================================================
import csv
from pathlib import Path

import numpy as np

from read import (getFromLabel,
                  normal1, normal2, normal3,
                  medial1, medial2, medial3,
                  lateral1, lateral2, lateral3)

# Zu analysierende Graphen: (Anzeigename, label, source)
METRICS = [
    ('Knee Adduction Moment',   'knee_adduction_l_moment', 'inverse_dynamic'),
    ('Hip Adduction Moment',    'hip_adduction_l_moment',  'inverse_dynamic'),
    ('GRF Medial/Lateral',      '1_ground_force_vz',       'analog'),
    ('Knee Adduction Angle',    'knee_adduction_l',        'inverse_kinematic'),
    ('Hip Adduction Angle',     'hip_adduction_l',         'inverse_kinematic'),
    ('GRF Anterior/Posterior',  '1_ground_force_vx',       'analog'),
]

# Reihenfolge: Normal -> Medial -> Lateral
CONDITIONS = [
    ('Normal',  [normal1, normal2, normal3]),
    ('Medial',  [medial1, medial2, medial3]),
    ('Lateral', [lateral1, lateral2, lateral3]),
]

N_POINTS = 101
SPLIT    = 50.0  # Trennung erste/zweite Haelfte (% Gangzyklus)
CSV_PATH = Path(__file__).parent / 'peaks.csv'


def normalized(trial, label, source, n=N_POINTS):
    """Gefensterte + auf 0-100 % Gangzyklus normalisierte Kurve (x, y)."""
    t = getFromLabel(trial[source], 'time')[1]
    y = getFromLabel(trial[source], label)[1]
    t0, t1 = trial['window']
    mask = (t >= t0) & (t <= t1)
    ts, ys = t[mask], y[mask]
    pct = (ts - ts[0]) / (ts[-1] - ts[0]) * 100
    x = np.linspace(0, 100, n)
    return x, np.interp(x, pct, ys)


def extremeByMagnitude(y):
    """Wert mit der groessten Auslenkung (|.|), Vorzeichen bleibt erhalten."""
    return float(y[np.argmax(np.abs(y))])


def trialPeaks(trial, label, source):
    """(1. Peak in 0-50 %, 2. Peak in 50-100 %)."""
    x, y = normalized(trial, label, source)
    first  = extremeByMagnitude(y[x <= SPLIT])
    second = extremeByMagnitude(y[x >  SPLIT])
    return first, second


def collect():
    """Baut die Ergebniszeilen: [Metrik, Bedingung, Trial, Peak1, Peak2]."""
    rows = []
    for mname, label, source in METRICS:
        for cname, trials in CONDITIONS:
            firsts, seconds = [], []
            for k, tr in enumerate(trials, 1):
                f, s = trialPeaks(tr, label, source)
                firsts.append(f)
                seconds.append(s)
                rows.append([mname, cname, f'{cname} {k}', f, s])
            rows.append([mname, cname, 'Mittelwert',
                         float(np.mean(firsts)), float(np.mean(seconds))])
    return rows


def printTable(rows):
    """Formatierte Tabelle pro Metrik in die Konsole."""
    by_metric = {}
    for r in rows:
        by_metric.setdefault(r[0], []).append(r)

    for mname, mrows in by_metric.items():
        print(f'\n=== {mname} ===')
        print(f'{"":12} {"1. Peak (0-50%)":>18} {"2. Peak (50-100%)":>18}')
        for _, cname, trial, p1, p2 in mrows:
            sep = '-' * 50 if trial == f'{cname} 1' else ''
            if sep:
                print(sep)
            #marker = '  <- Mittel' if trial == 'Mittelwert' else ''
            #print(f'{trial:12} {p1:18.3f} {p2:18.3f}{marker}')
            print(f'{trial:12} {p1:18.3f} {p2:18.3f}')


def writeCsv(rows, path=CSV_PATH):
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['Metrik', 'Bedingung', 'Trial',
                    'Peak1_0_50%', 'Peak2_50_100%'])
        for r in rows:
            w.writerow([r[0], r[1], r[2], f'{r[3]:.6f}', f'{r[4]:.6f}'])
    print(f'\nCSV gespeichert: {path}')


def main():
    rows = collect()
    printTable(rows)
    writeCsv(rows)


if __name__ == '__main__':
    main()
