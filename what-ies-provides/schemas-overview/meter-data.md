# MeterData v0.6

*A lightweight, high-throughput telemetry payload schema for exchanging smart-meter readings and events over the IES Data Exchange (Beckn) wire, without cryptographic wrapping.*

| Field | Value |
|---|---|
| Document | IES/MD/0.6 |
| Status | Stable field set for the nine record shapes and the Data Descriptor Engine (the internal `info.version` inside `attributes.yaml` still reads `0.5.0`, a labeling lag the source has not yet corrected). The overlap with `ElectricityCredential` (Section 11 below) is explicitly marked in the schema's own README as pending reconciliation in a future major version |
| Applicability | Issued by AMISPs, HES/MDM systems and DISCOMs; consumed by DISCOMs, regulators (SERC/CERC), TSPs and consented third parties over IES Data Exchange |
| This version | Covers the nine compact profile shapes and the shared Data Descriptor Engine, defined in [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/schema.json) |

## 1. Scope and Purpose

The stakeholders are the AMISP or HES/MDM system that holds smart-meter data, and the DISCOM, regulator, TSP or consented third party that needs it. Without a common shape for telemetry, each of these parties would exchange meter readings, billing resets, events and alarms in a bespoke format, and every new integration would require a fresh parser on both sides.

MeterData v0.6 is designed around a specific architectural fact: Head-End Systems handle millions of meters, so the wire format has to be cheap to parse and cheap to store, while billing handoffs need clarity and an auditable proof trail. The schema's own documentation (`UserGuide.md`) frames this as two different "forms" of the same nine record shapes — a compact matrix form for HES-to-MDM bulk telemetry, and an elaborated, self-describing form for MDM-to-billing handoffs where auditability matters more than bytes.

This document explains the **MeterData v0.6** schema — it does not define a new schema; it walks through the schema that already exists at `schemas/MeterData/v0.6/schema.json`.

## 2. What It Records / Covers

MeterData v0.6 captures, across nine record shapes:

- **Identity** — which meter(s), customer(s) and service delivery point(s) a payload is about, via the shared `BaseProfile` identity fields (`meterRefs`, `customerRefs`, `serviceDeliveryPointRefs`) that every telemetry profile inherits.
- **Slow-changing customer and service-point metadata** (`CustomerProfile`) — the customer, their tariff category, sanctioned load, payment mode, billing cycle day, contract maximum demand, sanctioned export load, and the meters, service delivery points and `Association` records (feeder/DT topology, telemetry provider, commissioning date, DER capacity) attached to their connection. A `CustomerDetails` sub-object carries the customer's name — the schema explicitly marks this as a **PII sub-object to be omitted entirely for anonymised or pseudonymous exchange**.
- **High-resolution interval readings** (`IntervalProfile`) — block load survey data at intervals such as 15 or 30 minutes (`PT15M`/`PT30M`).
- **Daily accumulated readings** (`DailyProfile`) — a daily load survey summary (`P1D` cadence), structurally identical to `IntervalProfile`.
- **Monthly billing resets** (`MonthlyProfile`) — cumulative registers, time-of-use buckets and maximum demand at each billing cycle. Notably, `MonthlyProfile` is *structurally forbidden* from using the compact matrix form: the schema requires `readings` and `touBuckets` directly and does not permit `intervals` or a `compactSequenceRef`, because — per the README — a monthly snapshot is "sparse and highly variable" (ad-hoc resets, mid-cycle meter swaps) and gains little from dense-array compression.
- **Computed billing details** (`BillDetails`) — bill amount, bill number, due dates, currency (ISO 4217), prepaid balance and payment status, plus a breakdown into `energyCharges`, `fixedCharges` and `otherCharges`.
- **Instantaneous electrical snapshots** (`InstantaneousProfile`) — voltages, currents, and active/reactive power at one moment in time.
- **Event history** (`EventProfile`) — diagnostic and tamper events matching IS 15959 codes, each with an integer `eventId`, phase, and duration.
- **Active alarms** (`AlarmProfile`) — real-time alerts such as tamper, low prepayment credit, voltage sag or overload, each carrying a `status` (`ACTIVE`/`CLEARED`) and `severity` (`CRITICAL`/`WARNING`/`INFO`).

A ninth, non-telemetry shape — `PayloadDescriptorProfile` — carries no readings itself; it is the shared dictionary described in Section 7.

It does not carry a cryptographic signature or proof of provenance — that is deliberately left out of this schema and handled separately (see Section 9). A concrete illustration of how compact the wire format gets: a `DailyProfile` interval row can be as small as

