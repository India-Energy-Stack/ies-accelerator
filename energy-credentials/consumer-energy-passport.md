# Consumer Energy Passport Credential

The **Consumer Energy Passport** is a wallet-held W3C Verifiable Credential 2.0 issued by a DISCOM that binds a consumer's identity to their connection, meter, sanctioned load, and DER / storage assets. It is the credential behind the [Consumer Energy Passport use case](../use-cases/consumer-energy-passport.md).

> **Status — draft.** The schema below is the working shape under review. The envelope, sub-profile composition, and `identityBinding` block are stable; the "minimum-disclosure presentation" profiles are still being agreed.

---

## Relationship to `CustomerCredential`

The Passport is a **superset** of [`CustomerCredential`](./schemas.md). Everything `CustomerCredential` carries, the Passport carries — plus an explicit `identityBinding` block that promotes the consumer's identity reference from an optional sub-field on `customerProfile` to a top-level, mandatory part of the credential subject.

| Concern | `CustomerCredential` | `ConsumerEnergyPassport` |
|---|---|---|
| Primary purpose | DISCOM-issued attestation about a meter and its assets | Wallet-shareable attestation the consumer presents to *any* verifier |
| Identity binding | Optional `customerProfile.idRef` | **Required** top-level `identityBinding` block |
| Selective disclosure | Possible via SD-JWT-VC | First-class — SD-JWT-VC presentation profiles per verifier kind |
| Re-issuance triggers | Same as Passport | Same — share the same lifecycle |

A DISCOM that already issues `CustomerCredential` per meter can issue the Passport from the same OpenCred service with the same data sources — only the `type` array, the `identityBinding` block, and the presentation profile change.

---

## Common Envelope

