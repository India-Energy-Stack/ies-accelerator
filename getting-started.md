# Getting Started

{% hint style="info" %}
**New here?** Unfamiliar terms (DID, DeDi, BAP/BPP, ERA, ARR…) link to the **[Glossary](glossary.md)** on first use. The Glossary is always available from the left nav.
{% endhint %}

This page gives you a five-minute orientation to IES before you dive into either capability.

---

## What is the India Energy Stack?

IES is an **open protocol and governance layer** for India's energy sector. It does not operate data — it defines the standards and interaction patterns that let diverse organisations share data and trust each other's claims.

IES has four developer-facing sections. The bottom two are the **foundations** every participant needs in place; the top two are the **capabilities** built on top of them.

### Identifiers and Addressing

The [DID](glossary.md#did) grammar IES uses to name every actor, asset, document, and dataset on the network — `did:web` for institutions and their assets, `did:key` / `did:jwk` for consumer wallets. All three are standard W3C DID methods; DeDi acts as a key-discovery layer for `did:web`, not as a separate method. Internal numbering (consumer numbers, asset SAP codes) is preserved and wrapped, never replaced.

**Who should use this:** Every participant — this is the addressing layer below everything else.

### Registries and Directories

[DeDi](glossary.md#dedi)-based public registries that resolve identifiers to records and act as the trust layer for credentials and [Beckn](glossary.md#beckn). Covers the IES reference registries ([DISCOMs](glossary.md#discom), regulators, network), the per-participant registries you need to operate (Beckn subscriber, revocation, public-keys), and the step-by-step process for creating them.

**Who should use this:** Every participant onboarding to IES. Start here with the [end-to-end onboarding checklist](./registries/README.md#end-to-end-onboarding-checklist).

### Energy Credentials

A framework for issuing, holding, and verifying **digital attestations** about energy assets and consumers, built on [W3C Verifiable Credentials](glossary.md#verifiable-credential-vc) and [DigiLocker](glossary.md#digilocker).

> **v1 scope.** DISCOMs are the sole **issuer**; consumers (or authorized actors on their behalf) are the **holder**; third parties **verify** or **receive** credentials depending on the use case. Other issuer roles (SERCs, DER OEMs, government bodies) are architecturally supported but out of scope for v1.

In v1, energy credentials enable:

- Consumers to carry a verified digital proof of their electricity connection
- DISCOMs to issue tamper-proof credentials without manual paper processes
- Third-party service providers to verify consumer identity and energy status instantly

**Who should use this:** DISCOMs, service providers doing KYC/address verification, fintech apps integrating with energy consumers.

### Data Exchange

A federated, policy-governed mechanism for discovering and exchanging structured energy datasets. Beckn always carries the **control plane** — discovery, offer, consent, contract, audit. The **payload** has two equally valid modes: it can ride **inline in the Beckn callback** when the dataset is small and a single signed message is the simplest workflow, or — for bulky / streaming / already-channelised data — Beckn hands off an **access method** (signed URL / SFTP / REST / [MQTT](glossary.md#mqtt) / Kafka / [OpenADR](glossary.md#openadr) / [XBRL](glossary.md#xbrl) artifact / [Akoma Ntoso](glossary.md#akoma-ntoso) document) that the consumer uses to pull or subscribe over the established channel. Covers:

- Smart meter telemetry — typically [DLMS-COSEM / IS 15959](glossary.md#dlms-cosem) at the field layer, [IEC 61968](glossary.md#iec-61968) / [CIM](glossary.md#cim) / [MultiSpeak](glossary.md#multispeak) between [HES](glossary.md#hes) and [MDM](glossary.md#mdms)
- Regulatory filings — [ARR](glossary.md#arr) submissions, tariff orders
- Tariff and policy data — rate structures, time-of-day surcharges

**Who should use this:** DISCOMs, [SERCs](glossary.md#serc), [AMISPs](glossary.md#amisp), VAS providers, researchers, grid operators.

---

## Choosing Your Path

- **A DISCOM, regulator, or [NP](glossary.md#np) onboarding to the IES network for the first time?**
  → Go to [Registries → Onboarding Checklist](./registries/README.md#end-to-end-onboarding-checklist).

- **Issuing or verifying credentials about energy consumers or assets?**
  → Go to [Energy Credentials → Onboarding Guide](./energy-credentials/README.md). You will also need the revocation + public-keys registries from the [Registries](./registries/README.md) chapter.

- **Exchanging structured energy datasets (telemetry, filings, tariffs)?**
  → Go to [Data Exchange → Quick Start](./data-exchange/README.md#quick-start--run-a-local-exchange-in-10-minutes). You will also need a Beckn subscriber registry from the [Registries](./registries/README.md) chapter.

- **Building a new application that needs both?**
  → Start with [Registries](./registries/README.md) (foundation) → then [Energy Credentials](./energy-credentials/README.md) (simpler integration surface) → then [Data Exchange](./data-exchange/README.md).

---

## Key Terminology

A complete, plain-language glossary lives at **[Glossary](glossary.md)** (also in the left nav). It covers identity ([DID](glossary.md#did), [DeDi](glossary.md#dedi), [VC](glossary.md#verifiable-credential-vc)), Beckn ([BAP](glossary.md#bap), [BPP](glossary.md#bpp), [ONIX](glossary.md#onix), [ERA](glossary.md#era)), India energy sector ([DISCOM](glossary.md#discom), [AMISP](glossary.md#amisp), [SERC](glossary.md#serc), [ARR](glossary.md#arr), [MYT](glossary.md#myt), [HT/LT](glossary.md#ht-lt), [ToD](glossary.md#tod), [RDSS](glossary.md#rdss), [HES](glossary.md#hes), [MDMS](glossary.md#mdms)), and standards ([CIM](glossary.md#cim), [IEC 61968](glossary.md#iec-61968), [DLMS-COSEM](glossary.md#dlms-cosem), [MultiSpeak](glossary.md#multispeak), [OpenADR](glossary.md#openadr), [XBRL](glossary.md#xbrl), [Akoma Ntoso](glossary.md#akoma-ntoso), [DCAT 3](glossary.md#dcat-3), [MQTT](glossary.md#mqtt)).

---

## Prerequisites by Capability

### Energy Credentials

- An organisation registered with [API Setu](https://apisetu.gov.in) as a DigiLocker issuer (for DISCOMs issuing consumer credentials)
- Access to the IES Credential Service API (contact the IES team)
- A [CIS](glossary.md#cis) / billing database to look up consumer records

### Data Exchange

- Docker and Docker Compose (for local development)
- Access to the IES testnet (`nfh.global/testnet-deg`)
- A Beckn-compatible adapter (ONIX is provided; see Quick Start)

---

## Getting Help

Raise an issue or start a discussion in the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator). For testnet access and API keys, contact the IES team directly.
