# Issuing Credentials

This page covers the end-to-end mechanics of issuing electricity credentials from OpenCred: single issue, batch issue, integrating with your CIS / NMS, packaging output, and revoking.

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
2. Build credentialSubject matching the CustomerCredential schema (see Schemas page)
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
5. (Later) Revoke or re-issue when facts change — POST /v1/credentials/revoke
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
| `validFrom` | ISO 8601 string | ✓ | Credential is valid from this instant (include timezone) |
| `validUntil` | ISO 8601 string | | Optional expiration (include timezone) |
| `schemaId` | string | one of these | Built-in schema ID — use `electricity/v1` |
| `inlineSchema` | object | one of these | JSON Schema fragment for the credential subject |
| `inlineContext` | object | | JSON-LD `@context` fragment to merge in (rarely needed when using a built-in `schemaId`) |
| `proofFormat` | enum | | `vc-jwt` (recommended) \| `data-integrity` \| `sd-jwt-vc` |
| `additionalTypes` | string[] | | E.g. `["CustomerCredential"]` to add the schema-canonical type label |
| `subjectDid` | string | | Overrides `credentialSubject.id` if you prefer to pass it separately |
| `selectiveDisclosureClaims` | string[] | | For `sd-jwt-vc` — which fields are individually disclosable |
| `revocationRegistryUrl` | string | | DeDi registry URL; OpenCred embeds the `credentialStatus` block |
| `credentialSchemaUrl` | string | | `credentialSchema.id` for the issued VC |
| `packageFormats` | enum[] | | Any of `qr-png`, `qr-svg`, `pdf`, `json`, `json-compact` |

> **Proof format note.** Worked examples below use `proofFormat: "vc-jwt"`. The built-in `electricity/v1` context currently collides with W3C V2 context terms when `additionalTypes` is passed together with `proofFormat: "data-integrity"` — the server returns `CRYPTO_ERROR: Invalid JSON-LD syntax; tried to redefine a protected term`. Use `vc-jwt` for the built-in schema until that's reconciled. `data-integrity` works against schemas you register yourself with a clean context.

### Response

```json
{
  "credential": { /* signed VC JSON-LD, or compact JWT string */ },
  "proofFormat": "vc-jwt",
  "isCompactToken": true,
  "packagedOutputs": [
    { "format": "pdf", "contentBase64": "JVBERi0xLj..." },
    { "format": "qr-png", "contentBase64": "iVBORw0KG..." }
  ]
}
```

Store the full `credential` payload — you will hand it to DigiLocker, to a DID wallet, or to a verifier.

---

## Worked Example — new connection (identity + consumption)

This is the foundational call: a new service connection gets a credential carrying `customerProfile`, `customerDetails`, and one `consumptionProfiles[]` entry. This single call validated end-to-end against `ghcr.io/nfh-trust-labs/opencred/opencred-server:latest`.

```bash
curl -X POST http://localhost:3100/v1/credentials/issue \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "issuerDid": "did:web:ies.tpddl.in",
    "schemaId":  "electricity/v1",
    "additionalTypes": ["CustomerCredential"],
    "proofFormat": "vc-jwt",
    "validFrom":  "2026-05-01T00:00:00+05:30",
    "validUntil": "2031-05-01T00:00:00+05:30",
    "subjectDid": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
    "credentialSubject": {
      "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
      "customerProfile": {
        "customerNumber": "TPDDL-2025-001234567",
        "meterNumber":    "MTR-98765432",
        "meterType":      "AMI",
        "idRef": {
          "issuedBy":  "did:web:uidai.gov.in",
          "subjectId": "uidai.gov.in:XXXX-XXXX-1234"
        }
      },
      "customerDetails": {
        "fullName": "Priya Sharma",
        "installationAddress": {
          "address":   "Flat 4B, Sector 12, Rohini",
          "city":      {"name": "New Delhi", "code": "DEL"},
          "state":     {"name": "Delhi",     "code": "DL"},
          "country":   {"name": "India",     "code": "IN"},
          "area_code": "110085"
        },
        "serviceConnectionDate": "2019-03-15T00:00:00+05:30"
      },
      "consumptionProfiles": [{
        "premisesType":       "Residential",
        "connectionType":     "Single-phase",
        "sanctionedLoadKW":   5,
        "tariffCategoryCode": "DOM-A2"
      }]
    },
    "revocationRegistryUrl": "https://dedi.global/dedi/query/tpddl/vc-revocation-registry",
    "packageFormats": ["pdf", "qr-png"]
  }'
```

OpenCred sets `issuer` to the `issuerDid` string, fills `proof`, and (with `revocationRegistryUrl`) fills `credentialStatus`. **The schema requires the full `issuer` object** (`id`, `name`, optional `idRef`), but OpenCred only accepts the DID string. Your integration service must replace the returned `issuer` field with the schema-conformant object before delivery:

