# MeterData v0.6 Changelog

Version 0.6 introduces a monumental architectural evolution to the `MeterData` schemas. The primary focus of this release is the centralization of metadata, hyper-optimization of dense telemetry arrays (compact sequences), and the enforcement of strict inheritance models. These changes collectively enable "Data Descriptor Engine" validation while reducing JSON payload sizes drastically.

---

## What's New in v0.6 (vs 0.5)

### 1. Removal of `MeterDataset` & Array-based Data Descriptors
The telemetry architecture has transitioned away from the rigid `MeterDataset` envelope.
* Root payloads are now simply JSON arrays (or single objects for individual profiles).
* Rather than wrapping data in a proprietary container, metadata (units, flow direction, labels) and column definitions are declared as an independent `PayloadDescriptorProfile` within the array.
* Data profiles (like `IntervalProfile` or `DailyProfile`) reference these definitions via `payloadDescriptorSetRef`.

### 2. Hyper-Optimized `CompactSequence` with Multi-Type Payloads
The compact representation (`IntervalProfile` and `DailyProfile`) has been fundamentally reimagined:
* **The `attribute` Enum**: `SequenceItem` definitions in the `compactSequences` now map directly to specific reading attributes (e.g., `value`, `occurredAt`, `openingValue`, `validationStatus`).
* **Multi-Type `payloads`**: The numerical `values` array in intervals has been replaced by `payloads` which supports both `number` and `string`. 
* **Targeted use of Overrides**: Because `payloads` can mix numbers (for energy) and strings (for timestamps or validation codes), metadata that previously required verbose sparse `overrides` arrays is now mapped as a native, dense column in the sequence matrix. The `overrides` array is now strictly retained for **quality deviance indication** (e.g., specific estimation methods `changeMethod` and failure codes `failCode` on a single bad interval), rather than routine timestamps.

### 3. Simplification of Identifiers (Short Codes & IES codes)
* The verbose `readingTypeRef` object (`{"scheme": "OBIS", "value": "..."}`) has been replaced by a flat **`readingType`** string across all schemas.
* Short codes (e.g., `"kWh imp"`, `"V_1P"`) are now heavily favored over raw OBIS codes for readability and bandwidth savings.
* **Resolution Flow**: Payload parsers first resolve semantics against the **local payload descriptor** inside the dataset. For strict mathematical compliance, this local descriptor is then validated against the central `IES codes.json` registry. Payload descriptors now optionally include an `obis` property for direct canonical linkage when a short code is used.

### 4. Strict Composition-Based Inheritance
The inheritance model in `attributes.yaml` has been strictly refactored:
* **`BaseProfile`** has been purged of all telemetry-specific properties (`readings`, `intervals`, `timestamp`, `timePeriod`). It now exclusively contains routing and identification context (`customerRefs`, `meterRefs`, etc.).
* Derived profiles inherit from `BaseProfile` via JSON Schema `allOf` and strictly define only their relevant properties (e.g., `IntervalProfile` only permits `intervals` and `compactSequenceRef`, never `readings`).

### 5. Transition to `IES codes.json` & Registry Enforcement
* The central registry `OBISMapping.json` used in version 0.5 has been replaced by **`IES codes.json`** in version 0.6.
* The validator engine (`validator.py`) has been upgraded to enforce **Data Descriptor Engine semantics** using the new registry.
* Any inline descriptor definitions must mathematically and physically align with the canonical `IES codes.json` registry. The validator dynamically asserts matrix arity and column data types across the entire dataset.

---

## Detailed Payload Examples

### Array-Based Profile Exchange

#### Monthly Profile Example:
```json
[
  {
    "@type": "PayloadDescriptorProfile",
    "profileType": "DESCRIPTOR",
    "id": "DESC-DAILY",
  "payloadDescriptorSets": [
    {
      "name": "DailyLoadSurveySet",
      "payloadDescriptors": [
        {
          "readingType": "kWh imp",
          "name": "Active Energy Import",
          "unit": "kWh",
          "flowDirection": "IMPORT",
          "reportedMode": "READING"
        },
        {
          "readingType": "MD kW",
          "name": "Maximum Demand Active Power",
          "unit": "kW",
          "flowDirection": "IMPORT",
          "reportedMode": "USAGE"
        }
      ],
      "compactSequences": [
        {
          "name": "DailyEnergySeq",
          "sequenceItems": [
            { "readingType": "kWh imp", "attribute": "value", "reportedMode": "READING" },
            { "readingType": "MD kW", "attribute": "value", "reportedMode": "USAGE" },
            { "readingType": "MD kW", "attribute": "occurredAt", "reportedMode": "USAGE" }
          ]
        }
      ]
  },
  {
    "@type": "DailyProfile",
    "profileType": "DAILY",
    "customerRefs": [
      { "scheme": "CONSUMER_NUMBER", "value": "RR-1234" }
    ],
    "meterRefs": [
      { "scheme": "METER_SERIAL", "value": "BESCOM-SM-2025-654321" }
    ],
    "payloadDescriptorSetRef": "DailyLoadSurveySet",
    "intervalPeriod": {
      "start": "2026-05-04T00:00:00+05:30",
      "duration": "P1D"
    },
    "intervals": [
      {
        "id": 0,
        "payloads": [
          1000.0,
          8.42,
          "2026-05-04T19:30:00+05:30"
        ]
      }
    ]
  }
]
```
