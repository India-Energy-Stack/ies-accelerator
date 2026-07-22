# Semantic, Duplication & Logical-Consistency Audit

**Scope:** all 79 tracked audience Markdown files (excluding `qaqc/`) at branch `repo-wide-qaqc`, content baseline `c5b5b9b6740ceecce94209f8d56946f5791c5069`, this correction dispatched at HEAD `7414ba8c2c43cc66d90f96d5f3111ac17b06e6b7`. Executed per `qaqc/05_APPROVED_SEMANTIC_AUDIT_WORK_ORDER.md`, using `qaqc/01_SPARK_MECHANICAL_AUDIT.md`, `qaqc/02_INDEPENDENT_QUALITY_GATE_AUDIT.md` and `qaqc/04_POST_PULL_MECHANICAL_REASSESSMENT.md` as binding inputs (`qaqc/01` is a binding input per Section 2.3 of the work order; where `qaqc/02`/`qaqc/04` retracted or corrected an `qaqc/01` claim, that retraction/superseding is noted explicitly at point of use, not silently). This report is read-only: no source, script, schema, navigation, or prior-audit file was edited.

---

## 1. Take

**Release posture: not release-ready.** Exactly three P1s remain: one genuinely new root cause (ISS-019), plus two carried-weakness semantic amplifications (ISS-001 and ISS-018).

- **ISS-019** (Consumer Meter Digest) is **genuinely new**: two paired pages (`use-cases-overview/consumer-meter-digest.md` and `use-cases/consumer-meter-digest/README.md`) describe payload fields and values (`meterReference`, `period`, `summary` with values `SUMMARY_TOTAL`/`SUMMARY_PEAK`/`SUMMARY_TOD`, `dataQuality`, and `RAW_15M`) that the current schema does not define; the implementation guide additionally gives a non-canonical OpenCred `schemaId`, a singular policy key where the repository documents `requiredCredentials`, and two capability keys not defined anywhere else in the repository.
- **ISS-001** (MeterDataRequest overview prose and artifact-side schema-framing) is a **semantic amplification of the already-carried MDR contradiction** (`qaqc/01` SPARK-MDR-001 / `qaqc/02` P1.1): the already-open contradiction that `kWh imp`/`kWh exp` appears under `IntervalProfile` in both docs and shipped artifact remains.
- **ISS-018** (external-schema conformance wording) is a **semantic amplification of a carried weakness** (`qaqc/02` P2.3, previously scored P2): `how-you-implement-ies/conformance.md` names schema validation via `scripts/validate_schema.py` as one of exactly four steps that establish B2C conformance (`:76-83`), then says credential-only issuers may issue production credentials as soon as those checks pass (`:95`) — while the validator substitutes permissive `{"type":"object"}` stubs for the four external schemas it references (`scripts/validate_schema.py:9-43`). This is a named conformance and production-readiness claim resting on a stub, meeting the work order's P1 criterion ("false conformance claim"), not merely an unnamed checklist gap.

Every prior technical release blocker carried from `qaqc/01`/`qaqc/02`/`qaqc/04` (schema reproducibility, PDF false-green, Windows resolver, CI breadth, ElectricityCredential ownership, exact duplicate examples) remains open and unchanged; this audit adds no new mechanical claim about them and defers entirely to the prior reports.

Two further corrections change the shape of the register without changing the release-blocked verdict. First, the **eight/nine MeterData profile-shape count**: of the eight previously-flagged locations, only **one is actually defective** — `schemas/MeterData/v0.6/ReferenceGuide.md:9` asserts "eight distinct profile shapes" with no telemetry/cadence qualifier and never mentions the `DESCRIPTOR` shape anywhere in the document (P2, internally resolvable). The other seven locations correctly scope "eight" to the telemetry/cadence-scoped, individually-requestable profile set — they either state the qualifier explicitly ("eight compact profile shapes representing different read cadences," "eight compact profiles cover every cadence") or, in one case (`use-cases/smart-meter-data-exchange/ies-meter-data-model.md:17-20`), explicitly list `PayloadDescriptorProfile`/`DESCRIPTOR` as a separate object kind before introducing "the eight profile shapes" — and require no correction. Second, the **standards-precedence claims** at `schemas/README.md:87,94` and `use-cases-overview/consumer-energy-passport.md:61,159` falsely say every schema records per-field provenance and that `x-standards-precedence` exists at every schema root: exhaustive artifact search finds zero `x-standards-precedence` keys, while singular `x-standard` occurs in only two of eleven schema-version directories (`ElectricityCredential/v1.2`, `OutageNotification/v0.1`).

A third class of finding is prose that is stale or under-anchored but not defective in substance: `pathways/researcher.md`'s two stale cross-references, `pathways/utility.md`'s two mislabeled links, and the public-status wording across `README.md`/`faq.md`/`how-you-implement-ies/README.md`, which — read closely — are three tense choices describing a status that could be true simultaneously (a completed 30-day challenge and an ongoing live sandbox are not mutually exclusive), not a proven contradiction; the underlying liveness claim remains externally `UNSUPPORTED` (ISS-008, scored **P2** — not a fourth semantic P1) and still requires one owner-approved posture (`OD-E1`) because the work order makes that posture a P1-closure gate as a matter of policy, independent of whether the three texts are logically incompatible. This report accordingly names exactly three P1s — ISS-001, ISS-018, ISS-019 — plus one P1-closure policy gate (`OD-E1`/ISS-008) that is not itself a fourth P1 finding.

---

## 2. Coverage ledger

### 2.1 Corpus ledger — all 79 files

Legend — axes: **1** Product/status · **2** Research/evidence · **3** Architecture · **4** Data/schema semantics · **5** Execution/tooling · **6** Team/governance. Finding IDs refer to Sections 4 (`DUP-`), 5 (`LIR-`) and 7 (`ISS-`) below. Axis columns list every axis the *file* touches; each finding's *own* primary axis is fixed once in Sections 4/5/7 and is not re-derived per file.

#### Root (8)

| # | File | Status | Axes | Findings |
|---|---|---|---|---|
| 1 | `README.md` | READ | 1,2,3,6 | ISS-008 |
| 2 | `SUMMARY.md` | READ | 1,6 | ISS-011, ISS-012 |
| 3 | `_sidebar.md` | READ | 1,6 | ISS-011 |
| 4 | `contributors.md` | READ | 1,6 | NO FINDING |
| 5 | `download-pdf.md` | READ | 1,5 | ISS-015 |
| 6 | `faq.md` | READ | 1,2,6 | ISS-008 |
| 7 | `glossary.md` | READ | 3,4 | NO FINDING |
| 8 | `index.md` | READ | 1,6 | ISS-011, ISS-012, ISS-013 |

#### `what-ies-provides/**` (13)

| # | File | Status | Axes | Findings |
|---|---|---|---|---|
| 9 | `what-ies-provides/README.md` | READ | 1,3 | NO FINDING |
| 10 | `what-ies-provides/register.md` | READ | 3,4 | NO FINDING (target, not source, of ISS-007) |
| 11 | `what-ies-provides/discover.md` | READ | 3 | NO FINDING |
| 12 | `what-ies-provides/exchange.md` | READ | 3,4 | NO FINDING |
| 13 | `what-ies-provides/energy-credentials/README.md` | READ | 3,4 | NO FINDING |
| 14 | `what-ies-provides/schemas-overview/README.md` | READ | 4,6 | NO FINDING (accurate: "eight telemetry profile shapes (plus a shared descriptor object)" — cited as the correct model for ISS-002) |
| 15 | `what-ies-provides/schemas-overview/electricity-credential.md` | READ | 4 | DUP-002.4, DUP-002.13 |
| 16 | `what-ies-provides/schemas-overview/meter-data.md` | READ | 4 | ISS-005 (originates); reports ISS-003 accurately |
| 17 | `what-ies-provides/schemas-overview/meter-data-credential.md` | READ | 4 | ISS-006 (originates), DUP-002.6 |
| 18 | `what-ies-provides/schemas-overview/meter-data-request.md` | READ | 4,5 | ISS-001 (originates, two locations: worked example and §10 line 126), DUP-002.7 |
| 19 | `what-ies-provides/schemas-overview/meter-data-request-credential.md` | READ | 4 | DUP-002.13 |
| 20 | `what-ies-provides/schemas-overview/arr-filing.md` | READ | 4,6 | DUP-002.2 |
| 21 | `what-ies-provides/schemas-overview/outage-notification.md` | READ | 1,4 | NO FINDING |

#### `how-you-implement-ies/**` (7)

| # | File | Status | Axes | Findings |
|---|---|---|---|---|
| 22 | `how-you-implement-ies/README.md` | READ | 1,5 | ISS-008 |
| 23 | `how-you-implement-ies/setup-register.md` | READ | 3,5 | NO FINDING |
| 24 | `how-you-implement-ies/issue-credentials.md` | READ | 3,4,5 | ISS-019 evidence — canonical OpenCred MeterDataCredential `schemaId` at :292,299 |
| 25 | `how-you-implement-ies/digilocker.md` | READ | 3,4 | NO FINDING |
| 26 | `how-you-implement-ies/setup-exchange.md` | READ | 3,5 | NO FINDING |
| 27 | `how-you-implement-ies/build-adapter.md` | READ | 3,5 | ISS-018 |
| 28 | `how-you-implement-ies/conformance.md` | READ | 5,2,6 | ISS-018 |

#### `pathways/**` (6)

| # | File | Status | Axes | Findings |
|---|---|---|---|---|
| 29 | `pathways/README.md` | READ | 6 | ISS-011 |
| 30 | `pathways/authority.md` | READ | 3,6 | NO FINDING |
| 31 | `pathways/researcher.md` | READ | 1,2,3 | ISS-009, ISS-010 |
| 32 | `pathways/secretariat.md` | READ | 3,6 | DUP-002.1 |
| 33 | `pathways/tsp.md` | READ | 3,4 | NO FINDING |
| 34 | `pathways/utility.md` | READ | 3,4 | ISS-007 |

#### `use-cases-overview/**` (8)

| # | File | Status | Axes | Findings |
|---|---|---|---|---|
| 35 | `use-cases-overview/README.md` | READ | 1,6 | DUP-002.8 canonical WIP-status evidence at :13-14; otherwise NO FINDING |
| 36 | `use-cases-overview/consumer-energy-passport.md` | READ | 1,4 | DUP-004 |
| 37 | `use-cases-overview/consumer-meter-digest.md` | READ | 4 | ISS-019 (originates); DUP-002.11 |
| 38 | `use-cases-overview/smart-meter-data-exchange.md` | READ | 4 | DUP-002.11; NO FINDING (reviewed for ISS-002 at :37,93,126; each is cadence-scoped and correct) |
| 39 | `use-cases-overview/der-visibility.md` | READ | 4 | NO FINDING |
| 40 | `use-cases-overview/discom-regulatory-filing.md` | READ | 1,4 | DUP-002.8 |
| 41 | `use-cases-overview/tariff-intelligence.md` | READ | 1,4 | DUP-002.8 |
| 42 | `use-cases-overview/p2p-energy-trading.md` | READ | 3,4,6 | ISS-012 (the omitted page) |

#### `use-cases/**` (9)

| # | File | Status | Axes | Findings |
|---|---|---|---|---|
| 43 | `use-cases/README.md` | READ | 1,6 | DUP-002.10 canonical WIP-status evidence at :20-27; otherwise NO FINDING |
| 44 | `use-cases/consumer-energy-passport/README.md` | READ | 4,5 | DUP-002.9 |
| 45 | `use-cases/consumer-meter-digest/README.md` | READ | 4,5 | ISS-018, ISS-019, DUP-002.9 |
| 46 | `use-cases/der-visibility/README.md` | READ | 4 | NO FINDING |
| 47 | `use-cases/discom-regulatory-filing/README.md` | READ | 1,4 | DUP-002.10; tested five-word checklist-label pair is explicitly non-qualifying under §4 method |
| 48 | `use-cases/p2p-energy-trading/README.md` | READ | 3,4,5 | NO FINDING |
| 49 | `use-cases/smart-meter-data-exchange/README.md` | READ | 4 | NO FINDING (reviewed for ISS-002 at :26; cadence-scoped and correct) |
| 50 | `use-cases/smart-meter-data-exchange/ies-meter-data-model.md` | READ | 4 | ISS-019 evidence — `INTERVAL` + `PT15M` mapping at :41-45; NO FINDING for ISS-002 at :17-20 |
| 51 | `use-cases/tariff-intelligence/README.md` | READ | 1,4 | DUP-002.10; tested five-word checklist-label pair is explicitly non-qualifying under §4 method |

#### `schemas/**/*.md` (28)

