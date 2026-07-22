# Draft remediation arbitration brief

**Status:** DRAFT — Fable must approve, revise, or reject this brief before any remediation starts.

**Frozen baseline:** local commit `6db16afbb1b092837d786827da5936d64b7021d9`, incorporating upstream `9257e8580906862c1c52b158c9d971a50eb1455e`. The accepted evidence base is `qaqc/02_INDEPENDENT_QUALITY_GATE_AUDIT.md`, `qaqc/04_POST_PULL_MECHANICAL_REASSESSMENT.md`, `qaqc/05_APPROVED_SEMANTIC_AUDIT_WORK_ORDER.md`, and `qaqc/06_SEMANTIC_DUPLICATION_LOGIC_AUDIT.md`.

## 1. Role contract

- **Primary orchestrator:** owns scope, dispatch, checkpoints, and final acceptance. Does not perform the remediation edits.
- **Fable, second-in-command:** arbitrates order and ownership, approves bounded work orders, resolves scope collisions, and enforces stop conditions. Fable does not perform production-file remediation.
- **Sonnet 5, primary semantic executor:** implements approved documentation-semantic batches with exact file and issue boundaries.
- **GPT-5.3 Codex Spark, bounded mechanical executor:** implements one Fable-approved, mechanically testable batch at a time.
- **Independent quality engineer:** verifies scope, evidence, behavior, and regression results without relying on executor self-assessment.

## 2. Non-negotiable boundaries

1. No production file changes begin until Fable records an approved execution order and work-order boundaries.
2. Batch 8b is blocked until an owner records `OD-E2`; neither Fable nor an executor may invent that policy posture.
3. Artifact/source-edit Batches 2b and 6 require separate authorization and a separate checkpoint. They may not be smuggled into a documentation batch.
4. No other open decision (`OD-E1` through `OD-E8`) may be resolved by inference.
5. Documentation-semantic remediation must remain separate from the carried technical release blockers in `qaqc/02` and `qaqc/04`.
6. Executors may touch only the files explicitly assigned in their current approved work order. Generated outputs are out of scope unless explicitly named.
7. Each lane stops on scope drift, ambiguous source truth, unexpected generated changes, a failing required check, or a newly discovered P1 condition.
8. Work remains local on `repo-wide-qaqc`. Do not push. Commit subjects and bodies must contain no model, authorship, or provenance wording.

## 3. Proposed Wave A — documentation-semantic remediation

**Proposed executor:** Sonnet 5.

**Proposed scope:** accepted Batches 1, 2a, 3, 4, 5, 7, and 8a from `qaqc/06` §9. These are internally resolvable, hand-authored Markdown changes. Batch 8b is expressly excluded even where it shares a file with Batch 8a.

| Batch | Exact file scope | Required boundary |
|---|---|---|
| 1 | `schemas/MeterData/v0.6/ReferenceGuide.md` | Correct only the unqualified profile-count statement identified in the audit. |
| 2a | `what-ies-provides/schemas-overview/meter-data-request.md` | Correct the worked register codes and the false Daily-only register-scope statement. Do not edit the shipped JSON example. |
| 3 | `use-cases-overview/consumer-meter-digest.md`; `use-cases/consumer-meter-digest/README.md` | Reconcile every cited payload/contract dependency. Leave guide line 76, the Batch 8b owner-gated claim, untouched. |
| 4 | `pathways/researcher.md`; `pathways/utility.md` | Replace only the four stale or mislabeled references with links to real headings. |
| 5 | `what-ies-provides/schemas-overview/meter-data-credential.md` | Remove or correct the unsupported revocation-description claim. |
| 7 | `schemas/README.md`; `use-cases-overview/consumer-energy-passport.md`; `use-cases-overview/consumer-meter-digest.md`; `use-cases-overview/smart-meter-data-exchange.md` | Correct the false universal standards claim and make dependent prose point to the canonical order at `schemas/README.md:89-92`. |
| 8a | `how-you-implement-ies/conformance.md` | Correct only the deterministic credential-root command/input boundary. Do not apply the owner-gated conformance posture. |

### Wave A acceptance

- The diff is confined to the eleven files above and the exact audited concepts.
- All Batch 1, 2a, 3, 4, 5, 7, and 8a acceptance tests in `qaqc/06` §9 pass.
- No JSON, YAML, JSON-LD, generated file, shipped example, navigation file, or validator changes.
- No owner decision is silently made or pre-empted.
- `git diff --check` passes, disputed tokens/links are re-searched, and relevant repository checks pass.
- The independent quality engineer accepts both semantics and scope before a local checkpoint commit.

## 4. Proposed Wave B — one bounded mechanical repair

**Proposed executor:** GPT-5.3 Codex Spark, after Wave A is accepted and checkpointed.

Fable must select **one** initial mechanical target from the carried evidence, define its exact files, fixtures, acceptance command, regression boundary, and kill criteria. Candidate families include:

1. directory-target link detection and repair;
2. `SUMMARY.md` / `_sidebar.md` / index-generation parity and stable slug reuse; or
3. another single mechanical defect already demonstrated by `qaqc/02` and confirmed unchanged by `qaqc/04`.

The first Spark work order must not bundle link validation, navigation generation, schema generation, PDF, CI, and platform portability into a broad rewrite. It must have a deterministic failing fixture before the fix and an independent verification command afterward.

## 5. Separate authorization lanes

These are not authorized by approval of Wave A or Wave B:

- **Batch 2b:** `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json`.
- **Batch 6:** `schemas/MeterData/v0.6/attributes.yaml` plus the schema-change proposal flow.
- **Batch 8b:** owner-gated stub-aware validation and conformance wording after recorded `OD-E2`.
- Any remaining release blocker governed by the full `qaqc/02` regression sequence and kill criteria.

## 6. Required Fable arbitration

Fable must return a written decision that:

1. approves, rejects, or reorders the proposed waves;
2. decides whether the complex Consumer Meter Digest Batch 3 should be isolated from the other Wave A edits;
3. confirms whether Batch 8a may proceed without prejudging `OD-E2` and states the exact exclusion boundary;
4. selects the first bounded Spark target, or explicitly defers Spark until a later gate;
5. assigns checkpoint boundaries and quality-engineer gates;
6. records stop conditions and any additional files that must be read but not edited; and
7. produces executor-ready work orders with exact file lists, acceptance tests, and forbidden changes.

Approval of this draft alone does not authorize a release or publication. The final regression sequence and kill criteria in `qaqc/02` remain controlling for any release-readiness claim.
