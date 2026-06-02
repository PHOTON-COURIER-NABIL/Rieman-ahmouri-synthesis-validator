import os
import sys
import pathlib

# Ensure repository root is on sys.path for imports during tests
root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from riemann_ahmouri_validator import RiemannAhmouriValidator


def test_generate_paper_figures_creates_files(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    v = RiemannAhmouriValidator(nzeros=10)
    # run only the figures generator to keep test fast
    v.generate_paper_figures(output_dir=str(out))

    expected = [
        'Figure_1_Crossover_Law.png',
        'Figure_2_LogLog.png',
        'Figure_3_Dimensional_Collapse.png',
        'Figure_4_Dichotomy.png',
        'Figure_5_GUE_Spacing.png',
        'Figure_6_Explicit_Formula.png',
        'Figure_7_59D_Framework.png',
    ]

    for fname in expected:
        assert (out / fname).exists(), f"Missing figure {fname}"
