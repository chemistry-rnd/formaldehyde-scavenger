# Iterative Technology Description Generator — Pipeline

Status: draft v0.1

## Goal

Generate and iteratively refine the project's **Technology Description** as Markdown.

Human-in-the-loop cycle:

```text
product specification
+ discovery/measurement specification
+ accumulated human requirements
+ previous technology-description version
                    ↓
                   LLM
                    ↓
       technology-description-vN.md
                    ↓
               human review
                    ↓
         new feedback / corrections
                    ↓
              next iteration
```

The human remains the source of truth for product requirements. The LLM is a document generator/editor, not an authority that may silently change requirements.

## Inputs

### Stable source documents

- `docs/product-spec.md` — product requirements and scope.
- `docs/discovery-pipeline-and-metrics.md` — measurable endpoints, experiment/discovery logic.
- selected reference/template material adapted from `rnd-forge`.

### Iterative inputs

- `technology-description/feedback.md` — append-only human clarifications/corrections.
- latest generated `technology-description/versions/vNN.md`.
- optional evidence/research files added later.

## Output

Each run creates a **new version**, never overwriting the previous one:

```text
technology-description/
  current.md
  feedback.md
  versions/
    v001.md
    v002.md
    ...
```

`current.md` is a copy of the latest generated version for convenient reading.

## Feedback contract

Human feedback is accumulated, not replaced.

Each feedback entry should contain:

- date / iteration;
- correction or new requirement;
- optional target section;
- status: active / superseded;
- optional reason/source.

Example:

```md
## F-003 — On-site cutting is the primary scenario
Status: active
Target: application scenario

Fresh cuts are made inside the customer's premises during furniture installation.
Do not describe treatment as occurring only after assembly.
```

If two requirements conflict, the generator must **surface the conflict** rather than choose one silently.

## Generation rules

On every iteration the LLM receives:

1. generator system prompt;
2. full product specification;
3. full measurement/discovery specification;
4. all active human feedback;
5. previous generated description, if one exists;
6. optional evidence pack.

It must then:

1. incorporate every active requirement;
2. preserve correct useful material from the previous version;
3. remove statements invalidated by newer feedback;
4. distinguish facts/evidence from hypotheses and proposed R&D;
5. never invent experimental results;
6. never turn unknown numerical targets into asserted values;
7. express measurable targets using the measurement specification;
8. explicitly mark missing information as TBD/question rather than hallucinating;
9. output the complete document, not a patch.

## Suggested document structure

1. Product problem and application scenario
2. Proposed technology / principle of operation
3. Composition R&D direction
4. Formulation-space generation and optimization
5. Key measurable requirements and methods
6. Application process at the customer site
7. Compatibility and safety constraints
8. Experimental validation program
9. Data / modelling / active-learning loop
10. Future application-device direction
11. Technical risks and unresolved questions
12. Expected R&D outputs

This can later be mapped to the fuller `rnd-forge`/Skolkovo technology-description structure when needed.

## LLM configuration

The repository must not contain a real API key.

Expected environment variables:

```text
LLM_API_KEY=
LLM_MODEL=
LLM_BASE_URL=   # optional for OpenAI-compatible providers
```

Provider-specific code should be behind a small adapter so the document workflow does not depend on one model vendor.

## CLI target

Planned interface:

```bash
python -m tech_description generate
```

Optional:

```bash
python -m tech_description generate --feedback technology-description/feedback.md
```

The command should:

1. validate required inputs;
2. determine next version number;
3. assemble prompt/context;
4. call configured LLM;
5. validate that output is Markdown and required sections exist;
6. save immutable `versions/vNN.md`;
7. update `current.md`;
8. emit a small generation manifest.

## Generation manifest

For reproducibility each version should have metadata such as:

```json
{
  "version": "v002",
  "model": "...",
  "generated_at": "...",
  "input_files": {
    "product_spec": "<sha256>",
    "metrics_spec": "<sha256>",
    "feedback": "<sha256>",
    "previous_version": "<sha256>"
  }
}
```

Do not store API keys or full secret-bearing environment state.

## GitHub Actions

Manual workflow:

`workflow_dispatch -> install -> generate -> upload generated MD as artifact`

Initially do **not** automatically commit LLM output to `main`.

Preferred human loop:

1. run generation;
2. download/read generated MD;
3. add corrections to `feedback.md`;
4. rerun;
5. once accepted, commit/promote the chosen version.

Later we may automate creation of a branch/PR containing the new version.

## Acceptance test without a real LLM

CI must support a deterministic mock provider.

Fixture requirements should include at least one correction that contradicts an older draft. Test passes only if the generated/mock pipeline:

- creates the next immutable version;
- preserves previous versions;
- consumes active feedback;
- produces the manifest;
- does not require a live API key for normal CI tests.

## Separation from formulation discovery

This generator creates the **human-readable technical description**.

It does not replace the numerical formulation-discovery pipeline.

```text
formulation discovery → evidence/results → technology description
human requirements ─────────────────────→ technology description
```

As real experimental evidence appears, it becomes an explicit input to later document iterations.
