# Energy Credentials for DISCOMs

This chapter is a complete, self-contained guide for a DISCOM tech team to start **issuing electricity credentials to consumers**. It walks from first principles through running the credential service, signing your first credential, and delivering it to consumers via DigiLocker or directly.

You do not need any prior knowledge of Verifiable Credentials. Every concept used downstream is explained in [Core Concepts](./concepts.md).

---

## What an Electricity Credential Is

An **Electricity Credential** is a cryptographically signed digital attestation a DISCOM makes about a consumer's meter and the assets behind it. It follows the [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) and the IES `ElectricityCredential` schema family — mirrored from Beckn DEG into this repo under [`/schemas/ElectricityCredential/v1.0/`](/schemas/ElectricityCredential/v1.0/).

A credential is a JSON document with three things inside it:

1. **An issuer block** — your DISCOM's DID, legal name, and an `idRef` pointing at your regulatory registration, so any verifier can prove the credential came from you.
2. **A credentialSubject block** — the consumer's DID and the specific facts you are attesting (customer profile, address, consumption, generation assets, storage assets).
3. **A proof block** — an Ed25519 / ECDSA signature over the credential body, produced by your DISCOM's private key.

Because the signature is over the canonicalised credential bytes, anyone holding the credential can independently verify it: no callback to the DISCOM, no shared database, no central registry lookup. Revocation is the only thing that needs a fresh check, and even that runs against a public hash registry rather than a DISCOM API.

---

## What You Can Issue

The IES Electricity Credential family currently spans three credential types — all issued by the DISCOM, all signed by the same OpenCred service, all verified the same way:

| Credential | Purpose | Issued |
|---|---|---|
| [`CustomerCredential`](./schemas.md) | DISCOM-side attestation about a meter and its assets | Once at onboarding; re-issued on material change |
| [`ConsumerEnergyPassport`](./consumer-energy-passport.md) (draft) | Wallet-shareable composite credential binding consumer identity to connection, meter, sanctioned load, and DER/storage assets — for presentation to banks, marketplaces, regulators, societies | Once at onboarding; re-issued on material change |
| [`ConsumerMeterDigest`](./consumer-meter-digest.md) (draft) | On-demand snapshot of the consumer's meter readings (raw or summary) the consumer holds in their wallet and shares with any third party | On consumer demand, freshly each time, with a short `validUntil` |

The use-case framing for the two consumer-facing credentials lives under [Use Cases → Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md) and [Use Cases → Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md).

The rest of this chapter is written from the DISCOM-as-issuer perspective and uses `CustomerCredential` as the running example. The two consumer-facing credentials reuse the same envelope, the same OpenCred deployment, and the same DigiLocker delivery path — only the schema and the trigger differ.

### `CustomerCredential` sub-profiles

You issue **one `CustomerCredential` per meter**. That single credential carries five equal-level sub-profiles inside its `credentialSubject` — only `customerProfile` is required; the others appear when the relevant facts exist for that meter:

| Sub-profile | What it attests | Required? |
|---|---|---|
| `customerProfile` | Customer number, meter number, meter type, optional `idRef` to a government ID | ✓ Always |
| `customerDetails` | Full name, installation address, service connection date | Whenever you have it |
| `consumptionProfiles[]` | Premises type, connection type, sanctioned load, tariff category — one entry per meter / tariff category | When applicable |
| `generationProfiles[]` | DER assets — generation type (Solar / Wind / MicroHydro), capacity, commissioning date — one entry per asset | When DERs are commissioned |
| `storageProfiles[]` | Battery storage — capacity (kWh), power rating (kW), storage technology — one entry per battery | When batteries are commissioned |

