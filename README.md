# India Energy Stack — Accelerator

The **India Energy Stack (IES) Accelerator** is the developer hub for building on top of India's open energy infrastructure. It provides everything you need to integrate with two core capabilities of the IES platform:

| Capability | What it does |
|---|---|
| [IES Energy Credentials](./energy-credentials/README.md) | Issue, hold, and verify cryptographically signed digital credentials for energy assets and consumers |
| [IES Data Exchange](./data-exchange/README.md) | Discover and exchange structured energy datasets — telemetry, regulatory filings, tariff policies — over the Beckn protocol |

---

## Why IES?

The Indian power sector runs on data that is siloed, bespoke, and hard to trust. Regulatory filings arrive as PDFs. Telemetry lives inside proprietary MDMS systems. Subsidy eligibility is verified manually. Credentials that prove ownership, green certification, or consumer identity have no standard form.

IES changes this by providing a **shared digital infrastructure layer** — open standards, verifiable data, and interoperable protocols — so that every actor in the energy ecosystem can transact with confidence.

```
Generators · Prosumers · DISCOMs · Regulators · Aggregators · Consumers
                            ↕
               India Energy Stack (IES)
          ┌──────────────────────────────────┐
          │  Energy Credentials              │  ← trust layer
          │  (W3C VCs + DigiLocker)          │
          ├──────────────────────────────────┤
          │  Data Exchange                   │  ← data layer
          │  (Beckn Protocol + IES schemas)  │
          └──────────────────────────────────┘
                            ↕
             Physical energy infrastructure
```

---

## Where to Start

**New to IES?** Read [Getting Started](./getting-started.md) for a five-minute orientation.

**Integrating Energy Credentials?** Go to the [Energy Credentials onboarding guide](./energy-credentials/onboarding.md).

**Building a data exchange application?** Go to the [Data Exchange quick start](./data-exchange/quick-start.md).

---

## Key Standards and Protocols

| Standard | Role in IES |
|---|---|
| [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/) | Data model for signed, machine-verifiable credentials |
| [W3C Decentralized Identifiers (DIDs)](https://www.w3.org/TR/did-core/) | Cryptographic identity for issuers, holders, and verifiers |
| [Beckn Protocol v2.0](https://becknprotocol.io) | Open peer-to-peer protocol for energy dataset discovery and exchange |
| [OpenADR 3.1.0](https://www.openadr.org) | Standard for telemetry reports (meter readings, demand signals) |
| [DigiLocker](https://digilocker.gov.in) | India's national digital document wallet — consumer-facing credential store |

---

## Related Repositories

- [ies-docs](https://github.com/India-Energy-Stack/ies-docs) — IES architecture primitives and implementation guides
- [Digital Energy Grid (DEG)](https://github.com/Beckn-One/DEG) — upstream open protocol specification
- [DDM](https://github.com/beckn/DDM) — Dataset Descriptor Model (`DatasetItem` schema)
