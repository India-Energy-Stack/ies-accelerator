# MeterData v0.6 Changelog

Version 0.6 introduces a major structural refactor to the `MeterData` schema. It unifies time representations, reduces redundant payload properties, reinstates Time of Use (ToU) buckets with an improved grouping structure, formalizes a **Universal Dual-Form Representation** (Form A - Elaborated and Form B - Compact) across all profiles, introduces prepayment balance attributes, and implements modular composition-based profile schemas alongside real-time active alarms.

---

## What's New in v0.6 (Latest Updates)

### 1. Split of Billing Profile into Monthly Profile and Bill Details
The legacy `BillingProfile` has been separated into:
* **`MonthlyProfile`**: Represents reset data expected from the physical meter on a monthly basis (cumulative energy registers, Time-of-Use buckets, and Maximum Demand).
* **`BillDetails`**: Represents utility billing and commercial details computed out-of-band (billing amount, currency, bill number, bill date, due date, payment status, and prepaid balance).

### 2. Composition-Based Inheritance for Profiles
Introduced a unified base schema **`BaseTelemetryProfile`** containing standard attributes (`customerRefs`, `meterRefs`, `serviceDeliveryPointRefs`, `timePeriod`, `readings`, and `intervalBlocks`). The derived profiles (`IntervalProfile`, `DailyProfile`, `MonthlyProfile`, and `InstantaneousProfile`) are refactored to inherit from `BaseTelemetryProfile` using JSON Schema `allOf`. This ensures optimal reuse, consistency, and a modular schema design.

### 3. Dedicated Alarm Profile & Real-Time Active Alarms
Added **`AlarmProfile`** (`profileType: "ALARM"`) and **`MeterAlarm`** types to capture active real-time conditions (e.g. voltage sag, overload, cover open, neutral disturbance) on the meter, complementing the periodic batch `EventProfile`.

### 4. OBIS Mapping Refactoring & Alarm Register mapping
* Transformed `"codes"` in `OBISMapping.json` from a key-value dictionary to a record array structure with the key `"obis"`.
* Added a list of target `"profiles"` to each code record to specify where it is valid.
* Added an `"attributes"` array for peak-occurrence metadata (e.g., peak demand timestamp) on Maximum Demand registers.
* Added standard Alarm Register OBIS code `0.0.97.98.0.255` and a standard alarm taxonomy mapping block under `"alarms"`.

### 5. Permissive Schema Compiler
Implemented a schema compiler `scripts/generate_schema_permissive.py` to handle nested `allOf` and `$ref` inheritances, resolving flat properties correctly during context and vocab compilation.

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

### 4. Compact Form Refinements (`IntervalBlock`)
* **Cadence Consolidation**: Removed `intervalLength` from `IntervalBlock`. The block cadence is now derived from `timePeriod.duration`.
* **Overrides Renaming & Expansion**: `qualityOverrides` has been renamed to **`overrides`** (referencing the `Override` component):
  * In `v0.5`, `QualityOverride` required `validationStatus`. In `v0.6`, `Override` requires `descriptorIndex` (referencing the column in the matrix).
  * Added optional fields `occurredAt` and `zone` inside the `Override` model, enabling sparse override of timestamps and zones inside the compact matrix rows without needing inline elaborated records.

### 5. Universal Dual-Form Support across Profiles
Every telemetry profile (Billing, Daily, Interval, Instantaneous, Event) now supports both paradigms:
* **Form A (Elaborated)**: Uses the `readings` array of `Reading` objects.
* **Form B (Compact)**: Uses the `intervalBlocks` array of `IntervalBlock` objects.
* To support both forms, `intervalBlocks` is no longer a required field in `IntervalProfile` and `DailyProfile`, allowing them to use `readings` directly if desired.

---

## Detailed Payload Examples

### Form A: Elaborated Representation (`readings` / `touBuckets`)
Ideal for sparse registers (e.g. `MonthlyProfile`, `BillDetails`, or `InstantaneousProfile`). Telemetry is presented as a list of discrete `Reading` objects containing inline values, timestamps, and register details.

#### Monthly Profile Example:
```json
{
  "@context": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterData/v0.6/context.jsonld",
  "@type": "MonthlyProfile",
  "profileType": "MONTHLY",
  "customerRefs": [
    { "scheme": "CONSUMER_NUMBER", "value": "RR-1234" }
  ],
  "meterRefs": [
    { "scheme": "METER_SERIAL", "value": "BESCOM-SM-2025-654321" }
  ],
  "timePeriod": {  "start": "2026-04-01T00:00:00+05:30", "duration": "P1M"  },
  "readings": [
    {
      "readingTypeRef": { "scheme": "OBIS", "value": "1.0.1.8.0.255" },
      "value": 412.5,
      "openingValue": 18432.5,
      "closingValue": 18845.0
    },
    {
      "readingTypeRef": { "scheme": "OBIS", "value": "1.0.9.8.0.255" },
      "value": 421.8,
      "openingValue": 18715.4,
      "closingValue": 19137.2
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

#### Bill Details Example:
```json
{
  "@context": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterData/v0.6/context.jsonld",
  "@type": "BillDetails",
  "profileType": "BILL_DETAILS",
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
  "amountDue": 4287.50,
  "prepaidBalance": 500.00,
  "paymentStatus": "UNPAID"
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
