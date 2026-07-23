# OutageNotification

> ⚠️ **WORK IN PROGRESS — subject to change.** Early draft family (v0.1) for discussion; field names, enums and interpretation are not final. Do not depend on it for production integrations yet.

*A machine-readable payload a distribution licensee publishes to describe one planned or unplanned electricity outage — usable both as a public outage-map feed and as a push alert to affected consumers.*

**Status:** Draft (current: **v0.1**) · **Issued by** DISCOMs (or their OMS / MDMS / SCADA / RTDAS) · **Consumed by** outage-map feeds, subscribed consumers, mass-alerting networks, reliability reporting

## What it records

One notice per outage, updated in place over its life (ALERT → UPDATE → RESTORED/CANCELLED, each version independently signed): classification (`outageClass` — planned / breakdown / rostering — separate from lifecycle `status`), a three-layer **cause** (IEEE 1782 category + the vendor's own fault code carried verbatim + free text), **affected assets** (feeders, DTs, substations, with voltage level and optional GeoJSON geometry) and **area**, **impact** (customers affected; de-energised/energised connection points reserved for an authenticated tier), **timing** (window, estimated and actual restoration — the inputs to IEEE 1366 indices — and a 240-minute SLA target), field **response**, localized **public-facing text** (CAP-shaped), and **provenance** back to the smart-meter signal and [MeterData](../MeterData/README.md) `AlarmProfile` that auto-detected it.

| Model | Purpose |
|-------|---------|
| `OutageNotification` | Root — class, status, cause, assets, area, timing, impact, response, public info, provenance, extensions |
| `OutageAsset` | Affected feeder/DT/substation with smart-meter ref and optional GeoJSON geometry |
| `OutageProvenance` | Detecting system, AMISP code, raw feeder-status signal, alarm refs into MeterData |

## How things are identified

A single `Identifier{scheme, value, namespace}` object throughout; the notice's `id` (the DISCOM's own breakdown/shutdown ID) stays constant across updates. Assets ideally carry a stable `GIS_FEATURE_ID` or `MRID` so consumers holding the DISCOM's GIS layer can join on id and pull geometry from GIS; inline `geo` is the fallback.

## Standards basis

No Indian standard yet covers outage publication; the schema composes one layer per standard: **IEC 61968-3 (CIM)** for outage/UsagePoint semantics and the planned/unplanned split, **OASIS CAP v1.2** for the push-alert envelope, **IEEE 1782-2022** (§4.4/§4.5) for the cause taxonomy, **IEEE 1366** for reliability-index inputs, plus the **ODIN** two-tier publication pattern, **MultiSpeak** detection flow and **GeoJSON (RFC 7946)**. A shipped crosswalk maps a real DISCOM's 31-code fault-reason pick-list onto the IEEE taxonomy.

## How it fits together

Downstream of a two-layer pipeline: a thin **detection/ingest** layer (an AMISP-operated substation meter's digital-input signal, batched into the `FeederStatusIngest` API) and a **publication** layer — the same notice serves a `GET /outages.geojson` map feed, a CAP feed for alerting (with SACHET/NDMA Cell Broadcast as the intended wide-area channel), and per-connection lookup. A coarse public tier carries no PII; an authenticated tier adds affected connection points. No IES use-case guide exists yet.

## Design note

- [v0.1/OutageNotification_Design.md](v0.1/OutageNotification_Design.md) — full rationale: standards survey, OMS/CAP/CIM mapping tables, GIS readiness, enum provenance
- [v0.1/FeederStatusIngest.openapi.yaml](v0.1/FeederStatusIngest.openapi.yaml) — feeder-status ingest API (detection layer)

## Open points

- "RS" in the source OMS shorthand is interpreted as Roster Shutdown (restoration modelled as a status transition, not a class) — pending confirmation with the source utility.
- Several enums are deliberately local (`outageClass`, `status`, `assetLevel`, `consumerCategory`, `source`); whether to propose any for standardisation is open, and vendor feeder-status codes are not yet mapped to the IS 15959 event/OBIS list.
- The public-tier vs. authenticated-tier granularity of `impact.deEnergized[]` is an open privacy question.

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.1](v0.1/README.md) | **Draft (WIP)** | Initial model: OutageNotification + sub-models; provenance links to MeterData AlarmProfile |
