# MeterData v0.6 Changelog

Version 0.6 introduces a monumental architectural evolution to the `MeterData` schemas. The primary focus of this release is the centralization of metadata, hyper-optimization of dense telemetry arrays (compact sequences), and the enforcement of strict inheritance models. These changes collectively enable "Data Descriptor Engine" validation while reducing JSON payload sizes drastically.

---

## What's New in v0.6 (vs 0.5)

### 1. The `MeterDataset` Envelope & Centralized Metadata
The telemetry architecture has transitioned from standalone independent profiles to a unified **`MeterDataset`** envelope. 
* A `MeterDataset` contains two primary collections: `payloadDescriptorSets` and `data` (which houses the profiles).
* Rather than repeating metadata across every profile, metadata (units, flow direction, labels) and column definitions are declared **once** at the root of the dataset in `payloadDescriptorSets`.
* Individual profiles now simply reference these central definitions using `compactSequenceRef`.

### 2. Hyper-Optimized `CompactSequence` with Multi-Type Payloads
The compact representation (`IntervalProfile` and `DailyProfile`) has been fundamentally reimagined:
* **The `attribute` Enum**: `SequenceItem` definitions in the `compactSequences` now map directly to specific reading attributes (e.g., `value`, `occurredAt`, `openingValue`, `validationStatus`).
* **Multi-Type `payloads`**: The numerical `values` array in intervals has been replaced by `payloads` which supports both `number` and `string`. 
* **Deprecation of Sparse Overrides**: Because `payloads` can mix numbers (for energy) and strings (for timestamps or validation codes), metadata that previously required verbose sparse `overrides` arrays is now mapped as a native, dense column in the sequence matrix. The `overrides` array has been largely eliminated in favor of strict matrix arity.

### 3. Simplification of Identifiers (Short Codes)
* The verbose `readingTypeRef` object (`{"scheme": "OBIS", "value": "..."}`) has been replaced by a flat **`readingType`** string across all schemas.
* Short codes (e.g., `"kWh imp"`, `"V_1P"`) are now heavily favored over raw OBIS codes for readability and bandwidth savings, with the system resolving the exact semantics against the central `OBISMapping.json` registry.

### 4. Strict Composition-Based Inheritance
The inheritance model in `attributes.yaml` has been strictly refactored:
* **`BaseProfile`** has been purged of all telemetry-specific properties (`readings`, `intervals`, `timestamp`, `timePeriod`). It now exclusively contains routing and identification context (`customerRefs`, `meterRefs`, etc.).
* Derived profiles inherit from `BaseProfile` via JSON Schema `allOf` and strictly define only their relevant properties (e.g., `IntervalProfile` only permits `intervals` and `compactSequenceRef`, never `readings`).

### 5. `OBISMapping.json` Registry Enforcement
* The validator engine (`validate_v06.py`) has been upgraded to enforce **Data Descriptor Engine semantics**.
* Any inline descriptor definitions must mathematically and physically align with the canonical `OBISMapping.json` registry. The validator dynamically asserts matrix arity and column data types across the entire dataset.

---

## Detailed Payload Examples

### MeterDataset Representation

```json
{
  "@context": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterData/v0.6/context.jsonld",
  "@type": "MeterDataset",
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
    }
  ],
  "data": [
    {
      "@type": "DailyProfile",
      "profileType": "DAILY",
      "customerRefs": [
        { "scheme": "CONSUMER_NUMBER", "value": "RR-1234" }
      ],
      "meterRefs": [
        { "scheme": "METER_SERIAL", "value": "BESCOM-SM-2025-654321" }
      ],
      "compactSequenceRef": "DailyEnergySeq",
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
}
```
