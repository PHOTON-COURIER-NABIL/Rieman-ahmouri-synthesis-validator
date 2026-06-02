# Riemann-Ahmouri Synthesis Validator

**Reproducible Python validator** for the **Riemann Hypothesis** within the spectral & 59D geometric framework proposed by Abdelilah Ahmouri (2026).

![CI](https://github.com/PHOTON-COURIER-NABIL/Rieman-ahmouri-synthesis-validator/actions/workflows/ci.yml/badge.svg)
![Release](https://img.shields.io/github/v/release/PHOTON-COURIER-NABIL/Rieman-ahmouri-synthesis-validator)
![PyPI](https://img.shields.io/pypi/v/rieman-ahmouri-synthesis-validator?label=PyPI)

This repository implements a unified **numerical-symbolic validator** that bridges **mathematics** (analytic number theory and the Riemann zeta function) with **physics** (quantum mechanical spectral operators and 59D geometric models). It tests the emergence of the critical line Re(s) = 0.5 through discretization of an elliptic differential operator inspired by the H59 operator in the positivity wall framework (Elliptic GinOE ensemble).

### Mathematical & Physical Foundation

The Riemann Hypothesis (RH) conjectures that all non-trivial zeros of the Riemann zeta function lie on the critical line Re(s) = 1/2. A long-standing approach to proving RH is the **Hilbert–Pólya conjecture**, which posits that these zeros correspond to the eigenvalues of a self-adjoint operator arising in quantum mechanics.

In the **Ahmouri 59D geometric synthesis**:
- A 1D effective elliptic operator is derived from the 59D compactified geometry.
- The operator takes the form:
  \[
  \mathcal{L}\psi = -\frac{d^2\psi}{dx^2} + (x^2 + g x^4)\psi
  \]
  (where \(g\) is the coupling constant controlling the anharmonic “positivity wall”).
- High-precision numerical discretization (finite-difference method on a large grid) yields a real symmetric matrix whose eigenvalues are analyzed for alignment with the critical line Re(s) = 0.5.
- Symbolic construction (via SymPy) ensures exact operator definition before numerical approximation.
- The model explicitly incorporates **Elliptic Ginibre Orthogonal Ensemble (GinOE)** statistics and the **H59 operator** structure, reproducing key features from the original 2026 paper.

This synthesis demonstrates a concrete **physics-to-mathematics bridge**: the spectral properties of a physically motivated Hamiltonian in a 59D framework naturally generate eigenvalue distributions consistent with the Riemann critical line.

### Features

- **Symbolic operator construction** — Exact differential operator using SymPy.
- **High-accuracy numerical matrix** — Finite-difference discretization (matrix size up to 100+).
- **Eigenvalue computation** — Real-part extraction with SciPy.
- **Critical-line validation** — Automatic percentage calculation and maximum deviation from Re(s) = 0.5.
- **Configurable parameters** — Matrix size and coupling \(g\) for sensitivity studies.
- **Reproducible & documented** — Full traceability from theory to code.

### Installation

```bash
# Clone the repository
git clone https://github.com/PHOTON-COURIER-NABIL/Rieman-ahmouri-synthesis-validator.git
cd Rieman-ahmouri-synthesis-validator

# Install dependencies (recommended)
pip install -r requirements.txt
```

### Usage

```bash
python3 riemann_ahmouri_validator.py
```

### Exemple de sortie

```
=== RIEMANN-AHMOURI SYNTHESIS VALIDATOR v2.0 (with paper figures) ===
Author: Abdelilah Ahmouri (2026) – From Intuition to Judgment + 59D Framework
[INFO] H59 operator constructed symbolically (59D geometric framework).
--- SPECTRAL VALIDATION (From Intuition to Judgment) ---
 [PASS] A2_Crossover_Variance
 [PASS] A4_Trace_Collapse
 [FAIL] A3_Mirror_Symmetry
 [PASS] A7_Symmetry_Positivity_Dichotomy

=== GENERATING PAPER FIGURES (exact match to Ahmouri 2026) ===
7 high-resolution figures (300 dpi) saved to current directory.
```

## Nouveau module H59 positivity wall

Un second script propre a été ajouté pour tester le mur de positivité du modèle H59 analogique.
- Fichier principal : `h59_full_positivity_model.py`
- Documentation rapide : `readme2.md`

Ce module construit un opérateur H59 discret, compare plusieurs formes de terme de positivité et identifie la meilleure forme ainsi que le meilleur paramètre `alpha` en fonction des zéros de la fonction zêta.

### Utilisation rapide du module H59

```bash
python3 h59_full_positivity_model.py --N 64 --alpha 0.5 --form quadratic
python3 h59_full_positivity_model.py --sweep
python3 h59_full_positivity_model.py --compare-zeta
```

Fichiers générés
- Figure_1_Crossover_Law.png
- Figure_2_LogLog.png
- Figure_3_Dimensional_Collapse.png
- Figure_4_Dichotomy.png
- Figure_5_GUE_Spacing.png
- Figure_6_Explicit_Formula.png
- Figure_7_59D_Framework.png

### Remarques

- Le calcul des zéros de la fonction zêta peut être lent si le nombre de zéros est élevé. Le script actuel utilise 100 zéros pour accélérer l'exécution et éviter des conversions coûteuses.
- Pour restaurer 400 zéros, éditez la fonction `generate_paper_figures` dans `riemann_ahmouri_validator.py`.

## Analyse paramétrique (nouveau)

Un utilitaire `analysis.py` a été ajouté pour lancer des explorations paramétriques du modèle H59 et tester plusieurs normalisations d'opérateur.

Usage rapide :

```bash
python3 analysis.py --out results/analysis_results_quick2.csv --quick
```

Résultats rapides sont ajoutés dans le dépôt sous :
- [results/analysis_results_quick2.csv](results/analysis_results_quick2.csv)
- [results/analysis_results_quick2.json](results/analysis_results_quick2.json)

Le script produit également un histogramme des erreurs (PNG) lorsque possible.

### Licence

MIT License © PHOTON-COURIER-NABIL (2026)
