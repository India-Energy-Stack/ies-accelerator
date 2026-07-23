# Owner Decision Ledger — CEP/Schema Recovery

This ledger records required `OD-E1` through `OD-E8` decisions in support of the
release-recovery execution sequence for branch `qaqc/cep-schedule-i-ii-v0-6`.
It is the single authoritative path for owner decisions.

## State model

Each decision is tracked in one state:

- `PROPOSED`
- `DECIDED`
- `IMPLEMENTED`
- `VERIFIED`
- `DEFERRED`
- `REJECTED`

Status transitions are owner-driven. Executors, Fable, and the orchestrator do not
choose outcomes.

For all entries below:

- **Decision owner** identifies who must decide.
- **Selected option** is the chosen option at the time of recording.
- **Decision date** is recorded as date + UTC offset.
- **Required work** links directly to one or more WA packages.

## OD-E1 — Public live/pilot status posture

- **Subject:** single, externally consistent public-status posture across:
  `README.md`, `faq.md`, `how-you-implement-ies/README.md`
- **Available options:**
  - `Live with explicit scope`: Keep “live in pilot” wording with explicit pilot-only limits.
  - `Not-live`: Remove/replace all “live” claims.
  - `Mixed timeline`: Explicitly split sandbox status from challenge outcome.
- **Selected option:** `Pending owner decision` (documentation consistency gate currently blocks closure).
- **Owner:** Repository owner / product lead.
- **Decision date:** 2026-07-23 (initial record).
- **Rationale:** P1-closure policy gate depends on this posture.
- **Affected files:** `README.md`, `faq.md`, `how-you-implement-ies/README.md`
- **Required implementation work:** WP-OD-E1 (policy-consistent wording updates).
- **Verification method:** Owner-submitted wording diff; QE checks for statement consistency across all three files.
- **Current state:** `PROPOSED`

## OD-E2 — External schema conformance wording

- **Subject:** Whether conformance statements remain authoritative while external `$ref` schemas remain stubbed.
- **Available options:**
  - `Strictly qualified`: State explicitly that full conformance depends on external-schema integration and network checks.
  - `Unqualified retained`: Keep current conformance wording unchanged (no change in status).
  - `Reclassified`: Remove/replace conformance claims from user-facing docs.
- **Selected option:** `Pending owner decision` (must be decided before WP-8b).
- **Owner:** Schema governance lead + documentation owner.
- **Decision date:** 2026-07-23 (initial record).
- **Rationale:** Closure of P1 conformance drift depends on explicit stance.
- **Affected files:** `how-you-implement-ies/conformance.md`, `how-you-implement-ies/issue-credentials.md` and any generated conformance references.
- **Required implementation work:** WP-8b.
- **Verification method:** Post-decision wording diff and conformance claim audit.
- **Current state:** `PROPOSED`

## OD-E3 — ElectricityCredential ownership model

- **Subject:** Maintain ElectricityCredential externally authoritative while enabling local schema generation, or move to local-generation-first ownership.
- **Available options:**
  - `External authority + local sync`: Keep external canonical source and implement deterministic sync path.
  - `Local generation authoritative`: Promote local generation as primary source with explicit refresh policy.
  - `Hybrid with explicit provenance`: Split authority by file type (canonical JSON-LD vs generated schema artifacts).
- **Selected option:** `Pending owner decision`.
- **Owner:** Schema tooling lead + credential architecture owner.
- **Decision date:** 2026-07-23 (initial record).
- **Rationale:** WP-P1.2 and related schema-generation flow are blocked until this is recorded.
- **Affected files:** `Makefile`, `.github/workflows/build-pdf.yml`, `scripts/generate_schema.py`, `scripts/generate_schema_permissive.py`, `schemas/ElectricityCredential/`.
- **Required implementation work:** WP-P1.2.
- **Verification method:** Package-scoped QE and reproducible generation proof.
- **Current state:** `PROPOSED`

## OD-E4 — `index.md` role in publication

- **Subject:** Canonical delivery of `index.md` versus curated navigation intent.
- **Available options:**
  - `Canonical`: `index.md` is a source-of-truth index.
  - `Curated aid`: `index.md` is curated navigation aid, not canonical.
  - `Retire`: remove/de-emphasize `index.md` and shift to alternate navigation.
