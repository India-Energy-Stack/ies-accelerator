# ElectricityCredential

> **Mirror.** This directory is a verbatim mirror of the Beckn DEG [`ElectricityCredential`](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential) specification, vendored into this repo so the IES accelerator docs can reference schema files at stable repo-relative paths.
>
> Canonical upstream source: [`beckn/DEG/specification/schema/ElectricityCredential`](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential). If you find a discrepancy between this mirror and upstream, treat upstream as authoritative and open an issue on this repo so the mirror can be refreshed.

Unified W3C Verifiable Credential (VC Data Model 2.0) issued per meter by electricity distribution utilities. Combines customer identity with optional consumption, generation, and storage profiles in a single credential.

**Namespace prefix:** `deg:` → `https://schema.beckn.io/deg/`

**Tags:** `energy` · `credential` · `verifiable-credential` · `electricity` · `customer` · `deg`

---

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v1.1](v1.1/README.md) | **Current** | Unified `energyResources[]` (EnergyResource/v2.0), multi-meter topology support |
| [v1.0](v1.0/README.md) | Previous | Separate `consumptionProfiles[]`, `generationProfiles[]`, `storageProfiles[]` arrays |

---

## Inheritance

```
beckn:Credential
  └── EnergyCredential
        └── ElectricityCredential  ← this schema
```

---

## credentialSubject Properties (v1.1)

| Property | Type | Required | Description |
|----------|------|:--------:|-------------|
| `id` | `string` (URI) | | Optional DID of the customer/credential subject |
| `customerProfile` | object | ✅ | Non-PII: customer number, all energy resources, tariff profiles |
| `customerProfile.customerNumber` | string | ✅ | Utility CA number |
| `customerProfile.energyResources[]` | array | ✅ | All physical assets — meters, DERs, storage (EnergyResource/v2.0) |
| `customerProfile.consumptionProfiles[]` | array | | Tariff/load profiles, linked to meters via `meterId` |
| `customerDetails` | object | | PII — full name, installation address, connection date |

---

## Linked Data (v1.1)

| Term | IRI |
|------|-----|
| `ElectricityCredential` | `deg:ElectricityCredential` |
| `customerProfile` | `deg:customerProfile` |
| `customerDetails` | `deg:customerDetails` |
| `energyResources` | `deg:energyResources` |
| `consumptionProfiles` | `deg:consumptionProfiles` |
| `meterId` | `deg:meterId` |

---

## v1.0 → v1.1 Migration Summary

| v1.0 | v1.1 |
|------|------|
| `customerProfile.meterNumber` | `energyResources[METER].id` |
| `customerProfile.meterType` | `energyResources[METER].attributes.meterType` |
| `generationProfiles[].assetId` | `energyResources[DER].id` |
| `generationProfiles[].capacityKW` | `energyResources[DER].attributes.ratedPowerKw` |
| `generationProfiles[].manufacturer` | `energyResources[DER].attributes.make` |
| `storageProfiles[].storageCapacityKWh` | `energyResources[DER].attributes.energyCapacityKwh` |
| `storageProfiles[].storageType` | `energyResources[DER].attributes.storageType` |
| `fullName` duplicated per profile entry | `customerDetails.fullName` (once only) |

See [v1.1/README.md](v1.1/README.md) for the full migration table.

---

## Usage

Issued by electricity distribution utilities to consumers and prosumers. Used for:
- P2P energy trading eligibility and identity verification
- Demand response and virtual power plant enrollment
- DER asset registration and grid service qualification
- Program enrollment and tariff management
