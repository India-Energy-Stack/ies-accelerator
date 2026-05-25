# MeterData v0.6 Changelog

Version 0.6 introduces a major structural refactor to the `MeterData` schema. It unifies time representations, reduces redundant payload properties, reinstates Time of Use (ToU) buckets with an improved grouping structure, and formalizes a **Universal Dual-Form Representation** (Form A - Elaborated and Form B - Compact) across all profiles.

---

## Schema Structural Changes

### 1. Unified Time Representation
Previously, time windows and execution timestamps were fragmented across different profiles (`billingPeriod`, `coveragePeriod`, `intervalPeriod`, `capturedAt`, `timestamp`).
* **Time Periods**: All period and coverage objects (`billingPeriod`, `coveragePeriod`, `intervalPeriod`) are replaced by the unified **`timePeriod`** object.
  * In `v0.5`, time intervals were defined as `TimeInterval` (with `start` and `end`).
  * In `v0.6`, `timePeriod` uses the `TimePeriod` definition, requiring `start` (timestamp) and **`duration`** (ISO-8601 duration), aligning with standard IEC/OpenADR telemetry patterns (e.g. `P1M`, `PT30M`, `PT1H`).
* **Execution Timestamp**: All execution markers (`capturedAt`, `timestamp`) are unified to **`timestamp`** (replacing `capturedAt` in instantaneous profiles).

### 2. Removal of Explicit Units & Phases from Readings
To reduce payload transmission size, inline `unit` and `phase` fields have been entirely removed from the schemas of reading records. Consumers must resolve these physical semantics using the `readingTypeRef` (OBIS or Short Codes) against the canonical lookup map.

### 3. Unified `Reading` Model & Restructured Register Fields
The legacy `TotalsEntry`, `InstantaneousValue`, and ToU readings are unified under a single **`Reading`** schema:
* Supported properties: `readingTypeRef`, `value`, `openingValue`, `closingValue`, `integrationPeriod`, `occurredAt`, `validationStatus`, `source`, `changeMethod`, `failCode`.
* Removed redundant inline properties: `unit`, `phase`, and `zone` from the individual reading.
* **Restructured Time of Use (ToU) Buckets**: Legacy flat `touBuckets` (where each reading record had its own `zone` property) are restructured into a nested **`TouBucket`** structure. A `TouBucket` contains a single parent `zone` (integer) and an array of nested `readings` (array of `Reading` objects), grouping multiple readings under a specific zone.

#### 4. Flat OpenADR-Aligned Compact Form (`intervalPeriod` & `intervals`)
* **Deprecation of IntervalBlocks**: The previous nested `intervalBlocks` array is completely removed. Profiles now directly contain:
  - **`payloadDescriptorSet`**: A top-level metadata definition specifying valid payload descriptors and compact sequences.
  - **`compactSequenceRef`**: A reference to the active named positional sequence.
  - **`intervalPeriod`**: Default starting timestamp and duration for the profile's intervals.
  - **`intervals`**: A flat array of interval objects containing sequential data.
* **Interval-Level Overrides & Cadence Inheritance**: `overrides` are now nested directly within individual `Interval` objects inside the flat `intervals` array. Individual intervals automatically inherit and calculate start times/durations from `intervalPeriod` unless locally overridden.
* **Telemetry Mode Categorization**: Introduced the `TelemetryMode` classification (`READING` vs `USAGE`) in `ReadingDefinition` and `PayloadDescriptor` to cleanly distinguish cumulative counters or snapshots from interval deltas.

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
      "reportedMode": "READING",
      "value": 412.5,
      "openingValue": 18432.5,
      "closingValue": 18845.0
    },
    {
      "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.6.0.255" },
      "reportedMode": "USAGE",
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
          "reportedMode": "READING",
          "value": 138.2
        }
      ]
    }
  ]
}
```

### Form B: Flat OpenADR-Aligned Compact Representation (`intervals` + `payloadDescriptorSet`)
Ideal for dense time-series telemetry (e.g. `IntervalProfile` or `DailyProfile`). Descriptors and compact sequences are declared at the profile root in `payloadDescriptorSet`, and data values are transmitted positionally inside numerical matrices (`intervals`). Overrides are nested directly within the targeted `Interval` row.

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
  "payloadDescriptorSet": {
    "name": "IntervalLoadSurveySet",
    "payloadDescriptors": [
      { "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.29.0.255" }, "reportedMode": "USAGE" },
      { "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.6.0.255" }, "reportedMode": "USAGE" }
    ],
    "compactSequences": [
      {
        "name": "IntervalEnergySeq",
        "sequenceItems": [
          { "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.29.0.255" }, "reportedMode": "USAGE" },
          { "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.6.0.255" }, "reportedMode": "USAGE" }
        ]
      }
    ]
  },
  "compactSequenceRef": "IntervalEnergySeq",
  "intervalPeriod": { "start": "2026-05-04T09:00:00+05:30", "duration": "PT30M" },
  "intervals": [
    { "id": 0, "payloads": [4.82, 9.15] },
    {
      "id": 1, 
      "payloads": [5.12, 8.42],
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
