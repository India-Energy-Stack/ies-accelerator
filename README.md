# India Energy Stack — Accelerator

**India Energy Stack (IES)** is a common set of specifications for sharing data across the power sector. It works the way UPI works for banking — UPI holds no money of its own; money stays in the customer's bank, and UPI is only the shared rules that let any bank pay any other. **IES is the same idea, for energy data.** The data stays in the systems that already hold it, and IES specs let any two systems exchange and act on it directly.

IES is **live**. Four pilot DISCOMs — [PVVNL, APEPDCL, DGVCL and Tata Power](concepts/pilots.md) — built their adapter and demonstrated DER Visibility, Consumer Energy Passport, Consumer Meter Digest and Smart Meter Data Exchange in the 30-day Challenge (21 May – 21 June 2026).

{% hint style="info" %}
📄 **Printable version:** download this entire guide as a single PDF — [**ies-report.pdf**](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf). Regenerated automatically whenever the docs change.
{% endhint %}

---

## How IES works — three steps

Every IES interaction follows the same three steps. They are the **spine of this entire GitBook** — Part 1 explains each step, Part 2 shows you how to set each one up, and Part 3 shows the use cases each step combines to deliver.

| Step | What it does | Example standard |
|---|---|---|
| **[1. Register](register.md)** | Every participant gets a verifiable digital identity and is listed in a shared directory. *Done once.* | [W3C Decentralised Identifiers](https://www.w3.org/TR/did-core/) |
| **[2. Discover](discover.md)** | Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. *No bilateral arrangement is needed.* | [Beckn protocol](https://becknprotocol.io) |
| **[3. Exchange](exchange.md)** | Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, the exchange also produces a **verifiable credential** the holder keeps. | DLMS/COSEM, IEEE 2030.5, OpenADR; W3C VCs |

IES picks the right open standard for each step and publishes a specification on top. **IES does not write new standards.** Build to the IES specs once, and a system can connect to any other IES-ready system without fresh integration work.

---

## How this guide is organised

Three top-level parts, each organised by the **Register / Discover / Exchange** spine.

### Part 1 — What IES Provides

The specifications. What is published.

| Section | What's in it |
|---|---|
| [What IES Is](concepts/what-ies-is.md) | The problem, the UPI analogy, what IES is and is not, the four pilots, FAQ. The intro page. |
| [Register](register.md) | Verifiable digital identity (W3C DIDs) and the shared directory (DeDi). Detail under: [Identifiers](identifiers/README.md), [Registries](registries/README.md). |
| [Discover](discover.md) | Beckn-protocol interaction. Detail under: [Data Exchange](data-exchange/README.md). |
| [Exchange](exchange.md) | Schemas, taxonomy and verifiable credentials. Detail under: [Energy Credentials](energy-credentials/README.md), [Schemas](schemas/README.md). |
| [Taxonomy](taxonomy.md) | Master schema map, standards precedence, versioning, how to propose a new schema. |

### Part 2 — [How you implement IES](implementation/README.md)

The action guides. What you do.

| Step | Action page | Time |
|---|---|---|
| 1 | [Setup Register](implementation/setup-identity.md) | 1–2 days |
| 2 | [Setup Discovery](implementation/setup-discovery.md) | 1–2 days |
| 3 | [Build your Internal-facing Adapter](implementation/build-adapter.md) | 1–4 weeks |
| 4 | [Conformance Checklist](implementation/conformance.md) | 1 day |

### Part 3 — [Use Case Implementation Guides](use-cases/README.md)

What you can ship, organised per the **[IES Documentation Template](use-cases/README.md#how-each-guide-is-organised)** so once you've read one, you know where to look in any other.

| Stage | Use cases |
|---|---|
| **Live in pilot** | [Consumer Energy Passport](use-cases/consumer-energy-passport/README.md) · [Consumer Meter Digest](use-cases/consumer-meter-digest/README.md) · [Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md) · [DER Visibility](use-cases/der-visibility/README.md) |
| **Live or staged** | [DISCOM Regulatory Filing](use-cases/discom-regulatory-filing/README.md) · [Tariff Intelligence](use-cases/tariff-intelligence/README.md) · [Outage Visibility](use-cases/outage-visibility/README.md) |
| **In progress** | [P2P Energy Exchange](use-cases/p2p-energy-exchange/README.md) · [DER Flexibility](use-cases/der-flexibility/README.md) |

---

## Where to start

- **New to IES?** Read **[What IES Is](concepts/what-ies-is.md)** — five minutes.
- **Decision-maker / reviewer?** Skim **[Part 1](#part-1-what-ies-provides)** in order: What IES Is → Register → Discover → Exchange.
- **DISCOM / regulator / vendor onboarding?** Go straight to **[Part 2 — How you implement IES](implementation/README.md)** — the same four steps the pilot DISCOMs followed in 30 days.
- **Picking a first use case?** Browse the table in **[Part 3](use-cases/README.md)** — pilot cases at the top.
- **Need a term defined?** Always-visible [Glossary](glossary.md).

---

## Why IES?

The Indian power sector has spent heavily on digital tools but not on a common way for those tools to work together. A single DISCOM often runs several metering systems supplied by different firms and spends years making them work together because none was built to a common standard. The same effort is repeated across the country.

IES is the **shared digital infrastructure** that ends that duplication — open specifications, verifiable data, interoperable protocols. The data stays where it is; the way it is described and requested becomes common.

For the longer answer, read **[What IES Is](concepts/what-ies-is.md)**.

---

## Key standards and protocols

| Standard | Role in IES |
|---|---|
| [W3C Decentralized Identifiers (DIDs)](https://www.w3.org/TR/did-core/) | The **Register** layer — cryptographic identity for issuers, holders, verifiers, assets and datasets |
| [Beckn Protocol v2.0](https://becknprotocol.io) | The **Discover** layer — peer-to-peer discovery, contracting, consent, audit |
| [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/) | The durable-record half of **Exchange** — signed, machine-verifiable credentials |
| [DLMS-COSEM / IS 15959](https://en.wikipedia.org/wiki/IEC_62056) | The meter-data half of **Exchange** — smart-meter wire protocol used in RDSS AMI deployments |
| [IEC 61968 / CIM / MultiSpeak](https://en.wikipedia.org/wiki/IEC_61968) | The asset-data-model half of **Exchange** — HES↔MDMS interoperability standards |
| [IEEE 2030.5 / IEEE 1547](https://standards.ieee.org/ieee/2030.5/5897/) | The DER / flexibility half of **Exchange** — solar, storage, EV charging |
| [OpenADR 3.1.0](https://www.openadr.org) | The demand-response half of **Exchange** — DR events and flexibility reporting |
| [DigiLocker](https://digilocker.gov.in) | India's national digital document wallet — consumer-facing credential store |

---

## Related Repositories

- [ies-docs](https://github.com/India-Energy-Stack/ies-docs) — IES architecture primitives and implementation guides
- [Digital Energy Grid (DEG)](https://github.com/Beckn-One/DEG) — upstream open protocol specification
- [DDM](https://github.com/beckn/DDM) — Dataset Descriptor Model (`DatasetItem` schema)
