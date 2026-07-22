# Getting Started

**India Energy Stack (IES)** is a common set of specifications for sharing data across the power sector. It works the way UPI works for banking — UPI holds no money of its own; money stays in the customer's bank, and UPI is only the shared rules that let any bank pay any other. **IES is the same idea, for energy data:** the data stays in the systems that already hold it, and IES specs let any two systems exchange and act on it directly — without replacing any existing system or standard.

{% hint style="info" %}
🧭 **New to IES?** **[What IES Is](concepts/what-ies-is.md)** tells the whole story on one page — the problem, the idea, what IES is and is not, what changes for each stakeholder, and where it's live. Unfamiliar terms (DID, DeDi, BAP/BPP, ARR…) link to the **[Glossary](glossary.md)** on first use.
{% endhint %}

IES is **live**. [Four pilot DISCOMs](concepts/what-ies-is.md#pilots-and-status) built their **adapter** — the small edge software that makes a system IES-ready (see **[What IES Is](concepts/what-ies-is.md#what-you-change-in-your-own-systems)**) — and demonstrated DER Visibility, Consumer Energy Passport, Consumer Meter Digest and Smart Meter Data Exchange in the 30-day Challenge (21 May – 21 June 2026).

{% hint style="info" %}
📄 **Printable version:** download this entire guide as a single PDF — [**ies-report.pdf**](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf). Schema reference material is included as an appendix at the end. Regenerated automatically whenever the docs change — see [Download PDF](download-pdf.md).
{% endhint %}

---

## How IES works — three steps

Every IES interaction follows the same three steps. They are the **spine of this entire GitBook**.

| Step | What it does | Example standard |
|---|---|---|
| **[1. Register](what-ies-provides/register.md)** | Every participant gets a verifiable digital identity and is listed in a shared directory. *Done once.* | [W3C Decentralised Identifiers](https://www.w3.org/TR/did-core/) |
| **[2. Discover](what-ies-provides/discover.md)** | Before every exchange, both systems look each other up, confirm the other is genuine, and agree on what will be exchanged and on what terms. *No bilateral arrangement is needed.* | [Beckn protocol](https://github.com/beckn/protocol-specifications-v2) |
| **[3. Exchange](what-ies-provides/exchange.md)** | Data moves using agreed field names and structure, following the public standard for that domain. Where the use case needs a durable record, a **verifiable credential** is issued that the holder keeps. | DLMS/COSEM, IEEE 2030.5, OpenADR; W3C VCs |

IES picks the right open standard for each step and publishes a specification on top. **IES does not write new standards.** Build to the IES specs once, and a system can connect to any other IES-ready system without fresh integration work.

---

## The building blocks

Two capabilities build on a shared identity foundation. The four capsules below orient you before you dive in.

### Identifiers and Addressing

The [DID](glossary.md#did) grammar IES uses to name every actor, asset, document, and dataset on the network — `did:web` for institutions, `did:key` / `did:jwk` for consumer wallets. All three are standard W3C DID methods; DeDi is a key-discovery layer for `did:web`, not a separate method. Internal numbering (consumer numbers, asset SAP codes) is preserved and wrapped, never replaced.

**Who should use this:** Every participant — this is the addressing layer below everything else.

### Registries and Directories

[DeDi](glossary.md#dedi)-based public registries that resolve identifiers to records and act as the trust layer for credentials and [Beckn](glossary.md#beckn). Covers the IES reference registries ([DISCOMs](glossary.md#discom), regulators, network), the per-participant registries you operate (Beckn subscriber, revocation, public-keys), and how to create them.

**Who should use this:** Every participant onboarding to IES. Start with [Setup Register](how-you-implement-ies/setup-register.md).

### Electricity Credentials

A framework for issuing, holding, and verifying **digital attestations** about energy assets and consumers, built on [W3C Verifiable Credentials](glossary.md#verifiable-credential-vc) and [DigiLocker](glossary.md#digilocker). Credential flows stand on their own — they do not require a [Beckn](glossary.md#beckn) network. Consumer-facing delivery happens over DigiLocker, a web portal, or any channel the issuer already runs; the Beckn network is what IES recommends for **B2B data exchange** (the next capability below).

> **v1 scope.** DISCOMs are the sole **issuer**; consumers (or authorized actors) are the **holder**; third parties **verify** or **receive** credentials depending on use case. Other issuer roles (SERCs, DER OEMs, government bodies) are supported architecturally but out of scope for v1.

**Who should use this:** DISCOMs, service providers doing KYC/address verification, fintech apps integrating with energy consumers.

### Data Exchange

A federated, policy-governed mechanism for discovering and exchanging structured energy datasets. Beckn always carries the **control plane** — discovery, offer, consent, contract, audit. The **payload** has two modes: it can ride **inline in the Beckn callback** for small datasets, or — for bulky / streaming / already-channelised data — Beckn hands off an **access method** (signed URL / SFTP / REST / [MQTT](glossary.md#mqtt) / Kafka / [OpenADR](glossary.md#openadr) / [XBRL](glossary.md#xbrl) artifact / [Akoma Ntoso](glossary.md#akoma-ntoso) document) that the consumer uses to pull or subscribe over that channel. Covers smart-meter telemetry ([DLMS-COSEM / IS 15959](glossary.md#dlms-cosem), [IEC 61968](glossary.md#iec-61968) / [CIM](glossary.md#cim) / [MultiSpeak](glossary.md#multispeak)), regulatory filings ([ARR](glossary.md#arr) submissions, tariff orders), and tariff / policy data.

**Who should use this:** DISCOMs, [SERCs](glossary.md#serc), [AMISPs](glossary.md#amisp), VAS providers, researchers, grid operators.

---

## How this guide is organised

Three top-level sections, each organised by the **Register / Discover / Exchange** spine.

### [What IES Provides](what-ies-provides/README.md)

The specifications. What is published.

| Section | What's in it |
|---|---|
| [What IES Is](concepts/what-ies-is.md) | The intro, on one page. Problem, UPI analogy, what IES is and is not, sector impact, the four pilots, FAQ. |
| [Register](what-ies-provides/register.md) | Verifiable digital identity (W3C DIDs) and the shared directory (DeDi) — one page. |
| [Discover](what-ies-provides/discover.md) | How two registered organisations find each other, agree terms and sign — the Beckn-protocol interaction (B2B). |
| [Exchange](what-ies-provides/exchange.md) | How data moves once discovered: the schemas, and where verifiable credentials (B2C) fit. |
| [Schemas](schemas/README.md) | The master vocabulary of IES — every domain object, its plain-language overview, and the schema that describes its shape; standards precedence, versioning, proposal flow. |

### [How you implement IES](how-you-implement-ies/README.md)

The action guides. What you do.

| Step | Action page | Time |
|---|---|---|
| 1 | [Setup Register](how-you-implement-ies/setup-register.md) | 1–2 days |
| 2 | [Issue Credentials](how-you-implement-ies/issue-credentials.md) *(credential use cases)* | ½ day |
| 3 | [Setup Exchange](how-you-implement-ies/setup-exchange.md) *(data-exchange use cases)* | 1–2 days |
| 4 | [Build your Internal-facing Adapter](how-you-implement-ies/build-adapter.md) | 1–4 weeks |
| 5 | [Conformance Checklist](how-you-implement-ies/conformance.md) | 1 day |

### [Use Case Implementation Guides](use-cases/README.md)

What you can ship, organised per the **[IES Documentation Template](use-cases/README.md#how-each-guide-is-organised)** so once you've read one, you know where to look in any other.

| Stage | Use cases |
|---|---|
| **Live in pilot** | [Consumer Energy Passport](use-cases/consumer-energy-passport/README.md) · [Consumer Meter Digest](use-cases/consumer-meter-digest/README.md) · [Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md) · [DER Visibility](use-cases/der-visibility/README.md) |
| **Work in progress** | [DISCOM Regulatory Filing](use-cases/discom-regulatory-filing/README.md) · [Policy as Code](use-cases/tariff-intelligence/README.md) · [P2P Energy Exchange](use-cases/p2p-energy-trading/README.md) |

---

## Choose your path

- **A DISCOM, regulator, or [NP](glossary.md#np) onboarding to the IES network for the first time?**
  → Go to [Setup Register](how-you-implement-ies/setup-register.md), the first step of [How you implement IES](how-you-implement-ies/README.md) — the same path the pilot DISCOMs followed in 30 days.
- **Issuing or verifying credentials about energy consumers or assets?**
  → Go to [Electricity Credentials](what-ies-provides/energy-credentials/README.md). You will also need the revocation + public-keys registries from the [Registries](what-ies-provides/register.md#the-directory-dedi) chapter.
- **Exchanging structured energy datasets (telemetry, filings, tariffs)?**
  → Go to [Data Exchange → Quick Start](how-you-implement-ies/setup-exchange.md#id-3.1-deploy-the-local-sandbox). You will also need a Beckn subscriber registry from the [Registries](what-ies-provides/register.md#the-directory-dedi) chapter.
- **Building a new application that needs both?**
  → Start with [Registries](what-ies-provides/register.md#the-directory-dedi) → then [Electricity Credentials](what-ies-provides/energy-credentials/README.md) (simpler integration surface) → then [Discover](what-ies-provides/discover.md) and [Exchange](what-ies-provides/exchange.md).
- **A decision-maker or reviewer?** Skim **[What IES Provides](what-ies-provides/README.md)** in order: What IES Is → Register → Discover → Exchange.
- **Picking a first use case?** Browse the table in **[Use Case Implementation Guides](use-cases/README.md)** — pilot cases at the top.

---

## Key terminology

A complete, plain-language glossary lives at **[Glossary](glossary.md)** (also in the left nav), covering identity ([DID](glossary.md#did), [DeDi](glossary.md#dedi), [VC](glossary.md#verifiable-credential-vc)), Beckn ([BAP](glossary.md#bap), [BPP](glossary.md#bpp), [ONIX](glossary.md#onix), [ERA](glossary.md#era)), the India energy sector ([DISCOM](glossary.md#discom), [AMISP](glossary.md#amisp), [SERC](glossary.md#serc), [ARR](glossary.md#arr), [MYT](glossary.md#myt), [HT/LT](glossary.md#ht-lt), [ToD](glossary.md#tod), [RDSS](glossary.md#rdss), [HES](glossary.md#hes), [MDMS](glossary.md#mdms)), and standards ([CIM](glossary.md#cim), [IEC 61968](glossary.md#iec-61968), [DLMS-COSEM](glossary.md#dlms-cosem), [MultiSpeak](glossary.md#multispeak), [OpenADR](glossary.md#openadr), [XBRL](glossary.md#xbrl), [Akoma Ntoso](glossary.md#akoma-ntoso), [DCAT 3](glossary.md#dcat-3), [MQTT](glossary.md#mqtt)).

---

## Prerequisites by capability

**Electricity credentials**

- An organisation registered with [API Setu](https://apisetu.gov.in) as a DigiLocker issuer (for DISCOMs issuing consumer credentials)
- Access to the IES Credential Service API (contact the IES team)
- A [CIS](glossary.md#cis) / billing database to look up consumer records

**Data exchange**

- Docker and Docker Compose (for local development)
- Access to the IES testnet (`nfh.global/testnet-deg`)
- A Beckn-compatible adapter (ONIX is provided; see Quick Start)

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

## Getting help & related repositories

Raise an issue or start a discussion in the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator). For testnet access and API keys, contact the IES team directly.

- [ies-docs](https://github.com/India-Energy-Stack/ies-docs) — IES architecture primitives and implementation guides
- [Digital Energy Grid (DEG)](https://github.com/Beckn-One/DEG) — upstream open protocol specification
- [DDM](https://github.com/beckn/DDM) — Decentralized Data Marketplace (`DatasetItem` schema family)
