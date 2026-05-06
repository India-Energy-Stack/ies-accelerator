# Unify but not uniform IES architecture with evolvability
**Proposal for review : April 2026**

**Use case:** Customer VC issuance - but scalable to all aspects  
**Approach:** Leveraging OpenADR 3.x with a Self-Describing Semantic Layer for Decentralized Energy Evolution

---

## 1. Executive Summary

This proposal outlines a scalable architecture for hosting an energy Resource Registry on the DeDi.global protocol. By leveraging the industry-standard structural definitions of OpenADR 3.x and augmenting them with a layered JSON-LD semantic layer, we enable a decentralized ecosystem where the India Energy Stack (IES), individual Utilities, and third parties can evolve definitions independently without breaking core interoperability.

**Goal:** UNIFY but NOT UNIFORM  
**Desired state:** Standards that enable interoperability and independent development. Ability to evolve with the evolving needs of the eco-system.  
**Avoid:** Standards become limiting and stifle innovation and evolution.

### Approach
1. **Leverage OpenADR 3.x Design**: Utilize the fixed schema that uses `valuesMap` for attributes and payloads. This establishes key structures like `RESOURCE`, `EVENT`, `REPORT`. But it allows for details to be very flexible — effectively allowing for an arbitrary key-value pair definitions.
2. **3-Layer Semantic Layer**: Using JSON-LD to define meaning. IES defines and evolves key terms without changing the schema. Utilities and others can add their own definitions formally. Occasionally common terms are adopted to allow for evolution.
3. **Application Profiles**: Establish minimum definitions necessary for safe execution of various use cases.

### Use Case: Customer Connection VC
The primary example for this architecture is the issuance of Verifiable Credentials (VCs) for Customer Connections. These VCs utilize the OpenADR `RESOURCE` object to encapsulate mandatory attributes: Customer Name, Address, Connection ID, Meter Number, and Sanctioned Load.

### The "Understand/Ignore" Mandate
To allow for systematic evolution, systems must be designed to understand what they can and ignore what they can't.

> [!IMPORTANT]
> **Mandatory Rule**: Critical safety or billing attributes must be registered as "Required" in an Application Profile. If a system encounters a required attribute it does not understand, it must trigger a Fail-Safe state (see Section 10: Fail-Safe and Validation Logic).

---

## 2. Three-Layer Semantic Architecture

The architecture is divided into three distinct layers to balance national standardization with local innovation:

*   **Layer 1: IES Core**: National standards and universal terms (e.g., `SANCTIONED_LOAD`).
*   **Layer 2: Utility Augmentation**: Regional extensions prefixed with local identifiers (e.g., `KA_SANCTIONED_LOAD`). Utilities define new attributes and meanings but do not change the core OpenADR schema.
*   **Layer 3: Third-Party Extensions**: Experimental or device-specific definitions for DERs and aggregators.

---

## 3. IES Team Setup (Layer 1)

The IES team manages the national root registry and defines the Application Profiles that govern VC issuance and verifier safety logic.

> [!NOTE]
> **Note on Application Profiles**: Ideally, Application Profiles should only include terms defined by the IES (Layer 1) to ensure universal compliance and avoid regional fragmentation in mandatory safety checks.

### Core Deliverables
*   **Structural Schema**: `ies-1.0.json` (The OpenADR-compliant container).
*   **Semantic Bundle**: `ies-core.jsonld` (Merged context and vocabulary mapping terms to IRIs and definitions).
*   **Application Profiles**: Rules for specific use cases (e.g., `customer-connection-v1.json`).

*See Section 8 for deployment commands and file contents.*

---

## 4. Utility Extension & Usage (Layer 2)

Utilities extend the IES Core when local specificities are required. Using DeDi.global, a Utility maps their extension to a local registry to establish formal meaning.

### Extension Policy
Extensions must use local prefixes (e.g., `KA_`). Utilities are responsible for submitting explanations for all expansions to IES to keep the ecosystem in check. To minimize HTTP overhead, Utilities must host a merged context/vocabulary bundle.

*See Section 9 for detailed mapping steps.*

---

## 5. Verification & Fail-Safe Logic

Verifiers process credentials through a Triple-Phase Validation process.

1.  **Phase 1: Structural**
2.  **Phase 2: Semantic**
3.  **Phase 3: Promotion Check**

A system verifies the JSON structure, then "expands" the document to ensure mandatory attributes resolve to IRIs via their `@type` annotations. Finally, Phase 3 handles the decentralized evolution of terms.

### Efficient Verification via Caching
To minimize latency, verifiers should implement a caching layer. Since context and vocabulary records are cryptographically anchored, they are ideal candidates for long-lived caching.

*See Section 10 for a Redis-based caching implementation.*

