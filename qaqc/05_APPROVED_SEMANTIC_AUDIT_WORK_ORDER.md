# Approved Semantic Audit Work Order

**Status:** Approved for dispatch. Supersedes `qaqc/03_DRAFT_SEMANTIC_AUDIT_WORK_ORDER.md`, whose 81-file counts predate the merge of PRs #150/#151; the binding corpus is Section 2. Executor: Sonnet 5, sole primary executor for semantic, duplication, and logical-consistency analysis. The audit phase is report-only: no repository source, script, schema, navigation, or prior-audit file may be edited, and no commit, push, or publication action is authorized. The only permitted worktree delta is creation and revision of the single deliverable named in Section 9.

## 1. Objective

Determine whether every audience-facing claim in the 79-file Markdown corpus is internally coherent, correctly scoped, and supported by the repository's schema, example, validation, build, and CI evidence, and produce one prioritized, evidence-anchored audit with owner decisions and release gates.

## 2. Locked baseline and inputs

### 2.1 Baseline

- Branch `repo-wide-qaqc` at commit `c5b5b9b6740ceecce94209f8d56946f5791c5069`; `git status --short` clean at dispatch.
- Audience corpus: every tracked `*.md` file excluding `qaqc/*.md` — exactly **79 files**. Reconcile at start; any mismatch triggers Section 11.

| Group | Count |
|---|---:|
| Root: `README.md`, `SUMMARY.md`, `_sidebar.md`, `index.md`, `faq.md`, `glossary.md`, `contributors.md`, `download-pdf.md` | 8 |
| `what-ies-provides/**` | 13 |
| `how-you-implement-ies/**` | 7 |
| `pathways/**` | 6 |
| `use-cases-overview/**` | 8 |
| `use-cases/**` | 9 |
| `schemas/**/*.md` | 28 |
| **Total** | **79** |

### 2.2 Evidence corpus — mandatory wherever technical truth is asserted

- Schema sources and compiled artifacts: 11 each of `attributes.yaml`, `schema.json`, `context.jsonld`, `vocab.jsonld`.
- Shipped examples: all 62 tracked `schemas/**/examples/*.json`.
- Validation: all 19 tracked files under `schemas/**/validation/**` (includes 2 validation Makefiles; the 2 validation READMEs are also corpus files) plus the 3 version-level Makefiles (`MeterData/v0.6`, `MeterDataRequest/v0.6`, `OutageNotification/v0.1`).
- Registries and crosswalks: `schemas/MeterData/v0.5/OBISMapping.json`, `schemas/MeterData/v0.6/IES codes.json`, `schemas/OutageNotification/v0.1/fault_reason_crosswalk.json`, `FeederStatusIngest.openapi.yaml`, `tools/transform_discom_csv.py`, `tools/discom_planned_shutdown.csv`.
- Build/CI controls: root `Makefile`, `.gitbook.yaml`, `.github/workflows/build-pdf.yml`, all 22 `scripts/*.py`, `scripts/build_pdf.sh`, both `scratch/*.py`.

### 2.3 Control inputs (not corpus)

`qaqc/01`, `qaqc/02`, and `qaqc/04` are binding mechanical evidence per Section 7. `qaqc/03` is superseded by this order.

## 3. Coverage rules

- **Complete coverage, not sampling.** All 79 corpus files are read in full and individually dispositioned. Sampling may order the reading; it can never support a broad claim ("all", "every", "consistent", "complete", "canonical", "no other").
- Any claim touching technical truth — fields, versions, required/optional status, validator behavior, example conformance, build/CI behavior, link/anchor generation — is adjudicated against the Section 2.2 artifacts, never against prose alone.
- A broad conclusion about a class of evidence artifacts requires inspecting the full class.

## 4. Audit axes — keep separate until synthesis

Every finding is assigned a primary axis; a finding may connect axes only after each axis has standalone evidence.

