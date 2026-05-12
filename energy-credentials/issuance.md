# Issuing Credentials

This page covers the end-to-end mechanics of issuing DEG energy credentials from OpenCred: single issue, batch issue, integrating with your CIS / NMS, packaging output, and revoking.

You should have OpenCred running and a signing key loaded ([Deployment](./onboarding.md)).

---

## The Core Flow

```
Your integration service
        │
        ▼
1. Read consumer/asset facts from CIS, NMS, MDM, DER registry
        │
        ▼
2. Build credentialSubject matching the DEG schema (see Schemas page)
        │
        ▼
3. POST /v1/credentials/issue → OpenCred signs locally, returns VC
        │
        ▼
4. Deliver to consumer:
       - Push to DigiLocker via PullURIResponse (most consumers)
       - Send to consumer wallet via DID-to-DID protocol
       - Email PDF / QR
       - Display in your DISCOM consumer portal
        │
        ▼
5. (Later) Revoke when facts change — POST /v1/credentials/revoke
```

Every step 1–5 is HTTP calls against OpenCred plus a thin glue layer in whichever language your DISCOM uses.

---

## `POST /v1/credentials/issue`

**Auth:** `Authorization: Bearer $OPENCRED_API_KEY`
**Content-Type:** `application/json`

### Request body

| Field | Type | Required | Notes |
|---|---|---|---|
| `issuerDid` | string | ✓ | Your DISCOM DID — `did:web:ies.tpddl.in` or `did:key:…` |
| `credentialSubject` | object | ✓ | The facts being attested. Must match the chosen schema. |
| `validFrom` | ISO 8601 string | ✓ | Credential is valid from this instant |
| `validUntil` | ISO 8601 string | | Optional expiration |
| `schemaId` | string | one of these | Built-in schema ID (e.g. `deg/utility-customer/v2`) |
| `inlineSchema` | object | one of these | JSON Schema fragment for the credential subject |
| `inlineContext` | object | | JSON-LD `@context` fragment to merge in |
| `proofFormat` | enum | | `vc-jwt` (OpenCred default) \| `data-integrity` (recommended for DEG) \| `sd-jwt-vc` |
| `additionalTypes` | string[] | | E.g. `["EnergyCredential", "UtilityCustomerCredential"]` |
| `subjectDid` | string | | Overrides `credentialSubject.id` if you prefer to pass it separately |
| `selectiveDisclosureClaims` | string[] | | For `sd-jwt-vc` — which fields are individually disclosable |
| `revocationRegistryUrl` | string | | DeDi registry URL; OpenCred embeds the `credentialStatus` block |
| `credentialSchemaUrl` | string | | `credentialSchema.id` for the issued VC |
| `packageFormats` | enum[] | | Any of `qr-png`, `qr-svg`, `pdf`, `json`, `json-compact` |

### Response

```json
{
  "credential": { /* signed VC JSON-LD, or compact JWT string */ },
  "proofFormat": "data-integrity",
  "isCompactToken": false,
  "packagedOutputs": [
    { "format": "pdf", "contentBase64": "JVBERi0xLj..." },
    { "format": "qr-png", "contentBase64": "iVBORw0KG..." }
  ]
}
```

Store the full `credential` JSON — you will hand it to DigiLocker, to a DID wallet, or to a verifier.

---

## Worked Example — `UtilityCustomerCredential`

This is the foundational credential every new connection should receive.

```bash
curl -X POST http://localhost:3100/v1/credentials/issue \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "issuerDid": "did:web:ies.tpddl.in",
    "additionalTypes": ["EnergyCredential", "UtilityCustomerCredential"],
    "proofFormat": "data-integrity",
    "validFrom": "2026-05-01T00:00:00Z",
    "validUntil": "2031-05-01T00:00:00Z",
    "inlineContext": {
      "@context": [
        "https://schema.beckn.io/EnergyCredential/v2.0",
        "https://schema.beckn.io/UtilityCustomerCredential/v2.0"
      ]
    },
    "credentialSubject": {
      "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
      "consumerNumber": "TPDDL-2025-001234567",
      "fullName": "Priya Sharma",
      "installationAddress": {
        "fullAddress": "Flat 4B, Sector 12, Rohini",
        "postalCode": "110085",
        "country": "IN",
        "city": "New Delhi",
        "stateProvince": "DL"
      },
      "meterNumber": "MTR-98765432",
      "serviceConnectionDate": "2019-03-15",
      "maskedIdNumber": "XXXX-XXXX-1234"
    },
    "revocationRegistryUrl": "https://dedi.global/dedi/query/tpddl/vc-revocation-registry",
    "packageFormats": ["pdf", "qr-png"]
  }'
```

