# MeterData v0.6 — Examples Index

This directory holds payload examples for the MeterData v0.6 schema. Files are kept flat (to preserve compatibility with existing tooling and scripts), but they fall into three categories:

## 1. Single-profile examples

Demonstrate one profile in isolation. Use these to understand a single profile's shape.

| Profile | File(s) |
|---|---|
| `INSTANTANEOUS` | `InstantaneousProfile.json` |
| `INTERVAL` | `IntervalProfile.json`, `IntervalProfile_Elaborated.json` |
| `DAILY` | `DailyProfile.json`, `DailyProfile_Elaborated.json`, `DailyProfile_ReadingMode.json`, `DailyProfile_ReadingMode_Elaborated.json` |
| `MONTHLY` | `MonthlyProfile.json`, `MDM_MonthlyProfile.json` |
| `BILL_DETAILS` | `BillDetails.json`, `Billing_MonthlyProfile.json` |
| `EVENT` | `EventProfile.json` |
| `ALARM` | `AlarmProfile.json` |
| `CUSTOMER` | `CustomerProfile.json`, `CustomerMapping.json`, `CustomerBillingSummary.json` |

## 2. Composed examples

Combine multiple profiles in one payload. Use these to see how the array envelope and `payloadDescriptorSetRef` work across profiles.

| File | What it shows |
|---|---|
| `MultiMeterBulkDataset.json` | Canonical bulk case: many meters, many profiles, one payload (compact form, OBIS keys) |
| `MultiMeterBulkDataset_Elaborated.json` | Same payload, fully elaborated (no compact sequences) |
| `MultiMeterBulkDatasetShortCodes.json` | Bulk case using short codes instead of raw OBIS |
| `MultiMeterBulkDatasetShortCodes_Elaborated.json` | Bulk case, short codes, elaborated |
| `AggregatedFeeder.json` / `AggregatedFeeder_Elaborated.json` | Feeder-level aggregation across meters |
| `Anonymised_Telemetry_Response.json` | Anonymised telemetry response for a request |
| `Anonymised_Topology_Example.json` | Topology relationships, anonymised |

## 3. Operational scenarios

Real-world operational events at large DISCOMs. These are not edge cases — they are weekly occurrences and must be expressible in the schema.

| File | Scenario |
|---|---|
| `Billing_MeterChange.json` | Mid-cycle meter changeover (swap, reinstall) |
| `MonthlyProfile_MultipleResets.json` | Multiple MD resets within a billing month |

## Naming conventions

- `*_Elaborated.json` — fully expanded form, no `compactSequences` indirection. See [`COMPACT_VS_ELABORATED.md`](./COMPACT_VS_ELABORATED.md).
- `*ShortCodes*.json` — uses IES short codes (`kWh imp`, `V_1P`) instead of raw OBIS codes as the primary `readingType`.
- `Anonymised_*` — sensitive identifiers replaced with placeholders.

## Generated examples

The `*_Elaborated.json` files are generated from their compact counterparts by `make elaborate`. Do not edit them by hand — edit the compact source and regenerate.
