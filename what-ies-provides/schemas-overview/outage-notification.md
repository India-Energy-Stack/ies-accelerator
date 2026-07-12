# OutageNotification v0.1

*A machine-readable payload a distribution licensee publishes to describe one planned or unplanned electricity outage, usable both as a public outage-map feed and as a push alert to affected consumers.*

| Field | Value |
|---|---|
| Document | IES/ON/0.1 |
| Status | Draft for technical review — the schema's own README and `attributes.yaml` `info.description` both mark it **"WORK IN PROGRESS — subject to change."** It is an early draft published for discussion; field names, enums and the SD/BD/RS interpretation are not final and may change without notice. Do not depend on it for production integrations yet. |
| Applicability | Issued by a distribution licensee (DISCOM), or a system acting on its behalf (an OMS, MDMS, SCADA, or a real-time data-acquisition system such as the DISCOM's RTDAS); consumed by outage-map/website feeds, subscribed consumers, mass-alerting networks, and downstream reliability reporting |
| This version | v0.1 covers the outage notice itself — class, cause, affected assets and area, timing, impact, response, public-facing text, and provenance back to the detecting smart-meter signal — defined in the companion JSON Schema file [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/schema.json). It is grounded directly in a live system of record (the DISCOM's Outage Management System at `discom.example`) and a published public artifact (the DISCOM's "Detail of Planned Shutdown" PDF), not designed in the abstract. |

## 1. Scope and Purpose

The stakeholders are the distribution licensee that must tell the public and its own field teams what is out, where, and for how long, and the consumers, subscribers and outage-map viewers who currently cannot get that information in a consistent, machine-readable form. A licensee's outage-management system (OMS) knows the moment a feeder trips or a shutdown is scheduled, but without a shared schema that knowledge stays locked inside the OMS — it cannot be republished automatically as a map feed, pushed as a subscriber alert, or linked back to the smart-meter reading that first detected it.

The design note behind this schema is explicit that no single dominant "outage publication" schema exists internationally — mature practice *composes* several standards, each contributing one layer (data model, publication pattern, push envelope, integration flow, reliability reporting). OutageNotification v0.1 is the result of that composition exercise, decoded from three authoritative inputs: the live OMS screens of a DISCOM (Breakdown-Shutdown entry, Main Dashboard, Workforce Supply-Complaints dashboard, Breakdown Details, Lineman-Allocation), the DISCOM's published planned-shutdown PDF (confirmed to be a flattened public projection of the same OMS data — nothing in the PDF is not already in the OMS), and the global standards survey below.

This document explains one schema, **OutageNotification v0.1**. It does not define a new schema — it is a plain-language walkthrough of the schema as published, ahead of the auto-generated field reference.

## 2. What It Records / Covers

For a single outage event, the schema captures:

- **Identity** of the notice itself — a stable id reused across updates, so a later message can refer back to the original. In the DISCOM source data this is a Breakdown/Shutdown ID (e.g. `DISCOM-BD-6357257`), and one such ID commonly spans *multiple feeders* under one substation — which is why `affectedAssets` is an array, not a single reference.
- **Classification** — `outageClass` (PLANNED, BREAKDOWN, SCHEDULED_ROSTERING, or EMERGENCY_ROSTERING — taken directly from the DISCOM OMS "Down Info" value set) and a separate lifecycle `status` (SCHEDULED, ACTIVE, PARTIALLY_RESTORED, RESTORED, or CANCELLED). The schema is explicit that restoration is a *status transition*, not a class of its own — an important distinction because the OMS dashboards' "SD/BD/RS" shorthand could otherwise be misread as including restoration.
- **Message semantics for push delivery** — `msgType` (ALERT/UPDATE/CANCEL, borrowed verbatim from OASIS CAP's `alert/msgType`), `references` (prior notice ids a message updates or cancels), and `severity` (EXTREME/SEVERE/MODERATE/MINOR/UNKNOWN, borrowed from CAP's `info/severity`), plus a `category` field that is deliberately *not* CAP's `info/category` — it is a coarse local display/filtering value (MAINTENANCE, UPGRADE, FAULT, LOAD_SHEDDING, WEATHER, SAFETY, OTHER) kept separate from the standardized `cause.category` used for analytics.
- **Cause**, in three layers: a standardized `category` + `subcategory` aligned to IEEE 1782-2022, the vendor's own fault-reason `code` carried verbatim (e.g. the DISCOM's numeric `FAULT_REASON`), an asset/voltage-level `faultType` (e.g. `11KV`), and free text (`text`) that may be localized — the real examples carry Hindi-origin reasons transliterated into English, e.g. *"Pole erection on long span & VCB replacement under Business Plan"*.
- **Network context** — the DISCOM's own organisational hierarchy, confirmed from the live OMS to run **Discom → Zone → Circle → Division → Subdivision → Substation → Feeder/DT** (the design note flags that the `Subdivision` level, sitting between Division and Substation, is easy to miss from the published PDF alone and only surfaced from the OMS screens).
- **Affected assets** — which feeders, distribution transformers, substations or line segments are out (`assetLevel`), each with a `voltageLevel` (e.g. 33kV/11kV/LT/DT), an optional `consumerCategory` (URBAN/RURAL/AGRICULTURE/INDUSTRIAL/MIXED/OTHER — taken from the DISCOM's own "Feeder Type" field), a `meterRef` joining to the smart meter that reports on it, and optional map geometry.
- **Affected area** — the geography affected, as free text (CAP's `areaDesc` pattern, e.g. `"SEC-14, 9, 11 Rajnagar"`), named administrative areas (villages/wards), and GeoJSON geometry.
- **Impact** — how many customers are affected (`customersAffected`), and which connection points are de-energized or confirmed still energized, expressed as CIM (IEC 61968-3) `UsagePoint` references reserved for an authenticated tier of consumers (not the public feed) because of the privacy sensitivity of a live list of affected connections.
- **Timing** — the outage window as one canonical `TimePeriod{start, duration}` (the DISCOM's "Down From"/"Down Hours"), the estimated restoration time (the DISCOM's "Estimated Time (in Minutes)"), the actual restoration time once known (which feeds IEEE 1366 indices), and an SLA target in minutes (the OMS dashboards bucket outages at a 4-hour/240-minute threshold — its own dashboard tallies, e.g. "Feeder Breakdown 121 ≤4h / 1723 >4h", are what motivated `slaTargetMinutes` as a first-class field rather than an afterthought).
- **Field response** — whether partial back-feed has been given via an alternate feed (OMS "Back-Feed given"), the resource/repair status (e.g. PENDING, RESOURCE_ALLOCATED, IN_PROGRESS — modelled after the OMS's own lineman-allocation states), and a linked complaint count (OMS "No. of Complaints").
- **Public-facing text** — a localized (BCP-47 `language`) headline, description and instruction for the consumer, mirroring CAP's `info` block, for both the outage-map feed and the push alert.
- **Provenance** — where the outage was auto-detected, a link back to the originating smart-meter signal (including the raw digital-input port and vendor status code) and the specific MeterData alarm(s) that triggered it.
- **Extensions** — a namespaced space for a DISCOM's own additional fields, e.g. `{"discom": {"breakdownId": "6357257", "downType": "FEEDER"}}` — the exact shape used to preserve the DISCOM's breakdown grouping ID without promoting a vendor-local concept into the shared schema.

A real planned-outage example from the schema's own examples directory shows several of these blocks together — one Breakdown ID spanning four rural 11kV feeders under a single substation, with polygon geometry for the whole affected area and a point geometry for one feeder:

```json
"id": { "scheme": "OTHER", "value": "DISCOM-BD-6357257", "namespace": "discom.example" },
"outageClass": "PLANNED", "status": "SCHEDULED",
"affectedAssets": [
  { "id": { "scheme": "FEEDER", "value": "barehta" }, "assetLevel": "FEEDER",
    "voltageLevel": "11kV", "consumerCategory": "RURAL",
    "geo": { "type": "Point", "coordinates": [77.45, 29.41] } },
  { "id": { "scheme": "FEEDER", "value": "Gosaiganj" }, "assetLevel": "FEEDER", "voltageLevel": "11kV", "consumerCategory": "RURAL" }
],
"timing": { "period": { "start": "2026-06-22T06:43:00+05:30", "duration": "PT5H" }, "slaTargetMinutes": 240 }
```

## 3. How Each Item is Identified

OutageNotification reuses a single `Identifier{scheme, value, namespace}` object throughout, rather than issuing DIDs for every asset. The notice itself carries a stable `id` of this form, reused across UPDATE and CANCEL messages so a viewer or subscriber can tell that a later message concerns the same outage — in the live examples this is literally the DISCOM's breakdown/shutdown ID carried as `scheme: OTHER, value: "DISCOM-BD-6562139", namespace: "discom.example"`, unchanged from ALERT through the RESTORED UPDATE.

Assets (feeders, substations, distribution transformers), meters, and network-context entries (e.g. `discom`, `substation`) are referenced the same way — as an `Identifier`, ideally a stable GIS feature id or an MRID where one exists, so the record can be joined to a map or to another IES record. The `Identifier.scheme` enum itself is of mixed origin: `MRID` is drawn from CIM (IEC 61968/61970), `DID` from W3C DID Core, and the remaining scheme values (`METER_SERIAL`, `GIS_FEATURE_ID`, `SERVICE_DELIVERY_POINT`, `FEEDER`, `SUBSTATION`, `DT`, `CONSUMER_NUMBER`, `ORG`, `OTHER`) are local vendor or DISCOM master keys carried as-is — the schema's own inline `$comment` on this field says so explicitly: *"MRID borrowed from IEC 61968/61970 (CIM); DID borrowed from W3C DID Core; remaining values local."*

The design note's GIS-readiness principle sharpens why this matters: every asset carrying a stable `Identifier` (ideally `GIS_FEATURE_ID` or `MRID`) lets a consumer that already holds the DISCOM's own GIS layer *join on id and pull geometry from GIS* rather than have the notice restate it — keeping notices small while GIS stays the single authoritative geometry source. Inline `geo` on the asset or affected area is the fallback for a consumer with no GIS of its own.

The schema does not mint DIDs for outages, assets or consumers itself; where a DID is already the identifier of record (for example a DISCOM's own `did:web`), that identifier is expressed through the same `Identifier` object with `scheme = DID`.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers.
- **AMISP** — an Advanced Metering Infrastructure Service Provider, the metering agency that posts the real-time feeder energized/de-energized signal (derived from a substation meter's digital-input port) into the DISCOM's MDMS/OMS.
- **RTDAS** — Real-Time Data Acquisition System, a DISCOM-specific detection system named directly in the `provenance.source` enum alongside MDMS/OMS/SCADA/AMI/MANUAL.
- **SERC/CERC** — State/Central Electricity Regulatory Commission, the tariff and licensing regulator for the power sector.
- **CIM (Common Information Model)** — the IEC 61968/61970 family's shared data model for electricity network objects. The 2021 edition of IEC 61968-3 split the older, single `OutagesAndFaults` package into five: `PlannedOutages`, `PlannedOutageNotifications`, `UnplannedOutages`, `EquipmentFaults`, and `LineFaults` — this schema's `outageClass` (PLANNED vs BREAKDOWN) mirrors that same planned/unplanned split, and `UnplannedOutages`' lists of energized/de-energized `UsagePoints` are the direct model for this schema's `impact.energized`/`impact.deEnergized`.
- **CAP (Common Alerting Protocol)** — OASIS CAP v1.2 (also referenced as ITU-T X.1303), the global all-hazard public-warning standard, explicitly inclusive of power outages. This schema borrows its `alert → info → area` envelope: message type, references between messages, severity, the affected area (with polygon/circle geometry), and headline/instruction text.
- **ODIN** — the Outage Data Initiative Nationwide, a US Department of Energy Office of Electricity / Oak Ridge National Laboratory publication pattern for utility outage data. It contributes the two-tier publishing model this schema follows: a coarse, anonymous public API/feed versus a finer-grained authenticated API for designated stakeholders (mirrored here as the public vs. authenticated tiers for `impact.deEnergized`), a subscribe model for push, and the pragmatic convention of a coded cause *plus* free text because real-world causes exceed any closed enum.
- **MultiSpeak** — a NRECA (US rural electric cooperative) utility-industry interoperability specification. Its outage interfaces — OD (outage detection from AMI), OA (outage analysis/OMS), CB/CH (customer calls), and the `ODEventNotification` device-status message — describe exactly the upstream flow the DISCOM's OMS screens implement (AMI/MDMS detects a feeder outage from meter alarms, the OMS confirms it, a notice is published), and validate this schema's provenance link from alarm to outage.
- **GeoJSON** — RFC 7946, the standard JSON format for geographic geometry (points, lines, polygons) in WGS84/EPSG:4326 coordinates, used here for GIS-ready outage maps and directly emittable as a `FeatureCollection` for map frontends.
- **IEEE 1366** — the IEEE guide defining electric power distribution reliability indices (SAIDI, SAIFI, CAIDI, MAIFI), which this schema's `actualRestoration` and `impact.customersAffected` fields feed as source data.
- **RDSS** — the Revamped Distribution Sector Scheme, India's smart-metering mandate; named in the design note as the concrete policy lever this schema's smart-meter-driven detection pipeline directly supports.
- **IEEE 1782-2022** — the IEEE guide "for Collecting, Categorizing, and Utilizing Information Related to Electric Power Distribution Interruption Events," providing a standardized taxonomy of ten outage cause categories (§4.4) and their subcategories (§4.5), used directly for this schema's `cause.category` and `cause.subcategory`. It is a *guide* (recommended practice), and its text is copyrighted — this schema cites its section numbers rather than reproducing its content.
- **MDMS/OMS/SCADA** — Meter Data Management System, Outage Management System, and Supervisory Control and Data Acquisition — the licensee-side systems that detect, record and manage outages.
- **UsagePoint** — a CIM (IEC 61968-3) concept for a point of connection to the network, used here to record which connections are de-energized or energized.
- **SACHET** — India's NDMA/C-DOT Common Alerting Protocol-based mass-alerting platform (paired with the NDMA Cell Broadcast system); named in the implementation guide as the concrete India-specific channel this schema's CAP-shaped push output is designed to feed for wide-area events.
- **IS 15959 / DLMS-COSEM (IEC 62056)** — the Indian Standard (aligned to IEC 62056) for smart-meter data exchange, cited as the standardized layer that the *vendor's own* feeder-status and alarm codes should ultimately be validated against; `MeterData`'s `AlarmProfile.alarmId` is the field in the companion schema that aligns to it.

## 5. Basis of Standards

The IES order of preference is fixed:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

OutageNotification v0.1 does not draw on a Bureau of Indian Standards specification or a CEA/IEGC provision directly — no Indian standard for outage-notification data currently exists to occupy the first two tiers. (The one IS-tier standard the surrounding pipeline does touch — IS 15959/DLMS-COSEM for meter event and OBIS codes — governs the *upstream* feeder-status signal, not this schema's own fields; see section 6.) The schema instead composes several standards at the IEC and IEEE tiers and beyond, each occupying a distinct layer:

- **IEC 61968-3 (CIM), 2021 edition** — outage and UsagePoint data semantics, and the planned-versus-unplanned split that this schema's `outageClass` mirrors (`PlannedOutage`/`PlannedOutageNotification` vs. `UnplannedOutage`). `impact.deEnergized`/`impact.energized` map to CIM's `Outage.deEnergizedUsagePoint`/`energizedUsagePoint`.
- **OASIS CAP v1.2** (also referenced as ITU-T X.1303) — the push-alert envelope: `msgType` maps to CAP `alert.msgType`, `references` to `alert.references`, `severity` to `info.severity`, `publicInfo.headline/description/instruction` to `info.headline/description/instruction`, and `affectedArea.text`/`geo` to `area.areaDesc`/`area.polygon`/`area.circle`.
- **IEEE 1366**, together with RDSS and CEA reliability reporting, for the restoration-time and customer-count fields that feed SAIDI/SAIFI/CAIDI/MAIFI indices.
- **IEEE 1782-2022 §4.4 and §4.5** for the standardized outage cause category (ten categories: EQUIPMENT, LIGHTNING, PLANNED, POWER_SUPPLY, PUBLIC, VEGETATION, WEATHER, WILDLIFE, UNKNOWN, OTHER) and subcategory taxonomy, used together with IEEE 1366.

Two further conventions are layered in without being formal IEC/IEEE standards themselves: the **ODIN** (US DOE/ORNL) publication pattern — public/authenticated two-tier APIs and the coded-plus-free-text cause convention — and **MultiSpeak**, for the AMI/MDMS-to-OMS detection flow and provenance chain. **GeoJSON (RFC 7946)** is used for all GIS geometry in WGS84. The design note also names two further de-facto references that shaped the delivery-pattern design without being cited as data-model standards inside the schema itself: the **UK Power Networks "Live Faults" open dataset**, the reference pattern for a public, near-real-time, GIS-ready outage feed; and the **US DOE OE-417/EIA** emergency-incident reporting regime and the **ENTSO-E Transparency Platform**, both cited as confirming a general regulatory need to publish outages in structured form, at the transmission level in ENTSO-E's case.

## 6. Where Indian Standards Do Not Yet Exist

The schema itself documents, field by field, exactly where a published standard applies and where it does not — this is the clearest account of the gap for this domain:

- **Cause classification** — no Indian standard defines a cause taxonomy for outage reporting. The schema uses IEEE 1782-2022 (§4.4 for `cause.category`, §4.5 for `cause.subcategory`), used together with IEEE 1366. Load-shedding/rostering has no standard category at all; scheduled rostering is mapped to the nearest category (PLANNED) and emergency rostering to OTHER, with the real nature of the event carried separately in `outageClass`. The gap is not merely theoretical: the schema's `fault_reason_crosswalk.json` maps all 31 codes of a real DISCOM OMS fault-reason pick-list (`FORM_ID 8312`) onto the IEEE taxonomy, and documents that the source pick-list itself is "operational and India-specific — not a published standard," and contains outright duplicates (code `13 Overload` and code `26 Overloading` map to the same category/subcategory; `20 System improvement work` and `29 System Improvement Work/Deposit Works` likewise; transformer faults are split unevenly across four separate codes, `3`, `4`, `10`, `11`, and `23`). The crosswalk further records non-obvious classification calls the DISCOM had to make, e.g. an 11kV (and LT/ABC) line fault is classified `EQUIPMENT` because it is a distribution feeder *downstream* of the substation, whereas IEEE's `POWER_SUPPLY` category is reserved for the system that *feeds* the substation (so a 33kV sub-transmission fault is `POWER_SUPPLY/SUBTRANSMISSION` while an 11kV feeder fault is `EQUIPMENT/OTHER`); a fire inside a control room or switchyard is `EQUIPMENT` (utility-originated) while an external fire reaching the line is `PUBLIC/FIRE_POLICE`.
- **Push-alert structure** — no Indian standard defines a consumer alert envelope. OASIS CAP v1.2 is used for `msgType`, `references`, `severity`, and the area/geometry block. India does have a national CAP-based channel — SACHET (NDMA/C-DOT) paired with the NDMA Cell Broadcast system — which the implementation guide names as the intended downstream consumer of this schema's CAP-shaped output for wide-area events, but SACHET is an alerting *platform*, not a data-format standard this schema itself conforms to beyond CAP.
- **Identifier scheme for assets** — no Indian standard exists here either; the `Identifier.scheme` enum is of mixed origin (`MRID` from CIM, `DID` from W3C DID Core, the rest local).
- **Reliability reporting maturity** — the design note cites an independent review of Indian DISCOM outage reporting finding that only about 17 of 36 DISCOMs currently publish SAIFI/SAIDI at all, and that most of the rest still publish bare interruption date/time lists with no affected-customer count. A schema that captures `impact.customersAffected` and `actualRestoration` as first-class, structured fields is presented explicitly as a direct upgrade path for India's reliability reporting, and as well-aligned with RDSS's smart-metering direction — but this is a gap the schema is designed to help close, not one it can be said to have already closed.
- **Vendor detection-signal codes** — the raw feeder-status codes coming off a substation meter's digital-input port (e.g. `FEEDER_STATUS=102`) are vendor/platform-specific, not a standard enum; the design note identifies IS 15959 Part 1/2 (DLMS-COSEM, aligned to IEC 62056) — specifically its OBIS codes and standard event/alarm code list — as the standardized layer these vendor codes should ultimately be validated against, the same layer `MeterData`'s `AlarmProfile.alarmId` aligns to. Mapping a specific vendor's raw codes to that standard is left as an open task for each deployment (see section 11).
- **Everything the schema marks as purely local** — `feederStatus`, `outageClass`, `status`, `category` (the display/filtering category, deliberately not CAP's `info/category`), `assetLevel`, `consumerCategory`, and `source` (the detecting system) have no applicable published standard at all today. `outageClass` in particular is taken directly from the DISCOM OMS "Down Info" value set — a local, additive enum, not a published standard. `consumerCategory` is sourced from the DISCOM's own "Feeder Type" field, which in the source PDF also includes values (`TEHSEEL`, `INDEPENDENT`) not yet represented in the schema's enum — the design note flags these as candidates to fold into `OTHER` or add as future additive values.

## 7. The Record(s)

OutageNotification defines one record type, the outage notice itself. It is not static: one signed record exists per outage, and it is updated in place over the life of that outage rather than replaced by an unrelated new object. A NEW record is issued at detection (or at scheduling, for a planned outage); one or more UPDATE records follow as the restoration estimate or field status changes; and a RESTORED or CANCELLED record closes it out. Each version is independently signed.

The real three-message lifecycle in the schema's own examples makes this concrete: an ALERT is issued the moment RTDAS detects a de-energized 11kV feeder (`status: ACTIVE`, `severity: SEVERE`, `provenance.source: RTDAS`, carrying the raw digital-input signal `feederStatus: DE_ENERGIZED, rawCode: "102"`); roughly three hours later an UPDATE closes the same notice id (`status: RESTORED`, `msgType: UPDATE`, `severity` downgraded to `MINOR`, `timing.actualRestoration` now set, and the signal block updated to `feederStatus: ENERGIZED, rawCode: "101"`) — the same `id` value (`DISCOM-BD-6562139`) ties both messages together, and the elapsed time between `detectedAt` and `actualRestoration` (2 hours 43 minutes here) is exactly the duration IEEE 1366 indices are computed from.

The record is issued by the distribution licensee or a system acting on its behalf (an OMS, MDMS or SCADA system, an RTDAS, or a manual entry — the `provenance.source` enum names all of these explicitly, with MANUAL reserved for outages entered by a human rather than detected automatically). Where the outage was auto-detected, the record's `provenance` block relates it directly to another IES record — the MeterData v0.6 schema's `AlarmProfile` — by carrying references into that record's alarms (`meterRef`, `alarmId`, `timestamp`), so a viewer can trace an outage notice back to the smart-meter signal that triggered it. The provenance block also carries the raw detection signal itself (`OutageSignal`: `eventId`, normalized `feederStatus`, the `diPort` the signal arrived on, and the vendor's `rawCode`) and a `detectionRef` pointing at the real-time detection record (e.g. the DISCOM's `RTDAS_DATA_ID`) — the schema notes that an absent `detectionRef`, or a `"0"` sentinel value, is itself the signal that an outage was entered manually rather than auto-detected.

## 8. Schedule I — Field Reference (summary)

OutageNotification v0.1 is built from the following logical blocks:

- **OutageNotification** — the root object: identity, class, status, message semantics, cause, timing window reference, network context, affected assets and area, impact, response, public-facing text, provenance, and extensions.
- **OutageCause** — the standardized cause category and subcategory, vendor fault type and code, and free-text reason.
- **OutageAsset** — one affected network asset (feeder, substation, DT, line segment, or service point), its level, and optional map geometry.
- **OutageNetworkContext** — the DISCOM's own organisational hierarchy (zone, circle, division, subdivision, substation, district).
- **OutageAffectedArea** — the affected geography as free text, named administrative areas, and GeoJSON geometry.
- **OutageImpact** — customers affected and the de-energized/energized connection points.
- **OutageTiming** — the outage window, estimated restoration, actual restoration, and SLA target.
- **OutageResponse** — back-feed status, field resource status, and linked complaint count.
- **OutagePublicInfo** — the localized headline, description and instruction shown to consumers.
- **OutageProvenance** — the detecting system, the AMISP code, the raw detection signal (`OutageSignal`), and references into the originating smart-meter signal and MeterData alarms (`OutageAlarmRef`).

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [OutageNotification v0.1 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/outagenotification/v0.1#field-reference).

## 9. Schedule II

Not applicable as a populated report template. OutageNotification is stand-alone: it is not a Verifiable Credential and does not wrap another IES schema as its payload. It does, however, reference another IES record — its `provenance.alarmRefs` field points into MeterData v0.6's `AlarmProfile` records where an outage was auto-detected — but this is a cross-reference between two independent records, not a wrapping relationship. The design note separately notes an optional, not-yet-adopted possibility: wrapping the notice as a W3C Verifiable Credential (`OutageNotificationCredential`, issued by the DISCOM's DID) for tamper-evidence and cross-network trust, mirroring the existing `MeterDataCredential` pattern — but for v0.1 as published, bare JSON is described as sufficient for ordinary web publishing.

## 10. How It Fits Together

OutageNotification is a stand-alone published payload — it is not issued as a W3C Verifiable Credential the way ElectricityCredential is; its delivery paths are the public web feed and the push alert described below. It sits downstream of a two-layer pipeline that the design note deliberately keeps separate: a thin **detection/ingest** layer and a **publication** layer. In the detection layer, an AMISP-operated substation meter's digital-input port reports a raw energized/de-energized signal (the companion `FeederStatusIngest.openapi.yaml` contract: bearer-token auth, a single `discomCode` tenant, client-supplied `eventId` for idempotency, and batch array input because one substation trip can cascade across many feeders at once); the licensee's MDMS/OMS/SCADA correlates consecutive signals per feeder, enriches them against master data (network hierarchy, GIS geometry, customer counts, the fault-reason crosswalk), and raises an `OutageNotification`. Where that detection path exists, this schema's `provenance` block links the resulting notice back to the specific MeterData `AlarmProfile` record and raw signal that triggered it, giving a reviewer a traceable chain from raw digital-input signal to public notice.

The same notice object serves two audiences without change: published as-is it becomes a pull feed for a website or outage map — the design note specifies a `GET /outages.geojson` mode emitting a GeoJSON `FeatureCollection`, one `Feature` per affected asset or area, with outage attributes in `properties` so it drops directly into a Leaflet/MapLibre/Mapbox map and can be weighted into a heatmap by `impact.customersAffected` — and pushed as-is it becomes a CAP-shaped alert to subscribed or affected consumers, with a companion `GET /outages.cap.xml` mode and an explicit downstream path into India's SACHET/NDMA Cell Broadcast mass-alerting infrastructure for wide-area events. A `GET /outages/lookup?sdp=...` or `?lat=&lon=` mode is also described, letting a single consumer ask "is my connection affected right now?" — the geospatial complement to the map and push views. The public feed and the push channel both draw a line, ODIN-style, between a coarse public tier (no PII) and an authenticated tier that adds the affected `UsagePoint` list.

There is currently no IES use-case guide built on this schema — it exists today as a published schema only, ahead of any use case that would combine it with identity, discovery or credential-issuance steps.

## 11. Points for Confirmation

1. The schema is explicitly marked Work In Progress by its own README and `attributes.yaml`; field names, enums and interpretation may change before a stable release, so nothing here should be treated as fixed for production integration.
2. The design note itself flags that the DISCOM dashboard shorthand "SD/BD/RS" needs confirmation from the DISCOM that RS specifically means Roster Shutdown (rotational load-shedding) and not another controlled-outage category — the schema's interpretation (restoration modelled as `status=RESTORED`, a transition, not as its own class) is stated as the working assumption, not yet verified with the source utility.
3. Whether the MDMS emits the smart-meter-alarm-to-unplanned-outage linkage fully automatically, or whether the OMS's "Create New Fault" step is a manual operator action, is an open question the design note raises directly — it determines which fields can be trusted to auto-populate versus which still need human entry.
4. No IES use-case guide yet exists for OutageNotification — how it will be combined with Register/Discover/Exchange steps in a full use case is not yet documented.
5. Several enums are explicitly local with no applicable published standard (`feederStatus`, `outageClass`, `status`, `category`, `assetLevel`, `consumerCategory`, `source`); whether any of these should be proposed for standardization, or left as DISCOM-local values, is open. `consumerCategory` in particular does not yet cover two values (`TEHSEEL`, `INDEPENDENT`) that appear in the source DISCOM PDF.
6. The vendor fault-reason code (`cause.code`) is deliberately left unstandardized and carried verbatim, with a separate crosswalk file mapping it to the IEEE 1782 taxonomy; the design note poses this directly as an open question — adopt the OMS-seeded code list as a canonical IES vocabulary, or keep the field purely free-text for v0.1 — and separately recommends the source DISCOM de-duplicate its own 31-code master list (which currently contains at least three duplicate pairs) before that decision is made.
7. Raw vendor feeder-status and digital-input codes (e.g. `FEEDER_STATUS=102`) are not yet mapped to the IS 15959/DLMS-COSEM (IEC 62056) standard event and OBIS code list that the design note identifies as the correct standardized target — each deployment currently has to obtain its own meter vendor's code legend and build that mapping itself.
8. The granularity of `impact.deEnergized[]` exposed on the public tier versus the authenticated tier is called out as an open privacy question, not yet settled by a published policy.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IEC 61968-3:2021 (CIM) | Outage/UsagePoint data semantics; the 2021 split into `PlannedOutages`/`PlannedOutageNotifications`/`UnplannedOutages`/`EquipmentFaults`/`LineFaults` underlies `outageClass`; `Outage.deEnergizedUsagePoint`/`energizedUsagePoint` underlie `impact` |
| OASIS CAP v1.2 (ITU-T X.1303) | Push-alert envelope: `msgType`, `references`, `severity`, `area`/geometry, `headline`/`description`/`instruction` |
| ODIN (US DOE/ORNL) | Public/authenticated two-tier publication pattern; subscribe/push model; coded-plus-free-text cause convention |
| MultiSpeak (NRECA) | AMI/MDMS-to-OMS detection flow (OD/OA/CB/CH interfaces, `ODEventNotification`) and provenance chain |
| GeoJSON (RFC 7946) | GIS geometry in WGS84/EPSG:4326 for outage maps; direct `FeatureCollection` emission |
| IEEE 1366 (with RDSS and CEA reliability reporting) | Restoration time and customer-count fields feeding SAIDI/SAIFI/CAIDI/MAIFI reliability indices |
| IEEE 1782-2022 | Outage cause category (§4.4, ten categories) and subcategory (§4.5) taxonomy |
| W3C DID Core | `Identifier.scheme = DID` values, where a DID is already the identifier of record |
| IS 15959 / DLMS-COSEM (IEC 62056) | Target standard for vendor feeder-status/meter event codes upstream of this schema (not yet mapped in v0.1) |

### Annexure B — Example Payloads

Example OutageNotification payloads are available in [schemas/OutageNotification/v0.1/examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/OutageNotification/v0.1/examples) — including a multi-feeder planned-shutdown notice, a three-message unplanned-breakdown lifecycle (ALERT → RESTORED UPDATE) with full detection provenance, and the DISCOM's published planned-shutdown set transformed into schema form.

### Annexure C — JSON Schema

The full machine-readable definitions are at [schemas/OutageNotification/v0.1/schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/schema.json) and [schemas/OutageNotification/v0.1/attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/attributes.yaml).