- **Selected option:** `Pending owner decision`.
- **Owner:** Documentation and publication owner.
- **Decision date:** 2026-07-23 (initial record).
- **Rationale:** Downstream publication and WP-OD-E4-ISS-013 closures require role clarity.
- **Affected files:** `index.md`, `SUMMARY.md`, `_sidebar.md`, `README.md` references, and related publication scripts.
- **Required implementation work:** WP-OD-E4-ISS-013 (slugger update now, role-dependent follow-up later).
- **Verification method:** Deterministic navigation checks and package-specific QE after decision is applied.
- **Current state:** `PROPOSED`

## OD-E5 — ArrFiling versioning convention

- **Subject:** Meaning of ArrFiling `v0.5/attributes.yaml` version `1.0.0` and migration intent.
- **Available options:**
  - `Convention A`: `info.version` tracks schema document revision (internal schema evolution).
  - `Convention B`: `info.version` tracks family public compatibility version.
  - `Convention C`: split schema into two families or deprecate with migration note.
- **Selected option:** `Pending owner decision`.
- **Owner:** MeterData/ArrFiling schema owner.
- **Decision date:** 2026-07-23 (initial record).
- **Rationale:** WP-OD-E5 is required for P1-closure and may drive Subwave 2 implementation.
- **Affected files:** `schemas/ArrFiling/v0.5/attributes.yaml`, `schemas/ArrFiling/v0.5/README.md`, related migration notes.
- **Required implementation work:** WP-OD-E5 (both subwaves).
- **Verification method:** Explicit versioning policy statement and schema metadata checks.
- **Current state:** `PROPOSED`

## OD-E6 — Pathways navigation intent

- **Subject:** Whether `pathways/` is intentionally hidden or intentionally listed in navigation.
- **Available options:**
  - `Intentionally hidden`: publish pointer from existing docs and mark intended rollout path.
  - `Publish`: add pathways to navigation surfaces.
  - `Retain excluded`: leave unlisted and remove all internal cross-link claims.
- **Selected option:** `Pending owner decision`.
- **Owner:** Documentation and IA owner.
- **Decision date:** 2026-07-23 (initial record).
- **Rationale:** WP-OD-E6 and related publication package scope is conditional on navigation stance.
- **Affected files:** `pathways/**`, `SUMMARY.md`, `_sidebar.md`, `index.md`.
- **Required implementation work:** WP-OD-E6.
- **Verification method:** Navigation presence tests and deterministic navigation output comparison.
- **Current state:** `PROPOSED`

## OD-E7 — Windows support posture

- **Subject:** Whether Windows support remains a required target or Windows is WSL/Ubuntu-first.
- **Available options:**
  - `Full Windows support`: document and fix all required blockers.
  - `WSL/Unix-first`: document Windows limitations and scope.
  - `Phased deprecation`: maintain limited support with explicit timeline.
- **Selected option:** `Pending owner decision`.
- **Owner:** QA and platform owner.
- **Decision date:** 2026-07-23 (initial record).
- **Rationale:** WP-P2.2 and WP-P1.3-P2.8 share this decision and cannot start without it.
- **Affected files:** `scripts/build_pdf.py`, `scripts/build_pdf.sh`, `scripts/validate_schema.py`, `README.md`.
- **Required implementation work:** WP-P2.2, WP-P1.3-P2.8.
- **Verification method:** Platform-specific checks and negative/positive fixture gates from package owner.
- **Current state:** `PROPOSED`

## OD-E8 — Billing profile duplicate disposition

- **Subject:** Disposition of byte-identical `CustomerBillingSummary.json` and `BillingProfile.json`.
- **Available options:**
  - `Remove duplicate`: remove the unreferenced duplicate.
  - `Repurpose duplicate`: add explicit purpose and references.
  - `Keep with intent`: document explicit intentional duplication in schema/readme.
- **Selected option:** `Pending owner decision`.
- **Owner:** MeterData schema owner + examples owner.
- **Decision date:** 2026-07-23 (initial record).
- **Rationale:** Duplicate handling affects both packaging and migration documentation and gates WP-OD-E8.
- **Affected files:** `schemas/MeterData/v0.5/examples/BillingProfile.json`, `schemas/MeterData/v0.5/examples/CustomerBillingSummary.json`, `schemas/MeterData/v0.5/README.md`, related example indices.
- **Required implementation work:** WP-OD-E8 (all branches).
- **Verification method:** Example coverage + packaging validation + repository cleanup audit.
- **Current state:** `PROPOSED`

## Change log

- 2026-07-23: ledger introduced with all eight decisions recorded in `PROPOSED` state and owner-routing metadata.
