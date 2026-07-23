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
- **Selected option:** `Evidence-bounded historical wording with separately maintained current-status reporting`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23 (initial record).
- **Decision text:** Public documentation shall state that four pilot DISCOMs completed a 30-day IES challenge using the IES sandbox. Undated documentation shall not claim that pilots are currently live, DISCOMs are currently building in the sandbox, sandbox remains operational, or production is active unless the current status is supported by dated owner-maintained evidence.
- **Affected files:** `README.md`, `faq.md`, `how-you-implement-ies/README.md`
- **Required implementation work:** WP-OD-E1 (policy-consistent wording updates).
- **Verification method:** Owner-submitted wording diff; QE checks for statement consistency across all three files.
- **Current state:** `DECIDED`

## OD-E2 — External schema conformance wording

- **Subject:** Whether conformance statements remain authoritative while external `$ref` schemas remain stubbed.
- **Available options:**
  - `Strictly qualified`: State explicitly that full conformance depends on external-schema integration and network checks.
  - `Unqualified retained`: Keep current conformance wording unchanged (no change in status).
  - `Reclassified`: Remove/replace conformance claims from user-facing docs.
- **Selected option:** `Split validation into two explicit gates: local structural validation and full external-schema conformance`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23 (initial record).
- **Decision text:** Local structural validation (schema + semantic checks) is distinct from full external-schema conformance; permissive stubs establish only local structural validation and shall not be represented as production conformance/readiness.
- **Affected files:** `how-you-implement-ies/conformance.md`, `how-you-implement-ies/build-adapter.md`, `use-cases/consumer-meter-digest/README.md`.
- **Required implementation work:** WP-8b.
- **Verification method:** Post-decision wording diff and conformance claim audit.
- **Current state:** `DECIDED`

## OD-E3 — ElectricityCredential ownership model

- **Subject:** Maintain ElectricityCredential externally authoritative while enabling local schema generation, or move to local-generation-first ownership.
- **Available options:**
  - `External authority + local sync`: Keep external canonical source and implement deterministic sync path.
  - `Local generation authoritative`: Promote local generation as primary source with explicit refresh policy.
  - `Hybrid with explicit provenance`: Split authority by file type (canonical JSON-LD vs generated schema artifacts).
- **Selected option:** `External upstream maintenance with repository-enforced sync and drift verifier`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23 (initial record).
- **Decision text:** ElectricityCredential remains externally maintained; repository must implement a verifier that pins upstream source, compares local mirror against it, passes only when synchronized, fails on drift fixture, and runs in CI.
- **Affected files:** `Makefile`, `.github/workflows/build-pdf.yml`, `scripts/generate_schema.py`, `scripts/generate_schema_permissive.py`, `schemas/ElectricityCredential/`.
- **Required implementation work:** WP-P1.2.
- **Verification method:** Package-scoped QE and reproducible generation proof.
- **Current state:** `DECIDED`

## OD-E4 — `index.md` role in publication

- **Subject:** Canonical delivery of `index.md` versus curated navigation intent.
- **Available options:**
  - `Canonical`: `index.md` is a source-of-truth index.
  - `Curated aid`: `index.md` is curated navigation aid, not canonical.
  - `Retire`: remove/de-emphasize `index.md` and shift to alternate navigation.
- **Selected option:** `Retire the generated exhaustive index as a release-navigation contract`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23 (initial record).
- **Decision text:** `SUMMARY.md` and `_sidebar.md` are authoritative; existing generated `index.md` is not a canonical inventory nor release-gating contract and may be removed or replaced by a non-normative landing page.
- **Affected files:** `index.md`, `SUMMARY.md`, `_sidebar.md`, `README.md` references, `scripts/generate_index.py`, `scripts/validate_links.py` (anchor checks where applicable).
- **Required implementation work:** WP-OD-E4-ISS-013 (slugger update now, role-dependent follow-up later).
- **Verification method:** Deterministic navigation checks and package-specific QE after decision is applied.
- **Current state:** `DECIDED`

## OD-E5 — ArrFiling versioning convention

- **Subject:** Meaning of ArrFiling `v0.5/attributes.yaml` version `1.0.0` and migration intent.
- **Available options:**
  - `Convention A`: `info.version` tracks schema document revision (internal schema evolution).
  - `Convention B`: `info.version` tracks family public compatibility version.
  - `Convention C`: split schema into two families or deprecate with migration note.
