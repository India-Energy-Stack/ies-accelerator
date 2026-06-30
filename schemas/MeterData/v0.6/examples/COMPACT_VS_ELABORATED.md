# Compact vs Elaborated Form — When to Use Which

MeterData v0.6 supports two equivalent representations of the same payload:

- **Compact form** — each row is a position-coded array. A `compactSequence` declared once in the descriptor explains the position-to-attribute mapping.
- **Elaborated form** — each row is a fully named object. Self-contained, no reference resolution required to interpret.

Conversion between them is mechanical. `make elaborate` generates the elaborated `*_Elaborated.json` file from any compact source.

## When to use each

| Situation | Recommended form |
|---|---|
| Bulk multi-meter exchange (hundreds of meters, many days) | **Compact** — descriptor declared once, payload size minimised |
| Single-profile, single-meter payload | Either is fine |
| Documentation, tutorials, walkthroughs | **Elaborated** — no descriptor lookup needed to read |
| Implementer onboarding / first integration | **Elaborated** — easier to inspect by eye |
| Air-gapped MDM or forensic archive | **Elaborated** — payload remains interpretable without the descriptor file |
| Low-volume one-off exchanges (alarm bursts, event logs) | **Elaborated** — compact savings are marginal |
| High-throughput streaming (interval blocks at AMI scale) | **Compact** — wire efficiency matters |

## Trade-offs at a glance

| Property | Compact | Elaborated |
|---|---|---|
| Wire size | Smaller (often 3–5×) | Larger |
| Human readability | Lower | Higher |
| Self-describing | Requires descriptor | Yes, standalone |
| Validation surface | Position-coded — typos in `compactSequences` propagate silently | Named — typos surface at validation |
| Best for | Many rows, same shape | Few rows, mixed shapes |

## Rule of thumb

> **If a payload has fewer than ~10 rows, prefer elaborated. If it repeats the same row shape across hundreds of rows, prefer compact.**

The two forms are first-class and interchangeable. A consumer that does not want to handle compact form can request elaborated only; conversion happens at the producer or via the reference tooling.

## Examples in this directory

For every multi-row example we ship a `*_Elaborated.json` companion (generated). Compare any pair to see the same data in both forms:

- `IntervalProfile.json` ↔ `IntervalProfile_Elaborated.json`
- `DailyProfile.json` ↔ `DailyProfile_Elaborated.json`
- `MultiMeterBulkDataset.json` ↔ `MultiMeterBulkDataset_Elaborated.json`
- `MultiMeterBulkDatasetShortCodes.json` ↔ `MultiMeterBulkDatasetShortCodes_Elaborated.json`
- `AggregatedFeeder.json` ↔ `AggregatedFeeder_Elaborated.json`
