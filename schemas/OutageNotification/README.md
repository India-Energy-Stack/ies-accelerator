# OutageNotification

> ⚠️ **WORK IN PROGRESS — subject to change.** Early draft family (v0.1) for discussion; not yet stable.

Schema for a distribution licensee (DISCOM) to publish **planned and unplanned electricity outage** details — as a website / outage-map feed (pull) and as push notifications to affected or subscribed consumers (push). GIS-ready (GeoJSON, WGS84) and future-proof (additive enums, namespaced extensions).

**Namespace prefix:** `ies:` → `https://india-energy-stack.github.io/ies-accelerator/schemas/ies#`

**Tags:** `outage` · `feeder` · `discom` · `oms` · `cap` · `gis` · `ies`

---

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.1](v0.1/README.md) | **Draft (WIP)** | Initial model: OutageNotification + sub-models; provenance links to MeterData AlarmProfile |

---

## Models

| Model | Purpose |
|-------|---------|
| `OutageNotification` | Root — class (planned/breakdown/roster/load-shedding), status, cause, affected assets, area, timing, impact, response, public info, provenance |
| `OutageAsset` | Affected feeder/DT/substation with smart-meter ref and optional GeoJSON geometry |
| `OutageProvenance` | Source, AMISP code, raw feeder-status signal, and alarm refs into MeterData |

---

## Design note

The full design rationale — standards survey, mapping tables (OMS/PVVNL/CAP/CIM), GIS/outage-map readiness, enum provenance, and the comparison with the draft real-time feeder-status push API — lives alongside the schema:

- [v0.1/OutageNotification_Design.md](v0.1/OutageNotification_Design.md) — design note
- [v0.1/FeederStatusIngest.openapi.yaml](v0.1/FeederStatusIngest.openapi.yaml) — cleaned feeder-status ingest API stub

## Usage

DISCOMs publish outage notices as a feed (`/outages`, `/outages.geojson`), a CAP feed for alerting, and webhooks to subscribers. Auto-detected outages carry provenance back to the smart-meter signal and the [MeterData](../MeterData/README.md) `AlarmProfile`.
