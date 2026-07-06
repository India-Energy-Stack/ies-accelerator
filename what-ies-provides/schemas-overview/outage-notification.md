# Outage Notification v0.1

*A machine-readable payload a distribution licensee publishes to describe one planned or unplanned electricity outage, usable both as a public outage-map feed and as a push alert to affected consumers.*

| Field | Value |
|---|---|
| Document | IES/ON/0.1 |
| Status | Draft for technical review — the schema's own README marks it **"WORK IN PROGRESS — subject to change."** It is an early draft published for discussion; field names, enums and interpretation are not final and may change without notice. Do not depend on it for production integrations yet. |
| Applicability | Issued by a distribution licensee (DISCOM), or a system acting on its behalf (an OMS, MDMS, or SCADA); consumed by outage-map/website feeds, subscribed consumers, and downstream reliability reporting |
| This version | v0.1 covers the outage notice itself — class, cause, affected assets and area, timing, impact, response, public-facing text, and provenance back to the detecting smart-meter signal — defined in the companion JSON Schema file [`schema.json`](../../schemas/OutageNotification/v0.1/schema.json) |

## 1. Scope and Purpose

The stakeholders are the distribution licensee that must tell the public and its own field teams what is out, where, and for how long, and the consumers, subscribers and outage-map viewers who currently cannot get that information in a consistent, machine-readable form. A licensee's outage-management system (OMS) knows the moment a feeder trips or a shutdown is scheduled, but without a shared schema that knowledge stays locked inside the OMS — it cannot be republished automatically as a map feed, pushed as a subscriber alert, or linked back to the smart-meter reading that first detected it.

This document explains one schema, **OutageNotification v0.1**. It does not define a new schema — it is a plain-language walkthrough of the schema as published, ahead of the auto-generated field reference.

## 2. What It Records / Covers

For a single outage event, the schema captures:

- **Identity** of the notice itself — a stable id reused across updates, so a later message can refer back to the original.
- **Classification** — whether the outage is planned, an unplanned breakdown, or scheduled/emergency rostering (rotational load-shedding), and its current lifecycle status (scheduled, active, partially restored, restored, or cancelled).
- **Message semantics for push delivery** — whether this message is a fresh alert, an update to a prior notice, or a cancellation, plus severity and a display category.
- **Cause** — a standardized cause category and subcategory, the vendor's own fault-reason code carried verbatim, a voltage/asset-level fault type, and free text.
- **Network context** — where in the licensee's own organisational hierarchy (zone, circle, division, subdivision, substation, district) the outage sits.
- **Affected assets** — which feeders, distribution transformers, substations or line segments are out, each with an optional map geometry.
- **Affected area** — the geography affected, as free text, named administrative areas, and GIS geometry.
- **Impact** — how many customers are affected, and which connection points are de-energized or confirmed still energized.
- **Timing** — the outage window, the estimated restoration time, the actual restoration time once known, and any SLA target.
- **Field response** — whether partial back-feed has been given, the resource/repair status, and linked complaint counts.
- **Public-facing text** — a localized headline, description and instruction for the consumer, for both the outage-map feed and the push alert.
- **Provenance** — where the outage was auto-detected, a link back to the originating smart-meter signal and system.
- **Extensions** — a namespaced space for a DISCOM's own additional fields.

## 3. How Each Item is Identified

