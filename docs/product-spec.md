# Product Specification — Post-install Formaldehyde Scavenger

Status: draft v0.2  
Source: product-owner clarification, 2026-10-07

## 1. Problem

Furniture made from particleboard/MDF may require additional cuts during installation inside the customer's apartment or other premises.

Factory-prepared surfaces and edges may already be laminated, edged, sealed or otherwise treated. However, **new cuts made by installers on site expose fresh board material**. These exposed cuts can emit formaldehyde.

Drilled/fastener holes may also expose material and emit formaldehyde, but they are a secondary target: there are fewer of them and they are often subsequently covered by fittings or other elements.

The primary product problem is therefore:

> Reduce formaldehyde emission from fresh, exposed cuts created on site during furniture installation.

## 2. Product concept

Develop a composition that an ordinary furniture installer can apply directly to fresh cuts and, where useful, exposed holes during installation at the customer's premises.

The composition should bind/neutralize formaldehyde and/or reduce its release from the exposed board.

This is **not only a factory-applied treatment**. On-site use after a new cut is a core requirement.

## 3. Primary use flow

1. Furniture boards arrive at the customer substantially factory-prepared.
2. During fitting/installation, an installer makes an additional cut.
3. A fresh particleboard/MDF surface becomes exposed.
4. The installer applies the treatment to that exposed surface.
5. The treatment dries quickly enough not to materially delay installation.
6. The treated area continues to reduce formaldehyde release during the important early period after installation.

## 4. Composition requirements

The composition should:

- be applicable manually on site without complex industrial equipment;
- form no significant thickness and not materially change part dimensions;
- not cause unacceptable swelling of particleboard/MDF;
- dry quickly enough for normal installer workflow;
- have no strong objectionable odor under normal use;
- be suitable for use around installers and occupants subject to validation of the final formulation;
- be inexpensive per treated part/order;
- bind or otherwise suppress a substantial share of formaldehyde released from the treated exposed surface during approximately the first 1–3 months;
- be compatible with common furniture installation materials, including laminate surfaces, edge banding, fittings and silicone/sealant systems;
- leave no noticeable marks on visible finished surfaces when used as intended.

Exact numerical thresholds are TBD and must be defined with the manufacturer and laboratory protocol.

## 5. Discovery objective

Do not search for one guessed formula.

Generate and compare a broad formulation space and determine the **key component ratios and interaction effects** that control useful properties.

For each candidate formulation, eventually evaluate or predict at least:

- formaldehyde capture / emission reduction;
- persistence of effect over time;
- drying time;
- substrate swelling / dimensional effect;
- visible residue / discoloration;
- odor / VOC-related properties;
- compatibility;
- material consumption per treated area;
- cost.

The system should identify:

- Pareto-optimal formulations;
- useful concentration ranges rather than only a single optimum;
- important component ratios;
- synergistic and antagonistic interactions;
- uncertainty;
- the next most informative laboratory experiments.

## 6. Measurement focus

The primary efficacy endpoint should represent **emission reduction over time versus an untreated control**, rather than only immediate capture after application.

Desired observation horizon:

- initial / day 0;
- ~24 hours;
- ~7 days;
- ~30 days;
- ~90 days.

The final laboratory protocol and units are TBD.

Experiments must record substrate type/batch, exposed area, application amount, environmental conditions and measurement method so results are comparable.

## 7. Software / modelling scope

Initial software validates the discovery loop on synthetic data:

`mixture design -> surrogate model -> uncertainty -> multi-objective ranking -> ratio/interaction analysis -> next experiments`

Synthetic benchmark results are **not chemical evidence**.

When real data arrives, measured observations must remain traceable to their provenance and protocol and must not be silently mixed with synthetic observations.

## 8. Future extension — application device

A separate follow-on product direction is a dedicated professional device for controlled application of the composition.

Potential goals:

- fast and repeatable application to fresh cuts;
- controlled dosage per unit area / cut geometry;
- reduced installer contact and mess;
- recording or calculating material consumption;
- potentially sensors/electronics or a chip if they provide real operational value.

The economics differ from a mass-market consumer device: a furniture company may equip a limited number of installers/crews, so higher device cost can be acceptable if it improves repeatability, safety or productivity.

This is **not a blocker for chemistry discovery**. The initial composition should remain usable with a simple application method.

## 9. Data needed later

From manufacturer / laboratory:

- board types and suppliers;
- typical on-site cut geometries and exposed areas;
- current emission measurements if available;
- candidate/allowed and forbidden substances;
- application constraints;
- maximum acceptable drying time;
- dimensional/swelling limits;
- cost target;
- compatibility requirements;
- target formaldehyde reduction and measurement standard;
- real formulation/experiment history, if available.

## 10. Current non-goals

For the bootstrap phase:

- no claim that a synthetic optimum is a real formulation;
- no safety claim without chemical/toxicological evidence;
- no automated recommendation for customer use;
- no need for GPU/DFT/MACE until real data or chemistry questions justify it;
- no detailed engineering of the application device yet.

## 11. Success criterion for discovery phase

Given a documented experimental dataset, the system can generate candidate formulations, compare their trade-offs, expose the most important component ratios/interactions, quantify uncertainty, and propose a small next batch of laboratory experiments that maximally improves the search.
