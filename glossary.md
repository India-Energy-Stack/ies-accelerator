# Glossary

Plain-language definitions for every acronym and term used across this book. Each term is anchor-linked from its first use in a chapter — click any link to jump directly to the definition below.

{% hint style="info" %}
This page is always visible in the left nav. If you hit a term you don't recognise, come back here.
{% endhint %}

---

## Identity and credentials

### DID

**Decentralized Identifier** — a globally unique, cryptographically verifiable identifier of the form `did:method:identifier` (e.g. `did:web:ies.discom.example`). Defined by the [W3C DID Core](https://www.w3.org/TR/did-core/) standard. Resolves to a **DID Document** containing public keys and service endpoints. IES uses DIDs to name every participant, asset, and credential issuer. See [Identifiers chapter](what-ies-provides/identifiers/README.md).

### DID methods used in IES

IES uses three standard W3C DID methods. There is no separate `did:dedi` method — DeDi-anchored identifiers are `did:web` DIDs whose document is hosted by a [DeDi runtime](#dedi) instead of (or alongside) the issuer's own domain.

- **`did:web`** — the DID resolves to a DID document fetched over HTTPS. Two forms in IES:
  - **Self-hosted by the institution.** `did:web:ies.discom.example` → `https://ies.discom.example/.well-known/did.json`. Used for DISCOMs, regulators, and other entities with a public web presence.
  - **Hosted by a DeDi runtime.** `did:web:<dedi-host>:<namespace>:<class>:<id>` → `https://<dedi-host>/<namespace>/<class>/<id>/did.json`. Used to give consumers, meters, assets, connections, and credential subjects a network-resolvable DID without requiring each one to operate a web server. The method is still `did:web`; DeDi just hosts the document. Example: `did:web:dedi.global:discom:consumers:DISCOM-2025-001234567`.
- **`did:key`** — the public key is encoded directly into the DID string. No domain or certificate required. Verifies fully offline; cannot rotate keys. Used for consumer wallets and first-deploy software keys.
- **`did:jwk`** — same idea as `did:key`, using JSON Web Key encoding. Wallet-friendly.

### DeDi

**Decentralised Directory** — distinguish the protocol from any runtime that implements it:

- **DeDi the protocol** — an open specification developed under the [Linux Foundation Decentralized Trust labs](https://github.com/LF-Decentralized-Trust-labs/decentralized-directory-protocol). Defines record shapes, namespace ownership, lookup/query semantics, revocation, and trust-anchor records. **IES picks DeDi-the-protocol** as the registry primitive.
- **DeDi runtimes** — any service that implements the DeDi protocol. [`dedi.global`](https://dedi.global) is one such hosted runtime; a DISCOM (or a network operator) can self-host a DeDi-compatible runtime — for a private internal mirror, for a regulated jurisdiction, or for redundancy. IES does not mandate a specific runtime; the same record shapes work across any conformant implementation.

A DeDi record has a `subscriber_id` and `record_id` and is looked up via a public HTTPS URL (e.g. `https://<runtime-host>/dedi/lookup/...`). IES uses DeDi for namespaces, network membership, public keys, revocation, and Beckn subscriber records. See [Registries chapter](what-ies-provides/registries/README.md).

<a id="verifiable-credential-vc"></a>

### Verifiable Credential (VC)

A tamper-evident JSON-LD document containing claims about a subject (the **holder**), signed by an **issuer**, that any party (the **verifier**) can validate offline using the issuer's published public key. Follows the [W3C VC Data Model](https://www.w3.org/TR/vc-data-model-2.0/). IES uses VCs for electricity credentials, consumer energy passports, and meter digests.

### Issuer / Holder / Verifier

The three roles in any credential exchange. **Issuer** signs and emits the credential. **Holder** keeps it (in DigiLocker, a wallet, or a DID-controlled store) and presents it on demand. **Verifier** receives a presentation and checks the signature against the issuer's published public key. In IES v1 the DISCOM is the issuer of electricity credentials; the consumer (or an authorized actor on their behalf) is the holder.

### OpenCred

The open-source credential service IES DISCOMs deploy to sign, verify, and revoke credentials. Holds your private signing key locally (or in a KMS) and exposes an HTTP API. **W3C-compliant** issuer: produces credentials that any standards-conformant verifier can validate. **DeDi-integrated** out of the box: credential revocation entries flow into a DeDi revocation registry automatically, and the container can optionally back up your `did.json` to DeDi so your DID stays resolvable even when your own domain is unreachable. Swap it for any other W3C-compliant signing pipeline if you prefer — the published `did.json` and credential format are unchanged.

- Image: `ghcr.io/nfh-trust-labs/opencred/opencred-server` ([releases](https://github.com/nfh-trust-labs/opencred/releases) · [docs](https://opencred.gitbook.io/docs))
- Bootcamp / first deploy: [opencred.gitbook.io/docs/bootcamp/local-docker](https://opencred.gitbook.io/docs/bootcamp/local-docker)
- See the [Energy Credentials chapter](what-ies-provides/energy-credentials/README.md) for the IES-specific issuance walkthrough.

### DigiLocker

[India's national digital document wallet](https://digilocker.gov.in). Consumer-facing store for government-issued documents. IES DISCOMs can deliver issued credentials to a consumer's DigiLocker via a Pull URI.

### API Setu

The [Government of India API exchange](https://apisetu.gov.in) where DISCOMs register as DigiLocker issuers.

---

## Data exchange and Beckn

### Beckn

The open, asynchronous, peer-to-peer protocol IES Data Exchange uses for the **control plane** — discovery, offer, consent, contract, and audit. Beckn can also carry the **payload inline** in the same flow when the dataset is small and a single signed message is the simplest workflow. For bulky datasets, telemetry streams, or anything already moved over an established channel (signed URL, REST, SFTP, MQTT, Kafka, OpenADR, etc.), Beckn instead delivers the **access method** via the `accessMethod` field on the DatasetItem. See [Data Exchange chapter](what-ies-provides/data-exchange/README.md).

### BAP

**Beckn Application Platform** — the consumer / buyer / data-requesting side in a Beckn exchange. In IES, a DISCOM consuming telemetry from an AMISP is the BAP.

### BPP

**Beckn Provider Platform** — the provider / seller / data-publishing side in a Beckn exchange. In IES, an AMISP publishing meter telemetry, or a SERC publishing a tariff order, is the BPP.

### ONIX

The reference Beckn adapter used in IES. Handles message signing, signature verification, DeDi lookup, network-membership checks, schema validation, and async callback routing. Ships as a container; your application code does not handle signing or key management directly.

### NFO

**Network Facilitator Organisation** — the organisation that operates a Beckn network: claims a verified DeDi namespace under its own domain, publishes one or more **network registries** under that namespace (one per environment / sector), curates membership by writing **subscriber reference records** that point at participant-owned subscriber records, and publishes the network's policy manifest. The network's identifier (`network_id`) is `<nfo-domain>/<registry-name>`. For IES, the network operator (REC / IES Secretariat) acts as the NFO under the `indiaenergystack.in` namespace. See [NFH docs — Setting up the network environment](https://docs.nfh.global/beckn/creating-an-open-network/setting-up-the-network-environment).

### DEG

**Digital Energy Grid** — the broader architecture from which IES Data Exchange inherits primitives (Energy Resource, Energy Catalogue, Energy Contract, Energy Credentials). See [Beckn DEG repo](https://github.com/Beckn-One/DEG).

### DDM

**Decentralized Data Marketplace** — the Beckn-protocol-based open network for buyers and providers to discover, offer, contract, and exchange datasets without a central middleman. The schema family describing the exchanged datasets is published at [beckn/DDM](https://github.com/beckn/DDM); IES extends it with its own schema families (MeterData, ArrFiling, OutageNotification, …).

### ERA

**Energy Resource Address** — a unique digital address for any energy asset (meter, generator, storage, EV). DEG primitive; surfaces in IES data exchanges via the `participants[]` and `provider` fields.

---

## India energy sector

### DISCOM

**Distribution Company** — the regulated entity that distributes electricity to consumers in a state or licence area. In IES v1, DISCOMs are the sole issuer of electricity credentials about consumers, meters, and assets.

### AMISP

**Advanced Metering Infrastructure Service Provider** — the entity (often a contracted vendor under [RDSS](#rdss)) that deploys, owns, and operates smart meters and the associated Head-End System on behalf of a DISCOM. AMISPs typically deliver meter data to the DISCOM's MDMS under an SLA.

### SERC

**State Electricity Regulatory Commission** — the state-level regulator that approves tariffs, reviews DISCOM filings, and issues regulatory orders. SERCs are the typical consumer of [`ArrFiling`](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5) filings and publisher of `IES_Policy`/`IES_Program` (tariff) datasets.

### ARR

**Aggregate Revenue Requirement** — the annual filing in which a DISCOM tells its SERC what total revenue it needs to recover for the coming year, broken down by cost head. The basis on which tariff is set.

### APR

**Annual Performance Review** — the mid-year reconciliation filing in which a DISCOM reports actual costs and revenues against the ARR projections.

### MYT

**Multi-Year Tariff** — the regulatory framework where tariffs are set for a multi-year control period (typically 3–5 years) with annual true-ups.

### True-up

The end-of-period adjustment by which actual costs are reconciled against the approved ARR, with the difference recovered or refunded through future tariffs.

### ACS-ARR gap

**Average Cost of Supply minus Average Revenue from sale** — the per-unit revenue shortfall a DISCOM carries. A standard KPI in regulatory and policy conversations.

### ATC loss

**AT&C loss** — Aggregate Technical & Commercial loss — the percentage of units injected into the network that are not realised as billed revenue, combining technical losses (line losses) and commercial losses (theft, under-billing, uncollected dues).

### HT-LT

**High Tension** / **Low Tension** — voltage-class classification of consumers. HT typically ≥11 kV (industrial, commercial); LT typically ≤ 440 V (residential, small commercial).

### DT

**Distribution Transformer** — the transformer that steps voltage down to LT for delivery to residential and small consumers. The unit of granularity for many distribution-network operations and analytics.

### Feeder

A medium-voltage line emerging from a substation that supplies a group of DTs and HT consumers.

### ToD

**Time of Day** tariff — a tariff structure in which the per-unit rate varies by time block (peak, off-peak, etc.).

### Regulatory asset

A deferred cost that the regulator allows the DISCOM to recover through future tariffs rather than the current year — typically used when actual costs significantly exceed approved ARR.

### NP

**Network Participant** — any entity (DISCOM, regulator, AMISP, aggregator) joined to an IES network with a published Beckn subscriber record and a verified DeDi namespace.

### RDSS

**Revamped Distribution Sector Scheme** — the Government of India scheme (announced 2021) under which DISCOMs receive central funding for smart metering, feeder segregation, and loss-reduction, in exchange for performance-linked obligations. RDSS is the policy context behind most of India's AMI deployment.

### CIS

**Consumer Information System** — the DISCOM's billing and consumer-master database. The system of record for customer numbers, addresses, tariff categories, and billing history.

### NMS

**Network Management System** — the DISCOM's operational system for monitoring the distribution network (substations, feeders, DTs).

### HES

**Head-End System** — the AMI software layer that talks to smart meters over the field network, collects readings, and forwards them to the MDM. Owned by the AMISP in an RDSS deployment.

### MDMS

**Meter Data Management System** (also **MDM**) — the utility-side platform that validates, stores, and analyses meter data received from the HES. The DISCOM's system of record for meter readings.

### DER

**Distributed Energy Resource** — any generation, storage, or controllable load on the consumer side of the meter (rooftop solar, battery, EV charger, behind-the-meter genset). Increasingly the subject of credentials and data exchanges in IES.

---

## Standards and protocols

### CIM

**Common Information Model** — the [IEC 61970 / 61968](https://en.wikipedia.org/wiki/Common_Information_Model_%28electricity%29) data model for power system information exchange. The lingua franca for HES↔MDM and enterprise integrations.

### IEC 61968

The series of standards for **information exchange between distribution management systems**. Part 9 (`IEC 61968-9`) specifically covers meter reading and control interfaces. The CEA's RDSS AMI interoperability guidance names IEC 61968 / IEC 61968-100 alongside MultiSpeak and Web Services for HES↔MDMS integration.

### DLMS-COSEM

The wire protocol between a **smart meter** and the AMI head-end (also referred to as **IS 15959**, the Bureau of Indian Standards profile aligned with the international `IEC 62056` family). The default for Indian RDSS smart-meter deployments.

### MultiSpeak

A utility software interoperability standard widely used in North America, named alongside CIM and IEC 61968 in India's AMI interoperability guidance. Version 3.0 is the common reference in Indian RDSS specifications.

### OpenADR

**Open Automated Demand Response** — the [protocol](https://www.openadr.org) for sending demand-response and flexibility signals to and from distributed resources. Version 3.1.0 is current. Used in IES for DR/DER events and flexibility reporting — **not** for generic interval meter reads.

### XBRL

**eXtensible Business Reporting Language** — the international standard for tagged, comparable structured financial and regulatory filings. The target structured format for [`ArrFiling`](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5). iXBRL embeds XBRL tags in human-readable XHTML.

### Akoma Ntoso

The [OASIS LegalDocML XML standard](https://www.oasis-open.org/standard/akn-v1-0/) for structured legal documents. Recommended for the order text of tariff and regulatory documents in IES (`IES_Policy`).

### DCAT 3

**Data Catalog Vocabulary** version 3 — the [W3C standard](https://www.w3.org/TR/vocab-dcat-3/) for describing datasets and data services. Recommended metadata format for tariff schedule discovery in IES.

### MQTT

A lightweight publish/subscribe messaging protocol commonly used for IoT and event-driven data flows. MQTT 5.0 is the current version. In IES, MQTT is an optional adapter for event or near-real-time meter telemetry — not the default for batch reads.

### W3C VC

Shorthand for [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model-2.0/). See [Verifiable Credential](#verifiable-credential-vc).
