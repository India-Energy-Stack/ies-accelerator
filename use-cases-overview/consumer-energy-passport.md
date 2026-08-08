# Consumer Energy Passport

*The IES [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2), issued holder-bound to a consumer's wallet (W3C Verifiable Credential).*

**[Implementation Guide →](../use-cases/consumer-energy-passport/README.md)**

| Field | Value |
|---|---|
| Document | IES/CEP-PROFILE/1.2 |
| Status | Piloted (four pilot DISCOMs) — see [Status](../STATUS.md) |
| Applicability | All distribution licensees |
| This version | Consumer Energy Passport *variant* of ElectricityCredential v1.2. Static credential only; live interval data uses MeterData, separately. |

---

## 1. Scope and Purpose

The stakeholder is the distribution licensee (DISCOM) and the consumer it serves. As rooftop solar, batteries and EV charging grow behind consumers' meters, the licensee often cannot see what's connected, at what capacity, or where; and the consumer cannot prove their connection and assets to a bank, subsidy portal or marketplace without a manual DISCOM letter.

This document defines the **Consumer Energy Passport** — the holder-bound issuance of the ElectricityCredential v1.2, carrying the static facts of a consumer's connection and the energy resources behind their meter. It does not define a new schema: ElectricityCredential v1.2 is the schema; the Passport profiles how it's shaped, issued and delivered when the consumer is the audience (`credentialSubject.id` = wallet DID; `customerProfile.idRef` = a government-ID reference).

## 2. What It Records / Covers

| Records | Detail | Source |
|---|---|---|
| Consumer & issuing licensee | The consumer and the DISCOM that issues the credential | ElectricityCredential v1.2 (`customerProfile`, `issuer`) |
| Service connection | Tariff category and sanctioned load | ElectricityCredential v1.2 (`consumptionProfiles[]`) |
| Meters | The net meter, and a generation meter where used | ElectricityCredential v1.2 (`energyResources[]`, type `METER`) |
| Distribution transformer | Where known | ElectricityCredential v1.2 (`energyResources[]`, network equipment) |
| Energy resources behind the meter | Solar, battery, EV charger, inverter, controllable load — with capacity, inspection status and equipment details | ElectricityCredential v1.2 (`energyResources[]`) |

It records identity, capacity and status — **not live readings**, which are the [MeterData](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) record, linked by asset identifier (see [Consumer Meter Digest](consumer-meter-digest.md)).

## 3. How Each Item is Identified

