import numpy as np
import sys
import pathlib
root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from riemann_ahmouri_validator import RiemannAhmouriValidator


def test_sample_elliptic_ginoe_shape():
    v = RiemannAhmouriValidator(matrix_size=20)
    M = v.sample_elliptic_ginoe()
    assert M.shape == (20,20)
    # symmetric + skew part scaled


def test_cli_defaults_run(tmp_path, capsys):
    v = RiemannAhmouriValidator(nzeros=5)
    # smoke run methods
    v.symbolic_operator_construction()
    v.execute_spectral_checks()
    v.generate_paper_figures(output_dir=str(tmp_path))
    out = capsys.readouterr()
    assert 'H59 operator constructed symbolically' in out.out
    # check at least one figure file exists
    assert (tmp_path / 'Figure_1_Crossover_Law.png').exists()
