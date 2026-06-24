# Outage Notification Schema — Design Note & Standards Survey

**Status:** Draft for discussion · **Date:** 2026-06-23
**Scope:** A standards-based, machine-readable schema for a DISCOM to publish **planned and unplanned outage** details — consumable as a website/outage-map feed (pull) and as push notifications to affected/subscribed consumers. Designed to be **GIS-ready** and **future-proof**.

This note is grounded in three authoritative inputs:
1. The live **UPPCL Outage Management System** (`1912.uppcl.org`) — screens reviewed: Breakdown-Shutdown entry, Main Dashboard (D11), Workforce Supply-Complaints dashboard (D07), Breakdown Details, Lineman-Allocation modal. This is the **system of record** and drives the field model.
2. The published **PVVNL "Detail of Planned Shutdown"** PDF (the public artifact today).
3. Global standards (§3) and existing **IES schema conventions** (`MeterData/v0.6`).

---

## 1. Problem & requirements

One canonical object that:

1. Describes a **planned** shutdown, an **unplanned/breakdown** outage, and a **restoration** event.
2. Is **published on the website / outage map** in machine-readable form — a *pull* feed.
3. Can be **pushed to affected/subscribed consumers** (SMS/app/email/IVR) — a *push* alert.
4. Models the outage at **feeder / DT / substation granularity**, matching what the MDMS produces from real-time substation smart-meter alarms.
5. Carries a clean **lifecycle** (scheduled → active → restored / cancelled) and a stable notice **identity** so updates/cancellations refer back to the original.
6. Where auto-detected, carries **provenance** back to the smart-meter alarm that triggered it — i.e. links to the IES `MeterData` `AlarmProfile`.
7. Is **GIS-ready**: every asset and affected area can carry or reference geometry so the same payload renders directly on an outage map (§6).
8. Is **future-proof**: additive enums, namespaced extensions, versioned per the IES family layout (§4).

---

## 2. Source artifacts decoded (authoritative)

### 2.1 UPPCL OMS — the system of record (from screenshots)

**Org hierarchy (confirmed, deeper than the PDF):**
`Discom → Zone → Circle → Division → Subdivision → Substation → Feeder / DT`
(e.g. PVVNL → Meerut-1 → EUDC-Meerut → EUDD-1 Meerut → EUDSD-8 Meerut → Transport Nagar → 11kV feeder.) **Note the `Subdivision` level** between Division and Substation.

**Outage classification — "Down Info":** the dashboards group outages as **SD / BD / RS**. Interpreted as **S**cheduled (planned maintenance) / **B**reak**D**own (unplanned fault) / **R**oster **S**hutdown — where *roster* is UPPCL's term for **scheduled rotational load-shedding** on a published rota (UPPCL publishes a "Rostering Schedule"). _[confirm exact legend with UPPCL — RS is **not** "Restoration"; restoration is a `status` transition, not a class.]_

**"Down Type" (asset level of the outage):** `FEEDER` (FDR) · `SUBSTATION` (SS) · `DT` (distribution transformer).

