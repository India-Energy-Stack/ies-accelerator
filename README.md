# India Energy Stack — Accelerator

Power utilities in India have added many digital tools at the consumer end — smart meters, rooftop solar, EV charging, demand-side measures — and each produces useful data. But the data stays locked inside separate systems: the DISCOM's own software, the metering agency's portal, each vendor's database, in formats that other systems cannot read. Each time two systems must share data, a fresh connection is built by hand. India has spent heavily on digital tools, but not on a common way for those tools to work together.

The cost of this fragmentation is borne across the sector. A single DISCOM often runs several metering systems supplied by different firms and spends years making them work together, because none was built to a common standard. System operators, regulators and technology providers face the same difficulty in their own systems, and the same effort is repeated across the country.

**India Energy Stack (IES)** is a common set of specifications for sharing data across the power sector. It works the way UPI works for banking — UPI holds no money of its own; money stays in the customer's bank, and UPI is only the shared rules that let any bank pay any other. **IES is the same idea, for energy data.** The data stays in the systems that already hold it, and IES specs let any two systems exchange and act on it directly. The sector already has rules and standards for what data to report and how it is structured; IES does not replace any of them — it makes the same data machine-readable, common across the sector, and verifiable.

IES is **live**. [Four pilot DISCOMs](concepts/what-ies-is.md#pilots-and-status) built their adapter and demonstrated DER Visibility, Consumer Energy Passport, Consumer Meter Digest and Smart Meter Data Exchange in the 30-day Challenge (21 May – 21 June 2026).

{% hint style="info" %}
📄 **Printable version:** download this entire guide as a single PDF — [**ies-report.pdf**](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf). Schema reference material is included as an appendix at the end. Regenerated automatically whenever the docs change — see [Download PDF](download-pdf.md).
{% endhint %}

---

## How IES works — three steps

Every IES interaction follows the same three steps. They are the **spine of this entire GitBook**.

| Step | What it does | Example standard |
|---|---|---|
| **[1. Register](what-ies-provides/register.md)** | Every participant gets a verifiable digital identity and is listed in a shared directory. *Done once.* | [W3C Decentralised Identifiers](https://www.w3.org/TR/did-core/) |
| **[2. Discover](what-ies-provides/discover.md)** | Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. *No bilateral arrangement is needed.* | [Beckn protocol](https://github.com/beckn/protocol-specifications-v2) |
| **[3. Exchange](what-ies-provides/exchange.md)** | Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, a **verifiable credential** is issued that the holder keeps. | DLMS/COSEM, IEEE 2030.5, OpenADR; W3C VCs |

IES picks the right open standard for each step and publishes a specification on top. **IES does not write new standards.** Build to the IES specs once, and a system can connect to any other IES-ready system without fresh integration work.

Two capabilities build on the shared identity foundation: **data exchange** — B2B exchange of structured datasets, for which IES recommends the Beckn protocol — and **energy credentials** — W3C Verifiable Credentials issued with OpenCred, verified against the issuer's published key, and delivered to consumers over DigiLocker, web portals or any channel the issuer already runs. Credentials do not require a Beckn network.

---

## What IES is not

To be clear, IES is **not**:

- a central platform or database that stores energy data;
- a replacement for any existing DISCOM system, meter-data-management system or consumer-information system;
- a new regulator or authority that frames energy rules;
- a software product that utilities buy and install; or
- a system that controls or monitors the physical grid.

An organisation's own systems are not changed. A small piece of software — the **adapter** — sits at the edge of each system to ensure conformance with IES specs. Part of it is ready-made and the same for everyone (the Beckn ONIX reference software); part is a small mapping, set up once, that translates between an organisation's own data formats and the IES specs. Databases, field names and internal software stay exactly as they are, and after this every new IES-ready partner connects with no further integration work.

## What IES makes possible

- **For consumers.** A consumer's energy history becomes portable and verifiable — usable to obtain a green loan, claim a subsidy or sign up for a service, without repeated paperwork or calls to the DISCOM.
- **For the grid.** Every distributed energy resource is given a verified identity when it is first connected, so operators gain reliable visibility, and connection across DISCOMs, AMISPs and aggregators happens without a separate arrangement for each pair.
- **For the regulator.** Filings reach the regulator already signed and in a single, consistent format. Tariff orders become computable, and regulators move from reading PDF documents to monitoring data directly.
- **For markets.** Demand-side flexibility, peer-to-peer energy exchange and open access become workable in practice, without a separate agreement between every pair of participants.

## What IES changes for the sector

- **Integration cost falls.** One published standard replaces bespoke point-to-point work — a new integration connects in days, not months.
- **No vendor lock-in.** IES conformance is written into the procurement specification; vendors build to a published standard, and the utility is not tied to any single supplier.
- **Each new capability costs less than the last.** The identity and trust foundation is reused, so distributed-resource, flexibility and market use cases build on what is already in place.
- **New services become viable.** Banks, financiers and aggregators can build services on verified energy data — as new lenders did on Account Aggregator in the financial sector — creating demand that flows back through the DISCOM.
- **Existing data becomes more useful.** Once energy data is verifiable and in a common format, it supports power procurement and demand forecasting, analytics such as loss reduction and load management, and consented services such as green lending.

## Who should participate

All State Governments and Union Territory Administrations, and all entities in the power sector, are invited to take part — distribution utilities, generation companies (GENCOs), transmission companies (TRANSCOs), State and National Load Despatch Centres, the Central and State electricity regulatory commissions and the Forum of Regulators, metering agencies (AMISPs), equipment manufacturers, technology and analytics providers, aggregators, and financial institutions that use verified energy data. The minimum needed to participate is the same for every organisation: create a digital identity and list the organisation in the shared directory; build the IES adapter once; and pass the basic conformance check.

---

## How this guide is organised

Three top-level sections, each organised by the **Register / Discover / Exchange** spine.

### [What IES Provides](what-ies-provides/README.md)

The specifications. What is published.

| Section | What's in it |
|---|---|
| [What IES Is](concepts/what-ies-is.md) | The intro, on one page. Problem, UPI analogy, what IES is and is not, sector impact, the four pilots, FAQ. |
| [Register](what-ies-provides/register.md) | Verifiable digital identity (W3C DIDs) and the shared directory (DeDi) — one page. |
| [Discover](what-ies-provides/discover.md) | How two registered organisations find each other, agree terms and sign — the Beckn-protocol interaction (B2B). |
| [Exchange](what-ies-provides/exchange.md) | How data moves once discovered: the schemas, and where verifiable credentials (B2C) fit. |
| [Schemas](schemas/README.md) | The master vocabulary of IES — every domain object, its plain-language overview, and the schema that describes its shape; standards precedence, versioning, proposal flow. |

### [How you implement IES](how-you-implement-ies/README.md)

The action guides. What you do.

| Step | Action page | Time |
|---|---|---|
| 1 | [Setup Register](how-you-implement-ies/setup-register.md) | 1–2 days |
| 2 | [Issue Credentials](how-you-implement-ies/issue-credentials.md) *(credential use cases)* | ½ day |
| 3 | [Setup Exchange](how-you-implement-ies/setup-exchange.md) *(data-exchange use cases)* | 1–2 days |
| 4 | [Build your Internal-facing Adapter](how-you-implement-ies/build-adapter.md) | 1–4 weeks |
| 5 | [Conformance Checklist](how-you-implement-ies/conformance.md) | 1 day |

### [Use Case Implementation Guides](use-cases/README.md)

What you can ship, organised per the **[IES Documentation Template](use-cases/README.md#how-each-guide-is-organised)** so once you've read one, you know where to look in any other.

| Stage | Use cases |
|---|---|
| **Live in pilot** | [Consumer Energy Passport](use-cases/consumer-energy-passport/README.md) · [Consumer Meter Digest](use-cases/consumer-meter-digest/README.md) · [Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md) · [DER Visibility](use-cases/der-visibility/README.md) |
| **Live or staged** | [DISCOM Regulatory Filing](use-cases/discom-regulatory-filing/README.md) · [Tariff Intelligence](use-cases/tariff-intelligence/README.md) |
| **In progress** | [P2P Energy Exchange](use-cases/p2p-energy-trading/README.md) |

---

## Where to start

- **New to IES?** Read **[What IES Is](concepts/what-ies-is.md)** — five minutes.
- **Decision-maker / reviewer?** Skim **[What IES Provides](what-ies-provides/README.md)** in order: What IES Is → Register → Discover → Exchange.
- **DISCOM / regulator / vendor onboarding?** Go straight to **[How you implement IES](how-you-implement-ies/README.md)** — the same path the pilot DISCOMs followed in 30 days.
- **Picking a first use case?** Browse the table in **[Use Case Implementation Guides](use-cases/README.md)** — pilot cases at the top.
- **Need a term defined?** Always-visible [Glossary](glossary.md).

---

## Key standards and protocols

| Standard | Role in IES |
|---|---|
| [W3C Decentralized Identifiers (DIDs)](https://www.w3.org/TR/did-core/) | The **Register** layer — cryptographic identity for issuers, holders, verifiers, assets and datasets |
| [Beckn Protocol v2.0](https://github.com/beckn/protocol-specifications-v2) | The **Discover** layer — peer-to-peer discovery, contracting, consent, audit |
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
