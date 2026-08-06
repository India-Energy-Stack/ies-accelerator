# Smart Meter Data Exchange

*A standard, audit-trailed way to exchange smart-meter telemetry between an AMISP, a DISCOM, a State regulator, and consented third parties — over [IES Data Exchange](../what-ies-provides/discover.md), carrying the [MeterData](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) payload.*

**[Implementation Guide →](../use-cases/smart-meter-data-exchange/README.md)**

| Field | Value |
|---|---|
| Document | IES/SMDX-PROFILE/0.6 |
| Status | Piloted — see [Status](../STATUS.md) |
| Applicability | All AMISPs, DISCOMs and SERCs |
| This version | Built on MeterData v0.6, MeterDataRequest v0.6 and (optional) MeterDataRequestCredential v0.1 over Beckn. |

> For consumer-pull of *their own* meter data, see **[Consumer Meter Digest](consumer-meter-digest.md)**. This is the bulk, scheduled, machine-to-machine flow.

---

## 1. Scope and Purpose

The stakeholders are the DISCOM (data fiduciary), the AMISP (data processor) and any authorised third party. Today every DISCOM-AMISP pair builds a bespoke integration — a one-time dump, then incremental files over FTP, or a project-specific API — negotiated and built from scratch each time.

This document defines **Smart Meter Data Exchange** — a one-to-many, standard data shape (MeterData v0.6) carried over a one-to-many discovery and contracting layer (Beckn). A TSP integrates once and the same pattern works across DISCOMs. IES standardises **the interface where parties exchange data** — it does not change how any party stores or moves data internally.

## 2. What It Records / Covers

Four things, and only these four:

| Records | Detail | Source |
|---|---|---|
| The contract | How a request is discovered and agreed | Beckn protocol |
| Consent & scope | How consent, scope and duration are recorded | MeterDataRequest v0.6 / MeterDataRequestCredential v0.1 |
| The data shape | The MeterData wire format | MeterData v0.6 (DLMS-COSEM / IS 15959) |
| Receipts & audit | Proof of what was exchanged | Beckn protocol; W3C VC |

The meter keeps speaking DLMS-COSEM / IS 15959; the head-end, MDM and AMISP's systems are unchanged.

Eight MeterData v0.6 compact profiles cover every cadence:

| Profile | Carries |
|---|---|
| `CUSTOMER` | Slow-changing customer / service-point / meter installation metadata |
| `INTERVAL` | Block load survey at 15- or 30-min resolution |
| `DAILY` | Daily accumulated load survey |
| `MONTHLY` | Monthly billing resets (cumulative kWh, ToU, MD) |
| `BILL_DETAILS` | Utility-side billing computed details |
| `INSTANTANEOUS` | Real-time snapshot of V/A/P/Q |
| `EVENT` | IS 15959 diagnostic / tamper events |
| `ALARM` | Real-time active alerts |

## 3. How Each Item is Identified

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (data fiduciary) | `did:web` on owned domain | `did:web:ies.discom.example` |
| AMISP / TSP (data processor) | `did:web` on owned domain | `did:web:np.example.com` |
| Meter / DT / Feeder | `did:web` under DISCOM domain | `did:web:ies.discom.example:assets:meter:NM-44091234` |

**No new IDs to allocate.** Existing meter SLNOs, DT codes and feeder codes stay exactly as they are; the `did:web` wrapper reuses them. Adoption is *nice to have* for a first deployment — bare IDs work in payloads initially.

## 4. Definitions

- **DLMS-COSEM** — the meter↔head-end wire protocol (IS 15959 in India).
- **OBIS** — Object Identification System code identifying a meter register.
- **HES** — Head-End System, the AMI layer talking to meters.
- **MDM/MDMS** — Meter Data Management System, the DISCOM's system of record.
- **AMISP** — the entity deploying and operating smart meters and the HES for a DISCOM.
- **READING vs USAGE** — the physical register value vs. the delta/consumed amount over a period.

## 5. Basis of Standards

