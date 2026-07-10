# How It Works: Register · Discover · Exchange

Every IES exchange — meter data, filings, credentials, DER visibility — follows the same three steps: learn once, recognise everywhere.

---

## The three steps

```
       Register                Discover                Exchange
       --------                --------                --------
  Verifiable identity     Interaction protocol      Schema, taxonomy, and
   (one-time setup)       (every exchange)         verifiable credentials

   Each participant       Both systems look          Data moves using
   gets a digital         each other up,             agreed field names,
   identity and is        confirm the other          following the public
   listed in a shared     is genuine, and agree      standard for that
   directory.             on what is exchanged.      domain.

   W3C DIDs               Beckn protocol             DLMS/COSEM, IEEE 2030.5,
                                                     OpenADR, IES schemas,
                                                     W3C Verifiable Credentials
```

---

## Step 1 — Register

> **Verifiable digital identity**, set up once per participant.

A DISCOM, AMISP, regulator, aggregator or vendor publishes a JSON file at its own URL, listing its public key — fetchable over HTTPS and verified by anyone, no central authority or middleware needed.

- **For organisations** — a `did:web` on a domain you own (e.g. `did:web:ies.discom.example`)
- **For consumers (when needed)** — a `did:key` in their wallet
- **For assets, meters, transformers, datasets** — a `did:web` under the issuing organisation's domain (`did:web:ies.discom.example:assets:meter:NM-44091234`)

Internal numbering (CIS consumer numbers, SAP codes, meter SLNOs) becomes the DID's tail; nothing is renamed.

**[DeDi](../glossary.md#dedi)** is the discovery and revocation layer: a public registry for namespaces, network membership, public keys and credential revocation.

**Full specification:** **[Register — Identifiers and Addressing](../what-ies-provides/identifiers/README.md)** and **[Registries and Directories](../what-ies-provides/registries/README.md)**.
**Implementation steps:** **[Setup Register](../how-you-implement-ies/setup-register.md)**.

---

## Step 2 — Discover

> **Interaction protocol**: both systems verify each other and agree terms before every exchange — no bilateral arrangement needed.

IES's control plane — discovery, offer, consent, contract, audit — runs on the open, asynchronous, peer-to-peer **[Beckn protocol](https://becknprotocol.io)**.

A typical lifecycle:

```
Seeker (BAP)                        Provider (BPP)
e.g. a bank, a SERC, a DISCOM       e.g. a DISCOM, an AMISP, an aggregator

  │── search ──────────────────────>│  "what data can I get?"
  │<── on_search ───────────────────│  catalogue of datasets / credentials
  │── select ──────────────────────>│  "I want this one"
  │<── on_select ───────────────────│  terms, conditions, required credentials
  │── init ────────────────────────>│  consent + contract draft
  │<── on_init ─────────────────────│
  │── confirm ─────────────────────>│  signed contract; payload or pointer
  │<── on_confirm ──────────────────│
  │── status ──────────────────────>│
  │<── on_status ───────────────────│  payload or signed access method
```

Every message is signed and verifiable via **[ONIX](../glossary.md#onix)**, the reference adapter — open software you configure, not build.

**Full specification:** **[Discover — Beckn Protocol](../what-ies-provides/data-exchange/README.md)**.
**Implementation steps:** **[Set up Discovery (Beckn ONIX)](../how-you-implement-ies/setup-discovery.md)**.

---

## Step 3 — Exchange

> **Schema, taxonomy and verifiable credentials**: data moves in agreed field names, per the domain's public standard.

IES publishes a specification on the right open standard for each domain:

| Domain | Underlying standard | IES specification |
|---|---|---|
| Meter telemetry | DLMS/COSEM (IS 15959) | **[MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6)** — eight compact profile shapes |
| Consumer credentials | W3C VC Data Model 2.0; CIM (IEC 61968/61970) | **[ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)** |
| Solar and storage attributes | IEEE 2030.5, IEC 61850-7-420 | **[ElectricityCredential](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)** energyResources |
| Demand response | OpenADR 3.1.0 | **[DemandFlex* family](../schemas/external/README.md#demand-flexibility)** (published; no IES use-case guide yet) |
| Regulatory filings | XBRL | **[ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5)** |
| Outage notices | OpenADR-aligned + DEG primitives | **[OutageNotification v0.1](https://india-energy-stack.gitbook.io/docs/schemas/outagenotification/v0.1)** |

Where needed, the exchange also produces a durable **[Verifiable Credential](../glossary.md#verifiable-credential-vc)** — e.g. a [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md), [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md), or DER Commissioning Record — held in [DigiLocker](../glossary.md#digilocker) and shared with any bank, regulator or scheme administrator, no return to the issuer needed.

**Full specifications:** **[Schemas](../schemas/README.md)** and **[Energy Credentials](../what-ies-provides/energy-credentials/README.md)**.
**Implementation steps:** **[Build Your Adapter](../how-you-implement-ies/build-adapter.md)**.

---

## Built on what already exists

IES adds no new standards — it reuses BIS, CEA, IEC and IEEE standards plus India's existing smart meters and systems. The adapter sits at the edge, so databases, software and field names stay unchanged.

```
                                ┌──────────────────────┐
   Your existing systems        │   ONIX adapter       │       Other IES
   (CIS · MDM · HES · ERP ·     │   (ONIX, ready)    │  ◄──► participants
    DERMS · billing · web)  ◄──►│   ─────────────      │       (other DISCOMs,
                                │   Your mapping       │        AMISPs, regulators,
   No changes needed.           │   (mapping, set up    │        banks, aggregators…)
                                │    once by your      │
                                │    vendor)           │
                                └──────────────────────┘
```

---

## The minimum to participate

Same for every organisation:

1. Create a digital identity and list your organisation in the shared directory.
2. Install the adapter once.
3. Pass the basic conformance check.

New partners then connect without fresh integration work. Full steps: **[How you implement IES](../how-you-implement-ies/README.md)**.

---

## Where to go next

- **Want a deep dive on a particular step?** → **[Register](../what-ies-provides/identifiers/README.md)** · **[Discover](../what-ies-provides/data-exchange/README.md)** · **[Exchange](../schemas/README.md)**
- **Want to implement?** → **[How you implement IES](../how-you-implement-ies/README.md)**
- **Want to see a use case end-to-end?** → **[Use Case Implementation Guides](../use-cases/README.md)**
