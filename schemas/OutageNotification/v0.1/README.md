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

Design rationale, the full standards survey, mapping tables (OMS/PVVNL/CAP/CIM), the GIS/outage-map readiness section, and the feeder-status ingest (detection) layer are in the design note alongside this schema: [OutageNotification_Design.md](./OutageNotification_Design.md) (and the ingest stub [FeederStatusIngest.openapi.yaml](./FeederStatusIngest.openapi.yaml)).

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
| `outageClass` | **Local** — UPPCL OMS "Down Info" value set |
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
| [`fault_reason_crosswalk.json`](./fault_reason_crosswalk.json) | UPPCL FAULT_REASON master (FORM_ID 8312) → `cause.category`/`cause.subcategory` (IEEE 1782 §4.4/§4.5) crosswalk. |
| [`OutageNotification_Implementation.md`](./OutageNotification_Implementation.md) | Step-by-step guide to build a production pull/push outage-notification system. |
| [`tools/`](./tools) | PVVNL planned-shutdown CSV + transformer script (CSV → OutageNotification JSON). |

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

_Auto-generated from `schema.json`. **Field**, **Type** (with units for QuantitativeValue models), **Status**, and **Description** are derived from the schema; **Standard** comes from each field's `x-standard` annotation (`—` when unset). One table per object._

### OutageNotification Payload

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `objectType` | OUTAGE_NOTIFICATION | — | Mandatory | — |
| `id` | Identifier | — | Mandatory | Stable notice identity; reused across UPDATE/CANCEL messages. |
| `outageClass` | PLANNED / BREAKDOWN / SCHEDULED_ROSTERING / EMERGENCY_ROSTERING | — | Mandatory | LOCAL enum (not from a standard) — derived from the UPPCL OMS "Down Info" value set (confirmed from the UPPCL BDSD export): PLANNED - "Planned Shutdown" (scheduled maintenance). BREAKDOWN - "Breakdown Shutdown" (unplanned / fault outage). SCHEDULED_ROSTERING - "Scheduled Rostering" (planned rotational load-shedding on a roster). EMERGENCY_ROSTERING - "Emergency Rostering" (load-driven, e.g. overload, rotational shedding). Additive enum: extend if the OMS adds further Down Info values. Restoration is a status transition (status=RESTORED), not a class. |
| `status` | SCHEDULED / ACTIVE / PARTIALLY_RESTORED / RESTORED / CANCELLED | — | Mandatory | Outage lifecycle state. LOCAL enum (not from a published standard); loosely aligned with the CIM Outage lifecycle. |
| `msgType` | ALERT / UPDATE / CANCEL | OASIS CAP v1.2 (alert/msgType) | Optional | Message type. Enum BORROWED from OASIS CAP v1.2 `alert/msgType` (Alert/Update/Cancel). UPDATE/CANCEL refer to a prior notice via references. |
| `references` | list of Identifier | OASIS CAP v1.2 (alert/references) | Optional | Prior notice ids this message updates or cancels (CAP `references`). |
| `severity` | EXTREME / SEVERE / MODERATE / MINOR / UNKNOWN | OASIS CAP v1.2 (info/severity) | Optional | Severity. Enum BORROWED from OASIS CAP v1.2 `info/severity` (Extreme/Severe/Moderate/Minor/Unknown). |
| `category` | MAINTENANCE / UPGRADE / FAULT / LOAD_SHEDDING / WEATHER / SAFETY / OTHER | — | Optional | Coarse outage descriptor for display/filtering. LOCAL enum (not from a standard). Distinct from the standardized `cause.category` (IEEE 1782) and from `outageClass` (OMS Down Info); this is NOT CAP's `info/category`. For analytics, prefer `cause.category`. |
| `cause` | OutageCause | — | Optional | — |
| `forceMajeure` | yes / no | — | Optional | OMS "Force Majeure" flag. |
| `issuedBy` | Party | — | Optional | — |
| `issuedAt` | date-time | — | Optional | — |
| `detectedAt` | date-time | — | Optional | When MDMS/SCADA first detected the outage (unplanned). |
| `lastUpdatedAt` | date-time | — | Optional | — |
| `network` | OutageNetworkContext | — | Optional | — |
| `affectedAssets` | list of OutageAsset | — | Mandatory | — |
| `affectedArea` | OutageAffectedArea | — | Optional | — |
| `impact` | OutageImpact | — | Optional | — |
| `timing` | OutageTiming | — | Mandatory | — |
| `response` | OutageResponse | — | Optional | — |
| `publicInfo` | OutagePublicInfo | — | Optional | — |
| `provenance` | OutageProvenance | — | Optional | — |
| `extensions` | object | — | Optional | Namespaced DISCOM-specific fields, e.g. { "uppcl": { "breakdownId": "6357257", "downType": "FEEDER" } }. |

