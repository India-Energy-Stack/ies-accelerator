# DER Visibility

A DISCOM publishes a **per-feeder view of every distributed energy resource** (rooftop solar, battery, EV charger) behind its meters — PII-free, built from the same `EnergyResource` and `ConsumptionProfile` building blocks that the consumer's [Energy Passport](../consumer-energy-passport/README.md) ([ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)) composes.

| | |
|---|---|
| **Document** | IES/DERV-PROFILE/1.2 |
| **Status** | Live in pilot |
| **Applicability** | All distribution licensees |
| **This version** | DER Visibility — a grid-side, PII-free publication of `energyResources[]` + `consumptionProfiles[]` arrays (the building blocks of [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)), issued per feeder / substation / licensee with the network locus — not a consumer — as subject. |

---

## 1. Scope and Purpose

The **stakeholders** are the DISCOM (issuer), its **grid operator** (forecasting, planning, dispatch), and any **aggregator** that wants to enrol controllable resources for demand response or flexibility. As rooftop solar, batteries and EV charging spread, the licensee often cannot answer the basic question: **what is connected on feeder F-02, at what capacity, where on the network, and is it controllable?**

This document defines **DER Visibility** — the DISCOM publishes a signed, aggregated view of one feeder, one substation, or the whole licensee. Grid operators and aggregators ingest it directly. The record **does not contain consumer PII** — only the asset facts the grid needs.

**A note on the schema.** ElectricityCredential is issued per consumer connection — its subject is one `customerProfile` with one customer number — so it **cannot combine multiple consumers' credentials** into a feeder- or substation-level record. Each consumer keeps their own credential (the Energy Passport). For grid visibility, remove the PII and publish simply an **array of `EnergyResource` entries** (with their topology links) plus the matching **`ConsumptionProfile` entries** (sanctioned load, export limits, keyed by meter) for the locus — the same building blocks ElectricityCredential composes, signed with the feeder / substation / licensee DID as subject. No new field definitions are needed.

## 2. What It Records / Covers

For one network locus (feeder, substation, licensee-wide) the record carries:

- the **issuing licensee** and the **network locus** it covers;
- the list of **distribution transformers** in scope (where known);
- each **energy resource** behind those DTs — solar, battery, EV charger, inverter, controllable load — with capacity, inspection status, equipment details (make / model), and the meter it sits behind;
- the **parent / sub-resource topology** — PV and BESS → Inverter → Meter → DT;
- optionally, an **aggregator binding** (`telemetryProvider`) where a resource is enrolled with a flexibility aggregator.

**Consumer identity is omitted, and consumers are never merged.** One consumer's credential is never combined with another's: the DER Visibility record carries only `energyResources[]` and `consumptionProfiles[]` entries for the locus — no `customerDetails`, no customer numbers. Each consumer's own credential exists separately as the Energy Passport, held by the consumer.

## 3. How Each Item is Identified