```python
vc = response["credential"]
vc["issuer"] = {
    "id":   ISSUER_DID,
    "name": ISSUER_NAME,
    "idRef": {
        "issuedBy":  REGULATOR_DID,         # e.g. did:web:derc.delhi.gov.in
        "subjectId": REGULATOR_SUBJECT_ID,  # e.g. derc.delhi.gov.in:DERC-DL-2025-0042
    },
}
```

Re-shaping `issuer` invalidates the original `proof`. The practical pattern is to re-sign in your integration service, or to pass the patched fields back through OpenCred for re-signing.

---

## Worked Example — rooftop solar commissioning

When a DER asset is commissioned for an existing connection, re-issue the credential with a populated `generationProfiles[]` entry. The new credential supersedes the previous one; revoke the previous credential after delivery.

```json
{
  "issuerDid": "did:web:ies.tpddl.in",
  "schemaId":  "electricity/v1",
  "additionalTypes": ["CustomerCredential"],
  "proofFormat": "vc-jwt",
  "validFrom":  "2024-08-20T00:00:00+05:30",
  "validUntil": "2034-08-20T00:00:00+05:30",
  "subjectDid": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
    "customerProfile": {
      "customerNumber": "TPDDL-2025-001234567",
      "meterNumber":    "MTR-98765432",
      "meterType":      "NetMeter"
    },
    "generationProfiles": [{
      "assetId":           "DER-TPDDL-2024-005678",
      "generationType":    "Solar",
      "capacityKW":        5.5,
      "commissioningDate": "2024-08-20T00:00:00+05:30",
      "manufacturer":      "Tata Power Solar",
      "modelNumber":       "TP540M-72"
    }]
  }
}
```

For a battery commissioning, populate `storageProfiles[]` with the same pattern. Multiple solar arrays or batteries on the same meter sit as multiple entries in their respective arrays — one credential covers them all.

The full field reference for every sub-profile is in [Schemas](./schemas.md).

---

## Integrating With Your CIS / NMS

Your integration service sits between the consumer-facing trigger (new connection, DER commissioning, asset change) and OpenCred.

### Reference architecture

```
   ┌──────────────────┐
   │ CIS / Billing DB │──┐
   └──────────────────┘  │     ┌─────────────────────┐      ┌──────────────┐
   ┌──────────────────┐  │     │  Issuance Service   │      │   OpenCred   │
   │ DER registry /   │──┼────▶│  (your code)        │─────▶│  /v1/issue   │
   │ Net-metering DB  │  │     │  Python / Java / Go │      └──────────────┘
   └──────────────────┘  │     └─────────────────────┘
                         │              │
                         │              ▼
                         │     ┌─────────────────────┐
                         └────▶│  Delivery channel   │
                               │  DigiLocker / DID / │
                               │  Email / Portal     │
                               └─────────────────────┘
```

### Triggers

Because the schema is a single per-meter credential, every material change is a **re-issue + revoke previous**. There is no "issue a separate credential for each change" pattern.

| Event | Source system | Action |
|---|---|---|
| New service connection activated | CIS | Issue with `customerProfile` + `customerDetails` + `consumptionProfiles[]` |
| Tariff category / load change | Billing | Re-issue with updated `consumptionProfiles`; revoke previous |
| Solar / DER commissioned or decommissioned | DER registry | Re-issue with updated `generationProfiles`; revoke previous |
| Battery commissioned or decommissioned | DER registry | Re-issue with updated `storageProfiles`; revoke previous |
| Address / name change | CIS | Re-issue with updated `customerDetails`; revoke previous |
| Meter swap | NMS / MDM | Re-issue with updated `customerProfile.meterNumber` / `meterType`; revoke previous |
| Disconnection / closure | CIS | Revoke; do not re-issue |

### Reference handler — Python

