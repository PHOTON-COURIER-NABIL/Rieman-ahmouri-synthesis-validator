import numpy as np
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

import h59_full_positivity_model as model


def test_build_h59_operator_shape():
    H = model.build_H59_operator(N=32, alpha=0.5, form='quadratic')
    assert H.shape == (32, 32)
    assert np.allclose(H, H.T)


def test_positivity_form_returns_error():
    error = model.test_positivity_form(pos_type='quadratic', alpha=0.5, N=24)
    assert error >= 0.0


def test_sweep_positivity_forms_best_match():
    best = model.sweep_positivity_forms(N=24)
    assert isinstance(best, tuple)
    assert best[0] in [
        'quadratic',
        'exponential',
        'inverse',
        'log',
        'oscillatory',
        'fractional',
        'linear',
    ]
    assert best[2] >= 0.0