Every item — consumer, connection, each meter, each asset — carries a [DID](../glossary.md#did). Existing licensee numbers are reused as aliases inside identifiers.

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (issuer) | `did:web` on owned domain | `did:web:ies.discom.example` |
| Regulator | `did:web` on owned domain | `did:web:ies.serc.example` |
| Consumer (holder) | `did:key` (wallet) or `tel:` URI | `did:key:z6MkjVQ8r4f3rPuY…` |
| Meter / inverter / DER / transformer | `did:web` under issuer domain | `did:web:ies.discom.example:assets:meter:NM-44091234` |
| Existing CIS consumer number | Plain string, kept verbatim | `1102004567` → `customerProfile.customerNumber` |

[DeDi](../glossary.md#dedi) is used only for Beckn subscriber registries and credential revocation — not as an identifier method for consumers, meters or assets.

## 4. Definitions

- **DER** — any device behind a meter that generates (solar, wind), stores (battery) or controllably consumes (EV charger) electricity.
- **DID** — verifiable digital identifier (W3C DID Core), detailed in §3.
- **Verifiable Credential (VC)** — a tamper-evident, signed document (W3C VC Data Model 2.0) a verifier checks offline against the issuer's published key.
- **Energy Resource** — any physical asset in the credential, one typed entry in `energyResources[]`.
- **QuantitativeValue** — a `{value, unit}` pair for every power/energy/capacity figure, mapped to QUDT.
- **Holder-bound** — issued to a specific holder's wallet, vs. a bearer credential.
- **Net Meter** — the bidirectional billing meter; the source of truth.
- **Aggregator** — a third party enrolling controllable resources for demand response.

## 5. Basis of Standards

Fixed order of preference: **IS → CEA Regulations / IEGC → IEC → IEEE**, recorded in the field tables below.

| Standard | Role here |
|---|---|
| **IS 16444** | Smart meter specification |
| **IS 15959** | DLMS/COSEM; OBIS codes for metering |
| **CEA (Installation and Operation of Meters) Regulations, 2006** | The net meter as the source of truth |

## 6. Where Indian Standards Do Not Yet Exist

- **Grid asset data model** — IEC CIM (IEC 61970-301, IEC 61968-11) underlies the `energyResources[]` kinds.
- **DER electrical attributes** — IEEE 1547-2018 (ride-through, anti-islanding, volt-var, freq-watt); CEA's own limits are retained where CEA sets them (harmonics per IEEE 519-2014; DC injection ≤0.5% under CEA Connectivity Regs 2013, am. 2019).
- **PV module rating** — DC array capacity (kWp) follows **IS 14286** (= IEC 61215).

## 7. The Record

One record: a static Verifiable Credential, changed only on commissioning, capacity change or ownership transfer, and re-issued (with revocation of the old) on material change. It is holder-bound — the consumer holds it in DigiLocker or a DID wallet and discloses fields selectively. Live interval data is a separate [MeterData](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) record, linked by identifier.

## 8. Schedule I --- Consumer Energy Passport (Static Record)

Schedule I is a standards-and-status reference table over the real ElectricityCredential v1.2 schema. Each row's **Normative Path** column is an actual JSON path in `schemas/ElectricityCredential/v1.2/schema.json`; **Schema Requires** reflects what the JSON Schema itself enforces. The **Type** column states the CEP profile's expected format for the field (e.g. "did:key", "text", "QuantitativeValue (kW)") — it is a schema-level constraint only where **Schema Requires** says so (e.g. an `enum`, a `required` object shape, a `pattern`); where **Schema Requires** is silent on format, **Type** is CEP profile expectation, not something `validate_schema.py` enforces. The **Standard** and **CEP Profile Guidance** columns are *informative annotations* — they record which standard governs the concept and whether the Consumer Energy Passport profile expects issuers to populate the field. They do not add fields to the schema. Where the earlier draft used a conceptual path with no EC v1.2 equivalent, it is retired to §8.6 as *not represented*, rather than mapped to something that doesn't exist.

### 8.1 Holder, Issuer and Customer Identity

| **Normative Path (EC v1.2)** | **Type** | **Schema Requires** | **Standard** *(informative)* | **CEP Profile Guidance** *(informative)* |
|---|---|---|---|---|
| `credentialSubject.id` | did:key (or did:web) | Optional | W3C DID Core | Mandatory — the holder's wallet DID |
| `credentialSubject.customerProfile` | object | Required | --- | Mandatory — the container for customer identity and assets |
| `credentialSubject.customerProfile.customerNumber` | text (billing number) | Required | CEA Meter Regs; DISCOM billing | Mandatory |
| `credentialSubject.customerProfile.energyResources` | array, min 1 | Required | --- | Mandatory |
| `credentialSubject.customerProfile.idRef.issuedBy` / `.subjectId` | IdRef {did/uri, string} | Object optional; if present, both `issuedBy` and `subjectId` are required | IES IdRef | Optional — government-ID reference (e.g. DigiLocker), see §11.1 |
| `credentialSubject.customerDetails.fullName` / `.installationAddress` / `.serviceConnectionDate` | text / GeoJSON+address / date-time | Optional object; if present, all three required | CIM (IEC 61968-1) | Mandatory — kept out of `customerProfile` since it is PII |
| `issuer.id` | did:web | Required | IES registry | Mandatory — the DISCOM's operational identifier |
| `issuer.name` | text | Required | --- | Mandatory |
| `issuer.idRef.issuedBy` / `.subjectId` | IdRef {did:web, string} | Optional | IES registry | Optional — regulator-issued DISCOM registration reference |

### 8.2 Service Connection and Metering

EC v1.2 has no standalone "service connection" object. Tariff and load facts for a connection live in `consumptionProfiles[]`, linked to its net meter by `meterId`; the meter itself is one entry in `energyResources[]`.

| **Normative Path** | **Type** | **Schema Requires** | **Standard** *(informative)* | **CEP Profile Guidance** *(informative)* |
|---|---|---|---|---|
| `credentialSubject.customerProfile.consumptionProfiles[].meterId` | text (= a `METER` `energyResources[].id`) | Required, within each entry | CIM UsagePoint | Mandatory |
| `consumptionProfiles[].tariffCategoryCode` | text | Required, within each entry | SERC tariff order | Mandatory |
| `consumptionProfiles[].sanctionedLoad` | QuantitativeValue (kW) | Required, within each entry | CEA; SERC supply code | Mandatory |
| `consumptionProfiles[].sanctionedExportLoad` | QuantitativeValue (kW) | Optional | CEA | Optional |
| `consumptionProfiles[].contractMaxDemand` | QuantitativeValue (kW) | Optional | CEA | Optional |
| `consumptionProfiles[].serviceStatus` | enum `active`/`suspended`/`closed` | Optional | CIM UsagePoint.status | Optional |
| `consumptionProfiles[].connectionType` | enum `Single-phase`/`Three-phase` | Optional | CIM UsagePoint.phaseCode | Optional |
| `consumptionProfiles[].premisesType` | enum Residential/Commercial/Industrial/Agricultural | Optional | --- | Optional |
| `consumptionProfiles[].paymentMode` | enum `POSTPAID`/`PREPAID` | Optional | CIM; ESPI | Optional |
| `consumptionProfiles[].billingCycleDay` | integer 1–31 | Optional | --- | Optional |
| `energyResources[]` (type `METER`) `.id` — net meter | did:web | Required, per resource | IS 16444; CIM Meter | Mandatory |
| `energyResources[]` (type `METER`) `.attributes.serialNumber` | text | Optional | IS 16444 | Optional |
| `energyResources[]` (type `METER`) `.attributes.meterCapability` | enum Electromechanical/CMRI/AMR/AMI | Optional | CIM AmiBillingReadyKind | Optional |
| `energyResources[]` (type `METER`) `.attributes.energyDirection` | enum Forward/Reverse/Bidirectional/Net | Optional | CIM FlowDirectionKind; ESPI | Optional — `Reverse` distinguishes a generation meter |
| `energyResources[]` (type `METER`, generation meter) `.parentResources[]` | array of resource ids | Optional | IES topology | Optional — points at the net meter's id |
| `energyResources[]` (type `INVERTER`) `.id` | did:web | Required, per resource | IEEE 1547; CIM PowerElectronicsConnection | Optional |
| `energyResources[]` (type `INVERTER`) `.attributes.serialNumber` | text | Optional | equipment nameplate | Optional |
| `energyResources[]` (type `DT`) `.id` — distribution transformer | did:web | Required, per resource | CIM PowerTransformer | Optional |
| `energyResources[]` (type `DT`) `.attributes.serialNumber` | text | Optional | equipment nameplate | Optional |
| `energyResources[]` (type `DT`) `.attributes.nominalVoltage` | QuantitativeValue (kV) | Optional | CIM BaseVoltage | Optional |

### 8.3 Energy Resources — Common Fields (every entry in `energyResources[]`, any type)

| **Normative Path** | **Type** | **Schema Requires** | **Standard** *(informative)* | **CEP Profile Guidance** *(informative)* |
|---|---|---|---|---|
| `energyResources[].id` | did:web | Required, per resource | IES; CIM | Mandatory |
| `energyResources[].type` | enum, per kind — see §8.4 | Required, per resource | IEC 61850-7-420; CIM | Mandatory |
| `energyResources[].parentResources[]` | array of resource id strings only | Optional | IES topology | Optional — carries the DER↔inverter↔meter↔DT topology, see §10 |
| `energyResources[].subResources[]` | array; each item is *either* a resource id string *or* an inline `EnergyResource` object | Optional | IES topology | Optional — carries the DER↔inverter↔meter↔DT topology, see §10 |
| `energyResources[].attributes.make` / `.model` / `.serialNumber` | text | Optional | equipment nameplate | Optional |
| `energyResources[].attributes.maxExport` / `.maxImport` / `.ratedPower` | QuantitativeValue (kW) | Optional | IEEE 1547-2018; CEA | Mandatory for generation/storage/EV-charger resources |
| `energyResources[].attributes.commissioningDate` | date-time | Optional | --- | Optional |
| `energyResources[].attributes.inspection.date` / `.result` / `.inspectorId` | date / enum pass,fail,conditional / text | Optional | IEEE 1547; CEA | Optional |
| `energyResources[].attributes.aggregator.id` / `.name` / `.controllable` / `.enrolledOn` | did:web / text / boolean / date | Optional | IEC 61850-7-420; IEEE 2030.5 | Optional — see §8.5 |

### 8.4 Energy-Resource Type Discriminators and Type-Specific Attributes

| **DER Concept** | **`energyResources[].type` value(s)** | **Type-specific attributes** | **Standard** *(informative)* |
|---|---|---|---|
| Solar (PV) | `SOLAR_PV` (`SOLAR` deprecated) | `attributes.dcArrayCapacity` (kW, "kWp" by convention), `.nominalPower` (kW), `.efficiency` (%) | IS 16221; IS 14286; IEC 61727 |
| Battery | `BESS` (`BATTERY` deprecated) | `attributes.storageCapacity` (kWh), `.storageType` (enum), `.stateOfHealthPct`, `.roundTripEfficiencyPct` | IEC 62933; IEC 62619 |
| EV charger | `EV_CHARGER` / `EV_V2G` (bidirectional) | `attributes.connectorType` (enum), `.controlProtocol` (enum), `.v2xProtocol` (schema-permitted on either type; CEP profile guidance restricts population to EV_V2G resources, not schema-enforced) | IS 17017; IEC 62196; OCPP; ISO 15118 |
| Wind | `WIND` | `attributes.nominalPower` / `.maxExport` (kW) | IEC 61400 |
| Other generation (hydro, biogas, CHP, fuel cell) | `HYDRO` / `BIOGAS` / `CHP` / `FUEL_CELL` | `attributes.nominalPower` (kW), `.efficiency` (% — most relevant for `CHP`/`FUEL_CELL`) | CIM GeneratingUnit (IEC 61970-301) |
| Inverter | `INVERTER` (const) | `attributes.ratedApparentPower` (kVA), `.maxReactivePower` / `.minReactivePower` (kVAR), `.rideThroughCategory`, `.operatingMode`, `.voltVarEnabled`, `.freqDroopEnabled`, `.enterServiceRampTimeSec` (seconds to ramp 0→rated power after reconnection) | IEEE 1547-2018; SunSpec DER Models |
| Distribution transformer / bus / feeder / microgrid | `DT` / `BUS` / `FEEDER` / `MICROGRID` | `attributes.nominalVoltage` (kV), `.zone`, `.substationId`, `.feederCode` | CIM (IEC 61970-301) |
| Controllable load | `SMART_HVAC` / `SMART_WATER_HEATER` / `CONTROLLABLE_LOAD` | `attributes.controlProtocol`, `.loadCategory` | IEC 61850-7-420; OpenADR 2.0b |

### 8.5 Aggregator Enrolment and Controllability (informative)

EC v1.2 has no separate array for "devices an aggregator can control." Any `energyResources[]` entry — a BESS, EV charger, or controllable load — carries its own `attributes.aggregator` object (`id`, `name`, `controllable` boolean, `enrolledOn`). Whether an asset is dispatchable is answered per-resource, not via a separate list, and a device that is both a DER and separately dispatchable (e.g. an aggregator-enrolled BESS) is one `energyResources[]` entry, not two.

### 8.6 Concepts Not Represented in ElectricityCredential v1.2

| **Conceptual field (earlier draft)** | **Disposition** |
|---|---|
| `serviceConnection.did` — a DID for the "service connection" itself | Not represented. The connection has no separate identifier; it is addressed via `consumptionProfiles[].meterId` pointing at the net meter's `energyResources[].id`. |
| `discom.trustDid` — a second "trust" DID for the issuer, distinct from its operational DID | Not represented. `issuer` carries a single `id` (did:web). A regulator-issued registration reference belongs in `issuer.idRef`. |
| `der[].profile.inverterDids[]` — an explicit list field linking a DER to its inverter(s) | Not represented as a field. Use `parentResources[]` on the DER entry, pointing at the inverter's id — see the topology diagram in §10. |
| `der[].profile.generationMeterDid` | Not represented as a field on the DER. A generation meter is its own `energyResources[]` entry (type `METER`), linked into the topology via its own `parentResources[]`. |
| `der[].profile.oemNameplate.maker` (as a did:web) / `.deviceId` (composite model.serial) | Not represented. Nameplate identity is flat text: `attributes.make`, `.model`, `.serialNumber` — there is no manufacturer DID field and no composite device-id field. |
| `controllableAssets[]` (separate array) / `.linkedDerDid` | Not represented as a separate array — see §8.5. |
| EV charger `operator` | Not represented — no operator field on `EnergyResourceEVChargerAttributes`. |
| `consumer.customerReference` — a separate consumer-facing reference distinct from the billing number | Not represented. `customerProfile.customerNumber` (the utility CA number) is the only customer-identity field; there is no second `customerReference` field. |
| `der[].profile.identity.imei` / `.m2mSimId` — device-level cellular/M2M identity metadata on a DER | Not represented as schema fields on any `EnergyResource` kind. `m2mSimId` is an out-of-band MeterData transport concept, documented in [DER Visibility §9.2](der-visibility.md#id-9.2-explicitly-informative-extensions-not-native-meterdata-v0.6-fields) — not a Schedule I / EC v1.2 field. |
| `der[].profile.battery.chargePower` / `.dischargePower` — dedicated battery charge/discharge-power telemetry fields | Not represented as named fields. A BESS resource's charge/discharge limits are carried on the common `attributes.maxImport` (charge) / `.maxExport` (discharge) fields inherited from `EnergyResourceCommonAttributes` — there are no BESS-specific `chargePower`/`dischargePower` fields. |

### 8.7 Example and Validation

Full worked example: [`schedule-i-example.json`](../use-cases/consumer-energy-passport/examples/schedule-i-example.json). It is an illustrative payload fixture — the `proof` block carries a placeholder value and is **not** a cryptographically valid signature.

Validate it structurally against ElectricityCredential v1.2:

```
python -X utf8 -B scripts/validate_schema.py schemas/ElectricityCredential/v1.2/schema.json use-cases/consumer-energy-passport/examples/schedule-i-example.json
```

## 9. Schedule II

**Not applicable.** The Consumer Energy Passport carries no time-dependent data. Every field in Schedule I is fixed at issuance and changes only on re-issuance after a material change, so there is no live half to map.

Live data that references this credential is exchanged separately, under its own use case:

| Live record | Where it is specified | How it links back |
|---|---|---|
| The consumer's own meter readings | [Consumer Meter Digest — Schedule II](consumer-meter-digest.md#id-9.-schedule-ii-meter-readings-live-record) | `meterRefs` carries the net meter's `energyResources[].id` from Schedule I |
| Telemetry from behind-the-meter DER (inverter, PV, battery) | [DER Visibility — Schedule II](der-visibility.md#id-9.-schedule-ii-der-telemetry-live-record) | `meterRefs` carries the inverter's `energyResources[].id` from Schedule I |

Neither is carried inside the Passport, and neither is required to read it.

## 10. How It Fits Together

```
                      ┌── Solar array
Grid ──[ Net Meter ]──┼── (Generation Meter *) ── Inverter ** ──┬── Solar array
   (billing meter,    │                                          └── Battery
    source of truth)  └── Inverter ** ── EV charger
  *  used by some licensees, not others.  ** may serve more than one asset.
  Topology: parentResources / subResources — PV and BESS → Inverter → Meter → DT.
```

Generation is measured at the net meter, a generation meter, or the inverter's own live data (MeterData). All assets live in one `energyResources[]` array; the credential carries identity and ratings, MeterData carries live readings.

## 11. Points for Confirmation

1. **Holder-binding method.** Confirmed for the DigiLocker Pull URI channel: the `DigiLockerId` from the pull request is carried into `customerProfile.idRef` as the identity binding (see [DigiLocker Integration — Identity Binding](../how-you-implement-ies/digilocker.md#identity-binding-the-digilocker-id)). Non-DigiLocker methods (offline-KYC XML, in-person) remain open, to be documented for privacy review.
2. **Selective-disclosure profile** with first verifiers (SD-JWT-VC typical).
3. **Re-issuance triggers** on material change, and revocation into the DeDi registry.
4. **Schema-host provenance** — served from `india-energy-stack.github.io/ies-accelerator`; a custom IES/gov domain is a governance decision.

---

## Schemas Used in This Use Case

A single schema — **[ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)** (W3C VC). No additional schemas: Schedule I is the whole record and there is no Schedule II (§9).

Live readings that reference this credential use [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) under their own use case — the consumer's own meter via [Consumer Meter Digest](consumer-meter-digest.md), behind-the-meter DER via [DER Visibility](der-visibility.md).

## Value Unlock

The consumer gains a portable, tamper-evident proof of their connection and assets, verifiable offline by banks, subsidy portals and marketplaces in seconds — no DISCOM callback. The DISCOM cuts verification load and fraud and gets a clean asset register as a by-product. Regulators get a consistent, auditable asset record across licensees. Selective disclosure lets the consumer reveal only what a verifier needs.

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 16444 (Parts 1, 2) | AC smart meter — specification |
| IS 15959 (Parts 1–3) | DLMS/COSEM companion spec; OBIS codes |
| IS 14286 (= IEC 61215) | PV module design qualification and type approval |
| IS 16221 (Parts 1, 2) (= IEC 62109-1/-2) | Inverter safety (inverter resource only) |
| IS 16270 | Solar PV batteries |
| IS 17017 (series) (from IEC 61851 / 62196) | EV conductive charging |
| CEA (Installation and Operation of Meters) Regs, 2006 | Metering legal framework; net meter as source of truth |
| CEA (Connectivity of DG Resources) Regs, 2013, am. 2019 | Connectivity below 33 kV; PCC; DC-injection; harmonics |
| IEC 61968-1 / -9 / -11 | CIM — customer, metering, distribution model |
| IEC 61970-301 / -302 | CIM — network model; DER / power-electronics / battery |
| IEC 61850-7-420 | DER control roles |
| IEC 61727 / IEC 62116 | PV utility interface; anti-islanding |
| IEC 62933 / 62933-2-1 / IEC 62619 | Storage systems; performance test; battery safety |
| IEC 62196 | EV connectors |
| IEC 62056 | DLMS/COSEM; OBIS |
| IEEE 1547-2018 | DER interconnection and interoperability |
| IEEE 519-2014 | Harmonic control (CEA-referenced) |
| IEEE 2030.5 | DER communications / aggregator roles |
| W3C VC Data Model 2.0; W3C DID Core | Credential envelope; identifiers |
| GeoJSON (RFC 7946); schema.org PostalAddress | Location and postal address |
| OCPP; ISO 15118 | EV charger control / V2G |

## Annexure B — Example Payload

A single-phase LT-Domestic connection with a 5 kW PV array on a 5 kVA inverter and a 6 kWh aggregator-enrolled battery, fed from one DT. Holder-bound; identifiers illustrative.

- **[`examples/example.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/ElectricityCredential/v1.2/examples/example.json)**
- **[`example-submetering.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/ElectricityCredential/v1.2/examples/example-submetering.json)** — building main meter + tenant sub-meters + rooftop solar
- **[`example-parallel-metering.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/ElectricityCredential/v1.2/examples/example-parallel-metering.json)** — import + export meter (solar FIT)

## Annexure C — JSON Schema

Canonical: `https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/` — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json) (Draft 2020-12), [`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.jsonld), [`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/vocab.jsonld). ElectricityCredential v1.2 is one of two schema-version directories (of eleven across IES) that annotates individual fields with their governing standard, via the singular `x-standard` property; the §5 order of preference (`IS → CEA Regulations / IEGC → IEC → IEEE`) applies regardless of whether a given schema carries that annotation.
