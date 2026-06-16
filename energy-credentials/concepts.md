# Core Concepts

This page explains every concept used downstream in this chapter. Read it once before deployment. You can issue your first credential after page 4 — this page just makes the field names mean something.

---

## Verifiable Credentials (VCs)

A **Verifiable Credential** is a JSON document containing claims about a subject, with a digital signature by the issuer attached. Three properties make it useful:

- **Tamper-evident** — modify the contents after the issuer signs them, and the signature stops verifying. Anyone receiving the credential can detect tampering.
- **Offline-verifiable** — any verifier checks the **signature** using the issuer's published public key. No callback to the issuer, no shared database. (Revocation status is a separate check — see [DeDi Revocation](#dedi-revocation).)
- **Self-contained trust** — the credential carries everything needed to prove who issued it, when, and that the contents haven't changed.

Three parties are involved in every credential's life:

| Role | Who, in DISCOM context |
|---|---|
| **Issuer** | The DISCOM signs and emits the credential |
| **Holder** | The consumer (in their DigiLocker / wallet) |
| **Verifier** | A bank, marketplace, regulator, service provider receiving the credential from the holder |

A minimum IES electricity credential (`type: "CustomerCredential"`) looks like this:

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.0/context.jsonld"
  ],
  "id": "urn:uuid:8e6b5e34-1c1b-4a3c-9c20-2fa8a3b9e1c0",
  "type": ["VerifiableCredential", "CustomerCredential"],
  "issuer": {
    "id": "did:web:ies.tpddl.in",
    "name": "Tata Power Delhi Distribution Limited",
    "idRef": {
      "issuedBy": "did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma",
      "subjectId": "india-energy-stack:tpddl"
    }
  },
  "validFrom":  "2026-05-01T00:00:00+05:30",
  "validUntil": "2031-05-01T00:00:00+05:30",
  "credentialSubject": {
    "id": "did:key:z6MkjVQ...",
    "customerProfile": {
      "customerNumber": "TPDDL-2025-001234567",
      "meterNumber":    "MTR-98765432",
      "meterType":      "AMI"
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
    }
  },
  "credentialStatus": {
    "id": "https://dedi.global/dedi/lookup/tpddl/vc-revocation-registry/<credential-id>",
    "type": "dedi",
    "statusPurpose": "revocation",
    "statusListCredential": "https://dedi.global/dedi/query/tpddl/vc-revocation-registry"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-05-01T10:00:00+05:30",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:web:ies.tpddl.in#key-1",
    "proofValue": "z3FXQjecWh...kKJh6vW3"
  }
}
```

| Block | What it does |
|---|---|
| `@context` | Defines the JSON-LD vocabulary. Must contain `https://www.w3.org/ns/credentials/v2`. |
| `id` | A globally unique URN UUID for this specific credential |
| `type` | Always `"VerifiableCredential"` + `"CustomerCredential"` |
| `issuer` | DID, legal name, and `idRef` pointing at the DISCOM's entry in the **IES DISCOMs Reference Registry** (see [Trust and the IES Reference Registry](#trust-and-the-ies-reference-registry)) |
| `validFrom` / `validUntil` | ISO 8601 timestamps with timezone offset |
| `credentialSubject` | The actual facts you are attesting — see [Schemas](./schemas.md) for the sub-profile structure |
| `credentialStatus` | DeDi revocation pointer (see below) |
| `proof` | Issuer's signature |

OpenCred constructs every block above for you. You hand it the `credentialSubject` data, an `issuerDid`, a `schemaId`, and validity dates; it produces the signed credential. (Your integration service then injects the full `issuer.name` and `issuer.idRef` before delivery — see [Issuance](./issuance.md).)

---

## Decentralized Identifiers (DIDs)

A **DID** is a globally unique identifier of the form `did:method:identifier` that does not depend on any central authority. **Cryptographically verifiable** means: the identifier itself can be turned into a public key (directly, or via a registry-anchored lookup) — so anyone receiving a signature made by the DID's holder can check it without having to trust an issuing authority's database.

OpenCred supports three DID methods. For DISCOMs, all three are useful at different points:

### `did:key` from a self-generated software key — recommended for dev / first deploy

The public key is encoded directly into the DID string. Generate an ECDSA P-256 PEM with `openssl`; OpenCred derives the `did:key` automatically on startup. No domain, no certificate, no cost — and the same DID is reproducible from the same PEM, so it survives container restarts. Read it back from `GET /v1/keys`.

This is the fastest way to evaluate the system end-to-end before provisioning production infrastructure.

### `did:web` — recommended for production

The DID's identifier *is* a domain you control. The corresponding public key is hosted at `https://<your-domain>/.well-known/did.json`. Example:

```
did:web:ies.tpddl.in
   ↓ resolves to
https://ies.tpddl.in/.well-known/did.json
```

**Why DISCOMs should default to this in production:** key rotation is just a file replace, and the trust chain terminates in your domain's TLS certificate — which is already validated by a public CA every browser trusts.

**One requirement:** you must be able to publish a single static JSON file under your domain. No backend needed.

### `did:key` from an existing DSC

For DISCOMs that already operate with a CCA-issued **Digital Signature Certificate** (Class-2 / Class-3, issued by eMudhra, Sify, NSDL, Capricorn, etc.) and want to anchor trust in the CSCA root chain. Mount the PFX/PEM; OpenCred derives the `did:key` from the certificate's public key (Type 1 issuer in OpenCred's [trust chains model](https://opencred.gitbook.io/docs/concepts/trust-chains)).

### `did:key` and `did:jwk` for consumers

The **consumer's holder DID** is generated client-side (by their wallet or by DigiLocker) and is almost always `did:key`. You receive it in the issuance request — you do not generate it.

OpenCred's `did:web` resolver enforces HTTPS-only, blocks redirects, rejects private-IP resolution targets, and times out at 10 seconds. Details: [OpenCred — DIDs](https://opencred.gitbook.io/docs/concepts/dids).

### DeDi as a `did:web` discovery fallback

Since **OpenCred v1.4.0**, an issuer that publishes its DID document to DeDi can let verifiers resolve it through DeDi when the canonical `https://<domain>/.well-known/did.json` is unreachable. Two equivalent ways to publish:

- **Manually** — `POST /v1/keys/publish` with the constructed DID document. Returns `{published: true, recordName, namespace}`.
- **Automatically at boot** — set `OPENCRED_DEDI_HOST_DID_DOC=true` on the container; OpenCred publishes its own DID document to the DeDi `public_key_registry` during startup. Ignored when `OPENCRED_ISSUER_DID_METHOD=key` (a `did:key` already encodes its public key directly in the DID string).

When a verifier walks `did:web:<your-domain>`:

1. The composite DID resolver tries `https://<your-domain>/.well-known/did.json` first.
2. If that fails (network error, 404, redirect, etc.) **and** the verifier has DeDi configured (`OPENCRED_DEDI_*` set), OpenCred falls back to looking the DID up in the DeDi `public_key_registry`.
3. The resolved DID document is the same shape in either path; the credential's `proof.verificationMethod` validates against the public key from whichever path succeeded.

A `did:web` issuer who has both posted `.well-known/did.json` *and* published to DeDi gets the most robust setup — the canonical HTTPS endpoint stays the primary path, and DeDi covers transient outages. An issuer who never serves a `.well-known/did.json` and relies entirely on DeDi works too, but only against verifiers that themselves have OpenCred-style DeDi awareness wired in.

### `keyStatus` rotation flag and the CORD anchor proof

When OpenCred resolves a DID document through DeDi (either as the primary path or as the `did:web` fallback above), the response carries two extra fields beyond the canonical DID document:

- **`keyStatus`** — `"current"` for a freshly-published record; flips to `"rotated"` after the issuer's auto-rotation hook runs (e.g. when a new signing key is generated). The flag is monotone (`current → rotated`, never back) and **advisory only**: a credential signed under a rotated key remains cryptographically valid because the signature is verified against the key in use at signing time. Verifier UIs typically surface a "key rotated since signing" badge — this is the `keyRotation` advisory check on the verify response. See [Verification → keyRotation](./verification.md#keyrotation-advisory).
- **`proof`** (when present) — a `DediRecordProof2026` block attesting that the DID record was anchored on the [CORD blockchain](https://cord.network/) by a named `creator_did`. This is **supplementary provenance**, not VC-signature verification: it tells the verifier "DeDi reports this DID record was anchored on CORD by *this* party". The verifier's `registryAnchor` advisory check surfaces a badge when the `creator_did` matches the credential's issuer DID, and a suspicion badge when it does not. Absence of a proof is benign on DeDi instances that don't anchor; the check degrades open.

Both fields are observational — neither failing flips the headline `valid` boolean. They exist so end-user verifier UIs can surface trust-relevant context that lives outside the cryptographic signature.

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

---

## Trust and the IES Reference Registry

A cryptographically valid signature is not enough on its own — it proves the credential was signed by *whoever holds that DID's private key*, but a verifier still needs to answer: **"is that DID a trusted DISCOM?"** On the IES network, the answer comes from the **IES DISCOMs Reference Registry**.

### The registry

The registry is hosted on [`dedi.global`](https://dedi.global). Its full base URL is:

```
https://api.dedi.global/dedi/lookup/did%3Aweb%3Adid.cord.network%3A76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma/
```

Throughout these docs we refer to a DISCOM's entry by its **relative path** `india-energy-stack/ies-discoms-reference-registry/<discom-id>`; prepend the base URL above to resolve.

| Property | Value |
|---|---|
| Host | `api.dedi.global` |
| Namespace (friendly) | `india-energy-stack` |
| Namespace DID | `did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma` |
| Registry | `ies-discoms-reference-registry` |
| Relative path | `india-energy-stack/ies-discoms-reference-registry/<discom-id>` |

Each registry entry holds, at a minimum: the DISCOM's issuer DID, its legal name, and its **published public key(s)**. Registry entries are managed by the IES network operator; DISCOMs cannot self-publish.

### The trust flow

When a verifier checks a credential issued on the IES network:

1. Parse the credential and read `issuer.idRef.subjectId` (e.g. `india-energy-stack:tpddl`)
2. Resolve the registry entry at `india-energy-stack/ies-discoms-reference-registry/tpddl` (i.e. the full URL formed by prepending the base above)
3. Confirm `issuer.id` in the credential matches the DID recorded in the registry entry
4. Read the public key from the registry entry
5. Verify the credential's `proof` against that public key

If any of steps 2–4 fails, the credential is **not trusted**, even if step 5 would have succeeded. This is what makes the registry the trust anchor: a forged credential signed with an unregistered key has no path to acceptance.

### Why this is better than relying on `did:web` alone

A pure `did:web` model anchors trust in the issuer's own TLS certificate. That works for organisations a verifier already knows out-of-band, but it does not answer "is this DISCOM real?" — anyone can stand up `did:web:not-a-real-discom.example` and self-attest.

The IES Reference Registry is the network's curated list of who counts as a DISCOM. A DISCOM still publishes its public key via `did:web` (so key rotation remains simple and self-service), but **registration in the IES registry is the act that makes that key trustworthy on this network**.

### Other DID methods still work for signing

The registry is the trust authority, but the underlying signing key can come from any of OpenCred's supported sources:

- **`did:web`** is the most common production setup — the registry entry references your `did:web:<your-domain>` and the public key resolves from your `.well-known/did.json`.
- **`did:key` from a self-generated PEM** — useful for dev and for early-stage DISCOMs. The registry entry references the `did:key:...` directly.
- **`did:key` from a DSC** — for DISCOMs anchoring trust additionally in the CSCA chain (Type 1 issuer in OpenCred's [trust chains model](https://opencred.gitbook.io/docs/concepts/trust-chains)). The registry entry can carry the certificate's `x5c` chain alongside the bare public key.

In every case, the verifier reaches the public key via the registry entry, not by trusting the DISCOM's domain or certificate authority on its own.

---

## DeDi Revocation

Electricity credentials need revocation: connections terminate, meters are replaced, assets are decommissioned. Revocation uses **DeDi (Decentralised Data Infrastructure)** — a public hash registry defined by Beckn DEG — instead of the W3C bitstring status list.

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
| **At revocation** | The DISCOM calls `POST /v1/credentials/revoke` with the hash and an optional `reason` (free-text descriptor; typical values are short tags like `"key-compromised"`, `"superseded"`, `"holder-request"`). OpenCred publishes the hash to your DeDi namespace using DISCOM-only credentials. DeDi stores the reason alongside the hash and `/v1/credentials/revocation-status` echoes it verbatim. |
| **At verification** | Verifier GETs `credentialStatus.id`. Hash found → revoked. Hash absent → valid. |

This means there is no central revocation list to maintain. Only DISCOMs with namespace credentials can publish to their own namespace.

> **Silent-skip warning.** If a verifier does **not** have DeDi configured, it cannot query the revocation registry and **skips the revocation check entirely** — a revoked credential will verify as `VALID` because the signature is intact and the date window is open. The response shows two checks (`signature`, `date`) instead of three (`signature`, `date`, `revocation`). IES verifier partners (banks, marketplaces, regulators) must configure DeDi or accept that their tamper-evidence guarantee leaks for the revocation case. The verifier-side guidance for this lives in [Verification → silent-skip](./verification.md#silent-skip-warning).

### The `credentialStatus` block

```json
"credentialStatus": {
  "id": "https://dedi.global/dedi/lookup/<namespace>/vc-revocation-registry/<credential-id>",
  "type": "dedi",
  "statusPurpose": "revocation",
  "statusListCredential": "https://dedi.global/dedi/query/<namespace>/vc-revocation-registry"
}
```

All four fields are required by the schema. OpenCred fills them automatically when you pass `revocationRegistryUrl` on the issue call.

Details: [OpenCred — Revocation](https://opencred.gitbook.io/docs/concepts/revocation).

---

## Proof Formats

OpenCred can package the same credential in three on-the-wire formats. You pick at issuance time with `proofFormat`.

| Format | What it looks like | Use when |
|---|---|---|
| `vc-jwt` | JSON-LD VC envelope with the compact JWS in `proof.jwt` | **Recommended default.** Matches OpenCred's bootcamp default (PR #599) and works for every bundled schema including `electricity/v1`. The credential is a normal JSON-LD object on disk; the cryptographic signature is the compact JWS string inside `proof.jwt`. |
| `data-integrity` | JSON-LD with an embedded `proof` block | Most human-readable. Use against schemas you register yourself with a clean context. **Do not use against the bundled `electricity/v1` context** — the protected-term collision returns `CRYPTO_ERROR: Invalid JSON-LD syntax; tried to redefine a protected term` (tracked as OpenCred [#596](https://github.com/nfh-trust-labs/opencred/issues/596)). |
| `sd-jwt-vc` | Compact `~`-separated selective-disclosure JWT | When holders need to prove individual claims without revealing the whole credential |

> **Verifier-side gotcha for `vc-jwt`.** When you POST a `vc-jwt` credential to `/v1/credentials/verify`, the request body's `credential` field must be the **compact JWS string** (the `.proof.jwt` value), **not** the stringified JSON-LD envelope. Sending the stringified envelope silently fails the signature check. Worked example in [Issuance → Verify immediately after issue](./issuance.md#verify-immediately-after-issue) and [Verification → request shapes per proof format](./verification.md#request-shapes-per-proof-format).

Selective disclosure is useful for energy: a consumer can prove "I have an active connection in Delhi" without revealing the exact address or meter number. To enable it, pass `selectiveDisclosureClaims: ["customerDetails.installationAddress.city", "customerDetails.installationAddress.state"]` at issuance.

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

You now know what a credential is, who signs it, how trust flows, and how revocation works. [Schemas](./schemas.md) shows the unified `CustomerCredential` and its five sub-profiles. Then [Deployment](./onboarding.md) walks you through standing up OpenCred.

---

## Glossary

Cryptographic and PKI terms used in this chapter:

| Term | Meaning |
|---|---|
| **ECDSA** | Elliptic Curve Digital Signature Algorithm — the asymmetric signature scheme used for `proof` |
| **P-256** | NIST elliptic curve (`prime256v1`), the standard curve for W3C VCs |
| **Ed25519** | Alternative signature scheme; supported but not the IES default |
| **SHA-256** | Cryptographic hash function used in the revocation hash |
| **JCS** | RFC 8785 JSON Canonicalization Scheme — deterministic JSON serialization, used to make hashes reproducible |
| **JWK** | JSON Web Key — public/private key encoded as JSON |
| **PKCS#8** | Standard binary encoding for private keys |
| **PFX** | PKCS#12 archive — usually a private key plus an X.509 certificate chain |
| **PEM** | Base64-armoured wrapper around PKCS#8 / X.509 |
| **JSON-LD** | JSON for Linked Data — JSON with a `@context` for semantic interoperability |
| **vc-jwt** | Verifiable Credential serialized as a compact JWT |
| **sd-jwt-vc** | Selective Disclosure JWT for VCs — holder reveals individual claims |
| **x5c** | "X.509 certificate chain" — a JWS/JWK header carrying the cert chain |
| **DID** | Decentralised Identifier (`did:method:value`) |
| **VC** | Verifiable Credential |
| **DSC** | Digital Signature Certificate — Class-2/Class-3 X.509 cert issued by a **CCA**-licensed CA in India |
| **CCA** | Controller of Certifying Authorities — the Indian government body that licences DSC-issuing CAs |
| **CSCA** | Country Signing Certificate Authority — the root in a national PKI |
| **HSM** | Hardware Security Module — tamper-resistant device that holds keys; cloud KMS is the managed equivalent |
| **DeDi** | Decentralised Data Infrastructure — the hash registry used for revocation |
| **SERC** | State Electricity Regulatory Commission — issues the utility's regulatory licence (the `issuer.idRef` value) |

---

## References

- [OpenCred — Concepts overview](https://opencred.gitbook.io/docs/concepts/concepts)
- [OpenCred — Verifiable Credentials](https://opencred.gitbook.io/docs/concepts/verifiable-credentials)
- [OpenCred — DIDs](https://opencred.gitbook.io/docs/concepts/dids)
- [OpenCred — Trust chains](https://opencred.gitbook.io/docs/concepts/trust-chains)
- [OpenCred — Revocation](https://opencred.gitbook.io/docs/concepts/revocation)
- [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [RFC 8785 JSON Canonicalization Scheme](https://datatracker.ietf.org/doc/html/rfc8785)
