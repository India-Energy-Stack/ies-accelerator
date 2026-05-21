# Verification

DISCOMs primarily *issue* credentials, but you will be asked two questions repeatedly by partners:

1. **"How do we verify the credentials you give our consumer?"** — for banks, marketplaces, regulators, service providers receiving a credential.
2. **"How do I check a credential I just issued is well-formed?"** — for your own QA before pushing to DigiLocker (the round-trip is also in [Issuance → Verify immediately after issue](./issuance.md#verify-immediately-after-issue)).

This page answers both. It is intentionally short — verification is a property of the credential, not something the DISCOM has to host as a service.

---

## Four Verification Surfaces

All four run the same `@opencred/verification` engine and return identical result shapes. Pick the surface that matches the verifier's environment:

| Path | Best for | Inputs accepted |
|---|---|---|
| **Desktop app — Verify tab** | Casual / one-off verification by humans | Pasted JSON · drag-dropped `.json` / `.jsonld` · QR-code image upload (PNG/JPG) · `.pdf` upload · live camera QR scan · pasted compact tokens (vc-jwt, sd-jwt-vc, `OPENCRED1:` PixelPass) |
| **Docker server — `POST /v1/credentials/verify`** | Programmatic / server-to-server / CI/CD | JSON body for text-shaped formats (auto-detected: JSON-LD VC, vc-jwt, sd-jwt-vc, `OPENCRED1:` QR data) **or** raw PDF body with `Content-Type: application/pdf` (v1.3.0+) |
| **`opencred verify` CLI** | One-shot verification from a shell, no HTTP server needed | File path or stdin. Auto-detects JSON-LD, vc-jwt, sd-jwt-vc, `OPENCRED1:`, or PDF. `--json` flag for scripted consumers. Ships inside the public Docker image. |
| **`@opencred/verify` SDK** | Embedding verification inside a Node.js verifier app — banks, marketplaces, regulators | Single-install npm facade over `@opencred/verification`. `createVerifier(options)`, `verifyCredential(input, options)`, `verifyPdf(bytes, options)`, `detectFormat(input)` |

For IES verifier partners building their own in-app verifier (bank loan-approval pipeline, marketplace listing flow, society DER registration), **`@opencred/verify`** is the recommended path — it's a single npm install, ships TypeScript types, and accepts `dedi` config + `trustAnchors` (PEM-encoded CSCA roots for DSC chains) directly in the options object. With zero config it handles `did:key` / `did:jwk` credentials fully offline.

---

## What Verification Checks

A successful verification confirms all of these. The names that appear in `checks[]` depend on the proof format and on what the verifier has configured (e.g. DeDi).

| Check | What it means | When it appears |
|---|---|---|
| `signature` | The `proof.jwt` (vc-jwt) or `proof.proofValue` (data-integrity) matches the issuer's published public key | Always |
| `date` (data-integrity, sd-jwt-vc) or `vc-jwt-claims` (vc-jwt) | `validFrom` ≤ now ≤ `validUntil` | Always |
| `keyResolution` | The issuer DID resolves successfully (for `did:web`, the well-known JSON exists or the DeDi `public_key_registry` fallback resolves) | Always |
| `x5c` (if present) | The DSC certificate chain validates against a CSCA trust store | When the credential carries an `x5c` header |
| `revocation` | The credential's hash is **not** present in the DeDi revocation registry | Only when the verifier has DeDi configured — see [silent-skip warning](#silent-skip-warning) below |
| `schema` | The credential body conforms to its `CustomerCredential` (or `ConsumerEnergyPassport` / `ConsumerMeterDigest`) schema | Always |
| `context` | All JSON-LD `@context` URLs are known and resolvable | data-integrity only |
| `keyRotation` *(advisory)* | DeDi reports `keyStatus: "rotated"` on the issuer's DID document — see [keyRotation](#keyrotation-advisory) | When DeDi is configured and the record has a `keyStatus` |
| `registryAnchor` *(advisory)* | DeDi anchored the DID record on the CORD blockchain by a `creator_did` matching the credential's issuer — see [registryAnchor](#registryanchor-advisory) | When the DeDi record carries a `DediRecordProof2026` |

The overall result is a single boolean plus an enum:

```json
{
  "valid": true,
  "code": "VALID",
  "message": "Credential is valid.",
  "checks": [
    { "name": "signature",  "passed": true },
    { "name": "date",       "passed": true },
    { "name": "revocation", "passed": true }
  ]
}
```

Possible `code` values: `VALID`, `REVOKED`, `EXPIRED`, `INVALID`, `UNRESOLVABLE`, `CONTEXT_MISSING`.

The two advisory checks (`keyRotation`, `registryAnchor`) **do not flip the headline `valid` boolean**. They are observational signals verifier UIs can surface as badges; a credential with `keyRotation: passed=false` is still cryptographically valid because the signature is checked against the key in use at signing time.

### Silent-skip warning

If a verifier does **not** have DeDi configured, OpenCred cannot query the revocation registry and **skips the revocation check entirely** — the response has two checks (`signature`, `date`) instead of three (`signature`, `date`, `revocation`) and a revoked credential will verify as `VALID`. IES verifier partners (banks, marketplaces, regulators, societies) **must** configure DeDi or accept that their tamper-evidence guarantee leaks for the revocation case. See [Concepts → silent-skip warning](./concepts.md#dedi-revocation) for the underlying mechanism.

### keyRotation (advisory)

When a DISCOM rotates its signing key, the DeDi `public_key_registry` record for the previous DID flips from `keyStatus: "current"` to `keyStatus: "rotated"`. The verifier surfaces this as `keyRotation: { passed: false }` — `passed: true` (and silent) otherwise. The credential's signature still verifies because the signature was made against the key in use at signing time; the flag is monotone (`current → rotated`, never back) and exists so end-user verifier UIs can show a "key rotated since signing" badge. Full rotation mechanics in [Concepts → keyStatus rotation](./concepts.md#keystatus-rotation-flag-and-the-cord-anchor-proof).

### registryAnchor (advisory)

When the DeDi instance anchors records on the [CORD blockchain](https://cord.network/), `/v1/keys/resolve` returns an extra `proof` block (`DediRecordProof2026`) attesting that the DID record was anchored on CORD by a named `creator_did`. The verifier compares `creator_did` against the credential's `issuer.id`:

- `passed: true` — the DID record was anchored by the same party that issued the credential. Verifier UIs show a "registry-anchored" badge.
- `passed: false` — anchored by a different party. Verifier UIs may show a suspicion badge.

A missing `proof` is benign on DeDi instances that don't anchor; the check degrades open.

---

## Verifying With OpenCred

Anyone — including your own QA pipeline — can run the same OpenCred server in verify-only mode. No issuer key is needed for verification; mount no `OPENCRED_KEY_PATH` and the server happily verifies inbound credentials.

### `POST /v1/credentials/verify`

**Auth:** `Authorization: Bearer $OPENCRED_API_KEY`
**Content-Type:** `application/json` (for JSON-LD VC / vc-jwt / sd-jwt-vc / OPENCRED1: token)
**Content-Type:** `application/pdf` (raw PDF body — OpenCred extracts the embedded payload)

#### Request shapes per proof format

The `credential` field in the JSON body is **always a string**, but the right string differs by proof format. This is the single most common source of "but my signature is fine, why does it verify as `INVALID`?" — get this right and the rest follows.

| Stored as | Send as `credential` | Notes |
|---|---|---|
| **`vc-jwt`** envelope (the issuance response from `electricity/v1`) | The compact JWS string at `credential.proof.jwt` — **not** the stringified envelope | `jq -r '.credential.proof.jwt' credential.json` |
| **`data-integrity`** JSON-LD envelope | The stringified JSON envelope itself | `jq -c '.credential' credential.json` (single line) or `jq '.credential \| tostring'` |
| **`sd-jwt-vc`** compact token | The raw `~`-separated token verbatim | `jq -r '.credential' credential.json` (if you stored the full response shape) |
| **`OPENCRED1:`** PixelPass payload | The compact token verbatim (the QR string) | typically piped from a QR-scanner / decoder |

Worked example for vc-jwt (matching `electricity/v1` issuance):

```bash
# vc-jwt — extract .proof.jwt and send as the credential field
jq -n --arg c "$(jq -r '.credential.proof.jwt' credential.json)" '{credential: $c}' | \
  curl -s -X POST http://localhost:3100/v1/credentials/verify \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" \
    -d @-
```

PDF certificate (drag the DigiLocker-rendered PDF straight in):

```bash
curl -X POST http://localhost:3100/v1/credentials/verify \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/pdf" \
  --data-binary @nycer-credential.pdf
```

For the PDF path, OpenCred reads the credential payload from the PDF's info-dictionary metadata (`OpenCredCredential`) and verifies it the same way as a directly-posted credential. The QR on the PDF carries the same payload as a fallback for older PDFs without info-dict embedding.

> **Tamper test** (the demo punchline): flip the last character of the JWS signature segment — the part after the last `.` in the JWT — and re-POST. `valid` flips to `false`, the `signature` check fails. For data-integrity / sd-jwt-vc, edit a field in the envelope instead. Worked snippet: [Issuance → Verify immediately after issue](./issuance.md#verify-immediately-after-issue).

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

Before pushing a newly issued credential to DigiLocker, round-trip it through Verify in your CI. The right shape depends on the proof format you used when issuing:

```python
# After POST /v1/credentials/issue
import json, requests

vc = response["credential"]
proof_format = response.get("proofFormat", "vc-jwt")

# Construct the verify body string per format.
if proof_format == "vc-jwt":
    credential_field = vc["proof"]["jwt"]          # compact JWS string
elif proof_format == "data-integrity":
    credential_field = json.dumps(vc)              # stringified JSON envelope
elif proof_format == "sd-jwt-vc":
    credential_field = vc                          # already a compact ~-separated token
else:
    raise ValueError(f"unhandled proof format: {proof_format}")

v = requests.post(
    f"{OPENCRED_URL}/v1/credentials/verify",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={"credential": credential_field},
).json()
assert v["valid"], v
```

This catches:

- Schema drift between your `inlineContext` and the canonical `ElectricityCredential` context
- Stale or unpublished `did:web` documents (you bumped the key but forgot to upload)
- DeDi misconfiguration (verifier can't reach the registry)
- Expired `validUntil` (clock skew on the issuing host)

Bake this into your integration tests.

### Inspecting issuer-DID identities from a key file

When debugging "which DID does this key file actually produce?" (during a DSC import, a key rotation, or while wiring up your CIS glue), use the CLI inspection helper that ships with the Docker image — no server needed:

```bash
docker run --rm \
  -v "$PWD/keys/issuer-key.pem:/secrets/key.pem:ro" \
  --entrypoint node \
  ghcr.io/nfh-trust-labs/opencred/opencred-server:latest \
  apps/server/dist/cli.js identity show --key /secrets/key.pem
```

Reports the derived `did:key` (or `did:web` if `OPENCRED_ISSUER_DID_METHOD=web` and `OPENCRED_ISSUER_DOMAIN` are set), the algorithm, the source (`software-file` / `pkcs11` / `os-cert-store` / `cloud-hsm`), and whether the key carries a certificate chain. Useful for confirming the DID a key file produces before standing up the server.

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

When a consumer shares an electricity credential through DigiLocker's OAuth flow, DigiLocker returns an XML envelope. Decode `<VcContent>` (base64) into a JSON object and pass it to OpenCred — picking the right verify shape per proof format:

```python
import base64, json, requests, xml.etree.ElementTree as ET

root = ET.fromstring(digilocker_xml)
vc_b64 = root.find(".//VcContent").text
vc_json = json.loads(base64.b64decode(vc_b64))

# IES electricity credentials default to vc-jwt — send the compact JWS string,
# not the JSON envelope (see "Request shapes per proof format" above).
credential_field = vc_json["proof"]["jwt"] if "proof" in vc_json and "jwt" in vc_json["proof"] \
                   else json.dumps(vc_json)

result = requests.post(
    f"{OPENCRED_URL}/v1/credentials/verify",
    headers={"Authorization": f"Bearer {OPENCRED_API_KEY}"},
    json={"credential": credential_field},
).json()
assert result["valid"]
```

The DigiLocker HMAC proves the envelope came from DigiLocker; the OpenCred verification proves the credential inside came from you. Verifiers should check both.

---

## References

- [OpenCred — API reference (verify)](https://opencred.gitbook.io/docs/docker-image/api-reference)
- [OpenCred — Verifying credentials (Desktop)](https://opencred.gitbook.io/docs/desktop-app/verifying-credentials)
- [OpenCred — Revocation](https://opencred.gitbook.io/docs/concepts/revocation)
