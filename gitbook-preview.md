# GitBook Preview — Local Walkthrough

This file emulates what the rendered GitBook will look like in `india-energy-stack/ies-accelerator`, so you can review the structure and flow without pushing to GitBook's preview environment. Each section below corresponds to one page in the actual book.

**Review-only artifact, not for merge.** This file is `gitbook-preview.md`, intentionally excluded from `SUMMARY.md` so it never appears in the published book. It exists to let a reviewer walk the rendered structure locally. **Run `git rm gitbook-preview.md && git commit -m "docs(preview): remove local review aid before merge"` before merging the PR to `main`** — keeping it in `main` would leave dead weight in the repo for no reader benefit.

---

## What this preview cannot show

| GitBook will render… | This file shows… |
|---|---|
| **Left nav** always visible | ASCII tree below |
| **Mermaid diagrams** as SVG | ASCII art approximation; original Mermaid source linked |
| **Hint callouts** (`{% hint %}`) as styled boxes | ASCII boxes |
| **Page link previews** on hover | Plain markdown links |
| **Code-block syntax highlighting** | Plain code fences |

---

## 🗂 Left navigation (from SUMMARY.md, top-level only)

```
┌─ India Energy Stack — Accelerator ─────────────────┐
│                                                    │
│   📄 Home                                          │
│   📄 Getting Started                               │
│   📚 Glossary                       ← NEW          │
│   ─────                                            │
│   📁 Identifiers and Addressing                    │
│   📁 Registries and Directories                    │
│   📁 Energy Credentials                            │
│   📁 Data Exchange                                 │
│   📁 Use Cases                                     │
│                                                    │
└────────────────────────────────────────────────────┘
```

The Glossary is the new top-level entry, present in this sidebar on every page in the book.

---

# 📄 PAGE 1 — Home

> Source: [README.md](./README.md)

---

# India Energy Stack — Accelerator

**India Energy Stack (IES)** is an open digital infrastructure layer for India's power sector — protocols and shared registries that let [DISCOMs↗](glossary.md#discom), [AMISPs↗](glossary.md#amisp), regulators, and consumers exchange data and trust each other's claims, without anyone owning the network.

```
╔══════════════════════════════════════════════════════════════════╗
║ MERMAID DIAGRAM — Renders as SVG in actual GitBook               ║
║──────────────────────────────────────────────────────────────────║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │ Generators · Prosumers · DISCOMs · Regulators ·          │   ║
║  │ Aggregators · Consumers                                  │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                              │                                   ║
║  ┌─ India Energy Stack (IES) ─────────────────────────────────┐ ║
║  │                                                            │ ║
║  │  ┌──────────────────────────────────────────────────────┐ │ ║
║  │  │ Energy Credentials                                   │ │ ║
║  │  │ W3C VCs + DigiLocker                                 │ │ ║
║  │  │ (trust layer)                                        │ │ ║
║  │  └──────────────────────────────────────────────────────┘ │ ║
║  │  ┌──────────────────────────────────────────────────────┐ │ ║
║  │  │ Data Exchange                                        │ │ ║
║  │  │ Beckn control plane + IES schemas                    │ │ ║
║  │  │ (data layer)                                         │ │ ║
║  │  └──────────────────────────────────────────────────────┘ │ ║
║  │  ┌──────────────────────────────────────────────────────┐ │ ║
║  │  │ Registries and Directories                           │ │ ║
║  │  │ DeDi: namespaces + records                           │ │ ║
║  │  │ (discovery + revocation)                             │ │ ║
║  │  └──────────────────────────────────────────────────────┘ │ ║
║  │  ┌──────────────────────────────────────────────────────┐ │ ║
║  │  │ Identifiers and Addressing                           │ │ ║
║  │  │ DIDs: did:web · did:key · did:dedi                   │ │ ║
║  │  │ (identity foundation)                                │ │ ║
║  │  └──────────────────────────────────────────────────────┘ │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                              │                                   ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │ Physical energy infrastructure                           │   ║
║  │ (meters · feeders · DERs · grid)                         │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

This **Accelerator** is the developer hub for building on it. Four core sections:

| Section | What it does |
|---|---|
| **IES Identifiers and Addressing** | [DIDs↗](glossary.md#did) and addressing grammar for DISCOMs, regulators, consumers, assets, meters, credentials, and datasets |
| **IES Registries and Directories** | [DeDi↗](glossary.md#dedi)-based public registries — namespaces, the IES reference registries, [Beckn↗](glossary.md#beckn) subscriber registries, revocation, public-keys |
| **IES Energy Credentials** | Issue, hold, and verify cryptographically signed digital credentials for energy assets and consumers |
| **IES Data Exchange** | Discover and contract dataset exchanges over Beckn — telemetry, regulatory filings, tariff policies. Payload uses the sector standard appropriate to the dataset (signed URL / REST / MQTT / OpenADR) |

---

## Where to Start

- **New to IES?** Read **Getting Started** for a five-minute orientation.
- **Onboarding as a DISCOM, regulator, or [NP↗](glossary.md#np)?** Go to the **Required Registries onboarding checklist**.
- **Integrating Energy Credentials?** Go to the **Energy Credentials onboarding guide**.
- **Building a data exchange application?** Go to the **Data Exchange quick start**.
- **Need a term defined?** Check the always-visible **Glossary**.

---

## Why IES?

The Indian power sector runs on data that is siloed, bespoke, and hard to trust — regulatory filings arrive as PDFs, telemetry lives inside proprietary [MDMS↗](glossary.md#mdms) systems, subsidy eligibility is verified manually, and credentials of ownership or identity have no standard form. IES provides a **shared digital infrastructure layer** — open standards, verifiable data, and interoperable protocols — so that every actor in the ecosystem can transact on common ground.

---

*(homepage continues with Key Standards and Protocols table and Related Repositories — see README.md for the full content)*

---

# 📄 PAGE 2 — Getting Started

> Source: [getting-started.md](./getting-started.md)

---

# Getting Started

```
╔══════════════════════════════════════════════════════════════════╗
║ ℹ️  HINT (info) — renders as styled callout in GitBook           ║
║──────────────────────────────────────────────────────────────────║
║                                                                  ║
║  New here? Unfamiliar terms (DID, DeDi, BAP/BPP, ERA, ARR…)      ║
║  link to the Glossary on first use. The Glossary is always       ║
║  available from the left nav.                                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

