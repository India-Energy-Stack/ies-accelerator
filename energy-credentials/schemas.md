# Energy Credential Schemas

DISCOMs issue credentials against the [Beckn DEG `EnergyCredential` schema family](https://github.com/beckn/DEG/tree/main/specification/schema/EnergyCredential). All five concrete schemas inherit a common envelope (issuer with regulatory licence number, validity dates, DeDi revocation status, W3C proof) and differ in their `credentialSubject` fields.

```
beckn:Credential
  └── deg:EnergyCredential                    (shared envelope)
        ├── deg:UtilityCustomerCredential     (identity)
        ├── deg:ConsumptionProfileCredential  (connection / load)
        ├── deg:GenerationProfileCredential   (DER generation)
        ├── deg:StorageProfileCredential      (battery storage)
        └── deg:ProgramEnrollmentCredential   (program enrolment)
```

**Schema location:** `https://schema.beckn.io/<CredentialType>/v2.0`
**Namespace prefix:** `deg:` → `https://schema.beckn.io/deg/EnergyCredential/v2.0/`

---

## Common Envelope — `EnergyCredential`

Every DEG energy credential includes these fields on top of W3C VC's standard ones.

| Property | Type | Required | Notes |
|---|---|---|---|
| `issuer.id` | URI | ✓ | DISCOM DID (`did:web:ies.tpddl.in`) |
| `issuer.name` | string | ✓ | Legal name of the distribution utility |
| `issuer.licenseNumber` | string | ✓ | **DEG-mandated.** Regulatory licence number from your SERC |
| `issuanceDate` | date-time | | ISO 8601 timestamp |
| `expirationDate` | date-time | | Optional |
| `credentialStatus.id` | URI | ✓ | DeDi lookup URL — `https://dedi.global/dedi/lookup/<namespace>/vc-revocation-registry/<hash>` |
| `credentialStatus.type` | const | ✓ | Must be `"dediregistry"` |
| `proof.*` | object | ✓ | W3C proof block — OpenCred fills this |

When you call OpenCred's issue endpoint, you supply `issuerDid`, `validFrom`, `validUntil`, and an optional `revocationRegistryUrl`. OpenCred constructs the envelope; you only need to send the **subject-specific fields** in `credentialSubject`.

---

## 1. `UtilityCustomerCredential`

**The foundational identity credential.** Every consumer should hold this. All other DEG profile credentials reference the same `credentialSubject.id` DID.

**Schema:** `https://schema.beckn.io/UtilityCustomerCredential/v2.0`

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | URI | ✓ | Consumer's DID |
| `consumerNumber` | string | ✓ | Consumer account number from your CIS |
| `fullName` | string | ✓ | Full name as on ID proof |
| `installationAddress` | object | ✓ | See below |
| `meterNumber` | string | ✓ | Unique meter serial number |
| `serviceConnectionDate` | date | ✓ | When the connection was activated |
| `maskedIdNumber` | string | | Masked Aadhaar / government ID. **Never** include the full ID. |

### `installationAddress`

| Property | Required |
|---|---|
| `fullAddress` | ✓ |
| `postalCode` | ✓ |
| `country` (ISO 3166-1 alpha-2, e.g. `IN`) | ✓ |
| `city` | |
| `district` | |
| `stateProvince` | |

### Example

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://schema.beckn.io/EnergyCredential/v2.0",
    "https://schema.beckn.io/UtilityCustomerCredential/v2.0"
  ],
  "type": ["VerifiableCredential", "EnergyCredential", "UtilityCustomerCredential"],
  "issuer": {
    "id": "did:web:ies.tpddl.in",
    "name": "Tata Power Delhi Distribution Limited",
    "licenseNumber": "DERC/DL/2025/0042"
  },
  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3...",
    "consumerNumber": "TPDDL-2025-001234567",
    "fullName": "Priya Sharma",
    "installationAddress": {
      "fullAddress": "Flat 4B, Sector 12, Rohini",
      "postalCode": "110085",
      "country": "IN",
      "city": "New Delhi",
      "stateProvince": "DL"
    },
    "meterNumber": "MTR-98765432",
    "serviceConnectionDate": "2019-03-15",
    "maskedIdNumber": "XXXX-XXXX-1234"
  }
}
```

---

## 2. `ConsumptionProfileCredential`

Connection and load characteristics. Used by tariff engines, demand response programs, and load forecasting.

**Schema:** `https://schema.beckn.io/ConsumptionProfileCredential/v2.0`

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | URI | ✓ | Consumer DID |
| `consumerNumber` | string | ✓ | Consumer account number |
| `fullName` | string | ✓ | Consumer name |
| `premisesType` | enum | ✓ | `Residential` \| `Commercial` \| `Industrial` \| `Agricultural` |
| `connectionType` | enum | ✓ | `Single-phase` \| `Three-phase` |
| `sanctionedLoadKW` | number (0.5–10000) | ✓ | Approved load in kW |
| `tariffCategoryCode` | string | ✓ | Your billing/tariff category code |
| `meterNumber` | string | | Meter serial number |

### Example `credentialSubject`

```json
{
  "id": "did:key:z6MkjVQ8r4f3...",
  "consumerNumber": "TPDDL-2025-001234567",
  "fullName": "Priya Sharma",
  "premisesType": "Residential",
  "connectionType": "Single-phase",
  "sanctionedLoadKW": 5.0,
  "tariffCategoryCode": "DOM-A2",
  "meterNumber": "MTR-98765432"
}
```

---

## 3. `GenerationProfileCredential`

DER asset capabilities. Required for net metering, green energy attribution, and P2P trading as a seller.

