# What IES Is

The India Energy Stack in plain words — the problem, the idea, how it works, what it is not, what changes for the sector, where it is live, and the questions most often asked.

---

## The problem

Power utilities in India have added many digital tools at the consumer end: smart meters, rooftop solar, EV charging, demand-side measures. Each produces useful data. **But the data stays locked inside separate systems** — the DISCOM's own software, the metering agency's portal (the [AMISP](../glossary.md#amisp)), each vendor's database — in formats other systems can't read. Every data share means a fresh connection built by hand; rules are issued and checked on paper; consumers can't use their own consumption records.

The cost is real and sector-wide: a DISCOM often runs several metering systems from different firms and spends years making them work together, because none was built to a common standard. **The same effort is repeated across the country.**

---

## The idea, in one paragraph

**The India Energy Stack (IES) is a common set of specifications for sharing data across the power sector.** It works the way UPI works for banking. UPI holds no money of its own. Money stays in the customer's bank, and UPI is only the shared set of rules that lets any bank's app pay any other bank's customer, without a separate arrangement for each pair. IES works the same way, for energy data rather than money. The data stays in the systems that already hold it, and IES specs ensure that any system can exchange data with any other, without a separate arrangement for each pair.

The sector already has rules and standards for what data to report and how it is structured. **IES does not replace any of them.** It makes the same data machine-readable, common across the sector, and verifiable, so any two systems can exchange and act on it directly.

| | UPI (banking) | IES (energy data) |
|---|---|---|
| Where the value lives | In each bank's accounts | In each system that already holds the data |
| What the standard owns | The interaction rules between banks | The interaction rules between systems |
| Who builds the connector | Each bank, once | Each organisation, once |
| What gets cheaper for everyone | New apps and services on top of money flows | New apps and services on top of verified energy data |

UPI did not replace banks. IES does not replace DISCOMs, MDMs, CIS systems, regulator portals or vendor databases.

---

## How it works — three steps

Every IES interaction follows the same three steps. They are the spine of this entire GitBook — each step has its own specification page in **[What IES Provides](../what-ies-provides/README.md)** and a matching set-up page in **[How you implement IES](../how-you-implement-ies/README.md)**.

| Step | What happens | Example standard |
|---|---|---|
| **1. [Register](../what-ies-provides/register.md)** | Every participant gets a verifiable digital identity and is listed in a shared directory. Done once. | [W3C Decentralised Identifiers](https://www.w3.org/TR/did-core/) |
| **2. [Discover](../what-ies-provides/discover.md)** | Before a data exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. No bilateral arrangement needed. | [Beckn protocol](https://github.com/beckn/protocol-specifications-v2) |
| **3. [Exchange](../what-ies-provides/exchange.md)** | Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, a verifiable credential is issued. | DLMS/COSEM for meter data, IEEE 2030.5 for solar/storage, W3C Verifiable Credentials |

Two capabilities build on this shared identity foundation:

- **Data exchange** — organisation-to-organisation (B2B) exchange of structured datasets: meter telemetry, regulatory filings, tariff data. IES recommends the open [Beckn protocol](https://github.com/beckn/protocol-specifications-v2) for this — discovery, consent, contract and audit trail between any two registered parties.
- **Energy credentials** — signed, durable records ([W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/)) a holder keeps and re-presents anywhere: a consumer's connection record, a signed meter digest. Credentials are verified against the issuer's published key and do not require a Beckn network — consumer-facing delivery happens over [DigiLocker](../glossary.md#digilocker), a web portal, or any channel the issuer already runs.

In Step 1 a DISCOM, AMISP, regulator, aggregator or vendor publishes a small JSON file (`did:web`) at a web address it controls, listing the public key it signs with; anyone can fetch it over plain HTTPS and check signatures on their own. Internal numbering (CIS consumer numbers, meter serial numbers) is preserved as the tail of the identifier — nothing renames. The discovery and revocation layer is **[DeDi](../glossary.md#dedi)**, a public registry mechanism for namespaces, network membership, public keys and credential revocation.

**IES selects the right open standard for each step and publishes a specification that builds on it. IES does not write new standards.** Build to the IES specifications once, and a system can connect to any other IES-ready system without fresh integration work.

---

## What you change in your own systems

**Nothing in your existing systems changes.** A small piece of software, called the **adapter**, sits at the edge of each system to ensure conformance with IES specs. The adapter comes in two parts:

- **ONIX (ready-made), the same for everyone.** Handles finding other systems and exchanging messages with them. This is the Beckn ONIX reference software, which the participant does not build. See **[Glossary → ONIX](../glossary.md#onix)**.
- **Mapping (specific to each organisation).** A small mapping that translates between its own data formats and the IES specs. Set up once, typically by your technology vendor. Databases, field names and internal software stay exactly as they are.

```
                                ┌──────────────────────┐
   Your existing systems        │   IES adapter        │       Other IES
   (CIS · MDM · HES · ERP ·     │   ONIX (ready-made)  │  ◄──► participants
    DERMS · billing · web)  ◄──►│   ─────────────      │       (DISCOMs, AMISPs,
                                │   Your mapping       │        regulators, banks,
   No changes needed.           │   (set up once)      │        aggregators…)
                                └──────────────────────┘
```

The minimum to participate is the same for every organisation:

1. Create a digital identity and list your organisation in the shared directory.
2. Install the adapter once.
3. Pass the basic conformance check.

After this, every new IES-ready partner connects with no further integration work. The how-to is in **[How you implement IES](../how-you-implement-ies/README.md)**.

---

## What IES is not

Five common confusions, cleared up:

| # | Confusion | Reality |
|---|---|---|
| 1 | **A central platform or database that stores energy data** | IES stores nothing. Data stays in the systems that already hold it. IES is only the shared set of specifications that lets any two systems exchange and act on it directly. |
| 2 | **A replacement for any existing DISCOM system, MDM or consumer-information system** | Your CIS, MDM, HES, DERMS, ERP, billing, web portal — none of these change. The IES adapter sits at the edge. |
| 3 | **A new regulator or authority that frames energy rules** | IES adds no new rules. It turns existing CEA, CERC and State Supply Code rules into a form software can read. The IES Cell, being constituted under the Central Electricity Authority, governs the specifications themselves — not the regulations they encode. |
| 4 | **A software product that utilities buy and install** | IES is a set of open, published specifications. No licence fee. No central platform. A ready-made adapter (the Beckn ONIX reference) is provided as open software to start with. |
| 5 | **A system that controls or monitors the physical grid** | IES facilitates a secure link between parties to exchange data. It does not touch SCADA, DMS, EMS or any safety-critical control system. |

And things IES does **not** ask for:

- **No new data.** IES asks for nothing the sector does not already produce. It only puts existing data into a common, signed format when it is shared.
- **No new compliance work.** If a DISCOM already files something today, IES makes that filing machine-readable. It does not invent a new filing.
- **No replacement of completed integrations.** Work just finished is not wasted; IES sets the standard the *next* integration will follow.
- **No mandatory bulk data transport.** IES specifies the data format and the coordination, not the transport. Bulk data moves over your normal channels — secure web, SFTP, Kafka, signed URL — with IES carrying the agreement, consent and audit trail.
- **No personal data storage.** Consumer data is shared only with explicit consent, for the stated purpose. IES holds no personal data.

IES is **infrastructure**, not application — like UPI for banking, or DigiLocker for documents. By staying tightly scoped to identity, discovery and data exchange, it avoids competing with the sector's existing software, regulators, or operational systems. The work it does is the work nobody owns today.

---

## What changes for the sector

None of this is new infrastructure or new compliance; it is what becomes possible once data is verifiable and exchangeable on a common standard.

| Outcome | What changes |
|---|---|
| **Integration cost falls** | One published standard replaces bespoke point-to-point work. A new integration connects in days, not months. |
| **No vendor lock-in** | IES conformance is written into the procurement specification. Vendors build to a published standard. |
| **Each new capability costs less than the last** | The identity and trust foundation is reused. Distributed resource, flexibility and market use cases build on what is already in place. |
| **New services become viable** | Banks, financiers and aggregators can build services on verified energy data, as new lenders did on Account Aggregator in the financial sector. |
| **Existing data becomes more useful** | Once energy data is verifiable and in a common format, it can be used for power procurement, demand forecasting, loss reduction and consented services like green lending. |

**For a DISCOM** — three gains: *lower cost* (one published standard replaces custom integration, no vendor lock-in); *better operations* (verifiable data improves forecasting and reduces losses); *wider use of existing data* (with consent, verified records support green lending and solar financing, with demand flowing back through the DISCOM). **IES is not a revenue scheme and does not monetise personal data.**

**For a consumer** — their energy history becomes portable and verifiable. The DISCOM signs it; the consumer holds it (in [DigiLocker](../glossary.md#digilocker) or a DID wallet); any verifier checks it offline against the DISCOM's published key. That unlocks green loans, subsidy claims and service enrolment without repeated paperwork; **selective disclosure** (prove "my sanctioned load is above 5 kW" without revealing the rest); and portability across DISCOMs and States. The credential types in use today are the **[Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md)** and the **[Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md)**.

**For the grid** — every distributed energy resource (rooftop solar, battery, EV charger) gets a verified identity when first connected. That makes practical: **[DER Visibility](../use-cases/der-visibility/README.md)** for the operator, aggregation across DISCOMs without bespoke per-utility integration, and flexibility programmes on the same identity layer.

**For regulators** — filings arrive already signed and in a single, consistent format ([ARR filings](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5)); tariff orders become computable; every share leaves an audit trail. See **[DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md)** and **[Tariff Intelligence](../use-cases/tariff-intelligence/README.md)**.

**For markets** — demand-side flexibility, **[P2P Energy Trading](../use-cases/p2p-energy-trading/README.md)** and open access become workable without a separate agreement between every pair of participants.

These compound: with one common standard the work is done once and every participant can use it. A consumer who moves in from another State arrives with an energy record that can be trusted at once. A bank or scheme anywhere in India can accept a record any DISCOM has issued. A service or vendor proven in one State is available to others without being rebuilt.

---

## Pilots and status

IES is **live**. The specifications have been published on this GitBook, the sandbox is working, and four pilot DISCOMs in four States have built their IES adapter and demonstrated a first set of live use cases.

### The 30-day DISCOM Challenge

**21 May 2026 – 21 June 2026.** Four pilot DISCOMs, spread across four States, built their IES adapters and demonstrated the four use cases live in the sandbox environment.

### Use cases demonstrated

| Use case | What was demonstrated | Before IES |
|---|---|---|
| **[DER Visibility](../use-cases/der-visibility/README.md)** | Solar unit registered with a verified digital identity; grid operator visibility confirmed | No reliable sector-wide method existed |
| **[Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md)** | Energy Passport issued and stored in DigiLocker; consumer able to share it for a green loan, subsidy claim or service enrolment | No portable, verifiable consumer energy record existed |
| **[Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md)** | Verifiable record of consumption history, reusable across DISCOMs and States without repeat verification | Manual and limited to a single DISCOM |
| **[Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md)** | IES-compliant data exchange completed between DISCOM and AMISP without a bilateral integration agreement | Weeks to months of bilateral integration per pair |

For each demonstration: an IES adapter (Beckn ONIX reference + DISCOM-specific mapping) running at the DISCOM, a `did:web` identity published and resolvable, a subscriber record in the IES network registry, an issued credential or completed exchange signed by the DISCOM's key, and end-to-end verification by a counterparty. The artefacts — example payloads, schemas, configuration — are public in this repository.

**Being added next:** [P2P Energy Trading](../use-cases/p2p-energy-trading/README.md) (schema published; pilot integrations being staged) and [OutageNotification](https://india-energy-stack.gitbook.io/docs/schemas/outagenotification/v0.1) (schema published; no use-case guide yet).

### The next phase

All State Governments, Union Territory Administrations and entities in the power sector are invited to take part — DISCOMs, GENCOs and TRANSCOs, load despatch centres, regulatory commissions, AMISPs, equipment manufacturers, technology and analytics providers, aggregators, and financial institutions using verified energy data. The minimum to participate is the three steps above; the implementation path is in **[How you implement IES](../how-you-implement-ies/README.md)**.

---

## Common questions

The questions most often asked by utilities, regulators and vendors, beyond what is covered above.

### Is IES only for connecting to other organisations, or also for internal systems?

**Mainly external** — that is where most of the difficulty lies today. The same adapter and standard also help within an organisation, where several systems from different vendors may not exchange data with each other. The larger gain is external; the internal improvement follows.

### Some functions can already be done within a single DISCOM. Why is IES needed?

A few functions, such as shifting demand within a single area, can be done alone today. **But IES is built for the whole country, and this benefits every participant.** Records, services and vendors proven in one State work in every other without fresh verification or rebuilding.

### Is IES still relevant for an organisation that mainly wants to improve existing systems rather than build new ones?

**Yes.** The same one-time adapter serves both purposes: it improves how current systems exchange data today, and provides the base to add new services later on the same standard.

### If a new service or a new kind of device is added later, does the process start over?

**No.** Each asset — a meter, a solar unit, an EV charger — is given its digital identity at the moment a use case first needs it. Everything already in place (verified identities, trust checks, agreed data formats) is reused. The first asset connected takes the most effort; each one after is far easier.

### Does IES meet cybersecurity requirements for the power sector?

**Yes.** IES is being designed to follow the applicable cyber-security regulations for the power sector. Every message carries a digital signature; the identity, consent and data layers are kept separate; the adapter sits at the edge only and creates no new internal integration points; and there is no central bottleneck all data must pass through. Security incidents follow the established power-sector incident response process.

### Does IES protect personal data?

**Yes.** IES stores no personal data. Consumer data is shared only with the consumer's explicit consent, for the stated purpose, and the consumer can prove a single fact (selective disclosure) without revealing the rest. IES is being designed to follow the applicable data protection law.

### Does IES change the relationship with the regulator?

**No.** IES only turns the existing CEA and CERC rules into a form software can read. If putting a rule into practice reveals a gap, IES points it out to the regulator. Only the regulator decides what to do about it.

### Does IES support large or bulk data transfers?

**Yes, with no size limit.** IES specifies the data format and the coordination, not the transport, so data moves over the organisation's normal channels (secure web, file transfer, signed URL, Kafka, MQTT, SFTP). Either **inline** — smaller batches inside the IES-formatted messages (best for small / mid-sized pulls) — or **by link** — the IES message carries a signed pointer or streaming endpoint (best for SLA-bound feeds and multi-gigabyte artefacts). Either way, IES handles discovery, consent, the data shape, and the audit trail.

### Who adds or updates the specifications and standards?

The **IES Cell** — the governance body being constituted under the Central Electricity Authority, with representation from across the sector. It owns the specifications, decides what is added or changed, and publishes each version. Its detailed governance framework will be notified separately.

### What is the process to request changes to the published specifications?

Any participant can propose a change to the IES Cell. Proposals are reviewed, and accepted changes are published as a new, versioned specification. Until the IES Cell's governance framework is notified, raise an issue or a discussion in the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator).

---

## Get in touch

- **IES Secretariat** — `ies.secretariat@fsrglobal.org`
- **REC (Nodal Agency)** — `ies@recindia.com`
- **Issues, discussions, contributions** — [github.com/India-Energy-Stack/ies-accelerator](https://github.com/India-Energy-Stack/ies-accelerator)

---

## Where to go next

- **Want the technical specifications?** → **[What IES Provides](../what-ies-provides/README.md)** — Register, Discover, Exchange, Taxonomy
- **Want to implement IES in your organisation?** → **[How you implement IES](../how-you-implement-ies/README.md)** — Setup Register, Issue Credentials, Setup Exchange, Build Adapter
- **Want to see a worked end-to-end use case?** → **[Use Case Implementation Guides](../use-cases/README.md)**
