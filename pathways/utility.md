# Utility Pathway: Step-by-Step IES Integration Roadmap

Welcome to the **Utility Pathway**. This guide provides an actionable and structured roadmap for an electricity distribution utility to easily adopt the capabilities of the India Energy Stack (IES).

To keep this guide extremely clean and focus on utility progress, technical specifications are referenced via hyperlinks rather than repeated. Expand any step to find actionable guidelines, cross-team advice, and prework checkpoints.

---

## Roadmap Overview

```mermaid
flowchart TD
    prep["Phase 1: Preparation (Step 1.1 - 1.2)"] --> init["Phase 2: Getting Started (Step 2.1 - 2.3)"]
    init --> passport["Phase 3: Consumer Energy Passport (Step 3.1 - 3.2)"]
    passport --> dex["Phase 4: Smart Meter Data Exchange (Step 4.1 - 4.5)"]
    dex --> bill["Phase 5: Consumer Meter Digest (Step 5.1 - 5.2)"]
    bill --> der["Phase 6: DER Visibility (Step 6.1 - 6.5)"]
    der --> arr["Phase 7: ARR Publication (Step 7.1)"]
```

---

## Prework & Pre-Alignment Matrix

Before commencing the integration pathway, we recommend aligning the following internal teams and core systems. Setting up these channels early ensures a seamless deployment experience:

| Department / Role | System / Resource Involved | Purpose in Pathway |
|---|---|---|
| **DNS & Web Master** | Utility domain controller (`tpddl.co.in`) | Exposing public `did:web` and verifying DeDi namespaces |
| **IT & Security Admin** | Cloud KMS / HSM, Docker Environments | Securing signing keypairs and deploying OpenCred/ONIX services |
| **Legal / Signatory** | Corporate credentials, API Setu | Submitting whitelists to IES Secretariat and registering on DigiLocker |
| **Billing & CRM Teams** | CIS, MDMS, Customer Databases | Mapping telemetry, tariff profiles, and triggering billing credentials |

---

## Phase 1: Preparation (Identity & Addressing)

In this phase, you will establish your institutional cryptographic identity and define clear naming grammars for your grid resources and consumers.