- **Selected option:** `info.version` tracks the schema family’s public version`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23 (initial record).
- **Decision text:** Directory families map to public versions (`v0.5` → `0.5.0`, `v1.2` → `1.2.0`); internal document revision must use separate metadata (`x-document-revision` or release/changelog).
- **Affected files:** `schemas/ArrFiling/v0.5/attributes.yaml`, `schemas/ArrFiling/v0.5/README.md`, related migration notes.
- **Required implementation work:** WP-OD-E5 (both subwaves).
- **Verification method:** Explicit versioning policy statement and schema metadata checks.
- **Current state:** `DECIDED`

## OD-E6 — Pathways navigation intent

- **Subject:** Whether `pathways/` is intentionally hidden or intentionally listed in navigation.
- **Available options:**
  - `Intentionally hidden`: publish pointer from existing docs and mark intended rollout path.
  - `Publish`: add pathways to navigation surfaces.
  - `Retain excluded`: leave unlisted and remove all internal cross-link claims.
- **Selected option:** `Publish Pathways as a normal documentation section`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23 (initial record).
- **Decision text:** Pathways is public onboarding content and must be added to canonical navigation in `SUMMARY.md` and `_sidebar.md` under a Pathways/Adoption section.
- **Affected files:** `pathways/**`, `SUMMARY.md`, `_sidebar.md`.
- **Required implementation work:** WP-OD-E6.
- **Verification method:** Navigation presence tests and deterministic navigation output comparison.
- **Current state:** `DECIDED`

## OD-E7 — Windows support posture

- **Subject:** Whether Windows support remains a required target or Windows is WSL/Ubuntu-first.
- **Available options:**
  - `Full Windows support`: document and fix all required blockers.
  - `WSL/Unix-first`: document Windows limitations and scope.
  - `Phased deprecation`: maintain limited support with explicit timeline.
- **Selected option:** `Support native Windows operation for core repository tooling`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23 (initial record).
- **Decision text:** Core Python-based authoring/validation/QA must run natively on Windows; Linux CI remains reference for PDF release while Windows blockers in core paths are treated as defects.
- **Affected files:** `scripts/build_pdf.py`, `scripts/build_pdf.sh`, `scripts/validate_schema.py`, `README.md`.
- **Required implementation work:** WP-P2.2, WP-P1.3-P2.8.
- **Verification method:** Platform-specific checks and negative/positive fixture gates from package owner.
- **Current state:** `DECIDED`

## OD-E8 — Billing profile duplicate disposition

- **Subject:** Disposition of byte-identical `CustomerBillingSummary.json` and `BillingProfile.json`.
- **Available options:**
  - `Remove duplicate`: remove the unreferenced duplicate.
  - `Repurpose duplicate`: add explicit purpose and references.
  - `Keep with intent`: document explicit intentional duplication in schema/readme.
- **Selected option:** `Remove duplicate CustomerBillingSummary example from v0.5`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23 (initial record).
- **Decision text:** Retain `BillingProfile.json` and remove byte-identical `CustomerBillingSummary.json`; update example index accordingly; no repurpose under deprecated v0.5.
- **Affected files:** `schemas/MeterData/v0.5/examples/BillingProfile.json`, `schemas/MeterData/v0.5/examples/CustomerBillingSummary.json`, `schemas/MeterData/v0.5/README.md`, related example indices.
- **Required implementation work:** WP-OD-E8 (all branches).
- **Verification method:** Example coverage + packaging validation + repository cleanup audit.
- **Current state:** `DECIDED`

## AUTH-WP-2B — MeterDataRequest shipped-example correction

- **Subject:** authorization for bounded example correction in `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json`.
- **Selected option:** `GO`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23.
- **Decision:** retain `profileType: IntervalProfile` and change readings to `kWh imp block` and `kWh exp block`; no unrelated schema changes authorized.
- **Required implementation work:** `WP-2B`.
- **Verification method:** generic and semantic validation succeed for the example.
- **Current state:** `DECIDED`

## AUTH-WP-6 — MeterData v0.6 metadata correction

- **Subject:** authorization for metadata correction in `schemas/MeterData/v0.6/attributes.yaml`.
- **Selected option:** `GO, AFTER WP-P1.2`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23.
- **Decision text:** authorize schema-change proposal to correct version and profile-description metadata; execution must wait until generator unification and acceptance.
- **Required implementation work:** `WP-6` (or exact child sub-package after `WP-P1.2` acceptance).
- **Current state:** `DECIDED`

## DIR-MIGRATION-V06 — Cross-version migration policy

- **Subject:** replace strict equivalence test with intentional breaking-change, migration coverage, and current-version validity checks.
- **Selected option:** `GO`.
- **Owner:** Rishabh Jain / Repository Owner.
- **Decision date:** 2026-07-23.
- **Decision text:** compatibility differences in names/counts/shape/metadata are not P1 failures when intentional; only unexplained migration loss fails. Required test matrix: intentional disposition, coverage, preservation, and v0.6 validity.
- **Required implementation work:** `WP-2` redesign of `scripts/verify_v05_v06_equivalence.py` + `schemas/MeterData/v0.6/MIGRATION_FROM_V0.5.md`.
- **Verification method:** migration QA passing across disposition/coverage/preservation/current-validity checks.
- **Current state:** `DECIDED`

## Change log

- 2026-07-23: ledger introduced with all eight decisions recorded in `PROPOSED` state and owner-routing metadata.
- 2026-07-23: updated with repository owner decisions for `OD-E1`…`OD-E8` and added separate authorization records for `AUTH-WP-2B`, `AUTH-WP-6`, and `DIR-MIGRATION-V06`.
