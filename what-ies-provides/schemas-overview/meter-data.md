# MeterData v0.6

*A lightweight, high-throughput telemetry payload schema for exchanging smart-meter readings and events over the IES Data Exchange (Beckn) wire, without cryptographic wrapping.*

| Field | Value |
|---|---|
| Document | IES/MD/0.6 |
| Status | Stable field set for the eight compact profiles and the Data Descriptor Engine; the overlap with ElectricityCredential (Section 11, Point 2 below) is explicitly marked in the schema's own README as pending reconciliation in a future major version |
| Applicability | Issued by AMISPs, HES/MDM systems and DISCOMs; consumed by DISCOMs, regulators (SERC/CERC), TSPs and consented third parties over IES Data Exchange |
| This version | Covers the eight compact telemetry profiles and the shared Data Descriptor Engine, defined in [schema.json](../../schemas/MeterData/v0.6/schema.json) |

## 1. Scope and Purpose

The stakeholders are the AMISP or HES/MDM system that holds smart-meter data, and the DISCOM, regulator, TSP or consented third party that needs it. Without a common shape for telemetry, each of these parties would exchange meter readings, billing resets, events and alarms in a bespoke format, and every new integration would require a fresh parser on both sides.

This document explains the **MeterData v0.6** schema — it does not define a new schema; it walks through the schema that already exists at `schemas/MeterData/v0.6/schema.json`.

## 2. What It Records / Covers

MeterData v0.6 captures, across eight profile shapes:

- **Identity** — which meter(s), customer(s) and service delivery point(s) a payload is about.
- **Slow-changing customer and service-point metadata** — the customer, their tariff category, sanctioned load, payment mode, and the meters and associations attached to their connection.
- **High-resolution interval readings** — block load survey data at intervals such as 15 or 30 minutes.
- **Daily accumulated readings** — a daily load survey summary.
- **Monthly billing resets** — cumulative registers, time-of-use buckets and maximum demand at each billing cycle.
- **Computed billing details** — bill amount, bill number, due dates, currency, prepaid balance and payment status.
- **Instantaneous electrical snapshots** — voltages, currents, and active/reactive power at one moment in time.
- **Event history** — diagnostic and tamper events matching IS 15959 codes.
- **Active alarms** — real-time alerts such as tamper, low prepayment credit, voltage sag or overload.

It does not carry a cryptographic signature or proof of provenance — that is deliberately left out of this schema and handled separately (see Section 9).

## 3. How Each Item is Identified

MeterData uses a generic `Identifier{scheme, value, namespace}` object rather than a single fixed identifier type. The `scheme` field names how the value should be read, and is one of: `METER_SERIAL`, `METER_BADGE`, `MRID`, `OBIS`, `SHORT_CODE`, `CONSUMER_NUMBER`, `SERVICE_DELIVERY_POINT`, `DID`, `ORG`, `OTHER`.

Most of these schemes carry existing identifiers verbatim — a meter serial number, a consumer number, a service-delivery-point code — reused as-is rather than replaced. Two schemes come from named external standards: `MRID` follows the Common Information Model (IEC 61968/61970), and `DID` follows W3C DID Core where a verifiable digital identifier is used instead of a local account number.

Individual readings are named either by their OBIS code (for example `1.0.1.8.0.255`) or by a short human-readable name (for example `kWh imp`); the crosswalk between the two forms lives in a canonical registry file, `IES codes.json`, shipped alongside the schema.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **Verifiable Credential (VC)** — a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer.
- **Beckn Protocol** — the open interaction protocol IES uses for discovery, negotiation and confirmation between parties (search / select / init / confirm / status and their `on_` callbacks); MeterData travels as a payload on this wire during Data Exchange.
- **AMISP** — an Advanced Metering Infrastructure Service Provider, the metering agency that operates smart-meter data collection on a DISCOM's behalf, and a typical issuer of MeterData payloads.
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers, and a typical consumer of MeterData payloads.
- **SERC/CERC** — State/Central Electricity Regulatory Commission, the tariff and licensing regulator for the power sector, and a downstream consumer of MeterData for regulatory reporting.
- **OBIS code** — the object identification system, standardised in India via IS 15959, used to name a specific register or reading, such as `1.0.1.8.0.255`.
- **Data Descriptor Engine** — the mechanism (the `PayloadDescriptorProfile` object, described in Section 7) that lets bulk numeric telemetry avoid repeating metadata inline.
- **READING vs. USAGE** — two modes a telemetry value can carry: `READING` is the physical register value at a point in time (strictly increasing for cumulative registers); `USAGE` is the delta or consumed amount over a period.
- **Common Information Model (CIM)** — the IEC 61968/61970 data model that defines `MRID`, one of the identifier schemes MeterData reuses.