---

## 6. Promotion Path (Submission Policy)

The onus is on Utilities to submit expansions for promotion to the IES Core:
1.  **Submit**: Utility submits an explanation of the term to IES.
2.  **Review**: IES reviews for multi-Utility utility.
3.  **Promote**: Term is added to `ies-core.jsonld` (e.g., `KA_SANCTIONED_LOAD` -> `SANCTIONED_LOAD`).

---

## 7. Critical Review & Architectural Risks

### Identified Risks
*   **Latency in Semantic Resolution**: Resolving layered contexts requires multiple HTTP calls. **Mitigation**: Mandatory Redis caching at the verifier node.
*   **Context Injection Attacks**: A malicious issuer could redefine a core IES term. **Mitigation**: Phase 2 validation must verify that the expanded IRI for a core term matches the known IES namespace.
*   **Schema Rigidity vs. Semantic Fluidity**: While OpenADR is flexible, structural validation is strict. Utilities must ensure extensions remain within the attributes bucket.

---

## 8. IES Core Registry Files & Deployment

### 1. IES-1.0 Structural Schema (ies-1.0.json)
Resolvable at: `https://api.dedi.global/v1/schemas/ies-1.0`

> [!NOTE]
> For brevity — this is limited to a subset of `RESOURCE` definition. The overall schema would be larger to include `REPORT`, `EVENT`, `POLICY`, etc.
>
> **Note**: The attributes is a very flexible key value pair.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "IES Resource Schema",
  "type": "object",
  "required": [
    "resourceName",
    "attributes"
  ],
  "properties": {
    "resourceName": {
      "type": "string"
    },
    "attributes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "type",
          "values"
        ],
        "properties": {
          "type": {
            "type": "string"
          },
          "values": {
            "type": "array"
          }
        }
      }
    }
  }
}
```

### 2. IES Core Context & Vocab (ies-core.jsonld)
Resolvable at: `https://api.dedi.global/v1/context/ies-core`

> [!NOTE]
> Note: this is establishing a set of standard attributes. This would be a much larger list.

```json
{
  "@context": {
    "ies": "https://api.dedi.global/v1/vocab/ies#",
    "schema": "https://schema.org/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "EnergyResource": "ies:EnergyResource",
    "CUSTOMER_NAME": "ies:CUSTOMER_NAME",
    "ADDRESS": "ies:ADDRESS",
    "CONNECTION_ID": "ies:CONNECTION_ID",
    "METER_SERIAL_NO": "ies:METER_SERIAL_NO",
    "SANCTIONED_LOAD": "ies:SANCTIONED_LOAD"
  },
  "@graph": [
    {
      "@id": "ies:EnergyResource",
      "@type": "rdfs:Class",
      "rdfs:label": "Energy Resource"
    },
    {
      "@id": "ies:CUSTOMER_NAME",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "schema:name",
      "rdfs:label": "Customer Name"
    },
    {
      "@id": "ies:ADDRESS",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "schema:address",
      "rdfs:label": "Connection Address"
    },
    {
      "@id": "ies:CONNECTION_ID",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "schema:serviceIdentifier",
      "rdfs:label": "Connection ID"
    },
    {
      "@id": "ies:METER_SERIAL_NO",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "schema:serialNumber",
      "rdfs:label": "Meter Serial Number"
    },
    {
      "@id": "ies:SANCTIONED_LOAD",
      "@type": "rdf:Property",
      "rdfs:label": "Sanctioned Load"
    }
  ]
}
```

### 3. Customer Connection Application Profile (customer-connection-v1.json)
Resolvable at: `https://api.dedi.global/v1/profiles/customer-connection-v1`

```json
{
  "profile": "CustomerConnection_v1",
  "version": "1.0.0",
  "required_term_uris": [
    "https://api.dedi.global/v1/vocab/ies#CUSTOMER_NAME",
    "https://api.dedi.global/v1/vocab/ies#ADDRESS",
    "https://api.dedi.global/v1/vocab/ies#CONNECTION_ID",
    "https://api.dedi.global/v1/vocab/ies#METER_SERIAL_NO",
    "https://api.dedi.global/v1/vocab/ies#SANCTIONED_LOAD"
  ]
}
```

### 4. Detailed DeDi Setup: IES Team
1. **Initialize Namespace**: `dedi ns create did:dedi:ies --admin <key>`
2. **Upload Artifacts**:
```bash
dedi record add --ns did:dedi:ies --id ies-1.0 --file ./ies-1.0.json --public
dedi record add --ns did:dedi:ies --id core-context --file ./ies-core.jsonld --public
dedi record add --ns did:dedi:ies --id customer-connection-profile --file ./customer-connection-v1.json --public
```

---