**Schema:** `https://schema.beckn.io/GenerationProfileCredential/v2.0`

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | URI | ✓ | Consumer DID |
| `consumerNumber` | string | ✓ | Consumer account number |
| `generationType` | enum | ✓ | `Solar` \| `Wind` \| `MicroHydro` \| `Other` |
| `capacityKW` | number (0.1–10000) | ✓ | Installed capacity in kW |
| `commissioningDate` | date | ✓ | Activation date |
| `fullName` | string | | Consumer name |
| `meterNumber` | string | | Net meter serial |
| `assetId` | string | | DER asset unique ID |
| `manufacturer` | string | | Panel / turbine manufacturer |
| `modelNumber` | string | | Equipment model |

### Example `credentialSubject`

```json
{
  "id": "did:key:z6MkjVQ8r4f3...",
  "consumerNumber": "TPDDL-2025-001234567",
  "generationType": "Solar",
  "capacityKW": 4.5,
  "commissioningDate": "2025-08-20",
  "assetId": "TPDDL-DER-2025-A11023",
  "manufacturer": "Tata Power Solar",
  "modelNumber": "TP-330W-MONO"
}
```

---

## 4. `StorageProfileCredential`

Behind-the-meter battery storage. Enables virtual power plant participation and time-of-use arbitrage.

**Schema:** `https://schema.beckn.io/StorageProfileCredential/v2.0`

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | URI | ✓ | Consumer DID |
| `consumerNumber` | string | ✓ | Consumer account number |
| `storageCapacityKWh` | number (0.1–10000) | ✓ | Storage capacity in kWh |
| `powerRatingKW` | number (0.1–10000) | ✓ | Charge/discharge rating in kW |
| `commissioningDate` | date | ✓ | Activation date |
| `fullName` | string | | Consumer name |
| `meterNumber` | string | | Meter serial |
| `assetId` | string | | Storage asset unique ID |
| `storageType` | enum | | `LithiumIon` \| `LeadAcid` \| `FlowBattery` \| `Other` |

---

## 5. `ProgramEnrollmentCredential`

On-chain proof of enrolment in a specific energy program — P2P trading, ToU tariff, demand response, VPP. Typically short-lived; `expirationDate` should match the program window.

**Schema:** `https://schema.beckn.io/ProgramEnrollmentCredential/v2.0`

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | URI | ✓ | Consumer DID |
| `consumerNumber` | string | ✓ | Consumer account number |
| `programName` | string | ✓ | Human-readable program name |
| `programCode` | string | ✓ | Unique program identifier |
| `enrollmentDate` | date | ✓ | Enrolment date |
| `fullName` | string | | Consumer name |
| `validUntil` | date | | Enrolment expiration |

### Example `credentialSubject`

```json
{
  "id": "did:key:z6MkjVQ8r4f3...",
  "consumerNumber": "TPDDL-2025-001234567",
  "programName": "Delhi Rooftop P2P Pilot — Cohort 2026A",
  "programCode": "TPDDL-P2P-2026A",
  "enrollmentDate": "2026-05-01",
  "validUntil": "2027-04-30"
}
```

---

## Schema Composition Strategies

DISCOMs typically issue **multiple credentials per consumer** as facts emerge:

| Trigger event | Credential to issue |
|---|---|
| New service connection | `UtilityCustomerCredential` + `ConsumptionProfileCredential` |
| Tariff category change | Re-issue `ConsumptionProfileCredential`, revoke the old one |
| Rooftop solar commissioning | `GenerationProfileCredential` |
| Battery commissioning | `StorageProfileCredential` |
| Program enrolment / withdrawal | `ProgramEnrollmentCredential` (issue or revoke) |

All five reference the same `credentialSubject.id` (the consumer's DID), so a verifier with the bundle can compose a complete picture: identity + connection + DER + storage + active programs.

---

## Implementing in OpenCred

OpenCred can load DEG schemas in three ways:

1. **Built-in schema ID** — once DEG schemas ship in the OpenCred image, pass `schemaId: "deg/utility-customer/v2"` (or similar; check `GET /v1/schemas`).
2. **Inline schema** — pass the JSON Schema fragment in the request body as `inlineSchema`.
3. **Inline context** — pass the JSON-LD `@context` fragment as `inlineContext`.

For day-one deployments without a built-in DEG schema, the simplest pattern is `inlineSchema` + `inlineContext` from the [DEG repo](https://github.com/beckn/DEG/tree/main/specification/schema/EnergyCredential). Worked examples are in [Issuing Credentials](./issuance.md).

---

## References

- [Beckn DEG — `EnergyCredential` v2.0](https://github.com/beckn/DEG/tree/main/specification/schema/EnergyCredential/v2.0)
- [Beckn DEG — `UtilityCustomerCredential` v2.0](https://github.com/beckn/DEG/tree/main/specification/schema/UtilityCustomerCredential/v2.0)
- [Beckn DEG — `ConsumptionProfileCredential` v2.0](https://github.com/beckn/DEG/tree/main/specification/schema/ConsumptionProfileCredential/v2.0)
- [Beckn DEG — `GenerationProfileCredential` v2.0](https://github.com/beckn/DEG/tree/main/specification/schema/GenerationProfileCredential/v2.0)
- [Beckn DEG — `StorageProfileCredential` v2.0](https://github.com/beckn/DEG/tree/main/specification/schema/StorageProfileCredential/v2.0)
- [Beckn DEG — `ProgramEnrollmentCredential` v2.0](https://github.com/beckn/DEG/tree/main/specification/schema/ProgramEnrollmentCredential/v2.0)