1. **Product/status** — what IES is, provides, has delivered; normative vs illustrative; current vs aspirational.
2. **Research/evidence** — whether asserted outcomes, pilots, and comparisons are supported by cited or in-repo evidence.
3. **Architecture** — Register/Discover/Exchange structure, adapter placement, trust topology, actor roles.
4. **Data/schema semantics** — source-to-compiled alignment, versions, field meaning, registries, examples, migration claims.
5. **Execution/tooling** — what validators, Make targets, scripts, and CI actually establish vs what prose claims they establish.
6. **Team/governance** — ownership, authority, secretariat/contributor roles, decision rights over specs and schemas.

## 5. Source-of-truth map (required)

For each topic: the canonical source (`file:heading`), every dependent restatement, verbatim divergences, and a verdict — `ALIGNED`, `DRIFT`, `CONTRADICTION`, or `NO CANONICAL SOURCE`. The map must also state whether each canonical source is reachable through published navigation (`pathways/**` sits outside `SUMMARY.md` and `_sidebar.md`).

1. Register / Discover / Exchange — prerequisites, actors, artifacts, sequence, claimed outcomes.
2. B2B vs B2C boundaries — credential issuance vs data exchange; catalogue, consent, and payload responsibilities.
3. Identity and data movement — DID/DeDi roles, Beckn registration and signing, DigiLocker delivery, adapter placement, consent/authorization; signer, holder, issuer, verifier, sender, receiver, and custody transitions.
4. Schema, version, and field semantics — including external-schema dependencies.
5. Use-case/pathway parity — all 7 overview↔implementation-guide pairs and all 5 role pathways (authority, researcher, secretariat, tsp, utility) against canonical product and implementation pages.
6. Security, privacy, and conformance — what validation actually proves vs what pages claim.
7. Live / pilot / WIP / timeline / actor assertions — demonstrated vs planned vs production-ready.

## 6. Duplication taxonomy

One stable `DUP-###` cluster per repeated concept, recording every location, candidate canonical source, variance, harm, and owner. Types and default treatment:

| Type | Treatment |
|---|---|
| Intentional overview-detail layering | Accept when the overview stays shallow, links to detail, and restates no mutable normative rule; flag drift or unclear authority. |
| Generated / versioned / template reuse | Accept when source, version, generation boundary, and owner are explicit. |
| Redundant normative prose | Harmful when the same rule can change independently in multiple places; name canonical candidate and dependents. |
| Contradictory duplicates | Defect; quote both propositions with paired `file:line` anchors; do not reconcile by preference. |
| Copy-paste residue | Defect or risk when names, versions, actors, paths, or status labels survive from another context. |

The 7 exact-paragraph duplicate groups reported in `qaqc/04` are an input list, not a verdict. **Counts never substitute for per-cluster semantic judgment.**

## 7. Mechanical inputs, partials to reassess, and retractions

### 7.1 Settled mechanical facts — inputs, not reruns

Treat the `qaqc/04` evidence matrix as fact: three live directory-link 404s plus one latent; `validate_links.py` false-green; MDR semantic-validator failure alongside generic pass; 12-artifact reproducibility drift across 5 directories; PDF missing-source false-green and CP-1252 failure; Windows resolver failure; CI limited to `build-pdf.yml`; metadata parity conflicts; migration-tool false-green/stale behavior; JSON-LD unwired; permissive external stubs; ElectricityCredential Make exclusion; byte-identical example pair. Do not rerun the builds and scans that established these. **Do** inspect the underlying sources for semantic interpretation, recording for each: `SEMANTIC IMPACT CONFIRMED`, `NO SEMANTIC IMPACT`, or `OWNER DECISION REQUIRED`.

### 7.2 Post-pull outcome — honored, not relitigated

- **RESOLVED:** explicit pilot calendar dates (zero corpus hits). Closed; do not reopen without new evidence.
- **PARTIALLY RESOLVED:** navigation cleanup and `SUMMARY`/`index` parity (Summary 57 / index 46 / shared 43 / Summary-only 14 / index-only 3; P2P overview omitted at `scripts/generate_index.py:111-119`).
- **REGRESSED:** numeric anchors (740 outline links; 262 slug mismatches; 224 numeric-label mismatches). Reassess **only** for semantic navigation intent — whether a reader following the index lands on the intended section; the mechanical counts stand.
- **UNCHANGED:** all technical release blockers (schema reproducibility, MDR contradiction, PDF, resolver, CI breadth, metadata, migration tooling, JSON-LD, stubs, ownership, duplicate examples).