**Two distinct "type" axes — keep them separate:**
- **Voltage / fault level:** `33KV` · `11KV` · `DT` · `LT` (Dashboard: "33 KV Faults / 11 KV Faults / DT Fault / LT Fault").
- **Consumer category** (PVVNL sheet's "Feeder Type"): `URBAN` · `RURAL` · `AGRICULTURE` · `INDUSTRIAL` · `TEHSEEL` · `INDEPENDENT`.

**Cause taxonomy — authoritative `Fault Type → Fault SubType`** (from the Lineman-Allocation dropdown and Faults grid):

| Fault Type | Fault SubType (observed) |
|---|---|
| 11 KV | 11 KV incomer fault · Breaker Fault · Underground cable fault · Overhead conductor fault · Low/High Voltage Information · Major Power Failure · Period of Scheduled Outage |
| DT | Fuse off · DT Damage |
| 33 KV / LT | (same family, asset-specific) |

**Grouping:** one **Breakdown/Shutdown ID** spans **multiple feeders** under a substation (Breakdown Details: ID `6357257` → feeders *barehta, Gosaiganj, Jaisinghpur(R), Kurebhar(R)* under substation BHATMAI, all `Down From 22-Jun 06:43 → Down To 22-Jun 11:43`). → the schema models **one notice with an `affectedAssets[]` array**.

**Operational fields present in the OMS (carry these so the notice is complete):**
- `Down Date`, `Down Start Time`, `Down Hours/Minutes` (duration), `Down From` / `Down To`.
- `Estimated Time (in Minutes)` → ETR.
- `SLA (HH:MM)` with a **≤4 hrs / >4 hrs** threshold (Dashboard buckets: Feeder Breakdown 121 ≤4h / 1723 >4h; Planned Outages 366 ≤4h / 1080 >4h).
- `Force Majeure` (boolean).
- `Back-Feed given` (boolean) — partial restoration via alternate feed.
- `Call By` / `Created By` (who reported/raised).
- `Status` — `Pending`, `Resource Allocated`, … and lineman/`Resource` allocation.
- Complaint linkage — `Complaint No.`, `Complaint Type` (e.g. NO SUPPLY), `Priority`, `Priority Remarks` (e.g. DT Failure), `Outage Type` (e.g. Area), `No. of Complaints`, `District`, `Address`, `Landmark`.

### 2.2 PVVNL published sheet → already mapped in §8.1. Net new vs the OMS: nothing — the PDF is a flattened public projection of the OMS.

---

## 3. Global best-practices survey

No single dominant "outage publication" schema exists; mature practice **composes** several standards. Each contributes a layer.

### 3.1 IEC 61968-3 (CIM) — canonical *data model*
`IEC 61968-3:2021` defines CIM message profiles for distribution network operations. The 2021 edition split the old `OutagesAndFaults` into **`PlannedOutages`**, **`PlannedOutageNotifications`**, **`UnplannedOutages`**, **`EquipmentFaults`**, **`LineFaults`**. `UnplannedOutages` carries lists of **energized / de-energized `UsagePoints`** — exactly "which connections are affected", against CIM `Outage`/`UsagePoint`/`Equipment`. Align *names and semantics* here (Outage, cause, period, affected UsagePoints, planned vs unplanned) without putting heavyweight CIM XML on the wire.

### 3.2 ODIN — *publication / interop* pattern (closest analogue)
The **Outage Data Initiative Nationwide** (US DOE Office of Electricity + Oak Ridge National Lab) is the most direct precedent for this exact use case — a standardized way for many utilities to **publish** outage data instead of scattering it across web pages and social media. Copy: **JSON + XML**; an **anonymous/public API** (coarse — US uses FIPS county) **plus** an **authenticated API** (finer granularity for designated stakeholders) — maps to our "public webpage feed" vs "authorized data-share"; a **subscribe** model for push; and the pragmatic **coded *and* free-text cause** (real causes exceed any closed enum).

### 3.3 OASIS CAP v1.2 (ITU-T X.1303) — *push alert* envelope
The **Common Alerting Protocol** is the global all-hazard public-warning standard, explicitly inclusive of power outages. Use it for **push-to-subscribers**. Its `alert → info → area → resource` structure gives, for free: stable `identifier`, `sender`, `sent`, `status`, `msgType` (**Alert / Update / Cancel**), `references` (link an update to the original), `urgency / severity / certainty`, `effective / onset / expires`, `headline / description / instruction`, and **`area` with `polygon` / `circle` / `geocode`** (a GIS-native alerting geometry). Map the schema 1:1 to CAP so a CAP feed is generated mechanically.

### 3.4 MultiSpeak — *internal OMS/AMI/MDMS integration* reference
**MultiSpeak** (NRECA) outage interfaces — **OD** (outage detection from AMI), **OA** (outage analysis/OMS), **CB/CH** (customer calls), `ODEventNotification` (AMI device-status change) — describe the upstream flow that the UPPCL screens implement: **AMI/MDMS detects feeder outage from meter alarms → OMS confirms → notice published.** Validates the provenance link (alarm → outage).

### 3.5 GIS / outage-map de-facto practice
- **UK – UK Power Networks Open Data "Live Faults"**: near-real-time planned + unplanned power cuts streamed from their ADMS, consumable via **API and as a geospatial dataset** — the reference pattern for a public, GIS-ready outage feed. (ENA is the industry body; there is no single ENA-wide API — each DNO publishes.)
- **US outage maps** (PG&E etc.) and ODIN render at county/polygon level — confirms **polygon service-areas + point assets** as the rendering primitives.
- **GeoJSON (RFC 7946)** is the lingua franca for web maps; **WGS84 / EPSG:4326** is the expected CRS. The schema therefore uses GeoJSON geometry and can emit a **GeoJSON `FeatureCollection`** directly (§6).

### 3.6 Reliability / regulatory reporting (downstream consumers)
- **IEEE 1366** — reliability indices SAIDI / SAIFI / CAIDI / MAIFI; the outage records are the *source data*. Keep `actualRestoration` + affected-customer counts so indices are computable.
- **India context (important for this deployment):** CEA reports SAIFI/SAIDI/ASAI; **RDSS** mandates smart metering and is the lever for reliability improvement; SERCs (e.g. MPERC) now specify SAIFI/SAIDI trajectories for towns ≥1 lakh population. Independent review notes only ~17/36 DISCOMs use SAIFI/SAIDI — **most still publish interruptions by date/time with no affected-customer count.** A schema that captures affected-customer counts and restoration times directly upgrades India's reliability reporting. Smart-meter-driven feeder outage detection (this project) is exactly the RDSS direction.
- **US – DOE OE-417 / EIA** emergency-incident reporting — confirms the regulatory need to publish major outages in a structured form.
- **EU – ENTSO-E Transparency Platform** — mandatory publication of planned/forced unavailability (transmission level, ENTSO-E's own format).

### 3.7 What we borrow

| Standard | Layer | What we take |
|---|---|---|
| IEC 61968-3 CIM | Data model | Outage/UsagePoint semantics; planned vs unplanned split; affected-UsagePoints |
| ODIN | Publication & interop | JSON+XML; public + authenticated tiers; subscribe/push; coded+free-text cause |
| OASIS CAP v1.2 | Push envelope | identifier/status/msgType/references; severity/urgency; **area+polygon**; headline/instruction |
| MultiSpeak | Internal integration | alarm→detection→OMS→notice flow; AMI provenance |
| UKPN Open Data / GeoJSON | GIS feed | live planned+unplanned API; **GeoJSON FeatureCollection**, WGS84 |
| IEEE 1366 + CEA/RDSS | Downstream KPI | restoration time + customer counts for SAIDI/SAIFI |

---

## 4. Design principles

**IES alignment** (see `feedback_schema_reusability`): JSON Schema **draft 2020-12**, single `schema.json` with `$defs`, full 6-file family layout (`schema.json`, `attributes.yaml`, `context.jsonld`, `vocab.jsonld`, `examples/`, `README.md`); **`Identifier {scheme,value,namespace}`** for every reference; **`TimePeriod {start,duration}`** as the one canonical time model; domain-neutral naming; **discriminator-on-`const`** (`outageClass`) mirroring `MeterData`'s `profileType`; provenance reuses `MeterData` `AlarmProfile`/`MeterAlarm` rather than redefining alarms.

**GIS-ready** (§6): geometry is optional everywhere but first-class — point (substation/DT), LineString (feeder route), Polygon/MultiPolygon (service area); reference-by-id so geometry can be resolved from a GIS layer instead of restated; emit GeoJSON `FeatureCollection`; WGS84.

**Future-proof:**
- **Additive enums** — closed vocabularies (`outageClass`, `assetLevel`) stay small and stable; open ones (`cause.code`, `category`) are *suggested* lists with an `OTHER` + free-text escape hatch (ODIN principle).
- **`extensions` bag** — a namespaced object for DISCOM-specific fields (e.g. `uppcl.breakdownId`, `slaTier`) without schema churn.
- **Versioned** per IES (`/OutageNotification/v0.1/…`); breaking changes go to a sibling version dir.
- **Asset model is generic** (`assetLevel` + `Identifier`) so feeder/DT/substation/transformer/line all fit one shape, and new asset levels are additive.

---

## 5. Proposed schema — `OutageNotification`

### 5.1 Object model

```
OutageNotification
├── id                  Identifier         notice identity (stable across updates)
├── outageClass         PLANNED|BREAKDOWN|SCHEDULED_ROSTERING|EMERGENCY_ROSTERING  (OMS Down Info)
├── status              SCHEDULED|ACTIVE|PARTIALLY_RESTORED|RESTORED|CANCELLED
├── msgType             ALERT|UPDATE|CANCEL                           (CAP)
├── references[]        Identifier         prior notice ids superseded (CAP references)
├── severity            EXTREME|SEVERE|MODERATE|MINOR|UNKNOWN          (CAP)
├── category            MAINTENANCE|UPGRADE|FAULT|LOAD_SHEDDING|WEATHER|SAFETY|OTHER
├── cause               { category (IES taxonomy, informed by IEEE 1782), code (vendor verbatim), codeNamespace?, faultType?, text }
├── forceMajeure        boolean
├── issuedBy            Party
├── issuedAt / lastUpdatedAt / detectedAt   date-time
├── network             NetworkContext     zone/circle/division/subdivision/substation
├── affectedAssets[]    Asset              feeder | DT | substation (+ meterRef + geo)
├── affectedArea        AffectedArea       text + adminAreas[] + geo (GeoJSON)
├── impact              { customersAffected, energized?, deEnergized?[] }  (CIM UsagePoints)
├── timing              { period, estimatedRestoration, actualRestoration, slaTargetMinutes }
├── response            { backFeedGiven, resourceStatus, complaintCount }
├── publicInfo          { headline, description, instruction, language }  (CAP info)
├── provenance          { source, alarmRefs[] }   link to MeterData AlarmProfile (MDMS)
└── extensions          object             namespaced DISCOM-specific fields
```

### 5.2 `schema.json` (core — draft 2020-12)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/schema.json",
  "title": "OutageNotification Payload",
  "description": "A planned or unplanned electricity outage notice, publishable as a web/outage-map feed or pushed to affected consumers.",
  "oneOf": [
    { "$ref": "#/$defs/OutageNotification" },
    { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/OutageNotification" } }
  ],
  "$defs": {
    "OutageNotification": {
      "type": "object",
      "required": ["id", "outageClass", "status", "affectedAssets", "timing"],
      "properties": {
        "id": { "$ref": "#/$defs/Identifier", "description": "Stable notice identity; reused across UPDATE/CANCEL." },
        "outageClass": { "type": "string", "enum": ["PLANNED", "BREAKDOWN", "SCHEDULED_ROSTERING", "EMERGENCY_ROSTERING"], "description": "LOCAL enum — OMS 'Down Info' value set (confirmed from UPPCL BDSD export)." },
        "status": { "type": "string", "enum": ["SCHEDULED", "ACTIVE", "PARTIALLY_RESTORED", "RESTORED", "CANCELLED"] },
        "msgType": { "type": "string", "enum": ["ALERT", "UPDATE", "CANCEL"], "default": "ALERT", "description": "CAP msgType." },
        "references": { "type": "array", "items": { "$ref": "#/$defs/Identifier" }, "description": "Prior notice ids this message updates/cancels (CAP references)." },
        "severity": { "type": "string", "enum": ["EXTREME", "SEVERE", "MODERATE", "MINOR", "UNKNOWN"], "default": "UNKNOWN" },
        "category": { "type": "string", "enum": ["MAINTENANCE", "UPGRADE", "FAULT", "LOAD_SHEDDING", "WEATHER", "SAFETY", "OTHER"] },
        "cause": {
          "type": "object",
          "description": "Cause category (IES taxonomy, informed by IEEE 1782) + vendor code (verbatim) + free text (ODIN).",
          "properties": {
            "category": { "type": "string", "enum": ["PLANNED", "EQUIPMENT_FAILURE", "WEATHER", "VEGETATION", "ANIMAL", "HUMAN_THIRD_PARTY", "OVERLOAD", "UPSTREAM_GRID", "LOAD_SHEDDING_ROSTER", "UNKNOWN", "OTHER"], "description": "IES taxonomy, informed by IEEE 1782-2022 (used with IEEE 1366). IEEE normative list is paywalled; values NOT verified against it — reconcile before claiming conformance." },
            "faultType": { "type": "string", "description": "e.g. 33KV, 11KV, DT, LT." },
            "code": { "type": "string", "description": "Vendor FAULT_REASON carried VERBATIM (vendor-defined, not standardized); map to category." },
            "codeNamespace": { "type": "string", "description": "Authority/vendor that defines `code`." },
            "text": { "type": "string", "description": "Free-text reason; may be localized (e.g. Hindi)." }
          }
        },
        "forceMajeure": { "type": "boolean", "description": "OMS 'Force Majeure' flag." },
        "issuedBy": { "$ref": "#/$defs/Party" },
        "issuedAt": { "type": "string", "format": "date-time" },
        "detectedAt": { "type": "string", "format": "date-time", "description": "When MDMS/SCADA first detected (unplanned)." },
        "lastUpdatedAt": { "type": "string", "format": "date-time" },
        "network": { "$ref": "#/$defs/NetworkContext" },
        "affectedAssets": { "type": "array", "minItems": 1, "items": { "$ref": "#/$defs/Asset" } },
        "affectedArea": { "$ref": "#/$defs/AffectedArea" },
        "impact": {
          "type": "object",
          "description": "CIM-aligned affected service points + customer counts (for SAIDI/SAIFI).",
          "properties": {
            "customersAffected": { "type": "integer", "minimum": 0 },
            "deEnergized": { "type": "array", "items": { "$ref": "#/$defs/Identifier" }, "description": "Optional SDP/UsagePoint refs (authenticated tier)." },
            "energized": { "type": "array", "items": { "$ref": "#/$defs/Identifier" } }
          }
        },
        "timing": {
          "type": "object",
          "required": ["period"],
          "properties": {
            "period": { "$ref": "#/$defs/TimePeriod", "description": "Outage window (Down From + duration)." },
            "estimatedRestoration": { "type": "string", "format": "date-time", "description": "ETR (OMS 'Estimated Time')." },
            "actualRestoration": { "type": "string", "format": "date-time", "description": "Set on RESTORED; feeds IEEE 1366 indices." },
            "slaTargetMinutes": { "type": "integer", "minimum": 0, "description": "SLA target, e.g. 240 (4 hrs)." }
          }
        },
        "response": {
          "type": "object",
          "properties": {
            "backFeedGiven": { "type": "boolean", "description": "Partial restoration via alternate feed (OMS 'Back-Feed given')." },
            "resourceStatus": { "type": "string", "description": "e.g. PENDING, RESOURCE_ALLOCATED, IN_PROGRESS." },
            "complaintCount": { "type": "integer", "minimum": 0, "description": "Linked consumer complaints (OMS 'No. of Complaints')." }
          }
        },
        "publicInfo": {
          "type": "object",
          "description": "CAP info block — human-readable text for web publishing and push.",
          "properties": {
            "language": { "type": "string", "description": "BCP-47, e.g. en, hi." },
            "headline": { "type": "string" },
            "description": { "type": "string" },
            "instruction": { "type": "string", "description": "What the consumer should do." }
          }
        },
        "provenance": {
          "type": "object",
          "description": "Link to the smart-meter alarm(s)/signal that triggered/confirmed the outage.",
          "properties": {
            "source": { "type": "string", "enum": ["MDMS", "OMS", "SCADA", "AMI", "MANUAL"], "description": "System that raised this notice." },
            "amispCode": { "type": "string", "description": "AMI Service Provider that supplied the detection signal (from the feeder-status ingest API)." },
            "signal": {
              "type": "object",
              "description": "Raw real-time feeder-status signal that triggered detection (see §7.4).",
              "properties": {
                "eventId": { "type": "string", "description": "Idempotency key of the originating feeder-status event." },
                "feederStatus": { "type": "string", "enum": ["ENERGIZED", "DE_ENERGIZED", "UNKNOWN"], "description": "Normalized; raw vendor code preserved in rawCode." },
                "diPort": { "type": "string", "description": "Digital-input port on the substation meter that carried the signal." },
                "rawCode": { "type": "string", "description": "Vendor-native status code as received (e.g. FEEDER_STATUS=102), for traceability." }
              }
            },
            "alarmRefs": {
              "type": "array",
              "description": "References into MeterData AlarmProfile records.",
              "items": {
                "type": "object",
                "required": ["meterRef"],
                "properties": {
                  "meterRef": { "$ref": "#/$defs/Identifier" },
                  "alarmId": { "type": "integer", "minimum": 1 },
                  "timestamp": { "type": "string", "format": "date-time" }
                }
              }
            }
          }
        },
        "extensions": { "type": "object", "description": "Namespaced DISCOM-specific fields, e.g. { \"uppcl\": { \"breakdownId\": \"6357257\" } }." }
      }
    },

    "Asset": {
      "type": "object",
      "description": "A network asset affected by the outage. Generic across feeder/DT/substation/line.",
      "required": ["id", "assetLevel"],
      "properties": {
        "id": { "$ref": "#/$defs/Identifier", "description": "Asset id/name; ideally a stable GIS feature id / MRID for map join." },
        "assetLevel": { "type": "string", "enum": ["SUBSTATION", "FEEDER", "DT", "LINE_SEGMENT", "SERVICE_POINT"] },
        "voltageLevel": { "type": "string", "description": "33kV, 11kV, LT, DT." },
        "consumerCategory": { "type": "string", "enum": ["URBAN", "RURAL", "AGRICULTURE", "INDUSTRIAL", "MIXED", "OTHER"], "description": "PVVNL 'Feeder Type'." },
        "meterRef": { "$ref": "#/$defs/Identifier", "description": "Feeder/substation smart-meter number — join key to MDMS/MeterData." },
        "parentRef": { "$ref": "#/$defs/Identifier", "description": "Parent asset (e.g. feeder's substation, DT's feeder)." },
        "geo": { "$ref": "#/$defs/GeoJSONGeometry", "description": "Optional inline geometry: Point (substation/DT), LineString (feeder), Polygon (service area)." }
      }
    },

    "NetworkContext": {
      "type": "object",
      "description": "DISCOM org hierarchy (UPPCL): Discom > Zone > Circle > Division > Subdivision > Substation. All optional for flat utilities.",
      "properties": {
        "discom": { "$ref": "#/$defs/Identifier" },
        "zone": { "type": "string" },
        "circle": { "type": "string" },
        "division": { "type": "string" },
        "subdivision": { "type": "string" },
        "substation": { "$ref": "#/$defs/Identifier" },
        "district": { "type": "string" }
      }
    },

    "AffectedArea": {
      "type": "object",
      "description": "CAP area block — text + structured admin areas + geometry (GIS-ready).",
      "properties": {
        "text": { "type": "string", "description": "Free-text localities (CAP areaDesc), e.g. 'SEC-14, 9, 11 Rajnagar'." },
        "adminAreas": { "type": "array", "items": { "type": "string" }, "description": "Named localities/wards/villages." },
        "geo": { "$ref": "#/$defs/GeoJSONGeometry", "description": "Polygon/MultiPolygon service area, or Point/circle (CAP). WGS84." }
      }
    },

    "Party": {
      "type": "object",
      "properties": {
        "id": { "$ref": "#/$defs/Identifier" },
        "name": { "type": "string" },
        "contact": { "type": "string", "description": "Phone/email/URL (e.g. 1912)." }
      }
    },

    "Identifier": {
      "type": "object",
      "required": ["scheme", "value"],
      "properties": {
        "scheme": { "type": "string", "enum": ["METER_SERIAL", "MRID", "GIS_FEATURE_ID", "SERVICE_DELIVERY_POINT", "FEEDER", "SUBSTATION", "DT", "CONSUMER_NUMBER", "ORG", "DID", "OTHER"] },
        "value": { "type": "string" },
        "namespace": { "type": "string" }
      }
    },

    "TimePeriod": {
      "type": "object",
      "required": ["start", "duration"],
      "properties": {
        "start": { "type": "string", "format": "date-time" },
        "duration": { "type": "string", "format": "duration", "description": "ISO-8601, e.g. PT2H. End is derived." }
      }
    },

    "GeoJSONGeometry": {
      "$ref": "https://schema.beckn.io/GeoJSONGeometry/v2.0/attributes.yaml#/components/schemas/GeoJSONGeometry"
    }
  }
}
```

### 5.3 Example — planned shutdown (one UPPCL Breakdown ID, multiple feeders, GIS-ready)

```json
{
  "id": { "scheme": "OTHER", "value": "PVVNL-BD-6357257", "namespace": "1912.uppcl.org" },
  "outageClass": "PLANNED",
  "status": "SCHEDULED",
  "msgType": "ALERT",
  "category": "MAINTENANCE",
  "cause": { "code": "SCHEDULED_OUTAGE", "text": "Pole erection on long span & VCB replacement under Business Plan" },
  "forceMajeure": false,
  "issuedBy": { "name": "PVVNL", "contact": "1912" },
  "issuedAt": "2026-06-21T18:00:00+05:30",
  "network": { "zone": "Muzaffarnagar", "circle": "EDC-2 Muzaffarnagar", "division": "EDD-Budhana", "substation": { "scheme": "SUBSTATION", "value": "BHATMAI" } },
  "affectedAssets": [
    { "id": { "scheme": "FEEDER", "value": "barehta" }, "assetLevel": "FEEDER", "voltageLevel": "11kV", "consumerCategory": "RURAL", "geo": { "type": "Point", "coordinates": [77.45, 29.41] } },
    { "id": { "scheme": "FEEDER", "value": "Gosaiganj" }, "assetLevel": "FEEDER", "voltageLevel": "11kV", "consumerCategory": "RURAL" },
    { "id": { "scheme": "FEEDER", "value": "Jaisinghpur(R)" }, "assetLevel": "FEEDER", "voltageLevel": "11kV", "consumerCategory": "RURAL" },
    { "id": { "scheme": "FEEDER", "value": "Kurebhar(R)" }, "assetLevel": "FEEDER", "voltageLevel": "11kV", "consumerCategory": "RURAL" }
  ],
  "affectedArea": { "text": "Villages under BHATMAI substation", "adminAreas": ["Barehta", "Gosaiganj", "Jaisinghpur", "Kurebhar"], "geo": { "type": "Polygon", "coordinates": [[[77.43,29.39],[77.48,29.39],[77.48,29.44],[77.43,29.44],[77.43,29.39]]] } },
  "timing": { "period": { "start": "2026-06-22T06:43:00+05:30", "duration": "PT5H" }, "slaTargetMinutes": 240 },
  "publicInfo": { "language": "en", "headline": "Planned shutdown — BHATMAI substation feeders, 22 Jun 06:43–11:43", "instruction": "Please plan for a ~5-hour interruption." },
  "extensions": { "uppcl": { "breakdownId": "6357257", "downType": "FEEDER" } }
}
```

### 5.4 Example — unplanned breakdown auto-raised from a smart-meter alarm (provenance)

```json
{
  "id": { "scheme": "OTHER", "value": "PVVNL-BD-6562139", "namespace": "1912.uppcl.org" },
  "outageClass": "BREAKDOWN",
  "status": "ACTIVE",
  "severity": "SEVERE",
  "category": "FAULT",
  "cause": { "faultType": "11KV", "code": "INCOMER_FAULT", "text": "11 KV incomer fault" },
  "forceMajeure": false,
  "detectedAt": "2026-06-22T15:41:55+05:30",
  "network": { "substation": { "scheme": "SUBSTATION", "value": "Gharaaha" }, "district": "SULTANPUR" },
  "affectedAssets": [ { "id": { "scheme": "FEEDER", "value": "Gharaaha" }, "assetLevel": "FEEDER", "voltageLevel": "11kV", "meterRef": { "scheme": "METER_SERIAL", "value": "HP3008071" } } ],
  "impact": { "customersAffected": 1840 },
  "timing": { "period": { "start": "2026-06-22T15:41:55+05:30", "duration": "PT0S" }, "estimatedRestoration": "2026-06-22T18:42:00+05:30", "slaTargetMinutes": 240 },
  "response": { "backFeedGiven": false, "resourceStatus": "RESOURCE_ALLOCATED", "complaintCount": 28 },
  "provenance": {
    "source": "MDMS",
    "amispCode": "AMISP1001",
    "signal": { "eventId": "AMISP1001-Gharaaha-20260622T1541", "feederStatus": "DE_ENERGIZED", "diPort": "DI1", "rawCode": "102" },
    "alarmRefs": [ { "meterRef": { "scheme": "METER_SERIAL", "value": "HP3008071" }, "alarmId": 7, "timestamp": "2026-06-22T15:41:55+05:30" } ]
  }
}
```

`provenance.alarmRefs[]` point at a `MeterData` `AlarmProfile` (`profileType: "ALARM"`, `MeterAlarm.alarmId/status/severity`) already carried by [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) — no alarm fields are redefined here.

---

## 6. GIS / outage-map readiness

Designed so the **same payload renders on a map** without a second data model:

1. **Geometry is first-class but optional.** `Asset.geo` and `AffectedArea.geo` use GeoJSON (RFC 7946), **WGS84 / EPSG:4326** — directly consumable by Leaflet / Mapbox / Google Maps.
2. **Geometry types per asset level:** Point (substation, DT), LineString (feeder route), Polygon / MultiPolygon (service area / affected zone), circle (CAP alerting).
3. **Reference-by-id, resolve-from-GIS.** Every asset carries a stable `Identifier` (`GIS_FEATURE_ID` / `MRID`). A consumer that already has the DISCOM's GIS layer can **join on id and pull geometry from GIS** instead of the notice restating it — keeps notices small and the GIS authoritative. Inline `geo` is the fallback when the consumer has no GIS.
4. **Direct GeoJSON output mode.** `GET /outages.geojson` returns a **`FeatureCollection`**, one `Feature` per affected asset/area, with outage attributes (class, status, ETR, customersAffected) in `properties` — drop-in for an outage map and for heatmaps weighted by `impact.customersAffected`.
5. **Affected-area derivation.** Where only point assets exist today, `affectedArea.geo` can be omitted and rendered as substation/feeder points; as GIS service-area polygons mature, the same field upgrades to polygons with no schema change.
6. **Future-proofing for maps:** `extensions` can carry tile/style hints; additive `assetLevel` values (e.g. `RING_MAIN_UNIT`) require no breaking change; CRS is fixed to WGS84 to avoid projection ambiguity.

---

## 7. Delivery patterns

### 7.1 Pull — OpenAPI feed for the website / outage map
```
GET /outages              ?status=ACTIVE,SCHEDULED &class=PLANNED,BREAKDOWN &from &to &substation &feederMeter
GET /outages/{id}                       single notice (+ UPDATE/CANCEL history via references)
GET /outages.geojson                    FeatureCollection for the outage map (§6)
GET /outages.cap.xml                    same set rendered as a CAP feed (alerting networks)
GET /outages/lookup?sdp=... | ?lat=&lon=  outages affecting a given connection / location
```
- **Public tier** = coarse (feeder/area + counts), no PII — ODIN anonymous-API analogue.
- **Authenticated tier** = adds `impact.deEnergized[]` and consumer refs — ODIN authenticated-API analogue.

### 7.2 Push — to affected/subscribed consumers
1. **CAP message/feed** for alerting infrastructure (cell broadcast, app push, SMS, IVR). Schema maps 1:1 to CAP (§8.2) → generated mechanically.
2. **Webhook/subscription** in IES style — consumers subscribe by service-delivery-point, substation, or **geo (point-in-polygon)**; DISCOM POSTs the `OutageNotification` on `ALERT`/`UPDATE`/`CANCEL`. Mirrors the existing IES data-exchange webhook pattern.

### 7.3 Optional — Verifiable Credential wrapper
For tamper-evidence / cross-network trust (consistent with `MeterDataCredential`), wrap as a W3C VC (`OutageNotificationCredential`) issued by the DISCOM DID. Optional; bare JSON suffices for web publishing.

### 7.4 Feeder-status ingest (detection layer)

Publication is fed by a thin **detection / ingest** layer, kept separate from publication. An **AMI Service Provider (AMISP)** posts a real-time feeder energized/de-energized signal — derived from a substation meter's **digital-input (DI) port** — to the central platform (MDMS/OMS). The OMS correlates consecutive signals per feeder, enriches them (cause, hierarchy, area, geometry, customer count), and emits an `OutageNotification`. The published notice's `provenance` carries `amispCode` + `signal.eventId` + `signal.rawCode`, so every public outage is traceable to its originating meter signal. Full contract: [`FeederStatusIngest.openapi.yaml`](./FeederStatusIngest.openapi.yaml).

**Contract principles:**
- **Named status enums** (`ENERGIZED`/`DE_ENERGIZED`/`UNKNOWN`); the raw vendor code is preserved in `rawStatus`. Vendor status codes are not standardized — the standard layer is IS 15959 / DLMS-COSEM (OBIS + event codes), which `MeterData` `AlarmProfile.alarmId` aligns to.
- **RFC 3339 timestamps with offset** (e.g. `2025-07-23T00:31:00+05:30`) — outage timing drives SLA/ETR math.
- **Bearer-token auth + a single `discomCode` tenant.**
- **Substation + feeder identification** (`substationCode` = the draft's SID, `feederCode`) — supports both feeder- and substation-level events and groups a cascaded trip by substation.
- **Client-supplied `eventId`** for idempotency / de-duplication of replayed signals.
- **Batch array input** — a substation trip cascades many feeders at once; the ack returns per-item results with typed error codes.
- **Optional `outageRef`** so a restoration (ENERGIZED) ties back to its onset (DE_ENERGIZED).

```jsonc
// POST /feeder-status   Authorization: Bearer <token>
[
  {
    "eventId": "AMISP1001-24391110044ALG-20250723T0031",   // idempotency key
    "discomCode": "1001",
    "substationCode": "517",              // SID = substation id
    "amispCode": "AMISP1001",
    "feederCode": "24391110044ALG",
    "feederStatus": "DE_ENERGIZED",       // normalized
    "rawStatus": { "feederStatus": "102", "diPortStatus": "402" },  // vendor codes preserved
    "eventTimestamp": "2025-07-23T00:31:00+05:30",          // RFC 3339 + offset
    "diPort": "DI1"
  }
]
// -> { "accepted": 1, "results": [ { "eventId": "...", "status": "OK" } ] }
```

**End-to-end flow:**
`AMISP → POST /feeder-status` → MDMS/OMS correlates consecutive DE_ENERGIZED/ENERGIZED events per feeder, enriches them → emits **`OutageNotification`** on `/outages`, `/outages.geojson`, CAP, and webhooks → consumers / outage map.

> This ingest contract was informed by a draft "REAL TIME FEEDER STATUS" push API contemplated by the DISCOM — see §11 References.

---

## 8. Mapping tables

### 8.1 UPPCL OMS / PVVNL sheet → schema
| OMS / PDF field | Schema path |
|---|---|
| Down Info (Planned/Breakdown/Scheduled Rostering/Emergency Rostering) | `outageClass` |
| Down Type (Feeder/Substation/DT) | `affectedAssets[].assetLevel` (+ `extensions.uppcl.downType`) |
| Discom/Zone/Circle/Division/Subdivision/Substation/District | `network.*` |
| Feeder / DT name | `affectedAssets[].id` |
| Feeder Smart Meter Number | `affectedAssets[].meterRef` (scheme `METER_SERIAL`) |
| Feeder Type = 11KV/33KV/LT | `affectedAssets[].voltageLevel` (and `cause.faultType`) |
| Feeder Type = Urban/Rural/Agriculture (PDF) | `affectedAssets[].consumerCategory` |
| Down Date + Start Time + Down Hours/Min · Down From/To | `timing.period` (start + duration) |
| Fault Type → Fault SubType | `cause.faultType` → `cause.code` |
| Reason / Remarks (incl. Hindi) | `cause.text` |
| Force Majeure | `forceMajeure` |
| Estimated Time (Minutes) | `timing.estimatedRestoration` |
| SLA (HH:MM) / ≤4hr threshold | `timing.slaTargetMinutes` |
| Back-Feed given | `response.backFeedGiven` |
| Status (Pending/Resource Allocated) | `response.resourceStatus` |
| No. of Complaints | `response.complaintCount` |
| Consumer Affected Area (localities) | `affectedArea.text` / `affectedArea.adminAreas[]` |
| Breakdown ID (groups feeders) | `extensions.uppcl.breakdownId` |

### 8.2 Schema → OASIS CAP v1.2
| Schema | CAP |
|---|---|
| `id` | `alert.identifier` |
| `issuedBy` / `issuedAt` | `alert.sender` / `alert.sent` |
| `msgType` | `alert.msgType` (Alert/Update/Cancel) |
| `references` | `alert.references` |
| `category` | `info.category` (Infra) + `info.event` |
| `severity` | `info.severity` |
| `timing.period.start` / `timing.estimatedRestoration` | `info.onset`(effective) / `info.expires` |
| `publicInfo.headline/description/instruction` | `info.headline/description/instruction` |
| `affectedArea.text` | `area.areaDesc` |
| `affectedArea.geo` (Polygon/Point) | `area.polygon` / `area.circle` |

### 8.3 Schema → IEC 61968-3 CIM
| Schema | CIM |
|---|---|
| `OutageNotification` (PLANNED) | `PlannedOutage` / `PlannedOutageNotification` |
| `OutageNotification` (BREAKDOWN) | `UnplannedOutage` (`Outage`) |
| `impact.deEnergized[]` / `impact.energized[]` | `Outage.deEnergizedUsagePoint` / `energizedUsagePoint` |
| `cause` | `Outage.cause` |
| `timing.period` / `actualRestoration` | `Outage.estimatedPeriod` / `actualPeriod` |
| `affectedAssets[]` | `Equipment` / `Feeder` refs |

---

## 9. Controlled vocabularies — and their provenance

Every enum declares whether it is **borrowed from a standard** (anchored to the standard's term IRI in `context.jsonld`) or **local**:

| Enum | Origin |
|------|--------|
| `msgType` | **Borrowed** — OASIS CAP v1.2 `alert/msgType` |
| `severity` | **Borrowed** — OASIS CAP v1.2 `info/severity` |
| `cause.category` | **Local taxonomy, informed by** IEEE 1782-2022 (with IEEE 1366) — IEEE normative list paywalled, values **not verified** against it: `PLANNED · EQUIPMENT_FAILURE · WEATHER · VEGETATION · ANIMAL · HUMAN_THIRD_PARTY · OVERLOAD · UPSTREAM_GRID · LOAD_SHEDDING_ROSTER · UNKNOWN · OTHER` |
| `Identifier.scheme` | **Mixed** — `MRID` (CIM IEC 61968/61970), `DID` (W3C DID Core); rest local |
| `feederStatus` | **Local** normalization; energized/de-energized align with CIM UsagePoint |
| `outageClass` | **Local** — UPPCL OMS Down Info: `PLANNED · BREAKDOWN · SCHEDULED_ROSTERING · EMERGENCY_ROSTERING` |
| `cause.code` | **Local/vendor** — carried verbatim (vendor `FAULT_REASON`; not standardized) |
| `cause.faultType` | **Local** (open): `33KV · 11KV · DT · LT` |
| `assetLevel` | **Local** (closed, additive): `SUBSTATION · FEEDER · DT · LINE_SEGMENT · SERVICE_POINT` |
| `consumerCategory` | **Local** (open): `URBAN · RURAL · AGRICULTURE · INDUSTRIAL · MIXED · OTHER` (PDF `TEHSEEL`/`INDEPENDENT` → `OTHER` or extend) |
| `status`, `category`, `source` | **Local** — not from a published standard |

> `category` (outage category) is **not** CAP's `info/category` — deliberately a different value set.

### 9.1 UPPCL FAULT_REASON master → `cause.category` crosswalk

The UPPCL OMS carries a fault-reason pick-list (`FORM_ID 8312`, 31 codes). It is **operational and India-specific — not a published standard**, and contains duplicates (`13 Overload`≈`26 Overloading`; `20 System improvement`≈`29 …/Deposit Works`; transformer split across `3/4/10/11/23`). It maps onto the IES `cause.category` taxonomy (a pragmatic set informed by IEEE 1782-2022, **not verified against the paywalled IEEE normative list**): the vendor code is carried verbatim in `cause.code` (`codeNamespace: uppcl-oms`) and resolved to a category via the machine-readable crosswalk [`fault_reason_crosswalk.json`](./fault_reason_crosswalk.json). Examples:

| FAULT_REASON | `cause.code` | `cause.category` | `outageClass` |
|---|---|---|---|
| 11KV Line Fault | `6` | `EQUIPMENT_FAILURE` | `BREAKDOWN` |
| Tree fallen on line | `19` | `VEGETATION` | `BREAKDOWN` |
| Animal/bird dead on line | `17` | `ANIMAL` | `BREAKDOWN` |
| Overload / Overloading | `13` / `26` | `OVERLOAD` | `BREAKDOWN` |
| Rostering | `1` | `LOAD_SHEDDING_ROSTER` | `SCHEDULED_ROSTERING` |
| Other than Schedule Rostering | `28` | `LOAD_SHEDDING_ROSTER` | `EMERGENCY_ROSTERING` |
| Substation / Line / DT Maintenance | `9` / `15` / `30` | `PLANNED` | `PLANNED` |

Recommendation to the DISCOM: de-duplicate the master list, and treat the crosswalk's `category` as the published cross-DISCOM dimension while keeping the local code for fidelity.

---

## 10. Open questions
- Does the MDMS emit the **smart-meter alarm → unplanned-outage** linkage automatically, or is the OMS "Create New Fault" step manual? Sets which fields auto-populate.
- `cause.code` — adopt this OMS-seeded list as the canonical IES vocabulary, or keep purely free-text for v0.1?
- GIS source of truth: do feeders/DTs have geometry in a GIS today (for `geo` and `GIS_FEATURE_ID`), or only substation points? Drives §6 rollout.
- Privacy: granularity of `impact.deEnergized[]` on the public vs authenticated tier.
- **SD/BD/RS legend** — confirm with UPPCL that **RS = Roster Shutdown** (rotational load-shedding), as interpreted here, and not another controlled-outage category. Restoration is modelled as `status=RESTORED` (a transition / CAP `Update`), not as a class.
- **Vendor status codes** — feeder-status numeric values (e.g. `FEEDER_STATUS:102`, `DI_PORT_STATUS:402`) are **vendor/platform-specific, not a standard enum**. The standardised layer for Indian meters is **IS 15959 Part 1/2 (DLMS/COSEM, IEC 62056)** — OBIS codes + the standard event/alarm code list (which `MeterData` `AlarmProfile.alarmId` aligns to). Obtain the vendor's code legend and map it to the normalized `feederStatus` enum.

---

## 11. References
- **IEC 61968-3:2021** — Distribution management, network operations. <https://webstore.iec.ch/en/publication/67251>
- **CIM (electricity) overview** — <https://en.wikipedia.org/wiki/Common_Information_Model_(electricity)>
- **ODIN — Outage Data Initiative Nationwide** (US DOE/ORNL) — <https://odin.ornl.gov/> · Developer Guide: <https://odin.ornl.gov/downloadables/ODIN_Developer_Guide.pdf> · FAQ: <https://odin.ornl.gov/downloadables/ODIN_FAQ_3-9-22.pdf>
- **OASIS Common Alerting Protocol v1.2** (ITU-T X.1303) — <https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2-os.html> · <https://www.oasis-open.org/standard/cap/>
- **MultiSpeak** (NRECA, OD/OA outage interfaces) — <https://www.multispeak.org/>
- **UK Power Networks — Live Faults open dataset/API** — <https://ukpowernetworks.opendatasoft.com/explore/dataset/ukpn-live-faults/> · ENA — <https://www.energynetworks.org/customers/power-cut>
- **GeoJSON (RFC 7946)** — <https://datatracker.ietf.org/doc/html/rfc7946>
- **IEEE 1366** — Guide for Electric Power Distribution Reliability Indices (SAIDI/SAIFI/CAIDI/MAIFI).
- **IEEE 1782-2022** — Guide for Collecting, Categorizing, and Utilizing Information Related to Electric Power Distribution Interruption Events (defines ~10 cause categories with subcategories, used with IEEE 1366). **Normative cause list is paywalled** — our `cause.category` is informed by it but not verified; reconcile against the standard. Abstract/purchase: <https://standards.ieee.org/ieee/1782/10257/> · <https://ieeexplore.ieee.org/document/9882080>
- **W3C Decentralized Identifiers (DID) Core** — <https://www.w3.org/TR/did-core/>
- **India reliability/RDSS context** — MPERC SAIFI/SAIDI order: <https://mperc.in/uploads/editor/Other%20Orders%20by%20MPERC/MPERC_ORDER_Specifying_Reliability_Indices_SAIFI_AND_SAIDI_20_06_2024.pdf> · Review of Indian DISCOM outage reporting: <https://blog.theleapjournal.org/2025/09/a-review-of-outage-reporting-by-indian.html> · UPCL reliability indices: <https://upcl.uk.gov.in/reliability-indices-saifi-saidi-maifi/>
- **ENTSO-E Transparency Platform** — <https://transparency.entsoe.eu/>
- **IES MeterData v0.6** (carries smart-meter alarms via `AlarmProfile`) — <https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6>
- **UPPCL OMS** (`1912.uppcl.org`) — system of record reviewed for this design.
- **PVVNL planned-shutdown example** — <https://pvvnl.org/uploads/news/1782054913.pdf>
- **DISCOM draft "REAL TIME FEEDER STATUS" push API** — vendor-contemplated AMISP push contract that informed the feeder-status ingest layer (§7.4).
