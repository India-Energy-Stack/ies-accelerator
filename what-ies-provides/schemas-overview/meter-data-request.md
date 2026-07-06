# MeterDataRequest v0.6

*The query, capability and authorisation shapes a party uses to ask for smart-meter telemetry — not the telemetry itself.*

| Field | Value |
|---|---|
| Document | IES/MDR/0.6 |
| Status | Draft for technical review |
| Applicability | DISCOMs and AMISPs (as providers/grantors); AMISPs, TSPs and other authorised third parties (as requesters/grantees) |
| This version | Covers the three composable request-layer models — MeterDataCapabilities, MeterDataAuthorisation, MeterDataRequest — defined in [`schema.json`](../../schemas/MeterDataRequest/v0.6/schema.json) |

## 1. Scope and Purpose

The stakeholders are the party that holds smart-meter data — typically a DISCOM or the AMISP acting on its behalf — and the party that wants a defined slice of it, such as another AMISP, a TSP, or a consented third party. Today, before any data can move, the two sides have to work out three things in an ad hoc way: what the provider is even able to serve, who has actually been allowed to ask for it, and exactly what window and scope a given query covers. Without a shared shape for these three things, each integration re-invents its own capability list, its own authorisation record, and its own query format.

This document explains the **MeterDataRequest v0.6** schema. It does not define a new schema — it walks through the existing one, ahead of the auto-generated field reference in the schema's own README.

## 2. What It Records / Covers

MeterDataRequest v0.6 is not a Verifiable Credential. It is the query/authorisation payload shape used to ask a meter-data provider for telemetry, and it covers three distinct things:

- **What a provider can serve** — the profile types it supports (customer, interval, daily, monthly, bill-details, instantaneous, event, alarm), optionally down to the specific registers or readings within each profile, which query scopes it can answer, and the longest historical window it can serve. This is the provider's published data-access envelope.
- **Who has been authorised, for what, and for how long** — a grant naming the authorising entity, the authorised entity, the purpose of access, a validity period, and the specific slice of capabilities being granted.
- **The actual query being asked** — which consumers or resources it targets, whether the request covers just that resource or its children too, the start time and length of the requested window, references to consumer consent, the authorisation backing the request, the specific capability slice being asked for, and an optional cap on how many records come back.

## 3. How Each Item is Identified

The schema targets consumers and resources by URI/DID: `consumers[]` is a list of consumer URIs or DIDs, and `resources[]` is a list of resource URIs or DIDs — for example meter DIDs or service-point URIs. `MeterDataAuthorisation.grantor` and `.grantee` are likewise URIs/DIDs identifying the authorising and authorised entities. The schema does not mint a new identifier scheme of its own; it consumes whatever DID or URI already identifies the consumer, meter, service point, or organisation elsewhere in IES.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **Verifiable Credential (VC)** — a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer.
- **Beckn Protocol** — the open interaction protocol IES uses for discovery, negotiation and confirmation between parties (search / select / init / confirm / status and their `on_` callbacks).
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers.
- **AMISP** — an Advanced Metering Infrastructure Service Provider, the metering agency that operates smart-meter data collection on a DISCOM's behalf.
- **SERC/CERC** — State/Central Electricity Regulatory Commission, the tariff and licensing regulator for the power sector.
- **MeterDataCapabilities** — the provider's advertised data-access envelope: which profile types and registers it can serve, which query scopes, and the longest history window.
- **MeterDataAuthorisation** — the grant/token recording who authorised whom, for what purpose, and for how long, over a stated capability slice.
- **MeterDataRequest** — the actual query payload: target consumers/resources, scope, time window, consent references, the backing authorisation, the capability slice requested, and an optional record cap.
- **ProfileCapability** — one entry in `MeterDataCapabilities.profiles[]`, naming a profile type (e.g. `IntervalProfile`) and optionally the specific registers/readings supported under it.
- **OBIS code** — the register identifier used inside `ValueCapability.value` to name a specific meter quantity (e.g. `1.0.1.8.0.255`).

## 5. Basis of Standards

The IES order of preference is fixed. Where more than one standard could apply, use, in order:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

MeterDataRequest v0.6 itself is a request/authorisation envelope, not a metering data-model schema, so it carries no `x-standard` field annotations of its own. Its one point of contact with a standard is indirect: `ValueCapability.value` names the register being requested or offered using an OBIS code — the same code space used by the MeterData payload schema, which follows IS 15959 / IEC 62056 directly.

## 6. Where Indian Standards Do Not Yet Exist

No gap is currently documented for this schema. The request/capability/authorisation shapes (which profiles a provider serves, who is authorised, what window a query covers) are an IES-specific query envelope; they do not correspond to a metering data-model area where an Indian standard would otherwise be expected.

