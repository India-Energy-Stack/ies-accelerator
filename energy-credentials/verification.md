# Verification

DISCOMs primarily *issue* credentials, but you will be asked two questions repeatedly by partners:

1. **"How do we verify the credentials you give our consumer?"** — for banks, marketplaces, regulators, service providers receiving a credential.
2. **"How do I check a credential I just issued is well-formed?"** — for your own QA before pushing to DigiLocker.

This page answers both. It is intentionally short — verification is a property of the credential, not something the DISCOM has to host as a service.

---

## What Verification Checks

A successful verification confirms all of these:

| Check | What it means |
|---|---|
| `signature` | The `proof.proofValue` matches the issuer's published public key |
| `date` / `notBefore` / `expiry` | `validFrom` ≤ now ≤ `validUntil` |
| `keyResolution` | The issuer DID resolves successfully (for `did:web`, the well-known JSON exists) |
| `x5c` (if present) | The DSC certificate chain validates against a CSCA trust store |
| `revocation` | The credential's hash is **not** present in the DeDi revocation registry |
| `schema` | The credential body conforms to its DEG schema |
| `context` | All JSON-LD `@context` URLs are known and resolvable |

The overall result is a single boolean plus an enum:

```json
{
  "valid": true,
  "code": "VALID",
  "message": "Credential is valid.",
  "checks": [
    { "name": "signature", "passed": true },
    { "name": "date", "passed": true },
    { "name": "revocation", "passed": true }
  ]
}
```

Possible `code` values: `VALID`, `REVOKED`, `EXPIRED`, `INVALID`, `UNRESOLVABLE`, `CONTEXT_MISSING`.

---

## Verifying With OpenCred

Anyone — including your own QA pipeline — can run the same OpenCred server in verify-only mode. No issuer key is needed for verification; mount no `OPENCRED_KEY_PATH` and the server happily verifies inbound credentials.

### `POST /v1/credentials/verify`

**Auth:** `Authorization: Bearer $OPENCRED_API_KEY`
**Content-Type:** `application/json` (for JSON-LD VC / vc-jwt / sd-jwt-vc / OPENCRED1: token)
**Content-Type:** `application/pdf` (raw PDF body — OpenCred extracts the embedded payload)

```bash
# JSON-LD credential
curl -X POST http://localhost:3100/v1/credentials/verify \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"credential": "<full VC JSON as a string>"}'

# PDF certificate
curl -X POST http://localhost:3100/v1/credentials/verify \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/pdf" \
  --data-binary @nycer-credential.pdf
```

The request body's `credential` field accepts the credential serialised as a string — JSON-LD, vc-jwt, sd-jwt-vc, or an `OPENCRED1:` compact token. OpenCred auto-detects the format.

---

## How a Partner Verifies What You Issued

Hand partners three things, and they can verify without contacting you:

1. **The credential JSON / PDF / QR** — delivered via DigiLocker or directly
2. **Your issuer DID** (`did:web:ies.tpddl.in`) — already inside the credential's `issuer.id`
3. **The OpenCred Docker image link** — `ghcr.io/nfh-trust-labs/opencred/opencred-server:latest`

That is the entire verifier onboarding. The partner runs OpenCred (or the `opencred verify` CLI, or the desktop app's Verify tab), feeds it the credential, and reads `valid: true|false`.

For `did:web` credentials, the partner needs outbound HTTPS to your domain so they can fetch `did.json`. For `did:key` credentials (from DSC-based issuers), verification works fully offline.

---

## Checking Revocation Status Separately

If a verifier already trusts the signature and only wants to recheck status — e.g. a verifier polling daily for a long-lived credential:

```bash
curl -X POST http://localhost:3100/v1/credentials/revocation-status \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"hash": "d6f4e2c9b7a8...e1f0"}'
```

The hash is `SHA-256(JCS(credential))` — computable from the credential without contacting you.

---

## QA Pattern for DISCOM Teams

Before pushing a newly issued credential to DigiLocker, round-trip it through Verify in your CI:

```python
# After POST /v1/credentials/issue
import json, requests
vc = response["credential"]
v = requests.post(
    f"{OPENCRED_URL}/v1/credentials/verify",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={"credential": json.dumps(vc)},
).json()
assert v["valid"], v
```

This catches:

- Schema drift between your `inlineContext` and the DEG canonical context
- Stale or unpublished `did:web` documents (you bumped the key but forgot to upload)
- DeDi misconfiguration (verifier can't reach the registry)
- Expired `validUntil` (clock skew on the issuing host)

Bake this into your integration tests.

---

## Common Failure Modes

| `code` | `checks` failure | What it means |
|---|---|---|
| `INVALID` | `signature` failed | Credential was modified after signing, or the verifier resolved the wrong public key |
| `EXPIRED` | `date` failed with `validUntil` in past | Re-issue or revoke |
| `REVOKED` | `revocation` failed | Credential hash is in DeDi — expected behaviour for revoked credentials |
| `UNRESOLVABLE` | `keyResolution` failed | `did:web` JSON not reachable; check `https://<domain>/.well-known/did.json` |
| `CONTEXT_MISSING` | `context` failed | A JSON-LD `@context` URL OpenCred doesn't recognise; ship updated contexts |

---

## DigiLocker-Delivered Credentials

When a consumer shares an NYCER / DEG credential through DigiLocker's OAuth flow, DigiLocker returns an XML envelope. Decode `<VcContent>` (base64) into a JSON object and pass it to OpenCred:

```python
import base64, json, requests, xml.etree.ElementTree as ET

root = ET.fromstring(digilocker_xml)
vc_b64 = root.find(".//VcContent").text
vc_json = json.loads(base64.b64decode(vc_b64))

result = requests.post(
    f"{OPENCRED_URL}/v1/credentials/verify",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={"credential": json.dumps(vc_json)},
).json()
assert result["valid"]
```

The DigiLocker HMAC proves the envelope came from DigiLocker; the OpenCred verification proves the credential inside came from you. Verifiers should check both.

---

## References

- [OpenCred — API reference (verify)](https://opencred.gitbook.io/docs/docker-image/api-reference)
- [OpenCred — Verifying credentials (Desktop)](https://opencred.gitbook.io/docs/desktop-app/verifying-credentials)
- [OpenCred — Revocation](https://opencred.gitbook.io/docs/concepts/revocation)