<details>
<summary><b>Step 1.1: Establish Your Institutional Identity ([did:web](../registries/resolution.md#didweb))</b></summary>

### 💡 Phase Advice
> Set up a quick call with your DNS administrator as your very first step. Securing a dedicated subdomain takes only a few minutes but forms the foundation of your secure cryptographic brand.

### 📋 Prework Required
* Confirm that your web admin has write-access to your target domain (e.g., `ies.tpddl.co.in`) to host the verification path.

### Execution Guidance
A [`did:web`](../registries/resolution.md#didweb) identifier leverages your existing DNS and SSL infrastructure to publish your public keys.
1. **Assign a Dedicated Domain**: Allocate an institutional subdomain, e.g., `ies.tpddl.co.in`.
2. **Expose the DID Document (First Step)**: Host your verification keys in a standard `did.json` file served over HTTPS under the path:
   `https://ies.tpddl.co.in/.well-known/did.json`
   Construct the `did.json` document according to the W3C DID Core specification, ensuring your public verification key is correctly mapped and referenced. Refer to [Step 1 — Mint the issuer DID (did:web)](../identifiers/issuance-reference.md#step-1--mint-the-issuer-did-didweb) for the step-by-step structural checklist.

### References & Anchors
* [Identifiers & Addressing Overview](../identifiers/README.md)
* [Resolution & Routing Specification](../registries/resolution.md#didweb) (Detailed resolution rules for `did:web` endpoints)
* [Step 1 — Mint the issuer DID (did:web)](../identifiers/issuance-reference.md#step-1--mint-the-issuer-did-didweb) (Step-by-step document parameters)
* [Basic Identifiers Checklist](../checklists/identifiers-basic-checklist.md#1-institutional-identity)
</details>

<details>
<summary><b>Step 1.2: Define Your Naming Grammars ([DeDi Identifiers](../identifiers/id-patterns.md))</b></summary>

### 💡 Phase Advice
> Aligning your IES identifiers with your existing SAP, GIS, or CIS master codes avoids double-mapping. Wrap your existing internal serials rather than replacing them!

### Execution Guidance
Map your internal customer numbers, SAP codes, and meter serial numbers to standard, [DeDi-based naming grammars](../identifiers/id-patterns.md). Before constructing your identifiers, ensure you review the core rules in [Identifier Concepts: Identifiers as Names and Resolution Details](../identifiers/concepts.md#identifiers-as-names-and-resolution-details) (which clarify that identifiers are names carrying no inherent business meaning, and all must resolve to a DID Document).

We recommend adopting the suggested reference patterns shown below:
1. **Consumers**: `did:dedi:<utility>:consumers:<consumer number>`
   *(e.g., `did:dedi:tpddl:consumers:CN-89721345`)*
2. **Grid Assets**: `did:dedi:<utility>:assets:<asset-class>:<internal id>`
   *(e.g., `did:dedi:tpddl:assets:transformer:DT-11KV-F02-452`)*
3. **Smart Meters**: `did:dedi:<utility>:assets:meter:<manufacturer code>_<serial number>`
   *(e.g., `did:dedi:tpddl:assets:meter:GEN_12345678`)*
4. **Service Connections**: `did:dedi:<utility>:connections:<connection id>`
   *(e.g., `did:dedi:tpddl:connections:CON-90234`)*

> [!WARNING]
> `did:dedi` is currently **not** a W3C standard DID method. Resolving these identifiers requires utilizing `dedi.global` resolvers or a compliant Decentralised Directory API endpoint directly. Make sure to review the [did:dedi Non-Standard DID Method Note](../identifiers/concepts.md#diddedi-standards-note) before deploying them.

### References & Anchors
* [Identifier Concepts: Identifiers as Names and Resolution Details](../identifiers/concepts.md#identifiers-as-names-and-resolution-details)
* [did:dedi Non-Standard DID Method Note](../identifiers/concepts.md#diddedi-standards-note)
* [Identifier Patterns and Grammars](../identifiers/id-patterns.md)
  * [Consumer Reference ID](../identifiers/id-patterns.md#consumer-reference-id)
  * [Asset Reference ID](../identifiers/id-patterns.md#asset-reference-id)
  * [Meter and Connection Reference DIDs](../identifiers/id-patterns.md#meter-and-connection-reference-dids)
</details>

---

## Phase 2: Getting Started (Registry Setup)

Establish your administrative namespaces on the public [Decentralized Directory (DeDi)](../registries/dedi-primer.md) and register your active endpoints with the network.

<details>
<summary><b>Step 2.1: Setup DeDi Namespace</b></summary>

### 💡 Phase Advice
> Using an institutional role-mailbox (e.g., `registry-admin@tpddl.co.in`) instead of a personal account ensures that namespace controls remain securely managed by your IT department across staff rotations.

### ⚠️ Caution
> **Namespace Domain Verification**: Domain ownership verification leverages your existing DNS TXT record or setup rather than requiring you to request a brand new record class from your network administrators, easing compliance boundaries.

### Execution Guidance
1. Register a secure role-mailbox on the DeDi Portal.
2. Establish a namespace matching your utility short-code (`<utility>`).
3. Expose the verification token in your DNS TXT records. Refer to [Registry Creation § Step 3](../registries/registry-creation.md#step-3--verify-the-namespace-against-a-domain) for formatting.

### References & Anchors
* [DeDi Primer](../registries/dedi-primer.md)
* [Registry Creation Guide](../registries/registry-creation.md#step-3--verify-the-namespace-against-a-domain)
* [Basic Registries Checklist](../checklists/registries-basic-checklist.md)
</details>

<details>
<summary><b>Step 2.2: Create Operational Registries</b></summary>

### 💡 Phase Advice
> Maintain strict separation of duties! Use separate registries for your keys, revocation list, and Beckn profiles to keep access privileges isolated.

### Execution Guidance
Create and initialize the following registries under your namespace:
* [`public-keys`](../registries/required-registries.md#public-keys-registry) (tag `public_key`): Houses versioned P-256 signing keys.
* [`vc-revocation-registry`](../registries/required-registries.md#revocation-registry) (tag `revoke`): Tracks real-time verifiable credential revocation.
* [`subscribers-test` & `subscribers-prod`](../registries/required-registries.md#beckn-subscriber-registry) (tag `beckn_subscriber`): Manages Beckn node configs.
* **Configure Backup Resolution via DeDi (Fallback Step)**: Once your DeDi namespace and registries are established, configure your OpenCred deployment to publish your primary DID document to DeDi. Set `OPENCRED_DEDI_HOST_DID_DOC=true` on the container (or by programmatically calling `/v1/keys/publish`). This registers your DID document within the DeDi `public-keys` registry, providing a fallback discovery mechanism for network participants if the primary HTTPS endpoint becomes temporarily unreachable.

### References & Anchors
* [Required Registries Catalog](../registries/required-registries.md)
  * [Public-keys registry](../registries/required-registries.md#public-keys-registry)
  * [Revocation registry](../registries/required-registries.md#revocation-registry)
  * [Beckn subscriber registry](../registries/required-registries.md#beckn-subscriber-registry)
* [OpenCred Key & DID Publishing Configuration](../energy-credentials/onboarding.md#deploy-opencred)
</details>

<details>
<summary><b>Step 2.3: Register with India Energy Stack</b></summary>

### 💡 Phase Advice
> Pre-verify your onboarding package! Double-checking that your URLs, service areas, and JWK keys are formatted correctly before emailing ensures immediate approval.

### 📋 Prework Required
* Stand up your subscriber registries (from Step 2.2) and prepare your endpoint URL payloads.

### Execution Guidance
Email your registration package (utility short-code, legal name, service area list, endpoints, and `did:web` JWK) to the IES Secretariat:
* **Primary Email**: [IES.Secretariat@fsrglobal.org](mailto:IES.Secretariat@fsrglobal.org)
* **Alternate Email**: [ies@recindia.com](mailto:ies@recindia.com)

The Secretariat will verify your credentials and register your endpoints inside the authoritative `ies-discoms-reference-registry` path.

### References & Anchors
* [Required Registries § How to get added](../registries/required-registries.md#how-to-get-added)
* [End-to-End Onboarding Checklist](../registries/required-registries.md#end-to-end-onboarding-checklist)
</details>

---

## Phase 3: Consumer Energy Passport (Verifiable Credentials)

Provide citizens with a secure, tamper-evident digital passport of their utility connection parameters, load limits, and registered assets.

<details>
<summary><b>Step 3.1: Setup Credential Issuance ([Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md))</b></summary>

### 💡 Phase Advice
> Leverage your existing Customer Relationship Management (CRM) tables. Since the Passport is a composite of standard customer master data, you only need to expose your existing billing/CIS databases to OpenCred.

### Execution Guidance
1. **Connect CRM Systems**: Map customer master data (sanctioned load, tariff slabs, connection status) from your CRM (e.g., SAP IS-U) to OpenCred.
2. **Configure Authentication**: Setup OTP or Aadhaar reference authentication gateways on your client portal.
3. **Deploy OpenCred**: Deploy the containerized OpenCred service using your secured P-256 signing keys.
4. **CRM Status Logging & Issuance**: Store active credential UUIDs in your database to coordinate revocations. Format and trigger credential issuance via OpenCred's `/v1/credentials/issue` API using the `ElectricityCredential` JSON shape.
5. **Verify Revocation Handling**: Ensure the verifier's revocation check logic is active. Be mindful of the silent-skip behavior if DeDi namespaces are misconfigured (refer to the [OpenCred Silent-Skip Warning](../energy-credentials/verification.md#silent-skip-warning)).
6. **Validate the Issued Credential**: Call the OpenCred verification endpoint (`/v1/credentials/verify`) using the issued VC to test the full verification cycle. This confirms that the verifier can successfully resolve the issuer's DID and validate the cryptographic signature. Note that if DeDi is disabled or the namespaces are not fully synchronized, the validation engine might exhibit specific resolve behaviors (refer to the [OpenCred Resolve Verification Check](../energy-credentials/onboarding.md#verifying-the-deployment)).

### References & Anchors
* [Energy Credentials Overview](../energy-credentials/README.md)
* [Energy Credentials Deployment Guide](../energy-credentials/onboarding.md)
* [OpenCred Resolve Verification Check & Env Options](../energy-credentials/onboarding.md#verifying-the-deployment)
* [OpenCred Silent-Skip Revocation Warning](../energy-credentials/verification.md#silent-skip-warning)
* [Batch Issuance at Scale (Queue & Workers)](../energy-credentials/issuance.md#batch-issuance-at-scale)
* [Multi-Replica Deployment Guidance](../energy-credentials/onboarding.md#multi-replica-and-batch-worker-fleet)
* [Consumer Energy Passport Use Case](../use-cases/consumer-energy-passport/README.md)
* [Consumer Energy Passport Checklist](../use-cases/consumer-energy-passport/checklist.md)
* [Consumer Energy Passport Schema (ElectricityCredential) Reference](../schemas/ElectricityCredential/README.md)
</details>

<details>
<summary><b>Step 3.2: Register with [DigiLocker](../energy-credentials/digilocker-integration.md)</b></summary>

### 💡 Phase Advice
> [API Setu](../energy-credentials/digilocker-integration.md) compliance checks can take time. Start your legal and institutional registrations on API Setu early in Phase 3 so that production gateways are cleared by the time your code is ready.

### 📋 Prework Required
* Secure authorization letters and corporate certificates from your legal department for [API Setu](../energy-credentials/digilocker-integration.md) access.

### References & Anchors
* [DigiLocker Integration Guide](../energy-credentials/digilocker-integration.md)
* [Issuing Credentials Checklist](../energy-credentials/issuance.md)
</details>

---

## Phase 4: Smart Meter Data Exchange ([Beckn Data Pipes](../data-exchange/concepts.md))

Enable federated, policy-governed data sharing of smart meter telemetry and master data with authorized third parties.

<details>
<summary><b>Step 4.1: Setup BPP Nodes ([BECKN Network](../data-exchange/quick-start.md))</b></summary>

### 💡 Phase Advice
> Deploying the ONIX adapter as a Docker service takes less than 10 minutes. Run the test sandbox local container first to easily verify your configurations before going to production.

### Execution Guidance
1. Deploy the standard Docker-based Beckn ONIX container.
2. Generate your Ed25519 node keypair.
3. Register your BPP credentials in DeDi [`subscribers-test`](../registries/required-registries.md#beckn-subscriber-registry).

### References & Anchors
* [Data Exchange Concepts](../data-exchange/concepts.md)
* [Data Exchange Quick Start](../data-exchange/quick-start.md)
* [ONIX Registry Setup](../data-exchange/registry-setup.md)
* [Data Exchange Onboarding Checklist](../checklists/data-exchange-checklist.md)
</details>

<details>
<summary><b>Step 4.2: Establish MDM Integration for Telemetry</b></summary>

### 💡 Phase Advice
> Protect your MDM database performance! Configure your MDMS adapter to write query results to a fast read-only caching replica or cache intermediate intervals to avoid overloading production transactional databases.

### ⚠️ Caution
> **Batch Telemetry Latency**: MDM database queries can be slow and can violate Beckn's transaction timeouts (usually 5 seconds). Ensure your telemetry API is highly optimized.

### Execution Guidance
Map HES DLMS-COSEM or IEC 61968-9 interval profiles to standard **[IntervalProfile](../schemas/MeterData/v0.6/README.md)**, **[DailyProfile](../schemas/MeterData/v0.6/README.md)**, **[InstantaneousProfile](../schemas/MeterData/v0.6/README.md)**, and **[EventProfile](../schemas/MeterData/v0.6/README.md)** formats.

### References & Anchors
* [Smart Meter Data Exchange Use Case](../use-cases/smart-meter-data-exchange/README.md)
  * [How It Works](../use-cases/smart-meter-data-exchange/README.md#how-it-works)
* [IES Meter Data Model](../use-cases/smart-meter-data-exchange/ies-meter-data-model.md)
* [MeterData Schema Specification](../schemas/MeterData/README.md)
</details>

<details>
<summary><b>Step 4.3: Integrate Customer Master Data</b></summary>

### 💡 Phase Advice
> Billing and customer profile files map directly to the **[CustomerProfile](../schemas/MeterData/v0.6/attributes.yaml)** schema. Ensure your CRM export script correctly aligns the tariff category, connection status, and sanctioned load.

### References & Anchors
* [MeterData Attributes & Customer Schema](../schemas/MeterData/v0.6/attributes.yaml)
</details>

<details>
<summary><b>Step 4.4: Establish Data Exchange Authorisation</b></summary>

### 💡 Phase Advice
> Leverage the **[MeterDataRequestCredential](../schemas/MeterDataRequestCredential/v0.1/README.md)** schema to formalise incoming B2B third-party data authorisations. The scope of the actual request for sharing can be a subset of the broader data authorised.

### Execution Guidance
While the technical authorisation logic is ultimately left to the utility, we suggest executing scoped access control by requiring the BAP to present a **[MeterDataRequestCredential](../schemas/MeterDataRequestCredential/v0.1/README.md)** (see [credential example](../schemas/MeterDataRequestCredential/v0.1/examples/example.json)) OR a **[Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md) with consent**. Your BPP ONIX adapter should verify these presented credentials at runtime before dispensing any interval profiles.

### ⚠️ Caution
> **Scoped Access Violations**: Never expose granular consumer interval data without verifying that the presented credential permits that specific access window and profile.

> [!WARNING]
> **Clarity Gap**: Standardized B2B automated token validation policies on BPP ONIX are currently under-specified in the core guidelines, requiring custom token validation structures for consumer-consented exchanges.

### References & Anchors
* [Data Exchange Security & Auth](../data-exchange/concepts.md#context-invariants)
* [MeterDataRequestCredential Schema](../schemas/MeterDataRequestCredential/v0.1/README.md)
* [MeterDataRequestCredential Example](../schemas/MeterDataRequestCredential/v0.1/examples/example.json)
</details>

<details>
<summary><b>Step 4.5: Enable Meter Data Exchange Go-Live</b></summary>

### 💡 Phase Advice
> Run a parallel pilot! Trade smart meter telemetry with a friendly test consumer or partner BAP to confirm that signing, encryption, and logging flows operate perfectly before live production exchange.

### References & Anchors
* [Data Exchange Onboarding Checklist](../checklists/data-exchange-checklist.md)
</details>

---

## Phase 5: [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) (Electricity Bill)

Move beyond static PDFs to compile and issue verifiable, machine-readable monthly electricity bills.

<details>
<summary><b>Step 5.1: Create the Consumer Meter Digest Verifiable Credential</b></summary>

### 💡 Phase Advice
> We suggest utilizing a credential that directly includes the **[MeterData](../schemas/MeterData/v0.6/README.md)** schema. When compiling the Digest for a billing cycle, the `CustomerProfile` and `BillingProfile` **must** be included. Additionally, an `IntervalProfile` containing intervals that span the entire billing period is strongly recommended to provide complete consumption transparency.

### Execution Guidance
1. **Request the Data**: Programmatically query your Data Exchange nodes with a `MeterDataRequest` spanning the billing duration and specifically targeting the required profiles.
   
   *Example `MeterDataRequest` for compiling a Digest:*
   ```json
   {
       "@context": "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/context.jsonld",
       "@type": "MeterDataRequest",
       "resources": [
           "did:dedi:ies:meter:IN-MH-MTR-89721"
       ],
       "scope": "ResourceOnly",
       "from": "2026-04-01T00:00:00Z",
       "duration": "P1M",
       "capabilitiesRequested": {
           "profiles": [
               { "profileType": "CustomerProfile" },
               { "profileType": "IntervalProfile" }
           ]
       }
   }
   ```

2. **Structure the Credential**: Package the resulting [`MeterData`](../schemas/MeterData/v0.6/README.md) payload inside the data subject of your verifiable credential envelope.
3. **Sign and Issue**: Sign and issue the verifiable credential utilizing your OpenCred service.


### References & Anchors
* [Electricity Bills and Digest Use Case](../use-cases/consumer-meter-digest/README.md)
  * [How It Works](../use-cases/consumer-meter-digest/README.md#how-it-works)
* [Consumer Meter Digest Checklist](../use-cases/consumer-meter-digest/checklist.md)
</details>

<details>
<summary><b>Step 5.2: Link Bills to [DigiLocker](../energy-credentials/digilocker-integration.md)</b></summary>

### 💡 Phase Advice
> Re-use your DigiLocker gateway! Since you cleared API Setu audits in Step 3.2, adding the verifiable bill credential is a simple path extension on your existing issuer record.

### References & Anchors
* [DigiLocker Issuer Setup](../energy-credentials/digilocker-integration.md)
</details>

---

## Phase 6: DER Visibility (Distributed Energy Resources)

Acquire real-time visibility into solar generation, battery storage, and feeder loading to balance the grid.

<details>
<summary><b>Step 6.1: Establish DER Sources</b></summary>

### 💡 Phase Advice
> Onboard consumer generation assets dynamically. Capture DER parameters (solar inverter rating, battery capacities) and map them to standard DIDs (e.g. `did:dedi:<utility>:assets:inverter:<inverter-serial-no>`).
</details>

<details>
<summary><b>Step 6.2: Start Receiving Data via Daily Profiles</b></summary>

### 💡 Phase Advice
> Prioritize your own grid telemetry first! Start by ingesting and mapping the utility's own smart meter consumption and generation profiles. Once established, expand your integration as a next step to connect with independent generators and public EV charging stations.

### 📋 Prework Required
* Confirm that smart meter generation register reads are active and mapped to standard profiles.
</details>

<details>
<summary><b>Step 6.3: Grid Topology & Data Exchange</b></summary>

### 💡 Phase Advice
> Publish hierarchical relationships. By linking substations, feeders, distribution transformers, smart meters, and DER assets, grid operators can programmatically map downstream loading. Leveraging **Data Exchange** networks enables you to share these grid datasets securely.

### References & Anchors
* [Grid Identifiers & Hierarchy Guide](../identifiers/id-patterns.md#asset-reference-id)
</details>

<details>
<summary><b>Step 6.4: Build a Feeder-Level Aggregator</b></summary>

### 💡 Phase Advice
> Keep fine-grained customer PII out of grid planning! By aggregating meter telemetry at the distribution transformer or feeder level, you can share real-time loading profiles without exposing individual customer details. These aggregated feeds are published securely via your **Data Exchange** nodes.

> **Leveraging Associations for Aggregation**: Use the optional `parentResources` property within the `CustomerProfile`'s `Association` block to trace every smart meter to its upstream parents (like feeder and Distribution Transformer). This deterministic linkage allows you to programmatically sum individual telemetry feeds into a single `AggregatedFeeder` payload!

### ⚠️ Caution
> **Imputation for Zero Readings**: Ensure your aggregator engine handles missing or zero readings securely (e.g., forward-fill or mean-imputation) to prevent aggregated peaks from showing artificial drops.

> Since the **MeterData** schema is used for telemetry exchange, we strongly suggest utilizing the `AccumulationBehaviour` property for annotating aggregation datasets. Ensure that aggregated datasets explicitly annotate `SUMMATION` as the `accumulationBehaviour`. Refer to this [Aggregated Feeder Example](../schemas/MeterData/v0.6/examples/AggregatedFeeder.json) showing a feeder-related aggregated `IntervalProfile` for a day.
</details>

<details>
<summary><b>Step 6.5: Build a DER Visualiser Dashboard</b></summary>

### 💡 Phase Advice
> Keep it visual! Query feeder aggregations over your Beckn BAP node and plot live timeseries graphs showing feeder loading, battery state-of-charge, and reverse solar back-feeding.
</details>

---

## Phase 7: ARR Publication (Annual Revenue Requirement)

Publish your Annual Revenue Requirement data in a standardized, machine-readable format to enable programmatic tariff analysis and regulatory transparency.

<details>
<summary><b>Step 7.1: Map Existing Data to [ARR Schema](../schemas/ArrFiling/v0.5/README.md)</b></summary>

### 💡 Phase Advice
> Rather than building new reporting pipelines from scratch, we suggest using your existing regulatory data sets and mapping them directly to the provided [ARR schema](../schemas/ArrFiling/v0.5/README.md).

### Execution Guidance
1. Extract historical, current, and forecasted monetary data from your existing tariff orders and regulatory filings.
2. Focus strictly on providing **only machine-readable data related to monetary data**. Avoid embedding unstructured text or PDF blobs.
3. Map this extracted monetary data directly to the canonical [`ArrFiling`](../schemas/ArrFiling/v0.5/README.md) schema structure.
4. **Note your experiences**: Treat this as an iterative mapping exercise. Document your experiences, friction points, or any missing schema fields encountered during the data mapping process to help inform future specification refinements.

### References & Anchors
* [ARR Filing Schema Reference](../schemas/ArrFiling/v0.5/README.md)
* [ARR Filing Machine-Readable Example](../schemas/ArrFiling/v0.5/examples/arr_filings.json)
</details>


