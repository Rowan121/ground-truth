# Self-Improving “Ground Truth” Research Agent

## The architecture

The simplest version is **not five websites you manually bounce between**. You use their dashboards once for setup, then your application connects them by API/SDK.

```text
                    ┌── Cognee ──► structured claims/evidence ──► HydraDB ──┐
CLAIM ─► RocketRide ┤                                                       ├─► VERDICT + ARTICLE
                    └── Search/APIs ─► Hotdata ─► pattern/contradiction ────┘
                                           │
                                  Rote remembers workflow
                                           │
                                  run #2+ = replay/repair

                              Snyk scans the codebase
```

That is essentially the hackathon's own page-5 architecture, adapted specifically to the Self-Improving Research Assistant idea on page 6. The guide explicitly assigns Cognee to extracting claims/sources/contradictions, HydraDB to the evolving research graph, Hotdata to querying live papers/signals, RocketRide to autonomous research execution, and Rote to turning the successful research path into a reusable pipeline. fileciteturn0file0

## The important part: you do **not** live inside all their interfaces

I would build **one Python project**, with **RocketRide as the thing you run**.

| Product | Where you actually touch it | What happens after setup |
|---|---|---|
| **RocketRide** | VS Code RocketRide extension / your Python app | Runs the whole research pipeline. RocketRide supports visual `.pipe` pipelines plus Python/TypeScript SDK execution. citeturn2search0turn2search6 |
| **Cognee** | Cognee Cloud once to get API key | Your code sends papers/articles to `remember()` and retrieves the resulting graph. Cognee supports a custom graph model and extraction prompt, and exposes dataset nodes + edges through its graph endpoint. citeturn0search4turn5search0turn5search11turn5search14 |
| **HydraDB** | Dashboard once for API key/tenant/connection | Your code writes/recalls the long-term evidence graph. HydraDB has Python/Node SDKs, a CLI, API tenants, and graph-enriched retrieval. citeturn8search1turn8search5 |
| **Hotdata** | CLI once: login/create DB | RocketRide sends it tables and SQL. Hotdata can load CSV/Parquet and execute SQL/vector/full-text queries through CLI or HTTP API. citeturn1search0turn1search1turn1search11 |
| **Rote** | Terminal / Codex / Claude Code | Records the successful sequence and turns it into a reusable Play. It can record API calls, local CLI/process calls, and browser actions. citeturn3search2turn3search11 |
| **Snyk** | Terminal | `snyk test` and `snyk code test` before submission. citeturn3search3turn3search4 |

So your repo effectively has:

```text
.env
research.pipe        ← RocketRide
research.py          ← glue code
extract.py           ← Cognee
memory.py            ← HydraDB
analyze.py           ← Hotdata
publish.py
```

**The dashboards are control panels. Your code is the integration.**

## What the product should actually discover

I would tighten your idea from “AI that finds the ground truth” to:

> **An AI that traces popular claims back through their evidence lineage and detects where the claim changed.**

That is much more defensible and actually makes the graph architecture useful.

For every source, Cognee should extract a tiny ontology like:

```text
SOURCE ──ASSERTS──► CLAIM
  │                  │
  └──CITES──► SOURCE │
                     ├── population
                     ├── quantity
                     ├── unit
                     ├── intervention
                     ├── outcome
                     └── qualifiers
```

Then classify transformations between claims:

```text
SUPPORTED
CONTRADICTS
GENERALIZED
UNIT_CHANGED
POPULATION_CHANGED
OUTCOME_CHANGED
CAUSALITY_INFLATED
CITATION_MISSING
```

Cognee is particularly useful here because its current API lets you supply both a **custom extraction prompt** and a **custom graph model**, rather than hoping generic entity extraction happens to discover the relationships you care about. citeturn5search0turn5search14

Your protein example demonstrates exactly why this matters. A 2013 study often relevant to this discussion tested **0, 10, 20, or 40 g of whey protein isolate in resistance-trained young men** and measured *myofibrillar muscle protein synthesis* over a defined post-exercise period; it concluded that 20 g was sufficient to maximally stimulate that specific outcome under those conditions. That is very different from the universal claim “humans cannot absorb more than ~30 g of protein.” citeturn6search0 A later whole-body resistance-exercise study found a greater MPS response with **40 g than 20 g** in young resistance-trained men, which further illustrates why the agent must retain study conditions rather than propagating a naked number. citeturn6search1

That is your product's “aha” moment:

```text
Internet claim:
"You can only absorb 30 g"

        ↓ trace provenance

Actual evidence:
20 g → particular MPS endpoint
      particular subjects
      particular protein
      particular exercise
      particular time window

        ↓

⚠ CLAIM DRIFT DETECTED
Outcome changed: "maximal MPS" → "absorption"
Scope changed: study population → all humans
```

## How each sponsor becomes genuinely load-bearing

**RocketRide starts the investigation.** Give it a claim such as `"You can only absorb 30g of protein per meal"`. It calls scholarly metadata/search sources, retrieves relevant papers and citation neighborhoods, invokes Cognee, queries HydraDB/Hotdata, and finally generates the report. RocketRide pipelines are portable JSON and can be driven visually in VS Code or through the Python SDK, so this can be one visible pipeline for the judges. citeturn2search0turn2search5

For literature discovery, use something like **Crossref + Semantic Scholar** rather than general Google results alone. Crossref exposes bibliographic metadata, references and post-publication metadata, while Semantic Scholar's Academic Graph API exposes paper references and citations—exactly what you need to walk backward through a claim's citation ancestry. citeturn6search3turn7search0

