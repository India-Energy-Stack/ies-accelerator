# Phase 3 Documentation: Documentation & JSON-LD Compilation

This phase produces rich documentation explaining the schema evolution and recompiles all semantic web contexts and ontologies.

## Changes Made

### 1. New Documentation Artifacts
- **`schemas/MeterData/v0.6/ReferenceGuide.md`**: Provides standard OBIS mappings, category classifications, telemetry modes (`READING` vs `USAGE`), and OpenADR-aligned cadence rules.
- **`schemas/MeterData/v0.6/UserGuide.md`**: Outlines integrating the schema within Head-End Systems (HES), Meter Data Management (MDM), and Billing systems, including diagrams and implementation rules.

### 2. Updated References
- **`schemas/MeterData/v0.6/README.md`**: Updated to cover the reading vs usage paradigms, flat intervals representation, and overrides. Added warnings against creating custom OBIS or Short labels.
- **`schemas/MeterData/v0.6/CHANGELOG.md`**: Expanded to detail the OpenADR-aligned flat matrix representation and mode categorization.
- **`schemas/MeterDataRequest/v0.5/README.md`**: Updated to document requesting specific values and modes via `ProfileRequest` in `includeDetails`.

### 3. JSON-LD Compilation
- recompiled `context.jsonld` and `vocab.jsonld` for both `MeterData/v0.6` and `MeterDataRequest/v0.5` to ensure semantic alignment.
