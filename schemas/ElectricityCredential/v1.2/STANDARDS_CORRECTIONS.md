# Standards-citation corrections — ElectricityCredential v1.2

**Branch:** `fix/standards-conformance-citations` · **Status:** proposal (not pushed)
**Basis:** independent standards-conformance review of the rendered Guide (the `x-standard`
annotations on the DER `EnergyResource` fields), re-verified 2026-07-04. Each change below is a
factual citation correction; none changes a field name, type, enum, or `$id`.

## ⚠️ Where the durable fix must land (read first)

This file (`schema.json`) is a **compiled bundle**: the DER field definitions carrying these
citations are authored **upstream** in `EnergyResource/v2.1` and `EnergyResourceCommon/v1.1`
(referenced from `attributes.yaml` as `$ref: https://schema.beckn.io/…`) and inlined here at
build time. Per this repo's mirror policy ("treat upstream as authoritative; do not edit schema
files in place"), the corrections below **must also be applied upstream in `beckn/DEG`** or they
will be overwritten the next time the bundle is regenerated. This branch edits the local bundle so
the fixes are concrete and reviewable; it does **not** substitute for the upstream change
(governance item O-10: re-home the domain-schema authoring into IES, or file the change upstream).

`README.md` was regenerated from the corrected `schema.json` via
`scripts/generate_field_tables.py` (the FIELD-TABLE region is auto-generated; the hand-written
kinds table above it was corrected in place).

## Applied — mechanical / factually unambiguous

| Field | Was | Now | Why |
|---|---|---|---|
|`fullName`, `installationAddress`, `serviceConnectionDate`|`IEC 61968-1 …`|`IEC 61968-11 …`|`Customer`/`ServiceLocation` are defined in 61968-11; 61968-1 is interface architecture|
|`ratedPower`, `nominalPower`|`IEC 61970 …`|`IEC 61970-301:2020 …`|Pin the CIM base sub-part + edition|
|`maxExport`|`IEC 61970-302 PowerElectronicsConnection.maxP`|`IEC 61970-301 PowerElectronicsUnit.maxP`|-302 is *CIM dynamics*; and `maxP` lives on `PowerElectronicsUnit` (the unit), not `PowerElectronicsConnection`|
|`maxImport`|`IEC 61970-302 PowerElectronicsConnection.maxP`|`IEC 61970-301 PowerElectronicsUnit.minP` (import = \|minP\|)|as above; absorption limit is the unit's signed `minP`|
|`storageCapacity`|`IEC 61970-302 BatteryUnit.ratedE`|`IEC 61970-301 BatteryUnit.ratedE`|`BatteryUnit` is a base-model class|
|`ratedApparentPower`/`maxReactivePower`/`minReactivePower`|`IEC 61970-302 …ratedS/maxQ/minQ`|`IEC 61970-301 …`|these attributes *are* on `PowerElectronicsConnection`, but in the base (-301), not dynamics|
|`inspection`|`IEEE 1547-2018 Cl. 11 (commissioning); CEA … 2013 (amended 2018)`|`CEA (…Connectivity below 33 kV) Regulations 2013 (as amended 2019); IEEE 1547-2018 Cl. 11 (test & verification…)`|precedence (CEA before IEEE); the operative amendment is 2019 not the 2018 draft; Cl. 11 is "Test and verification"|
|`aggregator`|`IEEE 2030.5; IEC 61850-7-420 …`|`IEC 61850-7-420:2021 …; IEEE 2030.5-2023 …`|precedence (IEC before IEEE); pin editions (2030.5-2018 → 2023)|
|`voltVarEnabled`|`IEEE 2030.5 …`|`IEEE 2030.5-2023 …`|pin current edition|
|`connectionType`|`IEC 61968-9 UsagePoint.phaseCode`|`IEC 61970-301 PhaseCode; via IEC 61968-9 UsagePoint.phaseCode`|`PhaseCode` enum is defined in 61970-301|
|`dcArrayCapacity`|`IS 16221 (PV module qualification); IEC 61727`|`IS 14286 (Part 1/Sec 1):2023 (= IEC 61215-1-1:2021); IEC 61727`|IS 16221 is inverter/converter **safety**, not module qualification — the one wrong BIS citation|
|`operatingMode`|`IEC 61970-302 PowerElectronicsConnection.inverterMode`|`IEEE 1547-2018 (GFM/GFL mode) — no native CIM attribute; IES extension candidate`|no `inverterMode` attribute exists, and grid-forming/following is not a native CIM concept|
|Prose descriptions (Storage, Inverter, kinds table, `vocab.jsonld` comments)|`IEC 61970-302`|`IEC 61970-301`|same sub-part correction in descriptive text|

