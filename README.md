# Formaldehyde Scavenger Discovery

CPU-first formulation-discovery workspace for post-installation treatment of exposed particleboard/MDF edges, cuts and holes.

## Goal
Explore many candidate formulations and identify useful **component ratios, interactions, trade-offs and uncertainty** before selecting laboratory experiments.

## v0
The initial dataset is deliberately **synthetic**. It validates the optimization software; it is **not evidence of chemical efficacy, compatibility or safety**.

Pipeline:
1. generate constrained mixture candidates;
2. evaluate a deterministic synthetic benchmark;
3. fit a surrogate model;
4. rank candidates and build a Pareto set;
5. estimate component importance/interactions and useful ranges;
6. propose the next experiments.

Run locally:

```bash
python -m pip install -r requirements.txt
python src/discover.py --out artifacts
pytest -q
```

GitHub Actions runs the same workflow on every push/PR and uploads `artifacts/`.

## Real-data contract
When laboratory data arrives, add it as a separate documented dataset. Keep provenance, units, measurement protocol, substrate/batch, application amount, age, temperature/humidity and uncertainty. Never silently mix synthetic and measured observations.

See issue #1 for bootstrap scope.
