# India Energy Stack — Accelerator

**India Energy Stack (IES)** is a common set of specifications for sharing data across the power sector. It works the way UPI works for banking — UPI holds no money of its own; money stays in the customer's bank, and UPI is only the shared rules that let any bank pay any other. **IES is the same idea, for energy data.** The data stays in the systems that already hold it, and IES specs let any two systems exchange and act on it directly.

IES is **live**. [Four pilot DISCOMs](concepts/what-ies-is.md#pilots-and-status) built their adapter and demonstrated DER Visibility, Consumer Energy Passport, Consumer Meter Digest and Smart Meter Data Exchange in the 30-day Challenge (21 May – 21 June 2026).

{% hint style="info" %}
📄 **Printable versions:** [**ies-report.pdf**](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf) (narrative + implementation guide) and [**IES_proposed_schemas.pdf**](https://india-energy-stack.github.io/ies-accelerator/IES_proposed_schemas.pdf) (schemas reference). Both regenerate automatically whenever the docs change — see [Download PDF](download-pdf.md).
{% endhint %}

---

## How IES works — three steps

Every IES interaction follows the same three steps. They are the **spine of this entire GitBook**.

| Step | What it does | Example standard |
|---|---|---|
| **[1. Register](what-ies-provides/register.md)** | Every participant gets a verifiable digital identity and is listed in a shared directory. *Done once.* | [W3C Decentralised Identifiers](https://www.w3.org/TR/did-core/) |
| **[2. Discover](what-ies-provides/discover.md)** | Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. *No bilateral arrangement is needed.* | [Beckn protocol](https://becknprotocol.io) |
| **[3. Exchange](what-ies-provides/exchange.md)** | Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, a **verifiable credential** is issued that the holder keeps. | DLMS/COSEM, IEEE 2030.5, OpenADR; W3C VCs |

IES picks the right open standard for each step and publishes a specification on top. **IES does not write new standards.** Build to the IES specs once, and a system can connect to any other IES-ready system without fresh integration work.

Two capabilities build on the shared identity foundation: **data exchange** — B2B exchange of structured datasets, for which IES recommends the Beckn protocol — and **energy credentials** — W3C Verifiable Credentials issued with OpenCred, verified against the issuer's published key, and delivered to consumers over DigiLocker, web portals or any channel the issuer already runs. Credentials do not require a Beckn network.

---

## How this guide is organised

Three top-level sections, each organised by the **Register / Discover / Exchange** spine.

### [What IES Provides](what-ies-provides/README.md)

The specifications. What is published.

| Section | What's in it |
|---|---|
| [What IES Is](concepts/what-ies-is.md) | The intro, on one page. Problem, UPI analogy, what IES is and is not, sector impact, the four pilots, FAQ. |
| [Register](what-ies-provides/register.md) | Verifiable digital identity (W3C DIDs) and the shared directory (DeDi). Detail under: [Identifiers](what-ies-provides/identifiers/README.md), [Registries](what-ies-provides/registries/README.md). |
| [Discover](what-ies-provides/discover.md) | Beckn-protocol interaction for data exchange. Detail under: [Data Exchange](what-ies-provides/data-exchange/README.md). |
| [Exchange](what-ies-provides/exchange.md) | The Taxonomy and verifiable credentials. Detail under: [Energy Credentials](what-ies-provides/energy-credentials/README.md), [Taxonomy](schemas/README.md). |
| [Taxonomy](schemas/README.md) | The master vocabulary of IES — every domain object, its plain-language overview, and the schema that describes its shape; standards precedence, versioning, proposal flow. |

### [How you implement IES](how-you-implement-ies/README.md)

The action guides. What you do.

| Step | Action page | Time |
|---|---|---|
| 1 | [Setup Register](how-you-implement-ies/setup-register.md) | 1–2 days |
| 2 | [Setup Discovery](how-you-implement-ies/setup-discovery.md) | 1–2 days |
| 3 | [Build your Internal-facing Adapter](how-you-implement-ies/build-adapter.md) | 1–4 weeks |
| 4 | [Conformance Checklist](how-you-implement-ies/conformance.md) | 1 day |

### [Use Case Implementation Guides](use-cases/README.md)

What you can ship, organised per the **[IES Documentation Template](use-cases/README.md#how-each-guide-is-organised)** so once you've read one, you know where to look in any other.

| Stage | Use cases |
|---|---|
| **Live in pilot** | [Consumer Energy Passport](use-cases/consumer-energy-passport/README.md) · [Consumer Meter Digest](use-cases/consumer-meter-digest/README.md) · [Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md) · [DER Visibility](use-cases/der-visibility/README.md) |
| **Live or staged** | [DISCOM Regulatory Filing](use-cases/discom-regulatory-filing/README.md) · [Tariff Intelligence](use-cases/tariff-intelligence/README.md) |
| **In progress** | [P2P Energy Trading](use-cases/p2p-energy-trading/README.md) |

---

## Where to start

- **New to IES?** Read **[What IES Is](concepts/what-ies-is.md)** — five minutes.
- **Decision-maker / reviewer?** Skim **[What IES Provides](what-ies-provides/README.md)** in order: What IES Is → Register → Discover → Exchange.
- **DISCOM / regulator / vendor onboarding?** Go straight to **[How you implement IES](how-you-implement-ies/README.md)** — the same four steps the pilot DISCOMs followed in 30 days.
- **Picking a first use case?** Browse the table in **[Use Case Implementation Guides](use-cases/README.md)** — pilot cases at the top.
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
- [DDM](https://github.com/beckn/DDM) — Decentralized Data Marketplace (`DatasetItem` schema family)