## Governance decisions — resolved 2026-07-04

Six items originally left as governance-gated (review §7 items 4, 8, 9, 10; open items O-2/O-4/O-5) were walked through and decided; all six are now applied to `schema.json` (+ the three `examples/*.json` for the proof-suite item). Decisions and rationale below.

| # | Field(s) | Decision | Now cites | Rationale |
|---|---|---|---|---|
|1|`type` (METER), `meterCapability`, `functions`|**IS-first, full rewrite**|`IS 16444 (Parts 1 & 2) [primary]; CEA (Installation and Operation of Meters) Regulations 2006 [authority]; CIM (…) [data model]`|Matches the document's own stated precedence rule (§2 of the review) rather than a co-citation that leaves CIM first|
|2|`energyDirection`|**IS-first + ESPI kept as informative footnote**|`IS 15959 (DLMS/COSEM) [primary]; CIM (FlowDirectionKind) [data model]; ESPI NAESB REQ.21 [informative — not normative]`|ESPI has no jurisdictional or semantic claim on this field (it's a US data-sharing authorization standard, not a metering data model) — demoted rather than dropped, since the enum values were originally modeled on Green Button and the footnote preserves that provenance for integrators|
|3|`paymentMode`|**Researched and resolved** (was an open factual gap, not a policy choice — O-2)|`IS 15884:2024 (AC Direct Connected Static Prepayment Meters, Class 1 & 2) [prepayment hardware]; IS 16444 (Parts 1 & 2) [shared platform]; CEA (Installation and Operation of Meters) (Amendment) Regulations 2022, Reg. 4 [mandate]; CIM (AmiBillingReadyKind) [data model]; ESPI [informative]`|Verified directly against the BIS catalogue + CEA regulation text (2026-07-04): **IS 16046 is unrelated** (portable battery safety, IEC 62133 adoption — confirmed NOT to be cited); **IS 15884 is real and current** (revised 2024), and CEA's 2022 amendment, Reg. 4, is the actual mandate requiring prepayment mode|
|4|`sanctionedLoad`, `tariffCategoryCode`|**Generic SERC placeholder**|`SERC Supply Code / SERC tariff order (state-specific) [authority]; CIM (…) [data model]`|Authority is genuinely state-specific (each SERC issues its own Supply Code/tariff order) — no single national instrument exists to name, so the field states the authority type without picking one state. (`sanctionedLoad`'s CIM part also corrected 61968-9 → 61968-11 while in the field, per the review's §8 recommendation.)|
|5|`connectorType`, `controlProtocol`, `v2xProtocol`|**Add IS 17017 as primary, IEC/ISO as parent**|`IS 17017 (relevant Part) [primary]; IEC 62196/61851 or ISO 15118/OCPP [parent/exchange protocol]`|These fields previously had no `x-standard` at all (only prose naming the international standards) — IS 17017 is India's harmonized EV-charging series|
|6|VC `proof.type` (3 example files)|**Migrated now**|`DataIntegrityProof` + `cryptosuite: eddsa-rdfc-2022`|`Ed25519Signature2020` is deprecated under VC 2.0. `proof.type` in `schema.json` has no enum constraint, so this only touched the three example payloads, not the schema shape|

All three examples re-validated 100% compliant against the corrected schema after every change (`scripts/validate_schema.py`).

Full context: the standalone review (`IES_Standards_Conformance_Review_FINAL`), §7 correction set and §8 per-citation tables.
