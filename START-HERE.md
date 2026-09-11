# Ground Truth: first build

## Product
Trace a popular claim back through cited evidence and identify where its meaning changed. Preserve uncertainty; never present an unsupported conclusion as ground truth.

## Cost boundary
Build a standalone Python application. Do not call Codex, launch coding agents, or require this chat to run investigations. External model and sponsor services may incur their own charges. Workflow replay can remove repeated orchestration reasoning, but new evidence may still require model inference.

## First milestone
Investigate the example claim: “Humans can only absorb 30 grams of protein per meal.” This is a claim to investigate, not an accepted fact.

Implement one end-to-end run before adding a polished UI:
1. Accept a claim from the command line.
2. Discover candidate papers and their citation metadata.
3. Retrieve accessible abstracts or full text; record exactly which was available.
4. Extract source-grounded claims with quotations, population, quantity, unit, outcome, intervention, and qualifiers.
5. Compare claims for outcome changes, population changes, generalization, changed units, and inflated causality. Distinguish a verified citation connection from merely similar subject matter.
6. Write a local JSON evidence record and Markdown report with source links, limitations, and an unresolved verdict when evidence is insufficient.

## Intended integrations, pending verification
- RocketRide: execute the pipeline with an independently configured inference provider.
- Cognee: extract structured claims and evidence.
- HydraDB: persist evidence across runs (deferred for submission build).
- Hotdata: query normalized claim records for patterns.
- Rote: capture and reuse a successfully executed workflow.
- Snyk: scan the resulting source and dependencies.

Verify current SDKs, credentials, and the event environment before implementing adapters. The original research report has internal citation markers without accessible source URLs; its API examples are design proposals, not verified integration contracts.

## Evidence record
Each source needs an ID, title, URL/DOI, retrieval timestamp, available text type, exact evidence excerpt, extracted claim, study conditions, and cited-source IDs. Each inferred relationship needs source and target IDs, a transformation label, supporting excerpts, and review status.

## Acceptance checks
- Run from Terminal with Codex closed.
- Every substantive conclusion links to retrieved evidence.
- Missing full text and uncertain lineage remain explicit.
- No invented source counts, dates, citations, or demonstration verdicts.
- Keep original retrieved evidence and per-run outputs for audit and reuse.
- Re-running a saved investigation reuses cached evidence where appropriate.

## Next concrete step
Connect RocketRide and identify the inference provider and available credits. Then implement the first search → evidence → report run. Add the remaining integrations incrementally after that run succeeds.

## Current state
Only the source research report and this build brief exist. No application, external integrations, or paid research jobs have been started.