OpenCred sets `issuer` from the `issuerDid` you pass, fills `proof`, and (with `revocationRegistryUrl`) fills `credentialStatus`. **OpenCred's request schema has no field for `issuer.name` or `issuer.licenseNumber`** — both are DEG-required, so your integration service must post-process the returned credential and replace the issuer block with the full DEG-conformant object:

```python
vc = response["credential"]
vc["issuer"] = {
    "id": ISSUER_DID,
    "name": ISSUER_NAME,
    "licenseNumber": LICENSE_NUMBER,
}
# Also rewrite credentialStatus.type from "dedi" to "dediregistry" — see concepts.md
if "credentialStatus" in vc:
    vc["credentialStatus"]["type"] = "dediregistry"
```

Wrap this in a thin DISCOM-side helper so every issued credential lands in DEG-conformant shape before delivery. (Note: post-processing the credential body invalidates the original `proof`. If you need a single signed-and-DEG-conformant artifact, re-sign the modified credential — typically by calling OpenCred again with the patched fields, or by signing it in your own service.)

---

## Worked Example — `GenerationProfileCredential`

For a rooftop solar commissioning:

```json
{
  "issuerDid": "did:web:ies.tpddl.in",
  "additionalTypes": ["EnergyCredential", "GenerationProfileCredential"],
  "proofFormat": "data-integrity",
  "validFrom": "2026-05-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3...",
    "consumerNumber": "TPDDL-2025-001234567",
    "generationType": "Solar",
    "capacityKW": 4.5,
    "commissioningDate": "2025-08-20",
    "assetId": "TPDDL-DER-2025-A11023",
    "manufacturer": "Tata Power Solar",
    "modelNumber": "TP-330W-MONO"
  },
  "revocationRegistryUrl": "https://dedi.global/dedi/query/tpddl/vc-revocation-registry"
}
```

All five DEG credential subject shapes are documented in [Schemas](./schemas.md).

---

## Integrating With Your CIS / NMS

Your integration service sits between the consumer-facing trigger (new connection, DER commissioning, program enrolment) and OpenCred.

### Reference architecture

```
   ┌──────────────────┐
   │ CIS / Billing DB │──┐
   └──────────────────┘  │     ┌─────────────────────┐      ┌──────────────┐
   ┌──────────────────┐  │     │  Issuance Service   │      │   OpenCred   │
   │ DER registry /   │──┼────▶│  (your code)        │─────▶│  /v1/issue   │
   │ Net-metering DB  │  │     │  Python / Java / Go │      └──────────────┘
   └──────────────────┘  │     └─────────────────────┘
   ┌──────────────────┐  │              │
   │ Program/DR DB    │──┘              ▼
   └──────────────────┘        ┌─────────────────────┐
                               │  Delivery channel   │
                               │  DigiLocker / DID / │
                               │  Email / Portal     │
                               └─────────────────────┘
```

### Triggers

| Event | Source system | Credential to issue |
|---|---|---|
| New service connection activated | CIS | `UtilityCustomerCredential` + `ConsumptionProfileCredential` |
| Tariff category change | Billing | New `ConsumptionProfileCredential`; revoke previous |
| Solar / DER commissioned | DER registry | `GenerationProfileCredential` |
| Battery commissioned | DER registry | `StorageProfileCredential` |
| Program enrolment | Program ops | `ProgramEnrollmentCredential` |
| Enrolment withdrawal / expiry | Program ops | Revoke `ProgramEnrollmentCredential` |
| Disconnection / closure | CIS | Revoke `UtilityCustomerCredential` + dependents |

### Reference handler — Python

