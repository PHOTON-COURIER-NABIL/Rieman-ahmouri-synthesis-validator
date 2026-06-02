"""
AHMOURI ABDELILAH

Clean H59 positivity wall model for the 59D operator.
This module builds a simple Hermitian H59 matrix, tests positivity wall functions,
and compares the lowest eigenvalues against known Riemann zeta zero imaginary parts.
"""

import argparse
import numpy as np
from mpmath import mp, zeta as mpmath_zeta

mp.dps = 50

ZETA_ZERO_LIST = [
    14.134725,
    21.022040,
    25.010858,
    30.424876,
    32.935062,
    37.586178,
    40.918719,
    43.327073,
    48.005151,
    49.773832,
]

DEFAULT_FORMS = [
    'quadratic',
    'exponential',
    'inverse',
    'log',
    'oscillatory',
    'fractional',
    'linear',
]


def finite_difference_laplacian(N, x):
    dx = x[1] - x[0]
    main = -2.0 * np.ones(N)
    off = np.ones(N - 1)
    lap = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
    return lap / dx**2


def positivity_wall(x, alpha, form='quadratic'):
    if form == 'quadratic':
        return alpha / (x**2 + 1)
    if form == 'exponential':
        return alpha * np.exp(-x)
    if form == 'inverse':
        return alpha / (x + 1)
    if form == 'log':
        return alpha / (np.log(x + 1.1) + 1)
    if form == 'oscillatory':
        return alpha * np.exp(-0.3 * x) * np.cos(0.8 * x)
    if form == 'fractional':
        return alpha / (x**0.7 + 1)
    if form == 'linear':
        return alpha / (x + 0.1)
    raise ValueError(f'Unknown positivity form: {form}')


def build_H59_operator(
    N,
    alpha=0.5,
    form='quadratic',
    x_min=0.01,
    x_max=15.0,
    weights=(29 / 59, 1 / 59),
):
    x = np.linspace(x_min, x_max, N)
    lap = finite_difference_laplacian(N, x)
    pos = positivity_wall(x, alpha, form)
    oscillator = np.diag(x**2)
    core = -lap + np.diag(pos)
    H = weights[0] * core + weights[1] * oscillator
    return H


def mean_zero_error(eigvals, zeros):
    count = min(len(eigvals), len(zeros))
    return np.mean(np.abs(eigvals[:count] - zeros[:count]))


def optimize_scaling_for_eigvals(evals, zeros, s_min=0.1, s_max=10.0, n_steps=200):
    """Find scalar s minimizing mean_zero_error(s * evals, zeros) by grid search."""
    s_vals = np.linspace(s_min, s_max, n_steps)
    best_s = None
    best_err = None
    evals_sorted = np.sort(np.real(evals))
    for s in s_vals:
        err = mean_zero_error(evals_sorted * s, zeros)
        if best_err is None or err < best_err:
            best_err = err
            best_s = s
    return best_s, best_err


def test_positivity_form(pos_type='quadratic', alpha=1.0, N=64):
    zeros = np.array(ZETA_ZERO_LIST[:8])
    H = build_H59_operator(N, alpha=alpha, form=pos_type)
    evals = np.linalg.eigvalsh(H)
    error = mean_zero_error(np.sort(np.real(evals)), zeros)
    print(f'{pos_type} (alpha={alpha:.2f}): mean error = {error:.6f}')
    return error


def test_all_forms(N=128, forms=None, alphas=None, x_min=0.01, x_max=15.0, weights=(29 / 59, 1 / 59), auto_scale=False, scale_min=0.1, scale_max=10.0, scale_steps=200):
    if forms is None:
        forms = DEFAULT_FORMS
    if alphas is None:
        alphas = np.linspace(0.1, 3.0, 15)

    zeros = np.array(ZETA_ZERO_LIST[:8])
    results = []

    for form in forms:
        for alpha in alphas:
            H = build_H59_operator(N, alpha=alpha, form=form, x_min=x_min, x_max=x_max, weights=weights)
            evals = np.linalg.eigvalsh(H)
            if auto_scale:
                s, err = optimize_scaling_for_eigvals(evals, zeros, s_min=scale_min, s_max=scale_max, n_steps=scale_steps)
                results.append((form, float(alpha), float(err), float(s)))
            else:
                error = mean_zero_error(np.sort(np.real(evals)), zeros)
                results.append((form, float(alpha), float(error)))

    best = min(results, key=lambda x: x[2])
    # print best with optional scale
    if len(best) >= 4:
        print(f'Best match: {best[0]} form, alpha={best[1]:.2f}, error={best[2]:.6f}, scale={best[3]:.4f}')
    else:
        print(f'Best match: {best[0]} form, alpha={best[1]:.2f}, error={best[2]:.6f}')
    return best