## 9. Utility Extension Registry

### Utility DeDi Setup
1. **Sub-Namespace**: `dedi ns create did:dedi:ies:bescom --parent did:dedi:ies`
2. **Merged Local Context/Vocab**:
```bash
dedi record add --ns did:dedi:ies:bescom --id context --file ./bescom-ext.jsonld --public
```

### Example bescom-ext.jsonld
Resolvable at: `https://api.dedi.global/v1/context/discom-ka`

```json
{
  "@context": {
    "bescom": "https://api.dedi.global/v1/vocab/bescom#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "KA_SANCTIONED_LOAD": "bescom:KA_SANCTIONED_LOAD",
    "KA_DISTRICT_CODE": "bescom:KA_DISTRICT_CODE"
  },
  "@graph": [
    {
      "@id": "bescom:KA_SANCTIONED_LOAD",
      "@type": "rdfs:Property",
      "rdfs:label": "KA Sanctioned Load"
    }
  ]
}
```

### Example: Issued Verifiable Credential (VC)
A BESCOM-issued VC referencing the national IES structural schema and the Customer Connection Application Profile.

> [!NOTE]
> Note the use of standard as well as extended attributes.

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://api.dedi.global/v1/context/ies-core",
    "https://api.dedi.global/v1/context/discom-ka"
  ],
  "id": "urn:uuid:550e8400-e29b-41d4-a716-446655440000",
  "type": [
    "VerifiableCredential",
    "EnergyResourceCredential"
  ],
  "issuer": "did:dedi:ies:bescom",
  "issuanceDate": "2025-10-01T12:00:00Z",
  "credentialSchema": {
    "id": "https://api.dedi.global/v1/schemas/ies-1.0",
    "type": "JsonSchemaValidator2018"
  },
  "applicationProfile": "https://api.dedi.global/v1/profiles/customer-connection-v1",
  "credentialSubject": {
    "id": "did:example:customer-123",
    "resourceName": "Connection-001",
    "attributes": [
      {
        "@type": "CUSTOMER_NAME",
        "type": "CUSTOMER_NAME",
        "values": [
          "Arjun Singh"
        ]
      },
      {
        "@type": "ADDRESS",
        "type": "ADDRESS",
        "values": [
          "123 MG Road, Bengaluru, KA, 560001"
        ]
      },
      {
        "@type": "CONNECTION_ID",
        "type": "CONNECTION_ID",
        "values": [
          "CONN-BENG-0992"
        ]
      },
      {
        "@type": "METER_SERIAL_NO",
        "type": "METER_SERIAL_NO",
        "values": [
          "MT-IES-778899"
        ]
      },
      {
        "@type": "SANCTIONED_LOAD",
        "type": "SANCTIONED_LOAD",
        "values": [
          5.5
        ]
      },
      {
        "@type": "KA_DISTRICT_CODE",
        "type": "KA_DISTRICT_CODE",
        "values": [
          "KA-03"
        ]
      }
    ]
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "proofValue": "..."
  }
}
```

---

## 10. Fail-Safe and Validation Logic
Python Triple-Phase Validator with Redis Caching

```python
import redis
import json
from pyld import jsonld
import jsonschema

# Initialize Redis Cache (TTL: 24 Hours)
cache = redis.Redis(host='localhost', port=6379, db=0)

async def get_cached_context(url):
    cached_data = cache.get(url)
    if cached_data:
        return json.loads(cached_data)
    
    # Fallback to DeDi HTTP resolution
    response = await fetch_from_dedi(url)
    cache.setex(url, 86400, json.dumps(response))
    return response

async def validate_customer_connection(payload, context_urls, profile):
    # PHASE 1: Structural Check
    jsonschema.validate(instance=payload, schema=ies_schema)

    # PHASE 2: Semantic Resolution with Caching
    local_contexts = {url: await get_cached_context(url) for url in context_urls}
    expanded = jsonld.expand(payload, {'expandContext': context_urls})
    
    # Extract resolved IRIs
    resolved_iris = []
    if expanded and 'https://api.dedi.global/v1/vocab/ies#attributes' in expanded[0]:
        attributes = expanded[0]['https://api.dedi.global/v1/vocab/ies#attributes']
        for attr in attributes:
            if '@type' in attr:
                resolved_iris.append(attr['@type'][0])

    # PHASE 3: Check against Profile Requirements
    for term_uri in profile['required_term_uris']:
        if term_uri not in resolved_iris:
            await trigger_fail_safe(term_uri)
            raise Exception(f"CRITICAL: Mandatory attribute {term_uri} missing.")
    
    return True

async def trigger_fail_safe(missing_term):
    print(f"!!! FAIL-SAFE ACTIVATED !!! Missing: {missing_term}")
```