```python
import os, requests
from datetime import datetime, timedelta

OPENCRED_URL = "http://opencred:3100"
OPENCRED_API_KEY = os.environ["OPENCRED_API_KEY"]
ISSUER_DID = "did:web:ies.tpddl.in"
ISSUER_NAME = "Tata Power Delhi Distribution Limited"
LICENSE_NUMBER = "DERC/DL/2025/0042"
DEDI_REVOCATION_URL = "https://dedi.global/dedi/query/tpddl/vc-revocation-registry"

def issue_utility_customer_credential(consumer, holder_did):
    body = {
        "issuerDid": ISSUER_DID,
        "additionalTypes": ["EnergyCredential", "UtilityCustomerCredential"],
        "proofFormat": "data-integrity",
        "validFrom": datetime.utcnow().isoformat() + "Z",
        "validUntil": (datetime.utcnow() + timedelta(days=5*365)).isoformat() + "Z",
        "credentialSubject": {
            "id": holder_did,
            "consumerNumber": consumer.consumer_number,
            "fullName": consumer.full_name,
            "installationAddress": {
                "fullAddress": consumer.address_line,
                "postalCode": consumer.pincode,
                "country": "IN",
                "city": consumer.city,
                "stateProvince": consumer.state_code,
            },
            "meterNumber": consumer.meter_number,
            "serviceConnectionDate": consumer.connection_date.isoformat(),
            "maskedIdNumber": consumer.masked_aadhaar,
        },
        "revocationRegistryUrl": DEDI_REVOCATION_URL,
        "packageFormats": ["pdf", "qr-png"],
    }
    r = requests.post(
        f"{OPENCRED_URL}/v1/credentials/issue",
        headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
        json=body,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()
```

### Where the consumer's DID comes from

| Delivery channel | Source of `credentialSubject.id` |
|---|---|
| **DigiLocker** | Generate a per-credential `did:key` and store the mapping in your CIS — DigiLocker does not provide a stable consumer DID today |
| **DID wallet** | The wallet performs a "request credential" handshake and presents its own DID first |
| **Email / paper QR** | Generate a `did:key` server-side and either bind it to the consumer record or accept that it is single-use |

For DigiLocker delivery specifically, see [DigiLocker Integration](./digilocker-integration.md).

---

## Batch Issuance

For migration / backfill scenarios — e.g. issuing `UtilityCustomerCredential` for every existing connection.

### `POST /v1/credentials/batch`

```bash
curl -X POST http://localhost:3100/v1/credentials/batch \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "csvContent": "consumerNumber,fullName,meterNumber,connectionDate\nTPDDL-001,...\n",
    "schemaId": "deg/utility-customer/v2",
    "issuerDid": "did:web:ies.tpddl.in",
    "validFrom": "2026-05-01T00:00:00Z",
    "proofFormat": "data-integrity",
    "additionalTypes": ["EnergyCredential", "UtilityCustomerCredential"],
    "revocationRegistryUrl": "https://dedi.global/dedi/query/tpddl/vc-revocation-registry"
  }'
```

Response:

```json
{
  "jobId": "a1e7c3f9-4b2d-4f21-8c3a-1f4d7e9b2c01",
  "headers": ["consumerNumber", "fullName", "meterNumber", "connectionDate"],
  "validCount": 42,
  "invalidCount": 1,
  "totalCount": 43
}
```

Poll `GET /v1/credentials/batch/{jobId}` for progress:

```json
{
  "jobId": "a1e7c3f9-…",
  "total": 42,
  "completed": 42,
  "successCount": 42,
  "errorCount": 0,
  "running": false,
  "cancelled": false
}
```

Limits: default 1,000 rows per request (configurable via `OPENCRED_BATCH_ROW_LIMIT`); results live in process memory for `OPENCRED_SESSION_TTL` seconds (default 4 hours). Drain to your CIS or object storage before TTL.

---

## Revoking a Credential

DeDi revocation publishes a credential's hash to your namespace. After publication, any verifier checking that credential will see `revoked: true`.

### Compute the hash first (optional, for audit logs)

```bash
curl -X POST http://localhost:3100/v1/credentials/revocation-hash \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"credential": { /* full signed VC */ }}'
# → {"hash":"d6f4e2c9b7a8...e1f0"}
```

### Publish the revocation

```bash
curl -X POST http://localhost:3100/v1/credentials/revoke \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"hash": "d6f4e2c9b7a8...e1f0"}'
# → {"hash":"d6f4...","revoked":true,"revokedAt":"2026-05-01T10:00:00.000Z"}
```

Or revoke by passing the full credential — OpenCred recomputes the hash:

```bash
curl -X POST http://localhost:3100/v1/credentials/revoke \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"credential": { /* full signed VC */ }}'
```

Only the namespace owner (your DISCOM, holding the DeDi API key configured on this OpenCred instance) can revoke into your namespace.

### Batch revocation hashes

```bash
curl -X POST http://localhost:3100/v1/credentials/revocation-hash/batch \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"credentials": [ /* …array of VCs… */ ]}'
```

### Hash stability rules

