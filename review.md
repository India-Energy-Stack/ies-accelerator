# India Energy Stack (IES) Documentation Review and Assessments

This document contains architectural assessments, identified documentation redundancies, and actionable suggestions to improve the readability and onboarding experience of the IES accelerator documentation.

---

## ⚠️ Summary of Duplicate or Overlapping Information

During our audit of the `ies-accelerator` documentation, we identified several instances where identical schemas, configurations, or operational guidelines are duplicated across different directories:

### 1. Public Registry Definitions
* **Overlapping Files & Sections**:
  - Link: [Registries — Public and Private](identifiers/registries.md#the-public-ies-registries) (Raw reference: `identifiers/registries.md#the-public-ies-registries`)
  - Link: [Required Registries for IES Onboarding](registries/required-registries.md#discom-reference-registry) (Raw reference: `registries/required-registries.md#discom-reference-registry`)
* **Description**: Both sections define the properties of the authoritative `india-energy-stack` registries (DISCOMs Reference Registry, Regulators Reference Registry, and Schemas Registry), even copy-pasting the exact same JSON payload schemas and field tables.
* **Suggested Corrective Action**: Centralize the canonical record schemas and lookup field tables in `registries/required-registries.md`. Update `identifiers/registries.md` to focus strictly on the conceptual routing and resolution mapping, replacing duplicate JSON examples with direct links.

### 2. Beckn Node Registration and Onboarding
* **Overlapping Files & Sections**:
  - Link: [Required Registries: Beckn subscriber registry](registries/required-registries.md#beckn-subscriber-registry) (Raw reference: `registries/required-registries.md#beckn-subscriber-registry`)
  - Link: [Data Exchange: Registry Setup](data-exchange/registry-setup.md) (Raw reference: `data-exchange/registry-setup.md`)
* **Description**: Both guides describe how to generate signature/encryption keys for Beckn adapters, write the subscriber record under the `<your-namespace>/subscribers-test` registry path, and email the IES Secretariat for whitelisting.
* **Suggested Corrective Action**: Keep the high-level registry requirements in `registries/required-registries.md`, but move all technical steps (such as Ed25519 key generation commands, base64 formatting, and ONIX configuration options) into `data-exchange/registry-setup.md`.

### 3. Checklist Redundancies
* **Overlapping Files & Sections**:
  - Link: [Checklists Directory](checklists/) (Raw reference: `checklists/`)
    - [Energy Credentials Basic Checklist](checklists/energy-credentials-basic-checklist.md) (Raw reference: `checklists/energy-credentials-basic-checklist.md`)
    - [Energy Credentials Simple Checklist](checklists/energy-credentials-checklist.md) (Raw reference: `checklists/energy-credentials-checklist.md`)
    - [Energy Credentials Detailed Checklist](checklists/energy-credentials-checklist-detailed.md) (Raw reference: `checklists/energy-credentials-checklist-detailed.md`)
  - Link: [Use Cases Directory](use-cases/) (Raw reference: `use-cases/`)
    - [Smart Meter Basic Checklist](use-cases/smart-meter-data-exchange/basic-checklist.md) (Raw reference: `use-cases/smart-meter-data-exchange/basic-checklist.md`)
    - [Consumer Meter Digest Basic Checklist](use-cases/consumer-meter-digest/basic-checklist.md) (Raw reference: `use-cases/consumer-meter-digest/basic-checklist.md`)
    - [Consumer Energy Passport Basic Checklist](use-cases/consumer-energy-passport/basic-checklist.md) (Raw reference: `use-cases/consumer-energy-passport/basic-checklist.md`)
    - [Regulatory Filing Basic Checklist](use-cases/discom-regulatory-filing/basic-checklist.md) (Raw reference: `use-cases/discom-regulatory-filing/basic-checklist.md`)
    - [Tariff Intelligence Basic Checklist](use-cases/tariff-intelligence/basic-checklist.md) (Raw reference: `use-cases/tariff-intelligence/basic-checklist.md`)
* **Description**: The generic checklists duplicate domain allocation, Docker configurations, and registry checks. Additionally, every use-case-specific basic checklist duplicates identical organizational registration steps.
* **Suggested Corrective Action**: Consolidate generic onboarding audits into a single, multi-tier checklist under `checklists/` (e.g., Identity Setup, Credentials Setup, Exchange Setup). Replace individual use-case checklist files with short, use-case-specific checklists embedded directly in their respective `README.md` files.

---

## 💡 Suggestions on How the Documentation Can Be Improved

To enable a new utility to onboard and integrate with minimal external support, we suggest implementing the following documentation enhancements in the repository:

### 1. Add a Private DeDi Resolver Implementation Guide
* **Target Location**: [Registry Creation Guide](registries/registry-creation.md) (Raw reference: `registries/registry-creation.md`)
* **Improvement Proposal**: While private registries are conceptually introduced as "FastAPI or PostgreSQL thin wrappers", there are no concrete instructions. We should add a minimal, copy-pasteable FastAPI code snippet showing how to implement the lookup endpoint (`GET /lookup/{namespace}/{registry}/{record-id}`) and authenticate incoming internal queries using mTLS.

### 2. Add Code Examples for DigiLocker Webhook Signature Verification
* **Target Location**: [DigiLocker Integration](energy-credentials/digilocker-integration.md) (Raw reference: `energy-credentials/digilocker-integration.md`)
* **Improvement Proposal**: Utilities must secure their DigiLocker callback endpoints to prevent webhook spoofing. We should document the exact HMAC-SHA256 signature verification steps, providing a Python/NodeJS example showing how to compute and compare the signature header against the API Setu shared secret.

### 3. Consolidate Credential Revocation Hash Logic
* **Target Location**: [Verifying Credentials](energy-credentials/verification.md#status-list) (Raw reference: `energy-credentials/verification.md#status-list`)
* **Improvement Proposal**: The method for generating credential hashes (published to DeDi revocation lists) is fragmented across multiple guides. We should add a unified section demonstrating how to generate the hash (e.g., canonicalizing JSON via JCS RFC 8785, omitting signature blocks, and hashing via SHA-256) with a runnable script to avoid syntax and sorting discrepancies during verification.

### 4. Provide a Single Master Onboarding Quickstart Flow
* **Target Location**: [Getting Started](getting-started.md) (Raw reference: `getting-started.md`)
* **Improvement Proposal**: Introduce a visual onboarding timeline diagram (using Mermaid) at the top of "Getting Started". This diagram will lay out the precise sequence of tasks (DNS setup -> Key generation -> Registry request -> Service deployment) so that a new utility has a clear, unified project-management blueprint from day one.

---

## 🧠 Architectural Assessment: Resolution, Registries, and Logical Reorganization

We have performed an assessment of the logical sequencing, placement, and content organization within the identity and registry layers to guide future refactoring of the documentation:

### 1. Logical Sequencing & Placement of Identifier Resolution
* **The Assessment**: Currently, identifier resolution is placed under `[Identifiers & Addressing (DIDs) - Use & Operations](identifiers/resolution.md)`. However, resolving identifiers on the IES network is almost entirely dependent on Decentralized Directory (DeDi) registry structures. 
  - To resolve a `did:dedi` identifier, a client must query the DeDi registry endpoints directly.
  - To resolve a `did:web` identifier, a client must retrieve a `did.json` document hosted at a web server location, which conceptually acts as a simple read-only endpoint registry.
* **Logical Reorganization Proposal**: We propose that the **Identifiers** section should focus purely on naming conventions, syntax, and cryptographic formats (like key generation and DIDs grammar), referencing the **Registries & Resolution** section for all lookup operations. Identifier resolution should be moved under the **Registries and Directories (DeDi)** building block, as "Resolution" is the primary operational consumer of registries.

### 2. Resolution Mechanics by DID Method
To prevent confusion for developers onboarding to the IES accelerator, the documentation should clearly delineate the distinct resolution mechanism required for each supported identifier method:
* **`did:key` / `did:jwk` (Offline Cryptographic)**:
  - *Mechanism*: Requires no network lookup or registry querying. The public key is mathematically encoded inside the identifier string itself. Resolution is performed entirely offline using local SDK functions.
* **`did:web` (HTTPS-based)**:
  - *Mechanism*: Resolves over the public web via an HTTPS request. The resolver translates the DID (e.g., `did:web:ies.tpddl.in`) into a standard path to fetch the public verification key (e.g., `https://ies.tpddl.in/.well-known/did.json`).
* **`did:dedi` (Directory API Query)**:
  - *Mechanism*: Resolves by querying the Decentralized Directory (DeDi) API. The resolver parses the coordinate string (`did:dedi:<namespace>:<registry>:<record-id>`) and issues a signed HTTP GET lookup request (e.g., `GET /lookup/<namespace>/<registry>/<record-id>`) against the registered DeDi resolver endpoints.

### 3. Unification of Public vs. Private Resolution Details
Resolution itself is the logical point where public and private views of network data converge. The documentation should bring these details together explicitly:
* **The Two-Resolver Model**: An identifier like `did:dedi:tpddl:consumers:CN-123` represents the same consumer entity in both public and private contexts. However, the resolver queries different endpoints depending on the routing context:
  - *Public Resolution*: Queries the public DeDi network, returning a redacted record containing only non-sensitive metadata (e.g., city, tariff category, status) to preserve DPDP compliance.
  - *Private Resolution*: Queries the utility's internal private DeDi resolver mirror, returning the full record with sensitive PII (name, address, billing details) for internal SCADA/billing consumption.
* **Unification via `privateRef`**: The public record contains a `privateRef` pointer (e.g., `https://internal-dedi.tpddl.in/dedi/lookup/...`) linking the two views. While public verifiers ignore this pointer, authorized internal clients follow it to retrieve the full, private state of the entity, unifying the public identity and private data planes.
