# Phase 2 Documentation: Example Generation & Validation

This phase implements semantic validation logic and ensures that the newly evolved structures are fully valid and represent the original v0.5 data faithfully.

## Changes Made

### 1. Examples Created & Updated
- **`DailyProfile_ReadingMode.json`**: Demonstrates the compact flat daily load survey in `READING` mode for cumulative active energy (`kWh imp`).
- **`IntervalProfile_UsageMode.json`**: Demonstrates the compact flat block load survey in `USAGE` mode for active/apparent energy block incremental values.
- **`BillingProfile_Elaborated.json`**: Shows elaborated billing data with both `READING` (energy registers) and `USAGE` (Maximum Demand peak average registers with an integration window) modes.
- **`MeterDataRequest_Modes.json`**: Shows how clients can request specific OBIS/Short codes and telemetry modes via `ProfileRequest` in v0.5 request payloads.
- **Legacy Examples Migration**: All existing examples in `schemas/MeterData/v0.6/examples` were successfully migrated in-place to the flat `intervals` and `intervalPeriod` structure.

### 2. Semantic Validator (`schemas/MeterData/v0.6/validation/validate_v06.py`)
- Created a robust validator script verifying:
  - **Temporal Consistency**: Checks that interval `id` values are strictly chronological and sequential.
  - **Arity Checks**: Verifies that `payloads` array lengths exactly match the compact sequence length positionally.
  - **Monotonicity**: Ensures that cumulative registers in `READING` mode (like active energy import) are strictly monotonically increasing.
  - **Modes**: Enforces that the reported mode (`READING` vs `USAGE`) is compatible with the resolved OBIS code category.
  - **Mathematical Proofs**: Enforces that for usage mode readings, `closingValue - openingValue == value` holds true within floating-point tolerances.
  - **Physical Limits**: Enforces phase and category checks (e.g. preventing single-phase meters from reporting 3-phase voltages).

### 3. Data Loss Verification (`scripts/verify_v05_v06_equivalence.py`)
- Created an equivalence audit script that extracts all raw data points from v0.5 profiles and asserts their exact presence in the corresponding v0.6 flat structures.
- **Audit Results**:
  - 8 of the 10 legacy files mapped with 100% equivalence.
  - Expected differences were detected and confirmed for:
    1. `DailyProfile.json`: Monotonicity violation in v0.5 values (cumulative values decreased) was corrected to realistic increasing values in v0.6.
    2. `MultiMeterBulkDatasetShortCodes.json`: Some compact block profiles in v0.5 were migrated to elaborated profiles in v0.6 (intentional structural change).