The hash is `SHA-256(JCS(credential))`. To stay reproducible, callers must always pass the **same shape** to both issuance and revocation — typically the signed credential. Mutating the `proof` block (e.g. via re-canonicalisation) changes the hash. OpenCred handles this internally; just always pass the credential as you stored it.

---

## Lifecycle Patterns

### Re-issuing on data change

When a fact changes (new tariff category, new sanctioned load), the cleanest pattern is:

1. Issue a new credential with the updated `credentialSubject`.
2. Revoke the old credential.
3. Push the new credential to the consumer's wallet / DigiLocker.

Do not edit and re-sign the old credential — the W3C VC model treats each `id` as immutable.

### Connection closures

On disconnection:

1. Revoke `UtilityCustomerCredential`, `ConsumptionProfileCredential`, and any active `GenerationProfileCredential` / `StorageProfileCredential` / `ProgramEnrollmentCredential`.
2. Push a notification to the consumer wallet (verifiers will see `revoked: true` on next check).

### Programme cohorts

For time-bounded programs (e.g. a 6-month DR pilot), set `validUntil` to the cohort end date. The credential expires automatically — no explicit revocation needed. Revoke only for early withdrawals.

---

## Operational Notes

### Logging and audit

OpenCred logs every issue / revoke call to stdout in JSON (pino). Ship to your aggregator and retain for the credential lifetime + audit window. Do not log `credentialSubject` payloads at level `info`; use `debug` and gate on environment.

### Rate limits

OpenCred itself does not impose rate limits. Apply at your gateway. Issuance is CPU-bound on the signing operation; an `m6i.large` typically handles ~200 ECDSA-P256 signs/sec single-threaded. Scale horizontally — all instances are stateless.

### Idempotency

OpenCred does not deduplicate on `id`. Generate `id` in your integration service (UUIDv4) and store the mapping `consumer_number → credential_id` in your CIS so you can detect a duplicate before signing.

### Selective disclosure

When integrating with verifiers who only need partial fields (e.g. a marketplace that needs `state` but not `address`), issue with `proofFormat: "sd-jwt-vc"` and list the disclosable claims:

```json
{
  "proofFormat": "sd-jwt-vc",
  "selectiveDisclosureClaims": [
    "installationAddress.city",
    "installationAddress.stateProvince",
    "premisesType",
    "connectionType"
  ]
}
```

The consumer's wallet decides which claims to reveal at presentation time.

---

## All Endpoints at a Glance

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/v1/health` | none | Liveness + signing key status |
| `GET` | `/v1/metrics` | none | Prometheus metrics |
| `GET` | `/v1/keys` | yes | List loaded signing keys |
| `POST` | `/v1/keys/publish` | yes | Publish DID doc to DeDi |
| `POST` | `/v1/keys/resolve` | yes | Resolve any DID |
| `GET` | `/v1/schemas` | yes | List available schemas |
| `GET` | `/v1/schemas/:id` | yes | Full schema definition |
| `POST` | `/v1/credentials/issue` | yes | Issue one credential |
| `POST` | `/v1/credentials/batch` | yes | Start batch issue from CSV |
| `GET` | `/v1/credentials/batch/:jobId` | yes | Batch progress |
| `GET` | `/v1/credentials/batch/:jobId/results` | yes | Fetch batch results (errors `409 JOB_RUNNING` while in-flight) |
| `POST` | `/v1/credentials/package` | yes | Re-package an existing credential into QR/PDF/JSON |
| `POST` | `/v1/schemas/generate` | yes | Generate a JSON Schema from a set of example fields |
| `POST` | `/v1/credentials/verify` | yes | Verify a credential (see [Verification](./verification.md)) |
| `POST` | `/v1/credentials/revocation-hash` | yes | Compute revocation hash |
| `POST` | `/v1/credentials/revocation-hash/batch` | yes | Batch hashes |
| `POST` | `/v1/credentials/revoke` | yes | Publish revocation |
| `POST` | `/v1/credentials/revocation-status` | yes | Look up revocation status |
| `POST` | `/v1/dedi/namespace/ensure` | yes | Ensure DeDi namespace + registries |

---

## References

- [OpenCred — API reference](https://opencred.gitbook.io/docs/docker-image/api-reference)
- [OpenCred — Issuing credentials (Desktop)](https://opencred.gitbook.io/docs/desktop-app/issuing-credentials)
- [DEG schemas](./schemas.md)
- [DigiLocker Integration](./digilocker-integration.md)
- [Verification](./verification.md)
