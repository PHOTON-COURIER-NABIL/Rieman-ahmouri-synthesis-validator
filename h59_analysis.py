"""
AHMOURI ABDELILAH

Comprehensive analysis script for H59 positivity wall models.
This script evaluates all positivity forms, generates comparison plots, and saves
results for extended numerical exploration.
"""

import argparse
import csv
import os
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from h59_full_positivity_model import (
    DEFAULT_FORMS,
    ZETA_ZERO_LIST,
    build_H59_operator,
    mean_zero_error,
)


def evaluate_forms(N, alphas, forms=None, zeros=None):
    if forms is None:
        forms = DEFAULT_FORMS
    if zeros is None:
        zeros = np.array(ZETA_ZERO_LIST[:8])

    results = {form: [] for form in forms}
    win_counts = {form: 0 for form in forms}

    for alpha in alphas:
        best_err = None
        best_form = None
        for form in forms:
            H = build_H59_operator(N, alpha=alpha, form=form)
            evals = np.sort(np.real(np.linalg.eigvalsh(H)))
            err = mean_zero_error(evals, zeros)
            results[form].append(float(err))
            if best_err is None or err < best_err:
                best_err = err
                best_form = form
        win_counts[best_form] += 1

    return results, win_counts


def save_csv(path, forms, alphas, results):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['form'] + [f'{alpha:.3f}' for alpha in alphas])
        for form in forms:
            writer.writerow([form] + [f'{results[form][i]:.6f}' for i in range(len(alphas))])


def plot_error_curves(path, forms, alphas, results):
    plt.figure(figsize=(10, 6))
    for form in forms:
        plt.plot(alphas, results[form], label=form)
    plt.xlabel('alpha')
    plt.ylabel('mean error')
    plt.title('H59 error vs alpha for each positivity form')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()


def plot_error_heatmap(path, forms, alphas, results):
    array = np.array([results[form] for form in forms])
    plt.figure(figsize=(8, 6))
    plt.imshow(array, aspect='auto', cmap='viridis', origin='lower')
    plt.colorbar(label='mean error')
    plt.yticks(range(len(forms)), forms)
    plt.xticks(range(0, len(alphas), 5), [f'{alphas[i]:.2f}' for i in range(0, len(alphas), 5)])
    plt.xlabel('alpha')
    plt.title('Error heatmap for H59 positivity forms')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()


def plot_win_counts(path, win_counts):
    forms = list(win_counts.keys())
    counts = [win_counts[form] for form in forms]
    plt.figure(figsize=(8, 4))
    plt.bar(forms, counts, color='teal')
    plt.xlabel('form')
    plt.ylabel('win count')
    plt.title('Number of alpha values where each form is best')
    plt.grid(axis='y')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()


def plot_rescaled_comparison(path, evals, zeros):
    k = min(len(evals), len(zeros))
    eig = evals[:k]
    z = zeros[:k]
    A = np.vstack([eig, np.ones_like(eig)]).T
    coef, _, _, _ = np.linalg.lstsq(A, z, rcond=None)
    a, b = coef[0], coef[1]
    eig_t = a * eig + b

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, k + 1), eig, 'bo-', label='Eigen (orig)')
    plt.plot(range(1, k + 1), z, 'rx--', label='Zeta zeros')
    plt.plot(range(1, k + 1), eig_t, 'g^-', label='Eigen (rescaled)')
    plt.title(f'Rescaled comparison a={a:.4f}, b={b:.4f}')
    plt.xlabel('index')
    plt.legend()
    plt.grid(True)
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()

    return a, b, float(np.mean(np.abs(eig - z))), float(np.mean(np.abs(eig_t - z)))


def save_summary(path, summary_text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(summary_text)


def make_zip(output_dir, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in os.listdir(output_dir):
            archive.write(os.path.join(output_dir, name), arcname=name)


def run_analysis(output_dir, N=256, alphas=None, forms=None):
    if forms is None:
        forms = DEFAULT_FORMS
    if alphas is None:
        alphas = np.linspace(0.1, 3.0, 30)
    zeros = np.array(ZETA_ZERO_LIST[:8])

    os.makedirs(output_dir, exist_ok=True)
    results, win_counts = evaluate_forms(N, alphas, forms=forms, zeros=zeros)

    save_csv(os.path.join(output_dir, 'h59_full_probabilities.csv'), forms, alphas, results)
    plot_error_curves(os.path.join(output_dir, 'h59_error_curves.png'), forms, alphas, results)
    plot_error_heatmap(os.path.join(output_dir, 'h59_error_heatmap.png'), forms, alphas, results)
    plot_win_counts(os.path.join(output_dir, 'h59_win_counts.png'), win_counts)

    best_form = min(forms, key=lambda f: min(results[f]))
    best_alpha_index = int(np.argmin(results[best_form]))
    best_alpha = float(alphas[best_alpha_index])
    best_err = float(min(results[best_form]))

    H = build_H59_operator(N, alpha=best_alpha, form=best_form)
    evals = np.sort(np.real(np.linalg.eigvalsh(H)))
    a, b, err_before, err_after = plot_rescaled_comparison(
        os.path.join(output_dir, 'h59_rescaled_vs_zeros.png'), evals, zeros
    )

    summary = [
        f'AHMOURI ABDELILAH H59 analysis output',
        f'N = {N}',
        f'forms = {forms}',
        f'alphas = {list(alphas)}',
        f'best overall form = {best_form}',
        f'best alpha for best form = {best_alpha}',
        f'best error = {best_err:.6f}',
        f'rescaled linear a = {a:.6f}',
        f'rescaled linear b = {b:.6f}',
        f'error before rescale = {err_before:.6f}',
        f'error after rescale = {err_after:.6f}',
        '',
        'win counts:',
    ]
    for form in forms:
        summary.append(f'  {form}: {win_counts[form]}')

    save_summary(os.path.join(output_dir, 'h59_analysis_summary.txt'), '\n'.join(summary))
    zip_path = os.path.join(output_dir, 'h59_analysis_results.zip')
    make_zip(output_dir, zip_path)
    return zip_path, summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run full H59 positivity analysis')
    parser.add_argument('--output-dir', type=str, default='/tmp/h59_analysis', help='Directory to save analysis results')
    parser.add_argument('--N', type=int, default=256, help='Grid size for analysis')
    parser.add_argument('--alpha-count', type=int, default=30, help='Number of alpha values to test')
    parser.add_argument('--forms', type=str, nargs='*', default=None, help='Positivity forms to test')
    args = parser.parse_args()

    alphas = np.linspace(0.1, 3.0, args.alpha_count)
    forms = args.forms if args.forms else None
    zip_path, summary = run_analysis(args.output_dir, N=args.N, alphas=alphas, forms=forms)
    print('Saved analysis files to', args.output_dir)
    print('Archive:', zip_path)
    print('\n'.join(summary))