### OutageCause

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `category` | EQUIPMENT / LIGHTNING / PLANNED / POWER_SUPPLY / PUBLIC / VEGETATION / WEATHER / WILDLIFE / UNKNOWN / OTHER | IEEE 1782-2022 §4.4 (with IEEE 1366) | Optional | Standardized interruption cause category — the ten categories of IEEE 1782-2022 §4.4 (IEEE Guide for Collecting, Categorizing, and Utilizing Information Related to Electric Power Distribution Interruption Events), used with IEEE 1366 for reliability benchmarking. EQUIPMENT, LIGHTNING, PLANNED, POWER_SUPPLY, PUBLIC, VEGETATION, WEATHER (other than lightning), WILDLIFE, UNKNOWN, OTHER. IEEE 1782 is a guide (recommended practice). Note: load-shedding / rostering has no IEEE 1782 cause category — scheduled rostering maps to PLANNED, forced/emergency rostering to OTHER, with the rostering nature carried in `outageClass`. |
| `subcategory` | DEGRADATION / EQUIPMENT_ERROR / ENVIRONMENTAL / DIRECT_STRIKE / INDIRECT_STRIKE / NEW_CONSTRUCTION / MAINTENANCE / CUSTOMER_REQUEST / OTHER_UTILITY_REQUEST / GENERATION / TRANSMISSION / SUBTRANSMISSION / DISTRIBUTION / DISTRIBUTED_GENERATION_STORAGE / OTHER_UTILITY_SUPPLY / DIG_IN / FOREIGN_CONTACT / FIRE_POLICE / VEHICLE / WITHIN_CLEARANCE_ZONE / OUTSIDE_CLEARANCE_ZONE / PRECIPITATION / ICE / WIND / EXTREME_TEMPERATURE / MAMMAL / BIRD / REPTILE_AMPHIBIAN / NO_SPECIFIC_CAUSE_FOUND / UTILITY_ERROR / OTHER_UTILITY_INITIATED / OTHER | IEEE 1782-2022 §4.5 | Optional | Standardized cause subcategory from IEEE 1782-2022 §4.5. Must be a subcategory valid for the chosen `category`: EQUIPMENT={DEGRADATION,EQUIPMENT_ERROR,ENVIRONMENTAL,OTHER}; LIGHTNING={DIRECT_STRIKE,INDIRECT_STRIKE}; PLANNED={NEW_CONSTRUCTION,MAINTENANCE,CUSTOMER_REQUEST,OTHER_UTILITY_REQUEST,OTHER}; POWER_SUPPLY={GENERATION,TRANSMISSION,SUBTRANSMISSION,DISTRIBUTION,DISTRIBUTED_GENERATION_STORAGE,OTHER_UTILITY_SUPPLY}; PUBLIC={DIG_IN,FOREIGN_CONTACT,FIRE_POLICE,VEHICLE,OTHER}; VEGETATION={WITHIN_CLEARANCE_ZONE,OUTSIDE_CLEARANCE_ZONE,OTHER}; WEATHER={PRECIPITATION,ICE,WIND,EXTREME_TEMPERATURE,OTHER}; WILDLIFE={MAMMAL,BIRD,REPTILE_AMPHIBIAN,OTHER}; UNKNOWN={NO_SPECIFIC_CAUSE_FOUND}; OTHER={UTILITY_ERROR,OTHER_UTILITY_INITIATED,OTHER}. Leave unset if the field finding is inconclusive (IEEE 1782 §4.5). |
| `faultType` | text | — | Optional | Vendor asset/voltage level of the fault, e.g. 33KV, 11KV, DT, LT. |
| `code` | text | — | Optional | Vendor/OMS fault-reason code carried VERBATIM (e.g. the UPPCL numeric FAULT_REASON, or a subtype like OVERHEAD_CONDUCTOR_FAULT). These codes are vendor-defined and NOT standardized; map them to the standardized `category`/`subcategory` for interoperability. For the UPPCL FAULT_REASON master (FORM_ID 8312) see fault_reason_crosswalk.json in this folder. Provide `codeNamespace` where the code's authority matters. |
| `codeNamespace` | text | — | Optional | Authority/vendor that defines `code` (e.g. the OMS vendor or DISCOM). |
| `text` | text | — | Optional | Free-text reason; may be localized (e.g. Hindi). |

