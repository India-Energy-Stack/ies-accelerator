# What Changes for the Sector

What changes for DISCOMs, consumers, regulators and markets once IES is in use — no new infrastructure or compliance, just what a common, verifiable data standard unlocks.

---

## The five sector-wide outcomes

| Outcome | What changes |
|---|---|
| **Integration cost falls** | One published standard replaces bespoke point-to-point work. A new integration connects in days, not months. |
| **No vendor lock-in** | IES conformance is written into the procurement specification. Vendors build to a published standard, and the utility is not tied to any single supplier. |
| **Each new capability costs less than the last** | The identity and trust foundation is reused. Distributed resource, flexibility and market use cases build on what is already in place. |
| **New services become viable** | Banks, financiers and aggregators can build services on verified energy data, as new lenders did on Account Aggregator in the financial sector. Demand for those services flows back through the DISCOM. |
| **Existing data becomes more useful** | Once energy data is verifiable and in a common format, it can be used for power procurement, demand forecasting, loss reduction and consented services like green lending. The same data the DISCOM already holds becomes usable beyond the system that created it. |

---

## For DISCOMs

Three plain-terms gains.

### 1. Lower cost

One published standard replaces custom integration work — lower procurement and integration spend, no vendor lock-in.

### 2. Better operations

Reliable, verifiable data improves demand forecasting, power procurement and loss reduction.

### 3. Wider use of existing data

With consent, verified records enable services like green lending and solar financing, with demand flowing back to the DISCOM — new service surface, no compliance burden.

> **IES is not a revenue scheme and does not monetise personal data** — it lowers cost and makes data the DISCOM already holds more useful.

See the implementation path for a DISCOM in **[How you implement IES](../how-you-implement-ies/README.md)**.

---

## For consumers

A consumer's energy history becomes **portable and verifiable** — DISCOM-signed, consumer-held (in [DigiLocker](../glossary.md#digilocker) or a DID wallet), checkable offline against the DISCOM's key.

That unlocks:

- **Green loans, subsidy claims and service enrolment** without repeated paperwork or DISCOM calls — DISCOM certificates are directly useful to banks, housing finance companies, scheme administrators and other providers needing verified energy data.
- **Faster enrolment** for any new service — rooftop solar, EV charging, prepaid plans, ToD tariffs.
- **Selective disclosure.** The consumer can prove one fact (e.g. "sanctioned load above 5 kW") without revealing the rest.
- **Portability across DISCOMs and States.** A consumer who moves arrives already trusted — no fresh verification.

Today's credential types: **[Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md)** (a holder-bound ElectricityCredential) and **[Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md)** (a verifiable bundle of consumption history).

---

## For the grid

Every distributed energy resource — rooftop solar, a battery, an EV charger — gets a **verified identity** on connection, giving operators visibility with no separate arrangement across DISCOMs, AMISPs and aggregators (firms pooling small resources).

That enables:

- **DER Visibility** for the operator — a live, signed register of what's connected, at what capacity. See **[DER Visibility use case](../use-cases/der-visibility/README.md)**.
- **Aggregation across DISCOMs.** A battery fleet can be dispatched without a bespoke integration per utility.
- **Flexibility programmes** built on the same identity layer, not reinvented.

---

## For regulators

Filings reach regulators **already signed, in a single, consistent format**, with computable tariff orders — regulators monitor data directly instead of reading PDFs.

- **[ARR filings](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5)** in a structured, comparable form across utilities.
- **Tariff orders** parsable by software, with stable references for every clause.
- **Audit trail** of who shared what, with whom, under what authorisation.

See the **[DISCOM Regulatory Filing use case](../use-cases/discom-regulatory-filing/README.md)** and **[Tariff Intelligence use case](../use-cases/tariff-intelligence/README.md)**.

---

## For markets

Demand-side flexibility, peer-to-peer energy exchange (consumers trading power directly) and open access (buying power from a non-local supplier) become workable — no separate agreement needed per pair.

Relevant use cases:

- **[P2P Energy Trading](../use-cases/p2p-energy-trading/README.md)** — direct trade between consumers under a market operator's rules.
- **Open Access** — verified consumer credentials and meter digests make eligibility checks instant.
- **Demand-side flexibility** — aggregators dispatching pooled resources for demand response. The `DemandFlex*` schema family is published (see [Schemas — External](../schemas/external/README.md#demand-flexibility)); no use-case guide yet.

---

## Why these compound

With one common standard, the work is done once and reused everywhere: a consumer moving States arrives already trusted, any bank in India accepts a DISCOM-issued record for faster service, and a service proven in one State works elsewhere without rebuilding.

> Next: read **[Pilots and Status](pilots.md)** to see where IES is live today, or **[Common Questions](faq.md)** for the questions most often asked.
