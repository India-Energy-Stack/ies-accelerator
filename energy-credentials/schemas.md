# Electricity Credential Schema

DISCOMs issue a single unified **`CustomerCredential`** (from the IES Electricity Credential schema family — see [`/schemas/ElectricityCredential/v1.0/`](../schemas/ElectricityCredential/v1.0/README.md)) per meter. One credential carries customer identity, address, consumption characteristics, generation assets, and storage assets as equal-level sub-profiles within a single W3C Verifiable Credential (VC Data Model 2.0).

> **Schema files.** All canonical schema artefacts referenced on this page live under [`/schemas/ElectricityCredential/v1.0/`](../schemas/ElectricityCredential/v1.0/README.md) in this repository. Repository root: **https://github.com/India-Energy-Stack/ies-accelerator**. The directory contains `schema.json` (JSON Schema 2020-12), `context.jsonld` (JSON-LD context), `attributes.yaml` (field reference), and `examples/example.json`.
>
> **Upstream provenance.** The schema is sourced from the Beckn DEG [`ElectricityCredential` v1.0](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential/v1.0) specification and mirrored into this repo for offline reference. All field rules below are normative against the mirrored `schema.json`.
>
> **`$id` URL.** Since OpenCred v1.5.0 ([PR #570](https://github.com/nfh-trust-labs/opencred/pull/570)) the built-in `electricity/v1` schema's `$id` is `https://schema.beckn.io/ElectricityCredential/1.0/schema.json` — the canonical Beckn-hosted URL. This is the value OpenCred writes into every issued credential's `credentialSchema.id`. The schema **content** (properties, required fields, enums) is byte-identical to the IES mirror above; only the dereference URL differs. The JSON-LD context still resolves from the `opencred-vc-schemas` mirror via the bundled context loader.

```
CustomerCredential
└── credentialSubject
      ├── id                    (optional — consumer DID)
      ├── customerProfile       (required — meter, customer number, idRef)
      ├── customerDetails       (optional — name, address, connection date)
      ├── consumptionProfiles[] (optional — premises, load, tariff per meter/category)
      ├── generationProfiles[]  (optional — one entry per DER asset)
      └── storageProfiles[]     (optional — one entry per battery)
```

One credential per meter. Multiple assets of the same kind go into the corresponding array; you do not issue separate credentials per asset.

---

## Common Envelope

Every credential includes these top-level fields on top of W3C VC's standard ones.

| Property | Type | Required | Notes |
|---|---|---|---|
| `@context` | array | ✓ | Must contain `https://www.w3.org/ns/credentials/v2`; minItems 2 |
| `id` | URI | ✓ | URN UUID — e.g. `urn:uuid:e5f6a7b8-9012-34ab-cdef-567890123456` |
| `type` | array | ✓ | Must contain `"CustomerCredential"`; minItems 2 — typically `["VerifiableCredential", "CustomerCredential"]` |
| `issuer.id` | URI | ✓ | DISCOM DID (`did:web:bescom.karnataka.gov.in`) or HTTPS URL |
| `issuer.name` | string | ✓ | Legal name of the distribution utility |
| `issuer.idRef` | object | | Regulatory registration of the utility — see [idRef](#idref) |
| `validFrom` | date-time | ✓ | ISO 8601 with explicit timezone offset |
| `validUntil` | date-time | | Optional expiration |
| `credentialStatus.id` | URI | ✓ | DeDi lookup URL — `https://dedi.global/dedi/lookup/<namespace>/vc-revocation-registry/<credential-id>` |
| `credentialStatus.type` | const | ✓ | `"dedi"` |
| `credentialStatus.statusPurpose` | enum | ✓ | `"revocation"` or `"suspension"` |
| `credentialStatus.statusListCredential` | URI | ✓ | Registry query URL — `https://dedi.global/dedi/query/<namespace>/vc-revocation-registry` |
| `credentialSubject` | object | ✓ | The profile sections — see below |
| `proof` | object | ✓ | W3C proof block — OpenCred fills this |

When you call OpenCred's issue endpoint, you supply `issuerDid`, `validFrom`, optional `validUntil`, and (if revocation is configured) `revocationRegistryUrl`. OpenCred sets `issuer.id` to your DID and fills `proof` and `credentialStatus`.

**OpenCred does not accept `issuer.name` or `issuer.idRef` as request fields.** Both are required by the schema, so your integration service must post-process the returned credential and inject the full `issuer` object before delivery. Note that re-shaping `issuer` invalidates the original `proof`; the practical pattern is to either re-sign in your integration service or pass the patched fields back through OpenCred for re-signing.

---

## credentialSubject

Only `customerProfile` is required. All other sub-profiles are optional and appear when the relevant assets/details exist for that meter.

### customerProfile (required)

| Field | Type | Required | Description |
|---|---|---|---|
| `customerNumber` | string | ✓ | Consumer account number from your CIS |
| `meterNumber` | string | ✓ | Unique meter serial number |
| `meterType` | enum | ✓ | See [meterType enum](#metertype-enum) |
| `idRef` | object | | Customer's external government-ID reference — see [idRef](#idref). **Never include the raw ID number.** |

#### meterType enum

Values derived from Green Button / ESPI meter-kind classifications:

| Value | Description |
|---|---|
| `AMR` | Automated Meter Reading |
| `AMI` | Advanced Metering Infrastructure (smart meter) |
| `Electromechanical` | Traditional electromechanical meter |
| `Forward` | Forward-only (import) meter |
| `Reverse` | Reverse-only (export) meter |
| `Bidirectional` | Bidirectional meter (import + export) |
| `Prepaid` | Prepaid / token-based meter |
| `NetMeter` | Net-metering meter |
| `Other` | Other |

### customerDetails

Personal and address information.

| Field | Type | Required | Description |
|---|---|---|---|
| `fullName` | string | ✓ | Full name as on ID proof |
| `installationAddress` | object | ✓ | See [installationAddress](#installationaddress) |
| `serviceConnectionDate` | date-time | ✓ | ISO 8601 with timezone (e.g. `"2019-03-15T00:00:00+05:30"`) |

#### installationAddress

The address object follows the [beckn Location](https://github.com/beckn/protocol-specifications/blob/master/schema/Location.yaml) shape — with an added `openLocationCode` field — and reuses [schema.org](https://schema.org/) vocabulary where applicable.

| Field | Type | Required | Description |
|---|---|---|---|
| `address` | string | ✓ | Complete postal address |
| `country` | object | ✓ | `{ name: string, code: string }` — ISO 3166-1 alpha-2 |
| `area_code` | string | ✓ | Postal / PIN code |
| `city` | object | | `{ name: string, code: string }` |
| `district` | string | | District / county |
| `state` | object | | `{ name: string, code: string }` |
| `gps` | string | | `"lat,lng"` |
| `openLocationCode` | string | | Open Location Code (OLC) |
| `id` | string | | Stable identifier for the location |
| `descriptor` | object | | `{ name, code, short_desc, long_desc }` |
| `map_url` | string (uri) | | Map link |
| `circle` | object | | Geo-fence — `{ gps, radius }` |
| `polygon` | string | | Boundary polygon |

### consumptionProfiles[]

Array with `minItems: 1` when present. One entry per meter or tariff category.

| Field | Type | Required | Description |
|---|---|---|---|
| `premisesType` | enum | ✓ | `Residential` \| `Commercial` \| `Industrial` \| `Agricultural` |
| `connectionType` | enum | ✓ | `Single-phase` \| `Three-phase` |
| `sanctionedLoadKW` | number | ✓ | Sanctioned load in kW |
| `tariffCategoryCode` | string | ✓ | Your billing / tariff category code |

### generationProfiles[]

Array with `minItems: 1` when present. One entry per DER asset.

| Field | Type | Required | Description |
|---|---|---|---|
| `generationType` | enum | ✓ | `Solar` \| `Wind` \| `MicroHydro` \| `Other` |
| `capacityKW` | number | ✓ | Installed capacity in kW |
| `commissioningDate` | date-time | ✓ | Activation timestamp |
| `assetId` | string | | DER asset unique ID |
| `manufacturer` | string | | Panel / turbine manufacturer |
| `modelNumber` | string | | Equipment model |

### storageProfiles[]

Array with `minItems: 1` when present. One entry per battery.

| Field | Type | Required | Description |
|---|---|---|---|
| `storageCapacityKWh` | number | ✓ | Storage capacity in kWh |
| `powerRatingKW` | number | ✓ | Charge / discharge rating in kW |
| `commissioningDate` | date-time | ✓ | Activation timestamp |
| `assetId` | string | | Storage asset unique ID |
| `storageType` | enum | | `LithiumIon` \| `LeadAcid` \| `FlowBattery` \| `Other` |

---

## idRef

A reusable identity-reference pattern used in two places:

- **`issuer.idRef`** — the DISCOM's entry in the **IES DISCOMs Reference Registry**. This is the trust anchor verifiers use to look up the issuer's published public key and confirm the DISCOM is a registered IES participant.
- **`customerProfile.idRef`** — the customer's external identity (e.g. Aadhaar / government ID), used **instead of** carrying the raw ID

| Field | Type | Required | Description |
|---|---|---|---|
| `issuedBy` | URI (DID) | ✓ | DID of the issuing authority |
| `subjectId` | string | ✓ | `authority-domain:id-value`, e.g. `india-energy-stack:tpddl` |

### IES DISCOMs Reference Registry

A DISCOM acting as an issuer must be registered in the **IES DISCOMs Reference Registry**. The registry is the canonical source of truth for **which DISCOMs are trusted issuers and what public key each has published**. Verifiers consult it during signature verification — without a registry entry, a credential cannot be trusted, even if the cryptographic signature itself is valid.

The registry lives on [`dedi.global`](https://dedi.global) under the IES namespace. Its full base URL is:

```
https://api.dedi.global/dedi/lookup/did%3Aweb%3Adid.cord.network%3A76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma/
```

That long path segment is the URL-encoded form of the namespace DID `did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma` — the cryptographic identifier of the `india-energy-stack` namespace on DeDi. Throughout the rest of these docs we refer to entries by the **relative path** below; prepend the base URL above to resolve.

| Property | Value |
|---|---|
| Host | `api.dedi.global` |
| Namespace (friendly) | `india-energy-stack` |
| Namespace DID | `did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma` |
| Registry name | `ies-discoms-reference-registry` |
| Relative path to a DISCOM entry | `india-energy-stack/ies-discoms-reference-registry/<discom-id>` |
| Issuer (`issuedBy`) DID | `did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma` |
| `subjectId` format | `india-energy-stack:<discom-short-code>` (e.g. `india-energy-stack:tpddl`, `india-energy-stack:bescom`) |

> A sibling registry — `ies-regulators-reference-registry` — lives in the same namespace and holds regulator entries (DERCs, KERCs, etc.). It is not consulted for `issuer.idRef` on electricity credentials, but it is the lookup destination if your application needs to verify a regulator separately.

Setting `issuer.idRef` to point at this registry is what makes a credential **verifiable on the IES network**. Verifiers do not need to know your DISCOM out-of-band — they resolve the registry entry and obtain both the trust assertion and the public key in one lookup.

Customer example (masked Aadhaar reference):

```json
"idRef": {
  "issuedBy": "did:web:uidai.gov.in",
  "subjectId": "uidai.gov.in:XXXX-XXXX-1234"
}
```

---

## Full example

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.0/context.jsonld"
  ],
  "id": "urn:uuid:e5f6a7b8-9012-34ab-cdef-567890123456",
  "type": ["VerifiableCredential", "CustomerCredential"],
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
    "customerProfile": {
      "customerNumber": "TPDDL-2025-001234567",
      "meterNumber": "MTR-98765432",
      "meterType": "AMI",
      "idRef": {
        "issuedBy": "did:web:uidai.gov.in",
        "subjectId": "uidai.gov.in:XXXX-XXXX-1234"
      }
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

## Lifecycle Patterns

DISCOMs issue **one credential per meter** and re-issue when material facts change:

| Trigger event | Action |
|---|---|
| New service connection activated | Issue with `customerProfile` + `customerDetails` + `consumptionProfiles[0]` |
| Tariff category change | Re-issue with updated `consumptionProfiles`; revoke the previous credential |
| Rooftop solar / DER commissioned | Re-issue with added `generationProfiles` entry; revoke previous |
| Battery commissioned | Re-issue with added `storageProfiles` entry; revoke previous |
| Asset decommissioned | Re-issue with the asset removed; revoke previous |
| Disconnection / closure | Revoke; do not re-issue |

Each re-issue gets a new `id` (URN UUID); the consumer DID (`credentialSubject.id`) stays the same so a verifier holding multiple historical credentials can still tie them to the same person.

---

## Implementing in OpenCred

OpenCred can load the schema in three ways:

1. **Built-in schema ID** — the published image ships `electricity/v1` as a built-in schema. Pass `schemaId: "electricity/v1"`. This is the **recommended path**.
2. **Inline schema** — supply the JSON Schema body as `inlineSchema`.
3. **Inline context** — supply the JSON-LD `@context` fragment as `inlineContext`.

Worked curls are in [Issuing Credentials](./issuance.md).

### Three gotchas first-time issuers hit

The OpenCred bootcamp's [§6d worked example](https://opencred.gitbook.io/docs/bootcamp/local-docker#6d-try-a-different-built-in-schema-electricityv1) calls out three field-shape traps that catch nearly every first attempt at `electricity/v1`. They are all already captured in the field tables on this page, but pulling them out here saves a debugging round:

1. **`country` is an object, not a string.** Beckn's `installationAddress.country` is `{ name?: string, code: string }` with `code` matching ISO 3166-1 alpha-2 (`^[A-Z]{2}$`). Passing `"country": "IN"` returns `400 SCHEMA_VALIDATION_ERROR` with `must be object`. The correct shape is `"country": { "name": "India", "code": "IN" }`.
2. **`serviceConnectionDate` is `date-time`, not `date`.** Pass a full ISO 8601 timestamp with timezone offset (e.g. `"2024-04-15T00:00:00+05:30"` or `"2024-04-15T00:00:00Z"`). A bare date (`"2024-04-15"`) returns `must match format "date-time"`.
3. **`meterType` is an enum.** Valid values are exactly the [meterType enum](#metertype-enum) table above — `AMR`, `AMI`, `Electromechanical`, `Forward`, `Reverse`, `Bidirectional`, `Prepaid`, `NetMeter`, `Other`. Anything else is rejected at the schema-validation step. (Beckn's upstream lists the same set; the IES mirror inherits it.)

`customerProfile` is the only required block under `credentialSubject`. `customerDetails`, `consumptionProfiles`, `generationProfiles`, and `storageProfiles` are all optional — you can issue a minimal credential with just `customerProfile` while you debug the rest of your CIS mapping.

---

## References

- [`/schemas/ElectricityCredential/v1.0/`](../schemas/ElectricityCredential/v1.0/README.md) — mirrored schema files in this repo (`schema.json`, `context.jsonld`, `attributes.yaml`, `examples/`)
- Repository root: [https://github.com/India-Energy-Stack/ies-accelerator](https://github.com/India-Energy-Stack/ies-accelerator)
- [Beckn DEG `ElectricityCredential` v1.0 — upstream](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential/v1.0)
- [W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [beckn Location schema](https://github.com/beckn/protocol-specifications/blob/master/schema/Location.yaml) — basis for `installationAddress`
- [Green Button / ESPI](https://www.energy.gov/data/green-button) — basis for `meterType` enum
