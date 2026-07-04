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

## Deliberately NOT applied — needs a governance decision

These are left unchanged; each needs a policy/authority choice, not a lookup (review §7 items 4, 8, 9, 10; open items O-4/O-5):

- **Meter Indian basis** (`type`, `meterCapability`, `energyDirection`, `functions`): add IS 16444 / IS 15959 and the CEA Metering Regulations 2006 as authority. Requires governance sign-off.
- **ESPI/NAESB demotion** (`energyDirection`, `paymentMode`): North-American references to drop or footnote — policy choice.
- **SERC authority** (`sanctionedLoad`, `tariffCategoryCode`): which state instrument to name.
- **`paymentMode`**: `AmiBillingReadyKind` ≠ prepaid/postpaid; the prepayment-meter basis is OPEN.
- **EV-charger IS 17017**, **VC proof-suite migration** (`Ed25519Signature2020 → eddsa-rdfc-2022`): governance/crypto policy.

Full context: the standalone review (`IES_Standards_Conformance_Review_FINAL`), §7 correction set and §8 per-citation tables.
