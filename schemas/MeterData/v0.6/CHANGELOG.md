# MeterData v0.6 Changelog

Version 0.6 introduces a major structural refactor to the `MeterData` schema, standardizing telemetry payloads, simplifying time terminology, and formalizing a **Universal Dual-Form Representation** that drastically increases flexibility.

## 1. Unified Time Terminology
Previously, time windows and execution timestamps were fragmented (`billingPeriod`, `coveragePeriod`, `intervalPeriod`, `capturedAt`, `timestamp`). 

**Changes:**
- All period objects have been unified into `timePeriod`, requiring only `start` and `end`.
- The redundant `duration` property has been removed.
- All point-in-time execution markers have been unified to `timestamp`.

## 2. Deprecation of Explicit Units & Phases
To reduce payload bloat, the inline `unit` and `phase` properties have been entirely removed from the reading objects. Consumers must now strictly rely on the canonical `OBISMapping.json` dictionary to infer these physical semantics based on the `readingTypeRef` (e.g. `OBIS` or `SHORT_CODE`).

## 3. Universal Dual-Form Representation
Every telemetry profile (Billing, Daily, Interval, Instantaneous, Event) now officially supports two structural paradigms for presenting data: **Form A (Elaborated)** and **Form B (Compact)**. 

### Form A: Elaborated Representation (`readings`)
Ideal for sparse reads (e.g. `InstantaneousProfile` or `BillingProfile`). Data is presented as an array of discrete `Reading` objects, allowing complex metadata (zones, validation status, timestamps) to be annotated directly inline.

**Example: Billing Profile with Inline Max Demand and Quality**
```json
{
  "@context": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterData/v0.6/context.jsonld",
  "@type": "BillingProfile",
  "timePeriod": {
    "start": "2026-04-01T00:00:00+05:30",
    "end": "2026-05-01T00:00:00+05:30"
  },
  "readings": [
    {
      "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh imp" },
      "value": 1500.5
    },
    {
      "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh TZ1" },
      "value": 450.2,
      "zone": 1
    },
    {
      "readingTypeRef": { "scheme": "SHORT_CODE", "value": "MD kW" },
      "value": 15.2,
      "occurredAt": "2026-04-23T19:30:00+05:30"
    },
    {
      "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kvarh Q1" },
      "value": 12.0,
      "validationStatus": "ESTIMATED"
    }
  ]
}
```

### Form B: Compact Representation (`intervals` + `overrides`)
Ideal for dense time-series telemetry (e.g. 15-minute `IntervalProfile`). Descriptors are hoisted to an array, and data is transmitted as highly-efficient numerical arrays (`IntervalRow`). 

**Changes:**
- `qualityOverrides` has been renamed and expanded to **`overrides`**.
- You can now use `overrides` to inject exact timestamps (like Max Demand `occurredAt`) or `zone` flags directly into specific matrix cells.

**Example: Interval Profile with Sparse Quality and Max Demand Overrides**
```json
{
  "@context": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterData/v0.6/context.jsonld",
  "@type": "IntervalProfile",
  "intervalLength": "PT30M",
  "payloadDescriptors": [
    { "readingTypeRef": { "scheme": "SHORT_CODE", "value": "kWh imp block" } },
    { "readingTypeRef": { "scheme": "SHORT_CODE", "value": "MD kW" } }
  ],
  "intervals": [
    { "id": 0, "values": [12.5, 4.2] },
    { "id": 1, "values": [14.0, 5.1] }
  ],
  "overrides": [
    {
      "intervalId": 1,
      "descriptorIndex": 1,
      "occurredAt": "2026-05-18T14:30:00+05:30"
    },
    {
      "intervalId": 0,
      "descriptorIndex": 0,
      "validationStatus": "ESTIMATED"
    }
  ]
}
```
