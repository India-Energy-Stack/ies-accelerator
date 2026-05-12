# Core Concepts

This page explains every concept used downstream in this chapter. Read it once before deployment. You can issue your first credential after page 4 — this page just makes the field names mean something.

---

## Verifiable Credentials (VCs)

A **Verifiable Credential** is a tamper-evident JSON document that contains claims about a subject and a digital signature by the issuer. Anyone holding the document can verify the signature without contacting the issuer.

Three parties are involved in every credential's life:

| Role | Who, in DISCOM context |
|---|---|
| **Issuer** | The DISCOM signs and emits the credential |
| **Holder** | The consumer (in their DigiLocker / wallet) |
| **Verifier** | A bank, marketplace, regulator, service provider receiving the credential from the holder |

A minimum DEG-style energy credential looks like this:

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://schema.beckn.io/EnergyCredential/v2.0",
    "https://schema.beckn.io/UtilityCustomerCredential/v2.0"
  ],
  "id": "urn:uuid:8e6b5e34-1c1b-4a3c-9c20-2fa8a3b9e1c0",
  "type": ["VerifiableCredential", "EnergyCredential", "UtilityCustomerCredential"],
  "issuer": {
    "id": "did:web:ies.tpddl.in",
    "name": "Tata Power Delhi Distribution Limited",
    "licenseNumber": "DERC/DL/2025/0042"
  },
  "issuanceDate": "2026-05-01T00:00:00Z",
  "expirationDate": "2031-05-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:key:z6MkjVQ...",
    "consumerNumber": "TPDDL-2025-001234567",
    "fullName": "Priya Sharma",
    "installationAddress": {
      "fullAddress": "Flat 4B, Sector 12, Rohini, New Delhi",
      "postalCode": "110085",
      "country": "IN",
      "city": "New Delhi",
      "stateProvince": "DL"
    },
    "meterNumber": "MTR-98765432",
    "serviceConnectionDate": "2019-03-15"
  },
  "credentialStatus": {
    "id": "https://dedi.global/dedi/lookup/tpddl/vc-revocation-registry/<hash>",
    "type": "dediregistry"
  },
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "ecdsa-2019",
    "created": "2026-05-01T10:00:00Z",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:web:ies.tpddl.in#key-1",
    "proofValue": "z3FXQjecWh...kKJh6vW3"
  }
}
```

| Block | What it does |
|---|---|
| `@context` | Defines the JSON-LD vocabulary — `EnergyCredential` and any subclass (e.g. `UtilityCustomerCredential`) |
| `id` | A globally unique URI for this specific credential |
| `type` | Always `VerifiableCredential` + `EnergyCredential` + the specific DEG subclass |
| `issuer` | DID, human name, and **regulatory `licenseNumber`** (DEG mandates this) |
| `issuanceDate` / `expirationDate` | ISO 8601 timestamps |
| `credentialSubject` | The actual facts you are attesting — fields vary by credential type |
| `credentialStatus` | DeDi revocation pointer (see below) |
| `proof` | Issuer's signature |

OpenCred constructs every block above for you. You hand it the `credentialSubject` data, an `issuerDid`, a `schemaId`, and validity dates; it produces the signed credential.

---

## Decentralized Identifiers (DIDs)

A **DID** is a globally unique, cryptographically verifiable identifier that does not depend on any central registry. It looks like `did:method:identifier`.

OpenCred supports three DID methods. For DISCOMs, only two matter:

### `did:web` — recommended for DISCOMs

The DID's identifier *is* a domain you control. The corresponding public key is hosted at `https://<your-domain>/.well-known/did.json`. Example:

```
did:web:ies.tpddl.in
   ↓ resolves to
https://ies.tpddl.in/.well-known/did.json
```

**Why DISCOMs should default to this:** key rotation is just a file replace, and the trust chain terminates in your domain's TLS certificate — which is already validated by a public CA every browser trusts.

**One requirement:** you must be able to publish a single static JSON file under your domain. No backend needed.

### `did:key` — for cases where you have an existing DSC

