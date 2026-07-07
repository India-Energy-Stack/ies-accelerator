# Tools — DISCOM planned-shutdown → OutageNotification

A worked example of turning a DISCOM's tabular planned-shutdown publication into the `OutageNotification` schema.

| File | Description |
|------|-------------|
| [`discom_planned_shutdown.csv`](./discom_planned_shutdown.csv) | Sample input mirroring the columns of a DISCOM "Detail of Planned Shutdown" sheet (a public PDF publication pattern used by Indian DISCOMs). One row per feeder; rows sharing `group_id` belong to one shutdown. Includes English and Hindi (Devanagari) reasons/areas. |
| [`transform_discom_csv.py`](./transform_discom_csv.py) | Transformer: CSV → array of `OutageNotification` JSON. |

## Run

```bash
python3 transform_discom_csv.py discom_planned_shutdown.csv -o ../examples/discom_planned_shutdown.json
# validate (from repo root):
python3 ../../../scripts/validate_schema.py ../schema.json ../examples
```

## Mapping notes

- Rows are grouped by **`group_id`** → one `OutageNotification` each; every feeder becomes an entry in **`affectedAssets[]`**.
- The **feeder smart-meter number** → `affectedAssets[].meterRef` (`scheme: METER_SERIAL`) — the 1:1 feeder↔meter link.
- `feeder_type` (URBAN/RURAL/AGRICULTURE/…) → `affectedAssets[].consumerCategory` (TEHSEEL/INDEPENDENT → `OTHER`).
- `date` + `from_time`/`to_time` → `timing.period` (start + ISO-8601 duration).
- `reason` → `cause.text` (verbatim) and `cause.subcategory` (`NEW_CONSTRUCTION` vs `MAINTENANCE`, IEEE 1782 §4.5, via keyword heuristic); all rows are planned shutdowns → `outageClass: PLANNED`, `cause.category: PLANNED`.
- **Language:** UTF-8 throughout (`ensure_ascii=False`); Hindi text is preserved verbatim in `cause.text` / `affectedArea.text` / `publicInfo.description`, and `publicInfo.language` is set to `hi` when Devanagari is detected.
