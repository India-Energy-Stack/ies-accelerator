# Phase 4 Documentation: OpenADR Integration (vOpenAdr)

This phase establishes the OpenADR 3.0-compliant schema (`vOpenAdr`), compiles it, migrates the evolved `v0.6` smart meter examples into OpenADR `report` payloads, and implements strict validation checks.

## Changes Made

### 1. Schema Base
- **`schemas/MeterData/vOpenAdr/openadr.yaml`**: The canonical OpenADR 3.0 YAML base specification, defining standard entities (`report`, `resource`, `payloadDescriptor`, `interval`, `intervalPeriod`, etc.).
- **`schemas/MeterData/vOpenAdr/schema.json`**: Compiled Draft 2020-12 JSON Schema for the `report` root payload.

### 2. Compilation and Migration Scripts
- **`scripts/generate_openadr_schema.py`**: Reads `openadr.yaml` and compiles it into the unified Draft 2020-12 `schema.json` with proper internal references mapped to `$defs`.
- **`scripts/migrate_v06_to_openadr.py`**: Migrates v0.6 examples into OpenADR compliant `report` payloads, mapping OBIS codes and categories to corresponding OpenADR `payloadType`s (`USAGE`, `DEMAND`, `VOLTAGE`, etc.) and `readingType`s (`SUM`, `PEAK`, `DIRECT_READ`).

### 3. OpenADR Examples
- **`schemas/MeterData/vOpenAdr/examples/vOpenAdr_Example.json`**: A canonical OpenADR report payload containing converted interval data (copied from migrated `IntervalProfile_UsageMode.json`).
- **`schemas/MeterData/vOpenAdr/examples/IntervalProfile_UsageMode_OpenAdr.json`**: Migrated interval profile.
- **`schemas/MeterData/vOpenAdr/examples/DailyProfile_ReadingMode_OpenAdr.json`**: Migrated daily profile.
- **`schemas/MeterData/vOpenAdr/examples/BillingProfile_Elaborated_OpenAdr.json`**: Migrated billing profile.

### 4. Validation & Parity checks
- **`schemas/MeterData/vOpenAdr/validation/validate_openadr.py`**: Performs structural validation using `schema.json` and strict data loss checks. It verifies that the sum of each telemetry category in the source `v0.6` payload matches the sum of the corresponding telemetry type in the migrated `vOpenAdr` report, ensuring 100% equivalence (zero data loss).