Same as [`CustomerCredential`](./schemas.md#common-envelope). The `type` array carries `"ConsumerEnergyPassport"`:

```json
"type": ["VerifiableCredential", "ConsumerEnergyPassport"]
```

All other top-level envelope fields (`@context`, `id`, `issuer`, `validFrom`, `validUntil`, `credentialStatus`, `proof`) are identical.

---

## credentialSubject

```
ConsumerEnergyPassport.credentialSubject
├── id                       (required — consumer DID)
├── identityBinding          (required)
├── customerProfile          (required)
├── customerDetails          (required for the Passport — recommended for CustomerCredential)
├── consumptionProfiles[]    (required — at least one)
├── generationProfiles[]     (optional — one entry per DER asset)
└── storageProfiles[]        (optional — one entry per battery)
```

### identityBinding (required)

The block that elevates the consumer's identity reference to first-class status. It binds the holder DID (`credentialSubject.id`) to a verifiable government-ID reference.

| Field | Type | Required | Description |
|---|---|---|---|
| `subjectDid` | URI (DID) | ✓ | The consumer's DID — must match `credentialSubject.id` |
| `idRef` | object | ✓ | Reference to the government identity — see [idRef](./schemas.md#idref). Carry the *reference*, not the raw ID number. |
| `bindingMethod` | enum | ✓ | How the binding was established: `"AADHAAR_OFFLINE_KYC"`, `"DIGILOCKER_PULL"`, `"IN_PERSON_VERIFICATION"`, `"DISCOM_RECORD_MATCH"` |
| `bindingDate` | date-time | ✓ | When the binding was performed |

### customerProfile, customerDetails, consumptionProfiles[], generationProfiles[], storageProfiles[]

Identical to [`CustomerCredential`](./schemas.md#credentialsubject). The Passport tightens two optionality rules:

- `customerDetails` is **required** in the Passport (verifiers expect to see the holder's name and address).
- `consumptionProfiles[]` is **required** with `minItems: 1`.

All field-level rules and enums (e.g. `meterType`, `premisesType`, `connectionType`, `generationType`, `storageType`) are unchanged.

---

## Full example

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/ElectricityCredential/v1.0/context.jsonld"
  ],
  "id": "urn:uuid:e5f6a7b8-9012-34ab-cdef-567890123456",
  "type": ["VerifiableCredential", "ConsumerEnergyPassport"],
  "issuer": {
    "id": "did:web:ies.tpddl.in",
    "name": "Tata Power Delhi Distribution Limited",
    "idRef": {
      "issuedBy": "did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma",
      "subjectId": "india-energy-stack:tpddl"
    }
  },
  "validFrom": "2026-05-01T00:00:00+05:30",
  "validUntil": "2031-05-01T00:00:00+05:30",
  "credentialStatus": {
    "id": "https://dedi.global/dedi/lookup/tpddl/vc-revocation-registry/e5f6a7b8-9012-34ab-cdef-567890123456",
    "type": "dedi",
    "statusPurpose": "revocation",
    "statusListCredential": "https://dedi.global/dedi/query/tpddl/vc-revocation-registry"
  },
  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
    "identityBinding": {
      "subjectDid": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
      "idRef": {
        "issuedBy": "did:web:uidai.gov.in",
        "subjectId": "uidai.gov.in:XXXX-XXXX-1234"
      },
      "bindingMethod": "DIGILOCKER_PULL",
      "bindingDate": "2026-04-28T10:30:00+05:30"
    },
    "customerProfile": {
      "customerNumber": "TPDDL-2025-001234567",
      "meterNumber": "MTR-98765432",
      "meterType": "AMI"
    },
    "customerDetails": {
      "fullName": "Priya Sharma",
      "installationAddress": {
        "address": "Flat 4B, Sector 12, Rohini",
        "city":    {"name": "New Delhi", "code": "DEL"},
        "state":   {"name": "Delhi",     "code": "DL"},
        "country": {"name": "India",     "code": "IN"},
        "area_code": "110085",
        "openLocationCode": "7JWVQ7G3+QR"
      },
      "serviceConnectionDate": "2019-03-15T00:00:00+05:30"
    },
    "consumptionProfiles": [{
      "premisesType": "Residential",
      "connectionType": "Single-phase",
      "sanctionedLoadKW": 5,
      "tariffCategoryCode": "DOM-A2"
    }],
    "generationProfiles": [{
      "assetId": "DER-TPDDL-2024-005678",
      "generationType": "Solar",
      "capacityKW": 5.5,
      "commissioningDate": "2024-08-20T00:00:00+05:30",
      "manufacturer": "Tata Power Solar",
      "modelNumber": "TP540M-72"
    }]
  }
}
```

---

## Issuing the Passport

Issuance reuses [the `CustomerCredential` issuance flow](./issuance.md) with two changes:

1. Pass `type: ["VerifiableCredential", "ConsumerEnergyPassport"]` in the issuance request.
2. Include the `identityBinding` block in `credentialSubject`. If you don't yet capture consumer DIDs at onboarding, use the DigiLocker pull path to mint one and record the binding as `bindingMethod: "DIGILOCKER_PULL"`.

OpenCred's built-in schema dispatch will validate against the `ConsumerEnergyPassport` schema once the canonical schema files land alongside [`/schemas/ElectricityCredential/v1.0/`](/schemas/ElectricityCredential/v1.0/). Until then, pass `inlineSchema` referencing the JSON Schema fragment derived from this page.

---

## Selective Disclosure Presentations

Three minimum-disclosure presentations are being formalised. Each is an SD-JWT-VC presentation profile that selectively reveals only the necessary claims:

| Presentation | Reveals | Use case |
|---|---|---|
| `passport-loan` | `identityBinding`, `customerDetails.fullName`, `consumptionProfiles[].sanctionedLoadKW`, `generationProfiles[]` | Green-loan / energy-efficiency loan applications |
| `passport-marketplace` | `customerProfile.meterNumber`, `generationProfiles[]`, `storageProfiles[]` | DER marketplace registration |
| `passport-subsidy` | `identityBinding`, `consumptionProfiles[].tariffCategoryCode`, `consumptionProfiles[].premisesType` | Government subsidy portals |

Verifiers indicate which presentation they need; the wallet redacts the rest.

---

## References

- [Consumer Energy Passport — use case](../use-cases/consumer-energy-passport.md)
- [`CustomerCredential` — base schema](./schemas.md)
- [Core Concepts](./concepts.md)
- [Issuance](./issuance.md)
- [Verification](./verification.md)
- [SD-JWT-VC](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/)
