# Technical Architecture — Post-install Formaldehyde Scavenger

Version: v001  
Status: working draft for human review  
Generated from: product specification + discovery/measurement specification + active requirement log  
Evidence status: architecture/hypotheses only; no formulation efficacy is asserted

## 1. Purpose

Develop an R&D system for discovering a practical composition that can be applied by a furniture installer to **fresh particleboard/MDF cuts created at the customer's premises during installation** and that reduces formaldehyde emission from those exposed surfaces.

The project is not limited to finding one candidate recipe. Its core technical objective is to build a reproducible discovery loop that:

1. defines a chemically admissible formulation space;
2. generates many formulation variants;
3. measures or predicts multiple product properties;
4. identifies important component concentrations, ratios and interaction effects;
5. selects a small, informative set of laboratory experiments;
6. learns from those measurements and iterates;
7. preserves evidence and uncertainty so later technical descriptions can distinguish measured facts from hypotheses.

Drilled and fastener holes are a secondary application case. Factory-prepared surfaces are not the primary target.

## 2. System boundaries

The project consists of three related but separable technical systems.

### 2.1 Chemistry discovery system

Owns formulation-space definition, candidate generation, experimental data, property models, uncertainty, multi-objective optimization and active learning.

### 2.2 Measurement and validation system

Owns experimental protocols and raw observations for formaldehyde emission, odor, drying, dimensional change, visible effects, compatibility, application workflow and cost-related consumption.

### 2.3 Application system

Initially this is a simple manual application process suitable for an installer. A controlled-dose professional applicator is a later R&D direction and must not be required for the first chemistry-discovery cycle.

The technical-document generator is outside this repository's scientific architecture. It lives in `rnd-forge` and consumes versioned requirements/evidence from this repository.

## 3. Product use architecture

```text
factory-prepared furniture board
              │
              ▼
delivery to customer premises
              │
              ▼
on-site fitting / additional cutting
              │
              ▼
fresh exposed particleboard/MDF cut
              │
              ▼
apply controlled amount of treatment
              │
              ▼
rapid drying / continuation of installation
              │
              ▼
treated cut during first 1–3 months
              │
              ▼
measure reduced HCHO emission vs matched untreated control
```

The formulation must therefore be optimized not only for chemical formaldehyde capture, but for the complete on-site process.

## 4. Formulation model

A formulation is represented as structured data rather than free text.

At minimum:

```text
Formulation
├── components[]
│   ├── identity
│   ├── functional role
│   ├── mass fraction / concentration
│   ├── provenance
│   └── safety/compatibility evidence state
├── carrier
├── formulation-state variables
│   └── e.g. pH where relevant
├── application dose
└── process conditions
```

Expected functional roles may include:

- formaldehyde scavenger;
- binder/barrier component;
- carrier;
- wetting aid;
- stabilizer;
- other functional additive.

These are roles in the search schema, not a claim that every final formulation requires every role.

All numerical candidate generation must obey mass balance and explicit min/max/combination constraints.

## 5. Search-space generation

### 5.1 Chemical admissibility layer

Before numerical mixture generation, candidate components and combinations are filtered by known constraints:

- permitted/prohibited chemistry;
- known hazard evidence;
- compatibility evidence;
- room-temperature/on-site applicability;
- formulation stability constraints;
- known incompatibilities;
- practical sourcing/cost constraints.

Unknown evidence is represented as `unresolved`, never silently treated as safe or compatible.

### 5.2 Mixture Design of Experiments

The initial candidate matrix is generated deterministically using mixture-aware Design of Experiments.

The design should cover:

- useful boundaries of allowed concentrations;
- interior mixture space;
- pairwise component ratios;
- suspected interactions;
- process/application-dose variation where relevant;
- controls and replicates.

An LLM may help propose chemical families or hypotheses, but it must not be the numerical formulation generator.

### 5.3 Large virtual candidate space

Once enough measurements exist to support models, the system can generate a much larger virtual candidate population.

Each candidate receives:

- predicted endpoints;
- uncertainty;
- feasibility/gate state;
- applicability/domain-distance indicator where available.

The objective is not merely to find the highest predicted score. The system must expose stable **regions** of formulation space and the relationships that produce them.

## 6. Property and measurement architecture

