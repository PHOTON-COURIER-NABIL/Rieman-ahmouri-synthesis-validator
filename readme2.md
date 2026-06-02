# H59 Full Positivity Model

**Auteur : AHMOURI ABDELILAH**

Ce module construit un opérateur H59 discret simple, teste plusieurs formes de mur de positivité, et compare les plus basses valeurs propres aux premiers zéros de la fonction zêta de Riemann.

## Objectif

- Construire un opérateur Hermitien pondéré inspiré du mur de positivité H59.
- Balayer plusieurs formes de terme de positivité.
- Trouver la forme et le paramètre `alpha` qui minimise l'écart moyen entre les plus petites valeurs propres et les zéros de Riemann.

## Fichiers

- `h59_full_positivity_model.py` : module principal
- `readme2.md` : documentation rapide

## Installation

```bash
pip install -r requirements.txt
```

## Exemples d'utilisation

### Exécuter un test rapide

```bash
python3 h59_full_positivity_model.py --N 64 --alpha 0.5 --form quadratic
```

### Balayer toutes les formes de positivité

```bash
python3 h59_full_positivity_model.py --sweep
```

### Comparer les valeurs propres au premier zéro de la zêta

```bash
python3 h59_full_positivity_model.py --compare-zeta
```

## Formes de positivité testées

- `quadratic`
- `exponential`
- `inverse`
- `log`
- `oscillatory`
- `fractional`
- `linear`

## Auteur

AHMOURI ABDELILAH
