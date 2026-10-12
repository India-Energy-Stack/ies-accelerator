# MeterData v0.6 Semantic Validator

This directory contains the semantic validator for `MeterData v0.6` smart meter telemetry profiles.

## Rules Enforced

The validator performs structural validation against the Draft 2020-12 JSON Schema (`schema.json`) and enforces the following physical and mathematical constraints:

1. **Reading Type Resolution**: All `readingType` parameters (OBIS codes or Short Labels) are resolved against `IES codes.json`.
2. **Profile Type Restrictions**: Verifies that each `readingType` is compatible with the profile shape it is contained in (e.g. `kWh imp` is only allowed in `DAILY` or `MONTHLY` profiles; block registers like `kWh imp block` are strictly restricted to `INTERVAL` profiles).
3. **Descriptor Set Consistency**: Ensures inline OBIS mappings, category classifications, flow directions, and units defined inside `PayloadDescriptorProfile` align with the canonical `IES codes.json` database.
4. **Arity Bounds for Matrix Sequences**: Verifies that each interval in compact profiles (`INTERVAL`, `DAILY`) has the correct number of payloads matching the descriptor sequence arity.
5. **Monotonicity (Cumulative Readings)**: Verifies that cumulative reading values (using `CUMULATIVE` accumulation behavior in `READING` reportedMode) are non-negative and strictly increasing.
6. **Time Order**: Verifies that interval `id` values are strictly increasing.
7. **Elaborated Usage Math Verification**: For cumulative registers, verifies that when `reportedMode` is `USAGE`, the opening/closing values exist and satisfy `value == closingValue - openingValue`.
8. **Meter Category Check**: Cross-references meter IDs against `MeterCategories.json` to verify that requested telemetry fields are supported for that meter's classification.

## CLI Usage

```bash
python validator.py <target_json_file_or_directory>
```