See [Schemas — Standards precedence](../schemas/README.md#standards-precedence) for the fixed IES order of preference.

| Standard | Role here |
|---|---|
| **IS 16444** | Smart meter specification (followed directly) |
| **IS 15959 / IEC 62056** (DLMS-COSEM) | Meter readings (followed directly) |
| **MeterData v0.6** | IES specification standardising the JSON shape that carries those readings |
| **IEC 61968 / -100** | HES↔MDMS interoperability (CEA/RDSS guidance, alongside MultiSpeak) |
| **CIM (IEC 61968-9)** | Master data |

## 6. Where Indian Standards Do Not Yet Exist

The compact-profile **JSON shape** is an IES specification — no predating Indian or international standard. Beckn (discovery/contracting) is also an IES choice. Event codes follow **IS 15959** allocations directly.

## 7. The Record

No Verifiable Credential by default. Each exchange produces: a **signed Beckn contract** (discovery, scope, parties, time-bound authorisation), a **signed MeterData v0.6 payload** (inline or signed-URL), and a **signed receipt**. Together: a verifiable audit trail for DPDP accountability and dispute resolution. For a durable, holder-bound record, wrap in **[MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6)** — see [Consumer Meter Digest](consumer-meter-digest.md).

## 8. Schedule I — Static Fields of the Data Exchange

Schedule I tabulates the static contracts that frame this exchange: [MeterDataRequest v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequest/v0.6) selects scope and capabilities, and the optional [MeterDataRequestCredential v0.1](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequestcredential/v0.1) makes a request portable and verifiable. The [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) response itself is the live half — see [Schedule II](#id-9.-schedule-ii-meter-readings-live-record). **Schema Requires** is normative for the named schema; **SMDX Guidance** is informative deployment guidance.

### 8.1 MeterDataRequest v0.6 — Query and Scope

| **Normative Path** | **Type / Allowed Value** | **Schema Requires** | **Standard** *(informative)* | **SMDX Guidance** *(informative)* |
|---|---|---|---|---|
| `consumers[]` | array of URI / DID | Optional | DID Core; DPDP consent scope | Use only for consumer-scoped requests |
| `resources[]` | array of resource URI / DID | Optional | IES identifiers | Use for meters, service points, feeders or other registered resources |
| `scope` | `ResourceOnly`, `ResourceAndChildren`, `ChildrenOnly` | Optional | MeterDataRequest v0.6 | State the hierarchy rule explicitly for feeder/DT requests |
| `from` | date-time | Required | ISO 8601 | Start of the requested data window |
| `duration` | duration | Required | ISO 8601 | Requested window length; the provider still enforces its advertised maximum |
| `consumerConsent[]` | array of consent references | Optional | DPDP accountability | Required by policy when the request exposes consumer-linked data |
| `authorisation` | inline `MeterDataAuthorisation` or URI | Optional | MeterDataRequest v0.6 | Bind the requester, purpose, validity and allowed capabilities |
| `capabilitiesRequested` | `MeterDataCapabilities` object | Required | MeterDataRequest v0.6 | Request only profiles/registers the provider advertises |
| `maxRecordsShared` | integer ≥ 1 | Optional | MeterDataRequest v0.6 | Use as a batch/page cap, not as a substitute for the time window |

### 8.2 Capabilities and Authorisation

| **Normative Path** | **Type / Allowed Value** | **Schema Requires** | **SMDX Guidance** *(informative)* |
|---|---|---|---|
| `capabilitiesRequested.profiles[]` | array of `ProfileCapability` | Required | Enumerate each requested telemetry profile |
| `profiles[].profileType` | `CustomerProfile`, `IntervalProfile`, `DailyProfile`, `MonthlyProfile`, `BillDetails`, `InstantaneousProfile`, `EventProfile`, `AlarmProfile` | Required per entry | `DESCRIPTOR` is not requestable; it accompanies the response when compact data needs a dictionary |
| `profiles[].readings[]` | array of `ValueCapability` | Optional | Omit to request all supported registers in that profile; otherwise list only required registers |
| `readings[].value` | OBIS code or governed short code | Required per value capability | Prefer the canonical code published by the provider |
| `readings[].mode` | `READING` or `USAGE` | Optional | Match the physical meaning of the register and response descriptor |
| `readings[].multiplier` / `.accuracy` | number / number | Optional | Request only when scaling or accuracy is material |
| `capabilitiesRequested.supportedScopes[]` | array of scope enums | Optional | Relevant in a provider capability advertisement; the request must stay within it |
| `capabilitiesRequested.maxHistoryDuration` | ISO 8601 duration | Optional | Provider-advertised history ceiling |
| `authorisation.grantor` / `.grantee` / `.purpose` | URI / URI / text | All required in an inline authorisation | Identify who granted access, who receives it, and why |
| `authorisation.validFrom` / `.validUntil` | date-time / date-time | Both required | Reject expired or not-yet-valid grants |
| `authorisation.capabilities` | `MeterDataCapabilities` | Required | Must cover the requested profile, scope and registers |

### 8.3 Optional MeterDataRequestCredential v0.1

| **Normative Path** | **Type** | **Schema Requires** | **SMDX Guidance** *(informative)* |
|---|---|---|---|
| `@context` / `type` | W3C credential context / type array | Required by the externally referenced W3C Credential branch | Include the W3C, EnergyCredential and MeterDataRequestCredential contexts and the concrete credential type |
| `id` | credential URI / URN | Optional; permitted by the open credential envelope | Assign a unique request-credential identifier |
| `issuer` | EnergyCredential issuer object | Optional at the EnergyCredential root; if present, `id`, `name` and `licenseNumber` are required | Mandatory for a portable authorisation; identify the issuing requester/authority |
| `validFrom` / `validUntil` / `credentialStatus` / `proof` | credential envelope fields | Not required at the wrapper root; nested status/proof requirements apply if those objects are present | Apply the validity, revocation and signature rules required by the exchange policy |
| `credentialSubject.id` | requester URI / DID | Optional when `credentialSubject` is present | Identify the authorised requesting entity |
| `credentialSubject.meterDataRequest` | MeterDataRequest v0.6 payload | Required inside `credentialSubject`; the wrapper does not currently require `credentialSubject` itself | Carry the exact scoped, time-bounded request being authorised |

As with MeterDataCredential, repository-local structural validation stubs the external EnergyCredential reference. A provider must enforce the complete credential envelope and exchange-policy requirements separately.

For Indian-terminology mapping, see **[IES Meter Data Model](../use-cases/smart-meter-data-exchange/ies-meter-data-model.md)**.

## 9. Schedule II — Meter Readings (Live Record)

Schedule II is the **live half** of this exchange — the fields that keep arriving after the request is agreed, as against the static request, authorisation and credential contracts of Schedule I. Every field below is carried in the [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) response.

Scope is set in Schedule I and enforced here: a response carries only the profiles and period the authorisation in §8.2 permits.

### 9.1 MeterData v0.6 — Response Profiles

MeterData has **nine total record shapes**: one shared `DESCRIPTOR` dictionary plus the eight requestable telemetry profiles below.

| **`profileType`** | **Schema-required Payload Fields** | **Purpose in this Use Case** | **Standards / Basis** *(informative)* |
|---|---|---|---|
| `DESCRIPTOR` | `id`, `payloadDescriptorSets[]` | Defines reading types, units, modes and compact sequences used by response profiles; not directly requestable | MeterData v0.6; IS 15959 / OBIS |
| `CUSTOMER` | `customer`, `serviceDeliveryPoints[]`, `meters[]`, `associations[]` | Slow-changing customer, connection, meter and topology metadata | CIM (IEC 61968-9) |
| `INTERVAL` | `meterRefs[]`, `intervalPeriod`; data in `intervals[]` or `readings[]` | 15- or 30-minute load survey | IS 15959 / DLMS-COSEM |
| `DAILY` | `meterRefs[]`, `intervalPeriod`; data in `intervals[]` or `readings[]` | Daily accumulated survey | IS 15959 / DLMS-COSEM |
| `MONTHLY` | `meterRefs[]`, `timePeriod`, `readings[]`; optional `touBuckets[]` | Billing-reset and ToU history | IS 15959; SERC tariff periods |
| `BILL_DETAILS` | `meterRefs[]`, `timePeriod`, `amountDue`; optional readings, charges and payment fields | Utility-computed billing outcome | Utility billing / CIS |
| `INSTANTANEOUS` | `meterRefs[]`, `timestamp`, `readings[]` | Real-time V/A/P/Q and related snapshot values | IS 15959 / DLMS-COSEM |
| `EVENT` | `meterRefs[]`, `timePeriod`, `events[]` | Diagnostic and tamper events | IS 15959 event allocation |
| `ALARM` | `meterRefs[]`, `timestamp`, `alarms[]` | Active or cleared alert state | MeterData v0.6 |

### 9.2 Shared Response Fields and Compact Data

| **Normative Path** | **Type / Allowed Value** | **Schema Requires** | **SMDX Guidance** *(informative)* |
|---|---|---|---|
| `meterRefs[]` | `Identifier` `{scheme, value, namespace?}` | Required on all seven non-customer telemetry profiles | Bind every series to its source meter(s) |
| `customerRefs[]` / `serviceDeliveryPointRefs[]` | arrays of `Identifier` | Optional | Include only at the authorised disclosure level |
| `payloadDescriptorSetRef` / `compactSequenceRef` | text references | Optional | Resolve against the accompanying `DESCRIPTOR` profile |
| `payloadDescriptorSets[].payloadDescriptors[]` | descriptor objects | Required inside each descriptor set | Declare `readingType`; add OBIS, unit, flow direction and `reportedMode` where known |
| `intervals[].id` | integer | Required per interval | Strictly increasing within a profile |
| `intervals[].payloads[]` | compact primitive array | Optional | Arity and order must match the referenced compact sequence |
| `intervals[].readings[]` / profile `readings[]` | array of `Reading` | Optional except where the profile requires it | Each reading requires `readingType` and numeric `value` |
| `readings[].validationStatus` / `.source` | governed enums | Optional | Preserve estimation, rejection and source provenance from HES/MDM |
| `events[].timestamp` / `.eventId` | date-time / integer | Both required per event | Use the IS 15959 event allocation where applicable |
| `alarms[].timestamp` / `.alarmId` / `.status` | date-time / integer / `ACTIVE` or `CLEARED` | All required per alarm | Keep alarm lifecycle state explicit |

## 10. How It Fits Together

```
Today: DISCOM ─bespoke─ AMISP-1 / AMISP-2 / analytics / third party  (n × m integrations)
With IES: DISCOM ── one MeterData v0.6 over Beckn ──► AMISP-1 / AMISP-2 / analytics / third party  (n + m)
```

**Roles don't change; the record makes them explicit.** The DISCOM remains the data fiduciary (authorises a TSP once, scoped, time-bound); the AMISP remains the processor (IES doesn't alter ownership); the TSP integrates once (same discovery/contract/shape across every adopting DISCOM). Every exchange leaves a signed receipt for DPDP accountability.

## 11. Points for Confirmation

1. **Chunking convention** for bulk historical pulls — being agreed across deployments.
2. **Quality flags** — the v0.6 `validationStatus` enum is stable; the per-cadence recommended profile is being tightened.
3. **Aggregator-controlled DERs** — the consent/control flow for *acting* on (not just reading) a DER is specified separately.

---

## Schemas Used in This Use Case

| Schema | Role |
|---|---|
| [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) | The payload — eight compact profiles |
| [MeterDataRequest v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequest/v0.6) | The query / capabilities shape |
| [MeterDataRequestCredential v0.1](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequestcredential/v0.1) *(optional)* | Seeker authorisation VC |

## Value Unlock

**DISCOMs/AMISPs** — one interface replaces bespoke pair-by-pair integration; months become days. **Regulators/analytics** — one consistent format with a verifiable audit trail; comparable analysis across DISCOMs. **Consumers** — consented third parties reading meter data on standard rails unlocks green loans, automated solar quotes and demand-shift offers.

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 16444 (Parts 1, 2) | AC smart meter — specification |
| IS 15959 (Parts 1–3) | DLMS/COSEM companion spec; OBIS codes; event codes |
| IEC 62056 | DLMS/COSEM |
| IEC 61968-9 | CIM — meter reading and control |
| IEC 61968-100 | Web service implementation profile (CEA AMI guidance) |
| CEA (Installation and Operation of Meters) Regs, 2006 | Metering legal framework |
| RDSS | Policy context for current AMI deployment |
| DPDP Act 2023 | Consent and accountability framework |
| W3C VC Data Model 2.0; W3C DID Core | (Optional — MeterDataRequestCredential) |

## Annexure B — Example Payloads

25 example payloads covering every profile shape and derived reports at **[`schemas/MeterData/v0.6/examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.6/examples)** — highlights: `CustomerProfile.json`, `IntervalProfile.json`, `DailyProfile.json` / `MonthlyProfile.json`, `MultiMeterBulkDataset*.json`, `EventProfile.json` / `AlarmProfile.json`, `AggregatedFeeder.json`.

## Annexure C — JSON Schema

Canonical: `https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/` — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/schema.json), [`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/context.jsonld), [`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/vocab.jsonld), [`IES codes.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/IES%20codes.json) (OBIS registry).

## Annexure D — Derived Views

Computed downstream by the recipient. None is an exchanged record or an additional IES schema.

| **Derived View** | **Inputs** | **Schema Status** | **Treatment** |
|---|---|---|---|
| Feeder-aggregated profile | Meter/SDP topology plus interval, daily or monthly profiles | Derived; no separate schema | Aggregate only within the authorised scope and retain source profile references |
| Anonymised response | Any requested profile after identifier/PII transformation | Derived; examples only | Record the anonymisation method and never imply that a transformed identifier is the original meter ID |
| Billing summary | `MONTHLY` and/or `BILL_DETAILS` profiles | Native source profiles; rendered summary is derived | Preserve the signed/raw response as the audit source |
| Data-quality dashboard | `validationStatus`, `source`, missing interval IDs and cadence | Derived; no `dataQuality` summary object in MeterData v0.6 | Compute rates and exceptions downstream |
| Exchange receipt | Beckn contract, signed response and acknowledgement | Protocol evidence, not a MeterData report | Retain with the request/response identifiers for DPDP and dispute audit |

Example payloads for these response patterns are under [`MeterData/v0.6/examples/`](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.6/examples).