Each human product requirement maps to one or more independently stored endpoints.

### 6.1 Formaldehyde efficacy

Primary comparison:

`reduction(t) = 1 - treated_emission(t) / matched_control_emission(t)`

Candidate time points: initial/day 1, day 7, day 30 and day 90.

Derived endpoints:

- absolute formaldehyde emission;
- reduction at each age;
- integrated 0–90 day emission / AUC;
- integrated reduction versus control;
- persistence/decay of treatment effect.

The main optimization must not reward a formulation that performs strongly only immediately after application.

### 6.2 Odor

“Does not smell” is not represented by one synthetic score.

Two measurement channels are maintained:

**Instrumental emissions**
- TVOC where appropriate;
- relevant individual VOCs;
- formaldehyde separately;
- other relevant aldehydes/volatiles suggested by the actual formulation chemistry.

**Sensory assessment**
- perceived odor intensity;
- acceptability;
- optionally hedonic tone;
- treatment-specific odor detection rate.

These measurements remain separate in the raw dataset. A product gate may later combine them only after a real acceptance criterion is agreed.

### 6.3 Drying and workflow

Store separately:

- tack-free time;
- handling-ready time;
- process-ready time;
- optionally drying/mass-loss curve.

The operational threshold is TBD with installers/manufacturer.

### 6.4 Dimensional effect

Measure:

- thickness change in mm;
- relative thickness change;
- mass uptake;
- local deformation where relevant;
- residual change after drying.

Transient wet swelling and permanent dimensional change are distinct endpoints.

### 6.5 Visible effects

Measure where relevant:

- color difference;
- gloss difference;
- residue/staining assessment;
- accidental-contact/cleanup result on finished surfaces.

### 6.6 Compatibility

Compatibility is represented as a matrix by material/system, including as relevant:

- laminate/melamine;
- edge banding and adhesive;
- silicone/sealants;
- fittings/metals;
- later adhesive operations.

A single universal “compatibility score” should not replace the underlying tests.

### 6.7 Safety

Safety is primarily a **hard evidence gate**, not an ML-generated score.

Evidence may include ingredient classification/SDS, exposure conditions, emissions, pH/irritation-relevant properties and applicable regulatory/occupational requirements.

Unknown safety evidence remains unresolved.

### 6.8 Cost and consumption

Core calculation:

`cost_per_treated_area = formulation_cost_per_mass × applied_mass_per_area`

Derived business metrics can include cost per metre of cut and cost per typical order once representative board thicknesses/geometries are known.

### 6.9 Installer usability

Possible measured endpoints:

- application time per metre/cut;
- dose variance between operators;
- overspread/error rate;
- coverage completeness;
- cleanup time;
- number of process steps.

These measurements later provide requirements for a dedicated applicator.

## 7. Experimental data model

Every raw observation must retain enough context to reproduce and compare it.

Minimum experiment identity:

```text
experiment_id
formulation_id + formulation batch
component identities/lots/fractions
substrate product/type/batch
cut geometry + exposed area
application dose + method + operator
temperature + relative humidity
time since treatment
protocol version
raw endpoint + unit
control/replicate relationship
measurement uncertainty / detection limit
notes/anomalies
```

Raw observations are immutable. Normalized scores and derived features are separate computed datasets.

Synthetic CI fixtures and real measurements must be physically/logically separated and carry an explicit data-source type.

## 8. Modelling architecture

The modelling layer is endpoint-oriented rather than one monolithic “material quality” model.

For each sufficiently populated endpoint:

```text
experimental observations
        ↓
surrogate/property model
        ↓
prediction + uncertainty
        ↓
cross-validation / applicability check
```

For early small-to-medium datasets, Gaussian Processes are a preferred candidate because uncertainty is first-class. Tree/ensemble models can provide nonlinear cross-checks.

A model is not required for an endpoint with insufficient data. The valid output is `insufficient_evidence`.

Chemistry-specific molecular models, MACE/DFT or other expensive simulation layers are optional later additions when a concrete question and suitable representation justify them.

## 9. Ratio and interaction analysis

This is a first-class output, not a visualization added after optimization.

For each meaningful component pair/system, estimate:

- response versus concentration;
- response versus component ratio;
- pairwise interaction;
- diminishing-return region;
- antagonistic region;
- robustness around promising regions;
- uncertainty throughout the map.

Preferred output:

> “Under the measured domain, useful A:B ratios cluster in range X–Y and remain robust across binder range Z.”

rather than:

> “Recipe 1837 is best.”

No numerical range is reported as real until supported by experimental data.

## 10. Multi-objective decision architecture

### 10.1 Hard feasibility gates

Examples:

- prohibited/unresolved critical safety state;
- unacceptable material damage;
- critical compatibility failure;
- impossible on-site process conditions.

Exact gates/thresholds are TBD.

### 10.2 Pareto objectives

Among feasible candidates, optimize multiple endpoints without immediately hiding trade-offs inside one weighted score:

- sustained formaldehyde reduction;
- persistence;
- odor acceptability/emissions;
- drying/process time;
- dimensional effect;
- cost;
- visible effects;
- robustness to dose/operator variation.

The system produces a Pareto frontier and explicit trade-offs.

## 11. Active-learning loop

```text
requirements + admissible chemistry
              ↓
      mixture DoE / candidates
              ↓
       laboratory batch
              ↓
     immutable raw results
              ↓
     endpoint surrogate models
              ↓
 ratios + interactions + Pareto + uncertainty
              ↓
 select next experiments:
   ├── promising
   ├── uncertain
   ├── hypothesis-discriminating
   └── controls/replicates
              ↓
             repeat
```

The next batch should maximize useful information per laboratory experiment, not merely test predicted winners.

## 12. Application-device extension

A later professional applicator may control and record dose, reduce operator variance, accelerate treatment and simplify cleanup.

Potential electronics/sensors/chip are justified only if they improve a measurable process property such as:

- dose accuracy;
- coverage verification;
- consumption logging;
- traceability;
- maintenance/refill workflow.

Device development is a separate workstream. Chemistry v1 must remain testable and usable with a simple manual application method.

## 13. Repository / document architecture

This chemistry repository is the source of truth for the **project state**.

Recommended structure:

```text
docs/
  product-spec.md
  discovery-pipeline-and-metrics.md

technology-description/
  requirements.md
  change-log.md
  current.md
  versions/
    v001.md
    v002.md
    ...
  manifests/
    v001.json
    v002.json
    ...

data/
  synthetic/
  experiments/
  derived/
```

`rnd-forge` owns the reusable generation engine, prompts/templates and provider adapters. It should consume a **pinned chemistry-repository commit** and return a generated document/version. It must not become the authoritative store for this project's requirements.

## 14. Requirements/version lifecycle

For many iterations, separate current truth from history:

### requirements.md
Canonical current set of accepted project requirements. Compact enough to be supplied to every generation.

### change-log.md
Append-only record of requirement changes: what changed, why, source/decision, and which generated version first incorporated it.

### versions/vNN.md
Immutable generated snapshots.

### current.md
Convenience copy/pointer to the accepted latest version.

### manifests/vNN.json
Reproducibility metadata: input commit/hashes, requirement revision, generator/template version, model, output hash and validation state.

Human feedback starts as a proposed change. Once accepted, it is normalized into `requirements.md`, appended to `change-log.md`, and incorporated into a new immutable document version.

## 15. Current unknowns requiring later clarification

- actual board types/suppliers and emission classes;
- target formaldehyde reduction and certification/screening protocol;
- practical maximum installer waiting time;
- acceptable permanent/transient dimensional changes;
- odor acceptance criterion and timing;
- allowed/prohibited chemical components;
- target cost per order/treated area;
- typical cut dimensions and total exposed area per order;
- actual application-dose range;
- compatibility priorities;
- laboratory capabilities and available historical formulation data.

These are explicit TBD inputs, not values to be guessed by the generator.

## 16. Near-term implementation sequence

1. Preserve the synthetic software benchmark as CI only.
2. Finalize requirements/change-log/version storage.
3. Define real experiment/data schemas.
4. Receive manufacturer/laboratory source data.
5. Define the first admissible component/search space.
6. Generate the first mixture DoE batch.
7. Run and ingest measurements.
8. Fit endpoint models only where supported.
9. Produce first real ratio/interaction/Pareto maps.
10. Select the next experiment batch through active learning.