**Cognee reads the actual evidence.** Feed it abstracts/full text/web pages and force extraction into `Study`, `Claim`, `Quantity`, `Unit`, `Population`, `Outcome`, `Source`, and `Citation` nodes. Cognee's `remember()` builds the graph in one operation, and the graph can subsequently be retrieved as nodes and edges. citeturn5search3turn5search11

**HydraDB is the permanent accumulated research memory.** After Cognee finishes a source, synchronize its structured claim/evidence relationships into your Hydra research tenant. Then later investigations can ask things such as *“Have we previously seen this number?”*, *“Which claims ultimately descend from this paper?”*, or *“What evidence has changed since we last investigated this topic?”* The hackathon guide explicitly wants HydraDB to persist the evolving research graph across sessions. fileciteturn0file0 HydraDB's current public interfaces support tenant-scoped durable knowledge/memory and graph-enriched recall, and HydraDB also advertises compatibility with Neo4j Bolt 5.x clients and a practical subset of OpenCypher. citeturn4search0turn8search0

**Hotdata finds suspicious patterns at scale.** Do *not* make Hotdata another memory store. Export a normalized table like:

```text
claim_id | number | unit | population | outcome | year | cites_source
```

Then ask SQL questions such as:

```sql
SELECT normalized_number, unit, COUNT(*) AS mentions
FROM claims
GROUP BY normalized_number, unit
ORDER BY mentions DESC;
```

or find hundreds of downstream sources ultimately dependent on a single experiment. Hotdata is specifically built for SQL/search over loaded or connected data, including direct Parquet/CSV loading and cross-source analytical queries. citeturn1search1turn1search2

**Rote becomes the actual “self improving” story.** Research claim #1 normally: search → fetch → citation expansion → Cognee extraction → Hydra synchronization → Hotdata analysis → publish. Run those successful external actions through Rote. Rote records API/process/browser actions into one workspace and can crystallize the successful trace into a parameterized Play; subsequent runs use fresh inputs without rediscovering the tool path. citeturn3search2turn3search10

Your demo becomes:

```text
FIRST CLAIM
"30 g protein"
Agent reasons + discovers workflow
             ↓
        SAVE AS ROTE PLAY
             ↓
SECOND CLAIM
"some other viral rule"
Same proven research procedure
+ new evidence
+ old Hydra memory
```

That is **exactly** the hackathon's required “memory → muscle memory” narrative. fileciteturn0file0

## The one integration wrinkle I would solve first

There is one genuine seam that the PDF makes sound easier than the public docs currently do: **Cognee → HydraDB**.

The hackathon guide says Cognee constructs the graph and HydraDB should be its durable backing store. fileciteturn0file0 Cognee's current public documentation does **not** list HydraDB as a built-in graph adapter; it documents a generic adapter interface for adding new graph databases. citeturn0search3 HydraDB, meanwhile, says it supports Neo4j-compatible Bolt 5.x clients/OpenCypher, while its newer public API is primarily organized around knowledge, memory, recall, and graph context. citeturn8search0turn8search1

So for an eight-hour hackathon, **do not write a giant integration**.

Use this bridge:

```text
Cognee
  GET dataset graph
       ↓
  nodes[] + edges[]
       ↓
~30 lines Python
       ↓
HydraDB
```

Cognee's dataset graph API already returns node IDs, labels, properties, sources, targets, and edge labels. citeturn5search11 If the HydraDB hackathon instance gives you the Bolt/OpenCypher connection string promised by the guide, write those nodes/edges with `MERGE` through a Neo4j-compatible driver; HydraDB explicitly advertises that compatibility. citeturn8search0 If the event instance instead exposes only the current Hydra API, serialize each structured claim/evidence record and ingest it through the Hydra SDK, which can infer and retain graph context. citeturn8search5turn8search6

**That little adapter is the only custom glue that should feel “hard.” Everything else is normal API calls.**

## What I would ship tonight

Make the product **one search box**:

> **What claim should I investigate?**

And return one beautiful card:

```text
┌───────────────────────────────────────────────────┐
│ CLAIM: "You can only absorb 30 g protein/meal"    │
│                                                   │
│ VERDICT: ⚠ Evidence was over-generalized          │
│                                                   │
│ Earliest evidence found: 2009 / 2013 studies      │
│ Citation descendants: 184                         │
│ Main distortion: MPS → total protein absorption   │
│ Population drift: trained young men → everyone    │
│ Contradictory/later evidence: found               │
│                                                   │
│ [See evidence chain]  [Read publishable report]   │
└───────────────────────────────────────────────────┘
```

Under that card, show the **Hydra/Cognee provenance chain** visually and a tiny badge:

```text
Run 1:  discovered method
Run 2:  reused Rote Play
Memory: +37 sources
```

Then publish the evidence card as Markdown/JSON to a simple site or GitHub-backed collection. RocketRide performs that final action; Hydra remembers what you concluded and why; future runs can revisit a claim when new evidence arrives. RocketRide's orchestration model supports external tools and reusable pipelines, while Rote's Play model preserves the successful executable method rather than merely preserving a transcript. citeturn2search0turn3search6

Finally run:

```bash
snyk test
snyk code test
```

before judging, because the event guide explicitly says security vulnerabilities will cost points, and those are Snyk's dependency and source-code scanning commands. fileciteturn0file0 citeturn3search3turn3search4

**The pitch in one sentence:**  
**“We don't fact-check the internet by asking another LLM what it thinks; we reconstruct where a claim came from, show exactly how it mutated, remember the evidence graph forever, and reuse the successful investigation method on the next claim.”**