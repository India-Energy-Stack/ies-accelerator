# What IES Is

A one-page explanation of the India Energy Stack, in plain words.

---

## The problem

Power utilities in India have added many digital tools at the consumer end: smart meters, rooftop solar, electric-vehicle charging, demand-side measures. Each produces useful data. **But the data stays locked inside separate systems** — the DISCOM's own software, the metering agency's portal (operated by the [AMISP](../glossary.md#amisp)), each vendor's database — in formats that other systems cannot read. Each time two systems must share data, a fresh connection has to be built by hand. Rules are issued and checked on paper. Consumers cannot use their own consumption records.

India has spent heavily on digital tools, but not on a common way for those tools to work together.

The cost is real, and it is borne across the sector. A single DISCOM often runs several metering systems supplied by different firms and spends years making them work together, because none was built to a common standard. System operators, regulators and technology providers face the same difficulty in their own systems. **The same effort is repeated across the country.**

---

## The idea, in one paragraph

**The India Energy Stack (IES) is a common set of specifications for sharing data across the power sector.** It works the way UPI works for banking. UPI holds no money of its own. Money stays in the customer's bank, and UPI is only the shared set of rules that lets any bank's app pay any other bank's customer, without a separate arrangement for each pair. IES works the same way, for energy data rather than money. The data stays in the systems that already hold it, and IES specs ensure that any system can exchange data with any other, without a separate arrangement for each pair.

The sector already has rules and standards for what data to report and how it is structured. **IES does not replace any of them.** It makes the same data machine-readable, common across the sector, and verifiable, so any two systems can exchange and act on it directly.

---

## What it does, in three steps

Every IES exchange follows the same three steps. They are the spine of this entire GitBook — each step has its own page in **[What IES Provides](../README.md#part-1-what-ies-provides)** and a matching set-up page in **[How you implement IES](../how-you-implement-ies/README.md)**.

| Step | What happens | Example standard |
|---|---|---|
| **1. [Register](../what-ies-provides/register.md)** | Every participant gets a verifiable digital identity and is listed in a shared directory. Done once. | [W3C Decentralised Identifiers](https://www.w3.org/TR/did-core/) |
| **2. [Discover](../what-ies-provides/discover.md)** | Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. No bilateral arrangement needed. | [Beckn protocol](https://becknprotocol.io) |
| **3. [Exchange](../what-ies-provides/exchange.md)** | Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, the exchange also produces a verifiable credential. | DLMS/COSEM for meter data, IEEE 2030.5 for solar/storage, OpenADR for demand response |

**IES selects the right open standard for each step and publishes a specification that builds on it. IES does not write new standards.** Build to the IES specifications once, and a system can connect to any other IES-ready system without fresh integration work.

---

## What you change in your own systems

**Nothing in your existing systems changes.** A small piece of software, called the **adapter**, sits at the edge of each system to ensure conformance with IES specs. The adapter comes in two parts:

- **Part 1 — ready-made, the same for everyone.** Handles finding other systems and exchanging messages with them. This is the Beckn ONIX reference software, which the participant does not build. See **[Glossary → ONIX](../glossary.md#onix)**.
- **Part 2 — specific to each organisation.** A small mapping that translates between its own data formats and the IES specs. Set up once. Databases, field names and internal software stay exactly as they are.

After this, every new IES-ready partner connects with no further integration work. The how-to is in **[How you implement IES](../how-you-implement-ies/README.md)**.

---

## Why the UPI analogy is exact

| | UPI (banking) | IES (energy data) |
|---|---|---|
| Where the value lives | In each bank's accounts | In each system that already holds the data |
| What the standard owns | The interaction rules between banks | The interaction rules between systems |
| Who builds the connector | Each bank, once | Each organisation, once |
| What gets cheaper for everyone | New apps and services on top of money flows | New apps and services on top of verified energy data |

UPI did not replace banks. IES does not replace DISCOMs, MDMs, CIS systems, regulator portals or vendor databases.

---

## What this means for you

- **For a DISCOM** — lower integration cost, no vendor lock-in, verifiable records that flow downstream as a new service surface. See **[What Changes for the Sector → For DISCOMs](sector-impact.md#for-discoms)**.
- **For a consumer** — a portable, verifiable record of their connection and consumption, held in [DigiLocker](../glossary.md#digilocker), shareable with a bank, subsidy portal or marketplace without going back to the DISCOM.
- **For a regulator** — filings arrive signed and in a single consistent format; tariff orders become computable.
- **For a vendor / OEM / aggregator / financier** — one published interface to build to, the same across DISCOMs and States.

For a fuller list see **[What Changes for the Sector](sector-impact.md)**.

---

## What IES is not

It is just as important to know what IES is **not**. Five common confusions are cleared up in **[What IES Is Not](what-ies-is-not.md)**.

---

## Where it stands today

IES is **live**. The specifications have been published on this GitBook, the sandbox is working, and four pilot DISCOMs ([PVVNL · APEPDCL · DGVCL · Tata Power](pilots.md)) have built their IES adapter and demonstrated a first set of live use cases. See **[Pilots and Status](pilots.md)** for what was shown.

---

## Where to go next

- **Want the technical specifications?** → **[What IES Provides](../README.md#part-1-what-ies-provides)** — Register, Discover, Exchange, Taxonomy
- **Want to implement IES in your organisation?** → **[How you implement IES](../how-you-implement-ies/README.md)** — Setup Register, Setup Discovery, Build Adapter
- **Want to see a worked end-to-end use case?** → **[Use Case Implementation Guides](../use-cases/README.md)**
