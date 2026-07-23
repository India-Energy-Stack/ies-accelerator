# India Energy Stack — Accelerator

**IES: the why, what and how.** The India Energy Stack in plain words — the problem, the idea, how it works, what it is not, what it changes for the sector, and where it is already live. This page is the starting point; the rest of the GitBook turns it into specifications, implementation steps and worked use cases.

{% hint style="info" %}
📄 **Printable version:** download this entire guide as a single PDF — [**ies-report.pdf**](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf). Schema reference material is included as an appendix at the end. Regenerated automatically whenever the docs change — see [Download PDF](download-pdf.md).
{% endhint %}

---

## The problem

Power utilities in India have added many digital tools at the consumer end: smart meters, rooftop solar, electric-vehicle charging and demand-side measures. Each of these produces useful data. But the data stays locked inside separate systems: the [DISCOM](glossary.md#discom)'s own software, the metering agency's portal (operated by the Advanced Metering Infrastructure Service Provider, or [AMISP](glossary.md#amisp)), and each vendor's database, in formats that other systems cannot read. Each time two systems must share data, a fresh connection has to be built by hand. Rules are issued and checked on paper. Consumers cannot use their own consumption records. India has spent heavily on digital tools, but not on a common way for those tools to work together.

The cost of this fragmentation is real, and it is borne across the sector. A single DISCOM often runs several metering systems supplied by different firms and spends years making them work together, because none was built to a common standard. System operators, regulators and technology providers face the same difficulty in their own systems. The same effort is repeated across the country.

---

## What IES is

The India Energy Stack (IES) is a common set of specifications for sharing data across the power sector. It works the way UPI (Unified Payments Interface) works for banking. UPI holds no money of its own. Money stays in the customer's bank, and UPI is only the shared set of rules that lets any bank's app pay any other bank's customer, without a separate arrangement for each pair. IES works the same way, for energy data rather than money. The data stays in the systems that already hold it, and IES specs ensure that any system can exchange data with any other, without a separate arrangement for each pair.

The sector already has rules and standards for what data to report and how it is structured. IES does not replace any of them. It makes the same data machine-readable, common across the sector, and verifiable, so any two systems can exchange and act on it directly.

| | UPI (banking) | IES (energy data) |
|---|---|---|
| Where the value lives | In each bank's accounts | In each system that already holds the data |
| What the standard owns | The interaction rules between banks | The interaction rules between systems |
| Who builds the connector | Each bank, once | Each organisation, once |
| What gets cheaper for everyone | New apps and services on top of money flows | New apps and services on top of verified energy data |

---

## What IES is not

To clarify, IES is **NOT**:

1. a central platform or database that stores energy data;
2. a replacement for any existing DISCOM system, meter-data-management system or consumer-information system;
3. a new regulator or authority that frames energy rules;
4. a software product that utilities buy and install; or
5. a system that controls or monitors the physical grid.

---

## How it works — three steps

IES tells any two systems in the power sector how to share data with each other. It works in three steps. They are the spine of this entire GitBook — each step has its own specification page in **[What IES Provides](what-ies-provides/README.md)** and a matching set-up page in **[How you implement IES](how-you-implement-ies/README.md)**.

- **(a) [Register](what-ies-provides/register.md) (verifiable digital identity).** Every participant gets a digital identity and is listed in a shared directory. This is done once. Uses [W3C Decentralised Identifiers](https://www.w3.org/TR/did-core/), for example.
- **(b) [Discover](what-ies-provides/discover.md) (interaction protocol).** Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. No bilateral arrangement is needed. Uses the [Beckn protocol](https://github.com/beckn/protocol-specifications-v2), for example.
- **(c) [Exchange](what-ies-provides/exchange.md) (schema, taxonomy and verifiable credentials).** Data moves using agreed field names and structure, following the public standard for that domain: DLMS/COSEM for meter data, IEEE 2030.5 for solar and storage, OpenADR for demand response. Where the use case needs a durable record, the exchange also produces a verifiable credential, such as a [Consumer Energy Passport](use-cases/consumer-energy-passport/README.md), a [Consumer Meter Digest](use-cases/consumer-meter-digest/README.md), or a DER Commissioning Record. The holder keeps it in [DigiLocker](glossary.md#digilocker) and can share it with any bank, regulator, or scheme administrator without returning to the issuer.

IES selects the right open standard for each step and publishes a specification that builds on it. **IES does not write new standards.** Build to the IES specifications once, and a system can connect to any other IES-ready system without fresh integration work.

---

## What you change in your own systems

An organisation's own systems are not changed. A small piece of "software", called the **adapter**, sits at the edge of each system to ensure conformance with IES specs. The adapter comes in two parts. The first part is ready-made and the same for everyone: it handles finding other systems and exchanging messages with them. This is the [Beckn ONIX](glossary.md#onix) reference software, which the participant does not build. The second part is specific to each organisation: a small mapping that translates between its own data formats and the IES specs. This is set up once. Databases, field names and internal software stay exactly as they are. After this, every new IES-ready partner connects with no further integration work.

```
                                ┌──────────────────────┐
   Your existing systems        │   IES adapter        │       Other IES
   (CIS · MDM · HES · ERP ·     │   ONIX (ready-made)  │  ◄──► participants
    DERMS · billing · web)  ◄──►│   ─────────────      │       (DISCOMs, AMISPs,
                                │   Your mapping       │        regulators, banks,
   No changes needed.           │   (set up once)      │        aggregators…)
                                └──────────────────────┘
```

The minimum to participate is the same for every organisation: create a digital identity and list your organisation in the shared directory; install the adapter once; and pass the basic conformance check. The how-to is in **[How you implement IES](how-you-implement-ies/README.md)**.

---

## What becomes possible

When the India Energy Stack is used, for example the following becomes possible:

- **For consumers.** A consumer's energy history becomes portable and verifiable. It can be used to obtain a green loan, claim a subsidy or sign up for a service, without repeated paperwork or calls to the DISCOM. Certificates issued by a DISCOM are of direct use to banks, housing finance companies, scheme administrators and service providers who need verified energy data. When consumers can prove their energy history, demand for those certificates flows back through the DISCOM.
- **For the grid.** Every distributed energy resource, for example a rooftop solar unit or a small battery, is given a verified identity when it is first connected. Operators obtain reliable visibility of these resources ([DER Visibility](use-cases/der-visibility/README.md)), and connection across DISCOMs, AMISPs and aggregators (firms that pool many small resources) happens without a separate arrangement for each pair.
- **For regulators.** Filings reach the regulator already signed and in a single, consistent format ([DISCOM Regulatory Filing](use-cases/discom-regulatory-filing/README.md)). Tariff orders become computable ([Policy as Code](use-cases/tariff-intelligence/README.md)). Regulators move from reading PDF documents to monitoring data directly.
- **For markets.** Demand-side flexibility, [peer-to-peer energy transaction](use-cases/p2p-energy-trading/README.md) (consumers buying and selling power directly) and open access (a large consumer buying power from a supplier other than the local DISCOM) become workable in practice, without a separate agreement between every pair of participants.

---

## What IES changes for the sector

Taken together, these specifications produce the following practical outcomes:

| Outcome | What changes |
|---|---|
| **Integration cost falls** | One published standard replaces bespoke point-to-point work. A new integration connects in days, not months. |
| **No vendor lock-in** | IES conformance is written into the procurement specification. Vendors build to a published standard, and the utility is not tied to any single supplier. |
| **Each new capability costs less than the last** | The identity and trust foundation is reused, so distributed resource, flexibility and market use cases build on what is already in place. |
| **New services become viable** | Banks, financiers and aggregators can build services on verified energy data, as new lenders did on Account Aggregator in the financial sector, creating demand that flows back through the DISCOM. |
| **Existing data becomes more useful** | Once energy data is verifiable and in a common format, it can be used for power procurement and demand forecasting, for analytics such as loss reduction and load management, and as the basis for consented services such as green lending. This is the same data the DISCOM already holds, now usable beyond the system that created it. |

**IES is not a revenue scheme and does not monetise personal data.**

---

## Pilots and status

IES is already running in a test environment. The specifications have been published on this GitBook, and the sandbox is working. Four pilot DISCOMs in four States undertook a 30-day challenge, in which each built its IES adapter and demonstrated a first set of live use cases.

### The 30-day DISCOM Challenge

The four pilot DISCOMs, spread across four States, were:

1. **Paschimanchal Vidyut Vitran Nigam Limited (PVVNL)**, Meerut, Uttar Pradesh;
2. **Eastern Power Distribution Company of Andhra Pradesh Limited (APEPDCL)**, Visakhapatnam, Andhra Pradesh;
3. **Dakshin Gujarat Vij Company Limited (DGVCL)**, Surat, Gujarat; and
4. **Tata Power**, Mumbai, Maharashtra.

### Use cases demonstrated

The four use cases demonstrated were DER Visibility, Consumer Energy Passport, Consumer Meter Digest, and Smart Meter Data Exchange. The outcomes recorded are set out below.

| Use case | What was demonstrated | With IES | Before IES |
|---|---|---|---|
| **[DER Visibility](use-cases/der-visibility/README.md)** | Solar unit registered with a verified digital identity; grid operator visibility confirmed | ✓ | No reliable sector-wide method existed |
| **[Consumer Energy Passport](use-cases/consumer-energy-passport/README.md)** | Energy Passport issued and stored in DigiLocker; consumer able to share it for a green loan, subsidy claim or service enrolment | ✓ | Not possible earlier: no portable, verifiable consumer energy record existed |
| **[Consumer Meter Digest](use-cases/consumer-meter-digest/README.md)** | Verifiable record of consumption history, reusable across DISCOMs and States without repeat verification | ✓ | Manual and limited to a single DISCOM; not reusable elsewhere |
| **[Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md)** | IES-compliant data exchange completed between DISCOM and AMISP without a bilateral integration agreement | ✓ | Weeks to months of bilateral integration per pair |

**Being added next:** [P2P Energy Transaction](use-cases/p2p-energy-trading/README.md) (schema published; pilot integrations being staged) and [OutageNotification](https://india-energy-stack.gitbook.io/docs/schemas/outagenotification/v0.1) (schema published; no use-case guide yet).

### The next phase

All State Governments and Union Territory Administrations, and all entities in the power sector, are requested to take part. Participation is sought from distribution utilities, generation companies (GENCOs), transmission companies (TRANSCOs), State Load Despatch Centres and the National Load Despatch Centre, the Central and State electricity regulatory commissions and the Forum of Regulators, metering agencies (AMISPs), equipment manufacturers (including electric-vehicle and metering OEMs), technology and analytics providers, aggregators, and financial institutions that use verified energy data. The minimum needed to participate is the same for every organisation: create a digital identity and list the organisation in the shared directory; build the IES adapter once; and pass the basic conformance check. After this, every new partner connects without fresh integration work. The implementation path is in **[How you implement IES](how-you-implement-ies/README.md)**.

---

## Common questions

The questions utilities, regulators and vendors ask most — *does IES replace my systems? will it create new compliance work? how is consumer data protected? does it support bulk transfers? who governs the specifications?* — are answered in the **[FAQ](faq.md)** (the 20 questions from Annexure A of the IES Technical Note).

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

## Get in touch

- **IES Secretariat** — `ies.secretariat@fsrglobal.org`
- **REC (Nodal Agency)** — `ies@recindia.com`
- **Issues, discussions, contributions** — [github.com/India-Energy-Stack/ies-accelerator](https://github.com/India-Energy-Stack/ies-accelerator)

### Related Repositories

- [ies-docs](https://github.com/India-Energy-Stack/ies-docs) — IES architecture primitives and implementation guides
- [Digital Energy Grid (DEG)](https://github.com/Beckn-One/DEG) — upstream open protocol specification
- [DDM](https://github.com/beckn/DDM) — Decentralized Data Marketplace (`DatasetItem` schema family)

---

## Where to go next

- **Want the technical specifications?** → **[What IES Provides](what-ies-provides/README.md)** — Register, Discover, Exchange, Verifiable Credentials, Schemas
- **Want to implement IES in your organisation?** → **[How you implement IES](how-you-implement-ies/README.md)** — the getting-started checklist: Setup Register, Issue Credentials, Setup Exchange, Build Adapter
- **Want to see a worked end-to-end use case?** → **[Use Case Implementation Guides](use-cases/README.md)**
- **Need a term defined?** → the always-visible [Glossary](glossary.md).
