# India Energy Stack — Accelerator

**India Energy Stack (IES)** is an open digital infrastructure layer for India's power sector — protocols and shared registries that let [DISCOMs](glossary.md#discom), [AMISPs](glossary.md#amisp), regulators, and consumers exchange data and trust each other's claims, without anyone owning the network.

{% hint style="info" %}
📄 **Printable version:** download this entire guide as a single PDF — [**ies-report.pdf**](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf). It is a printable version of this GitBook, regenerated automatically whenever the docs change.
{% endhint %}

```mermaid
flowchart TB
  actors["Generators · Prosumers · DISCOMs · Regulators · Aggregators · Consumers"]
  subgraph ies["India Energy Stack (IES)"]
    direction TB
    cred["<b>Energy Credentials</b><br/>W3C VCs + DigiLocker<br/><i>trust layer</i>"]
    data["<b>Data Exchange</b><br/>Beckn control plane + IES schemas<br/><i>data layer</i>"]
    reg["<b>Registries and Directories</b><br/>DeDi: namespaces + records<br/><i>discovery + revocation</i>"]
    id["<b>Identifiers and Addressing</b><br/>DIDs: did:web · did:key · did:jwk<br/><i>identity foundation</i>"]
    cred ~~~ data
    data ~~~ reg
    reg ~~~ id
  end
  infra["Physical energy infrastructure<br/>(meters · feeders · DERs · grid)"]
  actors --- ies
  ies --- infra
```

This **Accelerator** is the developer hub for building on it.

## How this guide is organised

| Part | What's in it |
|---|---|
| **[Part 1 — Understanding IES](./concepts/README.md)** | The why, what and how in plain words — start here if you are new |
| **[Part 2 — What IES Provides](#part-2-what-ies-provides)** | The four building blocks — Identifiers, Registries, Energy Credentials, Data Exchange |
| **[Part 3 — Implementing IES](./implementation/README.md)** | A step-by-step path from zero to a working IES adapter |
| **[Part 4 — Use Case Guides](./use-cases/README.md)** | Per-use-case integration guides, each following the IES Documentation Template |
| **[Part 5 — Pathways](./pathways/README.md)** | Role-based onboarding roadmaps (utility today; regulator next) |
| **[Reference — Schemas](./schemas/README.md)** | Canonical schema specifications, JSON-LD contexts, vocabularies |

## Part 2 — What IES Provides

The four building blocks. Each page is the **reference** — read [Part 3](./implementation/README.md) when you are ready to set them up.

| Building block | What it does |
|---|---|
| [Identifiers and Addressing](./identifiers/README.md) | [DIDs](glossary.md#did) and addressing grammar for DISCOMs, regulators, consumers, assets, meters, credentials and datasets |
| [Registries and Directories](./registries/README.md) | [DeDi](glossary.md#dedi)-based public registries — namespaces, the IES reference registries, [Beckn](glossary.md#beckn) subscriber registries, revocation, public-keys |
| [Energy Credentials](./energy-credentials/README.md) | Issue, hold and verify cryptographically signed digital credentials for energy assets and consumers |
| [Data Exchange](./data-exchange/README.md) | Discover and contract dataset exchanges over Beckn — telemetry, regulatory filings, tariff policies. Payload rides **inline** for small / simple datasets, or Beckn delivers an **access method** (signed URL / SFTP / Kafka / MQTT / OpenADR endpoint) when an established channel already moves the bytes |

---

## Where to Start

- **New to IES?** Read **[Part 1 — Understanding IES](./concepts/README.md)** — six short pages.
- **Want a five-minute orientation?** [Getting Started](./getting-started.md).
- **Onboarding as a DISCOM, regulator, or [NP](glossary.md#np)?** Go to **[Part 3 — Implementing IES](./implementation/README.md)** — the four-step path the pilot DISCOMs followed.
- **Picking a first use case?** Browse the table in **[Part 4 — Use Case Guides](./use-cases/README.md)** — pilot cases at the top.
- **Need a term defined?** Check the always-visible [Glossary](./glossary.md).

---

## Why IES?

The Indian power sector runs on data that is siloed, bespoke, and hard to trust — regulatory filings arrive as PDFs, telemetry lives inside proprietary [MDMS](glossary.md#mdms) systems, subsidy eligibility is verified manually, and credentials of ownership or identity have no standard form. IES provides a **shared digital infrastructure layer** — open standards, verifiable data, and interoperable protocols — so that every actor in the ecosystem can transact on common ground.

For the longer answer, read **[Part 1 — Understanding IES](./concepts/README.md)**.

---

## Key Standards and Protocols

| Standard | Role in IES |
|---|---|
| [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/) | Data model for signed, machine-verifiable credentials |
| [W3C Decentralized Identifiers (DIDs)](https://www.w3.org/TR/did-core/) | Cryptographic identity for issuers, holders, and verifiers |
| [Beckn Protocol v2.0](https://becknprotocol.io) | Peer-to-peer protocol for dataset discovery, contracting, consent, and audit. Carries payload inline for small / simple cases, or hands off an access method for established channels (signed URL, Kafka, MQTT, SFTP, OpenADR) |
| [DLMS-COSEM / IS 15959](https://en.wikipedia.org/wiki/IEC_62056) | Smart-meter wire protocol used in RDSS AMI deployments |
| [IEC 61968 / CIM / MultiSpeak](https://en.wikipedia.org/wiki/IEC_61968) | HES↔MDMS interoperability standards named in CEA AMI interoperability guidance |
| [OpenADR 3.1.0](https://www.openadr.org) | DR / DER event and flexibility-reporting protocol (not generic interval reads) |
| [DigiLocker](https://digilocker.gov.in) | India's national digital document wallet — consumer-facing credential store |

---

## Related Repositories

- [ies-docs](https://github.com/India-Energy-Stack/ies-docs) — IES architecture primitives and implementation guides
- [Digital Energy Grid (DEG)](https://github.com/Beckn-One/DEG) — upstream open protocol specification
- [DDM](https://github.com/beckn/DDM) — Dataset Descriptor Model (`DatasetItem` schema)