The public key is encoded directly into the DID string. OpenCred derives it from an existing Digital Signature Certificate (PFX/PEM) at import time. Use this if your DISCOM already operates with a CCA-issued DSC and wants to anchor trust in the CSCA root chain (Type 1 issuer in OpenCred's [trust chains model](https://opencred.gitbook.io/docs/concepts/trust-chains)).

### `did:key` and `did:jwk` for consumers

The **consumer's holder DID** is generated client-side (by their wallet or by DigiLocker) and is almost always `did:key`. You receive it in the issuance request — you do not generate it.

OpenCred's `did:web` resolver enforces HTTPS-only, blocks redirects, rejects private-IP resolution targets, and times out at 10 seconds. Details: [OpenCred — DIDs](https://opencred.gitbook.io/docs/concepts/dids).

---

## Signing Keys and Trust

When OpenCred boots, it loads exactly one **signing key** from one of these sources:

| Source | Env var | When to use |
|---|---|---|
| Software file (PEM, JWK, PKCS#8, PFX) | `OPENCRED_KEY_PATH` | Dev, small DISCOMs, simplest |
| AWS KMS | `OPENCRED_KMS_PROVIDER=aws`, `OPENCRED_KMS_KEY_ARN` | Production on AWS |
| Azure Key Vault | `OPENCRED_KMS_PROVIDER=azure`, `OPENCRED_AZURE_*` | Production on Azure |
| GCP Cloud KMS | `OPENCRED_KMS_PROVIDER=gcp`, `OPENCRED_GCP_KMS_KEY_NAME` | Production on GCP |

**The key never leaves the container.** OpenCred signs in-process; in KMS modes the private key never leaves the HSM at all. There is no shared signing service and no key escrow.

Trust flows from the verifier's root store to your credential signature:

- For `did:web`: verifier resolves your DID document over HTTPS → reads the public key → checks the credential's `proof.proofValue` → trust anchors in the TLS certificate of your domain.
- For `did:key` from a DSC: verifier extracts the public key from your DID → optionally validates the x5c certificate chain back to a configured CSCA root.

---

## DeDi Revocation

Energy credentials need revocation: connections terminate, meters are replaced, programs end. DEG uses **DeDi (Decentralised Data Infrastructure)** — a public hash registry — instead of the W3C bitstring status list.

### The model

The DeDi registry stores **only the hashes of revoked credentials**. A credential is valid unless its hash appears in the registry.

The hash is deterministic:

```
revocationHash = SHA-256(JCS(credential))
```

Where `JCS` is RFC 8785 JSON Canonicalization Scheme. OpenCred computes the hash the same way at issuance time (to embed `credentialStatus.id`) and at verification time. Issuers and verifiers always compute the same value.

### Lifecycle

| Phase | What happens |
|---|---|
| **At issuance** | OpenCred computes the hash and embeds `credentialStatus`. **Nothing is published to DeDi.** |
| **At revocation** | The DISCOM calls `POST /v1/credentials/revoke`. OpenCred publishes the hash to your DeDi namespace using DISCOM-only credentials. |
| **At verification** | Verifier GETs `credentialStatus.id`. Hash found → revoked. Hash absent → valid. |

This means there is no central revocation list to maintain. Only DISCOMs with namespace credentials can publish to their own namespace.

### The `credentialStatus` block

```json
"credentialStatus": {
  "id": "https://dedi.global/dedi/lookup/<namespace>/vc-revocation-registry/<hash>",
  "type": "dediregistry"
}
```

The DEG schema mandates `type: "dediregistry"`. OpenCred currently emits `type: "dedi"` and adds two extra fields — `statusPurpose: "revocation"` and `statusListCredential: "https://dedi.global/dedi/query/<namespace>/vc-revocation-registry"`. To produce a DEG-conformant credential, your integration service must post-process the OpenCred output and rewrite `credentialStatus.type` to `"dediregistry"` before delivering the credential. The `statusPurpose` and `statusListCredential` fields are harmless for DEG verifiers and can be retained.

Details: [OpenCred — Revocation](https://opencred.gitbook.io/docs/concepts/revocation).

---

## Proof Formats

OpenCred can package the same credential in three on-the-wire formats. You pick at issuance time with `proofFormat`.

| Format | What it looks like | Use when |
|---|---|---|
| `data-integrity` | JSON-LD with embedded `proof` block | **Recommended for DEG credentials** — most human-readable and matches the DEG schema. Pass `proofFormat: "data-integrity"` explicitly on every issue call. |
| `vc-jwt` | Compact JWT (`eyJhbGciOi...`) | OpenCred's built-in default if you omit `proofFormat`. Use when integrating with JWT-native systems (some OAuth clients). |
| `sd-jwt-vc` | Selective-disclosure JWT | When holders need to prove individual claims without revealing the whole credential |

Selective disclosure is useful for energy: a consumer can prove "I have an active connection in Delhi" without revealing the exact address or meter number. To enable it, pass `selectiveDisclosureClaims: ["serviceAddress.city", "stateProvince"]` at issuance.

---

## Packaging Outputs

Beyond the raw signed JSON, OpenCred can package a credential as:

- `pdf` — printable PDF with the credential payload embedded in the info dictionary and a scannable QR
- `qr-png` / `qr-svg` — QR code carrying a compact token (`OPENCRED1:...` or JWT)
- `json` / `json-compact` — the raw signed credential

Request these via the `packageFormats` array on the issue endpoint. The PDF carries the whole credential inside the file, so a verifier can drop the PDF into the OpenCred Verify tab and skip the QR scan entirely.

---

## Credential Lifecycle

```
Request → Issue → Hold → Present → Verify
                          │
                          └──> Revoke (issuer-initiated)
```

| Phase | Actor | What happens |
|---|---|---|
| **Request** | Consumer or DigiLocker | Triggers issuance by consumer-number lookup |
| **Issue** | DISCOM | OpenCred signs and packages the credential |
| **Hold** | Consumer | Credential lives in DigiLocker or a DID wallet |
| **Present** | Consumer | Shares the credential (or selective disclosures) with a verifier |
| **Verify** | Verifier | Checks signature, validity dates, revocation, schema |
| **Revoke** | DISCOM | Publishes the hash to DeDi; all future verifications fail |

---

## Next

You now know what a credential is, who signs it, how trust flows, and how revocation works. [Schemas](./schemas.md) shows the five DEG energy credential types and their fields. Then [Deployment](./onboarding.md) walks you through standing up OpenCred.

---

## References

- [OpenCred — Concepts overview](https://opencred.gitbook.io/docs/concepts/concepts)
- [OpenCred — Verifiable Credentials](https://opencred.gitbook.io/docs/concepts/verifiable-credentials)
- [OpenCred — DIDs](https://opencred.gitbook.io/docs/concepts/dids)
- [OpenCred — Trust chains](https://opencred.gitbook.io/docs/concepts/trust-chains)
- [OpenCred — Revocation](https://opencred.gitbook.io/docs/concepts/revocation)
- [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/)
- [RFC 8785 JSON Canonicalization Scheme](https://datatracker.ietf.org/doc/html/rfc8785)
