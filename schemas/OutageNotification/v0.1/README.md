> **Files** — [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/attributes.yaml) · [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/schema.json) · [context.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/context.jsonld) · [vocab.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/vocab.jsonld) · [examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/OutageNotification/v0.1/examples)

# Outage Notification Schema (v0.1)

> ⚠️ **WORK IN PROGRESS — subject to change.** This is an early draft (v0.1) published for discussion. Models, field names, enums, and the SD/BD/RS interpretation are not final and may change without notice before a stable release. Do not depend on it for production integrations yet.

Machine-readable schema for a distribution licensee (DISCOM) to publish **planned and unplanned electricity outage** details. One canonical object that is publishable as a **website / outage-map feed** (pull) and **pushable to affected or subscribed consumers** (push). Designed to be **GIS-ready** and **future-proof**.

## Overview

`OutageNotification` describes a single outage (planned shutdown, breakdown, roster/load-shedding) with its cause, affected assets, area, timing, impact, field response, and public-facing text. Where an outage is auto-detected, `provenance` links back to the originating smart-meter signal and the IES `MeterData` `AlarmProfile`.

It composes proven standards by layer:

- **IEC 61968-3 (CIM)** — outage/UsagePoint data semantics, planned vs unplanned.
- **ODIN** (US DOE/ORNL) — publication pattern; coded + free-text cause.
- **OASIS CAP v1.2** (ITU-T X.1303) — push-alert envelope (`msgType`, `references`, `severity`, area + polygon, headline/instruction).
- **MultiSpeak** — AMI/MDMS → OMS detection flow and provenance.
- **GeoJSON (RFC 7946)** — GIS geometry, WGS84, for outage maps.
- **IEEE 1366 / RDSS** — restoration time + customer counts for SAIDI/SAIFI.

Design rationale, the full standards survey, mapping tables (OMS/DISCOM/CAP/CIM), the GIS/outage-map readiness section, and the feeder-status ingest (detection) layer are in the design note alongside this schema: [OutageNotification_Design.md](./OutageNotification_Design.md) (and the ingest stub [FeederStatusIngest.openapi.yaml](./FeederStatusIngest.openapi.yaml)).

---

## Enum provenance (borrowed vs local)

Each enum declares its origin in its `description` (and a machine-readable `$comment`); enums borrowed wholesale from a standard are also semantically anchored in `context.jsonld` via their term IRI.

| Enum | Origin |
|------|--------|
| `msgType` | **Borrowed** — OASIS CAP v1.2 `alert/msgType` (anchored `urn:oasis:names:tc:emergency:cap:1.2#msgType`) |
| `severity` | **Borrowed** — OASIS CAP v1.2 `info/severity` (anchored `urn:oasis:names:tc:emergency:cap:1.2#severity`) |
| `cause.category` / `cause.subcategory` | **Aligned** — IEEE 1782-2022 §4.4 (ten cause categories) and §4.5 (subcategories), used with IEEE 1366 |
| `Identifier.scheme` | **Mixed** — `MRID` from CIM (IEC 61968/61970), `DID` from W3C DID Core; remaining values local |
| `feederStatus` | **Local** normalization; energized/de-energized align with CIM UsagePoint semantics |
| `outageClass` | **Local** — DISCOM OMS "Down Info" value set |
| `status`, `category`, `assetLevel`, `consumerCategory`, `source` | **Local** — not from a published standard |

> Note: `category` (outage category) is **not** CAP's `info/category` — it is a local value set with a deliberately different membership.

---

## Models

| Model | Purpose |
|-------|---------|
| `OutageNotification` | Root — class, status, cause, assets, area, timing, impact, response, public info, provenance |
| `OutageCause` | IEEE 1782 cause category + subcategory, vendor code (verbatim), free-text reason |
| `OutageAsset` | Affected asset (feeder/DT/substation/line) with meter ref + optional geometry |
| `OutageNetworkContext` | DISCOM org hierarchy (Discom > Zone > Circle > Division > Subdivision > Substation) |
| `OutageAffectedArea` | CAP area — text + admin areas + GeoJSON geometry |
| `OutageImpact` | Customers affected + de-/energized UsagePoints (CIM) |
| `OutageTiming` | Window (TimePeriod), ETR, actual restoration, SLA target |
| `OutageResponse` | Back-feed, resource status, complaint count |
| `OutagePublicInfo` | CAP info block for web/push |
| `OutageProvenance` | Source, AMISP code, raw signal, alarm refs into MeterData |

---

## Directory Structure and Files

