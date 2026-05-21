# India Energy Stack (IES) Documentation Index

Welcome to the India Energy Stack (IES) documentation map. This index organizes all documentation files in the `ies-accelerator` repository sequentially and systematically by building blocks and phases.

---

## 📖 Foundational General References

These documents provide a general introduction, terminology definitions, and layout structures for the repository.

| Document | Purpose / Summary | Audience |
| :--- | :--- | :--- |
| **[Repository Readme](README.md)** | Root-level introduction to the IES accelerator repository structure and codebase. | All Developers |
| **[Getting Started](getting-started.md)** | A 5-minute orientation to the core capabilities, prerequisites, and choice of onboarding paths. | All Roles |
| **[Glossary](glossary.md)** | Canonical glossary of energy sector (DISCOM, HES, MDMS), identity (DID, DeDi, VC), and protocol (Beckn, ONIX) terms. | All Roles |
| **[GitBook Summary](SUMMARY.md)** | Table of Contents defining the layout and navigation sidebar structure in GitBook. | Doc Maintainers |

---

## 🆔 1. Identifiers and Addressing (DIDs)

This block defines the cryptographic identity of utilities, consumers, assets, and datasets on the network.

### ⚙️ Setup & Configuration
* **[Identifiers Readme](identifiers/README.md)**
  - *Summary*: High-level introduction to the IES addressing layer.
  - *Onboarding Tip*: Explains how IES wraps legacy internal identifiers (like consumer numbers) rather than replacing them.
* **[Core Concepts](identifiers/concepts.md)**
  - *Summary*: Explains the cryptographic models behind DIDs (why DIDs are used, and the differences between `did:web`, `did:key`, and `did:dedi`).
* **[ID Patterns Specification](identifiers/id-patterns.md)**
  - *Summary*: Outlines specific naming grammars and patterns used for DISCOMs, regulators, consumers, and smart meter assets.
* **[Registries Mapping](identifiers/registries.md)**
  - *Summary*: Describes how DIDs map directly to Decentralized Directory (DeDi) registry records for discovery.

### 🔌 Use & Operations
* **[Resolution and Routing Specification](identifiers/resolution.md)**
  - *Summary*: Defines the resolver API methods (`resolve_did`, `resolve_record`, `resolve_endpoint`), standard resolution workflows (credentials, routing Beckn messages, asset outage checks), and error handling rules.
* **[Issuance Reference Implementation](identifiers/issuance-reference.md)**
  - *Summary*: A code-focused guide (using OpenSSL and Python) for minting an issuer keypair, building a compliant `did:web` `did.json` document, and registering the DISCOM on the IES reference registry.
* **[Identifiers Basic Checklist](checklists/identifiers-basic-checklist.md)**
  - *Summary*: A self-check list to verify that the utility's domains, keys, and DIDs are structurally correct.