```python
import os, requests
from datetime import datetime, timedelta, timezone

OPENCRED_URL = "http://opencred:3100"
OPENCRED_API_KEY = os.environ["OPENCRED_API_KEY"]
ISSUER_DID = "did:web:ies.tpddl.in"
ISSUER_NAME = "Tata Power Delhi Distribution Limited"
REGULATOR_DID = "did:web:derc.delhi.gov.in"
REGULATOR_SUBJECT_ID = "derc.delhi.gov.in:DERC-DL-2025-0042"
DEDI_REVOCATION_URL = "https://dedi.global/dedi/query/tpddl/vc-revocation-registry"

IST = timezone(timedelta(hours=5, minutes=30))

def issue_customer_credential(consumer, holder_did):
    body = {
        "issuerDid": ISSUER_DID,
        "schemaId":  "electricity/v1",
        "additionalTypes": ["CustomerCredential"],
        "proofFormat": "vc-jwt",
        "validFrom":  datetime.now(IST).isoformat(),
        "validUntil": (datetime.now(IST) + timedelta(days=5*365)).isoformat(),
        "subjectDid": holder_did,
        "credentialSubject": {
            "id": holder_did,
            "customerProfile": {
                "customerNumber": consumer.consumer_number,
                "meterNumber":    consumer.meter_number,
                "meterType":      consumer.meter_type,  # one of the meterType enum values
                "idRef": {
                    "issuedBy":  "did:web:uidai.gov.in",
                    "subjectId": f"uidai.gov.in:{consumer.masked_aadhaar}",
                },
            },
            "customerDetails": {
                "fullName": consumer.full_name,
                "installationAddress": {
                    "address":   consumer.address_line,
                    "city":      {"name": consumer.city,   "code": consumer.city_code},
                    "state":     {"name": consumer.state,  "code": consumer.state_code},
                    "country":   {"name": "India",         "code": "IN"},
                    "area_code": consumer.pincode,
                },
                "serviceConnectionDate": consumer.connection_date.isoformat(),
            },
            "consumptionProfiles": [{
                "premisesType":       consumer.premises_type,
                "connectionType":     consumer.connection_type,
                "sanctionedLoadKW":   consumer.sanctioned_load_kw,
                "tariffCategoryCode": consumer.tariff_code,
            }],
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
    result = r.json()

    # Inject the schema-required issuer object before delivery.
    # This invalidates the original proof; re-sign downstream if you need a single signed artifact.
    result["credential"]["issuer"] = {
        "id":   ISSUER_DID,
        "name": ISSUER_NAME,
        "idRef": {"issuedBy": REGULATOR_DID, "subjectId": REGULATOR_SUBJECT_ID},
    }
    return result
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

For migration / backfill scenarios — e.g. issuing a `CustomerCredential` for every existing connection.

### `POST /v1/credentials/batch`

```bash
curl -X POST http://localhost:3100/v1/credentials/batch \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "csvContent": "customerNumber,fullName,meterNumber,meterType,connectionDate,pincode,sanctionedLoadKW,tariffCategoryCode\nTPDDL-001,...\n",
    "schemaId":  "electricity/v1",
    "issuerDid": "did:web:ies.tpddl.in",
    "validFrom": "2026-05-01T00:00:00+05:30",
    "proofFormat": "vc-jwt",
    "additionalTypes": ["CustomerCredential"],
    "revocationRegistryUrl": "https://dedi.global/dedi/query/tpddl/vc-revocation-registry"
  }'
```

Response:

```json
{
  "jobId": "a1e7c3f9-4b2d-4f21-8c3a-1f4d7e9b2c01",
  "headers": ["customerNumber", "fullName", "meterNumber", "meterType", "connectionDate", "pincode", "sanctionedLoadKW", "tariffCategoryCode"],
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

The CSV-to-credential mapping is configured server-side; flat columns are mapped into the nested `customerProfile` / `customerDetails` / `consumptionProfiles[0]` shape.

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

Each material change to facts produces a new credential. The cleanest pattern:

1. Issue a new credential with the updated `credentialSubject`.
2. Revoke the previous credential.
3. Push the new credential to the consumer's wallet / DigiLocker.

Do not edit and re-sign an existing credential — the W3C VC model treats each `id` as immutable.

### Connection closures

On disconnection, revoke the active credential. Do not re-issue. Notify the consumer wallet so verifiers see `revoked: true` on next check.

### Time-bounded validity

For credentials tied to time-bounded states (e.g. a 6-month seasonal tariff), set `validUntil` to the end of the period. The credential expires automatically — no explicit revocation needed. Revoke only for early changes.

---

## Operational Notes

### Logging and audit

OpenCred logs every issue / revoke call to stdout in JSON (pino). Ship to your aggregator and retain for the credential lifetime + audit window. Do not log `credentialSubject` payloads at level `info`; use `debug` and gate on environment.

### Rate limits

OpenCred itself does not impose rate limits. Apply at your gateway. Issuance is CPU-bound on the signing operation; an `m6i.large` typically handles ~200 ECDSA-P256 signs/sec single-threaded. Scale horizontally — all instances are stateless.

### Idempotency

OpenCred does not deduplicate on `id`. Generate `id` in your integration service (URN UUID v4) and store the mapping `meter_number → credential_id` in your CIS so you can detect a duplicate before signing.

### Selective disclosure

When integrating with verifiers who only need partial fields (e.g. a marketplace that needs `state` but not full `address`), issue with `proofFormat: "sd-jwt-vc"` and list the disclosable claims:

```json
{
  "proofFormat": "sd-jwt-vc",
  "selectiveDisclosureClaims": [
    "customerDetails.installationAddress.city",
    "customerDetails.installationAddress.state",
    "consumptionProfiles[0].premisesType",
    "consumptionProfiles[0].connectionType"
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
| `POST` | `/v1/keys/resolve` | yes | Resolve any DID (currently requires DeDi — see [Deployment → Verification](./onboarding.md#verifying-the-deployment)) |
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
- [Schemas](./schemas.md)
- [DigiLocker Integration](./digilocker-integration.md)
- [Verification](./verification.md)