```json
{ "id": 0, "payloads": [24512.4, 25134.8] }
```

with the two numbers' meaning (which OBIS code, what unit, import or export) declared once in a shared `PayloadDescriptorProfile` rather than repeated per row.

## 3. How Each Item is Identified

MeterData uses a generic `Identifier{scheme, value, namespace}` object rather than a single fixed identifier type. The `scheme` field names how the value should be read, and is one of: `METER_SERIAL`, `METER_BADGE`, `MRID`, `OBIS`, `SHORT_CODE`, `CONSUMER_NUMBER`, `SERVICE_DELIVERY_POINT`, `DID`, `ORG`, `OTHER`. Fields that reference an entity by ID (`meterRefs`, `customerRefs`, `serviceDeliveryPointRefs`, `parentResources`, `Customer.id`, `Meter.id`, `ServiceDeliveryPoint.id`) use `IdentifierList` — a non-empty array whose first element is the primary identifier, with any additional elements as alternates under different schemes.

Most schemes carry existing identifiers verbatim — a meter serial number, a consumer number, a service-delivery-point code — reused as-is rather than replaced. Two schemes come from named external standards: `MRID` follows the Common Information Model (IEC 61968/61970), and `DID` follows W3C DID Core where a verifiable digital identifier is used instead of a local account number. In practice, the example payloads consistently use `DID` as the working identifier scheme in the shape `did:dedi:<discom>:<entity-class>:<local-id>` — for instance `did:dedi:bescom:consumers:CONSUMER-ACME-8888`, `did:dedi:bescom:assets:meter:METER-GENUS-01`, and `did:dedi:bescom:assets:feeder:FDR-11KV-BLR-04` for grid-topology parents — showing DeDi (Decentralised Digital Identity registry) naming conventions used consistently across consumer, meter, service-delivery-point, feeder and transformer references, not just meters.

Individual readings are named either by their OBIS code (for example `1.0.1.8.0.255`) or by a short human-readable name (for example `kWh imp`); the crosswalk between the two forms lives in a canonical registry file, `IES codes.json`, shipped alongside the schema. That registry currently lists 75 distinct register codes plus a 25-entry IS 15959 event taxonomy (IDs 1–305+, each with a phase and a kind — `occurrence`, `restoration`, `configurationChange` or `control`) and an 8-entry alarm register (e.g. Voltage Sag, Voltage Swell, Over Current, Magnetic Tamper). Each code entry in the registry carries its own `source` citation down to the table or clause — for example the meter serial number register (`0.0.96.1.0.255`) is sourced to "**IS 15959 Part 1 Table 30; Part 2 Table A12; Part 3 Table 12**", and the manufacturer name register to "**IS 15959 Part 2 Table A12**" — so the crosswalk is not just OBIS-to-label but OBIS-to-clause.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered. MeterData's examples consistently render these under a `did:dedi:` method.
- **DeDi** — the Decentralised Digital Identity registry referenced throughout the schema's guides as the place TSPs resolve `did:dedi:...` identifiers and utility endpoints, and where a `MeterDataCredential`'s `credentialStatus` (revocation) is checked.
- **Verifiable Credential (VC)** — a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer.
- **Beckn Protocol** — the open interaction protocol IES uses for discovery, negotiation and confirmation between parties (search / select / init / confirm / status and their `on_` callbacks); MeterData travels as a payload on this wire during Data Exchange.
- **AMISP** — an Advanced Metering Infrastructure Service Provider, the metering agency that operates smart-meter data collection on a DISCOM's behalf, and a typical issuer of MeterData payloads.
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers, and a typical consumer of MeterData payloads.
- **SERC/CERC** — State/Central Electricity Regulatory Commission, the tariff and licensing regulator for the power sector, and a downstream consumer of MeterData for regulatory reporting.
- **OBIS code** — the object identification system, standardised in India via IS 15959, used to name a specific register or reading, such as `1.0.1.8.0.255`.
- **Data Descriptor Engine** — the mechanism (the `PayloadDescriptorProfile` object, its `payloadDescriptors` and `compactSequences`, described in Section 7) that lets bulk numeric telemetry avoid repeating metadata inline.
- **READING vs. USAGE** — two modes a telemetry value can carry: `READING` is the physical register value at a point in time (strictly increasing for cumulative registers); `USAGE` is the delta or consumed amount over a period. The schema enforces mode-dependent field rules: `openingValue`/`closingValue` on a `Reading` **must only be provided when the associated payload descriptor specifies `reportedMode=USAGE`** — they are structurally excluded otherwise.
- **AccumulationBehaviour** — a register-level classification (`CUMULATIVE`, `DELTA`, `INSTANTANEOUS`, `SUMMATION`, `INDICATING`) distinct from but related to `TelemetryMode`; for example cumulative energy registers use `CUMULATIVE` behaviour and support both `READING` and `USAGE` modes, while Maximum Demand registers use `SUMMATION`/`INDICATING` behaviour and are strictly `USAGE`.
- **Common Information Model (CIM)** — the IEC 61968/61970 data model that defines `MRID`, one of the identifier schemes MeterData reuses.
- **MeterDataCapabilities / MeterDataRequest / MeterDataAuthorisation** — the companion `MeterDataRequest v0.6` schema family (not this schema) through which a Data Provider advertises what it can share, a Data Consumer scopes a query, and a utility issues a signed authorisation grant — the discovery-and-consent machinery that sits in front of a MeterData exchange.

