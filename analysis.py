"""
Parametric analysis for H59 positivity model.
Generates a CSV of parameter combinations, normalization methods, and mean errors
compared to the first Riemann zeta zeros.

Usage:
    python3 analysis.py --out analysis_results.csv [--quick]

"""
import csv
import json
import argparse
import numpy as np
import concurrent.futures
import matplotlib.pyplot as plt
from h59_full_positivity_model import (
    DEFAULT_FORMS,
    ZETA_ZERO_LIST,
    build_H59_operator,
    mean_zero_error,
)

zeros = np.array(ZETA_ZERO_LIST[:8])


def worker(combo):
    N, x_max, weights, form, alpha = combo
    out_rows = []
    try:
        H = build_H59_operator(N, alpha=alpha, form=form, x_min=0.01, x_max=x_max, weights=weights)
        for nm, func in NORMALIZATIONS.items():
            try:
                Hn = func(H)
                evals = np.linalg.eigvalsh(Hn)
                err = mean_zero_error(np.sort(np.real(evals)), zeros)
                out_rows.append((N, x_max, weights[0], weights[1], form, float(alpha), nm, float(err)))
            except Exception:
                out_rows.append((N, x_max, weights[0], weights[1], form, float(alpha), nm, float('nan')))
    except Exception:
        for nm in NORMALIZATIONS.keys():
            out_rows.append((N, x_max, weights[0], weights[1], form, float(alpha), nm, float('nan')))
    return out_rows


def normalize_none(H):
    return H


def normalize_by_max_eig(H):
    evals = np.linalg.eigvalsh(H)
    maxeig = np.max(np.abs(evals))
    if maxeig == 0:
        return H
    return H / maxeig


def normalize_by_trace(H):
    tr = np.trace(H)
    if tr == 0:
        return H
    return H / tr


def scale_first_eig_to_zero(H, target):
    evals = np.linalg.eigvalsh(H)
    first = np.sort(np.real(evals))[0]
    if first == 0:
        return H
    factor = target / first
    return H * factor


NORMALIZATIONS = {
    'none': normalize_none,
    'by_max_eig': normalize_by_max_eig,
    'by_trace': normalize_by_trace,
    'scale_first_to_zero1': lambda H: scale_first_eig_to_zero(H, zeros[0]),
}


def run_analysis(out_path, quick=False):
    if quick:
        Ns = [64, 128]
        x_maxs = [8.0, 15.0]
        weights_list = [(1.0, 0.0), (29 / 59, 1 / 59)]
        alphas = np.linspace(0.5, 3.0, 4)
        forms = DEFAULT_FORMS[:4]
    else:
        Ns = [64, 128, 256]
        x_maxs = [8.0, 10.0, 15.0]
        weights_list = [(1.0, 0.0), (29 / 59, 1 / 59)]
        alphas = np.linspace(0.1, 3.0, 15)
        forms = DEFAULT_FORMS

    rows = []
    combos = []
    for N in Ns:
        for x_max in x_maxs:
            for weights in weights_list:
                for form in forms:
                    for alpha in alphas:
                        combos.append((N, x_max, weights, form, float(alpha)))

    total = len(combos)
    print(f'Running analysis on {total} parameter blocks (x {len(NORMALIZATIONS)} normalizations)')

    # worker is implemented at module level to allow multiprocessing

    # parallel map
    with concurrent.futures.ProcessPoolExecutor() as ex:
        for i, res in enumerate(ex.map(worker, combos), start=1):
            rows.extend(res)
            if i % 25 == 0 or i == total:
                print(f'Progress: {i}/{total} parameter blocks processed')

    # write CSV
    header = ['N', 'x_max', 'weight_core', 'weight_osc', 'form', 'alpha', 'normalization', 'error']
    with open(out_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in rows:
            writer.writerow(r)

    # write JSON summary
    json_out = out_path.rsplit('.', 1)[0] + '.json'
    with open(json_out, 'w') as jf:
        json_rows = [dict(zip(header, r)) for r in rows]
        json.dump({'rows': json_rows}, jf, indent=2)

    # plot histogram of errors
    errors = [r[7] for r in rows if not np.isnan(r[7])]
    if errors:
        plt.figure(figsize=(6,4))
        plt.hist(errors, bins=50)
        plt.title('Distribution of mean errors')
        plt.xlabel('mean error')
        plt.ylabel('count')
        png_out = out_path.rsplit('.', 1)[0] + '.png'
        plt.tight_layout()
        plt.savefig(png_out)
        print(f'Plot saved to {png_out}')

    # print best 10
    rows_sorted = sorted([r for r in rows if not np.isnan(r[7])], key=lambda x: x[7])
    print('\nTop 10 results:')
    for r in rows_sorted[:10]:
        print(f'N={r[0]} x_max={r[1]} weights=({r[2]},{r[3]}) form={r[4]} alpha={r[5]:.2f} norm={r[6]} error={r[7]:.6f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=str, default='analysis_results.csv')
    parser.add_argument('--quick', action='store_true')
    args = parser.parse_args()
    run_analysis(args.out, quick=args.quick)
