### Summary of Changes

This Pull Request implements the MeterData v0.6 schema refactoring, short code examples migration, and MeterDataRequest v0.5 compatibility updates:

1. **MeterData v0.6 Schema Refactoring**:
   - **Billing Profile Split**: Split the legacy billing profile into `MonthlyProfile` (representing physical cumulative registers and Time-of-Use buckets expected from the meter on a monthly basis) and `BillDetails` (out-of-band computed commercial billing amount, period, and prepayment balance).
   - **OBISMapping Refactoring**: Transformed the mapping dictionary in `OBISMapping.json` into an array of records using `obis` as the key. Added profiles list for each code.
   - **Alarm Registers**: Added support for standard alarm registers (OBIS `0.0.97.98.0.255`) and mapped standard alarm flags (neutral disturbance, voltage sag, cover open, etc.) to the new `AlarmProfile` schema.
   - **Reduced Payload Size**: Removed physical semantics (unit, phase) from individual readings to reduce transmission bloat, delegating resolution to `OBISMapping.json`.

2. **Permissive Schema Compiler & Lossless Validation**:
   - Implemented `scripts/generate_schema_permissive.py` to correctly compile schemas, contexts, and vocabularies while supporting recursive flatting of nested schemas (e.g. `BaseTelemetryProfile`).
   - Verified that zero properties or OBIS codes were lost during migration from v0.5 to v0.6.

3. **Short Code Focus & README Examples Index**:
   - Updated all single-profile examples under `schemas/MeterData/v0.6/examples/` to use human-readable short codes (e.g., `"kWh imp"`) rather than raw OBIS strings.
   - Added a "Example Payloads and Scenarios" index in `README.md` containing 1-line statements linking directly to each of the 11 single-profile and bulk datasets.

4. **MeterDataRequest v0.6 Integration**:
   - Updated `includeDetails` enum in `attributes.yaml` to match the new v0.6 profiles (`MonthlyProfile`, `BillDetails`, `AlarmProfile`).
   - Documented the schema relationship: `MeterData` (what telemetry looks like) is complemented by `MeterDataRequest` (what meters, what data, for how long).
   - Created three distinct query scenarios as standalone JSON files under `examples/` and linked them in the README:
     1. **Credential Embedding** (`MeterDataRequest_FeederAllowance.json`): A DISCOM shares with a TSP to authorize interval data only for children of a feeder.
     2. **Provider Capabilities** (`MeterDataRequest_MDM_Capability.json` & `MeterDataRequest_Billing_Capability.json`): Advertising what queries an MDM vs. a Billing system supports.
     3. **Query Filters** (`MeterDataRequest_DigestCredentialFilter.json`): A query filter for retrieving customer profile, bills, and monthly/daily telemetry to compile a Meter Digest.
