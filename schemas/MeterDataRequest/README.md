# MeterDataRequest

Schema for querying smart meter telemetry. Specifies which meters, what data, and for how long — sent by a data consumer (BAP/seeker) to a data provider (BPP) in Beckn `select`/`init` flows.

**Tags:** `metering` · `request` · `telemetry` · `ies`

---

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.6](v0.6/README.md) | **Current** | Split into three composable models: MeterDataCapabilities, MeterDataAuthorisation, MeterDataRequest |
| [v0.5](v0.5/README.md) | Previous | Single unified request schema |

---

## Models (v0.6)

| Model | Purpose |
|-------|---------|
| `MeterDataCapabilities` | Provider declares what profiles, register keys, and query boundaries are supported |
| `MeterDataAuthorisation` | Consumer proves consent scope — meters/feeders, time window, profile types |
| `MeterDataRequest` | Active query binding capabilities to a specific authorisation |

---

## Usage

Consumer attaches a [MeterDataRequestCredential](../MeterDataRequestCredential/README.md) at `confirm` time to prove authorisation. Provider validates before delivering [MeterData](../MeterData/README.md) wrapped in a [MeterDataCredential](../MeterDataCredential/README.md).
