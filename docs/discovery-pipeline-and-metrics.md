# Discovery Pipeline and Measurement Metrics

Status: draft v0.1  
Purpose: translate the product requirements in `docs/product-spec.md` into a measurable formulation-search loop.

## 1. Principle

The optimization target is **not one magic formulation**.

The system should generate a broad, chemically admissible formulation space, learn which **component concentrations, ratios and interactions** control performance, and select a small number of high-information formulations for laboratory testing.

Every product-language requirement must be represented as:

`requirement -> measurable endpoint(s) -> protocol -> unit/scale -> direction/threshold -> uncertainty`

Do not collapse subjective requirements such as “does not smell” into a single proxy such as TVOC.

## 2. Formulation representation

Each candidate is a structured record, not free text.

Minimum fields:

- component identity and role;
- concentration / mass fraction;
- carrier fraction;
- optional pH and other formulation-state variables;
- application mass per exposed area;
- substrate type;
- process variables that materially affect performance.

Mixture fractions must obey explicit constraints and mass balance.

Later, chemical descriptors can be added for transfer between chemically related components.

## 3. Candidate-generation loop

### Stage A — define admissible space

For every component define:

- role: scavenger / binder-barrier / carrier / wetting aid / stabilizer / other;
- min/max concentration;
- allowed combinations;
- forbidden combinations;
- process constraints;
- evidence/provenance for why the component is in the search space.

Unknown safety or compatibility is not interpreted as safe.

### Stage B — initial design

Use mixture-aware Design of Experiments rather than random LLM-generated recipes.

The initial design should deliberately cover:

- pure/near-boundary regions where allowed;
- interior mixtures;
- important pairwise ratios;
- replicates and controls;
- untreated board control;
- process-variable variation where needed.

The LLM/research layer may propose chemical families and hypotheses, but deterministic code generates the numerical formulation matrix.

### Stage C — measure

Run the selected formulations against the same documented test protocol.

Store raw measurements and metadata, not only normalized scores.

### Stage D — fit surrogate models

For each endpoint fit a model that can provide:

- predicted value;
- uncertainty;
- cross-validation error;
- applicability/domain-distance indicator where possible.

Start CPU-first. Gaussian Process is preferred once the real dataset is small/moderate and uncertainty matters; tree models can be used as nonlinear cross-checks.

### Stage E — interpret ratios/interactions

Explicitly analyze:

- single-component concentration effects;
- pairwise ratios such as A:B;
- pairwise interaction terms;
- useful concentration windows;
- diminishing returns;
- antagonistic combinations;
- robustness around an optimum.

The output should say “useful region A:B ≈ X–Y” when supported, rather than only “candidate #1837 is best”.

### Stage F — multi-objective selection

Separate **hard gates** from optimization objectives.

A candidate failing a hard safety/process/compatibility gate must not win merely because another score is excellent.

Among feasible candidates, construct a Pareto frontier rather than immediately collapsing all endpoints into one weighted score.

### Stage G — active learning

Choose the next laboratory batch from a mixture of:

- promising candidates (exploitation);
- uncertain candidates (exploration);
- candidates that distinguish competing hypotheses / interaction models;
- replicates/controls for measurement quality.

Repeat until improvements and uncertainty become small enough for the project decision.

## 4. Translating product requirements into metrics

### A. “Binds/reduces formaldehyde”

**Primary metric:** formaldehyde emission rate or chamber concentration from a treated exposed cut relative to an otherwise matched untreated control.

Store both absolute measurement and normalized reduction:

`reduction(t) = 1 - treated_emission(t) / control_emission(t)`

Measure at multiple ages (target draft: day 0/1, 7, 30, 90).

Derived metrics:

- reduction at each time point;
- area under the emission-vs-time curve (AUC) over 0–90 d;
- integrated reduction vs control;
- decay/persistence of treatment effect.

The optimization target should favor sustained reduction, not only a strong day-1 result.

### B. “Does not smell / smells acceptable”

This is **two different measurement families**.

#### B1. Instrumental emissions

Measure, as appropriate:

- TVOC;
- selected individual VOCs associated with formulation ingredients/degradation;
- formaldehyde separately;
- other relevant aldehydes if chemistry suggests them.

This answers “what is emitted?”, but **TVOC alone does not measure whether humans find the odor acceptable**.

#### B2. Sensory odor

Use a blinded sensory protocol with untreated board, treated board and blanks.

Store separately:

- perceived odor intensity;
- odor acceptability;
- optionally hedonic tone (pleasant/unpleasant);
- fraction of panel members detecting a treatment-specific odor.

Assess after application and after relevant drying/aging intervals.

For later formal validation, align the chamber/sensory method with ISO 16000-28 or the applicable laboratory standard.

Candidate product-level gate (TBD from real testing): treatment should not create a materially less acceptable or more intense odor than the untreated/control installation condition after the intended return-to-room time.

### C. “Dries quickly”

Do not use one ambiguous “dry time”.

Measure separately:

