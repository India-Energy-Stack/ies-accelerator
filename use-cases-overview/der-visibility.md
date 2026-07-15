# DER Visibility

*A DISCOM publishes a per-feeder view of every distributed energy resource behind its meters — PII-free, built from the same `EnergyResource` and `ConsumptionProfile` building blocks that the consumer's [Energy Passport](consumer-energy-passport.md) ([ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)) composes.*

**[Implementation Guide →](../use-cases/der-visibility/README.md)**

| Field | Value |
|---|---|
| Document | IES/DERV-PROFILE/1.2 |
| Status | Live in pilot |
| Applicability | All distribution licensees |
| This version | A grid-side, PII-free publication of `energyResources[]` + `consumptionProfiles[]` arrays (the building blocks of ElectricityCredential v1.2), issued per feeder / substation / licensee with the network locus — not a consumer — as subject. |

---

## 1. Scope and Purpose

The stakeholders are the DISCOM (issuer), its grid operator, and any aggregator enrolling controllable resources. As rooftop solar, batteries and EV charging spread, the licensee often can't answer: what's connected on feeder F-02, at what capacity, and is it controllable?

This document defines **DER Visibility** — the DISCOM publishes a signed, aggregated view of one feeder, substation, or the whole licensee. Grid operators and aggregators ingest it directly. **No consumer PII.**

**A note on the schema.** ElectricityCredential is issued per consumer connection — its subject is one `customerProfile` with one customer number — so it **cannot combine multiple consumers' credentials** into a feeder- or substation-level record. Each consumer keeps their own credential (the Energy Passport). For grid visibility, remove the PII and publish simply an **array of `EnergyResource` entries** (with their topology links) plus the matching **`ConsumptionProfile` entries** (sanctioned load, export limits, keyed by meter) for the locus — the same building blocks ElectricityCredential composes, signed with the feeder / substation / licensee DID as subject. No new field definitions are needed.

## 2. What It Records / Covers

- the issuing licensee and network locus it covers;
- distribution transformers in scope, where known;
- each energy resource behind those DTs — solar, battery, EV charger, inverter, controllable load — with capacity, inspection status, equipment;
- parent/sub-resource topology (PV and BESS → Inverter → Meter → DT);
- optionally, an aggregator binding.

**Consumer identity is omitted, and consumers are never merged.** One consumer's credential is never combined with another's: the record carries only `energyResources[]` and `consumptionProfiles[]` entries for the locus — no `customerDetails`, no customer numbers. Each consumer's own credential exists separately as the Energy Passport, held by the consumer.

## 3. How Each Item is Identified

Identical to [Consumer Energy Passport §3](consumer-energy-passport.md#id-3.-how-each-item-is-identified). The `credentialSubject.id` differs by scope:

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

One signed Verifiable Credential per locus per refresh cycle. Unlike the consumer-held Passport, this credential is **published, not held** — grid operators and aggregators ingest it from the DISCOM's BPP catalogue. Re-issuance is regular (weekly for growth areas, monthly otherwise) or on material change; old credentials revoke through the same DeDi flow as the Passport.

## 8. Schedule I — Static Fields of the Credential

Identical to [Consumer Energy Passport §8](consumer-energy-passport.md#id-8.-schedule-i-static-fields-of-the-credential) — → **[ElectricityCredential v1.2 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2#field-reference)**. DER Visibility publishes `energyResources[]` (GENERATOR, STORAGE, EV_CHARGER, INVERTER, LOAD, NETWORK, METER) with the parent / sub-resource links, plus `consumptionProfiles[]` where sanctioned-load / export-limit context is needed. No `customerDetails`, no customer numbers.

## 9. Schedule II

Not applicable. The record is the report — a typical rate-of-DER-growth report or feeder-loading study is computed by the grid operator from a time series of these records, not a separate schema.

## 10. How It Fits Together

```
Feeder F-02
 ├── DT F02-DT-15 ── 14 consumers ──┐
 ├── DT F02-DT-16 ── 22 consumers ──┤ aggregated into one
 └── DT F02-DT-17 ── 31 consumers ──┘ ElectricityCredential v1.2
                                          │  (DER Visibility — asset facts only, no PII)
                                          ▼
                                  Grid operator / Aggregator (BAP)
```

Built from the same source-of-truth as the consumer Passport (CIS / DERMS / inspection register) — the two issuances stay in sync because they read the same data and use the same building blocks.

## 11. Points for Confirmation

1. **Refresh cadence per locus** — to be tuned per pilot.
2. **Aggregator binding** — the exact `telemetryProvider` field and the proof an aggregator presents to claim a resource.
3. **Privacy review** — confirmation the aggregated, PII-free issuance meets DPDP grid-side disclosure norms. `consumptionProfiles[]` entries are keyed by meter id — pseudonymous rather than anonymous — so their inclusion belongs behind the authenticated tier where required.
4. **Aggregate record shape** — ElectricityCredential requires a single `customerProfile` with one customer number, so the PII-free aggregate view needs its own credential-subject shape to be formalised upstream; until then this guide profiles it per locus.

---

## Schemas Used in This Use Case

The building blocks of **[ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)** — the `EnergyResource` and `ConsumptionProfile` schemas it composes — published as PII-free arrays per locus. No new field definitions are needed; each consumer's full credential remains their own Energy Passport.

## Value Unlock

**Grid operator** — first-class feeder-level visibility for forecasting, planning, dispatch and outage analysis. **Aggregators** — a signed discovery surface for controllable resources; enrolment becomes mechanical. **DISCOM** — the same data backing every consumer Passport, republished once, with no PII disclosure burden. **Regulators** — a consistent, auditable DER register across licensees.

---

## Annexure A — Standards Referenced

Identical to [Consumer Energy Passport — Annexure A](consumer-energy-passport.md#annexure-a-standards-referenced).

## Annexure B — Example Payload

The canonical example is a per-feeder payload carrying the `energyResources[]` (and, where needed, `consumptionProfiles[]`) entries drawn from the Passport `example.json`, with all PII removed and the subject set to a feeder DID.

## Annexure C — JSON Schema

Identical to [Consumer Energy Passport — Annexure C](consumer-energy-passport.md#annexure-c-json-schema) — same `schema.json`, `context.jsonld`, `vocab.jsonld`.
