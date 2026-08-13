# DER Visibility

*A DISCOM's view of every distributed energy resource (DER) behind its meters, in two halves: what is connected (Schedule I, [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md)) and what it is doing now (Schedule II, [MeterData v0.6](../schemas/MeterData/v0.6/README.md)). Both halves are executable today at the per-consumer / per-DER level; the grid-side per-locus **aggregate** of Schedule I remains an illustrative future profile — see §1 and §8.2.*

**[Implementation Guide →](../use-cases/der-visibility/README.md)**

| Field | Value |
|---|---|
| Applicability | All distribution licensees |
| This version | Executable today: the per-consumer ElectricityCredential v1.2 (Energy Passport). Illustrative, future: a grid-side, PII-free per-locus profile conceptually reusing `energyResources[]` + `consumptionProfiles[]` (the building blocks of ElectricityCredential v1.2), with the network locus — not a consumer — as subject; see §1. |

---

## 1. Scope and Purpose

The stakeholders are the DISCOM (issuer), its grid operator, and any aggregator enrolling controllable resources. As rooftop solar, batteries and EV charging spread, the licensee often can't answer: what's connected on feeder F-02, at what capacity, and is it controllable?

This document defines **DER Visibility** — a DISCOM's view of the distributed energy resources connected behind its meters, for grid operators and aggregators to ingest directly. It carries **no consumer names, addresses or contact details** in any tier.

**Two delivery tiers.** Not all of this use case carries the same privacy weight, and the distinction is load-bearing:

| Tier | What it carries | Who may read it |
|---|---|---|
| **Open** | Counts and capacity totals per feeder or substation — no resource identifiers, no meter identifiers | Anyone |
| **Authenticated** | The per-resource records of [Schedule I](#id-8.-schedule-i-static-fields-of-the-credential) and the per-DER telemetry of [Schedule II](#id-9.-schedule-ii-der-telemetry-live-record), keyed by resource and meter identifiers | Grid operators and enrolled aggregators, under a stated lawful basis |

Identifier-keyed records are **pseudonymous, not anonymous**: a meter or resource identifier resolves back to a single consumer through the licensee's own systems. They are therefore personal data, and they sit in the authenticated tier. Only the open tier is publishable without access control. This tiering is the *proposed* answer to the privacy review still open at [§11.3](#id-11.-points-for-confirmation) — it is not yet a settled position.

**What is executable today.** The only currently executable ElectricityCredential v1.2 path is the **per-consumer credential** — the [Consumer Energy Passport](consumer-energy-passport.md) — whose `credentialSubject.customerProfile.customerNumber` is a required field. It carries the same `EnergyResource` and `ConsumptionProfile` building blocks referenced below, issued to one consumer at a time. See the validated [Schedule I example](../use-cases/consumer-energy-passport/examples/schedule-i-example.json). Today, a grid operator or aggregator wanting per-connection detail would consume that credential (with consumer consent), not a feeder-level aggregate.

**A note on the aggregate (illustrative, future).** ElectricityCredential is issued per consumer connection — its subject is one `customerProfile` with one customer number — so it **cannot combine multiple consumers' credentials** into a feeder- or substation-level record; each consumer keeps their own Energy Passport. A PII-free, per-locus view is described below as an **illustrative future profile**: an array of `EnergyResource` entries (with their topology links) plus matching `ConsumptionProfile` entries (sanctioned load, export limits, keyed by meter) for the locus, subject to the feeder / substation / licensee DID. It may conceptually reuse the `EnergyResource` / `ConsumptionProfile` structures ElectricityCredential composes, but it **does not validate as EC v1.2** (which requires a single `customerProfile` / `customerNumber`), is **not a signed EC v1.2 credential**, and has **no canonical executable example** today. It remains pending a separately governed schema / credential-subject contract — see §11.4.

## 2. What It Records / Covers

*Illustrative — describes the future per-locus aggregate profile (§1); not a validated ElectricityCredential v1.2 payload.*

| Records | Detail | Source |
|---|---|---|
| Issuing licensee & locus | The DISCOM and the network locus the record covers | ElectricityCredential v1.2 (`issuer`) |
| Distribution transformers | Those in scope, where known | ElectricityCredential v1.2 (`energyResources[]`, network equipment) |
| Energy resources behind those DTs | Solar, battery, EV charger, inverter, controllable load — with capacity, inspection status, equipment | ElectricityCredential v1.2 (`energyResources[]`) |
| Topology | Parent/sub-resource chain (PV and BESS → Inverter → Meter → DT) | ElectricityCredential v1.2 (`parentResources[]` / `subResources[]`) |
| Aggregator binding | Optional third-party aggregator enrolment | ElectricityCredential v1.2 |

**Consumer identity is omitted, and consumers are never merged.** One consumer's credential is never combined with another's: the record carries only `energyResources[]` and `consumptionProfiles[]` entries for the locus — no `customerDetails`, no customer numbers. Each consumer's own credential exists separately as the Energy Passport, held by the consumer.

That removes *direct* identifiers, not *all* linkage. `consumptionProfiles[].meterId` and each `energyResources[].id` remain resolvable to one consumer inside the licensee's systems, which is why these records sit in the authenticated tier (§1) rather than the open one.

## 3. How Each Item is Identified

Identical to [Consumer Energy Passport §3](consumer-energy-passport.md#id-3.-how-each-item-is-identified) for the executable per-consumer path. *Illustrative, future (§1):* in the illustrative per-locus aggregate, the `credentialSubject.id` would differ by scope:

| Scope | Example |
|---|---|
| Per feeder | `did:web:ies.discom.example:assets:feeder:F02` |
| Per substation | `did:web:ies.discom.example:assets:substation:SS-11KV-12` |
| Licensee-wide | `did:web:ies.discom.example` |

## 4. Definitions

See [Consumer Energy Passport §4](consumer-energy-passport.md#id-4.-definitions) for shared terms (DER, DID, VC, EnergyResource, QuantitativeValue, Net Meter, Aggregator, DISCOM).

## 5. Basis of Standards

Identical to [Consumer Energy Passport §5](consumer-energy-passport.md#id-5.-basis-of-standards): IS → CEA → IEC → IEEE; metering follows IS 16444 / IS 15959 directly; the net meter is the source of truth under CEA (Installation and Operation of Meters) Regulations, 2006.

## 6. Where Indian Standards Do Not Yet Exist

Identical to [Consumer Energy Passport §6](consumer-energy-passport.md#id-6.-where-indian-standards-do-not-yet-exist) — IEC CIM for the asset model; IEEE 1547 for DER attributes (CEA's own limits retained where set); IS 14286 (= IEC 61215) for PV module rating.

## 7. The Record

This use case produces **two records, not one** — the split the Schedules follow:

| Record | Schedule | Nature | Status |
|---|---|---|---|
| The DER asset register — what is connected, where, at what capacity | [Schedule I](#id-8.-schedule-i-static-fields-of-the-credential) | Static; changes only on commissioning, capacity change or transfer | Executable today per consumer (§8.1); the PII-free per-locus aggregate is illustrative (§8.2) |
| DER telemetry — what those resources are doing now | [Schedule II](#id-9.-schedule-ii-der-telemetry-live-record) | Live; arrives continuously | Executable today, per DER |

*Illustrative (§1).* In the future per-locus profile, each locus would be one signed Verifiable Credential per refresh cycle. Unlike the consumer-held Passport, it would be **published rather than held** — grid operators and aggregators would ingest it from the DISCOM's BPP catalogue. Open publication applies only to the open tier defined in §1; any locus record carrying resource or meter identifiers is served through the authenticated tier instead. Re-issuance would be regular (weekly for growth areas, monthly otherwise) or on material change; revocation would use the same DeDi flow as the Passport.

## 8. Schedule I — Static Fields of the Credential

Schedule I separates the executable per-consumer contract from the illustrative future aggregate. Rows in §8.1 are real ElectricityCredential v1.2 paths. Rows in §8.2 are **conceptual mappings, not normative JSON paths**: no current schema permits a PII-free multi-consumer locus subject, and no canonical aggregate example exists.

### 8.1 Executable Today — Per-consumer ElectricityCredential v1.2

| **Record Surface** | **Normative EC v1.2 Path** | **Schema Requires** | **DER Visibility Treatment** |
|---|---|---|---|
| Issuer | `issuer.id` / `issuer.name` | Both required | The DISCOM is the credential issuer |
| Consumer subject | `credentialSubject.customerProfile` | Required | One credential covers one consumer connection only |
| Customer number | `credentialSubject.customerProfile.customerNumber` | Required | Prevents this schema from representing a PII-free multi-consumer aggregate |
| Energy resources | `credentialSubject.customerProfile.energyResources[]` | Required, minimum one | Carries meters, DER, inverters and network resources; see [Passport §8.3–8.4](consumer-energy-passport.md#id-8.3-energy-resources-common-fields-every-entry-in-energyresources-any-type) |
| Topology | `energyResources[].parentResources[]` / `.subResources[]` | Optional | Links DER → inverter → meter → DT/feeder where known |
| Capacity and controls | `energyResources[].attributes` | Optional | Carries rated/import/export limits, inspection, location and aggregator enrolment |
| Connection/load context | `credentialSubject.customerProfile.consumptionProfiles[]` | Optional array; required fields apply per entry | Links tariff/load/export facts to the relevant meter |
| Consumer PII | `credentialSubject.customerDetails` | Optional | Do not disclose to a grid operator unless separately authorised |
| Executable example | [`schedule-i-example.json`](../use-cases/consumer-energy-passport/examples/schedule-i-example.json) | Validated fixture | Use for the current per-connection ingestion path |

### 8.2 Illustrative Future — PII-free Per-locus Aggregate

The following table is a design inventory for a separately governed subject contract. It deliberately does not claim validation against ElectricityCredential v1.2.

| **Conceptual Field** *(not a current schema path)* | **Expected Shape** | **Reused Building Block / Basis** | **Status and Guidance** |
|---|---|---|---|
| Locus subject | feeder, substation or licensee DID/URI | `credentialSubject.id`; IES identifier patterns | Required by the future profile; the locus replaces the consumer as subject |
| Issuing licensee | issuer DID/URI and name | EC v1.2 `issuer` | Required; issuer remains the DISCOM |
| `energyResources[]` | array of typed resources | EC v1.2 `EnergyResource` union | Required; include only resources inside the stated locus |
| `energyResources[].id` / `.type` | stable resource identifier / governed discriminator | EC v1.2 common resource fields | Required per resource |
| `energyResources[].parentResources[]` / `.subResources[]` | arrays of resource identifiers or permitted inline children | EC v1.2 topology | Use to express DER → inverter → meter → DT/feeder relationships |
| `energyResources[].attributes.ratedPower` / `.maxExport` / `.maxImport` | unit-bearing quantities | EC v1.2 common attributes | Populate where capacity is known and material to operations |
| `energyResources[].attributes.inspection` | date, result and inspector reference | EC v1.2 inspection object | Optional commissioning/status evidence |
| `energyResources[].attributes.aggregator` | id, name, controllable flag, enrolment date | EC v1.2 aggregator object | Optional; records enrolment without duplicating the resource |
| `consumptionProfiles[]` | per-meter load/tariff context | EC v1.2 `ConsumptionProfile` | Include only where sanctioned-load/export-limit context is needed |
| `consumptionProfiles[].meterId` | resource identifier | EC v1.2 meter link | Required per included consumption profile |
| `consumptionProfiles[].sanctionedLoad` / `.sanctionedExportLoad` | unit-bearing quantities | EC v1.2 load fields | Operational context, not measured telemetry |
| Consumer identity | no `customerNumber`; no `customerDetails` | Privacy boundary in §1–2 | Must be absent from the future aggregate |
| Refresh/version metadata | separately governed | No current EC v1.2 aggregate field set | Open design item; must be specified before an executable fixture is published |

## 9. Schedule II — DER Telemetry (Live Record)

Schedule II is the **live half** of DER Visibility — the time-dependent fields exchanged for this use case, as against the static asset facts in Schedule I. Where Schedule I records what is connected and how big it is, Schedule II records what it is doing now.

It is a hybrid mapping over [MeterData v0.6](../schemas/MeterData/v0.6/README.md): a native electrical subset that validates directly against the schema and its semantic validator, plus explicitly informative extensions for concepts MeterData v0.6 does not carry natively, plus out-of-band transport and security requirements. **The complete Schedule II record does not validate natively as MeterData v0.6** — only the canonical subset in §9.1 does (see §9.4).

Two things distinguish Schedule II from the rest of this use case:

- **It is executable today, per DER.** Unlike the illustrative per-locus aggregate in §8.2, the mapping below validates against a shipped schema with a canonical fixture (§9.4).
- **It arrives on a different rail.** DER telemetry travels inverter → MQTT → the national MNRE M2M platform (§9.3) — not over Beckn, and not through the [Smart Meter Data Exchange](smart-meter-data-exchange.md) path that carries net-meter readings. See §10.

**Privacy.** Per-inverter telemetry is traceable to one consumer's premises. It is *pseudonymous, not anonymous*, and belongs behind the authenticated tier described in §1 — it is never part of an openly published aggregate. See §11.3.

### 9.1 Native MeterData v0.6 Mapping — Electrical Subset

MeterData v0.6 profiles are per-meter. `meterRefs` (an `Identifier` with `scheme: "DID"`) references the metering point — here the inverter's `energyResources[].id` from Schedule I. Semantic validation (`validator.py`) applies different rules to `reportedMode: READING` descriptors (cumulative, per-timestamp values — no `openingValue`/`closingValue`, and cumulative values must not decrease across a series) versus `reportedMode: USAGE` descriptors (block-incremental values, where `closingValue - openingValue` must match the reported `value`). The canonical fixture keeps these in separate profile objects accordingly: **INSTANTANEOUS** for READING-mode snapshots, **INTERVAL** for USAGE-mode block energy.

| **DER Concept** | **Native `readingType`** | **OBIS** | **Unit** | **`reportedMode` / profile** | **Standard** *(informative)* |
|---|---|---|---|---|---|
| Voltage, R/Y/B phase | `V_R` / `V_Y` / `V_B` | 1.0.32.7.0.255 / 1.0.52.7.0.255 / 1.0.72.7.0.255 | V | READING — INSTANTANEOUS | IEC 61724-1; IEC 61850 |
| Current, R/Y/B phase | `I_R` / `I_Y` / `I_B` | 1.0.31.7.0.255 / 1.0.51.7.0.255 / 1.0.71.7.0.255 | A | READING — INSTANTANEOUS | IEC 61850 |
| Power factor (3-phase) | `PF_3P` | 1.0.13.7.0.255 | ratio (no unit code) | READING — INSTANTANEOUS | IEC 61850 |
| Frequency | `Freq` | 1.0.14.7.0.255 | Hz | READING — INSTANTANEOUS | IEEE 1547; IEC 61850 |
| Active power import | `P_Import` | 1.0.1.7.0.255 | kW | READING — INSTANTANEOUS | IEC 61724-1; IEC 61850 |
| Reactive power (lag) | `Q_Lag` | 1.0.3.7.0.255 | kvar | READING — INSTANTANEOUS | IEEE 1547; IEC 61850 |
| Apparent power | `S_Total` | 1.0.9.7.0.255 | kVA | READING — INSTANTANEOUS | IEC 61850 |
| Active energy import — cumulative | `kWh imp` | 1.0.1.8.0.255 | kWh | READING — INSTANTANEOUS | IEC 61724-1; OBIS (IS 15959) |
| Active energy export — cumulative *(accepted in lieu of a generation meter)* | `kWh exp` | 1.0.2.8.0.255 | kWh | READING — INSTANTANEOUS | IEC 61724-1; OBIS (IS 15959) |
| Active energy import — block incremental | `kWh imp block` | 1.0.1.29.0.255 | kWh | USAGE — INTERVAL | IEC 61724-1; OBIS |
| Active energy export — block incremental | `kWh exp block` | 1.0.2.29.0.255 | kWh | USAGE — INTERVAL | IEC 61724-1; OBIS |

### 9.2 Explicitly Informative Extensions (not native MeterData v0.6 fields)

| **Concept** | **Why it is informative, not native** | **Suggested treatment** |
|---|---|---|
| Harmonic distortion *(at 11 kV and above)* | `%` is not in MeterData v0.6's `UnitOfMeasure` enum | Report out-of-band, or as an unvalidated custom descriptor with no `unit` set; standard remains IEEE 519-2014 (CEA-referenced) |
| DC voltage / current / power | MeterData v0.6 has no AC/DC discriminator field; `PayloadDescriptor.category` is a free string, not a governed enum | If reported, use a custom `category` (e.g. `"dc"`) on a V/A/kW-unit descriptor — this is a convention, not a defined native concept |
| Inverter state / fault code | Status/alarm codes are not a `Reading.value` (number). Binary fault conditions partially overlap the native `AlarmProfile`/`MeterAlarm` shape (`status`: ACTIVE/CLEARED, `severity`), but a general inverter operating-state code has no native field | Use `AlarmProfile` for binary fault conditions; treat richer state codes as an extension |
| Irradiance (plane of array), module/ambient temperature | `W/m²` and `°C` are not in the `UnitOfMeasure` enum | Report out-of-band or as an unvalidated custom descriptor |
| Battery state of charge / state of health | `%` is not in the `UnitOfMeasure` enum | Report out-of-band |
| EV session ID, connector status | String values, not `Reading.value` (number). Charging power and energy delivered *are* representable as native kW/kWh readings | Session/connector metadata stays out-of-band or in Schedule I's DER/aggregator attributes |
| `m2mSimId`, `tlsCertFingerprint` (device security certificate) | No device-credential fields exist in MeterData v0.6 | Out-of-band (see §9.3) |

### 9.3 Transport and Security (out-of-band — MNRE M2M framework)

| **Requirement** | **Standard** |
|---|---|
| Transport: MQTT to the national MNRE M2M platform | MNRE M2M |
| Device identity: `m2mSimId` | MNRE M2M |
| Transport security: TLS, with device certificate fingerprint | MNRE (TLS; IEC 62443 guidance) |
| Data residency: held in India | MNRE M2M |

These are transport/security requirements on the channel carrying MeterData v0.6 payloads, not fields inside the payload itself.

### 9.4 Example and Validation

Executable canonical-subset fixture: [`schedule-ii-example.json`](../use-cases/der-visibility/examples/schedule-ii-example.json) — one `DESCRIPTOR` profile plus one `INSTANTANEOUS` and one `INTERVAL` profile, covering the §9.1 electrical subset only.

Validate structurally against MeterData v0.6:

```
python -X utf8 -B scripts/validate_schema.py schemas/MeterData/v0.6/schema.json use-cases/der-visibility/examples/schedule-ii-example.json
```

Validate semantics:

```
python -X utf8 -B schemas/MeterData/v0.6/validation/validator.py use-cases/der-visibility/examples/schedule-ii-example.json
```

This fixture exercises OBIS-to-readingType resolution against the canonical descriptor set, mode/profile matching (each `readingType`'s `reportedMode` and permitted profile shape), allowed-attribute type checks on each interval payload, interval-id monotonicity (strictly increasing `id` within a profile), and compact-sequence arity (payload count per interval matching the referenced sequence's item count). It does **not** exercise cumulative non-decrease (its `INTERVAL` profile carries USAGE-mode block-incremental values, not READING-mode cumulative ones) or opening/closing math (no reading in this fixture carries `openingValue`/`closingValue`).

## 10. How It Fits Together

*Illustrative / non-normative — describes the future aggregate profile (§1); the boxes below are not a signed EC v1.2 credential.*

```
Feeder F-02
 ├── DT F02-DT-15 ── 14 consumers ──┐
 ├── DT F02-DT-16 ── 22 consumers ──┤ aggregated into one
 └── DT F02-DT-17 ── 31 consumers ──┘ future PII-free aggregate record
                                          │  (illustrative — asset facts only, no PII)
                                          ▼
                                  Grid operator / Aggregator (BAP)
```

Each consumer's own per-consumer ElectricityCredential v1.2 (the Energy Passport) is built from the same source-of-truth (CIS / DERMS / inspection register) that would back this future aggregate — the two stay conceptually in sync because they'd read the same data and reuse the same building blocks.

### 10.1 Where each Schedule's data comes from

DER Visibility is the one IES use case fed by **more than one exchange**. The two Schedules do not share a rail, a counterparty or a security model:

| Schedule | Data | Source | Transport |
|---|---|---|---|
| I — static | Asset register: resources, topology, capacity, inspection | DISCOM's own CIS / DERMS / inspection register | Internal; surfaced per consumer as an EC v1.2 credential (§8.1) |
| I — static | Aggregator enrolment and controllability | The aggregator | Per-resource `attributes.aggregator`, written into the register |
| II — live | DER telemetry (inverter, PV, BESS) | The inverter or its gateway | MQTT → national MNRE M2M platform (§9.3) |
| II — live | Net-meter readings, where used in place of inverter data | AMISP / MDM | Beckn, via [Smart Meter Data Exchange](smart-meter-data-exchange.md) |

DER Visibility is therefore not a single-schema use case. ElectricityCredential v1.2 carries the static register; the live half arrives over two other channels entirely. The resource and meter identifiers established in Schedule I are what join them.

## 11. Points for Confirmation

1. **Refresh cadence per locus** — to be tuned per pilot, once the aggregate profile is formalised.
2. **Aggregator binding** — the exact `telemetryProvider` field and the proof an aggregator presents to claim a resource.
3. **Privacy review** — confirmation that the two-tier split proposed in §1 meets DPDP grid-side disclosure norms. Both `consumptionProfiles[].meterId` (Schedule I) and per-inverter telemetry (Schedule II) are keyed to identifiers that resolve to one consumer — pseudonymous rather than anonymous — so both sit in the authenticated tier, and only aggregate counts and capacity totals are proposed for open publication. **This is a proposal, not a settled position**, and it is the open item on which Schedule II's disclosure model depends.
4. **Aggregate record shape** — ElectricityCredential requires a single `customerProfile` with one customer number, so it cannot represent a PII-free, multi-consumer aggregate. That aggregate needs its own credential-subject shape, formalised upstream through separate governance; until then it remains an illustrative future profile with no canonical executable example.

---

## Schemas Used in This Use Case

Two schemas, one per Schedule:

**Schedule I (static) — [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md).** Executable today, issued per consumer as the [Energy Passport](consumer-energy-passport.md) — see the validated [Schedule I example](../use-cases/consumer-energy-passport/examples/schedule-i-example.json).

**Schedule II (live) — [MeterData v0.6](../schemas/MeterData/v0.6/README.md).** Executable today, per DER — see the validated [Schedule II example](../use-cases/der-visibility/examples/schedule-ii-example.json). The canonical electrical subset (§9.1) validates natively; the extensions in §9.2 and the transport requirements in §9.3 do not and are marked informative.

**Illustrative, future:** a per-locus aggregate of the Schedule I register that would conceptually reuse the `EnergyResource` and `ConsumptionProfile` structures ElectricityCredential composes. It is not itself an EC v1.2 payload and has no schema of its own yet; formalising one is tracked in §11.4.

## Value Unlock

*Illustrative, future (§1) — describes the value case for the aggregate profile once it exists; the per-consumer Energy Passport is the only path executable today.*

**Grid operator** — first-class feeder-level visibility for forecasting, planning, dispatch and outage analysis. **Aggregators** — a signed discovery surface for controllable resources; enrolment becomes mechanical. **DISCOM** — the same data backing every consumer Passport, republished once, with names and addresses never disclosed at either tier. **Regulators** — a consistent, auditable DER register across licensees.

The live half (Schedule II) is what makes forecasting and dispatch real rather than notional: the static register says a 5 kW array exists, and only telemetry says what it is generating now.

---

## Annexure A — Standards Referenced

Identical to [Consumer Energy Passport — Annexure A](consumer-energy-passport.md#annexure-a-standards-referenced).

## Annexure B — Example Payload

**Schedule I (static):** the validated [Consumer Energy Passport Schedule I example](../use-cases/consumer-energy-passport/examples/schedule-i-example.json), for the executable per-consumer path.

**Schedule II (live):** the validated [`schedule-ii-example.json`](../use-cases/der-visibility/examples/schedule-ii-example.json) — one `DESCRIPTOR` profile plus one `INSTANTANEOUS` and one `INTERVAL` profile, covering the §9.1 electrical subset. Validation commands are in §9.4.

No canonical example exists for the illustrative per-locus aggregate (§1, §11.4) — it remains a conceptual future profile pending the separately governed credential-subject contract.

## Annexure C — JSON Schema

**Schedule I:** the EC v1.2 `schema.json`, `context.jsonld` and `vocab.jsonld` referenced in [Consumer Energy Passport — Annexure C](consumer-energy-passport.md#annexure-c-json-schema) apply to the per-consumer Energy Passport credential — see §1.

**Schedule II:** MeterData v0.6 — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/schema.json), with the semantic validator at `schemas/MeterData/v0.6/validation/validator.py`.

**The illustrative future per-locus aggregate has no schema, context or vocab of its own** — it is not an EC v1.2 payload and there is nothing to validate it against yet; formalising a schema is tracked in §11.4.

## Annexure D — Derived Views

Computed downstream from the Schedules. None is a schema, a populated template, or an exchanged record — they are what a consumer of this use case builds after ingestion.

| **Operational View** | **Inputs** | **Schema Status** | **Treatment** |
|---|---|---|---|
| Connected DER inventory | Schedule I `energyResources[]` grouped by type and locus | Derived | Count and capacity totals are computed from the source records; this is the open tier of §1 |
| DER growth over time | successive inventory snapshots | Derived | Compare versioned snapshots; do not present one credential as a time series |
| Feeder/DT loading study | Schedule I topology and sanctioned load/export limits, joined to Schedule II telemetry | Derived | Static facts do not substitute for measured load profiles |
| Controllability register | per-resource aggregator and controllable attributes | Derived | Preserve the underlying resource identifier and enrolment evidence |
| Exception list | missing topology, inspection or capacity fields | Derived | Report absence as an evidence gap, not as zero capacity |
| Future signed aggregate | conceptual §8.2 record | **Not currently executable** | Requires an approved schema/credential-subject contract and canonical fixture before publication |
