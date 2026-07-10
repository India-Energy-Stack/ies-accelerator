# India Energy Stack — Accelerator

**India Energy Stack (IES)** is a common set of specifications for sharing power-sector data — like UPI for banking, but for energy: no data sits with a middleman, only the shared rules for exchanging it directly between systems.

IES is **live**: [Four pilot DISCOMs](concepts/pilots.md) demonstrated DER Visibility, Consumer Energy Passport, Consumer Meter Digest, and Smart Meter Data Exchange in the 30-day Challenge (21 May – 21 June 2026).

{% hint style="info" %}
📄 **Printable version:** the whole guide as one PDF — [**ies-report.pdf**](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf), regenerated on every change.
{% endhint %}

---

## How IES works — three steps

Every IES interaction follows these three steps — the **spine of this GitBook**.

| Step | What it does | Example standard |
|---|---|---|
| **[1. Register](what-ies-provides/register.md)** | Every participant gets a verifiable digital identity and is listed in a shared directory. *Done once.* | [W3C Decentralised Identifiers](https://www.w3.org/TR/did-core/) |
| **[2. Discover](what-ies-provides/discover.md)** | Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. *No bilateral arrangement is needed.* | [Beckn protocol](https://becknprotocol.io) |
| **[3. Exchange](what-ies-provides/exchange.md)** | Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, the exchange also produces a **verifiable credential** the holder keeps. | DLMS/COSEM, IEEE 2030.5, OpenADR; W3C VCs |

IES picks the open standard for each step and layers a spec on top; **it writes none of its own.** Build once, and any IES-ready system connects without new integration work.

---

## How this guide is organised

Three top-level sections, each organised by the **Register / Discover / Exchange** spine.

### [What IES Provides](what-ies-provides/README.md)

The specifications — what's published.

| Section | What's in it |
|---|---|
| [What IES Is](concepts/what-ies-is.md) | The intro. Problem, UPI analogy, what IES is and is not, the four pilots, FAQ. |
| [Register](what-ies-provides/register.md) | Verifiable digital identity (W3C DIDs) and the shared directory (DeDi). Detail under: [Identifiers](what-ies-provides/identifiers/README.md), [Registries](what-ies-provides/registries/README.md). |
| [Discover](what-ies-provides/discover.md) | Beckn-protocol interaction. Detail under: [Data Exchange](what-ies-provides/data-exchange/README.md). |
| [Exchange](what-ies-provides/exchange.md) | Schemas, taxonomy and verifiable credentials. Detail under: [Energy Credentials](what-ies-provides/energy-credentials/README.md), [Schemas](schemas/README.md). |
| [Taxonomy](what-ies-provides/taxonomy.md) | Master schema map, standards precedence, versioning, how to propose a new schema. |

### [How you implement IES](how-you-implement-ies/README.md)

The action guides — what you do.

| Step | Action page | Time |
|---|---|---|
| 1 | [Setup Register](how-you-implement-ies/setup-register.md) | 1–2 days |
| 2 | [Setup Discovery](how-you-implement-ies/setup-discovery.md) | 1–2 days |
| 3 | [Build your Internal-facing Adapter](how-you-implement-ies/build-adapter.md) | 1–4 weeks |
| 4 | [Conformance Checklist](how-you-implement-ies/conformance.md) | 1 day |

### [Use Case Implementation Guides](use-cases/README.md)

What you can ship. Each guide pairs with a **[Use Case Overview](use-cases-overview/README.md)** per the **[IES Documentation Template](use-cases-overview/README.md#how-each-page-is-organised)** — the *why*, then the *how*.

| Stage | Use cases |
|---|---|
| **Live in pilot** | [Consumer Energy Passport](use-cases/consumer-energy-passport/README.md) · [Consumer Meter Digest](use-cases/consumer-meter-digest/README.md) · [Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md) · [DER Visibility](use-cases/der-visibility/README.md) |
| **Live or staged** | [DISCOM Regulatory Filing](use-cases/discom-regulatory-filing/README.md) · [Tariff Intelligence](use-cases/tariff-intelligence/README.md) |
| **In progress** | [P2P Energy Trading](use-cases/p2p-energy-trading/README.md) |

---

## Where to start

- **New to IES?** [What IES Is](concepts/what-ies-is.md) — five minutes.
- **Decision-maker?** [What IES Provides](what-ies-provides/README.md): What IES Is → Register → Discover → Exchange.
- **Onboarding a DISCOM, regulator, or vendor?** [How you implement IES](how-you-implement-ies/README.md) — the four steps the pilots followed in 30 days.
- **Picking a first use case?** [Use Case Implementation Guides](use-cases/README.md) — pilot cases at the top.
- **Need a term defined?** [Glossary](glossary.md) — always in the left nav.

---

## Why IES?

The Indian power sector has spent heavily on digital tools, not on making them interoperate — the same vendor-integration effort repeated at every DISCOM. IES is the **shared digital infrastructure** that ends it: open specs, verifiable data, interoperable protocols — data stays put, and only how it's described and requested becomes common.

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
- [DDM](https://github.com/beckn/DDM) — Decentralized Data Marketplace (`DatasetItem` schema family)
