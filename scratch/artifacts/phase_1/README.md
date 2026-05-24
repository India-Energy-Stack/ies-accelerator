# Phase 1 Documentation: Structure Setup and Schema Design

This phase establishes the foundational structure for the smart meter schema evolution, implementing the OpenADR-aligned flat interval representation and the reading/usage telemetry modes.

## Changes Made

### 1. `schemas/MeterData/v0.6`
- **`attributes.yaml`**:
  - Replaced the nested `intervalBlocks` and `timePeriod` structure with a flat OpenADR-aligned structure containing a top-level `intervalPeriod` (default start and duration) and `intervals` array.
  - Added new schemas: `TelemetryMode` (enum for `READING` vs `USAGE`), `ReadingDefinition` (static mapping defining default and supported modes), `PayloadDescriptorSet` (named sets containing payload descriptors and compact sequences), `CompactSequence` (named positional list of sequence items), `SequenceItem`, and `IntervalPeriod`/`Interval`.
  - Updated `Reading` to support `reportedMode`.
- **Generated files (`schema.json`, `context.jsonld`, `vocab.jsonld`)**: Compiled successfully using the generation script to reflect these structural updates.

### 2. `schemas/MeterDataRequest/v0.5`
- **`attributes.yaml`**:
  - Added `TelemetryMode` and `ProfileRequest` schemas.
  - Updated `includeDetails` to accept `ProfileRequest` objects instead of simple string constants, allowing clients to request specific telemetry items (`values`) and modes (`requestedMode`).
- **Generated files (`schema.json`, `context.jsonld`, `vocab.jsonld`)**: Compiled successfully.

### 3. Validation Boilerplate
- Created placeholder scripts for validation:
  - `schemas/MeterData/v0.6/validation/validate_v06.py`
  - `schemas/MeterData/vOpenAdr/validation/validate_openadr.py`
