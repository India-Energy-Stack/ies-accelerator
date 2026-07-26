# DER Visibility

*A DISCOM's future, illustrative per-feeder view of every distributed energy resource behind its meters — PII-free, conceptually reusing the same `EnergyResource` and `ConsumptionProfile` building blocks that the consumer's [Energy Passport](consumer-energy-passport.md) ([ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)) composes. The only currently executable EC v1.2 path is the per-consumer Energy Passport itself — see §1.*

**[Implementation Guide →](../use-cases/der-visibility/README.md)**

| Field | Value |
|---|---|
| Document | IES/DERV-PROFILE/1.2 |
| Status | Piloted — see [Status](../STATUS.md) |
| Applicability | All distribution licensees |
| This version | Executable today: the per-consumer ElectricityCredential v1.2 (Energy Passport). Illustrative, future: a grid-side, PII-free per-locus profile conceptually reusing `energyResources[]` + `consumptionProfiles[]` (the building blocks of ElectricityCredential v1.2), with the network locus — not a consumer — as subject; see §1. |

---

## 1. Scope and Purpose

The stakeholders are the DISCOM (issuer), its grid operator, and any aggregator enrolling controllable resources. As rooftop solar, batteries and EV charging spread, the licensee often can't answer: what's connected on feeder F-02, at what capacity, and is it controllable?

This document defines **DER Visibility** — a DISCOM's aggregated view of one feeder, substation, or the whole licensee, for grid operators and aggregators to ingest directly, with **no consumer PII**.

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

*Illustrative (§1).* In this future profile, each locus would be one signed Verifiable Credential per refresh cycle. Unlike the consumer-held Passport, it would be **published, not held** — grid operators and aggregators would ingest it from the DISCOM's BPP catalogue. Re-issuance would be regular (weekly for growth areas, monthly otherwise) or on material change; revocation would use the same DeDi flow as the Passport.

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

## 9. Schedule II

Schedule II contains downstream operational views, not a separate schema or populated template.

| **Operational View** | **Schedule I Inputs** | **Schema Status** | **Treatment** |
|---|---|---|---|
| Connected DER inventory | `energyResources[]` grouped by type and locus | Derived | Count and capacity totals are computed from the source records |
| DER growth over time | successive inventory snapshots | Derived | Compare versioned snapshots; do not present one credential as a time series |
| Feeder/DT loading study | resource topology, sanctioned load/export limits, separately obtained MeterData telemetry | Derived | Static Schedule I facts do not substitute for measured load profiles |
| Controllability register | per-resource aggregator and controllable attributes | Derived | Preserve the underlying resource identifier and enrolment evidence |
| Exception list | missing topology, inspection or capacity fields | Derived | Report absence as an evidence gap, not as zero capacity |
| Future signed aggregate | conceptual §8.2 record | **Not currently executable** | Requires an approved schema/credential-subject contract and canonical fixture before publication |

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

## 11. Points for Confirmation

1. **Refresh cadence per locus** — to be tuned per pilot, once the aggregate profile is formalised.
2. **Aggregator binding** — the exact `telemetryProvider` field and the proof an aggregator presents to claim a resource.
3. **Privacy review** — confirmation the aggregated, PII-free issuance meets DPDP grid-side disclosure norms. `consumptionProfiles[]` entries are keyed by meter id — pseudonymous rather than anonymous — so their inclusion belongs behind the authenticated tier where required.
4. **Aggregate record shape** — ElectricityCredential requires a single `customerProfile` with one customer number, so it cannot represent a PII-free, multi-consumer aggregate. That aggregate needs its own credential-subject shape, formalised upstream through separate governance; until then it remains an illustrative future profile with no canonical executable example.

---

## Schemas Used in This Use Case

**Executable today:** **[ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)**, issued per consumer as the [Energy Passport](consumer-energy-passport.md) — see the validated [Schedule I example](../use-cases/consumer-energy-passport/examples/schedule-i-example.json).

**Illustrative, future:** a PII-free, per-locus aggregate that would conceptually reuse the `EnergyResource` and `ConsumptionProfile` structures ElectricityCredential composes. It is not itself an EC v1.2 payload and has no schema of its own yet; formalising one is tracked in §11.4.

## Value Unlock

*Illustrative, future (§1) — describes the value case for the aggregate profile once it exists; the per-consumer Energy Passport is the only path executable today.*

**Grid operator** — first-class feeder-level visibility for forecasting, planning, dispatch and outage analysis. **Aggregators** — a signed discovery surface for controllable resources; enrolment becomes mechanical. **DISCOM** — the same data backing every consumer Passport, republished once, with no PII disclosure burden. **Regulators** — a consistent, auditable DER register across licensees.

---

## Annexure A — Standards Referenced

Identical to [Consumer Energy Passport — Annexure A](consumer-energy-passport.md#annexure-a-standards-referenced).

## Annexure B — Example Payload

For the executable per-consumer path, see the validated [Consumer Energy Passport Schedule I example](../use-cases/consumer-energy-passport/examples/schedule-i-example.json). No canonical example exists for the illustrative per-locus aggregate (§1, §11.4) — it remains a conceptual future profile pending the separately governed credential-subject contract.

## Annexure C — JSON Schema

**Executable today (per-consumer path only):** the EC v1.2 `schema.json`, `context.jsonld` and `vocab.jsonld` referenced in [Consumer Energy Passport — Annexure C](consumer-energy-passport.md#annexure-c-json-schema) apply to the per-consumer Energy Passport credential — see §1. **The illustrative future per-locus aggregate has no schema, context or vocab of its own** — it is not an EC v1.2 payload and there is nothing to validate it against yet; formalising a schema is tracked in §11.4.
