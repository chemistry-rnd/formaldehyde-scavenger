# Canonical Project Requirements

Revision: R001  
Status: active

This file is the compact source of truth for accepted requirements supplied to every Technology Description generation. Detailed rationale remains in source specs and `change-log.md`.

## Product
- Treat fresh exposed particleboard/MDF cuts created at the customer's premises during furniture installation.
- Drilled/fastener holes are secondary.
- Treatment must be usable manually on site without complex industrial equipment.
- Dedicated controlled-dose application equipment is a future optional workstream, not a dependency for chemistry discovery.

## Composition
- No significant added thickness or unacceptable dimensional change.
- No unacceptable board swelling.
- Fast enough drying for installer workflow; numerical threshold TBD.
- No strong objectionable treatment odor; define with instrumental + sensory endpoints.
- Safety must be evidence-gated; unknown is unresolved, not safe.
- Low cost per treated area/order.
- Target sustained formaldehyde reduction over approximately the first 1–3 months.
- Compatibility with relevant furniture surfaces, edge systems, fittings, silicone/sealants and installation materials.
- No noticeable visible damage/residue when used as intended.

## Discovery
- Generate many admissible formulations rather than guess one recipe.
- Identify component concentration windows, ratios, synergistic/antagonistic interactions and robust regions.
- Preserve uncertainty.
- Use multi-objective/Pareto selection.
- Use active learning to select informative laboratory experiments.
- LLM may assist chemical hypothesis generation/documentation but must not numerically invent formulations or experimental evidence.

## Measurement
- Compare treated exposed cuts against matched untreated controls.
- Track formaldehyde efficacy over time; draft ages include day 0/1, 7, 30, 90.
- Keep raw endpoints and metadata; never replace them with only aggregate scores.
- Odor requires both chemical-emission and sensory assessment; TVOC alone is insufficient.
- Synthetic benchmark data is never chemistry evidence.

## Documentation
- Chemistry repository owns project requirements, evidence and generated version history.
- `rnd-forge` owns the reusable document-generation engine.
- Every generation consumes a pinned chemistry repo revision.
- Previous generated prose is lower authority than accepted requirements and verified evidence.
- Missing facts remain TBD/questions rather than being fabricated.
