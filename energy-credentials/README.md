# Energy Credentials for DISCOMs

This chapter is a complete, self-contained guide for a DISCOM tech team to start **issuing energy credentials to consumers**. It walks from first principles through running the credential service, signing your first credential, and delivering it to consumers via DigiLocker or directly.

You do not need any prior knowledge of Verifiable Credentials. Every concept used downstream is explained in [Core Concepts](./concepts.md).

---

## What an Energy Credential Is

An **Energy Credential** is a cryptographically signed digital attestation that a DISCOM makes about one of its consumers or one of their energy assets. It follows the [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/) and the [Beckn DEG `EnergyCredential` schema family](https://github.com/beckn/DEG/tree/main/specification/schema/EnergyCredential).

A credential is a JSON document with three things inside it:

1. **An issuer block** — your DISCOM's DID and regulatory licence number, so any verifier can prove the credential came from you.
2. **A credentialSubject block** — the consumer's DID and the specific facts you are attesting to (consumer number, sanctioned load, generation capacity, etc.).
3. **A proof block** — an Ed25519 / ECDSA signature over the credential body, produced by your DISCOM's private key.

Because the signature is over the canonicalised credential bytes, anyone holding the credential can independently verify it: no callback to the DISCOM, no shared database, no central registry lookup. Revocation is the only thing that needs a fresh check, and even that runs against a public hash registry rather than a DISCOM API.

---

## What You Can Issue

The DEG `EnergyCredential` family defines five concrete credential types. All five share the same envelope (issuer with licence number, validity dates, revocation status, proof). They differ only in the `credentialSubject` fields.

| Credential type | What it attests | When to issue |
|---|---|---|
| **`UtilityCustomerCredential`** | Customer identity — consumer number, name, installation address, meter number, service connection date | At new connection; the foundational credential every consumer should have |
| **`ConsumptionProfileCredential`** | Premises type, connection type, sanctioned load, tariff category | Alongside the customer credential; needed for tariff and DR programs |
| **`GenerationProfileCredential`** | DER asset — generation type (Solar/Wind/MicroHydro), installed capacity, commissioning date | When a rooftop solar / DER is commissioned; required for net metering and P2P |
| **`StorageProfileCredential`** | Battery storage — capacity (kWh), power rating (kW), storage technology | When a behind-the-meter battery is commissioned |
| **`ProgramEnrollmentCredential`** | Enrolment in a specific energy program (P2P, ToU tariff, DR, VPP) | When the consumer opts into a program; expires with the enrolment |

Full schema details, JSON examples, and field-level requirements for each type are in [Schemas](./schemas.md).

---

## The DISCOM Issuance Flow

```
   Consumer system            DISCOM service             Consumer wallet
  (CIS, NMS, MDM)        (OpenCred + your integration)  (DigiLocker / DID)
        │                          │                            │
        │  consumer/asset data     │                            │
        │ ───────────────────────> │                            │
        │                          │ 1. Build credentialSubject │
        │                          │ 2. POST /v1/credentials/   │
        │                          │       issue (OpenCred)     │
        │                          │ 3. OpenCred signs locally  │
        │                          │    using your private key  │
        │                          │ 4. Package as JSON+PDF+QR  │
        │                          │ ─────────────────────────> │
        │                          │                            │
        │                          │       revocation (later)   │
        │                          │ POST /v1/credentials/      │
        │                          │       revoke               │
```

You run **two pieces of software**:

1. **OpenCred server** — an open-source Docker image (`ghcr.io/nfh-trust-labs/opencred/opencred-server`) that holds your signing key and exposes an HTTP API for `issue`, `verify`, `revoke`, etc. Your private key never leaves this container.
2. **A thin integration service you write** — pulls consumer or asset facts from your CIS / NMS, calls OpenCred's `issue` endpoint, and delivers the result to the consumer (DigiLocker Pull URI, email, app push, or DID-to-DID).

The "thin integration service" is the only custom code on your side. OpenCred handles every cryptographic operation, packaging, and DID resolution.

---

## What You Will Need

Before you start, gather:

- A Linux host (any cloud or on-prem) that can run a Docker container with outbound HTTPS
- A signing key — either an existing Digital Signature Certificate (PFX/PEM), a hardware token / HSM, or an ECDSA P-256 key OpenCred generates for you
- A domain you control if you want `did:web` (recommended for production), e.g. `ies.tpddl.in`
- Read access to your CIS / billing / meter database for consumer lookups
- (For DigiLocker delivery) an issuer account on [API Setu](https://apisetu.gov.in)
- (For DeDi revocation) a DeDi namespace from [dedi.global](https://dedi.global)

That is the entire prerequisite list. No PKI vendor contracts, no central IES gateway to integrate with.

---

## Recommended Reading Order

Follow these pages in sequence. Each one builds on the last.

| # | Page | What you learn |
|---|---|---|
| 1 | [Core Concepts](./concepts.md) | W3C VCs, DIDs, signing keys, trust chains, DeDi revocation. Read once, refer back as needed. |
| 2 | [Schemas](./schemas.md) | The five DEG `EnergyCredential` types, their fields, validation rules, and worked JSON examples. |
| 3 | [Deployment](./onboarding.md) | Stand up OpenCred on your infrastructure: Docker, environment variables, KMS, health checks. |
| 4 | [Issuing Credentials](./issuance.md) | Call `POST /v1/credentials/issue` with real DEG payloads; revoke when needed; batch operations. |
| 5 | [DigiLocker Integration](./digilocker-integration.md) | Build the Pull URI endpoint that lets consumers find your credential in DigiLocker. |
| 6 | [Verification](./verification.md) | How a counterparty (bank, marketplace, regulator) verifies a credential you've issued. Use this when onboarding verifier partners. |

By the end of page 5 you will have signed real credentials and delivered them to a consumer wallet.

---

## How OpenCred Fits In

[OpenCred](https://opencred.gitbook.io/docs) is the open-source W3C VC platform that powers IES Energy Credentials. The full reference docs live on the OpenCred GitBook; this chapter cites them at every step but you do not need to read them end-to-end.

Important properties of OpenCred that matter for DISCOMs:

- **Local-first signing** — issuer private keys never leave the container you run. There is no shared cloud signing service.
- **Stateless server** — restart at will; no database to back up. Revocation state lives in DeDi.
- **Standard W3C VC outputs** — every credential is interoperable with any W3C VC verifier; you are not locked into IES tooling.
- **Multiple proof formats** — `data-integrity` (JSON-LD, default), `vc-jwt`, and `sd-jwt-vc` for selective disclosure.
- **DeDi-based revocation** — hash-based, network-light, and the same registry the rest of the IES stack uses.

---

## References

- [OpenCred documentation (GitBook)](https://opencred.gitbook.io/docs) — comprehensive reference for the credential service
- [OpenCred API reference](https://opencred.gitbook.io/docs/docker-image/api-reference) — every HTTP endpoint with request/response schemas
- [Beckn DEG `EnergyCredential` schemas](https://github.com/beckn/DEG/tree/main/specification/schema/EnergyCredential) — source of truth for credential field definitions
- [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/)
- [W3C Decentralized Identifiers](https://www.w3.org/TR/did-core/)
- [DeDi — Decentralised Data Infrastructure](https://dedi.global)