### 7.3 Current partials requiring semantic reassessment — each becomes a dispositioned finding or `NO FINDING`

1. `pathways/researcher.md:33` — references a companion "What IES Is Not" **page**; determine whether such a page exists or only the `README.md` section does (stale post-deletion reference).
2. `pathways/researcher.md:51` — references "concepts pages"; no `concepts/` files are tracked; determine the referent or classify as stale.
3. Status-claim divergence: `README.md:105` (past-tense sandbox and completed challenge), `faq.md:45` ("It is live … building in it now", present tense), `how-you-implement-ies/README.md:120` (completed 30-day outcome). Determine one defensible status posture; externally unverifiable claims are `UNSUPPORTED`, not fact.
4. `SUMMARY`/`index` omissions, including `pathways/**` absent from both `SUMMARY.md` and `_sidebar.md` — intentional staging or navigation defect; `OWNER DECISION REQUIRED` if undeterminable.
5. Numeric-anchor regression — semantic navigation intent only, per 7.2.
6. Exact duplicate examples `schemas/MeterData/v0.5/examples/BillingProfile.json` / `CustomerBillingSummary.json` (byte-identical, 89 lines) — duplication-register entry with recommended disposition.
7. Metadata truth conflicts: `schemas/MeterData/v0.6/attributes.yaml:4-6` (0.5.0 / six shapes) vs its README (v0.6 / eight) — internally adjudicable; `schemas/ArrFiling/v0.5/attributes.yaml:4` (1.0.0) vs its README (v0.5) — versioning convention is an owner decision.
8. ElectricityCredential authority/ownership: Beckn-authoritative statements (`schemas/ElectricityCredential/README.md:5`, `v1.2/README.md:3`) vs `Makefile:20-22` exclusion vs locally tracked v1.0/v1.1/v1.2 artifacts with no sync verifier — what may the docs truthfully claim?
9. External-stub conformance wording: any prose implying validated conformance to EnergyCredential, EnergyResource, Address, or GeoJSONGeometry, against the permissive stubs at `scripts/validate_schema.py:7-43`. False conformance claims are P1 candidates.
10. MDR truth adjudication: `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json:15-18` vs `schemas/MeterData/v0.6/IES codes.json:338-348,353-362` vs the dedicated validator vs surrounding prose — determine which artifact is wrong as a semantic question; recommend, do not fix.

### 7.4 Preserved retractions — must not re-enter without new reproducible evidence

- The 64-item naive `id-*` anchor-failure set.
- The 1,533 duplicate-key scanner warnings (scanner artifacts, not duplicate keys).
- Contaminated aggregate link totals from the initial mechanical audit.

## 8. Severity, confidence, and classification

- **P1** — release-blocking contradiction, false conformance claim, destructive ambiguity (plausible readings drive materially wrong or harmful implementation), or broken primary journey (a published navigation path or core reader journey dead-ends or misleads).
- **P2** — material but bounded: workaround exists, single surface, or non-primary journey.
- **P3** — cleanup: clarity, residue, hygiene without decision impact.
- Every finding separates three layers: **FACT** (quoted proposition with `file:line`), **INTERPRETATION** (reasoning plus confidence High/Medium/Low with stated basis), and **OWNER DECISION** (what only an owner can settle). Interpretation is never presented as fact.
- Contradiction and parity findings require paired anchors and both quoted propositions. External claims unverifiable from the repository are `UNSUPPORTED CLAIM`, not contradictions.
- Deduplicate by root cause; IDs are stable and never renumbered; withdrawn items remain marked `RETRACTED`.

## 9. Deliverable

Exactly one file: **`qaqc/06_SEMANTIC_DUPLICATION_LOGIC_AUDIT.md`**, structured in this order:

