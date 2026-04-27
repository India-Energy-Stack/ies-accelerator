# Verifying Credentials

Verification checks that a credential is authentic, unexpired, and unrevoked. OpenCred handles this entirely locally — no network calls are needed for `did:key` credentials because JSON-LD contexts are bundled and DID resolution runs in-process.

> Full OpenCred documentation: [https://opencred.gitbook.io/docs](https://opencred.gitbook.io/docs)

---

## Two Ways to Verify

| Method | Best for |
|---|---|
| [Desktop Client](#desktop-client) | Manual spot checks, debugging |
| [Docker API](#docker-api) | Production — automated verification in your application |

---

## What Gets Checked

Every verification run performs these checks in sequence:

| Check | What it validates |
|---|---|
| **Signature** | Cryptographic proof against the issuer's public key |
| `validFrom` | Credential is not being used before its issuance date |
| `validUntil` | Credential has not expired |
| **DID resolution** | Issuer DID resolves to a DID document with a matching public key |
| **Revocation** | Credential hash is not present in the DeDi revocation registry |

A credential is valid only when **all checks pass**.

---

## Desktop Client

1. Go to the **Verify** page
2. Paste the credential JSON or load it from a file
3. Click **Verify**
4. Review the results — each check is shown as passed or failed with a reason

For `did:key` credentials, verification is fully offline. For `did:web` credentials, the desktop client fetches the DID document from `https://<domain>/.well-known/did.json` (requires network access).

---

## Docker API

### Deploy

See [Issuing Credentials — Docker API](./issuance.md#docker-api) for deployment instructions. The same container handles both issuance and verification.

### Verify a Credential

```http
POST http://localhost:3100/v1/credentials/verify
Authorization: Bearer sk_prod_change_me
Content-Type: application/json
```

```json
{
  "credential": {
    "@context": [
      "https://www.w3.org/2018/credentials/v1",
      "https://ies.energy/credentials/v1"
    ],
    "id": "urn:uuid:4b3a1c9e-...",
    "type": ["VerifiableCredential", "ElectricityConnectionCredential"],
    "issuer": "did:web:ies.tpddl.in",
    "validFrom": "2026-04-01T00:00:00Z",
    "validUntil": "2027-04-01T00:00:00Z",
    "credentialSubject": { "..." : "..." },
    "proof": { "..." : "..." }
  }
}
```

### Response

```json
{
  "isValid": true,
  "checks": [
    { "name": "signature",  "passed": true },
    { "name": "notBefore",  "passed": true },
    { "name": "expiry",     "passed": true },
    { "name": "revocation", "passed": true }
  ]
}
```

A failed check looks like:

```json
{
  "isValid": false,
  "checks": [
    { "name": "signature", "passed": true },
    { "name": "expiry",    "passed": false, "reason": "Credential expired on 2027-04-01T00:00:00Z" }
  ]
}
```

The HTTP status is always `200` — check the `isValid` field in the response body, not the status code.

---

## Checking Revocation Status Separately

If you only need to check revocation without a full verification:

```http
GET http://localhost:3100/v1/credentials/revocation-status?credentialId=urn:uuid:4b3a1c9e-...
Authorization: Bearer sk_prod_change_me
```

Response:
```json
{
  "revoked": false,
  "checkedAt": "2026-04-26T10:00:00Z"
}
```

---

## How Revocation Works

OpenCred uses a **hash-based revocation registry** via DeDi (a decentralised data infrastructure), rather than a bitstring status list.

When a credential is issued with a `revocationRegistryUrl`, it contains a `credentialStatus` block:

```json
{
  "credentialStatus": {
    "id": "https://dedi.global/dedi/lookup/<namespace>/vc-revocation-registry/<hash>",
    "type": "dedi",
    "statusPurpose": "revocation",
    "statusListCredential": "https://dedi.global/dedi/query/<namespace>/vc-revocation-registry"
  }
}
```

At verification time, OpenCred:
1. Computes `SHA-256(JCS(credential))` — a canonical hash of the credential
2. Queries the DeDi registry for that hash
3. If the hash is found → **revoked**; if not found → **valid**

This means there is no central revocation list to maintain — revocation is proven by presence of the hash, not by a bit at a known position.

---

## Verifying Credentials Shared via DigiLocker

When a consumer shares their credential through DigiLocker's OAuth flow, you receive an XML response. For strong cryptographic assurance beyond the DigiLocker HMAC, extract the `VcContent` field (base64-encoded W3C VC JSON-LD) and pass it to the OpenCred verify endpoint.

```python
import base64, json, requests

# Extract VcContent from DigiLocker XML response
vc_b64 = response_xml.find(".//VcContent").text
vc_json = json.loads(base64.b64decode(vc_b64).decode())

# Verify with OpenCred
result = requests.post(
    "http://localhost:3100/v1/credentials/verify",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={"credential": vc_json}
)
assert result.json()["isValid"]
```

---

## DID Methods and Network Requirements

| DID Method | Resolution | Network needed? |
|---|---|---|
| `did:key` | Decoded from DID string itself | No — fully offline |
| `did:jwk` | Decoded from DID string itself | No — fully offline |
| `did:web` | Fetched from `https://<domain>/.well-known/did.json` | Yes |

For production IES deployments using `did:web`, the verifier's system needs outbound HTTPS to the issuer's domain. OpenCred's `did:web` resolver enforces HTTPS-only, no redirects, private-IP blocking, and a 10-second timeout.

---

## Offline Verification

For `did:key` credentials, OpenCred bundles all required JSON-LD contexts and performs DID resolution in-process. No network calls are made. This makes air-gapped or restricted-network verification possible for credentials issued with `did:key`.
