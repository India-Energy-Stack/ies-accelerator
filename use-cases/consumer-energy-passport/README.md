# Consumer Energy Passport

The IES **[ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md)**, issued holder-bound to a consumer's wallet (W3C Verifiable Credential).

| | |
|---|---|
| **Document** | IES/CEP-PROFILE/1.2 |
| **Status** | Live in pilot (four pilot DISCOMs across four States; one DISCOM staged) |
| **Applicability** | All distribution licensees |
| **This version** | Consumer Energy Passport *variant* of [ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md). Static credential only; live interval data uses **[MeterData](../../schemas/MeterData/v0.6/README.md)**, separately. |

---

## 1. Scope and Purpose

The **stakeholder** is the distribution licensee (DISCOM) and the consumer it serves. As rooftop solar, batteries and EV charging grow behind consumers' meters, the licensee often **cannot see** what is connected, at what capacity, or where on the network it sits; and the consumer **cannot easily prove** their connection and assets to a bank, subsidy portal or marketplace without a manual letter from the DISCOM.

This document defines the **Consumer Energy Passport** — the holder-bound issuance of the IES ElectricityCredential v1.2, a W3C Verifiable Credential carrying the static facts of a consumer's connection and the energy resources behind their meter.

It does **not** define a new schema. ElectricityCredential v1.2 is the schema (authoritative, IES-hosted); the Passport profiles how that one credential is **shaped**, **issued** and **delivered** when the consumer is the audience (`credentialSubject.id` = wallet DID; `customerProfile.idRef` = a government-ID reference).

## 2. What It Records / Covers

For one consumer connection the Passport records:

- the **consumer** and the **issuing licensee**;
- the **service connection**, its tariff category and its sanctioned load;
- the **net meter**, and a generation meter where the licensee uses one;
- the **distribution transformer** the connection is fed from, where known;
- each **energy resource** behind the meter — solar, battery, EV charger, inverter or controllable load — with its capacity, inspection status and equipment details.

The Passport records identity, capacity and status. **It does not hold live readings** — those are the [MeterData](../../schemas/MeterData/v0.6/README.md) record, covered separately and linked by asset identifier (see the [Consumer Meter Digest](../consumer-meter-digest/README.md)).

## 3. How Each Item is Identified