### OutageAsset

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `id` | Identifier | — | Mandatory | Asset id/name; ideally a stable GIS feature id or MRID for map join. |
| `assetLevel` | SUBSTATION / FEEDER / DT / LINE_SEGMENT / SERVICE_POINT | — | Mandatory | Network level of the affected asset. LOCAL enum (not from a standard); concepts align with CIM (IEC 61968/61970) Equipment/UsagePoint. |
| `voltageLevel` | text | — | Optional | e.g. 33kV, 11kV, LT, DT. |
| `consumerCategory` | URBAN / RURAL / AGRICULTURE / INDUSTRIAL / MIXED / OTHER | — | Optional | Consumer mix on the asset (PVVNL sheet "Feeder Type"). LOCAL enum (not from a standard); derived from Indian DISCOM feeder typing. |
| `meterRef` | Identifier | — | Optional | Feeder/substation smart-meter number — join key to MDMS/MeterData. |
| `parentRef` | Identifier | — | Optional | Parent asset (e.g. a feeder's substation, a DT's feeder). |
| `geo` | GeoJSONGeometry | GeoJSON (RFC 7946), WGS84 | Optional | Optional inline geometry (WGS84): Point (substation/DT), LineString (feeder route), Polygon (service area). |

### OutageNetworkContext

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `discom` | Identifier | — | Optional | — |
| `zone` | text | — | Optional | — |
| `circle` | text | — | Optional | — |
| `division` | text | — | Optional | — |
| `subdivision` | text | — | Optional | — |
| `substation` | Identifier | — | Optional | — |
| `district` | text | — | Optional | — |

### OutageAffectedArea

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `text` | text | — | Optional | Free-text localities (CAP areaDesc), e.g. "SEC-14, 9, 11 Rajnagar". |
| `adminAreas` | list of text | — | Optional | Named localities / wards / villages. |
| `geo` | GeoJSONGeometry | GeoJSON (RFC 7946); CAP area | Optional | Polygon/MultiPolygon service area, or Point/circle (CAP). WGS84. |

### OutageImpact

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `customersAffected` | integer | — | Optional | — |
| `deEnergized` | list of Identifier | CIM (IEC 61968-3 UsagePoint) | Optional | Optional SDP/UsagePoint refs (authenticated tier). |
| `energized` | list of Identifier | CIM (IEC 61968-3 UsagePoint) | Optional | Optional points confirmed still energized. |

