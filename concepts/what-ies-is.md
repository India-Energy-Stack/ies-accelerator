# What IES Is

A one-page explanation of the India Energy Stack.

---

## The problem

Power utilities in India have added many consumer-end digital tools — smart meters, rooftop solar, EV charging, demand-side measures — but the data stays locked in separate, incompatible systems: DISCOM software, the metering agency's portal (run by the [AMISP](../glossary.md#amisp)), each vendor's database. Exchanges need hand-built connections, rules stay paper-based, and consumers can't access their own records — a cost DISCOMs, regulators and technology providers keep paying nationwide for lack of one common standard.

---

## The idea, in one paragraph

**The India Energy Stack (IES) is a common set of specifications for sharing data across the power sector** — the way UPI works for banking: UPI holds no money, just the rules letting any bank pay any other with no arrangement per pair. IES does the same for energy data, layered on the sector's existing rules rather than replacing them, making it machine-readable, common and verifiable so any two systems can exchange it directly.

---

## What it does, in three steps

Every IES exchange follows these three steps — the spine of this GitBook, detailed in **[What IES Provides](../what-ies-provides/README.md)** with set-up steps in **[How you implement IES](../how-you-implement-ies/README.md)**.

| Step | What happens | Example standard |
|---|---|---|
| **1. [Register](../what-ies-provides/register.md)** | Every participant gets a verifiable digital identity and is listed in a shared directory. Done once. | [W3C Decentralised Identifiers](https://www.w3.org/TR/did-core/) |
| **2. [Discover](../what-ies-provides/discover.md)** | Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. No bilateral arrangement needed. | [Beckn protocol](https://becknprotocol.io) |
| **3. [Exchange](../what-ies-provides/exchange.md)** | Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, the exchange also produces a verifiable credential. | DLMS/COSEM for meter data, IEEE 2030.5 for solar/storage, OpenADR for demand response |

**IES selects the right open standard for each step and publishes a spec on it, writing none of its own.** Build once, connect to any IES-ready system with no fresh integration work.

---

## What you change in your own systems

**Nothing changes in your existing systems.** A small **adapter** sits at the edge for IES conformance, in two parts:

- **ONIX (ready-made), the same for everyone.** Finds and messages other systems — the Beckn ONIX reference software; participants don't build it. See **[Glossary → ONIX](../glossary.md#onix)**.
- **Mapping (specific to each organisation).** Translates its own data formats to the IES specs, set up once — databases, field names and software stay unchanged.

New IES-ready partners then connect with no further integration work — the how-to is in **[How you implement IES](../how-you-implement-ies/README.md)**.

---

## Why the UPI analogy is exact

| | UPI (banking) | IES (energy data) |
|---|---|---|
| Where the value lives | In each bank's accounts | In each system that already holds the data |
| What the standard owns | The interaction rules between banks | The interaction rules between systems |
| Who builds the connector | Each bank, once | Each organisation, once |
| What gets cheaper for everyone | New apps and services on top of money flows | New apps and services on top of verified energy data |

UPI didn't replace banks; IES doesn't replace DISCOMs, MDMs, CIS systems, regulator portals or vendor databases.

---

## What this means for you

- **For a DISCOM** — lower integration cost, no vendor lock-in, verifiable records as a new downstream service surface. See **[What Changes for the Sector → For DISCOMs](sector-impact.md#for-discoms)**.
- **For a consumer** — a portable, verifiable record of connection and consumption, held in [DigiLocker](../glossary.md#digilocker), shareable with a bank, subsidy portal or marketplace without going back to the DISCOM.
- **For a regulator** — filings arrive signed and in a single consistent format; tariff orders become computable.
- **For a vendor / OEM / aggregator / financier** — one published interface to build to, the same across DISCOMs and States.

For a fuller list see **[What Changes for the Sector](sector-impact.md)**.

---

## What IES is not

Equally important is what IES is **not** — five common confusions, cleared up in **[What IES Is Not](what-ies-is-not.md)**.

---

## Where it stands today

IES is **live**: specs published, sandbox working, and [four pilot DISCOMs](pilots.md) have built their adapter and demonstrated live use cases. See **[Pilots and Status](pilots.md)** for what was shown.

---

## Where to go next

- **Want the technical specifications?** → **[What IES Provides](../what-ies-provides/README.md)** — Register, Discover, Exchange, Taxonomy
- **Want to implement IES in your organisation?** → **[How you implement IES](../how-you-implement-ies/README.md)** — Setup Register, Setup Discovery, Build Adapter
- **Want to see a worked end-to-end use case?** → **[Use Case Implementation Guides](../use-cases/README.md)**
