# Consumer Meter Digest Credential

The **Consumer Meter Digest** is a W3C Verifiable Credential 2.0 issued by a DISCOM, on consumer demand, that carries the consumer's own meter readings — either raw OpenADR 3 reports or derived summaries — in a form the consumer can hold in their wallet and share with any third party. It is the credential behind the [Consumer Meter Digest use case](../use-cases/consumer-meter-digest/README.md).

> **Status — draft.** The envelope, `meterReference`, `period`, `granularity`, and `readings` blocks are stable. The `summary` taxonomy is being formalised.
>
> The `readings` block reuses the OpenADR 3 `REPORT` envelope from [`IES_Report`](../use-cases/smart-meter-data-exchange/README.md), which itself is being finalised — see [Smart Meter Data Exchange § Open Items](../use-cases/smart-meter-data-exchange/README.md#open-items).

---

## What's Different From Other Credentials

`CustomerCredential` and `ConsumerEnergyPassport` attest to **slow-changing facts** about the meter and its assets. The Meter Digest attests to **a snapshot of readings**. Implications:

| Concern | Customer / Passport credentials | Consumer Meter Digest |
|---|---|---|
| Issued | Once at onboarding; re-issued on material change | On consumer demand, freshly each time |
| Lifespan (`validUntil`) | Years | Hours to days — readings are a point-in-time snapshot |
| Revocation | Common (asset change, disconnection) | Rare — Digests typically expire faster than they would need revocation |
| Holder action | Passive (issued and pushed) | **Active** (consumer requests it for a specific period) |
| Content | Slow-changing identity & asset facts | Time-bounded readings or derived summaries |

A DISCOM that already runs OpenCred for the other two credentials issues Digests from the same instance — only the schema, the trigger, and the short `validUntil` differ.

---

## Common Envelope

Same as [`CustomerCredential`](./schemas.md#common-envelope). The `type` array carries `"ConsumerMeterDigest"`:

```json
"type": ["VerifiableCredential", "ConsumerMeterDigest"]
```

`validFrom` is the issuance time; `validUntil` is typically `validFrom + 24h` to `validFrom + 7d` depending on the use case (loan applications often want fresh; subsidy portals tolerate a week).

---

## credentialSubject

```
ConsumerMeterDigest.credentialSubject
├── id                   (required — consumer DID)
├── meterReference       (required)
├── period               (required)
├── granularity          (required)
├── readings             (one of `readings` or `summary` is required)
├── summary              (one of `readings` or `summary` is required)
└── dataQuality          (required)
```

### meterReference (required)

Links the Digest unambiguously to the meter and the issuing DISCOM.

| Field | Type | Required | Description |
|---|---|---|---|
| `meterNumber` | string | ✓ | Unique meter serial number |
| `customerNumber` | string | ✓ | Consumer account number from DISCOM CIS |
| `discomId` | URI | ✓ | Issuing DISCOM `did:web` — must equal `issuer.id` |
| `meterType` | enum | ✓ | Same enumeration as `customerProfile.meterType` |

### period (required)

| Field | Type | Required | Description |
|---|---|---|---|
| `start` | date-time | ✓ | ISO 8601 start of the readings range, with timezone offset |
| `end` | date-time | ✓ | ISO 8601 end of the range (exclusive) |

### granularity (required)

Enum:

| Value | Meaning |
|---|---|
| `RAW_15M` | Raw 15-minute readings — `readings` block carries the OpenADR `REPORT` |
| `RAW_30M` | Raw 30-minute readings |
| `DAILY` | Daily totals — `readings` block carries `PT24H` intervals |
| `MONTHLY` | Monthly totals — `readings` block carries `P1M` intervals |
| `SUMMARY_MONTHLY_LADDER` | Per-month total kWh + per-month bill — `summary` block populated |
| `SUMMARY_TOD_PROFILE` | Average kWh per hour-of-day across the period — `summary` block populated |
| `SUMMARY_PEAK_DEMAND` | Peak kW per month with timestamps — `summary` block populated |

### readings

When `granularity` ∈ `RAW_15M / RAW_30M / DAILY / MONTHLY`, the `readings` block carries an OpenADR 3 `REPORT` covering the requested period. Same envelope as [`IES_Report`](../use-cases/smart-meter-data-exchange/README.md#the-dataset--ies_report).

### summary

When `granularity` ∈ `SUMMARY_*`, the `summary` block carries the derived aggregate. Field shape varies by summary type:

```json
"summary": {
  "type": "SUMMARY_MONTHLY_LADDER",
  "rows": [
    { "month": "2025-06", "kwh": 412, "billINR": 3185 },
    { "month": "2025-07", "kwh": 478, "billINR": 3942 }
    /* ... */
  ]
}
```

```json
"summary": {
  "type": "SUMMARY_TOD_PROFILE",
  "intervals": [
    { "hour": 0,  "avgKwh": 0.18 },
    { "hour": 1,  "avgKwh": 0.16 },
    /* ... 24 entries ... */
    { "hour": 19, "avgKwh": 0.94 }
  ]
}
```

### dataQuality (required)

| Field | Type | Required | Description |
|---|---|---|---|
| `coveragePercent` | number | ✓ | % of expected intervals that have a reading (100 = no gaps) |
| `estimatedPercent` | number | ✓ | % of returned intervals flagged `ESTIMATED` |
| `flags` | string[] | | Free-form quality flags (`"meter-replaced-mid-period"`, `"clock-skew-2025-08"`) |

A verifier can reject a Digest with low coverage or high estimation without inspecting the readings themselves.

---

## Full Example — Monthly Summary

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/ElectricityCredential/v1.0/context.jsonld"
  ],
  "id": "urn:uuid:9b3c1f0a-2d4e-4ba8-9f1c-1e7a90c8a5d2",
  "type": ["VerifiableCredential", "ConsumerMeterDigest"],
  "issuer": {
    "id": "did:web:ies.tpddl.in",
    "name": "Tata Power Delhi Distribution Limited",
    "idRef": {
      "issuedBy": "did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma",
      "subjectId": "india-energy-stack:tpddl"
    }
  },
  "validFrom": "2026-05-15T10:00:00+05:30",
  "validUntil": "2026-05-22T10:00:00+05:30",
  "credentialStatus": {
    "id": "https://dedi.global/dedi/lookup/tpddl/vc-revocation-registry/9b3c1f0a-2d4e-4ba8-9f1c-1e7a90c8a5d2",
    "type": "dedi",
    "statusPurpose": "revocation",
    "statusListCredential": "https://dedi.global/dedi/query/tpddl/vc-revocation-registry"
  },
  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
    "meterReference": {
      "meterNumber": "MTR-98765432",
      "customerNumber": "TPDDL-2025-001234567",
      "discomId": "did:web:ies.tpddl.in",
      "meterType": "AMI"
    },
    "period": {
      "start": "2025-05-01T00:00:00+05:30",
      "end":   "2026-05-01T00:00:00+05:30"
    },
    "granularity": "SUMMARY_MONTHLY_LADDER",
    "summary": {
      "type": "SUMMARY_MONTHLY_LADDER",
      "rows": [
        { "month": "2025-05", "kwh": 391, "billINR": 2987 },
        { "month": "2025-06", "kwh": 412, "billINR": 3185 },
        { "month": "2025-07", "kwh": 478, "billINR": 3942 },
        { "month": "2025-08", "kwh": 463, "billINR": 3791 },
        { "month": "2025-09", "kwh": 421, "billINR": 3268 },
        { "month": "2025-10", "kwh": 384, "billINR": 2918 },
        { "month": "2025-11", "kwh": 352, "billINR": 2603 },
        { "month": "2025-12", "kwh": 339, "billINR": 2479 },
        { "month": "2026-01", "kwh": 367, "billINR": 2745 },
        { "month": "2026-02", "kwh": 358, "billINR": 2659 },
        { "month": "2026-03", "kwh": 405, "billINR": 3108 },
        { "month": "2026-04", "kwh": 437, "billINR": 3402 }
      ]
    },
    "dataQuality": {
      "coveragePercent": 100,
      "estimatedPercent": 0
    }
  }
}
```

## Full Example — Raw Readings (excerpt)

```json
{
  "credentialSubject": {
    "meterReference": { "meterNumber": "MTR-98765432", /* ... */ },
    "period": { "start": "2026-05-01T00:00:00+05:30", "end": "2026-05-08T00:00:00+05:30" },
    "granularity": "RAW_15M",
    "readings": {
      "objectType": "REPORT",
      "reportID": "rep-MTR-98765432-2026-05-01-week",
      "programID": "consumer-pull",
      "reportPayloadDescriptors": [
        { "payloadType": "USAGE", "readingType": "DIRECT_READ", "units": "KWH" }
      ],
      "resources": [{
        "resourceName": "MTR-98765432",
        "intervalPeriod": { "start": "2026-05-01T00:00:00+05:30", "duration": "PT15M" },
        "intervals": [
          { "id": 0, "payloads": [{ "type": "USAGE", "values": [0.18] }] },
          { "id": 1, "payloads": [{ "type": "USAGE", "values": [0.16] }] }
          /* ... 670 more entries for the week ... */
        ]
      }]
    },
    "dataQuality": { "coveragePercent": 99.4, "estimatedPercent": 0.6 }
  }
}
```

---

## Issuing the Digest

Issuance is on demand: the consumer's wallet sends a Beckn `confirm` to the DISCOM's BPP, the BPP authorises the request against the consumer's `CustomerCredential` or `ConsumerEnergyPassport` presentation, queries MDMS for the period, and calls OpenCred to mint the Digest.

The OpenCred call mirrors the [`CustomerCredential` issuance flow](./issuance.md) with:

1. `type: ["VerifiableCredential", "ConsumerMeterDigest"]`
2. `credentialSubject.id` set to the consumer DID extracted from the inbound presentation
3. A short `validUntil` (1d–7d depending on policy)
4. The MDMS-derived `meterReference`/`period`/`granularity`/`readings`-or-`summary`/`dataQuality` block

Until the canonical schema files land alongside [`/schemas/ElectricityCredential/v1.0/`](../schemas/ElectricityCredential/v1.0/README.md), pass `inlineSchema` to OpenCred derived from this page.

---

## Verifying the Digest

Same flow as [Verification](./verification.md):

1. Resolve the DISCOM's `did:web` from the IES DISCOMs Reference Registry.
2. Verify the `proof` signature locally.
3. Check `credentialStatus` against DeDi for revocation.
4. Confirm `validUntil` is in the future.
5. Read `dataQuality.coveragePercent` and `dataQuality.estimatedPercent` against the verifier's tolerance threshold.
6. Read `readings` or `summary` and proceed.

---

## References

- [Consumer Meter Digest — use case](../use-cases/consumer-meter-digest/README.md)
- [`CustomerCredential` — base schema](./schemas.md)
- [Smart Meter Data Exchange — `IES_Report`](../use-cases/smart-meter-data-exchange/README.md)
- [Issuance](./issuance.md)
- [Verification](./verification.md)
- [OpenADR 3.1.0 Specification](https://www.openadr.org)
