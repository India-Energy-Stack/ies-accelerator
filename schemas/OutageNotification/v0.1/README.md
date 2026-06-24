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
| `cause.category` | **Borrowed/aligned** — IEEE 1782-2022 cause categories, used with IEEE 1366 (anchored to the IEEE 1782 term IRI) |
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
| `OutageCause` | Coded (OMS fault type/subtype) + free-text reason |
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