## 5. Basis of Standards

The IES order of preference is fixed, always in this order:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

MeterData follows Indian standards directly and, unusually for a schema in this stack, ties individual fields to specific clauses rather than citing the standard only at the schema level:

- **IS 15959** governs the OBIS-code and event-ID conventions used for Indian AMI. The schema's own `IES codes.json` registry cites, per register, the exact Part and table — for example the meter serial number and device ID registers are sourced to **IS 15959 Part 1 Table 30 / Part 2 Table A12 / Part 3 Table 12**, and other registers cite **Part 2 Clause 13**, **Clause 14**, **Table A1**, **Table A4**, **Table A8**, and combinations across Parts 1–3 — the registry's citations track which meter category, `A` through `D4`, each register applies to.
- **IS 16444** is the overarching AC smart meter specification that MeterData's profile shapes are built to carry data for.
- The `EventProfile`/`MeterEvent` shape and the 25-entry event taxonomy in `IES codes.json` (IDs 1–305+, phase-qualified, split into occurrence/restoration/configurationChange/control kinds) are sourced to IS 15959's event/diagnostic tables.

## 6. Where Indian Standards Do Not Yet Exist

The one gap documented for this schema is the identifier scheme: the `MRID` identifier scheme is sourced from the IEC Common Information Model (IEC 61968/61970) because no Indian standard defines an equivalent network-asset identifier scheme. MeterData reuses `MRID` as one value of its generic `IdentifierScheme` enum rather than inventing a parallel Indian scheme.

More broadly, MeterData's `Meter.serviceKind` field already anticipates gas, water and heat meters (`ELECTRICITY`/`GAS`/`WATER`/`HEAT`) alongside electricity, but IS 15959 and IS 16444 are electricity-specific — there is no equivalent Indian AMI standard cited in this schema's registry for the other utility kinds, so `serviceKind` values beyond `ELECTRICITY` currently travel without a documented Indian standards basis in this schema.

## 7. The Record(s)

MeterData v0.6 defines nine record shapes, discriminated by a `profileType` field:

- **CustomerProfile** (`profileType: CUSTOMER`) — slow-changing. Groups a `Customer` object (id, name, `consumerCategory`, `sanctionedLoadKw`, `billingCycleDay`, `paymentMode`, `connectionType`, `contractMaxDemandKw`, `tariffCategoryCode`, `sanctionedExportLoadKw`) with the customer's `ServiceDeliveryPoint`, `Meter` and `Association` records. `customer`, `serviceDeliveryPoints`, `meters` and `associations` are all required. Issued/updated by the DISCOM or AMISP whenever customer or connection details change. The schema's own guide notes this profile can also be issued in a **PII-redacted form** — customer name and account PII omitted, consumers referenced only by public DID — for anonymised grid-topology lookups by TSPs (see `Anonymised_Topology_Example.json`).
- **IntervalProfile** (`INTERVAL`) — high-frequency block load survey data at fixed intervals (e.g. `PT15M`/`PT30M`), required field `intervalPeriod`. Issued by the AMISP or HES on each read cycle, typically HES/MDM-originated and deliberately **omitting `customerRefs`** to decouple technical metering data from the commercial billing domain.
- **DailyProfile** (`DAILY`) — daily accumulated load survey (`P1D` cadence), same shape as `IntervalProfile`. Issued once per day.
- **MonthlyProfile** (`MONTHLY`) — cumulative registers, time-of-use buckets (`touBuckets`) and maximum demand at each billing reset; required fields `timePeriod` and `readings`. Structurally cannot carry `intervals` or `compactSequenceRef` (see Section 2). Issued once per billing cycle — or more than once, if a mid-cycle meter swap or an ad-hoc demand reset produces multiple `MonthlyProfile` records chained under the same consumer account (see `Billing_MeterChange.json` and `MonthlyProfile_MultipleResets.json` in the examples directory).
- **BillDetails** (`BILL_DETAILS`) — computed billing outcome for a cycle (`amountDue` and `timePeriod` required; `billNumber`, `billDate`, `dueDate`, `currency`, `energyCharges`, `fixedCharges`, `otherCharges`, `prepaidBalance`, `paymentStatus` optional). Issued by the billing/CIS system, and may carry `source: CIS_COMPUTED` on its readings to show they were derived rather than metered directly.
- **InstantaneousProfile** (`INSTANTANEOUS`) — a real-time snapshot of electrical quantities at one moment; required fields `timestamp` and `readings`. Issued on demand or on a short polling cycle.
- **EventProfile** (`EVENT`) — a log of `MeterEvent` entries (diagnostic and tamper events, matching IS 15959 codes); required fields `timePeriod` and `events`. Each `MeterEvent` has a required `timestamp` and integer `eventId`, plus optional `eventName`, `phase`, `sequence`, `magnitude` and `duration`. Issued as events occur — the guide is explicit that empty telemetry blocks should not be transmitted; the `events` array should only contain diagnosed instances.
- **AlarmProfile** (`ALARM`) — a log of `MeterAlarm` entries (immediate-state conditions: tamper, low prepayment credit, voltage sag, overload); required fields `timestamp` and `alarms`. Each `MeterAlarm` requires `timestamp`, `alarmId` and `status` (`ACTIVE`/`CLEARED`), with optional `alarmName` and `severity` (`CRITICAL`/`WARNING`/`INFO`). Issued as alarms activate or clear.
- **PayloadDescriptorProfile** (`DESCRIPTOR`) — not a telemetry profile itself; a shared dictionary object carried alongside the other profiles in a payload array. Required fields are `id` and `payloadDescriptorSets`, where each `PayloadDescriptorSet` bundles `payloadDescriptors` (register metadata: `readingType`, optional canonical `obis` code, `unit`, `flowDirection`, `category`, `reportedMode`, `touZone`, `multiplier`, `accuracy`) and `compactSequences` (named column layouts of dense numeric matrices, each `SequenceItem` mapping a `readingType` to one of five `attribute` kinds: `value`, `occurredAt`, `openingValue`, `closingValue`, `validationStatus`). This is the Data Descriptor Engine referred to elsewhere in this page.

Every one of the eight `profileType` telemetry records inherits from a common `BaseProfile`, which — as of v0.6 — carries *only* identity and routing fields (`meterRefs` required; `customerRefs`, `serviceDeliveryPointRefs`, `payloadDescriptorSetRef` optional). This is a deliberate architectural tightening: the schema's changelog describes `BaseProfile` as having been "purged of all telemetry-specific properties (`readings`, `intervals`, `timestamp`, `timePeriod`)" so that each derived profile can strictly declare only the fields relevant to its own cadence via JSON Schema `allOf` composition — an `IntervalProfile`, for instance, can never carry a bare `timestamp` or `touBuckets` field, because those belong to other profiles.

Within these profiles, individual readings distinguish `READING` (the physical register value) from `USAGE` (the delta over a period), and each `Reading` or `Override` carries a `validationStatus` (`VALID`/`ESTIMATED`/`MANUAL`/`SUSPECT`/`REJECTED`) and a `source` (`METER`/`HES`/`ESTIMATED`/`MANUAL`/`IMPORT`/`MDM_COMPUTED`/`CIS_COMPUTED`). In the compact matrix form, an `Interval.payloads` array holds positionally-aligned `number`/`string`/`boolean` values against the active `compactSequence`, and a separate sparse `overrides` array — keyed by `descriptorIndex` — is reserved specifically for quality deviance (a `changeMethod` or `failCode` on one bad interval), not for routine per-row metadata like timestamps, which now travel as dense columns instead.

## 8. Schedule I — Field Reference (summary)

MeterData v0.6 is built from these logical blocks:

