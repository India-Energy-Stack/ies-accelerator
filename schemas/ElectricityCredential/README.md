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
| [v1.2](v1.2/README.md) | **Current** | Composable EnergyResource kinds (7 typed discriminants); directional power fields; EV charger kind |
| [v1.1](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ElectricityCredential/v1.1) | Previous | Unified `energyResources[]` (EnergyResource/v2.0), multi-meter topology support |
| [v1.0](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ElectricityCredential/v1.0) | Deprecated | Separate `consumptionProfiles[]`, `generationProfiles[]`, `storageProfiles[]` arrays |

---

## Inheritance

```
beckn:Credential
  └── EnergyCredential
        └── ElectricityCredential  ← this schema
```

---

## Usage

Issued by electricity distribution utilities to consumers and prosumers. Used for:
- P2P energy trading eligibility and identity verification
- Demand response and virtual power plant enrollment
- DER asset registration and grid service qualification
- Program enrollment and tariff management