### OutageTiming

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `period` | TimePeriod | — | Mandatory | Outage window (Down From + duration). |
| `estimatedRestoration` | date-time | — | Optional | ETR (OMS "Estimated Time"). |
| `actualRestoration` | date-time | — | Optional | Set when status=RESTORED; feeds IEEE 1366 indices. |
| `slaTargetMinutes` | integer | — | Optional | SLA target, e.g. 240 (4 hrs). |

### OutageResponse

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `backFeedGiven` | yes / no | — | Optional | Partial restoration via alternate feed (OMS "Back-Feed given"). |
| `resourceStatus` | text | — | Optional | e.g. PENDING, RESOURCE_ALLOCATED, IN_PROGRESS. |
| `complaintCount` | integer | — | Optional | Linked consumer complaints (OMS "No. of Complaints"). |

### OutagePublicInfo

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `language` | text | — | Optional | BCP-47, e.g. en, hi. |
| `headline` | text | — | Optional | — |
| `description` | text | — | Optional | — |
| `instruction` | text | — | Optional | What the consumer should do. |

### OutageProvenance

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `source` | MDMS / OMS / SCADA / RTDAS / AMI / MANUAL | — | Optional | System that raised this notice (RTDAS = Real-Time Data Acquisition System). LOCAL enum (not from a standard). |
| `amispCode` | text | — | Optional | AMI Service Provider that supplied the detection signal (feeder-status ingest API). |
| `detectionRef` | Identifier | — | Optional | Reference to the automated real-time detection record that raised the outage — e.g. the UPPCL RTDAS_DATA_ID. A sentinel like "0" / absence indicates a manually entered outage (source=MANUAL) rather than auto-detected. |
| `signal` | OutageSignal | — | Optional | — |
| `alarmRefs` | list of OutageAlarmRef | — | Optional | References into MeterData AlarmProfile records. |

### OutageSignal

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `eventId` | text | — | Optional | Idempotency key of the originating feeder-status event. |
| `feederStatus` | ENERGIZED / DE_ENERGIZED / UNKNOWN | — | Optional | Normalized feeder status; raw vendor code preserved in rawCode. LOCAL enum (the normalization is ours); the energized / de-energized terms align with CIM (IEC 61968-3) UsagePoint energization semantics. |
| `diPort` | text | — | Optional | Digital-input port on the substation meter that carried the signal. |
| `rawCode` | text | — | Optional | Vendor-native status code as received (e.g. FEEDER_STATUS=102), for traceability. |

### OutageAlarmRef

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `meterRef` | Identifier | — | Mandatory | — |
| `alarmId` | integer | — | Optional | — |
| `timestamp` | date-time | — | Optional | — |

### Party

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `id` | Identifier | — | Optional | — |
| `name` | text | — | Optional | — |
| `contact` | text | — | Optional | Phone/email/URL for queries (e.g. 1912). |

### Identifier

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `scheme` | METER_SERIAL / MRID / GIS_FEATURE_ID / SERVICE_DELIVERY_POINT / FEEDER / SUBSTATION / DT / CONSUMER_NUMBER / ORG / DID / OTHER | MRID: CIM (IEC 61968/61970); DID: W3C DID Core | Mandatory | Identifier scheme. MIXED provenance: - MRID is BORROWED from CIM (IEC 61968 / IEC 61970) master resource id. - DID is BORROWED from W3C Decentralized Identifiers (DID Core). - the remaining values are LOCAL (vendor/DISCOM master keys, e.g. METER_SERIAL, FEEDER, SUBSTATION, CONSUMER_NUMBER). |
| `value` | text | — | Mandatory | — |
| `namespace` | text | — | Optional | — |

### TimePeriod

| Field | Type | Standard | Status | Description |
|---|---|---|---|---|
| `start` | date-time | — | Mandatory | — |
| `duration` | duration | — | Mandatory | ISO-8601, e.g. PT2H. |

<!-- FIELD-TABLE:END -->