OutageNotification reuses a single `Identifier{scheme, value, namespace}` object throughout, rather than issuing DIDs for every asset. The notice itself carries a stable `id` of this form, reused across UPDATE and CANCEL messages so a viewer or subscriber can tell that a later message concerns the same outage. Assets (feeders, substations, distribution transformers), meters, and network-context entries (e.g. `discom`, `substation`) are referenced the same way — as an `Identifier`, ideally a stable GIS feature id or an MRID where one exists, so the record can be joined to a map or to another IES record. The `Identifier.scheme` enum itself is of mixed origin: `MRID` is drawn from CIM (IEC 61968/61970), `DID` from W3C DID Core, and the remaining scheme values (meter serial, GIS feature id, service delivery point, feeder, substation, DT, consumer number, org, other) are local vendor or DISCOM master keys carried as-is. The schema does not mint DIDs for outages, assets or consumers itself; where a DID is already the identifier of record (for example a DISCOM's own `did:web`), that identifier is expressed through the same `Identifier` object with `scheme = DID`.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers.
- **AMISP** — an Advanced Metering Infrastructure Service Provider, the metering agency that operates smart-meter data collection on a DISCOM's behalf.
- **SERC/CERC** — State/Central Electricity Regulatory Commission, the tariff and licensing regulator for the power sector.
- **CIM (Common Information Model)** — the IEC 61968/61970 family's shared data model for electricity network objects (outages, usage points, equipment); referenced here for outage/UsagePoint semantics and the planned-versus-unplanned distinction.
- **CAP (Common Alerting Protocol)** — OASIS CAP v1.2 (also referenced as ITU-T X.1303), the standard envelope this schema borrows for push alerts: message type, references between messages, severity, the affected area, and headline/instruction text.
- **ODIN** — a US Department of Energy / Oak Ridge National Laboratory publication pattern for utility outage data, contributing the general publication approach and the convention of a coded cause plus free text.
- **MultiSpeak** — a utility-industry interoperability specification, contributing the AMI/MDMS-to-OMS detection flow and provenance chain used in this schema.
- **GeoJSON** — RFC 7946, the standard JSON format for geographic geometry (points, lines, polygons) in WGS84 coordinates, used here for GIS-ready outage maps.
- **IEEE 1366** — the IEEE standard defining electric power distribution reliability indices (including SAIDI/SAIFI), which this schema's restoration-time and customer-count fields feed.
- **RDSS** — a reliability data-collection convention paired with IEEE 1366 for restoration time and customer-count reporting.
- **IEEE 1782-2022** — the IEEE standard providing a standardized taxonomy of outage cause categories and subcategories, used directly for this schema's `cause.category` and `cause.subcategory`.
- **MDMS/OMS/SCADA** — Meter Data Management System, Outage Management System, and Supervisory Control and Data Acquisition — the licensee-side systems that detect, record and manage outages.
- **UsagePoint** — a CIM (IEC 61968-3) concept for a point of connection to the network, used here to record which connections are de-energized or energized.

## 5. Basis of Standards

The IES order of preference is fixed:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

OutageNotification v0.1 does not draw on a Bureau of Indian Standards specification or a CEA/IEGC provision directly — no Indian standard for outage-notification data currently exists to occupy the first two tiers. The schema instead composes several standards at the IEC and IEEE tiers and beyond: IEC 61968-3 (CIM) for outage and UsagePoint data semantics and the planned-versus-unplanned distinction; OASIS CAP v1.2 (also referenced as ITU-T X.1303) for the push-alert envelope; IEEE 1366, together with RDSS, for restoration-time and customer-count fields that feed SAIDI/SAIFI reliability indices; and IEEE 1782-2022 for the standardized outage cause category and subcategory taxonomy. Two further conventions are layered in without being formal IEC/IEEE standards themselves: the ODIN (US DOE/ORNL) publication pattern, and MultiSpeak for the AMI/MDMS-to-OMS detection flow. GeoJSON (RFC 7946) is used for all GIS geometry.

## 6. Where Indian Standards Do Not Yet Exist

The schema itself documents, field by field, exactly where a published standard applies and where it does not — this is the clearest account of the gap for this domain:

- **Cause classification** — no Indian standard defines a cause taxonomy for outage reporting. The schema uses IEEE 1782-2022 (sections 4.4 and 4.5) for `cause.category` and `cause.subcategory`, used together with IEEE 1366. Load-shedding/rostering has no standard category at all; scheduled rostering is mapped to the nearest category (PLANNED) and emergency rostering to OTHER, with the real nature of the event carried separately in `outageClass`.
- **Push-alert structure** — no Indian standard defines a consumer alert envelope. OASIS CAP v1.2 is used for `msgType`, `references`, `severity`, and the area/geometry block.
- **Identifier scheme for assets** — no Indian standard exists here either; the `Identifier.scheme` enum is of mixed origin (`MRID` from CIM, `DID` from W3C DID Core, the rest local).
- **Everything the schema marks as purely local** — `feederStatus`, `outageClass`, `status`, `category` (the display/filtering category, deliberately not CAP's `info/category`), `assetLevel`, `consumerCategory`, and `source` (the detecting system) have no applicable published standard at all today. `outageClass` in particular is taken directly from the UPPCL OMS "Down Info" value set — a local, additive enum, not a published standard.

## 7. The Record(s)

OutageNotification defines one record type, the outage notice itself. It is not static: one signed record exists per outage, and it is updated in place over the life of that outage rather than replaced by an unrelated new object. A NEW record is issued at detection (or at scheduling, for a planned outage); one or more UPDATE records follow as the restoration estimate or field status changes; and a RESTORED or CANCELLED record closes it out. Each version is independently signed. The record is issued by the distribution licensee or a system acting on its behalf (an OMS, MDMS or SCADA system, or a manual entry). Where the outage was auto-detected, the record's `provenance` block relates it directly to another IES record — the MeterData v0.6 schema's `AlarmProfile` — by carrying references into that record's alarms, so a viewer can trace an outage notice back to the smart-meter signal that triggered it.

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
- **OutageProvenance** — the detecting system, the AMISP code, and references into the originating smart-meter signal and MeterData alarms.

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [OutageNotification v0.1 — Field reference](../../schemas/OutageNotification/v0.1/README.md#field-reference).

## 9. Schedule II

Not applicable as a populated report template. OutageNotification is stand-alone: it is not a Verifiable Credential and does not wrap another IES schema as its payload. It does, however, reference another IES record — its `provenance.alarmRefs` field points into MeterData v0.6's `AlarmProfile` records where an outage was auto-detected — but this is a cross-reference between two independent records, not a wrapping relationship.

## 10. How It Fits Together

OutageNotification is signed at the Beckn envelope level when exchanged, not issued as a W3C Verifiable Credential the way ElectricityCredential is. It sits downstream of the smart-meter detection layer: an AMISP-operated meter or feeder-status signal reaches the licensee's MDMS/OMS/SCADA system, which raises an outage; where that detection path exists, this schema's `provenance` block links the resulting notice back to the specific MeterData `AlarmProfile` record that triggered it, giving a reviewer a traceable chain from raw signal to public notice. The same notice object serves two audiences without change: published as-is it becomes a pull feed for a website or outage map (using its GeoJSON geometry and affected-area text), and pushed as-is it becomes a CAP-shaped alert to subscribed or affected consumers. There is currently no IES use-case guide built on this schema — it exists today as a published schema only, ahead of any use case that would combine it with identity, discovery or credential-issuance steps.

## 11. Points for Confirmation

1. The schema is explicitly marked Work In Progress by its own README; field names, enums and interpretation may change before a stable release, so nothing here should be treated as fixed for production integration.
2. No IES use-case guide yet exists for OutageNotification — how it will be combined with Register/Discover/Exchange steps in a full use case is not yet documented.
3. Several enums are explicitly local with no applicable published standard (`feederStatus`, `outageClass`, `status`, `category`, `assetLevel`, `consumerCategory`, `source`); whether any of these should be proposed for standardization, or left as DISCOM-local values, is open.
4. The vendor fault-reason code (`cause.code`) is deliberately left unstandardized and carried verbatim, with a separate crosswalk file mapping it to the IEEE 1782 taxonomy; whether that crosswalk approach should become the general IES pattern for other vendor codes is not yet decided.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IEC 61968-3 (CIM) | Outage/UsagePoint data semantics; planned vs unplanned distinction |
| OASIS CAP v1.2 (ITU-T X.1303) | Push-alert envelope: message type, references, severity, area/geometry, headline/instruction text |
| ODIN (US DOE/ORNL) | General outage-data publication pattern; coded-plus-free-text cause convention |
| MultiSpeak | AMI/MDMS-to-OMS detection flow and provenance chain |
| GeoJSON (RFC 7946) | GIS geometry in WGS84 for outage maps |
| IEEE 1366 (with RDSS) | Restoration time and customer-count fields feeding SAIDI/SAIFI reliability indices |
| IEEE 1782-2022 | Outage cause category (section 4.4) and subcategory (section 4.5) taxonomy |

### Annexure B — Example Payloads

Example OutageNotification payloads are available in [schemas/OutageNotification/v0.1/examples/](../../schemas/OutageNotification/v0.1/examples/).

### Annexure C — JSON Schema

The full machine-readable definitions are at [schemas/OutageNotification/v0.1/schema.json](../../schemas/OutageNotification/v0.1/schema.json) and [schemas/OutageNotification/v0.1/attributes.yaml](../../schemas/OutageNotification/v0.1/attributes.yaml).