1. **Take** — one-paragraph verdict, release posture first.
2. **Coverage ledger** — one row per corpus file (all 79): `READ`, axes applied, finding IDs or `NO FINDING`; plus an evidence-file ledger for Section 2.2.
3. **Source-of-truth map** — Section 5 topics with verdicts.
4. **Duplication register** — every `DUP-###` cluster, all instances, type, treatment.
5. **Logical inconsistency register**.
6. **Cross-audience journey findings** — reader journeys across README → What IES Provides → How you implement → use cases → schemas, and pathway parity.
7. **Issue table** — ID | `file:line` | evidence | severity | confidence | recommendation | owner decision.
8. **Release gates**.
9. **Bounded remediation batches** — each with scope, target files, acceptance test, and owner precondition; no patches or diffs.
10. **Unresolved questions**.

The audit is report-only: recommendations name target and intent but contain no source edits. The deliverable contains no AI, model, authorship, or provenance wording.

## 10. Completion criteria

The audit is complete only when all of the following hold: every one of the 79 corpus files is marked `READ` and dispositioned; every Section 4 axis is closed with standalone evidence; every Section 7.3 item and every carried 7.1 fact has a recorded disposition; every Section 5 topic has a verdict; and no broad claim stands without full-class evidence.

## 11. Stop conditions — halt and escalate; do not improvise

- Material baseline drift: HEAD, tracked manifest, or any file content differs from Section 2.1 beyond creation/revision of the Section 9 deliverable.
- A required corpus or evidence file is missing or unreadable.
- An external live/pilot/timeline/actor/security claim is unverifiable **and** the gap blocks a P1 adjudication or the overall verdict (otherwise classify `UNSUPPORTED` and continue).
- Ambiguity that could be resolved only by inventing product truth — two plausible readings that produce different P1 outcomes.
- Completion would require a source edit, scope expansion, or any commit/push/publication action.

## 12. Owner-decision list — closed; additions require escalation

**Sonnet resolves operationally** (repository evidence suffices):

- **OD-S1** — MeterData v0.6 metadata staleness: which side is correct is internally determinable; recommend the correction target.
- **OD-S2** — numeric-anchor semantic-harm judgment (Section 7.3.5).
- **OD-S3** — duplication-cluster classification and canonical-candidate selection where the corpus itself declares authority.
- **OD-S4** — stale-reference determinations (`researcher.md:33`, `:51`) where a target's existence is directly checkable.

**Escalate to owner** (priority order):

- **OD-E1** (blocks P1 closure) — the single truthful public status posture for live/pilot/sandbox claims across `README.md:105`, `faq.md:45`, `how-you-implement-ies/README.md:120`.
- **OD-E2** (blocks P1 closure) — conformance wording permitted while external-schema validation is stub-only.
- **OD-E3** — ElectricityCredential ownership: declared externally maintained (with a sync verifier) vs brought under local generation.
- **OD-E4** — `index.md` role: canonical deliverable, curated aid, or retired — sets the severity of parity and anchor findings.
- **OD-E5** — versioning convention governing the ArrFiling 1.0.0-vs-v0.5 class of mismatch.
- **OD-E6** — `pathways/**` publication intent: added to navigation or deliberately unlisted.
- **OD-E7** — Windows support posture, setting resolver/encoding severity.
- **OD-E8** — disposition of the duplicate MeterData v0.5 example pair and of stale `scratch/` tooling.

## 13. Gates

### 13.1 Before the audit is accepted

- Coverage ledger reconciles to 79 corpus files and complete Section 2.2 evidence classes.
- Every Section 7.3 item and every carried 7.1 fact is dispositioned; no retracted item reintroduced; no resolved fact reopened without new evidence.
- Every P1 carries paired anchors, quoted propositions, and explicit fact/interpretation/owner-decision separation.
- `git status --short` shows only `qaqc/06_SEMANTIC_DUPLICATION_LOGIC_AUDIT.md` as the delta; all other files byte-identical to baseline.
- The owner-decision list matches Section 12 — no silent additions or removals.

### 13.2 Before remediation starts

- The audit has passed 13.1 and been accepted.
- Every remediation batch has a bounded file list and an acceptance test; batches that depend on an OD-E item carry the recorded owner decision before dispatch.
- No batch mixes documentation-semantic corrections with the unchanged technical release blockers (schema reproducibility, validators, PDF, CI), which remain governed by the regression sequence and kill criteria in `qaqc/02`.
- The report-only boundary holds until remediation is separately authorized.
