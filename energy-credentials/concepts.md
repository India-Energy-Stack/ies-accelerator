# Core Concepts — Energy Credentials

This page explains the foundational standards and terminology you need to understand before integrating with IES Energy Credentials.

---

## W3C Verifiable Credentials

A **Verifiable Credential (VC)** is a tamper-evident digital document that contains claims about a subject. It is structurally similar to a physical credential (a driving licence, a utility bill) but has one critical advantage: the issuer's digital signature can be verified by anyone, without calling back to the issuer.

The IES Credential Service implements the [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/), which is the same standard used by [OpenCred](https://opencred.gitbook.io/docs) and is globally interoperable.

### Credential Structure

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://ies.energy/credentials/v1"
  ],
  "id": "https://ies.energy/credentials/nycer-TPDDL-001234567",
  "type": ["VerifiableCredential", "ElectricityConnectionCredential"],
  "issuer": {
    "id": "did:ies:discom-tpddl",
    "name": "Tata Power Delhi Distribution Limited"
  },
  "issuanceDate": "2026-04-01T00:00:00Z",
  "expirationDate": "2027-04-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:ies:consumer-7a3f9b2c",
    "fullName": "Priya Sharma",
    "consumerNumber": "TPDDL-2025-001234567",
    "serviceAddress": "Flat 4B, Sector 12, Rohini, New Delhi – 110085",
    "serviceConnectionDate": "2019-03-15",
    "meterNumber": "MTR-98765432"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-04-01T10:00:00Z",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:ies:discom-tpddl#key-1",
    "proofValue": "z3FXQjecWh...signature...kKJh6vW3"
  }
}
```

| Field | Description |
|---|---|
| `@context` | JSON-LD context — declares the vocabulary for all fields |
| `id` | Globally unique identifier for this credential |
| `type` | Credential type(s) — must include `VerifiableCredential` |
| `issuer` | DID + human-readable name of the issuing organisation |
| `issuanceDate` | When the credential was issued |
| `expirationDate` | When it expires (optional) |
| `credentialSubject` | The claims being made — consumer details, asset attributes, etc. |
| `proof` | Cryptographic signature by the issuer |

---

## Decentralized Identifiers (DIDs)

A **DID** is a globally unique, cryptographically verifiable identifier that does not depend on a central registry. It looks like:

```
did:ies:discom-tpddl
did:ies:consumer-7a3f9b2c
did:ies:asset-solar-panel-kr-001
```

Each DID resolves to a **DID Document** that contains public keys and service endpoints. The IES Credential Service manages DID creation and resolution for registered organisations.

DIDs serve three purposes in the VC system:
1. **Issuer DID** — identifies the organisation signing the credential
2. **Subject DID** — identifies the entity the credential is about
3. **Holder DID** — identifies who controls and presents the credential (may differ from subject)

---

## Energy Resource Addresses (ERAs)

An **Energy Resource Address** is the IES-specific identifier for a physical or logical energy asset — a meter, a solar installation, an EV charger, a DISCOM service area. ERAs follow a structured naming convention similar to internet domain names:

```
household-solar-001.greenenergy.tpddl.in
IN*ECO*BTM*01*CCS2*A          (EVSE OCPI format)
meter-KA-98765432.amisp.bescom.in
```

Credentials issued about energy assets bind to the asset's ERA, not a person's identity. This allows a rooftop solar installation to carry its own trust record — green certification, grid approval, safety compliance — independently of who owns it.

---

## Verifiable Presentations

When a Holder wants to share credential claims with a Verifier, they create a **Verifiable Presentation (VP)**:

```json
{
  "@context": ["https://www.w3.org/2018/credentials/v1"],
  "type": "VerifiablePresentation",
  "verifiableCredential": [ /* one or more VCs */ ],
  "proof": {
    "type": "Ed25519Signature2020",
    "proofPurpose": "authentication",
    "challenge": "verifier-issued-nonce-xyz",
    "verificationMethod": "did:ies:consumer-7a3f9b2c#key-1",
    "proofValue": "z3Abc...holder signature...xyz"
  }
}
```

The VP has **two proofs**:
- The issuer's proof inside each embedded credential (proves authenticity)
- The holder's proof on the outer presentation (proves the holder controls the DID — prevents replay attacks)

The `challenge` is a nonce issued by the Verifier to prevent replay attacks. Always include it.

---

## Selective Disclosure

IES credentials support **selective disclosure**: a holder can prove a specific claim without revealing all credential fields.

**Example:** A service provider needs to verify that a consumer has an active electricity connection in Delhi. The consumer does not need to reveal their exact address or meter number — only a proof of:
- Connection is active
- Service area is Delhi

IES uses [BBS+ signatures](https://identity.foundation/bbs-signature/draft-irtf-cfrg-bbs-signatures.html) for selective disclosure. The IES Credential Service handles this automatically when you request a presentation with specific `revealedAttributes`.

---

## Credential Lifecycle

```
Request → Issue → Hold → Present → Verify
                              │
                              └──> Revoke (if needed)
```

| Phase | Who acts | What happens |
|---|---|---|
| **Request** | Holder or consumer | Submits identity/attribute data to issuer |
| **Issue** | Issuer (DISCOM, certifier) | Creates VC, signs with private key, delivers to holder |
| **Hold** | Holder | Stores VC in wallet (DigiLocker, software wallet) |
| **Present** | Holder | Creates VP in response to a verifier's challenge |
| **Verify** | Verifier | Checks issuer signature, holder binding, expiry, revocation |
| **Revoke** | Issuer | Publishes revocation hash; all future verifications fail |

IES uses **hash-based revocation via DeDi** (a decentralised data registry). OpenCred computes `SHA-256(JCS(credential))` and the issuer publishes that hash to their DeDi namespace. Verifiers check for the hash's presence — found means revoked, absent means valid. There is no central bitstring list to maintain.

---

## Credential Schemas

Every credential type is defined by a **schema** that specifies which fields are required, their data types, and validation rules. OpenCred ships with built-in schemas (Education, Employment, Identity, Health, Business) and supports custom schemas for energy-specific types.

The IES credential type for consumer electricity connections is `ElectricityConnectionCredential` (surfaced to DigiLocker as `NYCER` — National Yield Consumer Electricity Record). DISCOMs declare this `credentialType` in every `POST /v1/credentials/issue` call; no separate schema registration step is required in OpenCred.

---

## Further Reading

- [OpenCred Docs](https://opencred.gitbook.io/docs) — the open credential platform IES is built on. Covers Desktop Client, Docker API, key management, proof formats, revocation, and security model in full detail
- [OpenCred — Issuing credentials](https://opencred.gitbook.io/docs/desktop-client/issuing-credentials)
- [OpenCred — Verifying credentials](https://opencred.gitbook.io/docs/desktop-client/verifying-credentials)
- [OpenCred — Docker API reference](https://opencred.gitbook.io/docs/docker-image/api-reference)
- [W3C VC Data Model](https://www.w3.org/TR/vc-data-model/) — the normative specification
- [W3C DIDs](https://www.w3.org/TR/did-core/) — the DID specification