This page gives you a five-minute orientation to IES before you dive into either capability.

## What is the India Energy Stack?

IES is an **open protocol and governance layer** for India's energy sector. It does not operate data — it defines the standards and interaction patterns that let diverse organisations share data and trust each other's claims.

IES has four developer-facing sections. The bottom two are the **foundations** every participant needs in place; the top two are the **capabilities** built on top of them.

### Identifiers and Addressing
The [DID↗](glossary.md#did) grammar IES uses to name every actor, asset, document, and dataset on the network…

### Registries and Directories
[DeDi↗](glossary.md#dedi)-based public registries that resolve identifiers to records and act as the trust layer for credentials and [Beckn↗](glossary.md#beckn)…

### Energy Credentials
A framework for issuing, holding, and verifying **digital attestations** about energy assets and consumers, built on [W3C Verifiable Credentials↗](glossary.md#verifiable-credential-vc) and [DigiLocker↗](glossary.md#digilocker).

> **v1 scope.** DISCOMs are the sole **issuer**; consumers (or authorized actors on their behalf) are the **holder**; third parties **verify** or **receive** credentials depending on the use case. Other issuer roles (SERCs, DER OEMs, government bodies) are architecturally supported but out of scope for v1.

In v1, energy credentials enable:
- Consumers to carry a verified digital proof of their electricity connection
- DISCOMs to issue tamper-proof credentials without manual paper processes
- Third-party service providers to verify consumer identity and energy status instantly

### Data Exchange
A federated, policy-governed mechanism for discovering and exchanging structured energy datasets. Beckn is the **control plane** — discovery, offer, consent, contract, audit. Dataset bytes move over the sector standard appropriate to each class (signed URL / REST / [MQTT↗](glossary.md#mqtt) / [OpenADR↗](glossary.md#openadr) / [XBRL↗](glossary.md#xbrl) / [Akoma Ntoso↗](glossary.md#akoma-ntoso)). Covers:

- Smart meter telemetry — typically [DLMS-COSEM / IS 15959↗](glossary.md#dlms-cosem) at the field layer, [IEC 61968↗](glossary.md#iec-61968) / [CIM↗](glossary.md#cim) / [MultiSpeak↗](glossary.md#multispeak) between [HES↗](glossary.md#hes) and [MDM↗](glossary.md#mdms)
- Regulatory filings — [ARR↗](glossary.md#arr) submissions, tariff orders
- Tariff and policy data — rate structures, time-of-day surcharges

---

## Choosing Your Path

- **A DISCOM, regulator, or [NP↗](glossary.md#np) onboarding to the IES network for the first time?**
  → Go to **Required Registries → Onboarding Checklist**.
- **Issuing or verifying credentials about energy consumers or assets?**
  → Go to **Energy Credentials → Onboarding Guide**.
- **Exchanging structured energy datasets (telemetry, filings, tariffs)?**
  → Go to **Data Exchange → Quick Start**.
- **Building a new application that needs both?**
  → Start with **Registries** (foundation) → then **Energy Credentials** (simpler integration surface) → then **Data Exchange**.

---

*(rest of Getting Started — Key Terminology pointer, Prerequisites by Capability, Getting Help — see getting-started.md)*

---

# 📚 PAGE 3 — Glossary

> Source: [glossary.md](./glossary.md) — full 40+ term list. Excerpt below.

---

# Glossary

Plain-language definitions for every acronym and term used across this book. Each term is anchor-linked from its first use in a chapter — click any link to jump directly to the definition below.

```
╔══════════════════════════════════════════════════════════════════╗
║ ℹ️  HINT (info)                                                   ║
║──────────────────────────────────────────────────────────────────║
║                                                                  ║
║  This page is always visible in the left nav. If you hit a term  ║
║  you don't recognise, come back here.                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Identity and credentials

### DID
**Decentralized Identifier** — a globally unique, cryptographically verifiable identifier of the form `did:method:identifier` (e.g. `did:web:ies.tpddl.in`). Defined by the W3C DID Core standard. Resolves to a DID Document containing public keys and service endpoints. IES uses DIDs to name every participant, asset, and credential issuer.

### DeDi
**Decentralized Directory** — the public registry primitive IES uses for namespaces, network membership, public keys, revocation, and Beckn subscriber records. A DeDi record has a `subscriber_id` and `record_id` and is looked up via a public HTTPS URL.

### Verifiable Credential (VC)
A tamper-evident JSON-LD document containing claims about a subject (the **holder**), signed by an **issuer**, that any party (the **verifier**) can validate offline using the issuer's published public key.

### Issuer / Holder / Verifier
The three roles in any credential exchange. **Issuer** signs and emits the credential. **Holder** keeps it. **Verifier** receives a presentation and checks the signature.

*(~37 more terms across Data exchange/Beckn, India energy sector, and Standards/protocols sections — see glossary.md)*

---

# 📁 PAGE 4 — Energy Credentials (chapter intro)

> Source: [energy-credentials/README.md](./energy-credentials/README.md)

---

# Energy Credentials for DISCOMs

```
╔══════════════════════════════════════════════════════════════════╗
║ ℹ️  HINT (info)                                                   ║
║──────────────────────────────────────────────────────────────────║
║                                                                  ║
║  v1 scope. DISCOMs are the sole issuer of energy credentials     ║
║  about consumers, meters, and assets. Holders are consumers      ║
║  (or authorized actors acting on their behalf). Verifiers /      ║
║  recipients are third parties depending on the use case —        ║
║  banks, marketplaces, regulators, fintechs. Other issuer roles   ║
║  (SERCs, DER OEMs, government bodies) are architecturally        ║
║  supported but out of scope for v1.                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

This chapter is a complete, self-contained guide for a DISCOM tech team to start **issuing electricity credentials to consumers**. It walks from first principles through running the credential service, signing your first credential, and delivering it to consumers via [DigiLocker↗](../glossary.md#digilocker) or directly.

You do not need any prior knowledge of [Verifiable Credentials↗](../glossary.md#verifiable-credential-vc). Every concept used downstream is explained in Core Concepts.

### Credential lifecycle at a glance

```
╔══════════════════════════════════════════════════════════════════╗
║ MERMAID sequenceDiagram — renders as SVG in actual GitBook       ║
║──────────────────────────────────────────────────────────────────║
║                                                                  ║
║   DISCOM             Consumer/             Verifier/             ║
║   (Issuer)           Authorized            Recipient             ║
║                      Holder                                      ║
║      │                  │                     │                  ║
║      │ [Build CustomerCredential from CIS/NMS │                  ║
║      │  data; sign with OpenCred private key] │                  ║
║      │                  │                     │                  ║
║   1. │── Issue ─────────>│                     │                  ║
║      │ (DigiLocker Pull  │                     │                  ║
║      │  URI / DID push)  │                     │                  ║
║      │                   │                     │                  ║
║      │   [Hold in DigiLocker or               │                  ║
║      │    DID-controlled wallet]              │                  ║
║      │                   │                     │                  ║
║      │                2. │── Present ────────>│                  ║
║      │                   │ (push/share/QR)    │                  ║
║      │                   │                     │                  ║
║      │                   │  [Verify signature against            ║
║      │                   │   DISCOM's published public key]      ║
║      │                   │                     │                  ║
║   3. │<── (optional) revocation check in DeDi ─│                  ║
║      │                   │                     │                  ║
║      │                4. │<── Service granted /                  ║
║      │                   │    KYC complete ───│                  ║
║      │                   │                     │                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

*(chapter continues with What an Electricity Credential Is, sub-profiles, DISCOM Issuance Flow — see energy-credentials/README.md)*

---

# 📁 PAGE 5 — Data Exchange (chapter intro)

> Source: [data-exchange/README.md](./data-exchange/README.md)

---

# IES Data Exchange

**IES Data Exchange** is a federated, policy-governed way for energy-sector participants — [AMISPs↗](../glossary.md#amisp), [DISCOMs↗](../glossary.md#discom), [SERCs↗](../glossary.md#serc), and others — to discover, contract, and exchange structured datasets. [Beckn↗](../glossary.md#beckn) is the **control plane**: it carries discovery, offer, consent, contract, and audit. The dataset bytes themselves move over the sector standard appropriate to each dataset class — a signed download URL for an [XBRL↗](../glossary.md#xbrl) filing, an [MQTT↗](../glossary.md#mqtt) topic for near-real-time telemetry, [OpenADR↗](../glossary.md#openadr) for DR events, and so on — handed off via Beckn's `accessMethod` field.

## The Problem It Solves

…IES Data Exchange replaces these ad-hoc arrangements with **two complementary layers**:

1. **Control plane (Beckn Protocol v2.0 + IES schemas)** — how participants find each other, negotiate terms, give consent, sign contracts, and produce auditable records.
2. **Data plane (existing sector standards)** — how the bytes actually move, using whatever protocol the dataset class already standardises on (DLMS-COSEM, IEC 61968 / CIM / MultiSpeak, OpenADR, XBRL, Akoma Ntoso, or a plain signed URL).

## How It Works

…

### Why Beckn is not the payload wire

Wrapping every meter reading or every byte of a 50 MB filing in a signed Beckn message would be operationally heavy and would duplicate work the sector standards already do well. **Beckn coordinates; the existing protocols move bytes.** Expect **batch or near-real-time delivery after MDM validation** for smart-meter data; sub-minute streaming uses a transport credential handed off via Beckn, not Beckn itself.

## What Data Can Be Exchanged

The devkit ships **prebuilt schemas** for three IES dataset types. *These are examples seen in utility integrations; confirm the actual interface with your AMISP / HES / vendor stack.*

| Dataset (`schema`) | Beckn role | Common integration examples | Transfer pattern | Confirm with your vendor |
|---|---|---|---|---|
| Smart meter telemetry (`IES_Report`) | discovery + contract + consent + audit | Field: **DLMS-COSEM / IS 15959**. HES↔MDM: **IEC 61968-9 / CIM / MultiSpeak v3.0**. Optional event / near-real-time: **MQTT 5.0**. **OpenADR 3.1.0** for DR / DER events only — *not* generic interval reads. | Batch or near-real-time after MDM validation; signed URL or REST for bulk; MQTT for subscribed events | Which standard is actually deployed on your HES↔MDM interface and field network |
| ARR filing (`IES_ARR_Filing`) | discovery + contract + audit | **XBRL / iXBRL** (target). Current SERC portal practice: PDF/A + spreadsheet annexures. | HTTPS REST or signed object URL | Which annexure schema your SERC accepts today |
| Tariff policy (`IES_Policy` + `IES_Program`) | discovery + contract | Order text: **Akoma Ntoso / LegalDocML** XML. Schedules / slabs / [ToD↗](../glossary.md#tod) / subsidies: versioned CSV / JSON / JSON-LD with [DCAT 3↗](../glossary.md#dcat-3) metadata. | HTTPS REST or signed artifact | How your state publishes tariff orders today |

*(chapter continues with Key Components table — BAP, BPP, ONIX, IES Networks, sandbox-bpp/sandbox-bap — and Sections in This Chapter, Mock BPP planned, Related Repositories — see data-exchange/README.md)*

---

# 📁 PAGE 6 — Identifiers / Concepts (Mermaid before JSON)

> Source: [identifiers/concepts.md](./identifiers/concepts.md)

---

## What a DID Document contains

A DID string is *just* an identifier; what makes it useful is the DID Document it resolves to — the JSON that publishes the subject's public keys and service endpoints.

```
╔══════════════════════════════════════════════════════════════════╗
║ MERMAID flowchart — renders as SVG in actual GitBook             ║
║──────────────────────────────────────────────────────────────────║
║                                                                  ║
║   ┌──────────────────┐    resolve    ┌────────────────────┐     ║
║   │ DID string       │  ──────────>  │ DID Document       │     ║
║   │ did:web:ies.     │               │ (JSON)             │     ║
║   │ tpddl.in         │               │                    │     ║
║   └──────────────────┘               └─────────┬──────────┘     ║
║                                                │                 ║
║                          ┌─────────────────────┼─────────────┐  ║
║                          │                     │             │  ║
║                          ▼                     ▼             ▼  ║
║              ┌────────────────────┐ ┌──────────────┐ ┌─────────╗║
║              │ verificationMethod │ │ assertion-   │ │ service  ║
║              │ public keys a      │ │ Method       │ │ endpoints║
║              │ verifier uses to   │ │ which keys   │ │ (OpenCred║
║              │ check signatures   │ │ may issue    │ │ BAP/BPP  ║
║              │                    │ │ credentials  │ │ URLs)    ║
║              └────────────────────┘ └──────────────┘ └─────────╝║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

A minimal DID Document for an IES [DISCOM↗](../glossary.md#discom) looks like:

```json
{ ...full JSON example follows... }
```

---

# 📁 PAGE 7 — Data Exchange / Architecture (Beckn flow as sequenceDiagram)

> Source: [data-exchange/architecture.md](./data-exchange/architecture.md)

---

## Generic Beckn flow

Every action is a separate HTTP POST that returns an immediate `ACK`; the paired `on_*` callback arrives asynchronously at the caller's webhook. Which steps you actually run depends on the use case:

```
╔══════════════════════════════════════════════════════════════════╗
║ MERMAID sequenceDiagram — renders as SVG in actual GitBook       ║
║──────────────────────────────────────────────────────────────────║
║                                                                  ║
║  BAP App   ONIX BAP   beckn-router   ONIX BPP   BPP Server      ║
║    │          │            │             │           │           ║
║    │── Optional: publish-catalog · discover / on_discover        ║
║    │── Optional: select / init → on_select / on_init             ║
║    │          │            │             │           │           ║
║    │─confirm─>│            │             │           │           ║
║    │<──ACK────│            │             │           │           ║
║    │          │─confirm───>│─confirm────>│─confirm──>│           ║
║    │          │            │             │<──ACK─────│           ║
║    │          │            │             │           │           ║
║    │  ╔═══════════════════════════════════════════╗  │           ║
║    │  ║ ★ Minimal flow ends after on_confirm     ║  │           ║
║    │  ║                                           ║  │           ║
║    │  ║   │<──on_confirm──┼──on_confirm──────────│  │           ║
║    │  ║   │<──on_confirm──│             │        │  │           ║
║    │  ║<──on_confirm──────│             │        │  │           ║
║    │  ╚═══════════════════════════════════════════╝  │           ║
║    │          │            │             │           │           ║
║    │── Optional: status / on_status (async delivery)             ║
║    │── Optional: update / on_update (credential rotation)        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

The minimal-flow framing, the optional phases, and the `transactionId` / `messageId` correlation rules all live in Concepts § Beckn Protocol Lifecycle.

---

# 📝 What to look for when reviewing

1. **Cold-reader landing**: open `README.md` raw — would a skeptical DISCOM/AMISP architect understand what IES is and where to start within 30 seconds?
2. **Glossary discoverability**: every first-use of a term you don't already know should be a link to `glossary.md#term`. Spot-check 5 random terms across the affected pages.
3. **Beckn-as-control-plane**: read `data-exchange/README.md` from the top as if you've been burned by Beckn-for-telemetry claims before. The framing should now read as "Beckn coordinates; your existing standards transfer."
4. **Energy Credentials v1 scope**: the hint at the top of `energy-credentials/README.md` should preempt the "is this always true?" reaction.
5. **Mermaid rendering**: there are 4 Mermaid blocks in the actual docs (homepage layer, energy-credentials lifecycle, identifiers DID resolution, data-exchange/architecture Beckn flow). All MUST render as SVG in GitBook for the visual story to work. The only way to verify is GitBook preview — this file's ASCII approximations are not the final look.
6. **Anchor stability**: the `Verifiable Credential (VC)` heading has an explicit `<a id="verifiable-credential-vc">` because parens-in-headings handling varies between markdown renderers; the CIM Wikipedia URL parens are URL-encoded for the same reason.

---

# 🚫 What this preview deliberately doesn't show

- The actual Mermaid rendering (SVG) — only GitBook preview confirms it.
- Hover behavior on internal page links — GitBook may render a small preview card; this file shows plain markdown links.
- The full content of every chapter — pages 1, 2, 3, 4, 5 above are the highest-traffic ones rebuilt in this branch; pages 6 and 7 show the two figure-first changes. Other pages (registries/, schemas/, use-cases/, all checklists) are unchanged from `main`.
