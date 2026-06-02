import os
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from h59_analysis import run_analysis


def test_h59_analysis_creates_archive(tmp_path):
    output_dir = tmp_path / 'analysis'
    zip_path, summary = run_analysis(str(output_dir), N=64, alphas=[0.5, 1.0], forms=['log', 'quadratic'])
    assert os.path.exists(zip_path)
    assert 'best overall form' in '\n'.join(summary)
