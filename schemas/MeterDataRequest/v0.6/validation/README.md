# MeterDataRequest v0.6 Semantic Validator

This directory contains the semantic validator for `MeterDataRequest v0.6` request, capabilities, and authorization payloads.

## Rules Enforced

The validator performs structural validation against the Draft 2020-12 JSON Schema (`schema.json`) and enforces the following semantic rules:

1. **Reading Type Resolution**: Validates that all requested register value strings (OBIS/Short names) are resolvable against `IES codes.json`.
2. **Profile Type Restrictions**: Verifies that requested registers are permitted under the specific profile capability group (e.g. `kWh imp` must not be requested under `IntervalProfile`).
3. **Telemetry Mode Compatibility**: Verifies that requested query modes (such as `READING` or `USAGE`) are listed as supported in the register's `supportedModes` in `IES codes.json`.
4. **Authorization Validity Period**: Checks that the authorization time window is logically correct (`validUntil` is strictly after `validFrom`).

## CLI Usage

```bash
python validator.py <target_json_file_or_directory>
```
