# Consumer Energy Passport — credential reference

The **Consumer Energy Passport** is a W3C Verifiable Credential 2.0 of type `["VerifiableCredential", "ConsumerEnergyPassport"]`, issued by a DISCOM and held by a consumer in [DigiLocker](../glossary.md#digilocker) or a DID wallet. Verifiers — banks, marketplaces, regulators, subsidy portals — validate it offline against the DISCOM's published public key.

For the implementer guide, start with [Use cases → Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md). This page is the credential reference — what the type is, what its subject carries, and what makes it different from a plain `ElectricityCredential`.

---

## What it is

The Passport's `credentialSubject` is the [ElectricityCredential v1.2](../schemas/ElectricityCredential/README.md) subject **plus** one Passport-specific block: `identityBinding`.

```
credentialSubject
├── id                   — consumer wallet DID
├── identityBinding      — Passport-specific (see below)
├── customerProfile      — ElectricityCredential v1.2 (non-PII + energyResources[])
├── customerDetails      — ElectricityCredential v1.2 (PII)
└── consumptionProfiles[] — ElectricityCredential v1.2 (MeterServiceProfile per meter)
```

Everything except `identityBinding` is defined in [ElectricityCredential v1.2](../schemas/ElectricityCredential/README.md). Use that page for full field tables, CIM alignments, enums, and worked examples.

### How it differs from a plain `ElectricityCredential`

| Concern | `ElectricityCredential` (v1.2) | `ConsumerEnergyPassport` |
|---|---|---|
| Primary audience | DISCOM-issued attestation about a meter and its assets | Wallet-shareable attestation the consumer presents to *any* verifier |
| Identity binding | Optional `customerProfile.idRef` | **Required** top-level `identityBinding` block |
| Selective disclosure | Possible via SD-JWT-VC | First-class — SD-JWT-VC presentation profiles per verifier kind |
| Issuance / verification path | OpenCred | OpenCred (same) |

A DISCOM already issuing `ElectricityCredential` adds the `identityBinding` block and changes the `type` array — no new infrastructure.

---

## identityBinding (Passport-specific)

Binds the consumer's wallet DID (`credentialSubject.id`) to a verifiable government-ID reference.

| Field | Type | Description |
|---|---|---|
| `subjectDid` | URI (DID) | Must equal `credentialSubject.id` |
| `idRef` | object | Reference to a government identity — see [IdRef in ElectricityCredential v1.2](../schemas/ElectricityCredential/README.md). Carry the **reference**, never the raw ID number. |
| `bindingMethod` | enum | `AADHAAR_OFFLINE_KYC` / `DIGILOCKER_PULL` / `IN_PERSON_VERIFICATION` / `DISCOM_RECORD_MATCH` |
| `bindingDate` | date-time | When the binding was established |

---

## Envelope

The W3C VC envelope is identical to any other ElectricityCredential — see [ElectricityCredential v1.2 → Structure](../schemas/ElectricityCredential/README.md). The only Passport-specific things are:

- `type` includes `"ConsumerEnergyPassport"`
- `credentialSubject.identityBinding` is required

```json
"@context": [
  "https://www.w3.org/ns/credentials/v2",
  "https://schema.beckn.io/ElectricityCredential/v1.2/context.jsonld"
],
"type": ["VerifiableCredential", "ConsumerEnergyPassport"]
```

---

## Issuing the Passport

Reuses the [ElectricityCredential issuance flow](./issuance.md) with two changes:

1. Pass `type: ["VerifiableCredential", "ConsumerEnergyPassport"]` in the issuance request.
2. Include the `identityBinding` block in `credentialSubject`.

Use `proofFormat: "vc-jwt"`. Wallet delivery via [DigiLocker](./digilocker-integration.md) Pull URI for the bulk of consumers; direct DID push for non-DigiLocker wallets.

End-to-end implementer guide: [Use cases → Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md).

---

## Verification

A verifier:

1. Resolves the issuer DISCOM via the [IES DISCOMs Reference Registry](../registries/required-registries.md#discom-reference-registry).
2. Resolves the DISCOM's `did:web` to its current public key.
3. Validates the `proof` locally — no callback to the DISCOM.
4. Checks `credentialStatus` against the DISCOM's DeDi revocation registry.

Walkthrough: [Verifying Credentials](./verification.md).

---

## Selective disclosure

SD-JWT-VC enables minimum-disclosure presentations. The IES profile is consolidating three named presentation kinds: `passport-loan`, `passport-marketplace`, `passport-subsidy`. See the [Use cases → Appendix](../use-cases/consumer-energy-passport/README.md#a3-selective-disclosure) for the field sets.

---

## Status

The `ConsumerEnergyPassport` composite type is in draft. The envelope, the dependence on [ElectricityCredential v1.2](../schemas/ElectricityCredential/README.md), and the `identityBinding` block are stable. SD-JWT-VC presentation profiles are being formalised.

---

## References

- [Use cases → Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md) — implementer guide
- [ElectricityCredential v1.2 schema](../schemas/ElectricityCredential/README.md) — subject shape
- [Energy Credentials → Core Concepts](./concepts.md)
- [Energy Credentials → Issuance](./issuance.md)
- [Energy Credentials → Verification](./verification.md)
- [Energy Credentials → DigiLocker Integration](./digilocker-integration.md)
- [W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [SD-JWT-VC](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/)
