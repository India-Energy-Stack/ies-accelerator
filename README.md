---
layout:
  title:
    visible: false
---

# Getting Started

The **India Energy Stack (IES)** is an initiative of the **Ministry of Power**, Government of India, to build unified digital rails for the power sector — a common set of open specifications that lets any two systems in the sector share verified energy data without bespoke, pair-by-pair integration. **REC** is the nodal agency and **FSR Global** is the knowledge partner.

IES works the way UPI works for payments: it holds no data of its own. Data stays in the systems that already hold it — DISCOM software, metering platforms, vendor databases — and IES specifies how those systems identify each other, find each other, and exchange data in a common, verifiable form.

---

## How IES works — Register, Discover, Exchange

Every IES interaction follows the same three steps:

- **Register** — every participant gets a verifiable digital identity (a [W3C DID](https://www.w3.org/TR/did-core/)) and a listing in a shared directory (DeDi). Done once.
- **Discover** — before an exchange, the two systems look each other up, verify each other, and agree terms over the [Beckn protocol](https://github.com/beckn/protocol-specifications-v2). No bilateral arrangement needed.
- **Exchange** — data moves over the same signed Beckn channel that Discover established, shaped by published [IES schemas](schemas-ies/README.md) built on open standards (DLMS/COSEM for meter data, IEEE 2030.5 for DER, OpenADR for demand response). Where a durable record is needed, the exchange produces a [W3C Verifiable Credential](https://www.w3.org/TR/vc-data-model/) the holder keeps — in DigiLocker, for consumers.

The specifications cover five building blocks: **Register**, **Discover**, **Exchange**, **Verifiable Credentials**, and the **Security** posture that runs through all of them. IES selects the right open standard for each and publishes a specification that builds on it — IES does not write new standards, and it is not a platform, a database, or a product.

## What this GitBook is

This GitBook is the **technical reference** for building on IES: the schema definitions with their canonical URLs, per-use-case implementation guides with step-by-step checklists, and role-based adoption pathways. If you are here to build something, go straight to:

- **[Schemas Overview](what-ies-provides/schemas-overview/README.md)** — what each schema is for, in plain language
- **[Schemas](schemas-ies/README.md)** — the developer catalog: field references, canonical URIs, versions
- **Use Case Implementation Guides** — end-to-end build instructions with checklists: [Consumer Energy Passport](use-cases/consumer-energy-passport/README.md), [Consumer Meter Digest](use-cases/consumer-meter-digest/README.md), [Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md), [DER Visibility](use-cases/der-visibility/README.md), [P2P Energy Transaction](use-cases/p2p-energy-trading/README.md)
- **[Pathways](pathways/README.md)** — where to start, by the kind of organisation you are

## Before you build

Whatever you are building, every participant completes the same three prerequisites first: **register your organisation in the DeDi directory, create your `did:web` identity, and stand up your Beckn ONIX adapter**. Each implementation guide starts its checklist from these steps, and the **[Concepts](how-you-implement-ies/README.md)** section walks through each one in detail.

## The full story

This reference deliberately stays lean. For a detailed understanding of IES — the concepts, the in-depth architecture, the acceleration and adoption strategy, governance, and the pilot record — read the **IES report** at **[indiaenergystack.in/report](https://indiaenergystack.in/report)**.

**Where things stand:** the specifications are published and versioned in this repository. Four pilot DISCOMs — PVVNL (Uttar Pradesh), APEPDCL (Andhra Pradesh), DGVCL (Gujarat) and Tata Power (Maharashtra) — completed a 30-day DISCOM Challenge, each building an IES adapter and demonstrating the first four use cases (DER Visibility, Consumer Energy Passport, Consumer Meter Digest, Smart Meter Data Exchange) against the specifications and the pilot sandbox. That is a completed, historical outcome, not a claim that any pilot is running today.

{% hint style="info" %}
📄 **Printable version:** the deliverable subset of this reference is published as a single PDF — [**ies-report.pdf**](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf).
{% endhint %}

## Get in touch

- **IES Secretariat** — `ies.secretariat@fsrglobal.org`
- **REC (Nodal Agency)** — `ies@recindia.com`
- **Issues, discussions, contributions** — [github.com/India-Energy-Stack/ies-accelerator](https://github.com/India-Energy-Stack/ies-accelerator)
