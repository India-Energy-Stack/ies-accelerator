# Issuing Credentials

This page covers the IES Credential Service API calls used to create and sign credentials. The IES credential service is based on [OpenCred](https://opencred.gitbook.io/docs) — refer to the OpenCred documentation for deeper coverage of the underlying flows.

---

## Overview

Issuance involves two API calls:

1. `POST /credential/credentials/issue` — create and sign the credential
2. `GET /credential/credentials/{id}` — retrieve the credential (JSON-LD or PDF)

Both calls require your `issuer_did` and `schema_id` obtained during onboarding, plus an API key in the `Authorization` header.

---

## Step 1 — Issue a Credential

### Request

```http
POST /credential/credentials/issue
Authorization: Bearer {ies_api_key}
Content-Type: application/json
```

```json
{
  "issuer_did": "did:ies:discom-tpddl",
  "schema_id": "ies:schema:nycer:v1",
  "subject": {
    "fullName": "Priya Sharma",
    "consumerNumber": "TPDDL-2025-001234567",
    "serviceAddress": "Flat 4B, Sector 12, Rohini, New Delhi – 110085",
    "serviceConnectionDate": "2019-03-15",
    "meterNumber": "MTR-98765432",
    "maskedIdNumber": "XXXX-XXXX-1234"
  },
  "validity": {
    "from": "2026-04-01T00:00:00Z",
    "until": "2027-04-01T00:00:00Z"
  }
}
```

| Field | Required | Description |
|---|---|---|
| `issuer_did` | Yes | Your DISCOM's DID from onboarding |
| `schema_id` | Yes | Credential schema to use |
| `subject` | Yes | The claims to embed. Fields depend on schema. |
| `subject.maskedIdNumber` | Yes | Masked Aadhaar or other ID — never store or transmit the full number |
| `validity.from` | Yes | ISO 8601 — when the credential becomes valid |
| `validity.until` | No | ISO 8601 — expiry date. Omit for non-expiring credentials. |

### Response

```json
{
  "credential_id": "nycer-TPDDL-001234567-20260401",
  "status": "issued",
  "credential": {
    "@context": [
      "https://www.w3.org/2018/credentials/v1",
      "https://ies.energy/credentials/v1"
    ],
    "id": "https://ies.energy/credentials/nycer-TPDDL-001234567-20260401",
    "type": ["VerifiableCredential", "ElectricityConnectionCredential"],
    "issuer": {
      "id": "did:ies:discom-tpddl",
      "name": "Tata Power Delhi Distribution Limited"
    },
    "issuanceDate": "2026-04-01T10:00:00Z",
    "expirationDate": "2027-04-01T00:00:00Z",
    "credentialSubject": {
      "id": "did:ies:consumer-TPDDL-001234567",
      "fullName": "Priya Sharma",
      "consumerNumber": "TPDDL-2025-001234567",
      "serviceAddress": "Flat 4B, Sector 12, Rohini, New Delhi – 110085",
      "serviceConnectionDate": "2019-03-15",
      "meterNumber": "MTR-98765432"
    },
    "credentialStatus": {
      "id": "https://ies.energy/status/tpddl-2026#94567",
      "type": "StatusList2021Entry",
      "statusPurpose": "revocation",
      "statusListIndex": "94567",
      "statusListCredential": "https://ies.energy/status/tpddl-2026"
    },
    "proof": {
      "type": "Ed25519Signature2020",
      "created": "2026-04-01T10:00:00Z",
      "proofPurpose": "assertionMethod",
      "verificationMethod": "did:ies:discom-tpddl#key-1",
      "proofValue": "z3FXQ...signature...kKJh6"
    }
  }
}
```

Save the `credential_id` — you need it to retrieve the PDF and to pass in the DigiLocker Pull URI response.

---

## Step 2 — Retrieve the Credential PDF

The IES service renders the credential as a signed PDF with an embedded QR code.

### Request

```http
GET /credential/credentials/{credential_id}?template={template_id}
Authorization: Bearer {ies_api_key}
```

| Parameter | Description |
|---|---|
| `credential_id` | From the issue response |
| `template` | (optional) PDF template ID. Defaults to the IES standard template. |

### Response

```
Content-Type: application/pdf
Body: <binary PDF>
```

Base64-encode this PDF before embedding it in the DigiLocker `PullURIResponse`.

---

## Issuing Asset Credentials

For asset credentials (green energy certificates, safety compliance), the flow is the same. Use the appropriate schema and include asset-specific fields:

```json
{
  "issuer_did": "did:ies:renewable-authority",
  "schema_id": "ies:schema:green-energy-cert:v1",
  "subject": {
    "era": "household-solar-001.greenenergy.tpddl.in",
    "energySource": "solar",
    "installedCapacityKW": 5,
    "annualGenerationKWh": 6000,
    "certificationStandard": "ISO 50001:2018",
    "certificationDate": "2026-04-01"
  },
  "validity": {
    "from": "2026-04-01T00:00:00Z",
    "until": "2031-04-01T00:00:00Z"
  }
}
```

---

## Revoking a Credential

If a consumer's connection is terminated, or an asset fails a re-inspection, revoke the credential:

```http
POST /credential/credentials/{credential_id}/revoke
Authorization: Bearer {ies_api_key}
Content-Type: application/json
```

```json
{
  "reason": "connection_terminated"
}
```

This sets the bit at the credential's `statusListIndex` in the issuer's status list. Any subsequent verification will return `revoked: true`.

---

## Error Codes

| HTTP Status | Code | Description |
|---|---|---|
| 400 | `invalid_schema` | `schema_id` not registered or `subject` fields don't match schema |
| 401 | `unauthorized` | Invalid or missing API key |
| 422 | `subject_not_found` | Subject DID could not be resolved |
| 500 | `signing_failed` | Internal error during credential signing — retry |

---

## Reference

- [OpenCred Issuance Docs](https://opencred.gitbook.io/docs) — full issuance API reference with additional options (batch issuance, custom proof types, BBS+ selective disclosure setup)
- [W3C VC Data Model — Issuance](https://www.w3.org/TR/vc-data-model/#lifecycle-details)
