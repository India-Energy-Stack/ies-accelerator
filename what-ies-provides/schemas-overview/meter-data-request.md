# MeterDataRequest v0.6

*The query, capability and authorisation shapes a party uses to ask for smart-meter telemetry — not the telemetry itself.*

| Field | Value |
|---|---|
| Document | IES/MDR/0.6 |
| Status | Draft for technical review — v0.6 is a from-scratch redesign of v0.5 (see version history below), not yet marked stable |
| Applicability | DISCOMs and AMISPs (as providers/grantors); AMISPs, TSPs and other authorised third parties (as requesters/grantees) |
| This version | Covers the three composable request-layer models — MeterDataCapabilities, MeterDataAuthorisation, MeterDataRequest — defined in [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/schema.json) |

## 1. Scope and Purpose

The stakeholders are the party that holds smart-meter data — typically a DISCOM or the AMISP acting on its behalf — and the party that wants a defined slice of it, such as another AMISP, a TSP, or a consented third party. Today, before any data can move, the two sides have to work out three things in an ad hoc way: what the provider is even able to serve, who has actually been allowed to ask for it, and exactly what window and scope a given query covers. Without a shared shape for these three things, each integration re-invents its own capability list, its own authorisation record, and its own query format.

This document explains the **MeterDataRequest v0.6** schema. It does not define a new schema — it walks through the existing one, ahead of the auto-generated field reference in the schema's own README.

Version 0.6 is a structural break from v0.5. The v0.5 schema (still on disk for reference) was a single flat `MeterDataRequest` object: a requester listed `resources[]`, a `scope`, a `from`/`duration` window, and an `includeDetails[]` array of `ProfileRequest` objects (`profileType` + free-text `values[]` + `requestedMode`) — with no way to describe what the provider actually supported, and no separate authorisation record at all. v0.6 splits that single object into three composable models — `MeterDataCapabilities`, `MeterDataAuthorisation`, `MeterDataRequest` — so "what can be served," "who is allowed to ask," and "what is being asked for right now" become distinct, independently reusable records rather than one undifferentiated request blob.

## 2. What It Records / Covers

MeterDataRequest v0.6 is not a Verifiable Credential. It is a `oneOf` payload envelope — the schema's root type (`MeterDataRequest` in `schema.json`, titled "MeterDataRequest Payload") explicitly states a document conforming to it "can be a MeterDataRequest, a MeterDataAuthorisation, or a MeterDataCapabilities document" — and it covers three distinct things:

| Document type | What it records | Required fields |
|---|---|---|
| **`MeterDataCapabilities`** — what a provider can serve | The profile types it supports (`CustomerProfile`, `IntervalProfile`, `DailyProfile`, `MonthlyProfile`, `BillDetails`, `InstantaneousProfile`, `EventProfile`, `AlarmProfile`), optionally down to specific registers or readings (`ProfileCapability.readings[]`), which query scopes it can answer (`supportedScopes[]`), and the longest historical window (`maxHistoryDuration`) | `profiles[]` only (scope and history limit optional) |
| **`MeterDataAuthorisation`** — who is authorised, for what, how long | A grant naming the authorising entity (`grantor`), the authorised entity (`grantee`), the `purpose` as free text, a `validFrom`/`validUntil` window, and the specific slice of `capabilities` granted | all six: `grantor`, `grantee`, `purpose`, `validFrom`, `validUntil`, `capabilities` |
| **`MeterDataRequestObject`** — the actual query | Which `consumers[]` or `resources[]` it targets (both optional and independent), whether it covers just that resource or its children (`scope`), the `from` start and `duration`, `consumerConsent[]` references, the `authorisation` backing it, the `capabilitiesRequested` slice, and an optional `maxRecordsShared` cap | `from`, `duration`, `capabilitiesRequested` |

The profile-type enumeration is drawn from the DLMS-COSEM metering data model; all three document types belong to the MeterDataRequest v0.6 family.

A short real example makes the capability slice concrete. The shipped `Anonymised_Telemetry_Request.json` asks for two DISCOM meters' interval telemetry without naming any consumer at all:

```json
"resources": [
  "did:web:discom.example:meters:DISCOM-SM-2025-654321",
  "did:web:discom.example:meters:DISCOM-SM-2025-999999"
],
"scope": "ResourceOnly",
"capabilitiesRequested": {
  "profiles": [{ "profileType": "IntervalProfile",
    "readings": [{ "value": "kWh imp", "mode": "USAGE" }, { "value": "kWh exp", "mode": "USAGE" }] }]
}
```

## 3. How Each Item is Identified

The schema targets consumers and resources by URI/DID: `consumers[]` is a list of consumer URIs or DIDs, and `resources[]` is a list of resource URIs or DIDs — for example meter DIDs or service-point URIs. The real examples use the `did:web` method throughout — `did:web:ies.discom.example:customer:IN-MH-CUST-80`, `did:web:ies.discom.example:meter:IN-MH-MTR-89721`, `did:web:ies.discom.example:discom:DISCOM`, `did:web:ies.discom.example:tsp:ACME-TSP` — showing a consistent `did:web:<domain>:<role>:<local-id>` shape, though the schema itself only constrains these fields to `format: uri` and does not mandate any particular DID method. `MeterDataAuthorisation.grantor` and `.grantee` are likewise URIs/DIDs identifying the authorising and authorised entities. `consumerConsent[]` is looser still — plain `text` strings rather than `uri`-formatted, and the example payload uses a consent identifier (`did:web:ies.discom.example:consent:CN-89021-SIGNED-BY-USER`) rather than a hash, though the field description only calls for "consent references/receipts."

Individual registers within a capability are identified by `ValueCapability.value`, which is deliberately dual-form: either an OBIS code (e.g. `1.0.1.8.0.255`) or a human-readable short code (e.g. `kWh imp`). All six example payloads shipped with this schema use the short-code form exclusively (`kWh imp`, `kWh imp block`, `kVAh imp block`, `V_R`, `I_R`, `MD kW`, `MD kVA`) — none of them exercise the raw-OBIS form in `value`, even though the field description allows it. The authoritative mapping between these short codes and their underlying OBIS codes, permitted profiles, and supported telemetry modes lives outside this schema, in the sibling `MeterData` family's `IES codes.json` registry (see section 5).

