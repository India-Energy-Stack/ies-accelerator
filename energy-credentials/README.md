# IES Energy Credentials

**IES Energy Credentials** are cryptographically signed digital attestations about energy assets and consumers. They are the trust layer of the India Energy Stack — enabling any participant to prove claims about themselves or their assets without relying on paper documents or centralised intermediaries.

---

## What Can a Credential Attest?

| Credential Type | Issued By | Subject |
|---|---|---|
| Electricity Connection (NYCER) | DISCOM | Consumer — proves active connection, address |
| Green Energy Certification | Renewable Energy Authority | Prosumer/asset — proves solar/renewable source |
| Grid Interconnection Approval | Utility / DISCOM | DER asset — proves authorised grid connection |
| Safety & Standards Compliance | Certification body | EVSE / charging station |
| Subsidy Eligibility | MNRE / State Government | Consumer or asset |
| Asset Ownership | Land Registry / DISCOM | Prosumer — proves ownership rights |

---

## How It Works

IES Energy Credentials follow the [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/). Three roles are always involved:

```
  ISSUER                    HOLDER                   VERIFIER
(DISCOM, Govt,          (Consumer, Prosumer,      (Service provider,
 Certifier)              Asset owner)              Marketplace, App)
     │                        │                        │
     │── issues VC ──────────>│                        │
     │   (signed with         │                        │
     │    issuer's key)       │── presents VP ────────>│
     │                        │   (signed with         │
     │                        │    holder's key)       │── verifies ──>
     │                        │                        │   signatures
     │                        │                        │   + status
```

1. The **Issuer** creates a credential, signs it with their private key, and delivers it to the Holder.
2. The **Holder** stores it in a wallet (DigiLocker for consumers, or a software wallet for machines).
3. The **Verifier** receives a presentation from the Holder and verifies both the Issuer's signature and the Holder's binding — without contacting the Issuer.

---

## IES and DigiLocker

For consumer-facing credentials (e.g. electricity connection proof), IES integrates with **DigiLocker** — India's national digital document wallet operated by NeGD. This means:

- Consumers access their energy credential through the DigiLocker app they already have
- No new app install is required
- Credentials can be shared with any DigiLocker-connected verifier (banks, government portals, housing societies)

**OpenCred** handles the W3C VC lifecycle — issuance, signing, and verification. DISCOMs call OpenCred's Docker API from their Pull URI endpoint to produce a signed credential on demand, then return it to DigiLocker. DigiLocker handles consumer-facing storage and sharing.

For machine-to-machine credentials (e.g. DER assets in a P2P energy marketplace), credentials are issued directly to DID-controlled wallets without DigiLocker.

---

## Sections in This Chapter

| Page | What you'll learn |
|---|---|
| [Core Concepts](./concepts.md) | W3C VCs, DIDs, credential structure, selective disclosure |
| [Onboarding Guide](./onboarding.md) | Step-by-step setup for DISCOMs and service providers |
| [Issuing Credentials](./issuance.md) | API calls to create and sign credentials |
| [Verifying Credentials](./verification.md) | How to verify a credential presented by a holder |
| [DigiLocker Integration](./digilocker-integration.md) | Full DISCOM guide for the DigiLocker Pull URI endpoint |

---

## Reference

- [OpenCred Documentation](https://opencred.gitbook.io/docs) — the open credential platform IES is built on (Desktop Client, Docker API, key management, proof formats, revocation)
- [W3C Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/)
- [W3C Decentralized Identifiers](https://www.w3.org/TR/did-core/)
- [IES Energy Credentials Architecture](https://github.com/India-Energy-Stack/ies-docs/blob/main/architecture/03_Energy_Credentials.md)