When facts change (new tariff, new DER, decommissioning), you **re-issue and revoke the previous credential** — see [Issuance lifecycle patterns](./issuance.md#lifecycle-patterns). Field-level requirements and worked JSON examples are in [Schemas](./schemas.md).

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
2. **A thin integration service you write** — pulls consumer or asset facts from your CIS / NMS, calls OpenCred's `issue` endpoint, injects the full `issuer` object (name + `idRef`), and delivers the result to the consumer (DigiLocker Pull URI, email, app push, or DID-to-DID).

The "thin integration service" is the only custom code on your side. OpenCred handles every cryptographic operation, packaging, and DID resolution.

---

## What You Will Need

Before you start, gather:

- A Linux host (any cloud or on-prem) that can run a Docker container with outbound HTTPS — **or Docker Desktop on Windows / macOS** for dev evaluation
- A signing key — either an ECDSA P-256 PEM you generate (recommended for dev / first deploy), an existing Digital Signature Certificate (PFX/PEM), or an HSM / cloud KMS key for production
- (For production) a domain you control for `did:web`, e.g. `ies.tpddl.in`
- Read access to your CIS / billing / meter database for consumer lookups
- (For DigiLocker delivery) an issuer account on [API Setu](https://apisetu.gov.in)
- (For revocation) a DeDi namespace from [dedi.global](https://dedi.global)

That is the entire prerequisite list. No PKI vendor contracts, no central IES gateway to integrate with.

---

## Recommended Reading Order

Follow these pages in sequence. Each one builds on the last.

| # | Page | What you learn |
|---|---|---|
| 1 | [Core Concepts](./concepts.md) | W3C VCs, DIDs, signing keys, trust chains, DeDi revocation. Read once, refer back as needed. |
| 2 | [Schemas](./schemas.md) | The unified `CustomerCredential`, its five sub-profiles, validation rules, and worked JSON example. |
| 3 | [Deployment](./onboarding.md) | Stand up OpenCred on your infrastructure: Docker, environment variables, KMS, health checks. |
| 4 | [Issuing Credentials](./issuance.md) | Call `POST /v1/credentials/issue` with validated payloads; revoke and re-issue when facts change; batch operations. |
| 5 | [DigiLocker Integration](./digilocker-integration.md) | Build the Pull URI endpoint that lets consumers find your credential in DigiLocker. |
| 6 | [Verification](./verification.md) | How a counterparty (bank, marketplace, regulator) verifies a credential you've issued. Use this when onboarding verifier partners. |

By the end of page 5 you will have signed real credentials and delivered them to a consumer wallet.

---

## How OpenCred Fits In

[OpenCred](https://opencred.gitbook.io/docs) is the open-source W3C VC platform that powers IES Electricity Credentials. The full reference docs live on the OpenCred GitBook; this chapter cites them at every step but you do not need to read them end-to-end.

Important properties of OpenCred that matter for DISCOMs:

- **Local-first signing** — issuer private keys never leave the container you run. There is no shared cloud signing service.
- **Stateless server** — restart at will; no database to back up. Revocation state lives in DeDi.
- **Standard W3C VC outputs** — every credential is interoperable with any W3C VC verifier; you are not locked into IES tooling.
- **Multiple proof formats** — `vc-jwt` (recommended for the bundled `electricity/v1` schema), `data-integrity` (JSON-LD), and `sd-jwt-vc` for selective disclosure.
- **DeDi-based revocation** — hash-based, network-light, and the same registry the rest of the IES stack uses.

---

## References

- [OpenCred documentation (GitBook)](https://opencred.gitbook.io/docs) — comprehensive reference for the credential service
- [OpenCred API reference](https://opencred.gitbook.io/docs/docker-image/api-reference) — every HTTP endpoint with request/response schemas
- IES `ElectricityCredential` schemas — canonical field definitions at [`/schemas/ElectricityCredential/v1.0/`](/schemas/ElectricityCredential/v1.0/) (repo root: [`India-Energy-Stack/ies-accelerator`](https://github.com/India-Energy-Stack/ies-accelerator))
- [Beckn DEG `ElectricityCredential` (upstream)](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential)
- [W3C Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [W3C Decentralized Identifiers](https://www.w3.org/TR/did-core/)
- [DeDi — Decentralised Data Infrastructure](https://dedi.global)
