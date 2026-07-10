# DER Visibility

*A DISCOM publishes a per-feeder view of every distributed energy resource behind its meters — the same [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) the consumer's [Energy Passport](consumer-energy-passport.md) is built on, aggregated and re-published for grid-side consumers.*

**[Implementation Guide →](../use-cases/der-visibility/README.md)**

| Field | Value |
|---|---|
| Document | IES/DERV-PROFILE/1.2 |
| Status | Live in pilot |
| Applicability | All distribution licensees |
| This version | A *grid-side issuance* of ElectricityCredential v1.2. Same schema as the Energy Passport; different audience and `credentialSubject` (feeder / substation / licensee, not the consumer). |

---

## 1. Scope and Purpose

The stakeholders are the DISCOM (issuer), its grid operator, and any aggregator enrolling controllable resources. As rooftop solar, batteries and EV charging spread, the licensee often can't answer: what's connected on feeder F-02, at what capacity, and is it controllable?

This document defines **DER Visibility** — the DISCOM publishes the aggregated `energyResources[]` view of one feeder, substation, or the whole licensee, as a signed credential grid operators and aggregators ingest directly. **No consumer PII.** Not a new schema — a different issuance of ElectricityCredential v1.2.

## 2. What It Records / Covers

- the issuing licensee and network locus it covers;
- distribution transformers in scope, where known;
- each energy resource behind those DTs — solar, battery, EV charger, inverter, controllable load — with capacity, inspection status, equipment;
- parent/sub-resource topology (PV and BESS → Inverter → Meter → DT);
- optionally, an aggregator binding.

**Consumer identity is omitted** — `customerProfile` and `customerDetails` are blank. The consumer credential exists separately as the Energy Passport, held by the consumer.

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

Identical to [Consumer Energy Passport §8](consumer-energy-passport.md#id-8.-schedule-i-static-fields-of-the-credential) — → **[ElectricityCredential v1.2 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2#field-reference)**. DER Visibility populates `energyResources[]` (GENERATOR, STORAGE, EV_CHARGER, INVERTER, LOAD, NETWORK, METER) and topology links; `customerProfile` / `customerDetails` are omitted.

## 9. Schedule II

Not applicable — the credential is the report. A typical rate-of-DER-growth report or feeder-loading study is computed by the grid operator from a time series of these credentials, not a separate schema.

## 10. How It Fits Together

```
Feeder F-02
 ├── DT F02-DT-15 ── 14 consumers ──┐
 ├── DT F02-DT-16 ── 22 consumers ──┤ aggregated into one ElectricityCredential v1.2
 └── DT F02-DT-17 ── 31 consumers ──┘ (DER Visibility — asset facts only, no PII)
                                          │
                                          ▼
                                  Grid operator / Aggregator (BAP)
```

Built from the same source-of-truth as the consumer Passport (CIS / DERMS / inspection register) — the two issuances stay in sync because they read the same data and use the same schema.

## 11. Points for Confirmation

1. **Refresh cadence per locus** — to be tuned per pilot.
2. **Aggregator binding** — the exact `telemetryProvider` field and the proof an aggregator presents to claim a resource.
3. **Privacy review** — confirmation the aggregated, PII-free issuance meets DPDP grid-side disclosure norms.

---

## Schemas Used in This Use Case

A single schema — **[ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)**. DER Visibility is a grid-side issuance pattern; no separate schema.

## Value Unlock

**Grid operator** — first-class feeder-level visibility for forecasting, planning, dispatch and outage analysis. **Aggregators** — a signed discovery surface for controllable resources; enrolment becomes mechanical. **DISCOM** — the same data backing every consumer Passport, republished once, with no PII disclosure burden. **Regulators** — a consistent, auditable DER register across licensees.

---

## Annexure A — Standards Referenced

Identical to [Consumer Energy Passport — Annexure A](consumer-energy-passport.md#annexure-a-standards-referenced).

## Annexure B — Example Payload

The Passport `example.json` with `customerProfile` / `customerDetails` blanked and the subject set to a feeder DID.

## Annexure C — JSON Schema

Identical to [Consumer Energy Passport — Annexure C](consumer-energy-passport.md#annexure-c-json-schema) — same `schema.json`, `context.jsonld`, `vocab.jsonld`.