def sweep_positivity_forms(N=128, x_min=0.01, x_max=15.0, weights=(29 / 59, 1 / 59), auto_scale=False, scale_min=0.1, scale_max=10.0, scale_steps=200):
    print('Running full positivity wall sweep...')
    best = test_all_forms(N=N, x_min=x_min, x_max=x_max, weights=weights, auto_scale=auto_scale, scale_min=scale_min, scale_max=scale_max, scale_steps=scale_steps)
    return best


def compare_to_zeta_critical_line(num_zeros=5):
    print('Comparing the first zeta zeros on the critical line:')
    for i, t in enumerate(ZETA_ZERO_LIST[:num_zeros], start=1):
        s = 0.5 + t * 1j
        z = mpmath_zeta(s)
        print(f'  t_{i} = {t:.6f}  →  zeta(0.5 + {t:.6f}j) = {z}')


def run_h59_demo(
    N=64,
    alpha=0.5,
    form='quadratic',
    sweep=False,
    compare_zeta=False,
    x_min=0.01,
    x_max=15.0,
    weights=(29 / 59, 1 / 59),
    auto_scale=False,
    scale_min=0.1,
    scale_max=10.0,
    scale_steps=200,
):
    print('AHMOURI ABDELILAH - H59 positivity wall model')
    if sweep:
        best = sweep_positivity_forms(N=N, x_min=x_min, x_max=x_max, weights=weights, auto_scale=auto_scale, scale_min=scale_min, scale_max=scale_max, scale_steps=scale_steps)
        return best

    print(f'Building H59 operator with N={N}, form={form}, alpha={alpha:.2f}')
    H = build_H59_operator(N, alpha=alpha, form=form, x_min=x_min, x_max=x_max, weights=weights)
    eigvals = np.linalg.eigvalsh(H)
    zeros = np.array(ZETA_ZERO_LIST[:8])
    if auto_scale:
        s, error = optimize_scaling_for_eigvals(eigvals, zeros, s_min=scale_min, s_max=scale_max, n_steps=scale_steps)
        print(f'  Applied auto-scale factor: {s:.6f}')
    else:
        error = mean_zero_error(np.sort(np.real(eigvals)), zeros)
    print(f'  First eigenvalues: {np.sort(np.real(eigvals))[:5]}')
    print(f'  Mean error vs. first zeros: {error:.6f}')

    if compare_zeta:
        compare_to_zeta_critical_line(num_zeros=min(5, len(zeros)))

    return float(error)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='H59 positivity wall model for the Riemann zeta operator'
    )
    parser.add_argument('--N', type=int, default=64, help='Grid size for the operator')
    parser.add_argument('--alpha', type=float, default=0.5, help='Positivity wall amplitude')
    parser.add_argument('--form', type=str, default='quadratic', help='Positivity form')
    parser.add_argument('--sweep', action='store_true', help='Run full form sweep')
    parser.add_argument('--compare-zeta', action='store_true', help='Show zeta values on critical line')
    parser.add_argument('--x-min', type=float, default=0.01, help='Minimum x value for grid')
    parser.add_argument('--x-max', type=float, default=15.0, help='Maximum x value for grid')
    parser.add_argument('--weights', type=str, default=f"{29/59},{1/59}", help='Comma-separated weights for core and oscillator, e.g. "0.5,0.5"')
    parser.add_argument('--auto-scale', action='store_true', help='Automatically scale operator to minimize error')
    parser.add_argument('--scale-min', type=float, default=0.1, help='Minimum scale factor for auto-scaling')
    parser.add_argument('--scale-max', type=float, default=10.0, help='Maximum scale factor for auto-scaling')
    parser.add_argument('--scale-steps', type=int, default=200, help='Number of steps for scale grid search')
    args = parser.parse_args()

    # parse weights
    try:
        wparts = [float(x) for x in args.weights.split(',')]
        if len(wparts) != 2:
            raise ValueError
        weights = (wparts[0], wparts[1])
    except Exception:
        raise ValueError('Invalid --weights format. Use two comma-separated floats, e.g. "0.8,0.2"')

    run_h59_demo(
        N=args.N,
        alpha=args.alpha,
        form=args.form,
        sweep=args.sweep,
        compare_zeta=args.compare_zeta,
        x_min=args.x_min,
        x_max=args.x_max,
        weights=weights,
        auto_scale=args.auto_scale,
        scale_min=args.scale_min,
        scale_max=args.scale_max,
        scale_steps=args.scale_steps,
    )