| # | File | Status | Axes | Findings |
|---|---|---|---|---|
| 52 | `schemas/README.md` | READ | 4,6 | DUP-004; NO FINDING (reviewed for ISS-002 at :36; cadence-scoped and correct) |
| 53 | `schemas/external/README.md` | READ | 4 | NO FINDING |
| 54 | `schemas/ArrFiling/README.md` | READ | 4,6 | DUP-002.2 |
| 55 | `schemas/ArrFiling/v0.5/README.md` | READ | 4 | ISS-004; DUP-002.3 |
| 56 | `schemas/ElectricityCredential/README.md` | READ | 4,6 | ISS-017, DUP-002.4 |
| 57 | `schemas/ElectricityCredential/v1.0/README.md` | READ | 4 | ISS-005 (evidence) |
| 58 | `schemas/ElectricityCredential/v1.1/README.md` | READ | 4 | ISS-005 (evidence — locally defines `premisesType`); DUP-002.5 |
| 59 | `schemas/ElectricityCredential/v1.2/README.md` | READ | 4 | ISS-005 (evidence); DUP-004 (evidence — uses `x-standard`); DUP-002.5 |
| 60 | `schemas/MeterData/README.md` | READ | 4 | NO FINDING (accurate: "Nine record shapes") |
| 61 | `schemas/MeterData/v0.5/README.md` | READ | 4,5 | ISS-016; DUP-002.3 |
| 62 | `schemas/MeterData/v0.6/CHANGELOG.md` | READ | 4 | NO FINDING |
| 63 | `schemas/MeterData/v0.6/README.md` | READ | 4 | ISS-019 (evidence); NO FINDING (reviewed for ISS-002 at :7; cadence-scoped and correct) |
| 64 | `schemas/MeterData/v0.6/ReferenceGuide.md` | READ | 4 | ISS-002 (originates — sole confirmed instance) |
| 65 | `schemas/MeterData/v0.6/UserGuide.md` | READ | 4,5 | NO FINDING |
| 66 | `schemas/MeterData/v0.6/validation/README.md` | READ | 4,5 | NO FINDING |
| 67 | `schemas/MeterDataCredential/README.md` | READ | 4,6 | NO FINDING (evidence resolving ISS-006); DUP-002.6 |
| 68 | `schemas/MeterDataCredential/v0.6/README.md` | READ | 4 | ISS-019 (evidence); DUP-002.12 |
| 69 | `schemas/MeterDataRequest/README.md` | READ | 4 | DUP-002.7 |
| 70 | `schemas/MeterDataRequest/v0.5/README.md` | READ | 4,5 | NO FINDING |
| 71 | `schemas/MeterDataRequest/v0.6/README.md` | READ | 4 | NO FINDING (does not use "eight"/"nine" profile-count framing; the ISS-002 citation on this row in the prior pass was an error, corrected this pass) |
| 72 | `schemas/MeterDataRequest/v0.6/validation/README.md` | READ | 4,5 | ISS-001 (evidence, opened this pass) |
| 73 | `schemas/MeterDataRequestCredential/README.md` | READ | 4 | ISS-019 evidence — canonical plural policy path at :22 |
| 74 | `schemas/MeterDataRequestCredential/v0.1/README.md` | READ | 4 | ISS-019 evidence — canonical plural policy path at :100; DUP-002.12 |
| 75 | `schemas/OutageNotification/README.md` | READ | 1,4 | NO FINDING |
| 76 | `schemas/OutageNotification/v0.1/README.md` | READ | 4,5 | ISS-014 |
| 77 | `schemas/OutageNotification/v0.1/OutageNotification_Design.md` | READ | 1,3,4,6 | NO FINDING |
| 78 | `schemas/OutageNotification/v0.1/OutageNotification_Implementation.md` | READ | 5 | NO FINDING |
| 79 | `schemas/OutageNotification/v0.1/tools/README.md` | READ | 4,5 | NO FINDING |

**Reconciliation:** 8 + 13 + 7 + 6 + 8 + 9 + 28 = **79/79**, matching Section 2.1 of the work order exactly. No mismatch — Section 11 baseline-drift stop condition not triggered. `git status --short` at report time shows only this deliverable as a delta from baseline.

### 2.2 Evidence-file ledger — individual disposition, every required Section 2.2 file

Per Section 7.1 of the work order, heavy mechanical re-scans (Make regeneration, full validator sweeps, JSON-LD checks) are not rerun; the `qaqc/01`/`qaqc/02`/`qaqc/04` command-level results are treated as fact. Every file in every Section 2.2 evidence class is nonetheless individually listed below with one of two dispositions: **OPENED** (read this pass, with the finding it evidences) or **CARRIED** (relied on the `qaqc/01`/`qaqc/02`/`qaqc/04` matrix; no audience-facing claim in the 79-file corpus required independently reopening it this pass).

**a) `attributes.yaml` (11 tracked)**

| File | Disposition |
|---|---|
| `schemas/ArrFiling/v0.5/attributes.yaml` | OPENED — `info.version: 1.0.0` confirmed (ISS-004) |
| `schemas/ElectricityCredential/v1.0/attributes.yaml` | OPENED — `consumptionProfiles` is an external `$ref` (no local `premisesType`); lines 133-144 (ISS-005) |
| `schemas/ElectricityCredential/v1.1/attributes.yaml` | OPENED — local `premisesType` enum at lines 202-210, field-mapping comment at line 27 (ISS-005) |
| `schemas/ElectricityCredential/v1.2/attributes.yaml` | OPENED — `consumptionProfiles.items` locally references `ConsumptionProfile`, whose definition externally references `MeterServiceProfile/v1.1`; no local `premisesType`; lines 115-135 (ISS-005). Confirms zero `x-standard` occurrences in this source file while bundled `schema.json` has exactly 31 (DUP-004). |
| `schemas/MeterData/v0.5/attributes.yaml` | CARRIED — `qaqc/01`/`qaqc/04` structural pass; no new audience claim |
| `schemas/MeterData/v0.6/attributes.yaml` | OPENED — `version: 0.5.0`, six-shape description at lines 4-6 (ISS-003) |
| `schemas/MeterDataCredential/v0.6/attributes.yaml` | CARRIED — `qaqc/01` P1.2 reproducibility-drift matrix; no new audience claim |
| `schemas/MeterDataRequest/v0.5/attributes.yaml` | CARRIED — `qaqc/01`/`qaqc/04` structural pass; no new audience claim |
| `schemas/MeterDataRequest/v0.6/attributes.yaml` | OPENED — `profileType` enum at lines 134-144 confirms `DESCRIPTOR` excluded from requestable profiles (ISS-002) |
| `schemas/MeterDataRequestCredential/v0.1/attributes.yaml` | CARRIED — `qaqc/01` P1.2 reproducibility-drift matrix; no new audience claim |
| `schemas/OutageNotification/v0.1/attributes.yaml` | OPENED — exact count of 10 `x-standard` occurrences, matching the compiled `schema.json` count exactly (source and compiled agree for this family, unlike ElectricityCredential/v1.2) (DUP-004); disposition of the underlying OutageNotification content otherwise carried |

**b) `schema.json` (11 tracked)**

| File | Disposition |
|---|---|
| `schemas/ArrFiling/v0.5/schema.json` | CARRIED — `qaqc/01` Draft-2020-12 meta-schema pass; no new audience claim |
| `schemas/ElectricityCredential/v1.0/schema.json` | CARRIED — `qaqc/01` meta-schema pass; no new audience claim |
| `schemas/ElectricityCredential/v1.1/schema.json` | CARRIED — `qaqc/01` meta-schema pass; no new audience claim |
| `schemas/ElectricityCredential/v1.2/schema.json` | OPENED — full-file grep confirms exact count of **31** `x-standard` (singular) annotations; source attributes for the same family have zero `x-standard` occurrences. |
| `schemas/MeterData/v0.5/schema.json` | CARRIED — `qaqc/01` meta-schema pass; no new audience claim |
| `schemas/MeterData/v0.6/schema.json` | OPENED — `MonthlyProfile` `$defs` block has no `additionalProperties: false` (ISS-019); also confirms the `Address` stub consumer at line 1162 and `GeoJSONGeometry` stub consumer at line 1165, both reachable from `ServiceDeliveryPoint` (ISS-018) |
| `schemas/MeterDataCredential/v0.6/schema.json` | OPENED — `"additionalProperties": true` explicit at line 7; `MeterDataCredentialSubject` `$defs` at lines 23-46 has only `id`/`meterData` (ISS-019); also confirms the `EnergyCredential` stub consumer at line 10, and that no root-level `required` array exists, so `credentialSubject` is optional at the root (ISS-018) |
| `schemas/MeterDataRequest/v0.5/schema.json` | CARRIED — `qaqc/01` meta-schema pass; no new audience claim |
| `schemas/MeterDataRequest/v0.6/schema.json` | OPENED — `profileType` enum at lines 167-176 confirms `DESCRIPTOR` excluded (ISS-002) |
| `schemas/MeterDataRequestCredential/v0.1/schema.json` | OPENED — confirms the `EnergyCredential` stub consumer at line 10, same pattern as `MeterDataCredential/v0.6` (ISS-018) |
| `schemas/OutageNotification/v0.1/schema.json` | OPENED — confirms the sole other `x-standard` usage (exact count 10 occurrences), zero `x-standards-precedence` (DUP-004); also confirms the `GeoJSONGeometry` stub consumer at lines 308 and 363 (ISS-018) |

**c) `context.jsonld` (11 tracked) — all CARRIED**

| File | Disposition |
|---|---|
| `schemas/ArrFiling/v0.5/context.jsonld` | CARRIED — `qaqc/01`/`qaqc/04`; no audience page in the 79-file corpus asserts specific JSON-LD content for this family |
| `schemas/ElectricityCredential/v1.0/context.jsonld` | CARRIED — same basis |
| `schemas/ElectricityCredential/v1.1/context.jsonld` | CARRIED — same basis |
| `schemas/ElectricityCredential/v1.2/context.jsonld` | CARRIED — same basis |
| `schemas/MeterData/v0.5/context.jsonld` | CARRIED — same basis |
| `schemas/MeterData/v0.6/context.jsonld` | CARRIED — same basis |
| `schemas/MeterDataCredential/v0.6/context.jsonld` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.5/context.jsonld` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.6/context.jsonld` | CARRIED — same basis |
| `schemas/MeterDataRequestCredential/v0.1/context.jsonld` | CARRIED — same basis |
| `schemas/OutageNotification/v0.1/context.jsonld` | CARRIED — same basis |

Each family's `context.jsonld` existing at all is a `qaqc/01`/`qaqc/04` carried fact; no audience-facing page in the 79-file corpus asserts specific JSON-LD content, so no row above required opening the file this pass.

**d) `vocab.jsonld` (11 tracked) — all CARRIED**

| File | Disposition |
|---|---|
| `schemas/ArrFiling/v0.5/vocab.jsonld` | CARRIED — same basis as (c) |
| `schemas/ElectricityCredential/v1.0/vocab.jsonld` | CARRIED — same basis |
| `schemas/ElectricityCredential/v1.1/vocab.jsonld` | CARRIED — same basis |
| `schemas/ElectricityCredential/v1.2/vocab.jsonld` | CARRIED — same basis |
| `schemas/MeterData/v0.5/vocab.jsonld` | CARRIED — same basis |
| `schemas/MeterData/v0.6/vocab.jsonld` | CARRIED — same basis |
| `schemas/MeterDataCredential/v0.6/vocab.jsonld` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.5/vocab.jsonld` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.6/vocab.jsonld` | CARRIED — same basis |
| `schemas/MeterDataRequestCredential/v0.1/vocab.jsonld` | CARRIED — same basis |
| `schemas/OutageNotification/v0.1/vocab.jsonld` | CARRIED — same basis |

**e) `schemas/**/examples/*.json` (62 tracked exactly — verified this pass by directory listing; corrects the prior pass's per-family sub-counts, which undercounted ElectricityCredential and MeterData v0.6 and overcounted MeterData v0.5's post-duplicate remainder)**