Identical identifier scheme to **[Consumer Energy Passport §3](../consumer-energy-passport/README.md#id-3.-how-each-item-is-identified)** — `did:web` for the licensee and assets; bare licensee codes for existing asset numbers; DeDi only for subscriber registries and credential revocation.

The `credentialSubject.id` differs by issuance scope:

| Scope | `credentialSubject.id` example |
|---|---|
| Per feeder | `did:web:ies.discom.example:assets:feeder:F02` |
| Per substation | `did:web:ies.discom.example:assets:substation:SS-11KV-12` |
| Licensee-wide | `did:web:ies.discom.example` |

## 4. Definitions

See **[Consumer Energy Passport §4](../consumer-energy-passport/README.md#id-4.-definitions)** for shared terms (DER, DID, VC, EnergyResource, QuantitativeValue, Net Meter, Aggregator, DISCOM).

## 5. Basis of Standards

Identical to **[Consumer Energy Passport §5](../consumer-energy-passport/README.md#id-5.-basis-of-standards)**. IS → CEA → IEC → IEEE precedence; metering follows IS 16444 / IS 15959 directly; net meter is the source of truth under CEA (Installation and Operation of Meters) Regulations, 2006.

## 6. Where Indian Standards Do Not Yet Exist

Identical to **[Consumer Energy Passport §6](../consumer-energy-passport/README.md#id-6.-where-indian-standards-do-not-yet-exist)** — IEC CIM is used for the asset data model; IEEE 1547 for DER electrical attributes (with CEA's own limits retained where CEA sets them); IS 14286 (= IEC 61215) for PV module rating.

## 7. The Record

DER Visibility produces **one signed Verifiable Credential** per locus per refresh cycle. Unlike the consumer-held Passport, the DER Visibility credential is **published, not held** — the grid operator and aggregator ingest it from the DISCOM's BPP catalogue.

Re-issuance is on a regular cadence (typical: weekly for an active growth area, monthly otherwise) or on material change (new DER commissioned, capacity revised, equipment swapped). Old credentials are revoked through the same DeDi revocation flow as the Passport.

## 8. Schedule I — Static Fields of the Credential

Identical to **[Consumer Energy Passport §8](../consumer-energy-passport/README.md#id-8.-schedule-i-static-fields-of-the-credential)**:

→ **[ElectricityCredential v1.2 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2#field-reference)**

DER Visibility publishes `energyResources[]` (typed entries: GENERATOR, STORAGE, EV_CHARGER, INVERTER, LOAD, NETWORK, METER) with the parent / sub-resource links (`parentResources` / `subResources`), plus `consumptionProfiles[]` where sanctioned-load / export-limit context is needed. No `customerDetails`, no customer numbers.

## 9. Schedule II

Not applicable. The DER Visibility credential is the report.

A typical downstream **rate-of-DER-growth report** or **feeder-loading study** is computed by the grid operator from a time series of DER Visibility credentials, not a separate IES schema.

## 10. How It Fits Together

```
Feeder F-02
 ├── DT F02-DT-15  ── 14 consumers ──┐
 │                                   │ aggregated into one
 ├── DT F02-DT-16  ── 22 consumers ──┤ ElectricityCredential v1.2
 │                                   │ (DER Visibility issuance —
 └── DT F02-DT-17  ── 31 consumers ──┘  asset facts only, no PII)
                                          │
                                          ▼
                                  Grid operator / Aggregator
                                  (BAP — consumes the credential
                                   from the DISCOM's BPP catalogue)
```

The credential is built from the same source-of-truth as the consumer Passport (the DISCOM's CIS / DERMS / inspection register). The two issuances stay in sync because they read the same data and use the same schema.

## 11. Points for Confirmation

1. **Refresh cadence per locus** — weekly vs monthly vs on-material-change — to be tuned per pilot.
2. **Aggregator binding** — exact field for `telemetryProvider` and the credential proof an aggregator presents to claim a resource.
3. **Privacy review** — confirmation that the aggregated, PII-free issuance meets DPDP grid-side disclosure norms. Note `consumptionProfiles[]` entries are keyed by meter id — pseudonymous rather than anonymous — so their inclusion belongs behind the authenticated tier where required.
4. **Aggregate record shape** — ElectricityCredential requires a single `customerProfile` with one customer number, so the PII-free aggregate view (`energyResources[]` + `consumptionProfiles[]` arrays with a network-locus subject) needs its own credential-subject shape to be formalised upstream; until then this guide profiles it per locus.

---

## Schemas Used in This Use Case

The building blocks of **[ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)** — the `EnergyResource` and `ConsumptionProfile` schemas it composes — published as PII-free arrays per locus. No new field definitions are needed; each consumer's full credential remains their own Energy Passport.

## Value Unlock

**For the grid operator** — first-class visibility into what's behind every feeder. Forecasting, planning, dispatch and outage analysis all gain a clean input.

**For aggregators** — a discovery surface for controllable resources, signed by the DISCOM. Enrolment becomes mechanical.

**For the DISCOM** — the same data that backs every consumer Passport is republished once for grid use. No duplicate data system; no consent burden (no PII in scope).

**For regulators** — a consistent, auditable DER asset register across licensees.

---

## Setup: Register → Discover → Exchange

Built on the four implementation steps in **[How you implement IES](../../how-you-implement-ies/README.md)**. Use-case-specific items only below.

### Register — identity reused

- [ ] [Identity setup](../../how-you-implement-ies/setup-register.md) complete (same `did:web` as the Energy Passport)
- [ ] Feeder / substation identifier convention confirmed (existing IDs wrapped in `did:web`)

### Discover — grid-side catalogue

- [ ] [Discovery setup](../../how-you-implement-ies/setup-discovery-exchange.md) complete
- [ ] BPP catalogue entries published per locus (feeder / substation / licensee-wide) — `accessMethod: INLINE`
- [ ] Grid-operator and aggregator consumers tested as BAPs

### Exchange — issuance shape

- [ ] [Adapter built](../../how-you-implement-ies/build-adapter.md) for the grid-side issuance shape (PII-free `energyResources[]` + `consumptionProfiles[]` arrays)
- [ ] PII excluded at issuance time — no `customerDetails`, no customer numbers; one consumer's data never merged with another's credential
- [ ] `energyResources[]` populated from CIS / DERMS / inspection register
- [ ] `consumptionProfiles[]` included only where sanctioned-load / export-limit context is needed
- [ ] Topology links (`parentResources`, `subResources`) populated where the DT mapping is known
- [ ] Schema validation passes against [ElectricityCredential v1.2 schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json)
- [ ] Refresh cadence agreed and scheduled
- [ ] Revocation tested

### Team

- [ ] Network / planning SPOC
- [ ] IT SPOC
- [ ] Inspection / commissioning SPOC

---

## Dev kits and code

- **Schema source** — [`schemas/ElectricityCredential/v1.2/attributes.yaml`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/attributes.yaml)
- **JSON Schema** — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json)
- **Example payloads** — [`examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ElectricityCredential/v1.2/examples) (start from `example.json`; blank `customerProfile` / `customerDetails` for the DER Visibility issuance shape)
- **Validation** — `python3 scripts/validate_schema.py schemas/ElectricityCredential/v1.2/schema.json <your-output.json>`

---

## Annexure A — Standards Referenced

Identical to **[Consumer Energy Passport — Annexure A](../consumer-energy-passport/README.md#annexure-a-standards-referenced)**.

## Annexure B — Example Payload

The canonical example is a per-feeder payload carrying the `energyResources[]` (and, where needed, `consumptionProfiles[]`) entries drawn from the Passport `example.json`, with all PII removed and the subject set to a feeder DID.

## Annexure C — JSON Schema

Identical to **[Consumer Energy Passport — Annexure C](../consumer-energy-passport/README.md#annexure-c-json-schema)** — same `schema.json`, same `context.jsonld`, same `vocab.jsonld`.