### 🛠️ Update & Maintenance
* **[Resolution: Caching Strategy](identifiers/resolution.md#caching-strategy)**
  - *Summary*: Specifies time-to-live (TTL) limits and rules for caching DIDs and records (including asymmetric negative caching for revocation lookups).
* **[Resolution: Error Handling](identifiers/resolution.md#error-handling)**
  - *Summary*: Actionable matrix on how to respond to resolver timeouts, DIDs mismatching, and decommissioned assets.

---

## 🗄️ 2. Registries and Directories (DeDi)

This block describes the directories that store and resolve identifiers to participant records.

### ⚙️ Setup & Configuration
* **[Registries Overview](registries/README.md)**
  - *Summary*: Introduction to the trust registry layer.
* **[DeDi Primer](registries/dedi-primer.md)**
  - *Summary*: Conceptual primer on Decentralized Directories, namespace control, and resolving records over HTTP.
* **[Registry Creation Guide](registries/registry-creation.md)**
  - *Summary*: Step-by-step developer walkthrough for configuring namespace controller keys and creating DeDi registries.
* **[Required Registries](registries/required-registries.md)**
  - *Summary*: Specification of properties, structures, and JSON schemas for reference registries (DISCOMs, Regulators).

### 🔌 Use & Operations
* **[Onboarding Checklist](registries/required-registries.md#end-to-end-onboarding-checklist)**
  - *Summary*: The master sequence for initializing registries, keys, and whitelists when onboarding.
* **[Registries Basic Checklist](checklists/registries-basic-checklist.md)**
  - *Summary*: Checklist to verify that registries are correctly provisioned, whitelisted, and accessible.

### 🛠️ Update & Maintenance
* **[Registry record Updates](registries/registry-creation.md#updating-registries)**
  - *Summary*: Explains how to invoke the DeDi API to mutate or append registry records when updating subscriber endpoints or keys.

---

## 🪪 3. Energy Credentials (VCs / OpenCred)

This block handles digital attestations of connections, billing summaries, and consumer identities.

### ⚙️ Setup & Configuration
* **[Credentials Overview](energy-credentials/README.md)**
  - *Summary*: Introduction to IES Verifiable Credentials.
* **[Core Concepts](energy-credentials/concepts.md)**
  - *Summary*: Core architectural roles (Issuer, Holder, Verifier) and the trust delegation chain (Regulator -> DISCOM -> Consumer).
* **[Credential Schemas](energy-credentials/schemas.md)**
  - *Summary*: Details how JSON-LD contexts and JSON schemas are wrapped and served for credentials.
* **[Deployment Guide](energy-credentials/onboarding.md)**
  - *Summary*: Step-by-step instructions for deploying the OpenCred service locally or on cloud environments using Docker.

### 🔌 Use & Operations
* **[Issuing Credentials](energy-credentials/issuance.md)**
  - *Summary*: Explains how to map customer data to OpenCred `/v1/credentials/issue` payloads and configure signing keys.
* **[Verifying Credentials](energy-credentials/verification.md)**
  - *Summary*: Explains how verifiers perform signature checks, validate schema compliance, and check revocation status.
* **[DigiLocker Integration](energy-credentials/digilocker-integration.md)**
  - *Summary*: Step-by-step implementation for integrating OpenCred with India's DigiLocker Pull URI protocol.
* **[Consumer Energy Passport Spec](energy-credentials/consumer-energy-passport.md)**
  - *Summary*: Details the structure, fields, and purposes of the Consumer Energy Passport credential.
* **[Consumer Meter Digest Spec](energy-credentials/consumer-meter-digest.md)**
  - *Summary*: Details the structure and parameters of the Consumer Meter Digest credential.
* **[Energy Credentials Checklists](checklists/)**
  - *Summary*: Tiered check lists for credential operations:
    - **[Basic Checklist](checklists/energy-credentials-basic-checklist.md)**: Identity and issuance test verification.
    - **[Simple Checklist](checklists/energy-credentials-checklist.md)**: Quick configuration and endpoints audit.
    - **[Detailed Checklist](checklists/energy-credentials-checklist-detailed.md)**: Deep dive into API, DB mapping, and security verification.

### 🛠️ Update & Maintenance
* **[Revocation Management](energy-credentials/verification.md#status-list)**
  - *Summary*: Documents how to revoke credentials by writing hashes to DeDi status lists, and how verifiers check status.

---

## 🔌 4. Data Exchange (Beckn)

This block governs data discovery, consent, and the transfer of telemetry and regulatory datasets.

### ⚙️ Setup & Configuration
* **[Data Exchange Overview](data-exchange/README.md)**
  - *Summary*: Conceptual introduction to federated energy data exchange.
* **[Core Concepts](data-exchange/concepts.md)**
  - *Summary*: Differentiates between the Control Plane (Beckn protocol) and Data Plane (MQTT, REST, SFTP channels).
* **[Architecture](data-exchange/architecture.md)**
  - *Summary*: Details the network topology of Beckn Gateway (BG), BAPs, and BPPs in the energy grid.
* **[Quick Start](data-exchange/quick-start.md)**
  - *Summary*: Developer guide to running local data exchange sandboxes using ONIX docker images.
* **[Registry Setup](data-exchange/registry-setup.md)**
  - *Summary*: Guide to registering BAP and BPP nodes inside Beckn subscriber registries.

### 🔌 Use & Operations
* **[Data Exchange Checklists](checklists/)**
  - *Summary*: Checklists to verify nodes and networks:
    - **[Basic Checklist](checklists/data-exchange-basic-checklist.md)**: Sandboxing and local callback validation.
    - **[Simple Checklist](checklists/data-exchange-checklist.md)**: Port and proxy audits.
    - **[Detailed Checklist](checklists/data-exchange-checklist-detailed.md)**: Production network readiness and security verification.

### 🛠️ Update & Maintenance
* **[Subscriber Key Rotations](data-exchange/registry-setup.md#key-rotation)**
  - *Summary*: Guide to updating signature and encryption keys inside Beckn subscriber records.

---

## 🗃️ 5. Schemas

Detailed documentation for the JSON and JSON-LD schema formats used in the accelerator.

| Schema Directory | Version | Description | Reference Link |
| :--- | :--- | :--- | :--- |
| **ElectricityCredential** | `v1.0` | Attestation format for utility consumers. | **[ElectricityCredential v1.0 README](schemas/ElectricityCredential/v1.0/README.md)** |
| **MeterData** | `v0.5` | Standard schema for telemetry, profiles, and billing summaries. | **[MeterData v0.5 README](schemas/MeterData/v0.5/README.md)** |
| **MeterData** | `v0.6` | Upgraded schema introducing Form A (Elaborated) / Form B (Compact) dual representation. | **[MeterData v0.6 README](schemas/MeterData/v0.6/README.md)** (with **[v0.6 Changelog](schemas/MeterData/v0.6/CHANGELOG.md)**) |
| **ArrFiling** | `v0.5` | Schema representing annual revenue requirement filings. | **[ArrFiling v0.5 README](schemas/ArrFiling/v0.5/README.md)** |
| **MeterDataRequest** | `v0.5` | Schema representing consumer queries and requests for datasets. | **[MeterDataRequest v0.5 README](schemas/MeterDataRequest/v0.5/README.md)** |

---

## 🎯 6. Use Cases

Practical deployment and mapping implementations for specific grid business processes.

* **[Use Cases Overview](use-cases/README.md)**
  - *Summary*: Catalog of standard use cases.
* **[Smart Meter Data Exchange](use-cases/smart-meter-data-exchange/README.md)**
  - *Summary*: Exchanging telemetry datasets. Includes:
    - **[IES Data Model Mapping](use-cases/smart-meter-data-exchange/ies-data-model.md)**: Mapping DLMS-COSEM/CIM fields to IES json.
    - **[Survey of Existing Terminology](use-cases/smart-meter-data-exchange/survey-of-existing-terminology.md)**: Cross-reference between standard naming groups.
    - **[Basic Checklist](use-cases/smart-meter-data-exchange/basic-checklist.md)**: Verification of BPP datasets.
* **[Consumer Meter Digest](use-cases/consumer-meter-digest/README.md)** (with **[Basic Checklist](use-cases/consumer-meter-digest/basic-checklist.md)**)
  - *Summary*: Pulling credentials for meter parameter digests.
* **[Consumer Energy Passport](use-cases/consumer-energy-passport/README.md)** (with **[Basic Checklist](use-cases/consumer-energy-passport/basic-checklist.md)**)
  - *Summary*: Aggregating verified energy records into a passport credential.
* **[DISCOM Regulatory Filing](use-cases/discom-regulatory-filing/README.md)** (with **[Basic Checklist](use-cases/discom-regulatory-filing/basic-checklist.md)**)
  - *Summary*: Submitting ARR filing datasets to regulators.
* **[Tariff Intelligence](use-cases/tariff-intelligence/README.md)** (with **[Basic Checklist](use-cases/tariff-intelligence/basic-checklist.md)**)
  - *Summary*: Sharing billing profiles and tariff rates across the network.

---

## 🗺️ 7. Operational Pathways (Roadmaps)

Step-by-step project-management pathways for onboarding and network operations.

* **[Pathways Index](pathways/README.md)**
  - *Summary*: Map of available roles and roadmaps.
* **[Utility Pathway](pathways/utility.md)**
  - *Summary*: The sequential blueprint for a new utility/DISCOM onboarding. Guides them through Identity Setup, Registry configuration, Credential Issuance, and Beckn Data Exchange.
* **[Secretariat Pathway](pathways/secretariat.md)**
  - *Summary*: The internal operational handbook for the IES Secretariat to setup registries, verify intakes, whitelist participants, handle key compromises, and maintain schemas.

---

## ⚠️ Summary of Duplicate or Overlapping Information

During our audit of the `ies-accelerator` documentation, we identified several instances where identical schemas, configurations, or operational guidelines are duplicated across different directories:

### 1. Public Registry Definitions
* **Overlapping Files & Sections**:
  - `[Registries — Public and Private](identifiers/registries.md#the-public-ies-registries)`
  - `[Required Registries for IES Onboarding](registries/required-registries.md#discom-reference-registry)`
* **Description**: Both sections define the properties of the authoritative `india-energy-stack` registries (DISCOMs Reference Registry, Regulators Reference Registry, and Schemas Registry), even copy-pasting the exact same JSON payload schemas and field tables.
* **Suggested Corrective Action**: Centralize the canonical record schemas and lookup field tables in `registries/required-registries.md`. Update `identifiers/registries.md` to focus strictly on the conceptual routing and resolution mapping, replacing duplicate JSON examples with direct links.

### 2. Beckn Node Registration and Onboarding
* **Overlapping Files & Sections**:
  - `[Required Registries: Beckn subscriber registry](registries/required-registries.md#beckn-subscriber-registry)`
  - `[Data Exchange: Registry Setup](data-exchange/registry-setup.md)`
* **Description**: Both guides describe how to generate signature/encryption keys for Beckn adapters, write the subscriber record under the `<your-namespace>/subscribers-test` registry path, and email the IES Secretariat for whitelisting.
* **Suggested Corrective Action**: Keep the high-level registry requirements in `registries/required-registries.md`, but move all technical steps (such as Ed25519 key generation commands, base64 formatting, and ONIX configuration options) into `data-exchange/registry-setup.md`.

### 3. Checklist Redundancies
* **Overlapping Files & Sections**:
  - Multiple checklists under the `checklists/` directory: `energy-credentials-basic-checklist.md`, `energy-credentials-checklist.md`, `energy-credentials-checklist-detailed.md`.
  - Use-case-specific checklists: `use-cases/smart-meter-data-exchange/basic-checklist.md`, `use-cases/consumer-meter-digest/basic-checklist.md`, `use-cases/consumer-energy-passport/basic-checklist.md`, `use-cases/discom-regulatory-filing/basic-checklist.md`, and `use-cases/tariff-intelligence/basic-checklist.md`.
* **Description**: The generic checklists duplicate domain allocation, Docker configurations, and registry checks. Additionally, every use-case-specific basic checklist duplicates identical organizational registration steps.
* **Suggested Corrective Action**: Consolidate generic onboarding audits into a single, multi-tier checklist under `checklists/` (e.g., Identity Setup, Credentials Setup, Exchange Setup). Replace individual use-case checklist files with short, use-case-specific checklists embedded directly in their respective `README.md` files.

---

## 💡 Suggestions on How the Documentation Can Be Improved

To enable a new utility to onboard and integrate with minimal external support, we suggest implementing the following documentation enhancements in the repository:

### 1. Add a Private DeDi Resolver Implementation Guide
* **Target Location**: `[Registry Creation Guide](registries/registry-creation.md)`
* **Improvement Proposal**: While private registries are conceptually introduced as "FastAPI or PostgreSQL thin wrappers", there are no concrete instructions. We should add a minimal, copy-pasteable FastAPI code snippet showing how to implement the lookup endpoint (`GET /lookup/{namespace}/{registry}/{record-id}`) and authenticate incoming internal queries using mTLS.

### 2. Add Code Examples for DigiLocker Webhook Signature Verification
* **Target Location**: `[DigiLocker Integration](energy-credentials/digilocker-integration.md)`
* **Improvement Proposal**: Utilities must secure their DigiLocker callback endpoints to prevent webhook spoofing. We should document the exact HMAC-SHA256 signature verification steps, providing a Python/NodeJS example showing how to compute and compare the signature header against the API Setu shared secret.

### 3. Consolidate Credential Revocation Hash Logic
* **Target Location**: `[Verifying Credentials](energy-credentials/verification.md#status-list)`
* **Improvement Proposal**: The method for generating credential hashes (published to DeDi revocation lists) is fragmented across multiple guides. We should add a unified section demonstrating how to generate the hash (e.g., canonicalizing JSON via JCS RFC 8785, omitting signature blocks, and hashing via SHA-256) with a runnable script to avoid syntax and sorting discrepancies during verification.

### 4. Provide a Single Master Onboarding Quickstart Flow
* **Target Location**: `[Getting Started](getting-started.md)`
* **Improvement Proposal**: Introduce a visual onboarding timeline diagram (using Mermaid) at the top of "Getting Started". This diagram will lay out the precise sequence of tasks (DNS setup -> Key generation -> Registry request -> Service deployment) so that a new utility has a clear, unified project-management blueprint from day one.