- tack-free time;
- time until normal handling/contact is possible;
- time until subsequent installation operation is safe;
- mass-loss/drying curve if useful.

Units: minutes.

The manufacturer should define the operational threshold (for example, the maximum delay tolerated by an installer). Until then this is an optimization direction, not an invented pass/fail number.

### D. “Does not swell / change dimensions”

Measure on standardized exposed-board coupons:

- thickness change, mm;
- relative thickness change, %;
- mass uptake, %;
- optional local edge deformation/warp;
- recovery after drying if relevant.

Compare treated sample to matched untreated/control and to the same specimen baseline.

Important: distinguish transient wet swelling during application from permanent dimensional change after drying.

### E. “Does not leave visible marks”

Use both instrument and human inspection where practical:

- color difference ΔE before/after on accidentally contacted visible surface;
- gloss difference;
- visible residue/staining score under defined lighting;
- edge appearance score.

Also run a misuse/contact test: small accidental contact with laminate/finished surface followed by the intended wipe/cleanup procedure.

### F. “Compatible with furniture materials”

Compatibility is a test matrix, not one scalar.

Test treatment contact with representative:

- laminate/melamine surfaces;
- edge banding and its adhesive;
- silicone/sealants;
- common fittings/materials;
- any later adhesive operation that can contact the treated cut.

Endpoints can include:

- visible damage;
- softening/tack;
- adhesion change;
- cure interference;
- corrosion where relevant;
- bond-strength change where relevant.

Initially store per-material pass/fail plus quantitative measurement where a meaningful standard test exists.

### G. “Safe for installer and occupants”

Do **not** train a model to invent a generic “safety score”.

Use hard evidence gates:

- ingredient hazard classification / SDS data;
- exposure route and concentration;
- relevant VOC/aldehyde emissions;
- pH / irritation-related formulation properties where relevant;
- applicable regulatory/occupational limits;
- final formulation toxicology review where required.

Unknown = unresolved, not pass.

Safety is primarily a feasibility constraint.

### H. “Cheap”

Calculate cost from the actual applied dose:

`cost_per_m2_cut = formulation_cost_per_kg * application_kg_per_m2`

Then estimate:

- cost per metre of typical cut (requires board thickness);
- cost per typical furniture order;
- waste/refill loss;
- later, applicator consumable cost.

This makes concentration-vs-dose tradeoffs explicit.

### I. “Easy for an installer”

Measure workflow rather than asking only for opinion:

- application time per metre / per cut;
- number of steps;
- cleanup time;
- accidental overspread rate;
- dose variability between installers;
- percentage of area successfully covered;
- training time / observed application errors.

Later the dedicated applicator can be evaluated by how much it reduces dose variance, time and errors.

## 5. Proposed optimization structure

### Hard gates

Examples; exact thresholds TBD:

- unresolved/unacceptable safety;
- prohibited component;
- unacceptable compatibility failure;
- permanent dimensional damage;
- unacceptable visible damage;
- process impossible at room/on-site conditions.

### Primary objectives

1. maximize integrated formaldehyde reduction over the target period;
2. maximize persistence / 30–90 d efficacy;
3. minimize sensory odor impact;
4. minimize drying/handling time;
5. minimize dimensional effect;
6. minimize cost per treated area/order.

### Secondary objectives

- minimize visible residue;
- maximize robustness to application-dose variation;
- maximize compatibility breadth;
- maximize shelf/formulation stability when that data exists.

## 6. Suggested experiment record

Each laboratory row should identify:

- formulation_id;
- exact component lot/identity and fractions;
- preparation date/batch;
- substrate product/type/batch;
- cut geometry and exposed area;
- application dose;
- application method;
- operator;
- temperature/RH;
- age since treatment;
- raw endpoint values and units;
- replicate/control relationship;
- protocol version;
- measurement uncertainty / detection limit where available;
- notes/anomalies.

Never overwrite raw results with normalized scores.

## 7. Derived outputs for the discovery system

Each run should produce:

- candidate formulations;
- feasibility/gate results;
- endpoint predictions + uncertainty;
- Pareto frontier;
- component importance;
- ratio-response maps;
- interaction matrix;
- robust optimum regions;
- next laboratory experiments;
- evidence/provenance report.

## 8. Standards anchors (protocol details TBD)

For formaldehyde emission, chamber-based methods for wood products such as ASTM D6007/E1333 or the applicable EN/ISO method are useful anchors; the final laboratory protocol must be selected for the project and target market.

For odor, ISO 16000-28 is a useful anchor because it treats sensory odor from building products/materials in chambers and distinguishes perceived intensity and acceptability.

These references are protocol anchors, not an assertion that every R&D screening experiment must immediately be run as a full certification test.

## 9. Bootstrap vs real chemistry

The current repository's synthetic objective exists only to test software.

When real data arrives:

1. preserve synthetic tests as CI fixtures;
2. add a separate real-data schema;
3. implement the actual measurement endpoints above;
4. fit models only where enough data exists;
5. expose “insufficient evidence” instead of fabricating predictions;
6. use active learning to decide what to measure next.
