# Outage Notification System — Implementation Guide

**Status:** Draft for discussion · **Audience:** DISCOM IT / system integrators building a production outage-notification service.
**Goal:** a modern **pull + push** notification system that publishes planned and unplanned outages as the [`OutageNotification`](https://india-energy-stack.gitbook.io/docs/schemas/outagenotification/v0.1) format, so a utility can serve websites, apps, outage maps, alerting networks, and subscribed consumers from one source of truth — making operations more efficient and transparent.

This is a *how to build it* guide. For the data model and rationale see [OutageNotification_Design.md](OutageNotification_Design.md); for the upstream detection contract see [FeederStatusIngest.openapi.yaml](FeederStatusIngest.openapi.yaml).

---

## 1. Architecture at a glance

```
 SOURCES                        INGEST & ENRICH                  SYSTEM OF RECORD            DISTRIBUTION
┌──────────────────┐          ┌───────────────────────┐        ┌────────────────────┐     ┌─────────────────────────┐
│ AMISP / RTDAS    │  feeder  │ Feeder Status Ingest   │ events │ Correlation +      │     │ PULL  (read APIs + CDN) │
│ smart-meter DI   ├─────────►│ API  → event broker    ├───────►│ Enrichment service ├────►│  /outages /outages.geojson
│ MDMS alarms      │  signals │ (idempotent, batched)  │        │ → OutageNotification│     │  /outages.cap.xml /lookup│
├──────────────────┤          └───────────────────────┘        │   store (DB+PostGIS)│     ├─────────────────────────┤
│ OMS manual entry │  planned / rostering ───────────────────► │  (validated JSON,   │     │ PUSH (fan-out)          │
│ (shutdowns)      │                                            │   lifecycle state)  ├────►│  webhooks · FCM/app     │
└──────────────────┘                                            └─────────┬──────────┘     │  SMS/WhatsApp/email/IVR │
                                                                          │  publish events  │  CAP → SACHET / cell-bc │
                                                                          └─────────────────►│ MAP (Leaflet/MapLibre)  │
                                                                                             └─────────────────────────┘
```

**Two layers, kept separate:** a thin **detection/ingest** layer (real-time feeder signals) and a **publication** layer (enriched `OutageNotification` served to the world). Keep both — see Design note §7.4.

---

## 2. Where the data comes from (assumptions)

This guide assumes the service **receives or produces validated `OutageNotification` JSON**. In a DISCOM that means:

| Outage type | Producer | Trigger |
|---|---|---|
| **Breakdown** (unplanned) | MDMS/OMS enrichment, fed by the **Feeder Status Ingest API** (AMISP/RTDAS DI-port signals) | Real-time feeder de-energized signal |
| **Planned shutdown** | OMS (manual entry) | Operator schedules maintenance |
| **Scheduled / Emergency Rostering** | OMS / load-dispatch | Roster or load-driven shedding |
| **Restoration** | MDMS/OMS, fed by the ENERGIZED signal | Feeder re-energized |

The **enrichment step** turns a bare feeder signal into a publishable notice: it resolves `feederCode`/`substationCode` against master data to fill `network.*`, `affectedAssets[]`, `affectedArea` (geometry), `impact.customersAffected`, `cause` (via the [fault-reason crosswalk](fault_reason_crosswalk.json)), and `timing`. If your OMS can already emit `OutageNotification` directly, you can skip the ingest/enrichment build and start at Step 5.

---

## 3. Prerequisites

**Master data (the hard part — get this right first):**
- Network hierarchy with **stable IDs**: discom → zone → circle → division → subdivision → substation → feeder → DT. Prefer a durable id (`MRID` / GIS feature id).
- **Consumer ↔ feeder/DT mapping**, or **feeder service-area polygons** (GeoJSON, WGS84) — needed to answer "who is affected?" for push and `/lookup`.
- **Contact channels with consent**: phone / app push token / email / WhatsApp opt-in, keyed to service-delivery-point.
- **GIS geometry** for substations/feeders/DTs (points and, ideally, service-area polygons).

**Platform:** a datastore (PostgreSQL + PostGIS), an event broker (Kafka / NATS / Redis Streams / cloud pub-sub), an API gateway + CDN, push providers, and a map frontend.

**Conventions:** RFC 3339 timestamps **with offset**; NTP-synced clocks; the [`OutageNotification` schema](schema.json) + [fault-reason crosswalk](fault_reason_crosswalk.json); bearer-token auth for ingest and subscriptions.

---

## 4. Step-by-step

### Step 1 — Adopt the schema and validate at the edge
Treat [`schema.json`](schema.json) as the contract. Validate every inbound/outbound payload with a JSON-Schema validator ([json-schema.org](https://json-schema.org/), [implementations list](https://json-schema.org/implementations)). Publish your REST surface as [OpenAPI 3.1](https://www.openapis.org/).

### Step 2 — Build the ingest layer (detection)
Implement [`FeederStatusIngest.openapi.yaml`](FeederStatusIngest.openapi.yaml): bearer auth, **client-supplied `eventId` for idempotency**, **batch array** input, normalized `feederStatus` + raw vendor code. Write accepted events to an event broker — [Apache Kafka](https://kafka.apache.org/), [NATS JetStream](https://docs.nats.io/nats-concepts/jetstream), [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/), [Google Pub/Sub](https://cloud.google.com/pubsub/docs), or [AWS SNS](https://docs.aws.amazon.com/sns/)+[SQS](https://docs.aws.amazon.com/sqs/). Follow the [IETF Idempotency-Key](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/) pattern.

### Step 3 — Correlate and enrich → produce `OutageNotification`
A stream processor groups consecutive `DE_ENERGIZED`/`ENERGIZED` events per feeder, joins master data + GIS, applies the [fault-reason crosswalk](fault_reason_crosswalk.json), and writes a validated `OutageNotification` to the store. Use **[PostgreSQL](https://www.postgresql.org/) + [PostGIS](https://postgis.net/)** so geometry and `customersAffected` (point-in-polygon over the service area) are computed in-database.

### Step 4 — Manage lifecycle
Model the state machine: `SCHEDULED → ACTIVE → (PARTIALLY_RESTORED) → RESTORED`, plus `CANCELLED`. Each change emits a new message with `msgType` `ALERT` / `UPDATE` / `CANCEL` (CAP semantics), reusing the stable outage `id` and setting `actualRestoration` on restore. Publish an internal "outage changed" event for the distribution layer to consume.

### Step 5 — Pull API (web + outage map feed)
Expose read endpoints and make them cheap and cacheable:
```
GET /outages            ?status= &class= &from= &to= &substation= &feederMeter=
GET /outages/{id}
GET /outages.geojson    FeatureCollection for maps (RFC 7946, WGS84)
GET /outages.cap.xml    CAP feed for alerting networks
GET /outages/lookup     ?sdp= | ?lat=&lon=   "is my connection affected?"
```
Public reads are bursty during big outages — put a **CDN** in front ([Cloudflare](https://developers.cloudflare.com/cache/), [AWS CloudFront](https://docs.aws.amazon.com/cloudfront/)) and use [HTTP caching / ETag](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching). Serve a **public tier** (coarse, no PII) and an **authenticated tier** (adds affected service points) — the ODIN pattern.

### Step 6 — Outage map
Render `/outages.geojson` with [Leaflet](https://leafletjs.com/), [MapLibre GL JS](https://maplibre.org/) (open source) or [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/). Weight a heatmap by `impact.customersAffected`. For scale, serve vector tiles from PostGIS. Real-world references: [UK Power Networks live faults open data](https://ukpowernetworks.opendatasoft.com/) and [ODIN](https://odin.ornl.gov/).

### Step 7 — Push / notification fan-out
On each "outage changed" event:
1. **Resolve recipients** — geospatial match (PostGIS point-in-polygon) of affected feeders/area to consenting subscribers.
2. **Webhooks** for integrators/apps — sign and retry per [Standard Webhooks](https://www.standardwebhooks.com/) (HMAC + timestamp + unique id; adopted by Anthropic, OpenAI, Supabase…); optionally use [Svix](https://docs.svix.com/) as managed infra. Wrap events in [CloudEvents](https://cloudevents.io/) for a portable envelope.
3. **Consumer channels** — app push via [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging); SMS/voice via [Twilio](https://www.twilio.com/docs) or India providers like [MSG91](https://docs.msg91.com/); [WhatsApp Business Platform](https://developers.facebook.com/docs/whatsapp); email via [Amazon SES](https://docs.aws.amazon.com/ses/) / [SendGrid](https://www.twilio.com/docs/sendgrid).
4. **Public mass alerting** — emit **CAP** and feed India's [SACHET](https://sachet.ndma.gov.in/) (NDMA/C-DOT, CAP-based) and the [NDMA Cell Broadcast](https://ndma.gov.in/) system for wide-area events; CAP maps 1:1 from the schema (Design note §8.2).

### Step 8 — Delivery guarantees
Idempotent producers and consumers (dedupe on `id`+`msgType`+`lastUpdatedAt`); retries with exponential backoff + dead-letter queues; per-outage ordering; suppress duplicate consumer notifications (one per status change, not per feeder).

### Step 9 — Observability & reliability KPIs
Instrument with [OpenTelemetry](https://opentelemetry.io/) + [Prometheus](https://prometheus.io/)/[Grafana](https://grafana.com/). Track **detection→publish latency**, push delivery/open rates, and compute **SAIDI/SAIFI/CAIDI** ([IEEE 1366](https://standards.ieee.org/ieee/1366/)) from `actualRestoration` + `customersAffected` — the records double as your regulatory reliability source (CEA/RDSS).

### Step 10 — Security, privacy, governance
PII (consumer lists/contacts) only on the **authenticated tier**; record consent; rate-limit and authenticate all writes; sign webhooks; audit-log lifecycle changes. Optionally issue notices as W3C [Verifiable Credentials](https://www.w3.org/TR/vc-data-model/) for cross-network trust (mirrors `MeterDataCredential`).

### Step 11 — Test & roll out
Contract-test producers against `schema.json`; load-test the pull feed behind the CDN at outage-storm volumes; chaos-test push retries; pilot on **one circle**, validate SAIDI/SAIFI against existing reports, then scale.

---

## 5. Reference building blocks

| Concern | Options |
|---|---|
| Schema / API | [JSON Schema](https://json-schema.org/) · [OpenAPI](https://www.openapis.org/) · [CAP v1.2](https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2-os.html) · [GeoJSON RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946) · [CloudEvents](https://cloudevents.io/) |
| Event broker | [Kafka](https://kafka.apache.org/) · [NATS JetStream](https://docs.nats.io/nats-concepts/jetstream) · [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/) · [Google Pub/Sub](https://cloud.google.com/pubsub/docs) · [AWS SNS](https://docs.aws.amazon.com/sns/)/[SQS](https://docs.aws.amazon.com/sqs/) |
| Store / geo | [PostgreSQL](https://www.postgresql.org/) · [PostGIS](https://postgis.net/) |
| Pull edge | [Cloudflare CDN](https://developers.cloudflare.com/cache/) · [CloudFront](https://docs.aws.amazon.com/cloudfront/) · [HTTP caching/ETag](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching) |
| Webhooks | [Standard Webhooks](https://www.standardwebhooks.com/) · [Svix](https://docs.svix.com/) |
| Consumer push | [FCM](https://firebase.google.com/docs/cloud-messaging) · [Twilio](https://www.twilio.com/docs) · [MSG91](https://docs.msg91.com/) · [WhatsApp](https://developers.facebook.com/docs/whatsapp) · [SES](https://docs.aws.amazon.com/ses/) |
| Public alerting (India) | [SACHET](https://sachet.ndma.gov.in/) · [NDMA](https://ndma.gov.in/) Cell Broadcast |
| Map UI | [Leaflet](https://leafletjs.com/) · [MapLibre GL](https://maplibre.org/) · [Mapbox GL](https://docs.mapbox.com/mapbox-gl-js/) |
| Observability | [OpenTelemetry](https://opentelemetry.io/) · [Prometheus](https://prometheus.io/) · [Grafana](https://grafana.com/) |
| Working examples | [UK Power Networks live faults](https://ukpowernetworks.opendatasoft.com/) · [ODIN](https://odin.ornl.gov/) |

---

## 6. MVP vs full system

| | MVP (weeks) | Full (production) |
|---|---|---|
| Ingest | Manual OMS entry only | AMISP/RTDAS feeder-status ingest + enrichment |
| Store | Postgres | Postgres + PostGIS + broker |
| Pull | `/outages` + `/outages.geojson` behind CDN | + `/lookup`, CAP feed, public/auth tiers |
| Push | One channel (SMS or app) by area | Webhooks + multi-channel + CAP/SACHET, geo-targeted |
| Map | Leaflet + GeoJSON | Vector tiles + heatmap |
| KPIs | Manual | Automated SAIDI/SAIFI dashboards |

---

## 7. Why this makes operations more efficient
- **One source of truth** replaces PDFs/WhatsApp forwards — every channel (web, app, map, SMS, CAP) renders the same validated object.
- **Auto-detection → auto-publish** cuts the lag between a feeder trip and customer awareness, reducing call-centre load (the OMS already tracks `complaintCount`).
- **Geo-targeted push** notifies only affected consumers, building trust and cutting "no power?" calls.
- **Reliability KPIs fall out for free** — `actualRestoration` + `customersAffected` feed SAIDI/SAIFI/CAIDI for CEA/RDSS reporting without a separate data pull.
- **Interoperable** — standards-aligned (CAP/CIM/IEEE 1782/GeoJSON) so aggregators, regulators, and apps integrate once.