## 7. The Record(s)

MeterDataRequest v0.6 defines three related, composable records, all carried as plain JSON payloads rather than credentials:

- **MeterDataCapabilities** — a relatively static record. It is published by a provider (a DISCOM or AMISP) describing what it can serve, and it changes only when the provider's supported profiles, registers, scopes, or history window change. In practice it is advertised as a Beckn catalog entry, so a requester can discover it before asking for anything.
- **MeterDataAuthorisation** — a grant record with a defined validity window (`validFrom`/`validUntil`). It is issued by the grantor (e.g. the DISCOM) to a grantee (e.g. a TSP) for a stated purpose, and it names a specific `MeterDataCapabilities` subset the grantee is allowed to draw on. It changes whenever access is newly granted, narrowed, or expires.
- **MeterDataRequest** — the per-query record, issued by the authorised requester each time it wants telemetry. It carries its own capability slice (`capabilitiesRequested`), references or embeds the backing `MeterDataAuthorisation`, and states the specific window, scope and targets for that one query. It is the most frequently created of the three.

These three records relate to each other by direct composition — a `MeterDataRequest` embeds or references a `MeterDataAuthorisation`, which in turn names a `MeterDataCapabilities` subset — and they relate to the wider IES schema set as the request leg that is answered by a separate MeterData response payload.

## 8. Schedule I — Field Reference (summary)

MeterDataRequest v0.6 is built from four logical blocks:

- **MeterDataCapabilities** — a provider's advertised profiles, supported scopes, and maximum history window.
- **MeterDataAuthorisation** — the grantor, grantee, purpose, validity period, and granted capability slice.
- **MeterDataRequest** — the query itself: targets, scope, time window, consent references, authorisation, requested capability slice, and record cap.
- **ProfileCapability / ValueCapability** — the nested detail inside a capabilities block, naming individual profile types and, where needed, the specific registers (by OBIS or short code) and telemetry mode within them.

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [MeterDataRequest v0.6 — Field reference](../../schemas/MeterDataRequest/v0.6/README.md#field-reference).

## 9. Schedule II

Not applicable as a stand-alone dependency in this direction, but MeterDataRequest is itself depended on. MeterDataRequest v0.6 is a plain payload schema — it does not wrap or depend on another schema. It can, however, optionally be wrapped: a `MeterDataRequest` payload may be carried inside a `MeterDataRequestCredential`, a Verifiable Credential used to prove the requester's authorisation at Beckn `confirm` time. That wrapping is the other schema's concern, not this one's.

## 10. How It Fits Together

MeterDataRequest v0.6 is the request/query leg of the Smart Meter Data Exchange use case (see [use-cases/smart-meter-data-exchange/README.md](../../use-cases/smart-meter-data-exchange/README.md)). A provider (DISCOM or AMISP) advertises a `MeterDataCapabilities` catalog entry over Beckn; a requester obtains a `MeterDataAuthorisation` naming the capability slice it may draw on; it then issues a `MeterDataRequest` naming its target consumers or resources, the window it wants, and the capability slice it is asking for. That request is answered by a separate MeterData response payload carrying the actual readings. Where the requester needs to prove its authorisation cryptographically at Beckn `confirm` time rather than relying on the plain JSON alone, the `MeterDataRequest` is wrapped in a `MeterDataRequestCredential`.

## 11. Points for Confirmation

1. This schema's status is Draft for technical review — the split into three composable models (MeterDataCapabilities / MeterDataAuthorisation / MeterDataRequest) is new in v0.6 and has not yet been marked stable.
2. The relationship between an inline `MeterDataAuthorisation` object and a URI reference to one (both are valid for the `authorisation` field) needs a documented convention for when each form is expected, particularly for audit and revocation checking.
3. The OBIS-code touchpoint in `ValueCapability.value` ties this schema to the MeterData payload schema's IS 15959 / IEC 62056 basis, but that link is implicit rather than declared as a formal standard reference on this schema — worth confirming whether it should be made explicit.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 15959 / IEC 62056 | OBIS code space used to name individual registers in `ValueCapability.value` (standard basis of the related MeterData payload schema, referenced here only indirectly) |

### Annexure B — Example Payloads

Example payloads for all three composable models are at [schemas/MeterDataRequest/v0.6/examples/](../../schemas/MeterDataRequest/v0.6/examples/).

### Annexure C — JSON Schema

The JSON Schema and attribute source are at [schemas/MeterDataRequest/v0.6/schema.json](../../schemas/MeterDataRequest/v0.6/schema.json) and [schemas/MeterDataRequest/v0.6/attributes.yaml](../../schemas/MeterDataRequest/v0.6/attributes.yaml).
