# Getting Started

This page gives you a five-minute orientation to IES before you dive into either capability.

---

## What is the India Energy Stack?

IES is an **open protocol and governance layer** for India's energy sector. It does not operate data — it defines the standards and interaction patterns that let diverse organisations share data and trust each other's claims.

IES has four developer-facing sections. The bottom two are the **foundations** every participant needs in place; the top two are the **capabilities** built on top of them.

### Identifiers and Addressing

The DID grammar IES uses to name every actor, asset, document, and dataset on the network — `did:web` for institutions, `did:key` / `did:jwk` for consumers, `did:dedi` for registry-anchored records. Internal numbering (consumer numbers, asset SAP codes) is preserved and wrapped, never replaced.

**Who should use this:** Every participant — this is the addressing layer below everything else.

### Registries and Directories

DeDi-based public registries that resolve identifiers to records and act as the trust layer for credentials and Beckn. Covers the IES reference registries (DISCOMs, regulators, network), the per-participant registries you need to operate (Beckn subscriber, revocation, public-keys), and the step-by-step process for creating them.

**Who should use this:** Every participant onboarding to IES. Start here with the [end-to-end onboarding checklist](./registries/required-registries.md#end-to-end-onboarding-checklist).

### Energy Credentials

A framework for issuing, holding, and verifying **digital attestations** about energy assets and consumers. Built on W3C Verifiable Credentials and DigiLocker, energy credentials enable:

- Consumers to carry a verified digital proof of their electricity connection
- DISCOMs to issue tamper-proof credentials without manual paper processes
- Third-party service providers to verify consumer identity and energy status instantly

**Who should use this:** DISCOMs, service providers doing KYC/address verification, fintech apps integrating with energy consumers.

### Data Exchange

A Beckn Protocol v2.0 network for discovering and exchanging structured energy datasets. Unlike file transfers or point-to-point APIs, the IES Data Exchange provides a **federated, policy-governed, auditable** mechanism for data flows including:

- Smart meter telemetry (AMI data, 15-min interval readings)
- Regulatory filings (ARR submissions, tariff orders)
- Tariff and policy data (rate structures, time-of-day surcharges)

**Who should use this:** DISCOMs, SERCs, AMISPs, VAS providers, researchers, grid operators.

---

## Choosing Your Path

```
Are you a DISCOM / regulator / NP onboarding to the IES network for the first time?
  → Go to: Registries and Directories → Required Registries → Onboarding Checklist

Are you issuing or verifying credentials about energy consumers or assets?
  → Go to: Energy Credentials → Onboarding Guide
  (you will need the revocation + public-keys registries from Registries section)

Are you exchanging structured energy datasets (telemetry, filings, tariffs)?
  → Go to: Data Exchange → Onboarding Guide
  (you will need a Beckn subscriber registry from Registries section)

Are you building a new application that needs both?
  → Start with Registries (foundation)
  → Then Energy Credentials (simpler integration surface)
  → Then Data Exchange
```

---

## Key Terminology

| Term | Meaning |
|---|---|
| **DID** | Decentralized Identifier — a cryptographic, self-sovereign identity (e.g. `did:ies:discom-tpddl`) |
| **VC / Verifiable Credential** | A signed digital document asserting claims about a subject, following the W3C standard |
| **ERA** | Energy Resource Address — a unique digital identifier for any energy asset |
| **BAP** | Beckn Application Platform — the consumer/buyer side in a Beckn data exchange |
| **BPP** | Beckn Provider Platform — the provider/seller side in a Beckn data exchange |
| **ONIX** | The Beckn adapter used by IES — handles signing, routing, and schema validation |
| **DISCOM** | Distribution company — electricity distributor |
| **AMISP** | Advanced Metering Infrastructure Service Provider |
| **SERC** | State Electricity Regulatory Commission |
| **ARR** | Aggregate Revenue Requirement — annual regulatory cost filing |

---

## Prerequisites by Capability

### Energy Credentials

- An organisation registered with [API Setu](https://apisetu.gov.in) as a DigiLocker issuer (for DISCOMs issuing consumer credentials)
- Access to the IES Credential Service API (contact the IES team)
- A CIS/billing database to look up consumer records

### Data Exchange

- Docker and Docker Compose (for local development)
- Access to the IES testnet (`nfh.global/testnet-deg`)
- A Beckn-compatible adapter (ONIX is provided; see Quick Start)

---

## Getting Help

Raise an issue or start a discussion in the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator). For testnet access and API keys, contact the IES team directly.
