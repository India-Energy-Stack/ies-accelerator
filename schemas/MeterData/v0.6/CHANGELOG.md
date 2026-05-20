# MeterData v0.6 Changelog

Version 0.6 introduces a major structural refactor to the `MeterData` schema. It unifies time representations, reduces redundant payload properties, reinstates Time of Use (ToU) buckets with an improved grouping structure, and formalizes a **Universal Dual-Form Representation** (Form A - Elaborated and Form B - Compact) across all profiles.

---

## Summary of Changes

### 1. Unified Time Terminology
Previously, time windows and execution timestamps were fragmented (`billingPeriod`, `coveragePeriod`, `intervalPeriod`, `capturedAt`, `timestamp`).
* All period objects are unified into **`timePeriod`**.
* The `timePeriod` object strictly requires a `start` timestamp (ISO-8601 with timezone offset) and a **`duration`** (ISO-8601 duration), perfectly aligning with standard IEC/OpenADR patterns (e.g., `duration: "P1M"`, `duration: "PT30M"`).
* All single point-in-time execution markers have been unified to the single property **`timestamp`** (replacing `capturedAt`).

### 2. Deprecation of Explicit Units & Phases from Inline Readings
To reduce transmission bloat, inline `unit` and `phase` fields have been entirely removed from the reading schemas. Consumers are mandated to derive physical semantics (e.g. Volts, Amperes, Phase R/Y/B) from the canonical `OBISMapping.json` definitions using the provided `readingTypeRef` (OBIS or Short Codes).

### 3. Restructured Time of Use (ToU) Buckets
`touBuckets` inside `BillingProfile` has been reintroduced and structurally optimized:
* Instead of keeping `zone` inside each reading object, readings are now grouped under a parent **`TouBucket`** object containing a `zone` key and a nested `readings` array of `Reading` objects.
* Redundant `zone` fields are removed from the generic `Reading` model, ensuring a cleaner nested structure.

### 4. Billing Register Metadata Support
Three billing register properties are added back to the `Reading` object to support Indian utility billing calculations without data loss:
* `openingValue` (number)
* `closingValue` (number)
* `integrationPeriod` (ISO-8601 duration)

---

## Detailed Payload Examples

### Form A: Elaborated Representation (`readings` / `touBuckets`)
Ideal for sparse registers (e.g. `BillingProfile` or `InstantaneousProfile`). Telemetry is presented as a list of discrete `Reading` objects containing inline values, timestamps, and register details.

```json
{
  "@context": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterData/v0.6/context.jsonld",
  "@type": "BillingProfile",
  "profileType": "BILLING",
  "customerRefs": [
    { "scheme": "CONSUMER_NUMBER", "value": "RR-1234" }
  ],
  "meterRefs": [
    { "scheme": "METER_SERIAL", "value": "BESCOM-SM-2025-654321" }
  ],
  "timePeriod": {  "start": "2026-04-01T00:00:00+05:30", "duration": "P1M"  },
  "billNumber": "BESCOM-RR-1234-202604",
  "billDate": "2026-05-01",
  "dueDate": "2026-05-21",
  "currency": "INR",
  "amountDue": 4287.5,
  "readings": [
    {
      "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.8.0.255" },
      "value": 412.5,
      "openingValue": 18432.5,
      "closingValue": 18845.0
    },
    {
      "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.6.0.255" },
      "value": 8.42,
      "occurredAt": "2026-04-23T19:30:00+05:30",
      "integrationPeriod": "PT30M"
    }
  ],
  "touBuckets": [
    {
      "zone": 1,
      "readings": [
        {
          "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.8.1.255" },
          "value": 138.2
        }
      ]
    }
  ]
}
```

### Form B: Compact Representation (`intervalBlocks` -> `intervals` + `overrides`)
Ideal for dense time-series telemetry (e.g. `IntervalProfile` or `DailyProfile`). Descriptors are declared once in `payloadDescriptors`, and data values are transmitted positionally inside numerical matrices (`intervals`). Sparse metadata (timestamps, quality codes) is annotated using the `overrides` array mapping back to the row and column index.

```json
{
  "@context": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterData/v0.6/context.jsonld",
  "@type": "IntervalProfile",
  "profileType": "INTERVAL",
  "customerRefs": [
    { "scheme": "CONSUMER_NUMBER", "value": "RR-1234" }
  ],
  "meterRefs": [
    { "scheme": "METER_SERIAL", "value": "BESCOM-SM-2025-654321" }
  ],
  "timePeriod": {  "start": "2026-05-04T09:00:00+05:30", "duration": "PT2H"  },
  "intervalBlocks": [
    {
      "timePeriod": {  "start": "2026-05-04T09:00:00+05:30", "duration": "PT30M"  },
      "payloadDescriptors": [
        { "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.8.0.255" } },
        { "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.6.0.255" } }
      ],
      "intervals": [
        { "id": 0, "values": [4.82, 9.15] },
        { "id": 1, "values": [5.12, 8.42] }
      ],
      "overrides": [
        {
          "intervalId": 1,
          "descriptorIndex": 1,
          "occurredAt": "2026-05-04T09:45:00+05:30"
        }
      ]
    }
  ]
}
```