| File | Disposition |
|---|---|
| `schemas/ArrFiling/v0.5/examples/arr_filings.json` | CARRIED — `qaqc/01`/`qaqc/02` structural-validation pass; searched for ISS-019 disputed tokens (see note below), no match |
| `schemas/ElectricityCredential/v1.0/examples/example.json` | CARRIED — same basis |
| `schemas/ElectricityCredential/v1.1/examples/example.json` | CARRIED — same basis |
| `schemas/ElectricityCredential/v1.1/examples/example-parallel-metering.json` | CARRIED — same basis |
| `schemas/ElectricityCredential/v1.1/examples/example-submetering.json` | CARRIED — same basis |
| `schemas/ElectricityCredential/v1.2/examples/example.json` | CARRIED — same basis |
| `schemas/ElectricityCredential/v1.2/examples/example-parallel-metering.json` | CARRIED — same basis |
| `schemas/ElectricityCredential/v1.2/examples/example-submetering.json` | CARRIED — same basis |
| `schemas/MeterData/v0.5/examples/AggregatedFeeder.json` | CARRIED — same basis |
| `schemas/MeterData/v0.5/examples/BillingProfile.json` | CARRIED — `qaqc/04` byte-identical-pair fact (ISS-016/DUP-003) |
| `schemas/MeterData/v0.5/examples/CustomerBillingSummary.json` | CARRIED — `qaqc/04` byte-identical-pair fact (ISS-016/DUP-003) |
| `schemas/MeterData/v0.5/examples/CustomerProfile.json` | CARRIED — same basis as other structural-pass rows |
| `schemas/MeterData/v0.5/examples/DailyProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.5/examples/EventProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.5/examples/InstantaneousProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.5/examples/IntervalProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.5/examples/MultiMeterBulkDataset.json` | CARRIED — same basis |
| `schemas/MeterData/v0.5/examples/MultiMeterBulkDatasetShortCodes.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/AggregatedFeeder.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/AggregatedFeeder_Elaborated.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/AlarmProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/Anonymised_Telemetry_Response.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/Anonymised_Topology_Example.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/BillDetails.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/Billing_MeterChange.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/Billing_MonthlyProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/CustomerBillingSummary.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/CustomerMapping.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/CustomerProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/DailyProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/DailyProfile_Elaborated.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/DailyProfile_ReadingMode.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/DailyProfile_ReadingMode_Elaborated.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/EventProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/InstantaneousProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/IntervalProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/IntervalProfile_Elaborated.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/MDM_MonthlyProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/MonthlyProfile.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/MonthlyProfile_MultipleResets.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/MultiMeterBulkDataset.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/MultiMeterBulkDataset_Elaborated.json` | OPENED — :277-285 confirms `profileType: INTERVAL` plus `intervalPeriod.duration: PT15M` (ISS-019) |
| `schemas/MeterData/v0.6/examples/MultiMeterBulkDatasetShortCodes.json` | CARRIED — same basis |
| `schemas/MeterData/v0.6/examples/MultiMeterBulkDatasetShortCodes_Elaborated.json` | CARRIED — same basis |
| `schemas/MeterDataCredential/v0.6/examples/example-customer-profile.json` | CARRIED — same basis |
| `schemas/MeterDataCredential/v0.6/examples/example-interval-profile.json` | CARRIED — same basis |
| `schemas/MeterDataCredential/v0.6/examples/example-monthly-profile.json` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.5/examples/MeterDataRequest_Billing_Capability.json` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.5/examples/MeterDataRequest_DigestCredentialFilter.json` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.5/examples/MeterDataRequest_Example.json` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.5/examples/MeterDataRequest_FeederAllowance.json` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.5/examples/MeterDataRequest_MDM_Capability.json` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.5/examples/MeterDataRequest_Modes.json` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json` | OPENED, full file — lines 15-18 (ISS-001) |
| `schemas/MeterDataRequest/v0.6/examples/Authorisation_Example.json` | CARRIED — same basis as other structural-pass rows |
| `schemas/MeterDataRequest/v0.6/examples/Billing_Capabilities_Example.json` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.6/examples/Capabilities_Example.json` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.6/examples/MDM_Capabilities_Example.json` | CARRIED — same basis |
| `schemas/MeterDataRequest/v0.6/examples/Request_Example.json` | CARRIED — same basis |
| `schemas/MeterDataRequestCredential/v0.1/examples/example.json` | CARRIED — same basis |
| `schemas/OutageNotification/v0.1/examples/discom_planned_shutdown.json` | CARRIED — same basis |
| `schemas/OutageNotification/v0.1/examples/outage_notifications.json` | CARRIED — same basis |

Per-family example counts, verified this pass by direct directory listing (correcting the prior pass, which stated "ElectricityCredential — 8 files," "MeterData/v0.5 — 7 remaining," and "MeterData/v0.6 — 21 files"): `ArrFiling/v0.5` 1; `ElectricityCredential` **7** total across v1.0(1)/v1.1(3)/v1.2(3); `MeterData/v0.5` 10 total, **8 remaining** after excluding the byte-identical `BillingProfile.json`/`CustomerBillingSummary.json` pair; `MeterData/v0.6` **26**; `MeterDataCredential/v0.6` 3; `MeterDataRequest/v0.5` 6; `MeterDataRequest/v0.6` 6 (including the OPENED `Anonymised_Telemetry_Request.json`); `MeterDataRequestCredential/v0.1` 1; `OutageNotification/v0.1` 2. Sum: 1+7+10+26+3+6+6+1+2 = 62, matching the tracked total exactly.

**ISS-019 token search, applied to every one of the 62 files above (CARRIED and OPENED alike):** each file was mechanically searched (case-insensitive, whole-tree) for the exact disputed tokens `SUMMARY_TOTAL`, `SUMMARY_PEAK`, `SUMMARY_TOD`, `meterReference`, `dataQuality`, and `RAW_15M` — zero matches anywhere in `schemas/` for any of these six tokens, which is affirmative evidence for ISS-019, not merely an unopened default. This zero-match claim is scoped to these six exact tokens only; the generic words "period" and "summary" do occur legitimately elsewhere in `schemas/` (e.g. `intervalPeriod`, `timePeriod`, `integrationPeriod`, and descriptive prose), so no claim of zero matches is made for those generic terms.

**ISS-019 implementation-contract cross-check:** across the 79-file audience corpus (excluding `qaqc/`), the exact code tokens `requiredCredential` (singular), `granularityOptions`, and `maxRange` occur only at `use-cases/consumer-meter-digest/README.md:69-70`; repository guidance instead documents `offerAttributes.policy.requiredCredentials` at `schemas/MeterDataRequestCredential/README.md:22` and `v0.1/README.md:100`. The same guide explicitly labels `MeterDataCredential/v0.6` as an OpenCred `schemaId` at `:50,74`, while the linked issuance guide gives the registry ID `ies/meter-data-credential/v0.6` at `how-you-implement-ies/issue-credentials.md:292,299`. Other audience uses of `MeterDataCredential/v0.6` are human-facing family/version labels or paths, not competing OpenCred `schemaId` instructions.

**f) `schemas/**/validation/**` (19 tracked, includes 2 Makefiles and 2 READMEs already counted in the corpus)**

| File | Disposition |
|---|---|
| `schemas/MeterData/v0.6/validation/README.md` | CARRIED — corpus file #66, no new claim beyond `qaqc/01`/`qaqc/02` |
| `schemas/MeterData/v0.6/validation/Makefile` | CARRIED — `qaqc/01` command-level pass |
| `schemas/MeterData/v0.6/validation/out.txt` | CARRIED — build artifact, no audience claim |
| `schemas/MeterData/v0.6/validation/test_cases/invalid_cumulative_decrease.json` | CARRIED — `qaqc/02` 6/6 fixture-pass fact |
| `schemas/MeterData/v0.6/validation/test_cases/invalid_math_consistency.json` | CARRIED — same |
| `schemas/MeterData/v0.6/validation/test_cases/invalid_missing_descriptor.json` | CARRIED — same |
| `schemas/MeterData/v0.6/validation/test_cases/invalid_missing_descriptor_ref.json` | CARRIED — same |
| `schemas/MeterData/v0.6/validation/test_cases/invalid_profile_type_mismatch.json` | CARRIED — same |
| `schemas/MeterData/v0.6/validation/test_cases/valid_interval_profile.json` | CARRIED — same |
| `schemas/MeterData/v0.6/validation/test_runner.py` | CARRIED — `qaqc/02` command-level result |
| `schemas/MeterData/v0.6/validation/validator.py` | CARRIED — `qaqc/02` command-level result |
| `schemas/MeterDataRequest/v0.6/validation/README.md` | OPENED, full file — lines 7-11 (ISS-001) |
| `schemas/MeterDataRequest/v0.6/validation/Makefile` | CARRIED — `qaqc/01` command-level pass |
| `schemas/MeterDataRequest/v0.6/validation/test_cases/invalid_authorisation_expired.json` | CARRIED — `qaqc/02` 4/4 fixture-pass fact |
| `schemas/MeterDataRequest/v0.6/validation/test_cases/invalid_request_mode_unsupported.json` | CARRIED — same |
| `schemas/MeterDataRequest/v0.6/validation/test_cases/invalid_request_profile_mismatch.json` | OPENED, full file — lines 7-10, the invalid fixture pairing `kWh imp` with `IntervalProfile` (ISS-001) |
| `schemas/MeterDataRequest/v0.6/validation/test_cases/valid_request.json` | OPENED, full file — lines 7-10, the valid fixture pairing `kWh imp block` with `IntervalProfile` (ISS-001) |
| `schemas/MeterDataRequest/v0.6/validation/test_runner.py` | CARRIED — `qaqc/02` command-level result |
| `schemas/MeterDataRequest/v0.6/validation/validator.py` | CARRIED — `qaqc/02` command-level result (exit 1 on the shipped example) |

**g) Version-level Makefiles (3, excluding the 2 validation Makefiles already listed in (f))**

| File | Disposition |
|---|---|
| `schemas/MeterData/v0.6/Makefile` | CARRIED — no audience claim makes a build-target assertion specific enough to require opening it |
| `schemas/MeterDataRequest/v0.6/Makefile` | CARRIED — same |
| `schemas/OutageNotification/v0.1/Makefile` | CARRIED — same |

**h) Registries and crosswalks (6)**

| File | Disposition |
|---|---|
| `schemas/MeterData/v0.5/OBISMapping.json` | CARRIED — `qaqc/04` prior review |
| `schemas/MeterData/v0.6/IES codes.json` | OPENED — lines 338-348 (`kWh imp`), 352-366 (`kWh exp`): both `profiles: ["DAILY","MONTHLY","INSTANTANEOUS"]`; lines 453-467 (`kWh imp block`): `profiles: ["INTERVAL"]` (ISS-001) |
| `schemas/OutageNotification/v0.1/fault_reason_crosswalk.json` | CARRIED — `qaqc/04` prior review, cross-checked narratively against `OutageNotification_Design.md` §9.1, found consistent |
| `schemas/OutageNotification/v0.1/FeederStatusIngest.openapi.yaml` | CARRIED — `qaqc/04` prior review |
| `schemas/OutageNotification/v0.1/tools/transform_discom_csv.py` | CARRIED — `qaqc/04` prior review |
| `schemas/OutageNotification/v0.1/tools/discom_planned_shutdown.csv` | CARRIED — `qaqc/04` prior review |

**i) Build/CI controls (28: root `Makefile`, `.gitbook.yaml`, `.github/workflows/build-pdf.yml`, 22 `scripts/*.py`, `scripts/build_pdf.sh`, 2 `scratch/*.py`)**

| File | Disposition |
|---|---|
| `Makefile` | CARRIED — confirms ElectricityCredential exclusion at lines 20-22 (`qaqc/01`/`qaqc/04` fact; ISS-017) |
| `.gitbook.yaml` | CARRIED — `qaqc/01` command-level result |
| `.github/workflows/build-pdf.yml` | CARRIED — `qaqc/01`/`qaqc/02` Ubuntu-only CI-breadth fact |
| `scripts/build_pdf.py` | CARRIED — `qaqc/01` P1.3 missing-source-count / CP-1252 facts (ISS-015) |
| `scripts/build_pdf.sh` | CARRIED — `qaqc/02` fact (no argument parser) |
| `scripts/check_jsonld.py` | CARRIED — `qaqc/01`/`qaqc/02` `pyld`-unwired fact |
| `scripts/cleanup_examples.py` | CARRIED — no audience claim references it |
| `scripts/compare_v05_v06.py` | CARRIED — `qaqc/01` P2.6 fact |
| `scripts/format_examples.py` | CARRIED — no audience claim references it |
| `scripts/generate_billing_from_mdm.py` | CARRIED — no audience claim references it |
| `scripts/generate_elaborated_profiles.py` | CARRIED — no audience claim references it |
| `scripts/generate_external_field_tables.py` | CARRIED — `qaqc/02` fact (requires separate DEG checkout) |
| `scripts/generate_field_tables.py` | OPENED, full file this pass — confirms it reads only the already-compiled `schema.json` and resolves solely local `#/$defs/...` refs, with no external-`$ref` expansion capability (ISS-005); also the `qaqc/02` `--all --check` fact is the basis for treating the compiled field-reference tables as authoritative throughout this report |
| `scripts/generate_index.py` | OPENED, full file — hardcoded 46-entry section list (lines 77-144) is the direct basis for deriving the Summary-only-14 / index-only-3 sets (ISS-011, ISS-012, ISS-013) |
| `scripts/generate_openadr_schema.py` | CARRIED — no audience claim references it |
| `scripts/generate_schema.py` | CARRIED — `qaqc/01` P1.2 fact (correct cross-file `$ref` mapping, contrasted with the permissive generator) |
| `scripts/generate_schema_permissive.py` | CARRIED — `qaqc/01` P1.2 fact (Make-selected generator, drift source) |
| `scripts/migrate_v05_to_v06.py` | CARRIED — no audience claim references it |
| `scripts/migrate_v06_examples.py` | CARRIED — no audience claim references it |
| `scripts/migrate_v06_to_openadr.py` | CARRIED — no audience claim references it |
| `scripts/migrate_v06_to_v06_flat.py` | CARRIED — no audience claim references it |
| `scripts/patch_obis.py` | CARRIED — no audience claim references it |
| `scripts/remove_customerRefs.py` | CARRIED — no audience claim references it |
| `scripts/validate_links.py` | CARRIED — `qaqc/01`/`qaqc/02` GitBook-slug-rule fact (ISS-013 basis) |
| `scripts/validate_schema.py` | OPENED, lines 1-60 — four permissive substitute objects at :9-38 and their external-URL registrations at :39-43, confirmed verbatim (ISS-018) |
| `scripts/verify_v05_v06_equivalence.py` | CARRIED — `qaqc/01` P2.6 fact (exit 1) |
| `scratch/transform_obis.py` | CARRIED — no audience claim references it |
| `scratch/verify_no_loss.py` | CARRIED — `qaqc/01` fact (crashes on removed `OBISMapping.json` path) |

No broad claim in this report ("all", "every", "consistent", "zero") rests on partial-class sampling; every full-class claim above (e.g., "zero `x-standards-precedence` occurrences in any `schema.json`/`attributes.yaml` under `schemas/`", "zero matches for the six ISS-019 disputed tokens anywhere in `schemas/`", "zero `pathways` references outside `pathways/`") was established by an exhaustive search of the full class, not a sample.

### 2.3 Axis closures (Section 4 of the work order)

Each of the six audit axes is closed here with standalone evidence, before any cross-axis synthesis in Sections 3, 6, and 7.

1. **Product/status.** Findings: ISS-008 (status-posture divergence across `README.md`/`faq.md`/`how-you-implement-ies/README.md`), the "Live in pilot" status field on `use-cases-overview/consumer-meter-digest.md:10` (accurate as a status label independent of ISS-019's field-content problem), DUP-002.8/.10 (WIP-hint duplication, itself an honest status signal). **Verdict:** product/status claims are internally coherent except the live/pilot posture, which is externally `UNSUPPORTED` and requires one owner-approved formulation (`OD-E1`) — not because the three texts are logically incompatible (they are not), but because the underlying liveness claim cannot be verified from the repository.
2. **Research/evidence.** Findings: ISS-008 (externally unverifiable pilot claims, classified `UNSUPPORTED` rather than fact), ISS-018 (a named conformance claim resting on evidence — permissive stubs — that does not establish what it is cited for). **Verdict:** both instances where the corpus treats something as established fact are either unverifiable from the repository or evidenced only by a stub; both are folded into their axis-4/axis-5 findings above rather than double-counted here.
3. **Architecture.** Findings: ISS-007 (`pathways/utility.md` mislabels plain `register.md` subsections), ISS-009/ISS-010 (`pathways/researcher.md` stale cross-references to a non-existent page and non-existent "concepts pages"), DUP-002.1 (`pathways/secretariat.md` self-referential template block). Source-of-truth topics 1-3 (Register/Discover/Exchange; B2B/B2C boundaries; identity and data movement) are `ALIGNED` with no verbatim divergence found across every dependent page read. **Verdict:** the core architecture narrative itself is sound; every axis-3 defect is residue or staleness in a pointer to it, not a defect in the narrative.
4. **Data/schema semantics.** Findings: ISS-001/LIR-001 (MDR — spans overview prose and the shipped `Anonymised_Telemetry_Request.json` example; not confined to either layer), ISS-002/DUP-001 (eight/nine shapes — one confirmed defect after per-occurrence reinspection, seven of eight originally-flagged locations correctly scoped), ISS-003/LIR-004 (MeterData v0.6 metadata staleness), ISS-004 (ArrFiling versioning), ISS-005/LIR-002 (`premisesType` source-vs-bundled clarity issue — reclassified `NO CONTRADICTION`, not drift), ISS-006/LIR-003 (non-existent revocation-wording contradiction), ISS-016/DUP-003 (duplicate examples), ISS-019/LIR-008 (Consumer Meter Digest fields not defined by the current schema), DUP-004 (standards-precedence false claim). **Verdict:** `DRIFT`, carrying two of the three P1s in this pass (ISS-001, spanning prose and a shipped artifact; ISS-019, confined to prose) — both internally resolvable without an owner decision — plus a set of P2/P3 metadata findings, of which `OD-E5` requires owner decision on convention, `OD-S1` is internally resolvable in-source, and ISS-004 remains escalated (`OD-E5`) rather than internally adjudicable.
5. **Execution/tooling.** Findings: LIR-005/ISS-015 (PDF completeness claim vs. discarded missing-source count), LIR-007/ISS-014 (`./examples` directory links resolving to live 404s), ISS-012/ISS-013 (`generate_index.py`'s hardcoded list and slugger drifting from `SUMMARY.md` and GitBook respectively), ISS-018 (validator-based conformance claim resting on stubs). **Verdict:** a consistent pattern across four independent findings — audience-facing claims about what the tooling establishes (completeness, link validity, index accuracy, conformance) systematically overstate what it actually establishes.
6. **Team/governance.** Findings: ISS-011 (`pathways/**` absent from all three navigation surfaces and from every other corpus file — `OD-E6`), ISS-017 (ElectricityCredential upstream-authoritative framing vs. `Makefile:20-22` exclusion with no sync verifier — `OD-E3`). **Verdict:** two open ownership/publication-intent questions, neither closable from repository evidence alone; no page makes a false governance claim.

---

## 3. Source-of-truth map

| # | Topic | Canonical source | Verdict | Navigation reachability |
|---|---|---|---|---|
| 1 | Register / Discover / Exchange | `README.md#how-it-works-three-steps` + `what-ies-provides/README.md` | **ALIGNED** | Canonical source and its direct dependents (`how-you-implement-ies/*`, all use-case pages) are reachable through `SUMMARY.md`/`_sidebar.md`. **`pathways/**` is not** — despite pathway pages narratively building on this same Register/Discover/Exchange sequence, none of the 6 pathway files is linked from `SUMMARY.md`, `_sidebar.md`, or `index.md`, and no other corpus file outside `pathways/` links into it either (confirmed by an exhaustive case-insensitive search for "pathways" across all 79 files: the only hits are `pathways/README.md` itself). See ISS-011. |
| 2 | B2B vs B2C boundaries | `what-ies-provides/discover.md#two-rails-two-kinds-of-trust` | **ALIGNED** | Same trust-model table (credentials = unilateral/any-channel; data exchange = bilateral/Beckn-bounded) restated consistently in `exchange.md`, `energy-credentials/README.md`, `issue-credentials.md`, `setup-exchange.md`, and every use-case page that names its rail. No verbatim divergence found. Reachable via nav. |
| 3 | Identity and data movement (DID/DeDi, Beckn signing, DigiLocker, adapter placement, consent) | `what-ies-provides/register.md` + `how-you-implement-ies/setup-register.md` | **ALIGNED, with one documented and consistent exception** | P2P Energy Transaction deliberately uses **plain network subscriber IDs**, not `did:web`, for TP/LP/DISCOM participants (`use-cases-overview/p2p-energy-trading.md §3`, `use-cases/p2p-energy-trading/README.md`) — stated explicitly and identically in both P2P pages. One residue: `pathways/utility.md` mislabels a plain subsection of `register.md` as "Appendix D" (ISS-007) — cosmetic, not a routing error. |
| 4 | Schema, version, and field semantics | `schemas/README.md#versioning` + each family's own field-reference table | **DRIFT** | Seven confirmed instances: the MeterDataRequest overview/example register-code contradiction spanning prose and a shipped artifact (ISS-001), MeterData v0.6 profile-shape count — one confirmed instance after reinspection (ISS-002), MeterData v0.6 `attributes.yaml` metadata staleness (ISS-003), ArrFiling `attributes.yaml` version label (ISS-004), the `premisesType` source-vs-bundled clarity issue (ISS-005, `NO CONTRADICTION`), the standards-precedence claim (DUP-004), and Consumer Meter Digest's payload fields not defined by the current schema (ISS-019). Five of the seven (ISS-001, ISS-002, ISS-003, ISS-005, ISS-019) are internally adjudicable from artifacts already in the corpus/evidence classes; DUP-004 is likewise internally adjudicable; **ISS-004 is not** — it remains escalated at `OD-E5`, so this topic is not uniformly internally adjudicable — see Section 7. |
| 5 | Use-case/pathway parity (7 overview↔implementation pairs; 5 role pathways) | `use-cases-overview/README.md` + `use-cases/README.md` template | **ALIGNED for 6 of 7 pairs; one content-layer P1; navigation DRIFT** | Consumer Meter Digest is the exception: both pages share a non-schema payload model, while the guide adds non-canonical `schemaId`, policy-path, and undefined capability-key claims (ISS-019). Navigation: all six `pathways/**` files are absent from `SUMMARY.md`, `_sidebar.md`, and `index.md` (ISS-011); P2P overview is absent from `index.md`'s hardcoded list (ISS-012). |
| 6 | Security, privacy, and conformance | `how-you-implement-ies/conformance.md` + `scripts/validate_schema.py` | **FALSE CONFORMANCE CLAIM (P1)**, not merely "no canonical source" | `conformance.md:76-83` frames `scripts/validate_schema.py` as step 2 of exactly four self-contained B2C checks that establish conformance, and `:95` promotes passing those checks directly to production issuance. `scripts/validate_schema.py:9-43` defines and registers permissive `{"type":"object"}` substitutes for four external schema URLs, but only three are currently consumed: `EnergyCredential` at MeterDataCredential and MeterDataRequestCredential; `Address` and `GeoJSONGeometry` at MeterData; and `GeoJSONGeometry` again at OutageNotification. There is no `EnergyResource` consumer. The B2B path (`conformance.md:33,72`), `build-adapter.md:100-110,120,157`, and the Consumer Meter Digest checklist (`use-cases/consumer-meter-digest/README.md:76`) repeat canonical-schema-validation promises without this boundary. See ISS-018. |
| 7 | Live / pilot / WIP / timeline / actor assertions | `README.md#pilots-and-status` | **UNSUPPORTED (externally unverifiable), not a proven contradiction** | Three texts, read closely: `README.md:105` — "IES is already running in a test environment... the sandbox is working. Four pilot DISCOMs... **undertook** a 30-day challenge" (present tense for the sandbox, simple past — not past-perfect — for the challenge); `faq.md:45` — "It **is live**. The sandbox **is running**, and four pilot DISCOMs **are building** in it now" (present/ongoing); `how-you-implement-ies/README.md:120` — "The four pilot DISCOMs each **went** from cold start to four demonstrated use cases in 30 days" (simple past, describing the challenge specifically, not the sandbox's current state). A completed 30-day challenge and an ongoing live sandbox are not mutually exclusive readings — all three are compatible with a single underlying timeline ("the challenge finished; DISCOMs continue using the sandbox"). The claim this repository cannot verify is whether that timeline is currently true at all. Classified `UNSUPPORTED` per work order §11, not `CONTRADICTION`. Still blocks P1 closure (`OD-E1`) per work order §12, because the work order gates on the posture being owner-approved, independent of internal consistency. See ISS-008. |

---

## 4. Duplication register

| ID | Type (§6 taxonomy) | Primary axis | Instances | Canonical candidate | Variance / harm | Treatment |
|---|---|---|---|---|---|---|
| **DUP-001** | Redundant normative prose (defect, one confirmed instance) | 4 | All eight originally-flagged locations were individually reinspected in full surrounding context this pass: `schemas/MeterData/v0.6/README.md:7`; `schemas/MeterData/v0.6/ReferenceGuide.md:9`; `schemas/README.md:36`; `use-cases-overview/smart-meter-data-exchange.md:37,93,126`; `use-cases/smart-meter-data-exchange/README.md:26`; `use-cases/smart-meter-data-exchange/ies-meter-data-model.md:17-20`. **Only one is defective: `schemas/MeterData/v0.6/ReferenceGuide.md:9`** ("the standard organizes data exchanges into eight distinct profile shapes," with no cadence/telemetry qualifier, and no mention anywhere in that document of the separate `DESCRIPTOR`/`PayloadDescriptorProfile` shape). The other seven state "eight" with an explicit cadence/telemetry scope ("eight compact profile shapes representing different read cadences," `MeterData/v0.6/README.md:7`; "8 compact profiles: CUSTOMER...ALARM" naming exactly the eight telemetry profiles, `schemas/README.md:36`; "cover every cadence" / "covering every smart-meter cadence," `smart-meter-data-exchange.md:37` and `use-cases/smart-meter-data-exchange/README.md:26`, with `:93` and `:126` terse recaps inheriting that same scoping from the same document) — or, at `ies-meter-data-model.md:17-20`, explicitly lists `PayloadDescriptorProfile`/`DESCRIPTOR` as a separate object kind *before* introducing "the eight profile shapes," which is the clearest correct treatment of the nine-total/eight-telemetry-plus-one-descriptor split of all eight locations checked. | `schemas/MeterData/README.md` ("Nine record shapes, discriminated by `profileType`") — matches the compiled field-reference table in `schemas/MeterData/v0.6/README.md` (a `PayloadDescriptorProfile`/`DESCRIPTOR` block exists alongside the other eight) | The correct model is: **nine total record shapes = one descriptor (`DESCRIPTOR`/`PayloadDescriptorProfile`) plus eight telemetry/reading profiles**; `DESCRIPTOR` is not itself requestable through MeterDataRequest (`MeterDataRequest/v0.6/attributes.yaml:134-144` and `schema.json:167-176` both confirm it is excluded from the requestable-profile enum). Only `ReferenceGuide.md:9` falsely implies eight is the *total* shape count with no telemetry/cadence scope and no acknowledgment of `DESCRIPTOR` anywhere in the document. The other seven locations already correctly distinguish, or correctly scope to, the eight-telemetry/nine-total split and require no change. Harm is confined to the one defective location: a reader relying solely on `ReferenceGuide.md` would conclude MeterData v0.6 has eight total shapes. | Correct only `schemas/MeterData/v0.6/ReferenceGuide.md:9` — reword to name the cadence/telemetry scope explicitly (e.g. "eight telemetry profile shapes, plus the shared `PayloadDescriptorProfile`/`DESCRIPTOR` dictionary") and add a brief mention of `DESCRIPTOR` to the document. Do not change the other seven locations — they are already correct as scoped. Never describe `DESCRIPTOR` as requestable. Canonical source: `schemas/MeterData/README.md` plus the compiled field-reference table. See ISS-002. |
| **DUP-002** | Mixed (see per-cluster type below) | — (per-cluster) | Re-derived this pass — see methodology and full list below | — | — | — |
| **DUP-003** | Copy-paste residue / stale exact duplicate | 4 | `schemas/MeterData/v0.5/examples/BillingProfile.json` and `CustomerBillingSummary.json` — byte-identical, 89 lines (carried fact, `qaqc/04`) | `BillingProfile.json` — it is the one referenced from `schemas/MeterData/v0.5/README.md:151` | `CustomerBillingSummary.json` is unreferenced from any prose in the audience corpus and inflates example coverage for a schema version (v0.5) superseded by v0.6. | Recommend removing or clearly repurposing `CustomerBillingSummary.json`, or documenting why the duplicate is intentional. Owner decision: `OD-E8`. See ISS-016. |
| **DUP-004** | Redundant normative prose — mutually consistent universality claims that contradict the schema artifacts | 4 | `schemas/README.md:87` ("Every schema in IES records, per field, the standard that governs it") and `:94` (`x-standards-precedence` at every root; `x-standard` on every property), restated at `use-cases-overview/consumer-energy-passport.md:61,159` | Artifact inventory itself: zero plural/root keys; singular `x-standard` only where present | Exhaustive search of all 22 `schema.json`/`attributes.yaml` files across 11 version directories finds zero `x-standards-precedence` or plural `x-standards`. Singular `x-standard` occurs 31 times in `ElectricityCredential/v1.2/schema.json` and 10 times each in OutageNotification's compiled and source artifacts; it is present in only two of eleven version directories. Thus both the broad sentence at `schemas/README.md:87` and the key-specific claims at `:94`/Consumer Energy Passport are false. | Correct `schemas/README.md:87,94` and both Consumer Energy Passport locations to state the observed optional scope or remove universality. Preserve the separate canonical standards order at `schemas/README.md:89-92`. No owner decision needed. |

### DUP-002 — exact-paragraph duplicate groups (re-derived this pass)

**Methodology.** `qaqc/04` carries the input fact "exact-paragraph scan still reports 7 duplicate groups, unchanged from baseline" (§ Deleted-page / duplication cleanup row) without naming the groups or the scan parameters, and the work order (§6) is explicit that this count is "an input list, not a verdict" and that "counts never substitute for per-cluster semantic judgment." Per the current correction cycle, deferring the re-derivation to a future pass is no longer acceptable, so this pass performed the re-derivation directly: every one of the 79 corpus files was split into blank-line-delimited blocks and each block was normalized and compared for byte-for-byte duplication only when it has ≥8 words and sentence punctuation. Excluded intentionally were (a) fenced code blocks, (b) Markdown tables, (c) list-only/checklist label blocks (for example: `## Checklist`, `## References`, `## Scope and Purpose`), (d) auto-generated markers (`<!-- FIELD-TABLE:START -->`), and (e) the repeated "Auto-generated from `schema.json`" footer note. None of these exclusions are omitted by design; each is documented here because it intentionally removes structural repeats rather than substantive prose overlap.

This method surfaces **14 qualifying exact block-pair groups**, which reconcile to **13 stable repeated-concept clusters** under the work order's "one stable `DUP-###` cluster per repeated concept" rule. DUP-002.9 combines two adjacent qualifying block pairs between the same two guides (the checklist intro sentence and Step 0 sentence) into one checklist-template concept; it does not count the excluded heading between them. The corpus is unchanged, so the difference from `qaqc/04`'s uninstantiated "7" is scanner parameterization, not new content. Most matches are sentence-level template blocks; a stricter three-sentence threshold finds fewer. Five QE-identified pairs were tested: four qualify; the fifth is the five-word checklist label documented after the table and excluded by the declared threshold/list-label rule. The table is exhaustive at both levels: 14 qualifying block-pair groups, 13 judged concept clusters.

| Sub-ID | Instances | Primary axis | Canonical candidate | Owner | Taxonomy | Semantic judgment | Treatment |
|---|---|---|---|---|---|---|---|
| **DUP-002.1** | `pathways/secretariat.md:150-152` and `:180-182` | 6 | `pathways/secretariat.md:150-152` | IES documentation owner — Pathways | Generated/versioned/template reuse | Hand-authored same-file template; source exemplar is the first block, boundary is only the three-line "References & Anchors" footer inside two `<details>` sections, and no generator/version propagation is claimed. | Accept; keep both role-local footers synchronized under the named owner. |
| **DUP-002.2** | `schemas/ArrFiling/README.md:3` and `what-ies-provides/schemas-overview/arr-filing.md:3` | 4 | `schemas/ArrFiling/README.md:3` | IES Cell — ArrFiling schema docs | Intentional overview-detail layering | Family page is the detail source; overview repeats only the one-sentence scope tagline and links onward, with no mutable rule. | Accept; family page remains canonical. |
| **DUP-002.3** | `schemas/ArrFiling/v0.5/README.md:46-47` and `schemas/MeterData/v0.5/README.md:49-50` | 5 | `schemas/ArrFiling/v0.5/README.md:44-47` | IES Cell — versioned schema docs | Generated/versioned/template reuse | Hand-authored exemplar, not generator output; boundary is only the validation heading/lead, while commands and version content remain family-specific. | Accept within that two-line boundary; owner must update both if the common validation instruction changes. |
| **DUP-002.4** | `schemas/ElectricityCredential/README.md:3` and `what-ies-provides/schemas-overview/electricity-credential.md:3` | 4 | `schemas/ElectricityCredential/README.md:3` | IES Cell — ElectricityCredential mirror docs | Intentional overview-detail layering | Family page is the detail source; overview repeats only its one-sentence scope tagline. | Accept; family page remains canonical. |
| **DUP-002.5** | `schemas/ElectricityCredential/v1.1/README.md:7` and `schemas/ElectricityCredential/v1.2/README.md:7` | 4 | `schemas/ElectricityCredential/v1.2/README.md:7` | Beckn DEG upstream / IES mirror steward | Generated/versioned/template reuse | Current v1.2 mirror is the candidate source; reuse boundary is the single unchanged description line, while all version-specific artifacts remain isolated. | Accept only within that one-line mirror boundary. |
| **DUP-002.6** | `schemas/MeterDataCredential/README.md:3` and `what-ies-provides/schemas-overview/meter-data-credential.md:3` | 4 | `schemas/MeterDataCredential/README.md:3` | IES Cell — MeterDataCredential docs | Intentional overview-detail layering | Family page is the detail source; overview repeats only the scope tagline. | Accept; family page remains canonical. |
| **DUP-002.7** | `schemas/MeterDataRequest/README.md:3` and `what-ies-provides/schemas-overview/meter-data-request.md:3` | 4 | `schemas/MeterDataRequest/README.md:3` | IES Cell — MeterDataRequest docs | Intentional overview-detail layering | Family page is the detail source; overview repeats only the scope tagline. | Accept; family page remains canonical. |
| **DUP-002.8** | `use-cases-overview/discom-regulatory-filing.md:5-7` and `use-cases-overview/tariff-intelligence.md:5-7` | 1 | `use-cases-overview/README.md:13-14` | IES documentation owner — use-case overviews | Generated/versioned/template reuse | Canonical status register marks both WIP; hand-authored reuse boundary is only the WIP notice, with page substance independent. | Accept while both statuses match the register; owner updates notice and register together. |
| **DUP-002.9** | Two qualifying block pairs: `use-cases/consumer-energy-passport/README.md:59` ↔ `use-cases/consumer-meter-digest/README.md:56`, and Passport `:61` ↔ Digest `:58` | 5 | `use-cases/consumer-energy-passport/README.md:59,61` | IES documentation owner — implementation guides | Generated/versioned/template reuse | The two adjacent substantive blocks form one checklist-template concept for the same file pair. The intervening `## Checklist` heading is excluded and not counted. Content from Step 1 onward diverges. | Accept within those two sentence blocks; named owner maintains the shared intro/Step 0 template. |
| **DUP-002.10** | `use-cases/discom-regulatory-filing/README.md:7-9` and `use-cases/tariff-intelligence/README.md:7-9` | 1 | `use-cases/README.md:20-27` | IES documentation owner — implementation guides | Generated/versioned/template reuse | Canonical WIP register lists both guides; hand-authored reuse boundary is only the WIP notice (distinct from overview wording). | Accept while both statuses match the register; owner updates notice and register together. |
| **DUP-002.11** | `use-cases-overview/consumer-meter-digest.md:58` and `use-cases-overview/smart-meter-data-exchange.md:71` | 4 | `schemas/README.md:89-92` | IES Cell — standards/schema documentation | Mutable normative prose | Both pages repeat the same standards-order guidance. The copies currently agree with the canonical four-item order, so this is not a present contradiction; it is still mutable normative prose rather than harmless template reuse. | Parallel copies can drift and obscure canonical ownership. Replace each copied rule with a short pointer to `schemas/README.md:89-92` in Batch 7; do not treat false universality at `:87` as canonical. |
| **DUP-002.12** | `schemas/MeterDataCredential/v0.6/README.md:32` and `schemas/MeterDataRequestCredential/v0.1/README.md:32` | 4 | `schemas/MeterDataCredential/v0.6/README.md:32` | IES Cell — credential schema docs | Generated/versioned/template reuse | Hand-authored envelope-intro exemplar; boundary is one sentence before family-specific tables, which then diverge. | Accept within the one-line boundary; owner maintains shared envelope terminology. |
| **DUP-002.13** | `what-ies-provides/schemas-overview/electricity-credential.md:114` and `what-ies-provides/schemas-overview/meter-data-request-credential.md:85` | 4 | `what-ies-provides/schemas-overview/electricity-credential.md:114` | IES documentation owner — schema overviews | Generated/versioned/template reuse | Hand-authored logical-blocks intro exemplar; boundary is one sentence, followed by different family tables. | Accept within the one-line boundary; owner maintains the shared intro. |
**Explicit non-qualifying tested pair:** `use-cases/discom-regulatory-filing/README.md:158` and `use-cases/tariff-intelligence/README.md:133` both contain the isolated five-word checklist label "8. Production deployment and go-live." It is not assigned a `DUP-002.x` ID because it is below the ≥8-word threshold and is a list-only/checklist label, both declared exclusions. The substantive bullet content beneath the labels differs.

**Cluster-level conclusion:** unlike the paraphrased-fact duplications in this register (DUP-001, DUP-004), one of the 13 qualifying exact-duplicate clusters requires remediation (DUP-002.11) because it is mutable normative prose. The remaining 12 qualify as accepted template/overview-detail reuse. No qualifying `DUP-002.x` sub-cluster is left untracked.

---

## 5. Logical inconsistency register

| ID | Primary axis | Proposition A | Proposition B | Verdict | Severity |
|---|---|---|---|---|---|
| **LIR-001** | 4 | `what-ies-provides/schemas-overview/meter-data-request.md:32-44` (worked example) and `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json:15-18` both request `"value": "kWh imp"` / `"kWh exp"` under `"profileType": "IntervalProfile"` | `schemas/MeterData/v0.6/IES codes.json:338-348` (`kWh imp`) and `:352-366` (`kWh exp`) each declare `"profiles": ["DAILY","MONTHLY","INSTANTANEOUS"]` — `INTERVAL` is absent from both; the *separate* register entries `kWh imp block` at `:453-467` and `kWh exp block` at `:468-479` each declare `"profiles": ["INTERVAL"]` exclusively; `schemas/MeterDataRequest/v0.6/validation/README.md:7-11` states the rule ("`kWh imp` must not be requested under `IntervalProfile`"); the validator's own regression fixtures make the same point structurally — `test_cases/invalid_request_profile_mismatch.json:7-10` pairs `kWh imp` with `IntervalProfile` as the **invalid** case, `test_cases/valid_request.json:7-10` pairs `kWh imp block` with `IntervalProfile` as the **valid** case. This fixture proves only the `kWh imp block` side of the corrected pairing directly — no fixture in the validation suite exercises `kWh exp block` — but the registry's own `:468-479` entry establishes the same `["INTERVAL"]`-only permission for `kWh exp block` by the identical structural rule. | **CONTRADICTION** — the shipped example and the overview's worked example use the exact pairing the schema family's own registry, validator, and regression-test suite jointly and consistently reject; the corrected pairing that *would* pass (per the schema's own valid fixture, and per the registry's parallel `kWh exp block` entry) is `kWh imp block`/`kWh exp block`, not a `profileType` change. Per `qaqc/02` P1.1 (carried fact), the dedicated validator exits 1 on this file. | **P1** — see ISS-001 |
| **LIR-002** | 4 | `what-ies-provides/schemas-overview/meter-data.md:147` says `premisesType` is locally defined only in v1.1 source attributes | v1.0 `consumptionProfiles.items` directly references external `ConsumptionProfileCredential/v2.0` (`attributes.yaml:133-144`); v1.2 items locally reference `#/components/schemas/ConsumptionProfile`, whose definition references external `MeterServiceProfile/v1.1` (`:115-135`). Neither source defines `premisesType` locally; v1.1 does at `:202-210`. Bundled `schema.json` artifacts contain the inlined field, and the table generator reads only bundled schemas/local refs. | **NOT a contradiction — precise source-vs-bundled representation distinction.** | **P3** — see ISS-005 |
| **LIR-003** | 4 | `what-ies-provides/schemas-overview/meter-data-credential.md` §6 and §11 item 2 assert the MeterDataCredential family's top-level `README.md` "describes the v0.6 revocation mechanism as 'BitstringStatusListEntry' revocation" | `schemas/MeterDataCredential/README.md` (the actual family top-level README) contains no occurrence of "BitstringStatusListEntry" anywhere; its Versions table and "How things are identified" section both state **"DeDi-registry revocation (`credentialStatus.type: dediregistry`)"**, consistent with the compiled schema and all three examples | **CONTRADICTION, but not the one claimed** — the cross-document contradiction the overview page describes does not exist in the current corpus; the overview page's own claim about a sibling document's wording is itself inaccurate. | **P3** — see ISS-006 |
| **LIR-004** | 4 | `schemas/MeterData/v0.6/attributes.yaml:4-6` — `version: 0.5.0`, description: *"the six compact profile shapes (CUSTOMER, INTERVAL, DAILY, BILLING, INSTANTANEOUS, EVENT)"* | `schemas/MeterData/v0.6/README.md`'s own compiled field-reference table (and `schemas/MeterData/README.md`'s "Nine record shapes") show nine shapes with `MONTHLY`/`BILL_DETAILS`/`ALARM`/`DESCRIPTOR` added and `BILLING` renamed | **CONTRADICTION, internally adjudicable** — already self-disclosed as an open point in `schemas/MeterData/README.md` and `schemas-overview/meter-data.md` §11.1. Correction target is the source (`attributes.yaml`'s `info` block), not the README. | **P2** (`OD-S1`) — see ISS-003 |
| **LIR-005** | 5 | `download-pdf.md:17`: *"There's no separate 'publish' step — whatever is live on this GitBook is what the PDF reflects"* | `qaqc/01`/`qaqc/02` P1.3 (carried fact): `build_pdf.py`'s missing-source count is computed but discarded (`main()` ignores the return and unconditionally exits 0), so a missing `SUMMARY.md` source can be silently omitted from the PDF while the workflow stays green | **CONTRADICTION** — the audience-facing completeness claim is not backed by the pipeline's actual behavior. | **P3** — see ISS-015 |
| **LIR-006** | 3 | `pathways/utility.md:55` labels a link to `register.md` "Resolution & Routing Specification," and `pathways/utility.md:67` labels a link to `register.md#identifier-vs.-record` "Appendix D" | `what-ies-provides/register.md` has no heading named "Resolution & Routing Specification" and uses no appendix-lettering scheme anywhere in the document | **Copy-paste residue** — the labels imply a document structure (named specs, lettered appendices) that `register.md` does not have. The anchor itself resolves correctly; only the label is wrong. | **P3** — see ISS-007 |
| **LIR-007** | 5 | Three schema-family pages link to `./examples` as a directory: `schemas/OutageNotification/v0.1/README.md:69`, `schemas/MeterData/v0.6/README.md:29`, `schemas/ArrFiling/v0.5/README.md:25` | GitBook renders these as links to a GitHub URL ending `/examples/README.md`, which returns HTTP 404 (carried fact, `qaqc/01`/`qaqc/02`, unchanged per `qaqc/04`) | **CONTRADICTION between the published link and its target** — carried, not re-run. | **P2** — see ISS-014 |
| **LIR-008** | 4 | Current-schema framing at `use-cases-overview/consumer-meter-digest.md:3,12,20` and `use-cases/consumer-meter-digest/README.md:15-25`; dependent field/value claims at overview `:28,32,52,79,85,103,127` and guide `:25,33,35,62-63,87`; implementation claims at guide `:50,69-70,74,76` | Actual compiled fields are `profileType`, `meterRefs`, `intervalPeriod`/`timePeriod`, `intervals`/`readings`, and `validationStatus`; none of the six exact disputed tokens (`SUMMARY_TOTAL`, `SUMMARY_PEAK`, `SUMMARY_TOD`, `meterReference`, `dataQuality`, `RAW_15M`) appears under `schemas/`. The generic `summary`/`period` dependents at overview `:52,103,127` and guide `:33` still presuppose the same non-schema model. Fifteen-minute data requires both `profileType: INTERVAL` and `intervalPeriod.duration: PT15M` (`use-cases/smart-meter-data-exchange/ies-meter-data-model.md:41-45`; `schemas/MeterData/v0.6/examples/MultiMeterBulkDataset_Elaborated.json:277-285`). The canonical OpenCred ID is `ies/meter-data-credential/v0.6` (`issue-credentials.md:292,299`), and repository guidance names plural `offerAttributes.policy.requiredCredentials`; singular `requiredCredential`, `granularityOptions`, and `maxRange` occur only in this guide. Line 76 is cross-dispositioned under ISS-018. Permissive `additionalProperties` may admit extra keys, but required actual fields still govern validity. | **CONTRADICTION — current-schema and exchange guidance uses a non-canonical payload and implementation contract.** | **P1** — see ISS-019 |

---

## 6. Cross-audience journey findings

Reader journeys were walked README → What IES Provides → How you implement → use cases → schemas, plus the five role pathways, checking that each hop's claims survive into the next page without drift.

- **README → What IES Provides → Schemas (product journey).** ALIGNED. The three-step Register/Discover/Exchange framing in `README.md` is restated identically in `what-ies-provides/README.md`, and every downstream page (`register.md`, `discover.md`, `exchange.md`) closes with a "Where this fits" table pointing back to the same three-step sequence. No drift found across this journey.
- **What IES Provides → Schemas Overview → Schemas (schema journey).** ALIGNED, with one narrow exception confined to a single document (DUP-001/ISS-002). A reader who starts at `what-ies-provides/exchange.md`, follows to `schemas-overview/meter-data.md` (which correctly says "nine"), then continues to `schemas/MeterData/v0.6/README.md`, receives a page that is itself internally consistent: its opening prose ("eight compact profile shapes representing different read cadences," `:7`) is correctly cadence-scoped, and its own field table 470+ lines later shows nine total shapes including `DESCRIPTOR` — no contradiction between the two. The one location on this journey that would mislead a reader is `schemas/MeterData/v0.6/ReferenceGuide.md:9`, a separate document reachable from the same family, which states "eight distinct profile shapes" with no cadence qualifier and never mentions `DESCRIPTOR`.
- **What IES Provides → Schemas Overview → MeterDataRequest (request journey).** DRIFT (ISS-001). A reader following `what-ies-provides/schemas-overview/meter-data-request.md` sees a worked example and a "DailyProfile-only" characterization that both disagree with the schema's own registry, validator, and test fixtures — reachable only by opening `schemas/MeterDataRequest/v0.6/validation/README.md` and `IES codes.json` directly, which the overview page's own stated purpose ("the *why* before the *what*," `schemas-overview/README.md:5`) discourages a reader from doing.
- **Use-case overview → Use-case implementation guide (7 pairs).** ALIGNED for six of seven pairs. The Consumer Meter Digest pair (ISS-019) is the exception: both pages describe a field shape not defined by the schema they link to, and the implementation guide adds three contract-level defects of its own — non-canonical OpenCred `schemaId`, singular `requiredCredential` instead of `offerAttributes.policy.requiredCredentials`, and undefined `granularityOptions`/`maxRange` keys. A reader who relies on the promised overview/guide layer without independently inspecting schemas and issuance guidance will not discover those mismatches.
- **How you implement IES → Schema validation → Conformance (execution journey).** FALSE CONFORMANCE CLAIM, not a gap (ISS-018) — with two compounding defects. First, `how-you-implement-ies/build-adapter.md:100-110,120,157`, the Consumer Meter Digest checklist (`use-cases/consumer-meter-digest/README.md:76`), and `conformance.md:33,72,76-83` promise schema validation and self-contained conformance even though `validate_schema.py:9-43` registers permissive substitutes for external schemas consumed by MeterDataCredential, MeterDataRequestCredential, MeterData, and OutageNotification. `conformance.md:95` carries that unsupported conclusion into production readiness. Second, `conformance.md:79` says `credentialSubject`, while its command passes a credential-root schema; for MeterDataCredential, the subject is optional at the root and its meaningful constraint is nested beneath it, so an arbitrary object can pass. Self-contained schemas such as ElectricityCredential do not share this gap.
- **Pathways (5 role journeys).** Internally ALIGNED (each pathway's cross-references to `register.md`/`schemas/README.md`/use-case pages resolve to the content they claim, aside from ISS-007/ISS-009/ISS-010), but **unreachable as a class and unreferenced from anywhere else in the corpus** — none of the 6 pathway pages is linked from `SUMMARY.md`, `_sidebar.md`, or `index.md`, and no other one of the other 73 corpus files links into `pathways/` either (ISS-011). A reader following only the published navigation surfaces, or reading every other page in the corpus, will never discover Pathways exists.
- **README "Pilots and status" → downstream status restatements.** UNSUPPORTED, not a proven contradiction (ISS-008, source-of-truth topic 7) — three tense choices describing a status that is jointly readable as one coherent (if externally unverifiable) timeline, requiring an owner-approved single posture regardless.

---

## 7. Issue table

| ID | Primary axis | `file:line` | Evidence | Severity | Confidence | Recommendation | Owner decision |
|---|---|---|---|---|---|---|---|
| **ISS-001** | 4 | `what-ies-provides/schemas-overview/meter-data-request.md:32-44` (worked example) and `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json:15-18`; separate ancillary `what-ies-provides/schemas-overview/meter-data-request.md:126` ("DailyProfile-only" claim) | **FACT:** the worked example and shipped `Anonymised_Telemetry_Request.json` payload both request `kWh imp`/`kWh exp` under `"profileType": "IntervalProfile"`. **FACT:** `IES codes.json:338-348` (`kWh imp`) and `:352-366` (`kWh exp`) restrict both to `["DAILY","MONTHLY","INSTANTANEOUS"]`; the separate `kWh imp block` entry at `:453-467` and `kWh exp block` entry at `:468-479` are the ones that permit `INTERVAL`. **FACT:** `validation/README.md:7-11` states the rule using this exact register as its own worked counter-example. **FACT:** the validator's own regression fixtures agree structurally — `invalid_request_profile_mismatch.json:7-10` (invalid: `kWh imp` + `IntervalProfile`) vs. `valid_request.json:7-10` (valid: `kWh imp block` + `IntervalProfile`); this fixture directly proves only the `kWh imp block` side of the corrected pairing — the `kWh exp block` side rests on the registry's parallel `:468-479` entry rather than a dedicated fixture, though the entry's structure is identical. **FACT:** at line 126, the overview separately calls `kWh imp` "a `DailyProfile`-only register per the code table," which is also false — the registry permits `DAILY`, `MONTHLY`, **and** `INSTANTANEOUS`. **INTERPRETATION (High confidence — basis: the worked example and the false line-126 claim are independently documented and both materially false against registry/fixture facts):** a reader following only the docs is led to believe this register/profile pairing is valid and that `kWh imp` is exclusively daily-cadence. | **P1** — carried amplification, not a new root cause (`qaqc/01` SPARK-MDR-001 / `qaqc/02` P1.1) | High | Two separately-scoped corrections, each internally resolvable (see Batch 2a): (1) docs-only correction to the worked example, (2) docs-only correction to the false line-126 claim. A separate artifact-only batch (2b) updates the shipped example payload. Both converge on `kWh imp block`/`kWh exp block` for `IntervalProfile` and `DAILY`/`MONTHLY`/`INSTANTANEOUS` for plain `kWh imp`. | **None.** Registry, fixtures, and `IES codes.json` are mutually consistent; the correction target is internally determinable from existing artifacts, not an owner-governance decision. |
| **ISS-002** | 4 | `schemas/MeterData/v0.6/ReferenceGuide.md:9` (sole confirmed defect); seven other locations reinspected and found correct: `schemas/MeterData/v0.6/README.md:7`; `schemas/README.md:36`; `use-cases-overview/smart-meter-data-exchange.md:37,93,126`; `use-cases/smart-meter-data-exchange/README.md:26`; `use-cases/smart-meter-data-exchange/ies-meter-data-model.md:17-20` | FACT: all eight originally-flagged locations were reread in full surrounding context this pass. FACT: `ReferenceGuide.md:9` states "eight distinct profile shapes" with no cadence/telemetry qualifier and never mentions `DESCRIPTOR`/`PayloadDescriptorProfile` anywhere in the document. FACT: the other seven all state "eight" with an explicit cadence/telemetry scope ("representing different read cadences," "cover every cadence," "covering every smart-meter cadence," or an explicit named list of exactly the eight non-descriptor profiles), or — at `ies-meter-data-model.md:17-20` — explicitly list `PayloadDescriptorProfile`/`DESCRIPTOR` as a separate object kind before introducing "the eight profile shapes." FACT: `schemas/MeterData/README.md` states "Nine record shapes," matched by the compiled field-reference table. FACT: `MeterDataRequest/v0.6/attributes.yaml:134-144` and `schema.json:167-176` confirm `DESCRIPTOR` genuinely is excluded from what a requester can ask for. FACT: `what-ies-provides/schemas-overview/README.md:10` already states the correct distinction ("eight telemetry profile shapes (plus a shared descriptor object)"). | **P2** | High | Correct only `schemas/MeterData/v0.6/ReferenceGuide.md:9` — reword to name the cadence/telemetry scope and add a brief mention of `DESCRIPTOR`. Do not change the other seven locations; they are already correctly scoped and a blanket "eight → nine" edit across all eight would introduce incorrect total-count claims into seven locations that do not make one. Do not describe `DESCRIPTOR` as requestable anywhere. | None needed — internally determinable (`OD-S3` pattern: the corpus itself, via `schemas/MeterData/README.md` and `schemas-overview/README.md:10`, already declares the correct distinction). |
| **ISS-003** | 4 | `schemas/MeterData/v0.6/attributes.yaml:4-6` | FACT: `version: 0.5.0`, description names six shapes using the retired `BILLING` label. Already self-disclosed in `schemas/MeterData/README.md` "Open points" and `schemas-overview/meter-data.md` §11.1. | **P2** | High | Correct the `info.version` and `info.description` fields in `attributes.yaml` to match the compiled v0.6/nine-shape reality. | **`OD-S1`** (closed list, internally resolvable) — correction target is `attributes.yaml`. |
| **ISS-004** | 4 | `schemas/ArrFiling/v0.5/attributes.yaml:4` | FACT: `version: 1.0.0` inside the `v0.5` directory; no audience page discloses this mismatch (unlike MeterData's self-disclosed case). | **P2** | High (fact) / owner call on remedy | Decide and document the versioning convention (does `info.version` track the OpenAPI-document's own revision, or the schema family's public version?) before treating this as a defect vs. an intentional convention. | **`OD-E5`** (escalate) |
| **ISS-005** | 4 | `what-ies-provides/schemas-overview/meter-data.md:147` | FACT: `premisesType` is not locally defined in v1.0/v1.2 source attributes; v1.0 reaches external `ConsumptionProfileCredential` directly, while v1.2 uses local `ConsumptionProfile` as an indirection to external `MeterServiceProfile`. v1.1 defines the enum locally. Bundled v1.0/v1.2 schemas already inline the field, and field tables faithfully render those bundled artifacts; local table tooling does not fetch external refs. | **P3** | High | Reword only to distinguish source-local definitions from bundled inlined content; retain MeterData's deliberate `consumerCategory` choice. | None — internally determinable clarity fix (`NO CONTRADICTION`). |
| **ISS-006** | 4 | `what-ies-provides/schemas-overview/meter-data-credential.md` §6, §11 item 2 | FACT: claims the family `README.md` describes "BitstringStatusListEntry" revocation. FACT: `schemas/MeterDataCredential/README.md` contains no such text and instead states DeDi-registry revocation consistently with the schema and examples. | **P3** | High | Remove or correct the claimed inconsistency — as currently written it asserts a contradiction that does not exist in the corpus. | None needed. |
| **ISS-007** | 3 | `pathways/utility.md:55,67` | FACT: labels plain `register.md` subsections "Resolution & Routing Specification" and "Appendix D." FACT: `register.md` has no such named specification and no appendix-lettering scheme anywhere. | **P3** | High | Replace both labels with the actual section names ("Identifiers & Addressing," "Identifier patterns → Identifier vs. record"). | None needed. |
| **ISS-008** | 1 | `README.md:105`; `faq.md:45`; `how-you-implement-ies/README.md:120` | **FACT (quoted):** `README.md:105` — "IES is already running in a test environment... the sandbox is working. Four pilot DISCOMs... **undertook** a 30-day challenge" (present tense for sandbox state; simple past, not past-perfect, for the challenge). `faq.md:45` — "It **is live**. The sandbox **is running**, and four pilot DISCOMs **are building** in it now" (present/ongoing). `how-you-implement-ies/README.md:120` — "The four pilot DISCOMs each **went** from cold start to four demonstrated use cases in 30 days" (simple past, describing the challenge, not the sandbox's present state). **INTERPRETATION (Medium confidence that a reader could find the combination momentarily unclear; Low confidence that the three are logically incompatible — a completed challenge and an ongoing live sandbox are compatible readings of one timeline). OWNER DECISION:** the single defensible public status posture is externally unverifiable from the repository, so classified `UNSUPPORTED` per work order §11 rather than adjudicated as fact or contradiction. | **P2** — not a fourth semantic P1; `OD-E1` is nonetheless a **P1-closure policy gate** per work order §12 (a gate on closing the other P1s, not itself a P1 finding) | Medium (that a reader could be confused) / N/A (which posture is true) | Adopt one defensible public status posture and apply it uniformly across all three pages; until decided, treat live/pilot claims as `UNSUPPORTED` rather than fact. | **`OD-E1`** (escalate, blocks P1 closure per work order §12) |
| **ISS-009** | 3 | `pathways/researcher.md:33` | FACT: references a companion "What IES Is Not" **page**. FACT: only a same-named section exists inside `README.md` (`README.md:34`, "## What IES is not"); no separate file exists in the 79-file corpus or elsewhere in the tree. | **P2** | High | Reword to "section" and link `README.md#what-ies-is-not` directly. | **`OD-S4`** (closed list, internally resolvable) |
| **ISS-010** | 3 | `pathways/researcher.md:51` | FACT: references "the concepts pages." FACT: no `concepts/` directory or file is tracked anywhere in the repository. | **P2** | High | Replace with a concrete referent — most likely "the sandbox referenced in [Pilots and Status](../README.md#pilots-and-status)" per the surrounding sentence's own context. | **`OD-S4`** |
| **ISS-011** | 6 | `SUMMARY.md`; `_sidebar.md`; `index.md` (all three, whole-file); all 73 non-`pathways/` corpus files (whole-corpus search) | FACT: none of the three navigation files lists any of the 6 `pathways/**` files. FACT: an exhaustive case-insensitive search for the string "pathways" across all 79 corpus files finds hits only inside `pathways/README.md` itself — no other file, including `README.md`, links to or names Pathways. | **P2** | High | Decide whether Pathways is intentionally unlisted (staged rollout) or a navigation defect; if staged, say so discoverably (e.g. a pointer from `README.md`). | **`OD-E6`** (escalate) |
| **ISS-012** | 5 | `scripts/generate_index.py:111-118` (`usecases_overview` list); `SUMMARY.md:61`; `index.md` (rendered Use Case Overviews section) | FACT: `generate_index.py`'s hardcoded `usecases_overview` list has 7 entries, omitting `use-cases-overview/p2p-energy-trading.md`. FACT: `SUMMARY.md:61` and `_sidebar.md` both include it. Carried mechanical fact (`qaqc/04`), independently re-confirmed here by reading `generate_index.py` in full and diffing its hardcoded list against `SUMMARY.md`. | **P2** | High | Add the missing entry to `generate_index.py`'s list. | None needed beyond the carried fact — this is a script-side fix, out of this report's edit scope. |
| **ISS-013** | 5 | `scripts/generate_index.py` (slugger used to build `index.md`'s internal anchor links) vs. `scripts/validate_links.py:24-56` (GitBook-verified slugger) | FACT: `validate_links.py`'s `slugify()` is documented as verified against the live GitBook deployment and correctly keeps periods literally and prepends `id-` to digit-led headings. FACT: `qaqc/04`'s carried count (740 outline links, 262 slug mismatches) shows `index.md`'s *own* self-generated links use a different, unverified slugger. | **P2** | High | Point `generate_index.py` at the same slug logic already implemented and GitBook-verified in `validate_links.py`. | **`OD-S2`** (closed list; semantic-harm judgment: real harm specifically to `index.md`'s own self-generated links) |
| **ISS-014** | 5 | `schemas/OutageNotification/v0.1/README.md:69`, `schemas/MeterData/v0.6/README.md:29`, `schemas/ArrFiling/v0.5/README.md:25` | Carried fact (`qaqc/01`/`qaqc/02` P2.1, unchanged per `qaqc/04`): each links `./examples` as a directory, which GitBook resolves to a 404ing GitHub URL. | **P2** | High (carried, not re-run) | Link to a specific file inside `examples/` or to the GitHub tree view explicitly. | None needed beyond the carried fact. |
| **ISS-015** | 5 | `download-pdf.md:17` | FACT: claims "whatever is live on this GitBook is what the PDF reflects." FACT (carried, `qaqc/01` P1.3): `build_pdf.py` computes but discards its missing-source count, so omissions can occur silently. | **P3** | High | Soften the claim (e.g. "built from the same source... on every merge") or note the known completeness gap. | None needed. |
| **ISS-016** | 4 | `schemas/MeterData/v0.5/examples/BillingProfile.json`, `CustomerBillingSummary.json` | Carried fact (`qaqc/04`): byte-identical, SHA-256-confirmed, 89 lines; only `BillingProfile.json` is referenced from `schemas/MeterData/v0.5/README.md:151`. | **P3** | High (carried) | Remove or repurpose the unreferenced duplicate, or document the duplication as intentional. | **`OD-E8`** (escalate) |
| **ISS-017** | 6 | `schemas/ElectricityCredential/README.md:5`; `Makefile:22` | FACT: family page states "Upstream is authoritative; open an issue if you find a discrepancy" (an honest mirror framing). FACT: `Makefile:22` excludes ElectricityCredential from the local build/regeneration pipeline, and no sync/drift verifier exists in the corpus. | **P3** | High (fact) / N/A (which ownership model is right) | No page makes a false claim — but no page can currently *prove* upstream parity either. Decide the ownership model. | **`OD-E3`** (escalate) |
| **ISS-018** | 5 | Validation/conformance promises: `how-you-implement-ies/build-adapter.md:100-110,120,157`; `how-you-implement-ies/conformance.md:33,72,76,79,83,95`; `use-cases/consumer-meter-digest/README.md:76`. Validator/consumer evidence: `scripts/validate_schema.py:9-43`; `schemas/MeterDataCredential/v0.6/schema.json:6-45`; `schemas/MeterDataRequestCredential/v0.1/schema.json:10`; `schemas/MeterData/v0.6/schema.json:1162,1165`; `schemas/OutageNotification/v0.1/schema.json:308,363` | **Defect 1 — named validation, conformance, and production-readiness claims rest on stubs.** `validate_schema.py:9-38` defines permissive substitute objects and `:39-43` registers them for `EnergyCredential`, `EnergyResource`, `Address`, and `GeoJSONGeometry`. Actual consumers are MeterDataCredential/MeterDataRequestCredential (`EnergyCredential`), MeterData (`Address`/`GeoJSONGeometry`), and OutageNotification (`GeoJSONGeometry`); none consumes `EnergyResource`, and ElectricityCredential is self-contained. The cited pages omit this boundary; `conformance.md:76-83` says the checks establish B2C conformance and `:95` promotes them to production readiness. **Defect 2 — `conformance.md:79` names the wrong input boundary.** Its prose says `credentialSubject`, while its command passes a credential-root schema. MeterDataCredential has no root `required` array; its real constraint is reachable only if `credentialSubject` exists, so an arbitrary object can pass the stub-backed step. **INTERPRETATION (High confidence):** explicit conformance overclaiming. | **P1** (semantic amplification of carried `qaqc/02` P2.3) | High | Batch 8a corrects `:79`; owner-gated Batch 8b applies the chosen posture to every cited promise, including adapter steps `:120,157` and downstream production claim `conformance.md:95`. | **`OD-E2`** (required for Batch 8b/P1 closure, not 8a) |
| **ISS-019** | 4 | Current-schema framing: `use-cases-overview/consumer-meter-digest.md:3,12,20` and `use-cases/consumer-meter-digest/README.md:15-25`. All dependent payload/value anchors: overview `:28,32,52,79,85,103,127`; guide `:25,33,35,62-63,87`. Implementation anchors: guide `:50,69-70,74,76`; comparisons at `how-you-implement-ies/issue-credentials.md:292,299`, `schemas/MeterDataRequestCredential/README.md:22`, and `schemas/MeterDataRequestCredential/v0.1/README.md:100` | **FACT — payload model:** both pages describe current MeterDataCredential/MeterData v0.6 using `meterReference`, `period`, `summary` with `SUMMARY_*`, `dataQuality`, and `RAW_15M`; the exact disputed tokens do not occur under `schemas/`. Overview `:52,103,127` and guide `:33` are dependent generic restatements of the same `summary`/`period` model. Actual fields are `profileType`, `meterRefs`, `intervalPeriod`/`timePeriod`, `intervals`/`readings`, and `validationStatus`. Fifteen-minute data requires `profileType: INTERVAL` plus `intervalPeriod.duration: PT15M`; a bare label substitution loses cadence. **FACT — implementation contract:** guide `:50,74` uses non-canonical OpenCred ID `MeterDataCredential/v0.6`; `:69` uses singular `requiredCredential`; `:70` presents undefined `granularityOptions`/`maxRange` contract keys. Canonical sources give `ies/meter-data-credential/v0.6` and `offerAttributes.policy.requiredCredentials`. Guide `:76` is cross-dispositioned under ISS-018. **FACT, qualified validation:** permissive extra-key handling does not remove actual required-field obligations. **INTERPRETATION (High confidence):** this is a paired non-canonical payload plus guide-only contract drift, not an isolated typo. | **P1** (genuinely new) | High | Correct every cited dependent occurrence: use actual schema fields; express 15-minute data as `INTERVAL` + `PT15M`; remove schema-undefined summary/period claims or explicitly frame derived analytics as outside the credential schema; use canonical OpenCred ID and plural policy path; express granularity/range as prose, not undefined keys. Coordinate guide `:76` only through ISS-018 Batch 8b. | **None.** Internally resolvable from current artifacts and canonical guidance. |

---

## 8. Release gates

### 8.1 Disposition of every Section 7.1 carried mechanical fact

Per work order §7.1, none of the following was rerun; each is treated as settled fact and is dispositioned here purely for semantic impact on the audience corpus.

| Carried `qaqc/01`/`qaqc/04` fact | Disposition | Basis |
|---|---|---|
| Three live directory-link 404s + one latent (`./examples` links) | **SEMANTIC IMPACT CONFIRMED** | ISS-014 — the affected pages are in the audience corpus and the links are read by real visitors following the published journey. |
| `validate_links.py` false-green (misses directory-publishability class) | **NO SEMANTIC IMPACT** beyond ISS-014 above | No audience page makes a claim about link-checking coverage itself; the tool gap is orthogonal to prose content. |
| MDR semantic-validator failure alongside generic-validator pass | **SEMANTIC IMPACT CONFIRMED** | This *is* ISS-001/LIR-001 — the audience page presents the failing example without caveat, and separately makes a related false claim (line 126). |
| 12-artifact reproducibility drift across 5 directories | **NO SEMANTIC IMPACT on audience prose directly** | No page in the 79-file corpus claims "regeneration is reproducible" or "clean diff" as an audience-facing promise. Relevant context for `OD-E3`/`OD-E8` but no standalone audience-facing claim to correct. |
| PDF missing-source false-green; CP-1252 encoding failure | **SEMANTIC IMPACT CONFIRMED** (missing-source half) / **NO SEMANTIC IMPACT** (CP-1252 half) | ISS-015 covers the completeness claim in `download-pdf.md`. The CP-1252 encoding failure is a Windows-only local-build issue; `download-pdf.md:23-26` already documents macOS/Linux `brew`-based build commands only, so no audience claim asserts Windows local-build support to contradict. |
| Windows cross-schema resolver failure | **NO SEMANTIC IMPACT found in this pass** | No audience page asserts Windows support for `validate_schema.py` specifically; `how-you-implement-ies/setup-register.md:113` already caveats a *different* script's Windows limitation candidly. Deferred to `OD-E7` (Unresolved Questions). |
| CI limited to `build-pdf.yml` | **NO SEMANTIC IMPACT** | No audience page claims broader CI coverage exists; this is a real gap but not a contradicted claim. |
| Metadata parity conflicts (MeterData v0.6, ArrFiling v0.5) | **SEMANTIC IMPACT CONFIRMED** | ISS-003 (`OD-S1`, internally resolvable) and ISS-004 (`OD-E5`, owner decision). |
| Migration-tool false-green/stale (`verify_v05_v06_equivalence.py`, `compare_v05_v06.py`, `scratch/verify_no_loss.py`) | **NO SEMANTIC IMPACT** | No audience page cites these tools' output as evidence of migration correctness. |
| JSON-LD unwired (`check_jsonld.py` not in Make/CI, `pyld` undeclared) | **NO SEMANTIC IMPACT** | No audience page asserts JSON-LD content is CI-verified; `context.jsonld` is described only as "present," which is true. |
| Permissive external stubs (`EnergyCredential`, `EnergyResource`, `Address`, `GeoJSONGeometry`) | **SEMANTIC IMPACT CONFIRMED, upgraded** | ISS-018 — this pass found the impact is a *named* conformance claim, not a diffuse gap, warranting the P1 upgrade over the carried P2.3 rating. |
| ElectricityCredential excluded from `Makefile` build (lines 20-22) | **SEMANTIC IMPACT CONFIRMED** | ISS-017 (`OD-E3`, owner decision) — the family pages' "verbatim mirror, upstream authoritative" framing is honest but currently unverifiable either way. |
| Byte-identical MeterData v0.5 example pair | **SEMANTIC IMPACT CONFIRMED (low severity)** | ISS-016/DUP-003 (`OD-E8`, owner decision). |

### 8.2 Overall gate verdict

Restating and extending `qaqc/01`/`qaqc/02`'s verdict (unchanged per `qaqc/04`) with this pass's additions. **Overall: not release-green.**

| Gate | Status | Basis |
|---|---|---|
| Schema reproducibility, MDR structural contradiction, PDF completeness, Windows resolver, CI breadth, ElectricityCredential ownership, exact duplicate examples | **FAIL / unchanged** | Carried verbatim from `qaqc/01`/`qaqc/02`/`qaqc/04`; this audit reruns none of it and found no evidence to reopen or soften any of these verdicts. |
| Docs describe only shipped, validator-consistent schema behavior | **FAIL (new, this pass)** | ISS-001 (carried amplification, spanning overview prose and a shipped example artifact — not confined to either layer) and ISS-019 (genuinely new, confined to prose) — both P1. |
| Conformance language matches what validation tooling actually establishes | **FAIL (upgraded to P1, this pass)** | ISS-018 — two compounding defects: a named, explicit conformance claim resting on stub validation scoped to specific consumer files (not universal), plus a `:79` instruction/command mismatch that is concretely exploitable for stub-backed wrappers. |
| Public status posture is single-valued and owner-approved | **FAIL (carried, reframed)** | ISS-008 / `OD-E1` — scored P2, not a fourth P1; not because the three texts contradict, but because the underlying claim is externally `UNSUPPORTED` and the work order gates P1 closure on an owner-approved posture regardless. |
| Primary navigation surfaces (`SUMMARY.md`, `_sidebar.md`, `index.md`) list every published section | **FAIL (new detail on a carried gap)** | ISS-011 (Pathways entirely unlisted on all three surfaces, and unreferenced from every other corpus file) and ISS-012 (P2P overview unlisted on `index.md` only). |
| Schema/version metadata internally consistent with compiled artifacts | **FAIL (carried, narrowed after reinspection)** | ISS-002 (one confirmed instance, `ReferenceGuide.md:9`, after seven of eight originally-flagged locations were found correctly scoped), ISS-003, ISS-004, DUP-004. ISS-005 is **not** included here — reclassified `NO CONTRADICTION` (a wording-clarity issue, not a metadata inconsistency). |

No gate that was passing in `qaqc/01`/`qaqc/02`/`qaqc/04` is downgraded by this pass, and no `RETRACTED` item (the naive `id-*` anchor set, the 1,533 duplicate-key warnings, the contaminated aggregate link totals) is revived anywhere above.

---

## 9. Bounded remediation batches

**Docs-only** is defined by file type, not directory: a batch is docs-only only if every file it touches is hand-authored Markdown (`.md`), regardless of which directory that file lives in — including `.md` files inside `schemas/`. Any edit to a JSON or YAML file, a generated/compiled artifact, or a shipped example (`.json`, `.yaml`, `schema.json`, `attributes.yaml`, `context.jsonld`, `vocab.jsonld`, anything under an `examples/` directory) is an **artifact/source-edit** batch, never docs-only, regardless of how minor the change — this applies even when a docs-only and an artifact correction address the same underlying defect (see Batch 2a/2b). Artifact/source-edit batches additionally require the schema-change proposal flow and separate authorization per `qaqc/05` §13.2's boundary against mixing documentation-semantic corrections with the unchanged technical release blockers. No batch below claims every batch in this section is docs-only — Batch 2b and Batch 6 explicitly are not.

**Batch 1 — MeterData profile-count correction (docs-only)**
- Scope: correct exactly one location, `schemas/MeterData/v0.6/ReferenceGuide.md:9`, from "eight distinct profile shapes" (no cadence qualifier, no mention of `DESCRIPTOR`) to a cadence-scoped statement that also names `DESCRIPTOR`/`PayloadDescriptorProfile`. The other seven originally-flagged locations (`schemas/MeterData/v0.6/README.md:7`; `schemas/README.md:36`; `use-cases-overview/smart-meter-data-exchange.md:37,93,126`; `use-cases/smart-meter-data-exchange/README.md:26`; `use-cases/smart-meter-data-exchange/ies-meter-data-model.md:17-20`) are **out of scope for this batch** — reinspection this pass found each already correctly cadence-scoped or, at `ies-meter-data-model.md:17-20`, already correctly separating `DESCRIPTOR` from the eight-profile list.
- Acceptance test: `schemas/MeterData/v0.6/ReferenceGuide.md` states the cadence/telemetry scope explicitly and names `DESCRIPTOR`/`PayloadDescriptorProfile` alongside the other eight profile names, without describing `DESCRIPTOR` as requestable; no other file in the corpus changes under this batch.
- Owner precondition: none — internally determinable from the corpus's own compiled field-reference table and `what-ies-provides/schemas-overview/README.md:10`'s existing correct wording.

**Batch 2a — MeterDataRequest overview and register-scope correction (docs-only)**
- Scope: (a) correct the worked example at `what-ies-provides/schemas-overview/meter-data-request.md:32-44` to use `kWh imp block`/`kWh exp block` in place of `kWh imp`/`kWh exp`; (b) correct the false "`DailyProfile`-only" claim at `meter-data-request.md:126` to state the actual permitted profile set (`DAILY`, `MONTHLY`, `INSTANTANEOUS`). This batch touches only hand-authored Markdown; it does not include the shipped JSON example, which is a separate artifact batch (2b) per the docs-only/artifact boundary defined above.
- Acceptance test: the worked example's register short codes match `IES codes.json`'s `kWh imp block`/`kWh exp block` entries (`:453-467`, `:468-479`); line 126's register-scope claim matches `IES codes.json`'s `kWh imp` entry (`DAILY`, `MONTHLY`, `INSTANTANEOUS`) exactly; no other wording in `meter-data-request.md` changes.
- Owner precondition: none — the correction target (change the register short code, not the `profileType`) is internally determinable from the validator's own valid fixture (`valid_request.json:7-10`, proving the `kWh imp block` side) and the registry's parallel `kWh exp block` entry, per ISS-001.

**Batch 2b — MeterDataRequest shipped-example correction (artifact/source-edit — requires separate authorization)**
- Scope: `schemas/MeterDataRequest/v0.6/examples/Anonymised_Telemetry_Request.json:15-18` — a shipped JSON example file, not hand-authored Markdown, so it is a distinct artifact batch from 2a even though both correct the same underlying register-code defect.
- Acceptance test (recorded now for when authorized; **not executed under this report's report-only boundary**): the payload's register short codes are `kWh imp block`/`kWh exp block` in place of `kWh imp`/`kWh exp`, and the file passes `schemas/MeterDataRequest/v0.6/validation/validator.py` with exit 0.
- Owner precondition: none on the correction target (same internally-determinable basis as Batch 2a), but execution requires the shipped-example change authorization separate from the docs-only remediation set, per the work order's boundary against mixing documentation-semantic corrections with artifact edits.

**Batch 3 — Consumer Meter Digest payload and implementation-contract correction (docs-only)**
- Scope: `use-cases-overview/consumer-meter-digest.md:28,32,52,79,85,103,127` and `use-cases/consumer-meter-digest/README.md:25,33,35,50,62-63,69-70,74,87`. Correct every primary and dependent occurrence of the non-schema payload model; express 15-minute data as `profileType: INTERVAL` plus `intervalPeriod.duration: PT15M`; reframe derived summaries as downstream analytics outside the current credential schema (or remove them); replace generic `period` with the applicable schema field; correct both OpenCred IDs; use `offerAttributes.policy.requiredCredentials`; and state granularity/range policy in prose rather than undefined keys. Line 76 remains exclusively in owner-gated Batch 8b; line 75 is valid and unchanged.
- Acceptance test: every cited primary and dependent occurrence is reconciled; no schema-body claim retains the six disputed tokens or generic `summary`/`period` as if they were current fields; any derived-analytics discussion is explicitly outside the credential schema; 15-minute representation preserves profile and cadence; both OpenCred IDs match `issue-credentials.md:292,299`; the policy key matches `schemas/MeterDataRequestCredential/v0.1/README.md:100`; and neither `granularityOptions` nor `maxRange` remains an undefined contract key.
- Owner precondition: **none.** Current documentation is corrected to current schema truth; this is fully internally resolvable.

**Batch 4 — Stale/mislabeled cross-references (docs-only)**
- Scope: `pathways/researcher.md:33,51` (ISS-009, ISS-010) and `pathways/utility.md:55,67` (ISS-007).
- Acceptance test: no reference to a "What IES Is Not" page, "concepts pages," "Resolution & Routing Specification," or "Appendix D" remains anywhere in `pathways/**`; replacement links resolve to real headings.
- Owner precondition: none.

**Batch 5 — MeterDataCredential revocation-claim correction (docs-only)**
- Scope: `what-ies-provides/schemas-overview/meter-data-credential.md` §6 and §11 item 2 (ISS-006).
- Acceptance test: the page no longer asserts that the family `README.md` describes "BitstringStatusListEntry" revocation; it either removes the claim or accurately states the family README already agrees with the v0.6 files (DeDi-registry).
- Owner precondition: none.

**Batch 6 — MeterData v0.6 metadata correction (source-edit — requires separate authorization)**
- Scope: `schemas/MeterData/v0.6/attributes.yaml:4-6` `info.version`/`info.description`.
- Acceptance test (recorded now for when authorized; **not executed under this report's report-only boundary**): `info.version` matches the directory's `v0.6` designation, and `info.description` names all nine current shapes (`CUSTOMER`, `INTERVAL`, `DAILY`, `MONTHLY`, `BILL_DETAILS`, `INSTANTANEOUS`, `EVENT`, `ALARM`, `DESCRIPTOR`) with the current `BILL_DETAILS` label, not the retired `BILLING` label; `scripts/generate_field_tables.py --all --check` still passes afterward.
- Owner precondition: `OD-S1` already settles *what* the correction should say (this is a source file, not a documentation page — its correction requires the schema-change proposal flow in `schemas/README.md#proposing-a-new-schema-or-a-change`, separate from and not authorized under this docs-focused remediation set).

**Batch 7 — Standards-precedence claim and dependent-prose correction (docs-only)**
- Scope: `schemas/README.md:87,94` and `use-cases-overview/consumer-energy-passport.md:61,159` (DUP-004), plus the duplicated mutable guidance at `use-cases-overview/consumer-meter-digest.md:58` and `use-cases-overview/smart-meter-data-exchange.md:71` (DUP-002.11). The canonical standards order is only `schemas/README.md:89-92`.
- Acceptance test: no scoped page claims every schema records per-field standards, `x-standards-precedence` exists at every schema root, or `x-standard`/`x-standards` is used on every property; wording names the actual key (`x-standard`, singular, per-field) and actual scope — two of eleven schema-version directories — or removes the unsupported universality claim. Both duplicated dependent pages point to the canonical order at `:89-92` rather than carrying independently mutable copies.
- Owner precondition: none — internally determinable from an exhaustive search of every `schema.json` and `attributes.yaml` under `schemas/`.

**Batch 8a — Conformance instruction-boundary correction (docs-only; internally resolvable)**
- Scope: `how-you-implement-ies/conformance.md:79` only. Correct the prose so it describes what the cited command actually validates: the credential-root document against the credential-root schema, not an isolated `credentialSubject`.
- Acceptance test: line 79's prose and command name the same credential-root input boundary; the edit does not claim that the external references have been fully validated.
- Owner precondition: none — the command boundary is mechanically determinable from the command itself.

**Batch 8b — Stub-aware structural-validation/conformance wording (docs-only; owner-gated)**
- Scope: `how-you-implement-ies/build-adapter.md:100-110,120,157`, `how-you-implement-ies/conformance.md:33,72,76,79,83,95`, and `use-cases/consumer-meter-digest/README.md:76`. Apply the recorded `OD-E2` posture across every live promise that the local validator establishes schema validation, conformance, or immediate production readiness.
- Acceptance test: the owner-approved wording distinguishes the structural validation the current tool actually establishes from external-schema conformance; it names only the actual stub-backed files (`MeterDataCredential/v0.6`, `MeterDataRequestCredential/v0.1`, `MeterData/v0.6`, `OutageNotification/v0.1`), does not claim `EnergyResource` has a current consumer, and leaves no cited page asserting unqualified conformance or production readiness from the stub-backed step.
- Owner precondition: **recorded `OD-E2` decision required.** This batch chooses public conformance posture and therefore cannot be executed as an internally determined wording fix.

No docs-only batch above (1, 2a, 3, 4, 5, 7, 8a, 8b) mixes with the unchanged technical release blockers (schema reproducibility, validators, PDF, CI) per gate 13.2; Batch 8b remains owner-gated. Batch 2b and Batch 6 are kept separate and explicitly marked as the two batches in this set that are not docs-only and not authorized for execution here.

---

## 10. Unresolved questions

1. **`OD-E1` (status posture):** which of the three tenses in ISS-008 is the intended public posture, and is there a fourth, more precise formulation (e.g. "completed a 30-day pilot; sandbox remains open for onboarding") that states the timeline unambiguously?
2. **`OD-E2` (conformance wording):** should checklist items that currently say "schema validation passes" be split into two gates ("structural validation passes" vs. "external-schema conformance — not yet established"), or is a centralized caveat sufficient only if every live validation promise links to it? Batch 8a can correct the deterministic `:79` command boundary immediately; Batch 8b must wait for this recorded posture decision and then apply it consistently to every cited validation/conformance promise.
3. **`OD-E3` (ElectricityCredential ownership):** externally-maintained-with-a-sync-verifier, or brought under local generation? No audience page currently claims either state as achieved, but the "verbatim mirror, upstream authoritative" framing is unverifiable either way without one.
4. **`OD-E5` (ArrFiling versioning convention):** does `attributes.yaml`'s `info.version` intentionally track something other than the schema family's public version number? If yes, the convention should be stated somewhere in the corpus; today it is stated nowhere.
5. **`OD-E6` (Pathways publication intent):** deliberately unlisted (staged) or a navigation defect? This determines whether ISS-011 is P2 (defect) or informational (intentional staging not yet documented as such).
6. **`OD-E4` (`index.md`'s role):** canonical deliverable, curated reading aid, or a page that should be retired? This sets the real severity of ISS-011/ISS-012/ISS-013 — if `index.md` is merely a curated aid (not itself a navigation contract), its self-generated anchor mismatches (ISS-013) are cosmetic; if it is meant to be a reliable clickable map (as its own opening prose claims — "organizes all documentation files... sequentially and systematically," `index.md:1-3`), they are a functional defect. No page in the corpus states which of these `index.md` is meant to be.

   **Full per-path disposition of the 14 Summary-only and 3 index-only paths** (derived from `SUMMARY.md`'s 57-entry link list vs. `scripts/generate_index.py`'s 46-entry hardcoded `sections` dict, Section 2.2(i)):

   | # | Path | Category | Disposition |
   |---|---|---|---|
   | 1 | `what-ies-provides/README.md` | what-ies-provides | Summary-only; hardcoded list never added it |
   | 2 | `schemas/MeterData/README.md` | schema family-root | Summary-only; hardcoded list never added it |
   | 3 | `schemas/MeterDataCredential/README.md` | schema family-root | Summary-only; hardcoded list never added it |
   | 4 | `schemas/MeterDataCredential/v0.6/README.md` | schema version-level | Summary-only; hardcoded list never added it |
   | 5 | `schemas/MeterDataRequest/README.md` | schema family-root | Summary-only; hardcoded list never added it |
   | 6 | `schemas/MeterDataRequestCredential/README.md` | schema family-root | Summary-only; hardcoded list never added it |
   | 7 | `schemas/ArrFiling/README.md` | schema family-root | Summary-only; hardcoded list never added it |
   | 8 | `schemas/OutageNotification/README.md` | schema family-root | Summary-only; hardcoded list never added it |
   | 9 | `schemas/OutageNotification/v0.1/README.md` | schema version-level | Summary-only; hardcoded list never added it |
   | 10 | `schemas/external/README.md` | schema, external-index | Summary-only; hardcoded list never added it |
   | 11 | `how-you-implement-ies/README.md` | how-you-implement-ies | Summary-only; hardcoded list never added it |
   | 12 | `how-you-implement-ies/build-adapter.md` | how-you-implement-ies | Summary-only; hardcoded list never added it |
   | 13 | `how-you-implement-ies/conformance.md` | how-you-implement-ies | Summary-only; hardcoded list never added it |
   | 14 | `use-cases-overview/p2p-energy-trading.md` | use-cases-overview | Summary-only; also ISS-012 (the one Summary-only entry independently confirmed against `generate_index.py`'s source list) |
   | 15 | `SUMMARY.md` | foundational reference | index-only; index curator surfaces it beyond `SUMMARY.md`'s own link list |
   | 16 | `schemas/README.md` | schemas master map | index-only; same basis |
   | 17 | `schemas/MeterData/v0.6/CHANGELOG.md` | schema changelog | index-only; same basis |

   **Nine of the 14 Summary-only paths are under `schemas/`** (rows 2-10 above) — not eight as a prior pass stated. Of those nine, six are true family-root READMEs (`MeterData`, `MeterDataCredential`, `MeterDataRequest`, `MeterDataRequestCredential`, `ArrFiling`, `OutageNotification`), two are version-level READMEs for families whose *other* versions' pages `generate_index.py` does include (`MeterDataCredential/v0.6`, `OutageNotification/v0.1`), and one is the external-schemas index (`schemas/external/README.md`), which is not a versioned family page at all — the prior "8 schema family-root READMEs" figure undercounted by conflating this mixed set with a single category. None of the 17 paths across both sets is evidence of intentional exclusion; all read as `generate_index.py`'s hardcoded list simply not being kept in sync as pages were added or as the index curator's own additions beyond `SUMMARY.md` — which is what `OD-E4` would settle the required remedy for.
7. **`OD-E7` (Windows support posture) and `OD-E8` (duplicate example / `scratch/` disposition):** both remain open per `qaqc/01`/`qaqc/02`/`qaqc/04`; nothing in the 79-file audience corpus bears on them further, so this audit adds no new evidence and defers entirely to the prior reports on these two items.
8. **DUP-002 count reconciliation:** the reproducible scan yields 14 qualifying exact block-pair groups, reconciled into 13 repeated-concept clusters because DUP-002.9 merges two adjacent block pairs for the same checklist template and file pair. All 13 concept clusters are judged: 12 accepted; DUP-002.11 assigned to Batch 7. The five-word checklist label is outside both counts. The difference from `qaqc/04`'s bare 7 is scanner parameterization, not content drift.
