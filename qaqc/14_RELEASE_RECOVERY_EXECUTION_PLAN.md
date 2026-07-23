# IES Accelerator v0.6 Release-Recovery Execution Plan

## Scope

Applied on branch `qaqc/cep-schedule-i-ii-v0-6` to align the repository with the
recovery objectives in the attached plan: coherence, reproducibility, explicit
migration accounting, decision traceability, and reproducible publication evidence.

Current branch is:

- `qaqc/cep-schedule-i-ii-v0-6`
- `HEAD 32f613fe4703a7cb7b86f689a9cc9971ae883131`
- Working tree: clean

## Plan status (current)

| Phase | Status | Gate condition | Evidence/checkpoint |
|---|---|---|---|
| Phase 0 — Baseline | **In-progress** | Branch/HEAD/working tree recorded and tied to review | `qaqc/14_RELEASE_RECOVERY_EXECUTION_PLAN.md`, `qaqc/11_OWNER_DECISION_LEDGER.md` |
| Phase 1 — Owner decisions | **Started** | `qaqc/11_OWNER_DECISION_LEDGER.md` exists and all OD-E entries recorded | `qaqc/11_OWNER_DECISION_LEDGER.md` |
| Phase 2 — Migration policy redesign | **Not started** | OD-E and schema tooling owners define new equivalence contract | Not yet edited |
| Phase 3 — MDR v0.6 example consistency | **Not started** | `OD-E3`/schema owner closure | Existing shipped-shape mismatch remains |
| Phase 4 — CEP Schedule I model | **Not started** | CEP model decision + mapping validation | File currently mixed-model and needs normative mapping |
| Phase 5 — CEP identifier policy | **Not started** | Identifier matrix and policy published | `did:web` / `did:dedi` conflict remains unresolved |
| Phase 6 — CEP Schedule II mapping | **Not started** | Schedule II executable schema mapping declared | Mapping path not yet finalized |
| Phase 7 — Deterministic generation | **Not started** | Manifest + CI generation policy implemented | `scripts/verify_v05_v06_equivalence.py` and generation policy need redesign |
| Phase 8 — JSON-LD restoration | **Not started** | Dependency + CI wiring completed and checked | `scripts/check_jsonld.py` still dependency-sensitive |
| Phase 9 — QA docs repair | **In-progress** | All stale QA entries reconciled with current state and linked proof | `qaqc/13_STAGE_GATE_AND_PENDING_WORK_NOTES.md`, `qaqc/12_CURRENT_STATE_RECONCILIATION.md`, new ledger |
| Phase 10 — Publication artifacts | **Not started** | Clean checkout builds + PDF/public mirror checks pass | No publication artifact proof attached to current branch HEAD yet |
| Phase 11 — Independent final review | **Not started** | Blocked by unresolved P1 and unimplemented remediation phases | Planned after all prior phases close |

## Phase 0 evidence (recorded in this action)

- `git rev-parse --abbrev-ref HEAD` → `qaqc/cep-schedule-i-ii-v0-6`
- `git rev-parse HEAD` → `32f613fe4703a7cb7b86f689a9cc9971ae883131`
- `git status --short` → clean
- `git log --oneline -n 8` confirms this branch head and history lineage

## Required owner-decision ledger completion

All eight owner decision rows are now formally present in:

- `qaqc/11_OWNER_DECISION_LEDGER.md`

Each row includes state, owner, rationale, affected files, required work, and
verification path. At present, all entries are in `PROPOSED` state and are waiting
for owner decisions.

## Clarification against current plan intent

- Backward compatibility between v0.5 and v0.6 is not a release blocker by itself;
  it remains only where compatibility expectations are explicitly claimed in docs.
- The branch review remains constrained by the `qaqc` execution controls and the
  final `qaqc/02` regression gate. This document does not declare release-green
  status.

## Next recommended action order

1. Route each `OD-E` owner decision to completion in `qaqc/11_OWNER_DECISION_LEDGER.md`.
2. Re-design migration QA in `scripts/verify_v05_v06_equivalence.py` and add
   `schemas/MeterData/v0.6/MIGRATION_FROM_V0.5.md`.
3. Execute CEP Schedule I and II alignment (Model decision + mapping + examples + validation).
4. Implement deterministic generation manifest and CI checks.
5. Restore JSON-LD execution path and wire into QA/CI.
6. Complete publication artifact generation and verification.
7. Run a single independent final regression and report `PASS/FAIL/BLOCKED` with exact command evidence.