Every item — the consumer, the connection, each meter, each asset — carries a verifiable digital identifier (a [DID](../../glossary.md#did)). Existing licensee numbers are reused as aliases inside the identifiers; the licensee keeps its numbering.

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (issuer) | `did:web` on owned domain | `did:web:ies.discom.example` |
| Regulator | `did:web` on owned domain | `did:web:ies.serc.example` |
| Consumer (holder) | `did:key` (wallet) or `tel:` URI | `did:key:z6MkjVQ8r4f3rPuY…` |
| Meter / inverter / DER / transformer | `did:web` under the issuer domain, with path | `did:web:ies.discom.example:assets:meter:NM-44091234` |
| Existing CIS consumer number | Plain string, kept verbatim | `1102004567` → `customerProfile.customerNumber` |

[DeDi](../../glossary.md#dedi) is used only for the Beckn subscriber registries and the credential revocation registry (`credentialStatus`) — **not** as an identifier method for consumers, meters or assets. Serial numbers and asset codes ride inside the signed credential as attributes.

## 4. Definitions

- **DER** (Distributed Energy Resource) — any device behind a consumer's meter that generates electricity (solar, wind), stores it (a battery), or consumes it in a controllable way (an EV charger).
- **DID** (Decentralised Identifier) — the verifiable digital identifier described in Section 3 (W3C DID Core).
- **Verifiable Credential (VC)** — a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback.
- **Energy Resource** — any physical asset in the credential — meter, inverter, DER, transformer or controllable load — represented as one typed entry in `energyResources[]`.
- **QuantitativeValue** — a `{value, unit}` pair used for every power, energy and capacity figure (units mapped to QUDT in the JSON-LD context).
- **Holder-bound** — issued to a specific holder's wallet (`credentialSubject.id` = wallet DID), as opposed to a bearer credential.
- **Net Meter** — the bidirectional billing meter; the billing source of truth and the point at which any control instruction is applied.
- **Aggregator** — a third party that enrols controllable resources for demand response or flexibility.
- **DISCOM / Distribution Licensee** — the licensee that issues and maintains the Passport.

## 5. Basis of Standards

The IES order of preference is fixed. Where more than one standard could apply, use, in order:

1. **Bureau of Indian Standards (IS)**
2. **CEA Regulations** and the **Indian Electricity Grid Code (IEGC)**
3. **International Electrotechnical Commission (IEC)** — the Common Information Model (IEC 61968 distribution, IEC 61970 transmission/DER) provides the data model
4. **Institute of Electrical and Electronics Engineers (IEEE)**

The **Standard** column in the schema's field tables lists references in this order; the same order is recorded as the `x-standards-precedence` map at the root of the JSON Schema.

Metering follows Indian standards directly: **IS 16444** (AC smart meter specification) and **IS 15959** (DLMS/COSEM companion specification; OBIS codes). The net meter is the billing source of truth under the **CEA (Installation and Operation of Meters) Regulations, 2006**.

## 6. Where Indian Standards Do Not Yet Exist

Three areas where no Indian standard applies and an international one is used:

- **A data model for grid assets** — IEC Common Information Model (IEC 61970-301, IEC 61968-11) is used for structure; it underlies the `energyResources[]` kinds.
- **DER electrical attributes** — IEEE 1547-2018 (interconnection and interoperability: ride-through, anti-islanding, volt-var, frequency-watt). **CEA's own limits are retained where CEA sets them** (harmonics per IEEE 519-2014; DC injection limited to 0.5% of rated output under the CEA Connectivity Regs 2013, am. 2019).
- **PV module rating** — DC array capacity (kWp) is a module/array quantity governed by **IS 14286** (= IEC 61215, module design qualification).

## 7. The Record

The Passport defines **one record**: a static Verifiable Credential. It changes only when an asset is commissioned, capacity is added, or ownership transfers; the licensee issues it after inspection. A material change is handled by revoking and re-issuing, with status published to the DeDi revocation registry.

It is **holder-bound**. The consumer holds it in DigiLocker or a DID wallet and discloses fields selectively; verifiers check it offline against the licensee's published `did.json`.

The live interval data (generation and consumption readings) is a **separate record** — the [MeterData](../../schemas/MeterData/v0.6/README.md) schema, exchanged over Beckn Data Exchange — linked to this credential by the meter and asset identifiers.

## 8. Schedule I — Static Fields of the Credential

The full, authoritative field tables (envelope, `customerProfile`, `customerDetails`, `energyResources[]` for each kind, `consumptionProfiles[]`) are in the schema:

→ **[ElectricityCredential v1.2 — Field reference](../../schemas/ElectricityCredential/v1.2/README.md#field-reference)**

Eight tables in all: envelope, `CustomerDetails`, `CustomerProfile`, the typed `EnergyResource*` kinds (METER, GENERATOR, STORAGE, EV_CHARGER, INVERTER, LOAD, NETWORK), and `ConsumptionProfile`. Each row carries `Field`, `Type`, the standard(s) it is **Based on**, and `Status` (Mandatory / Optional).

## 9. Schedule II

Not applicable as a populated report template. The Passport is a single self-contained credential; it does not pull fields into a downstream reporting template.

The one interdependent schema is the live [MeterData](../../schemas/MeterData/v0.6/README.md) record: it references the meter and asset identifiers registered here (so it depends on this credential), but it is a separate data-exchange schema carried over Beckn, not a Schedule II report populated from this credential.

## 10. How It Fits Together

```
                      ┌── Solar array
                      │
Grid ──[ Net Meter ]──┼── (Generation Meter *) ── Inverter ** ──┬── Solar array
   (billing meter,    │                                          └── Battery
    two-way, the      └── Inverter ** ── EV charger
    source of truth)
  *  Generation meter is used by some licensees, not others.
  ** One inverter may serve more than one asset.
  Topology is carried by parentResources / subResources:
  PV and BESS → Inverter → Meter → DT.
```

The net meter is the billing source of truth. Generation is measured at the net meter, at a generation meter where one is used, or by the inverter's own live data (the MeterData record). All physical assets live in one `energyResources[]` array, typed and linked by parent/child references; the credential carries identity and ratings, the MeterData record carries the live readings.

## 11. Points for Confirmation

1. **Holder-binding method** for the Passport (DigiLocker Aadhaar pull / offline-KYC XML / in-person), to be documented for privacy review.
2. **Selective-disclosure profile** with first verifiers (SD-JWT-VC typical), so `customerDetails` PII is disclosed field-by-field by the wallet.
3. **Re-issuance triggers** on material change (meter swap, sanctioned-load change, DER commissioning) and the revocation flow into the DeDi registry.
4. **Schema-host provenance.** The credential context is served from `india-energy-stack.github.io/ies-accelerator`. A custom IES/gov host domain is a governance decision.

---

## Schemas Used in This Use Case

A **single schema** — **[ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md)** (W3C VC). The Passport is the holder-bound issuance of that one credential and combines no additional schemas. When the consumer later shares live readings, that uses the [MeterData](../../schemas/MeterData/v0.6/README.md) schema over Beckn Data Exchange — a separate exchange, not part of the credential. See [Consumer Meter Digest](../consumer-meter-digest/README.md).

## Value Unlock

The consumer gains a **portable, tamper-evident proof** of their connection and assets that they hold themselves. Banks, subsidy portals, net-metering desks and DER marketplaces verify it offline in seconds — no DISCOM callback, no manual site check. The DISCOM cuts verification load and fraud (forged sanction letters, ghost assets) and gets a clean asset register as a by-product. Regulators get a consistent, auditable asset record across licensees. **Selective disclosure** lets the consumer reveal only what a given verifier needs — sanctioned load to a lender, asset capacity to a marketplace — without exposing the rest.

---

## Setup: Register → Discover → Exchange

Built on the four implementation steps in **[How you implement IES](../../how-you-implement-ies/README.md)**. Use-case-specific items only below.

### Register — identity and proofing

The Passport sets `credentialSubject.id` to the wallet DID and `customerProfile.idRef` to a government-ID *reference*, both vouched for at issuance.

- [ ] [Identity setup](../../how-you-implement-ies/setup-register.md) complete (DISCOM `did:web` resolves; DeDi namespace verified)
- [ ] Identity-proofing method chosen and documented (DigiLocker pull / Aadhaar Offline KYC / in-person / DISCOM record match)
- [ ] Privacy review completed; procedure tested with one consumer

### Discover — wallet delivery

- [ ] [Discovery setup](../../how-you-implement-ies/setup-discovery.md) complete (ONIX running; subscriber record published)
- [ ] DigiLocker Pull URI registered → [DigiLocker delivery](../../what-ies-provides/energy-credentials/digilocker.md)
- [ ] Direct DID-push tested for one non-DigiLocker wallet (where relevant)
- [ ] A freshly issued Passport reaches a wallet end-to-end

### Exchange — issuance shape

- [ ] [Adapter built](../../how-you-implement-ies/build-adapter.md) for the [ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md) schema
- [ ] `credentialSubject.id` = wallet DID
- [ ] `customerProfile.idRef` = verified government-ID *reference* (not the raw number)
- [ ] `validUntil` set to a sensible horizon (re-issued on material change)
- [ ] Schema validation passes against [ElectricityCredential v1.2 schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json)
- [ ] Selective-disclosure profile agreed with the first verifiers (SD-JWT-VC typical)
- [ ] Verification rehearsed with one verifier (bank / marketplace / subsidy portal)
- [ ] Revocation tested — revoking invalidates all presentations within minutes

### Team

- [ ] Customer-ops SPOC (identity proofing)
- [ ] IT SPOC (wallet delivery)
- [ ] Governance / Compliance SPOC (privacy review)

---

## Dev kits and code

- **Schema source** — [`schemas/ElectricityCredential/v1.2/attributes.yaml`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/attributes.yaml) (compile with `make build`)
- **JSON Schema** — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json)
- **JSON-LD context** — [`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.jsonld)
- **Example payloads** — [`examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ElectricityCredential/v1.2/examples) (single meter + PV; sub-metering; parallel metering)
- **Validation** — `python3 scripts/validate_schema.py schemas/ElectricityCredential/v1.2/schema.json <your-output.json>`
- **Reference issuer (OpenCred)** — `ghcr.io/nfh-trust-labs/opencred/opencred-server`
- **Issuance walkthrough** — [Energy Credentials — Issue your first credential](../../what-ies-provides/energy-credentials/README.md#issue-your-first-credential)

---

## Annexure A — Standards Referenced

Every standard cited above with a one-line scope. Full version-by-version provenance is in the schema's `x-standards` annotations.

| Standard | Scope |
|---|---|
| IS 16444 (Parts 1, 2) | AC smart meter — specification |
| IS 15959 (Parts 1–3) | DLMS/COSEM data-exchange companion specification; OBIS codes |
| IS 14286 (= IEC 61215) | Crystalline-silicon PV modules — design qualification and type approval |
| IS 16221 (Parts 1, 2) (= IEC 62109-1/-2) | Safety of power converters (inverters) for PV systems — BIS-CRS (inverter resource only) |
| IS 16270 | Secondary cells/batteries for solar PV application |
| IS 17017 (series) (from IEC 61851 / 62196) | EV conductive charging |
| CEA (Installation and Operation of Meters) Regulations, 2006 | Metering legal framework; net meter as billing source of truth |
| CEA (Technical Standards for Connectivity of DG Resources) Regulations, 2013, am. 2019 | Connectivity below 33 kV; PCC; DC-injection limit; harmonics |
| IEC 61968-1 / -9 / -11 | CIM — customer, metering, distribution model |
| IEC 61970-301 / -302 | CIM — base network model; DER / power-electronics / battery |
| IEC 61850-7-420 | DER information model; DER control roles |
| IEC 61727 / IEC 62116 | PV utility interface; anti-islanding |
| IEC 62933 / 62933-2-1 / IEC 62619 | Energy storage systems; performance test; lithium battery safety |
| IEC 62196 | EV connectors |
| IEC 62056 | DLMS/COSEM; OBIS (IS 15959 is the Indian companion) |
| IEEE 1547-2018 | DER interconnection and interoperability (ride-through, anti-islanding, volt-var, freq-watt) |
| IEEE 519-2014 | Harmonic control — CEA-referenced |
| IEEE 2030.5 | Smart energy profile; DER communications / aggregator roles |
| W3C VC Data Model 2.0; W3C DID Core | Verifiable Credential envelope; decentralized identifiers (the credential framework) |
| GeoJSON (RFC 7946); schema.org PostalAddress | Location geometry and postal address |
| OCPP; ISO 15118 | EV charger control / V2G protocols |

## Annexure B — Example Payload

A single-phase LT-Domestic connection with a 5 kW PV array on a 5 kVA inverter and a 6 kWh aggregator-enrolled battery, fed from one distribution transformer. Holder-bound (`credentialSubject.id` = wallet DID; `idRef` = DigiLocker reference). Validates against ElectricityCredential v1.2. Identifiers are illustrative.

Full payload: **[`examples/example.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/ElectricityCredential/v1.2/examples/example.json)** in the repository.

Two additional examples in the same directory:

- **[`example-submetering.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/ElectricityCredential/v1.2/examples/example-submetering.json)** — Building main meter + two tenant sub-meters + rooftop solar
- **[`example-parallel-metering.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/ElectricityCredential/v1.2/examples/example-parallel-metering.json)** — Import meter + export meter (solar FIT)

## Annexure C — JSON Schema

The authoritative definitions are the IES-hosted artifacts, not this document:

- Canonical reference: [`india-energy-stack/ies-accelerator`](https://github.com/India-Energy-Stack/ies-accelerator), served at `https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/`
- **[`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json)** — bundled JSON Schema (Draft 2020-12)
- **[`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.jsonld)** — JSON-LD context (units, vocab)
- **[`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/vocab.jsonld)** — RDF vocabulary with CIM alignments

The standard governing each field is recorded as the machine-readable `x-standards` array; the §5 order of preference is kept at the root as `x-standards-precedence { IS:1, CEA:2, IEGC:2, IEC:3, IEEE:4 }`.