The schema does not mint a new identifier scheme of its own; it consumes whatever DID or URI already identifies the consumer, meter, service point, or organisation elsewhere in IES.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **Verifiable Credential (VC)** — a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer.
- **Beckn Protocol** — the open interaction protocol IES uses for discovery, negotiation and confirmation between parties (search / select / init / confirm / status and their `on_` callbacks).
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers.
- **AMISP** — an Advanced Metering Infrastructure Service Provider, the metering agency that operates smart-meter data collection on a DISCOM's behalf.
- **SERC/CERC** — State/Central Electricity Regulatory Commission, the tariff and licensing regulator for the power sector.
- **MeterDataCapabilities** — the provider's advertised data-access envelope: which profile types and registers it can serve (`profiles[]`, required), which query scopes it supports (`supportedScopes[]`), and the longest history window (`maxHistoryDuration`).
- **MeterDataAuthorisation** — the grant/token recording who authorised whom (`grantor`/`grantee`), for what `purpose`, for how long (`validFrom`/`validUntil`), over a stated `capabilities` slice. All six fields are required.
- **MeterDataRequest** (`MeterDataRequestObject` in the schema definitions) — the actual query payload: target `consumers[]`/`resources[]`, `scope`, `from`/`duration` time window, `consumerConsent[]` references, the backing `authorisation`, the `capabilitiesRequested` slice, and an optional `maxRecordsShared` cap.
- **ProfileCapability** — one entry in `MeterDataCapabilities.profiles[]`, naming a `profileType` (one of the eight enumerated profile types, e.g. `IntervalProfile`) and optionally the specific `readings[]` (registers) supported under it — if `readings` is omitted, the description states "all readings under this profile are supported."
- **ValueCapability** — one entry in `ProfileCapability.readings[]`: the register's `value` (OBIS or short code), its telemetry `mode`, and two rarely-populated optional fields — `multiplier` (a decimal scaling factor, e.g. `0.001` or `1000`) and `accuracy` (an accuracy class or precision value). Only the shipped `Capabilities_Example.json` and `MDM_Capabilities_Example.json` populate `multiplier`/`accuracy` (both `1.0` / `0.5` for interval-profile registers); every other example omits them.
- **ScopeType** — the three-value enum (`ResourceOnly`, `ResourceAndChildren`, `ChildrenOnly`) shared by `MeterDataRequestObject.scope` and `MeterDataCapabilities.supportedScopes[]`, describing whether a query or capability applies to the named resource alone, the resource and everything under it, or only its children (e.g. a feeder's meters but not the feeder itself).
- **TelemetryMode** — the two-value enum (`READING`, `USAGE`) naming whether a register is being asked for as a raw cumulative reading or as a derived usage/consumption figure over the window.
- **OBIS code** — the register identifier used inside `ValueCapability.value` to name a specific meter quantity (e.g. `1.0.1.8.0.255`), drawn from the same code space as IS 15959 / IEC 62056.

## 5. Basis of Standards

The IES order of preference is fixed: **IS → CEA Regulations/IEGC → IEC → IEEE**. MeterDataRequest v0.6 is a request/authorisation envelope, not a metering data model, so `attributes.yaml` carries no `x-standard` field annotations of its own; its one point of contact with a standard is indirect — `ValueCapability.value` names a register using an OBIS/short code from the same register space the sibling `MeterData` schema follows.

| Standard | Role here |
|---|---|
| **IS 15959** ("Data Exchange for Electricity Meter Reading, Tariff and Load Control") | Anchors the register space. The `MeterData v0.6` family's `IES codes.json` gives 75 register entries, each citing a specific IS 15959 part/table/clause — e.g. `0.0.96.1.0.255` (meter serial) → Part 1 Table 30 / Part 2 Table A12 / Part 3 Table 12; `0.0.1.0.0.255` (clock) → Part 2 Table A1; current/voltage/energy registers → Part 2 Clauses 13/14 |
| **IEC 62056** (OBIS / DLMS-COSEM) | Second-order reference behind IS 15959 in the order of preference — the international harmonisation of the OBIS code space, not cited directly by this schema |

Each register entry also states its valid `profiles[]` and `supportedModes[]` (`READING`/`USAGE`), which this schema's `ProfileCapability.profileType` and `ValueCapability.mode` enums are checked against (see section 7).

## 6. Where Indian Standards Do Not Yet Exist

No gap is currently documented for this schema. The request/capability/authorisation shapes (which profiles a provider serves, who is authorised, what window a query covers) are an IES-specific query envelope; they do not correspond to a metering data-model area where an Indian standard would otherwise be expected. The one area with any standards content — the OBIS/short-code register space named in `ValueCapability.value` — is already anchored to specific IS 15959 parts, tables and clauses in the `MeterData` family's code registry, not left undocumented.

## 7. The Record(s)

MeterDataRequest v0.6 defines three related, composable records, all carried as plain JSON payloads rather than credentials:

- **MeterDataCapabilities** — a relatively static record. It is published by a provider (a DISCOM or AMISP) describing what it can serve, and it changes only when the provider's supported profiles, registers, scopes, or history window change. In practice it is advertised as a Beckn catalog entry, so a requester can discover it before asking for anything. The shipped examples show real variety in how granular a capabilities record can be: `Billing_Capabilities_Example.json` advertises a `CustomerProfile` and a `BillDetails` profile with no `readings` at all (meaning "everything under these profiles") alongside a `MonthlyProfile` with four explicit billing registers (`kWh imp`, `kWh exp`, `MD kW`, `MD kVA`) and a ten-year `maxHistoryDuration: "P10Y"`; `MDM_Capabilities_Example.json` instead advertises five profile types including `AlarmProfile` and `EventProfile` (each with no readings listed), a six-register `InstantaneousProfile` naming individual phase voltages/currents (`V_R`, `V_Y`, `V_B`, `I_R`, `I_Y`, `I_B`), all three `supportedScopes` values, and only a three-year `maxHistoryDuration: "P3Y"`.
- **MeterDataAuthorisation** — a grant record with a defined validity window (`validFrom`/`validUntil`). It is issued by the grantor (e.g. the DISCOM) to a grantee (e.g. a TSP) for a stated purpose, and it names a specific `MeterDataCapabilities` subset the grantee is allowed to draw on. It changes whenever access is newly granted, narrowed, or expires. The shipped `Authorisation_Example.json` is concrete about what a real grant narrows down to: the DISCOM (`did:web:ies.discom.example:discom:DISCOM`) grants ACME-TSP (`did:web:ies.discom.example:tsp:ACME-TSP`) a one-year window (`2026-05-01` to `2027-05-01`) for "ESG Carbon Accounting & Trend Analysis" — restricted to just two registers (`kWh imp block` under `IntervalProfile`, `kWh imp` under `DailyProfile`), a single scope (`ResourceOnly`), and a one-year history cap (`P1Y`) — visibly narrower than the provider's full advertised capability set.
- **MeterDataRequest** — the per-query record, issued by the authorised requester each time it wants telemetry. It carries its own capability slice (`capabilitiesRequested`), references or embeds the backing `MeterDataAuthorisation`, and states the specific window, scope and targets for that one query. It is the most frequently created of the three. Both shipped request examples reference their authorisation **by URI rather than embedding it inline** — `Request_Example.json` and `Anonymised_Telemetry_Request.json` both set `"authorisation"` to a full URL pointing at `Authorisation_Example.json`, even though `authorisation` is defined as a `oneOf` accepting either an inline `MeterDataAuthorisation` object or a `uri` string. Neither shipped example exercises the inline-object form, despite it being schema-valid.

These three records relate to each other by direct composition — a `MeterDataRequest` embeds or references a `MeterDataAuthorisation`, which in turn names a `MeterDataCapabilities` subset — and they relate to the wider IES schema set as the request leg that is answered by a separate MeterData response payload.

## 8. Schedule I — Field Reference (summary)

MeterDataRequest v0.6 is built from five logical blocks:

- **MeterDataCapabilities** — a provider's advertised profiles, supported scopes, and maximum history window. Only `profiles[]` is required.
- **MeterDataAuthorisation** — the grantor, grantee, purpose, validity period, and granted capability slice. All six fields (`grantor`, `grantee`, `purpose`, `validFrom`, `validUntil`, `capabilities`) are required.
- **MeterDataRequest** (`MeterDataRequestObject`) — the query itself: targets, scope, time window, consent references, authorisation, requested capability slice, and record cap. Only `from`, `duration` and `capabilitiesRequested` are required.
- **ProfileCapability** — the nested detail inside a capabilities block, naming individual profile types (one of eight enumerated values) and, where needed, the specific registers within them.
- **ValueCapability** — the innermost detail: a register's OBIS/short code, telemetry mode, and optional multiplier/accuracy.

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [MeterDataRequest v0.6 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequest/v0.6#field-reference).

## 9. Schedule II

Not applicable as a stand-alone dependency in this direction, but MeterDataRequest is itself depended on. MeterDataRequest v0.6 is a plain payload schema — it does not wrap or depend on another schema. It can, however, optionally be wrapped: a `MeterDataRequest` payload may be carried inside a **MeterDataRequestCredential** (schema family `MeterDataRequestCredential v0.1`), a W3C Verifiable Credential (VC Data Model 2.0) used to prove the requester's authorisation at Beckn `confirm` time. That wrapper schema is itself declared a **subclass of `EnergyCredential v2.0`** (the Beckn DEG specification's common energy-credential envelope, expressed in its `attributes.yaml` as `allOf: - $ref: https://schema.beckn.io/EnergyCredential/v2.0`), inheriting `issuer`, `validFrom`/`validUntil`, `credentialStatus` and `proof` from that parent rather than redefining them. See the dedicated [MeterDataRequestCredential overview](meter-data-request-credential.md) for that wrapping schema's own field reference.

## 10. How It Fits Together

MeterDataRequest v0.6 is the request/query leg of the Smart Meter Data Exchange use case (see [use-cases/smart-meter-data-exchange/README.md](../../use-cases/smart-meter-data-exchange/README.md)). A provider (DISCOM or AMISP) advertises a `MeterDataCapabilities` catalog entry over Beckn; a requester obtains a `MeterDataAuthorisation` naming the capability slice it may draw on; it then issues a `MeterDataRequest` naming its target consumers or resources, the window it wants, and the capability slice it is asking for. That request is answered by a separate MeterData response payload carrying the actual readings.

Where the requester needs to prove its authorisation cryptographically at Beckn `confirm` time rather than relying on the plain JSON alone, the `MeterDataRequest` is wrapped in a `MeterDataRequestCredential`. The credential's own README describes the check the provider performs on receipt: verify the credential type is `MeterDataRequestCredential`, that `validUntil` has not passed, that `credentialStatus` (checked against the DeDi registry) is not revoked, and that the embedded `MeterDataRequest.resources` fall within the contracted scope. The same credential also carries, in its `resourceAttributes`, an `ies:capabilityProfile` — a `MeterDataRequest`-shaped object describing the *maximum* scope the provider can serve — so the check on `confirm` is really "is the requester's embedded `MeterDataRequest` a subset of the provider's advertised `capabilityProfile`," tying all three of this schema's models (capabilities, authorisation, request) directly into the credential-verification step.

The schema's own semantic validator (`validation/validator.py`, sharing core logic with `MeterData/v0.6/validation/validator.py`) illustrates where structural JSON Schema validation stops and semantic checking begins: it re-parses every `ValueCapability.value` string against the `MeterData` family's `IES codes.json` register table to confirm the register is real, that it is permitted under the stated `profileType` (the validator's own test fixture `invalid_request_profile_mismatch.json` requests `kWh imp` — a `DailyProfile`-only register per the code table — under `IntervalProfile`, which the JSON Schema alone cannot catch), that the requested `mode` is one of the register's `supportedModes` (`invalid_request_mode_unsupported.json` requests `READING` mode for a register whose code-table entry only supports `USAGE`), and that any embedded `MeterDataAuthorisation`'s `validUntil` is strictly after its `validFrom` (`invalid_authorisation_expired.json` sets `validUntil` one hour *before* `validFrom`). None of these four checks are expressible in `schema.json` alone — they depend on the external code registry and on comparing two date-time fields against each other.

## 11. Points for Confirmation

1. This schema's status is Draft for technical review — the split into three composable models (MeterDataCapabilities / MeterDataAuthorisation / MeterDataRequest) is a structural break from v0.5's single flat request object and has not yet been marked stable.
2. The relationship between an inline `MeterDataAuthorisation` object and a URI reference to one (both are valid for the `authorisation` field) needs a documented convention for when each form is expected — notably, both shipped examples (`Request_Example.json`, `Anonymised_Telemetry_Request.json`) use the URI form exclusively, so the inline-object path is currently unexercised by any real example, particularly for audit and revocation checking.
3. `ValueCapability.value` accepts either a raw OBIS code or a human-readable short code, but every shipped example uses only the short-code form — worth confirming whether the OBIS form is expected to appear in production traffic or is effectively vestigial for this schema.
4. The semantic checks that actually give `ValueCapability.value` + `mode` + `profileType` their meaning — resolvability against the `MeterData` family's `IES codes.json`, profile-membership, and mode-support — live entirely in an external validator script and a sibling schema's code table, not in `schema.json` itself; worth confirming whether that dependency should be declared explicitly (e.g. as a schema reference or `x-standard` annotation) rather than left implicit in a validation script.
5. The OBIS/short-code touchpoint in `ValueCapability.value` ties this schema to IS 15959 (via the `MeterData` code table's part/table/clause citations), but that link is carried only through the external code registry, not declared as a formal standard reference on this schema itself — worth confirming whether it should be made explicit.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 15959 (Parts 1–3) | Register/OBIS code space used to name individual registers in `ValueCapability.value`; cited at the individual register level (specific Part/Table/Clause per code) in the related `MeterData` family's `IES codes.json`, referenced here only indirectly |
| IEC 62056 | International harmonisation of the OBIS code space underlying IS 15959; second in the fixed IES order of preference, not cited directly by this schema |
| W3C Verifiable Credentials Data Model 2.0 | Basis of the optional `MeterDataRequestCredential` wrapper (a separate schema family) used to carry a `MeterDataRequest` cryptographically at Beckn `confirm` time |

### Annexure B — Example Payloads

Example payloads for all three composable models are at [schemas/MeterDataRequest/v0.6/examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterDataRequest/v0.6/examples), including a general capabilities example, a billing-focused capabilities example, an MDM (meter data management) capabilities example with alarm/event profiles, an authorisation example, a full request example, and an anonymised (no-consumer) telemetry request example.

### Annexure C — JSON Schema

The JSON Schema and attribute source are at [schemas/MeterDataRequest/v0.6/schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/schema.json) and [schemas/MeterDataRequest/v0.6/attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataRequest/v0.6/attributes.yaml).
