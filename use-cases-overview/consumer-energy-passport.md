# Consumer Energy Passport

*The IES [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2), issued holder-bound to a consumer's wallet (W3C Verifiable Credential).*

**[Implementation Guide →](../use-cases/consumer-energy-passport/README.md)**

| Field | Value |
|---|---|
| Document | IES/CEP-PROFILE/1.2 |
| Status | Live in pilot (four pilot DISCOMs; one staged) |
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

## 8. Schedule I — Static Fields of the Credential

| Reference | What it covers |
|---|---|
| [ElectricityCredential v1.2 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2#field-reference) | Eight tables: envelope, `CustomerDetails`, `CustomerProfile`, the typed `EnergyResource*` kinds (METER, GENERATOR, STORAGE, EV_CHARGER, INVERTER, LOAD, NETWORK), and `ConsumptionProfile`. Each row: `Field`, `Type`, standard(s) **Based on**, `Status` (Mandatory / Optional). |

## 9. Schedule II

| Wrapping / dependency | Detail |
|---|---|
| Not applicable | The Passport is self-contained. The one interdependency is the live [MeterData](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) record, which references this credential's meter/asset identifiers but is a separate exchange, not a populated report. |

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

A single schema — **[ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)** (W3C VC). No additional schemas. Live readings use [MeterData](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) separately — see [Consumer Meter Digest](consumer-meter-digest.md).

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
