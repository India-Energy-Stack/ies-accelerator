# How It Works: Register · Discover · Exchange

Every IES exchange — meter data, regulatory filings, consumer credentials, DER visibility — follows the same three steps. Learn it once, recognise it everywhere.

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

> **Verifiable digital identity.** Every participant gets a digital identity and is listed in a shared directory. This is done once.

A DISCOM, AMISP, regulator, aggregator or vendor publishes a small JSON file at a web address it controls. That file lists the public key it signs things with. Anyone — a wallet, another DISCOM, a regulator — can fetch that file over plain HTTPS and check signatures on their own. No central authority, no API key, no special middleware.

- **For organisations** — a `did:web` on a domain you own (e.g. `did:web:ies.apepdcl.in`)
- **For consumers (when needed)** — a `did:key` in their wallet
- **For assets, meters, transformers, datasets** — a `did:web` under the issuing organisation's domain (`did:web:ies.apepdcl.in:assets:meter:NM-44091234`)

Internal numbering (CIS consumer numbers, SAP codes, meter SLNOs) is preserved and reused as the tail of the DID. Nothing in your existing systems renames.

The discovery and revocation layer is **[DeDi](../glossary.md#dedi)** — a public registry mechanism for namespaces, network membership, public keys and credential revocation.

**Full specification:** **[Register — Identifiers and Addressing](../what-ies-provides/identifiers/README.md)** and **[Registries and Directories](../what-ies-provides/registries/README.md)**.
**Implementation steps:** **[Set up Identity](../how-you-implement-ies/setup-register.md)**.

---

## Step 2 — Discover

> **Interaction protocol.** Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. No bilateral arrangement is needed.

IES uses the **[Beckn protocol](https://becknprotocol.io)** for the control plane — discovery, offer, consent, contract, and audit. Beckn is open, asynchronous, peer-to-peer and trust-bounded.

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

Every message is signed and verifiable. The reference adapter implementing the Beckn protocol is **[ONIX](../glossary.md#onix)** — open software the participant configures, not builds.

**Full specification:** **[Discover — Beckn Protocol](../what-ies-provides/data-exchange/README.md)**.
**Implementation steps:** **[Set up Discovery (Beckn ONIX)](../how-you-implement-ies/setup-discovery.md)**.

---

## Step 3 — Exchange

> **Schema, taxonomy and verifiable credentials.** Data moves using agreed field names and structure, following the public standard for that domain.

IES selects the right open standard for each domain and publishes a specification that builds on it:

| Domain | Underlying standard | IES specification |
|---|---|---|
| Meter telemetry | DLMS/COSEM (IS 15959) | **[MeterData v0.6](../schemas/MeterData/v0.6/README.md)** — eight compact profile shapes |
| Consumer credentials | W3C VC Data Model 2.0; CIM (IEC 61968/61970) | **[ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md)** |
| Solar and storage attributes | IEEE 2030.5, IEC 61850-7-420 | **[ElectricityCredential](../schemas/ElectricityCredential/v1.2/README.md)** energyResources |
| Demand response | OpenADR 3.1.0 | (in progress — DER flexibility) |
| Regulatory filings | XBRL | **[ArrFiling v0.5](../schemas/ArrFiling/v0.5/README.md)** |
| Outage notices | OpenADR-aligned + DEG primitives | **[OutageNotification v0.1](../schemas/OutageNotification/v0.1/README.md)** |

Where the use case needs a durable record, the exchange also produces a **[Verifiable Credential](../glossary.md#verifiable-credential-vc)** — for example a [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md), a [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md), or a DER Commissioning Record. The holder keeps it in [DigiLocker](../glossary.md#digilocker) and can share it with any bank, regulator or scheme administrator without returning to the issuer.

**Full specifications:** **[Schemas](../schemas/README.md)** and **[Energy Credentials](../what-ies-provides/energy-credentials/README.md)**.
**Implementation steps:** **[Build Your Adapter](../how-you-implement-ies/build-adapter.md)**.

---

## Built on what already exists

IES uses standards already in use, from BIS, CEA, IEC and IEEE — it writes none of its own. The smart meters and systems India has already paid for are reused, not replaced. The adapter sits at the edge: your databases, software and field names stay exactly as they are.

```
                                ┌──────────────────────┐
   Your existing systems        │   ONIX adapter       │       Other IES
   (CIS · MDM · HES · ERP ·     │   (Part 1, ready)    │  ◄──► participants
    DERMS · billing · web)  ◄──►│   ─────────────      │       (other DISCOMs,
                                │   Your mapping       │        AMISPs, regulators,
   No changes needed.           │   (Part 2, set up    │        banks, aggregators…)
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

After this, every new partner connects without fresh integration work. Full step-by-step in **[Part 3 — Implementing IES](../how-you-implement-ies/README.md)**.

---

## Where to go next

- **Want a deep dive on a particular step?** → **[Register](../what-ies-provides/identifiers/README.md)** · **[Discover](../what-ies-provides/data-exchange/README.md)** · **[Exchange](../schemas/README.md)**
- **Want to implement?** → **[Part 3 — Implementing IES](../how-you-implement-ies/README.md)**
- **Want to see a use case end-to-end?** → **[Part 4 — Use Case Guides](../use-cases/README.md)**