| File | Description |
|------|-------------|
| [`attributes.yaml`](./attributes.yaml) | Canonical OpenAPI 3.1.0 source of truth describing all models, attributes, and types. |
| [`schema.json`](./schema.json) | Compiled Draft 2020-12 JSON Schema for payload validation. |
| [`context.jsonld`](./context.jsonld) | Compiled JSON-LD context mapping attributes to `ies:` terms. |
| [`vocab.jsonld`](./vocab.jsonld) | Compiled JSON-LD vocabulary (classes and properties). |
| [`examples/`](./examples) | JSON-LD example payloads (planned multi-feeder shutdown; unplanned breakdown with provenance; restoration UPDATE). |
| [`OutageNotification_Design.md`](./OutageNotification_Design.md) | Design note — standards survey, mapping tables, GIS readiness, enum provenance. |
| [`FeederStatusIngest.openapi.yaml`](./FeederStatusIngest.openapi.yaml) | Real-time feeder-status ingest API (detection layer). |
| [`fault_reason_crosswalk.json`](./fault_reason_crosswalk.json) | DISCOM FAULT_REASON master (FORM_ID 8312) → `cause.category`/`cause.subcategory` (IEEE 1782 §4.4/§4.5) crosswalk. |
| [`OutageNotification_Implementation.md`](./OutageNotification_Implementation.md) | Step-by-step guide to build a production pull/push outage-notification system. |
| [`tools/`](./tools) | DISCOM planned-shutdown CSV + transformer script (CSV → OutageNotification JSON). |

---

## Schema Generation and Validation

`schema.json`, `context.jsonld`, and `vocab.jsonld` are **compiled** from `attributes.yaml` — do not edit them by hand.

```bash
# from this directory
make            # generate + validate
# or, from the repo root:
python3 scripts/generate_schema_permissive.py schemas/OutageNotification/v0.1
python3 scripts/validate_schema.py schemas/OutageNotification/v0.1/schema.json schemas/OutageNotification/v0.1/examples
```


---

<!-- FIELD-TABLE:START — auto-generated by scripts/generate_field_tables.py from schema.json; do not edit by hand -->
## Field reference

