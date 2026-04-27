# Verifying Credentials

This page covers how verifiers — service providers, marketplaces, applications — check that a credential presented by a holder is authentic, current, and unrevoked.

---

## Two Verification Paths

| Path | When to use | How |
|---|---|---|
| **DigiLocker HMAC verification** | Consumer shares via DigiLocker OAuth | Verify the HMAC header on the DigiLocker response |
| **IES direct verification** | Independent check of the W3C VC | Call `GET /credential/credentials/{id}/verify` |

Both paths can be combined for maximum assurance.

---

## Path 1 — DigiLocker HMAC Verification

When a consumer shares their credential through DigiLocker's OAuth flow, DigiLocker sends you a credential XML with an `x-digilocker-hmac` header. Verify it before trusting any fields.

### Compute the Expected HMAC

```python
import hmac, hashlib, base64

def verify_digilocker_response_hmac(
    response_body: bytes,
    api_key: str,
    received_hmac: str
) -> bool:
    expected = base64.b64encode(
        hmac.new(api_key.encode(), response_body, hashlib.sha256).digest()
    ).decode()
    return hmac.compare_digest(expected, received_hmac)
```

Use `hmac.compare_digest` — not `==` — to prevent timing attacks.

### Extract Claims from the Response

Once the HMAC is verified, parse the credential XML:

```xml
<DocDetails>
  <FullName>Priya Sharma</FullName>
  <ConsumerNumber>TPDDL-2025-001234567</ConsumerNumber>
  <ServiceAddress>Flat 4B, Sector 12, Rohini, New Delhi – 110085</ServiceAddress>
  <ServiceConnectionDate>2019-03-15</ServiceConnectionDate>
  <IssuedBy>Tata Power Delhi Distribution Limited</IssuedBy>
</DocDetails>
```

This is sufficient for most address-verification and consumer-identity use cases.

---

## Path 2 — IES Direct Verification

For stronger assurance — especially in automated or machine-to-machine contexts — call the IES verification API directly.

### Request

```http
GET /credential/credentials/{credential_id}/verify
Authorization: Bearer {verifier_api_key}
```

### Response

```json
{
  "credential_id": "nycer-TPDDL-001234567-20260401",
  "verified": true,
  "checks": {
    "proof_valid": true,
    "not_expired": true,
    "revoked": false,
    "schema_valid": true
  },
  "issuer": {
    "did": "did:ies:discom-tpddl",
    "name": "Tata Power Delhi Distribution Limited",
    "trusted": true
  },
  "subject": {
    "consumerNumber": "TPDDL-2025-001234567",
    "serviceAddress": "Flat 4B, Sector 12, Rohini, New Delhi – 110085"
  }
}
```

| Field | Meaning |
|---|---|
| `proof_valid` | Issuer's cryptographic signature checks out |
| `not_expired` | Current timestamp is within `issuanceDate` – `expirationDate` |
| `revoked` | `false` means the issuer has not revoked this credential |
| `schema_valid` | Credential fields conform to the registered schema |
| `issuer.trusted` | The issuer DID is on the IES trusted issuer registry |

A credential is valid only when **all four checks pass and `revoked` is false**.

---

## Verifying a Verifiable Presentation

In machine-to-machine flows (e.g. a prosumer presenting credentials during a P2P energy trade), the holder sends a **Verifiable Presentation** containing one or more VCs.

### Request

```http
POST /credential/presentations/verify
Authorization: Bearer {verifier_api_key}
Content-Type: application/json
```

```json
{
  "presentation": {
    "@context": ["https://www.w3.org/2018/credentials/v1"],
    "type": "VerifiablePresentation",
    "verifiableCredential": [ /* embedded VCs */ ],
    "proof": {
      "type": "Ed25519Signature2020",
      "challenge": "verifier-nonce-abc123",
      "verificationMethod": "did:ies:consumer-7a3f9b2c#key-1",
      "proofValue": "z3Abc...holder signature...xyz"
    }
  },
  "challenge": "verifier-nonce-abc123",
  "domain": "ies.energy"
}
```

Always pass the same `challenge` you issued to the holder. The service verifies:
- Holder's signature on the outer presentation
- Issuer's signature on each embedded credential
- Challenge matches (prevents replay)
- All embedded credentials pass the standard four checks

### Response

```json
{
  "verified": true,
  "holder_did": "did:ies:consumer-7a3f9b2c",
  "credentials": [
    {
      "id": "nycer-TPDDL-001234567-20260401",
      "type": "ElectricityConnectionCredential",
      "verified": true,
      "issuer": "did:ies:discom-tpddl"
    }
  ]
}
```

---

## Selective Disclosure Verification

When a holder presents a credential with selective disclosure (revealing only certain fields), verify using the same endpoint. The IES service handles BBS+ proof verification automatically. Your response will only contain the fields the holder chose to reveal:

```json
{
  "verified": true,
  "revealed_claims": {
    "serviceConnectionActive": true,
    "serviceState": "Delhi"
  }
}
```

---

## Trusted Issuer Registry

IES maintains a registry of trusted issuer DIDs. Credentials from issuers not on the registry will return `issuer.trusted: false` in the verification response. You may choose to reject such credentials or flag them for manual review.

Contact the IES team to add your organisation's issuer DID to the trusted registry.

---

## Error Codes

| HTTP Status | Code | Description |
|---|---|---|
| 400 | `invalid_presentation` | Malformed VC or VP structure |
| 400 | `challenge_mismatch` | `challenge` in presentation does not match `challenge` in request |
| 404 | `credential_not_found` | `credential_id` does not exist |
| 200 | — | Always 200 even for failed verifications — check `verified` field |

---

## Reference

- [OpenCred Verification Docs](https://opencred.gitbook.io/docs) — deeper coverage of presentation protocols, BBS+ proofs, and custom verification policies
- [W3C VC Verification](https://www.w3.org/TR/vc-data-model/#verification)
- [Status List 2021](https://www.w3.org/TR/vc-status-list/)
