import argparse
from pathlib import Path

VALID_FORMS = {"quadratic", "exponential", "inverse", "log", "oscillatory", "fractional", "linear"}


def validate_positive_int(value, *, name, minimum=1):
    ivalue = int(value)
    if ivalue < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return ivalue


def validate_positive_float(value, *, name, minimum=0.0):
    fvalue = float(value)
    if fvalue < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return fvalue


def validate_weights(raw_weights):
    try:
        values = [float(x) for x in raw_weights.split(",")]
    except Exception as exc:
        raise ValueError("--weights must be two comma-separated floats") from exc
    if len(values) != 2:
        raise ValueError("--weights must contain exactly two values")
    core, osc = values
    if core < 0 or osc < 0:
        raise ValueError("weight values must be non-negative")
    total = core + osc
    if abs(total - 1.0) > 1e-9:
        raise ValueError("weights must sum to 1.0")
    return (core, osc)


def validate_form(name):
    form = str(name)
    if form not in VALID_FORMS:
        raise ValueError(f"Unknown form '{form}'. Allowed: {sorted(VALID_FORMS)}")
    return form


def safe_output_dir(path):
    out_dir = Path(path).expanduser().resolve()
    project_root = Path.cwd().resolve()
    if project_root not in out_dir.parents and out_dir != project_root:
        raise ValueError("Output directory must remain inside the project root")
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def build_parser():
    parser = argparse.ArgumentParser(description="Riemann-Ahmouri synthesis validator")
    parser.add_argument("--matrix-size", type=int, default=100)
    parser.add_argument("--g", type=float, default=0.5)
    parser.add_argument("--nzeros", type=int, default=400)
    parser.add_argument("--out", type=str, default=".")
    parser.add_argument("--form", type=str, default="quadratic")
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--weights", type=str, default="0.49,0.51")
    return parser


def validate_args(args):
    args.matrix_size = validate_positive_int(args.matrix_size, name="--matrix-size", minimum=2)
    args.g = validate_positive_float(args.g, name="--g", minimum=0.0)
    args.nzeros = validate_positive_int(args.nzeros, name="--nzeros", minimum=1)
    args.alpha = validate_positive_float(args.alpha, name="--alpha", minimum=0.0)
    args.form = validate_form(args.form)
    args.weights = validate_weights(args.weights)
    args.out = str(safe_output_dir(args.out))
    return args