_Auto-generated from `schema.json`. A field name in **bold** with a trailing **\*** is required; all others are optional. **Type** shows units for QuantitativeValue models. Where a field is derived from a standard, its description begins with **Based on** and the standard reference (from the field's `x-standard` annotation). One table per object._

### OutageNotification Payload

| Field | Type | Description |
|----|-------|-----------------|
| **`objectType`** \* | `OUTAGE_NOTIFICATION` | — |
| **`id`** \* | Identifier | Stable notice identity; reused across UPDATE/CANCEL messages. |
| **`outageClass`** \* | `PLANNED` / `BREAKDOWN` / `SCHEDULED_ROSTERING` / `EMERGENCY_ROSTERING` | Outage class, from the DISCOM OMS "Down Info" set (local, additive enum). Rostering = rotational load-shedding (scheduled vs emergency). Restoration is a status transition (status=RESTORED), not a class. |
| **`status`** \* | `SCHEDULED` / `ACTIVE` / `PARTIALLY_RESTORED` / `RESTORED` / `CANCELLED` | Outage lifecycle state. LOCAL enum (not from a published standard); loosely aligned with the CIM Outage lifecycle. |
| `msgType` | `ALERT` / `UPDATE` / `CANCEL` | **Based on** OASIS CAP v1.2 (alert/msgType). Message type; UPDATE/CANCEL refer to a prior notice via `references`. |
| `references` | list of Identifier | **Based on** OASIS CAP v1.2 (alert/references). Prior notice ids this message updates or cancels (CAP `references`). |
| `severity` | `EXTREME` / `SEVERE` / `MODERATE` / `MINOR` / `UNKNOWN` | **Based on** OASIS CAP v1.2 (info/severity). Severity of the outage. |
| `category` | `MAINTENANCE` / `UPGRADE` / `FAULT` / `LOAD_SHEDDING` / `WEATHER` / `SAFETY` / `OTHER` | Coarse descriptor for display/filtering (local enum; not CAP `info/category`). For analytics, prefer the standardized `cause.category`. |
| `cause` | OutageCause | — |
| `forceMajeure` | yes / no | OMS "Force Majeure" flag. |
| `issuedBy` | Party | — |
| `issuedAt` | date-time | — |
| `detectedAt` | date-time | When MDMS/SCADA first detected the outage (unplanned). |
| `lastUpdatedAt` | date-time | — |
| `network` | OutageNetworkContext | — |
| **`affectedAssets`** \* | list of OutageAsset | — |
| `affectedArea` | OutageAffectedArea | — |
| `impact` | OutageImpact | — |
| **`timing`** \* | OutageTiming | — |
| `response` | OutageResponse | — |
| `publicInfo` | OutagePublicInfo | — |
| `provenance` | OutageProvenance | — |
| `extensions` | object | Namespaced DISCOM-specific fields, e.g. { "discom": { "breakdownId": "6357257", "downType": "FEEDER" } }. |

### OutageCause

| Field | Type | Description |
|----|-------|-----------------|
| `category` | `EQUIPMENT` / `LIGHTNING` / `PLANNED` / `POWER_SUPPLY` / `PUBLIC` / `VEGETATION` / `WEATHER` / `WILDLIFE` / `UNKNOWN` / `OTHER` | **Based on** IEEE 1782-2022 §4.4 (with IEEE 1366). Standardized interruption cause category, for reliability benchmarking. Load-shedding/rostering has no standard category — map scheduled rostering to PLANNED, emergency to OTHER, and carry the nature in `outageClass`. |
| `subcategory` | `DEGRADATION` / `EQUIPMENT_ERROR` / `ENVIRONMENTAL` / `DIRECT_STRIKE` / `INDIRECT_STRIKE` / `NEW_CONSTRUCTION` / `MAINTENANCE` / `CUSTOMER_REQUEST` / `OTHER_UTILITY_REQUEST` / `GENERATION` / `TRANSMISSION` / `SUBTRANSMISSION` / `DISTRIBUTION` / `DISTRIBUTED_GENERATION_STORAGE` / `OTHER_UTILITY_SUPPLY` / `DIG_IN` / `FOREIGN_CONTACT` / `FIRE_POLICE` / `VEHICLE` / `WITHIN_CLEARANCE_ZONE` / `OUTSIDE_CLEARANCE_ZONE` / `PRECIPITATION` / `ICE` / `WIND` / `EXTREME_TEMPERATURE` / `MAMMAL` / `BIRD` / `REPTILE_AMPHIBIAN` / `NO_SPECIFIC_CAUSE_FOUND` / `UTILITY_ERROR` / `OTHER_UTILITY_INITIATED` / `OTHER` | **Based on** IEEE 1782-2022 §4.5. Standardized cause subcategory; must be valid for the chosen `category` (see $comment for the mapping). Leave unset if the field finding is inconclusive. |
| `faultType` | text | Vendor asset/voltage level of the fault, e.g. 33KV, 11KV, DT, LT. |
| `code` | text | Vendor/OMS fault-reason code, carried verbatim (e.g. a DISCOM FAULT_REASON) — not standardized; map to `category`/`subcategory` for interoperability (see fault_reason_crosswalk.json). Set `codeNamespace` where the code's authority matters. |
| `codeNamespace` | text | Authority/vendor that defines `code` (e.g. the OMS vendor or DISCOM). |
| `text` | text | Free-text reason; may be localized (e.g. Hindi). |

### OutageAsset

| Field | Type | Description |
|----|-------|-----------------|
| **`id`** \* | Identifier | Asset id/name; ideally a stable GIS feature id or MRID for map join. |
| **`assetLevel`** \* | `SUBSTATION` / `FEEDER` / `DT` / `LINE_SEGMENT` / `SERVICE_POINT` | Network level of the affected asset (local enum; aligns with CIM Equipment/UsagePoint). |
| `voltageLevel` | text | e.g. 33kV, 11kV, LT, DT. |
| `consumerCategory` | `URBAN` / `RURAL` / `AGRICULTURE` / `INDUSTRIAL` / `MIXED` / `OTHER` | Consumer mix on the asset (local enum; DISCOM "Feeder Type"). |
| `meterRef` | Identifier | Feeder/substation smart-meter number — join key to MDMS/MeterData. |
| `parentRef` | Identifier | Parent asset (e.g. a feeder's substation, a DT's feeder). |
| `geo` | GeoJSONGeometry | **Based on** GeoJSON (RFC 7946), WGS84. Optional inline geometry (WGS84): Point (substation/DT), LineString (feeder route), Polygon (service area). |

### OutageNetworkContext

| Field | Type | Description |
|----|-------|-----------------|
| `discom` | Identifier | — |
| `zone` | text | — |
| `circle` | text | — |
| `division` | text | — |
| `subdivision` | text | — |
| `substation` | Identifier | — |
| `district` | text | — |

### OutageAffectedArea

| Field | Type | Description |
|----|-------|-----------------|
| `text` | text | Free-text localities (CAP areaDesc), e.g. "SEC-14, 9, 11 Rajnagar". |
| `adminAreas` | list of text | Named localities / wards / villages. |
| `geo` | GeoJSONGeometry | **Based on** GeoJSON (RFC 7946); CAP area. Polygon/MultiPolygon service area, or Point/circle (CAP). WGS84. |

### OutageImpact

| Field | Type | Description |
|----|-------|-----------------|
| `customersAffected` | integer | — |
| `deEnergized` | list of Identifier | **Based on** CIM (IEC 61968-3 UsagePoint). Optional SDP/UsagePoint refs (authenticated tier). |
| `energized` | list of Identifier | **Based on** CIM (IEC 61968-3 UsagePoint). Optional points confirmed still energized. |

### OutageTiming

| Field | Type | Description |
|----|-------|-----------------|
| **`period`** \* | TimePeriod | Outage window (Down From + duration). |
| `estimatedRestoration` | date-time | ETR (OMS "Estimated Time"). |
| `actualRestoration` | date-time | Set when status=RESTORED; feeds IEEE 1366 indices. |
| `slaTargetMinutes` | integer | SLA target, e.g. 240 (4 hrs). |

### OutageResponse

| Field | Type | Description |
|----|-------|-----------------|
| `backFeedGiven` | yes / no | Partial restoration via alternate feed (OMS "Back-Feed given"). |
| `resourceStatus` | text | e.g. PENDING, RESOURCE_ALLOCATED, IN_PROGRESS. |
| `complaintCount` | integer | Linked consumer complaints (OMS "No. of Complaints"). |

### OutagePublicInfo

| Field | Type | Description |
|----|-------|-----------------|
| `language` | text | BCP-47, e.g. en, hi. |
| `headline` | text | — |
| `description` | text | — |
| `instruction` | text | What the consumer should do. |

### OutageProvenance

| Field | Type | Description |
|----|-------|-----------------|
| `source` | `MDMS` / `OMS` / `SCADA` / `RTDAS` / `AMI` / `MANUAL` | System that raised this notice (local enum; RTDAS = Real-Time Data Acquisition System). |
| `amispCode` | text | AMI Service Provider that supplied the detection signal (feeder-status ingest API). |
| `detectionRef` | Identifier | Reference to the real-time detection record that raised the outage (e.g. a DISCOM RTDAS_DATA_ID). Absence or a "0" sentinel indicates a manually entered outage (source=MANUAL). |
| `signal` | OutageSignal | — |
| `alarmRefs` | list of OutageAlarmRef | References into MeterData AlarmProfile records. |

### OutageSignal

| Field | Type | Description |
|----|-------|-----------------|
| `eventId` | text | Idempotency key of the originating feeder-status event. |
| `feederStatus` | `ENERGIZED` / `DE_ENERGIZED` / `UNKNOWN` | Normalized feeder status (local enum); raw vendor code in `rawCode`. Energized/de-energized align with CIM UsagePoint semantics. |
| `diPort` | text | Digital-input port on the substation meter that carried the signal. |
| `rawCode` | text | Vendor-native status code as received (e.g. FEEDER_STATUS=102), for traceability. |

### OutageAlarmRef

| Field | Type | Description |
|----|-------|-----------------|
| **`meterRef`** \* | Identifier | — |
| `alarmId` | integer | — |
| `timestamp` | date-time | — |

### Party

| Field | Type | Description |
|----|-------|-----------------|
| `id` | Identifier | — |
| `name` | text | — |
| `contact` | text | Phone/email/URL for queries (e.g. 1912). |

### Identifier

| Field | Type | Description |
|----|-------|-----------------|
| **`scheme`** \* | `METER_SERIAL` / `MRID` / `GIS_FEATURE_ID` / `SERVICE_DELIVERY_POINT` / `FEEDER` / `SUBSTATION` / `DT` / `CONSUMER_NUMBER` / `ORG` / `DID` / `OTHER` | **Based on** MRID: CIM (IEC 61968/61970); DID: W3C DID Core. Identifier scheme (mixed provenance). MRID and DID are borrowed from their standards; the rest are local vendor/DISCOM master keys. |
| **`value`** \* | text | — |
| `namespace` | text | — |

### TimePeriod

| Field | Type | Description |
|----|-------|-----------------|
| **`start`** \* | date-time | — |
| **`duration`** \* | duration | ISO-8601, e.g. PT2H. |

<!-- FIELD-TABLE:END -->
