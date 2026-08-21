# Migrating MeterData examples from v0.5 to v0.6

v0.6 intentionally changes profile names, descriptor placement, identifier
forms, and several compact payload structures. It is therefore not expected to
be byte-for-byte or shape-for-shape equivalent to v0.5. The release gate is
instead `scripts/verify_v05_v06_equivalence.py`, which checks four separate
questions:

1. Does every v0.5 example have an explicit disposition?
2. Does each source profile have a declared v0.6 target profile with preserved
   meter/service-point identity (including two declared short-code rewrites)?
3. Are telemetry values, interval row associations, timestamps, events,
   overrides, identifiers, and critical customer or billing facts preserved
   unless an exact correction is explicitly listed?
4. Do all current v0.6 examples pass structural and semantic validation?

## Intentional disposition table

| v0.5 example | v0.6 target | Intentional difference |
|---|---|---|
| `AggregatedFeeder.json` | `AggregatedFeeder.json` | Adds an explicit descriptor profile. |
| `BillingProfile.json` | `CustomerBillingSummary.json` | Coalesces the duplicate v0.5 billing shape into `BillDetails`. |
| `CustomerBillingSummary.json` | `CustomerBillingSummary.json` | Renames and reshapes `BILLING` as `BILL_DETAILS`. |
| `CustomerProfile.json` | `CustomerProfile.json` | Retains the identified profile and adds one anonymised variant. |
| `DailyProfile.json` | `DailyProfile.json` | Adds a descriptor, replaces the malformed import-delta series with the exact approved monotonic cumulative series, and leaves consumer linkage to the meter/customer profile. Export and maximum-demand values and maximum-demand timestamps remain exact. |
| `EventProfile.json` | `EventProfile.json` | Retains the event profile and resolves consumer linkage separately through the meter. |
| `InstantaneousProfile.json` | `InstantaneousProfile.json` | Adds a descriptor and leaves consumer linkage to the meter/customer profile. |
| `IntervalProfile.json` | `IntervalProfile.json` | Migrates cumulative energy registers to interval block registers and leaves consumer linkage to the meter/customer profile. |
| `MultiMeterBulkDataset.json` | `MultiMeterBulkDataset.json` | Adds a descriptor and one new alarm profile; omits the customer name from the bulk telemetry payload. |
| `MultiMeterBulkDatasetShortCodes.json` | `MultiMeterBulkDatasetShortCodes.json` | Adds a descriptor and one new alarm profile; omits the customer name from the bulk telemetry payload; explicitly rewrites `METER-GENUS-01` to `METER-GENUS-01-ELABORATED` and `METER-HPL-02` to `METER-HPL-02-COMPACT`. |

Any new v0.5 example must be added to this disposition contract before the
migration check will pass. Missing targets, unexplained target additions, lost
or reassigned telemetry, changed timestamps, unapproved corrected values, and
invalid v0.6 examples all return a non-zero exit. The committed migration CLI
fixtures under `scripts/fixtures/` currently exercise missing disposition,
approved-value drift, direct timestamp drift, row/timestamp reassignment, and
meter-identity association drift; the positive gate exercises target coverage,
addition accounting, telemetry preservation, and current-version validity.
