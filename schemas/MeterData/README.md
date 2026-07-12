# MeterData

*A lightweight, high-throughput telemetry payload for exchanging smart-meter readings, events and alarms — cheap to parse and store at Head-End-System scale, without cryptographic wrapping.*

**Status:** Stable (current: **v0.6**) · **Issued by** AMISPs, HES/MDM systems, DISCOMs · **Consumed by** DISCOMs, regulators, TSPs and consented third parties

## What it records

Nine record shapes, discriminated by `profileType`:

| Profile | Description |
|---------|-------------|
| `CUSTOMER` | Slow-changing customer metadata, service points, meter installations (PII sub-object omissible for anonymised exchange) |
| `INTERVAL` | Block load survey at high-resolution intervals (15 or 30 min) |
| `DAILY` | Daily accumulated load survey |
| `MONTHLY` | Monthly billing resets — ToU buckets, MD, cumulative registers |
| `BILL_DETAILS` | Computed billing details — amount, due date, payment status |
| `INSTANTANEOUS` | Real-time snapshot of voltages, currents, powers |
| `EVENT` | IS 15959 diagnostic codes and tamper events |
| `ALARM` | Active alerts — tamper, low prepayment credit, voltage sag, overload |
| `DESCRIPTOR` | Shared dictionary (the Data Descriptor Engine) — register metadata and compact column layouts declared once, not per row |

Readings distinguish `READING` (register value) from `USAGE` (delta over a period) and carry a `validationStatus` and `source`. The compact matrix form keeps a `DailyProfile` interval row as small as `{"id": 0, "payloads": [24512.4, 25134.8]}`. The schema carries no signature — when provenance attestation is needed, the payload is wrapped in a [MeterDataCredential](../MeterDataCredential/README.md).

## How things are identified

A generic `Identifier{scheme, value, namespace}` object; schemes include `METER_SERIAL`, `CONSUMER_NUMBER`, `OBIS`, `MRID` (from CIM — the one field with no Indian equivalent), and `DID`. Existing identifiers are carried verbatim. Individual registers are named by OBIS code or short code; the crosswalk (75 registers, plus IS 15959 event and alarm taxonomies) lives in the schema's own `IES codes.json` registry, cited per register down to the IS 15959 part/table/clause.

## Standards basis

- **IS 15959 (Parts 1–3)** — OBIS codes, event IDs and meter categories, cited at individual-register granularity in `IES codes.json`.
- **IS 16444** — the AC smart meter specification the profiles are built to carry.

## How it fits together

The primary telemetry payload of **[Smart Meter Data Exchange](../../use-cases/smart-meter-data-exchange/README.md)**, carried B2B over the IES Beckn network; the payload itself is wire-agnostic and consumer-facing delivery need not involve Beckn. The companion [MeterDataRequest](../MeterDataRequest/README.md) family (capabilities → authorisation → request) sits in front of the exchange; the [MeterDataCredential](../MeterDataCredential/README.md) wrapper adds provenance where needed (the **Consumer Meter Digest** pattern). A PII-redacted `CustomerProfile` doubles as an anonymised grid-topology index for TSPs.

## Open points

- A documented overlap with ElectricityCredential (consumer and DER-capacity concepts) is pending reconciliation in a future major version.
- `attributes.yaml`'s internal `info.version` still reads `0.5.0` under the `v0.6` directory — a labelling lag in the source.

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.6](v0.6/README.md) | **Current** | Adds ALARM profile, anonymised topology, reading mode, split billing |
| [v0.5](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.5) | Previous | Six profiles: CUSTOMER, INTERVAL, DAILY, BILLING, INSTANTANEOUS, EVENT |