- **BaseProfile** — shared identity/routing fields (`meterRefs` required; `customerRefs`, `serviceDeliveryPointRefs`, `payloadDescriptorSetRef` optional) inherited by every telemetry profile.
- **CustomerProfile / Customer / ServiceDeliveryPoint / Meter / Association / CustomerDetails** — customer, connection and meter-installation metadata, including feeder/DT topology (`parentResources`, replacing older `feederId`/`dtId` fields), lightweight DER capacity fields (`generationCapacityKw`, `storageCapacityKw`) on `Association`, a multi-utility `serviceKind` on `Meter`, and a PII-isolated `CustomerDetails` sub-object.
- **IntervalProfile, DailyProfile, MonthlyProfile** — the three load-survey cadences, plus `TouBucket` for time-of-use segmentation.
- **BillDetailsProfile** (`BillDetails` in the schema) — computed billing outcome with a charges breakdown.
- **InstantaneousProfile** — real-time electrical snapshot.
- **EventProfile / MeterEvent** — diagnostic and tamper event log.
- **AlarmProfile / MeterAlarm** — active alert state.
- **PayloadDescriptorProfile / PayloadDescriptorSet / PayloadDescriptor / CompactSequence / SequenceItem** — the shared descriptor dictionary that powers the Data Descriptor Engine.
- **Reading / Override / TimePeriod / IntervalPeriod / Interval** — the shared reading and time-window primitives used across profiles.
- **Identifier / IdentifierList** — the generic `{scheme, value, namespace}` object and its non-empty-array wrapper, used throughout (Section 3).

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [MeterData v0.6 — README](../../schemas/MeterData/v0.6/README.md#field-reference).

## 9. Schedule II

MeterData v0.6 is a stand-alone payload schema — it does not itself wrap or depend on another schema. When a use case needs cryptographic proof of provenance (a signed, durable record rather than a raw telemetry exchange), a MeterData payload is instead wrapped *inside* the separate **MeterDataCredential v0.6** schema, which is itself a subclass of **`EnergyCredential v2.0`** (from the Beckn DEG specification) rather than a bespoke envelope: `MeterDataCredential` inherits `issuer`, `validFrom`/`validUntil`, `credentialStatus` (checked against a DeDi registry for revocation) and `proof` (an Ed25519Signature2020 signature) from `EnergyCredential`, and defines only `credentialSubject.meterData` itself. MeterData itself carries no such wrapper, no `issuer`, and no `proof` block.

## 10. How It Fits Together

MeterData is the payload that travels on the IES Data Exchange (Beckn) wire whenever raw smart-meter telemetry needs to move between an AMISP, a DISCOM, a regulator or a consented third party — this is its role in the **Smart Meter Data Exchange** use case, where it is the primary telemetry payload. When a consumer instead wants a durable, verifiable record of their own readings — for example to share with a bank or another verifier — the same MeterData payload shape is wrapped inside a **MeterDataCredential**, which is the pattern used in the **Consumer Meter Digest** use case. In both cases MeterData defines what the data looks like; it is the surrounding exchange (Beckn) or wrapper (MeterDataCredential) that determines how it is discovered, requested and, where needed, signed.

The companion **MeterDataRequest v0.6** family (`MeterDataCapabilities`, `MeterDataRequest`, `MeterDataAuthorisation`) sits in front of the exchange: a provider advertises what profile types, OBIS registers, multipliers and modes it supports via a `MeterDataCapabilities` document; a consumer scopes a query against that capability set; and a utility issues a signed `MeterDataAuthorisation` naming the grantee, grantor, validity window, purpose and the granted capability subset — before any `MeterData` payload is returned. The schema's own `UserGuide.md` documents a five-step TSP access flow (Discovery → Authorisation → User Consent → Data Request → Data Retrieval) that ends with the utility returning a cryptographically signed `MeterData` payload.

A documented "anonymised directory lookup" pattern also uses `CustomerProfile` itself as a PII-redacted topology index: a utility can return a `CustomerProfile` with customer name omitted and consumers referenced only by DID, so a TSP can resolve which meters sit under a given feeder or transformer (via `Association.parentResources`) purely for grid-planning purposes, without ever seeing billing PII.

MeterData also has a documented, not-yet-reconciled overlap with the **ElectricityCredential** schema (see Section 11), since both schemas separately describe some overlapping consumer and DER-capacity concepts for different purposes.

## 11. Points for Confirmation

1. **Internal version label lags the directory name.** `attributes.yaml`'s `info.version` still reads `0.5.0` and its `info.description` still describes "six compact profile shapes (CUSTOMER, INTERVAL, DAILY, BILLING, INSTANTANEOUS, EVENT)" even though the directory is `v0.6` and the schema now defines nine shapes (adding `MONTHLY`, `ALARM` and `DESCRIPTOR`, and renaming `BILLING` to `BILL_DETAILS`). Reviewers should confirm whether this is a stale label needing a fix, or an intentional versioning convention explained elsewhere.
2. **meterType vs. meterCategory.** MeterData keeps both fields on `Meter`: `meterType` (the meter's communication/technology capability, e.g. AMR/AMI/Prepaid/NetMeter/Bidirectional) and `meterCategory` (the IS 15959 regulatory category, A/B/C/D1–D4). Both are retained deliberately; no consolidation is planned, but reviewers should confirm this is still the intended design.
3. **premisesType vs. consumerCategory.** `ElectricityCredential v1.1`'s `attributes.yaml` defines `premisesType` (Residential/Commercial/Industrial/Agricultural) — it is not present in the `v1.0` or `v1.2` `attributes.yaml` files, which instead reference `consumptionProfiles[]` items from an external schema — while `MeterData` separately defines `consumerCategory` (the utility tariff category, e.g. LT2A/NDS/HT/HT-1). These were kept as two separate fields across the two schemas — the pre-existing `consumerCategory` was retained and `premisesType` deliberately excluded from MeterData to avoid breaking backward compatibility — and are explicitly marked in the schema's own README for future reconciliation.
4. **DER capacity modelling divergence.** `ElectricityCredential v1.2` models every physical DER asset richly via a typed, discriminated `energyResources[]` array (seven kinds: `EnergyResourceMeter`, `EnergyResourceGenerator`, `EnergyResourceStorage`, `EnergyResourceEVCharger`, `EnergyResourceInverter`, `EnergyResourceLoad`, `EnergyResourceNetwork`, each inheriting a common attribute bag), while `MeterData` only carries three lightweight capacity fields — `sanctionedExportLoadKw` (on `Customer`), and `generationCapacityKw` / `storageCapacityKw` (on `Association`). This structural divergence is explicitly documented as pending alignment in a future major version.
5. **serviceKind beyond electricity has no cited Indian standard in this schema.** `Meter.serviceKind` already includes `GAS`, `WATER` and `HEAT` alongside `ELECTRICITY`, but every standard cited in this schema (IS 15959, IS 16444) is electricity-specific. It is unclear whether multi-utility metering under `MeterData` is an intentional forward-looking extension point or an artifact of reusing a shared enum, and whether a separate standards basis is expected before non-electricity `serviceKind` values are used in production.
6. **Address representation in `ServiceDeliveryPoint` diverges between schema and examples.** `attributes.yaml` defines `ServiceDeliveryPoint.address` as a reference to the external Beckn `Address/v2.0` schema and `.geo` as a `GeoJSONGeometry`, but the shipped example payloads (e.g. `CustomerProfile.json`, `Billing_MeterChange.json`) instead place flat `addressLine`, `city`, `postalCode`, `latitude` and `longitude` fields directly on the service delivery point. Since the schema is permissive (extra properties are not rejected), both forms currently validate, but reviewers should confirm which representation is the intended canonical one going forward.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 15959 (Parts 1–3) | OBIS-code and event-ID conventions for Indian AMI; the schema's `IES codes.json` registry cites specific Part/Table/Clause references per register (e.g. Part 1 Table 30 / Part 2 Table A12 / Part 3 Table 12 for the meter serial number register; Part 2 Clause 13 and Clause 14 for others) |
| IS 16444 | AC smart meter specification |
| IEC 61968 / IEC 61970 | Common Information Model (CIM) — source of the `MRID` identifier scheme |
| W3C DID Core | Basis of the `DID` identifier scheme, used throughout examples under a `did:dedi:` method |
| W3C VC Data Model 2.0 / Beckn EnergyCredential v2.0 | Not used by MeterData itself, but the basis of the companion `MeterDataCredential` wrapper (Section 9) |

### Annexure B — Example Payloads

Example payloads for each profile type, including edge cases (mid-cycle meter swaps, multiple monthly resets, anonymised topology lookups, OBIS vs. short-code representations, and multi-meter bulk datasets), are available in [`schemas/MeterData/v0.6/examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.6/examples).

### Annexure C — JSON Schema

The authoritative machine-readable definitions are [`schemas/MeterData/v0.6/schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/schema.json) and [`schemas/MeterData/v0.6/attributes.yaml`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/attributes.yaml).
