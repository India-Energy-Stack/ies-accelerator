# Pilots and Status

IES is **live**. The specifications have been published on this GitBook, the sandbox is working, and four pilot DISCOMs in four States have built their IES adapter and demonstrated a first set of live use cases.

---

## The 30-day DISCOM Challenge

**21 May 2026 – 21 June 2026.** Four pilot DISCOMs, spread across four States, built their IES adapters and demonstrated the four use cases live in the sandbox environment.

---

## Use cases demonstrated

| Use case | What was demonstrated | Before IES |
|---|---|---|
| **[DER Visibility](../use-cases/der-visibility/README.md)** | Solar unit registered with a verified digital identity; grid operator visibility confirmed | No reliable sector-wide method existed |
| **[Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md)** | Energy Passport issued and stored in DigiLocker; consumer able to share it for a green loan, subsidy claim or service enrolment | Not possible earlier: no portable, verifiable consumer energy record existed |
| **[Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md)** | Verifiable record of consumption history, reusable across DISCOMs and States without repeat verification | Manual and limited to a single DISCOM; not reusable elsewhere |
| **[Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md)** | IES-compliant data exchange completed between DISCOM and AMISP without a bilateral integration agreement | Weeks to months of bilateral integration per pair |

---

## What "live in pilot" means

For each demonstration:

- An IES adapter (Beckn ONIX reference + DISCOM-specific mapping) running at the DISCOM
- A `did:web` identity published and resolvable
- A subscriber record in the IES network registry
- An issued credential (Passport, Digest) or a completed exchange (meter data) signed by the DISCOM's key
- Verified end-to-end by a counterparty (another DISCOM, a wallet, the IES Secretariat)

The artefacts — example payloads, schemas, configuration — are public in this repository.

---

## What is being added next

- **P2P Energy Trading** — schema published; pilot integrations being staged. See [external schemas](../schemas/external/README.md#energy-trading-p2p).
- **OutageNotification** — [v0.1](../schemas/OutageNotification/v0.1/README.md) is published; no IES use-case guide yet.

---

## The next phase

All State Governments, Union Territory Administrations and entities in the power sector are invited to take part. The minimum to participate is the same for every organisation:

1. Create a digital identity and list your organisation in the shared directory.
2. Install the adapter once.
3. Pass the basic conformance check.

After this, every new partner connects without fresh integration work. The implementation path is in **[How you implement IES](../how-you-implement-ies/README.md)**.

---

## Who is invited

| | |
|---|---|
| Distribution utilities (DISCOMs) | GENCOs and TRANSCOs |
| State and National Load Despatch Centres (SLDCs, NLDC) | Central and State electricity regulatory commissions; Forum of Regulators |
| Metering agencies (AMISPs) | Equipment manufacturers (EV, metering OEMs) |
| Technology and analytics providers | Aggregators (DER, demand response) |
| Financial institutions using verified energy data | State Governments and Union Territory Administrations |

---

## Get in touch

- **IES Secretariat** — `ies.secretariat@fsrglobal.org`
- **REC (Nodal Agency)** — `ies@recindia.com`
- **Issues, discussions, contributions** — [github.com/India-Energy-Stack/ies-accelerator](https://github.com/India-Energy-Stack/ies-accelerator)
- **The full repository** — this GitBook is rendered from the source at the link above.
