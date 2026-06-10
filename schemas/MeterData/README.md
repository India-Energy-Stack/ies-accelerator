# MeterData

Smart meter telemetry payload schema for the India Energy Stack. Defines compact profile shapes for meter readings, billing data, and events — designed for high-efficiency data-only exchange without cryptographic wrapping.

**Namespace prefix:** `ies:` → `https://india-energy-stack.gitbook.io/docs/schemas/ies#`

**Tags:** `metering` · `telemetry` · `smart-meter` · `ies`

---

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.6](v0.6/README.md) | **Current** | Adds ALARM profile, anonymised topology, reading mode, split billing |
| [v0.5](v0.5/README.md) | Previous | Six profiles: CUSTOMER, INTERVAL, DAILY, BILLING, INSTANTANEOUS, EVENT |

---

## Profile shapes

| Profile | Description |
|---------|-------------|
| `CUSTOMER` | Slow-changing customer metadata, service points, meter installations |
| `INTERVAL` | Block load survey at high-resolution intervals (15 or 30 min) |
| `DAILY` | Daily accumulated load survey profiles |
| `MONTHLY` | Monthly billing resets — ToU buckets, MD, cumulative registers |
| `BILL_DETAILS` | Computed billing details — amount, due date, payment status |
| `INSTANTANEOUS` | Real-time snapshot of voltages, currents, powers |
| `EVENT` | IS 15959 diagnostic codes and tamper events |
| `ALARM` | Active alerts — tamper, low prepayment credit, voltage sag, overload *(v0.6+)* |

---

## Usage

Used in Beckn `on_status` flows by data providers (AMISP, MDM, DISCOM) to deliver smart meter telemetry. When delivered with provenance attestation, wrap in [MeterDataCredential](../MeterDataCredential/README.md).