## 5. Basis of Standards

The IES order of preference is fixed, always in this order:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

MeterData follows Indian standards directly wherever telemetry conventions exist: **IS 15959** governs the OBIS-code and event-ID conventions used for Indian AMI, and **IS 16444** is the overarching AC smart meter specification that MeterData's profile shapes are built to carry data for.

## 6. Where Indian Standards Do Not Yet Exist

The one gap documented for this schema is the identifier scheme: the `MRID` identifier scheme is sourced from the IEC Common Information Model (IEC 61968/61970) because no Indian standard defines an equivalent network-asset identifier scheme.

## 7. The Record(s)

MeterData v0.6 defines nine record shapes, discriminated by a `profileType` field on eight of them:

- **CustomerProfile** — slow-changing. Groups a `Customer` object (tariff category, sanctioned load, billing cycle, payment mode, connection type, contract maximum demand, sanctioned export load) with the customer's `ServiceDeliveryPoint`, `Meter` and `Association` records. Issued/updated by the DISCOM or AMISP whenever customer or connection details change.
- **IntervalProfile** — high-frequency. Block load survey data at fixed intervals (e.g., 15/30 minutes). Issued by the AMISP or HES on each read cycle.
- **DailyProfile** — daily accumulated load survey. Issued once per day.
- **MonthlyProfile** — monthly. Cumulative registers, time-of-use buckets and maximum demand at each billing reset. Issued once per billing cycle.
- **BillDetailsProfile** — computed billing outcome for a cycle (amount, bill number, due dates, currency, prepaid balance, payment status). Issued by the billing/CIS system.
- **InstantaneousProfile** — a real-time snapshot of electrical quantities at one moment. Issued on demand or on a short polling cycle.
- **EventProfile** — a log of `MeterEvent` entries (diagnostic and tamper events, matching IS 15959 codes). Issued as events occur.
- **AlarmProfile** — a log of `MeterAlarm` entries (immediate-state conditions: tamper, low prepayment credit, voltage sag, overload). Issued as alarms activate or clear.
- **PayloadDescriptorProfile** — not a telemetry profile itself. A shared dictionary object carried alongside the other profiles in a payload: `payloadDescriptors` holds reading metadata (readingType, unit, flowDirection, category, multiplier) and `compactSequences` holds the column layout of dense numeric matrices, so bulk numeric data does not need to repeat this metadata inline. This is the Data Descriptor Engine referred to elsewhere in this page.

Every one of the eight `profileType` records inherits from a common `BaseProfile`, which carries only identity fields (`meterRefs`, `customerRefs`, `serviceDeliveryPointRefs`, `profileType`); each derived profile then adds only the fields relevant to its own cadence. Individual readings within these profiles distinguish `READING` (the physical register value) from `USAGE` (the delta over a period), and each carries a `validationStatus` (`VALID`/`ESTIMATED`/`MANUAL`/`SUSPECT`/`REJECTED`) and a `source` (`METER`/`HES`/`ESTIMATED`/`MANUAL`/`IMPORT`/`MDM_COMPUTED`/`CIS_COMPUTED`).

## 8. Schedule I — Field Reference (summary)

MeterData v0.6 is built from these logical blocks:

- **BaseProfile** — shared identity fields (`meterRefs`, `customerRefs`, `serviceDeliveryPointRefs`, `profileType`) inherited by every profile.
- **CustomerProfile / Customer / ServiceDeliveryPoint / Meter / Association** — customer, connection and meter-installation metadata, including feeder/DT topology (`parentResources`) and lightweight DER capacity fields (`generationCapacityKw`, `storageCapacityKw`) on `Association`.
- **IntervalProfile, DailyProfile, MonthlyProfile** — the three load-survey cadences.
- **BillDetailsProfile** — computed billing outcome.
- **InstantaneousProfile** — real-time electrical snapshot.
- **EventProfile / MeterEvent** — diagnostic and tamper event log.
- **AlarmProfile / MeterAlarm** — active alert state.
- **PayloadDescriptorProfile** — the shared descriptor dictionary (`payloadDescriptors`, `compactSequences`) that powers the Data Descriptor Engine.
- **Identifier** — the generic `{scheme, value, namespace}` object used throughout (Section 3).

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [MeterData v0.6 — README](../../schemas/MeterData/v0.6/README.md#field-reference).

## 9. Schedule II

MeterData v0.6 is a stand-alone payload schema — it does not itself wrap or depend on another schema. When a use case needs cryptographic proof of provenance (a signed, durable record rather than a raw telemetry exchange), a MeterData payload is instead wrapped *inside* the separate **MeterDataCredential** schema, which adds the Verifiable Credential envelope around it. MeterData itself carries no such wrapper.

## 10. How It Fits Together

MeterData is the payload that travels on the IES Data Exchange (Beckn) wire whenever raw smart-meter telemetry needs to move between an AMISP, a DISCOM, a regulator or a consented third party — this is its role in the **Smart Meter Data Exchange** use case, where it is the primary telemetry payload. When a consumer instead wants a durable, verifiable record of their own readings — for example to share with a bank or another verifier — the same MeterData payload shape is wrapped inside a **MeterDataCredential**, which is the pattern used in the **Consumer Meter Digest** use case. In both cases MeterData defines what the data looks like; it is the surrounding exchange (Beckn) or wrapper (MeterDataCredential) that determines how it is discovered, requested and, where needed, signed.

MeterData also has a documented, not-yet-reconciled overlap with the **ElectricityCredential** schema (see Section 11), since both schemas separately describe some overlapping consumer and DER-capacity concepts for different purposes.

## 11. Points for Confirmation

1. **meterType vs. meterCategory** — MeterData keeps both fields on `Meter`: `meterType` (the meter's communication/technology capability, e.g. AMR/AMI) and `meterCategory` (the IS 15959 regulatory category, A/B/C/D1-D4). Both are retained deliberately; no consolidation is planned, but reviewers should confirm this is still the intended design.
2. **premisesType vs. consumerCategory** — `ElectricityCredential` defines `premisesType` and `MeterData` separately defines `consumerCategory` (the utility tariff category, e.g. LT2A/NDS/HT). These were kept as two separate fields across the two schemas to avoid breaking backward compatibility, and are explicitly marked in the schema's own README for future reconciliation.
3. **DER capacity modelling divergence** — `ElectricityCredential` models every physical DER asset richly via a typed `energyResources[]` array, while `MeterData` only carries two lightweight capacity fields (`generationCapacityKw`, `storageCapacityKw`) on its `Association` object. This structural divergence is explicitly documented as pending alignment in a future major version.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 15959 | OBIS-code and event-ID conventions for Indian AMI |
| IS 16444 | AC smart meter specification |
| IEC 61968 / IEC 61970 | Common Information Model (CIM) — source of the `MRID` identifier scheme |

### Annexure B — Example Payloads

Example payloads for each profile type are available in [`schemas/MeterData/v0.6/examples/`](../../schemas/MeterData/v0.6/examples).

### Annexure C — JSON Schema

The authoritative machine-readable definitions are [`schemas/MeterData/v0.6/schema.json`](../../schemas/MeterData/v0.6/schema.json) and [`schemas/MeterData/v0.6/attributes.yaml`](../../schemas/MeterData/v0.6/attributes.yaml).
