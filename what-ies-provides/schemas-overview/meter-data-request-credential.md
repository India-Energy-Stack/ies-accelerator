# MeterDataRequestCredential v0.1

*A W3C Verifiable Credential that a data requester attaches to a Beckn request to prove it is authorised to ask for smart-meter telemetry.*

| Field | Value |
|---|---|
| Document | IES/MDRC/0.1 |
| Status | Draft for technical review -- the schema's own changelog records v0.1, dated 2026-05-26, as "Initial draft"; stable status has not yet been confirmed |
| Applicability | Issued by a data requester (e.g. a DISCOM, or a third-party aggregator such as a Technical Service Provider) that attaches it in `commitmentAttributes.ies:meterDataRequest` at Beckn `confirm`; consumed by the metering data provider (e.g. an AMISP or MDM system) that receives it |
| This version | Defines the credential envelope and its one substantive field, `credentialSubject`, whose `meterDataRequest` property wraps a `MeterDataRequest` object from the separate **MeterDataRequest v0.6** schema family, as specified in [attributes.yaml](../../schemas/MeterDataRequestCredential/v0.1/attributes.yaml) |

## 1. Scope and Purpose

The stakeholders are a data requester -- typically a DISCOM, though `attributes.yaml` explicitly also names a "third-party aggregator" as a possible requester -- and a metering data provider -- typically an AMISP or an MDM (Meter Data Management) system. In a Beckn data-exchange flow, the provider cannot safely hand over smart-meter telemetry to a seeker based on an unverified claim of identity and scope: it needs to know, cryptographically and without a call back to anyone, who is asking, whether they are still authorised, and exactly what they are allowed to ask for.

The schema's own description states the purpose precisely: the credential "binds the requester's identity to a scoped, time-bounded query expressed as a MeterDataRequest." It exists specifically to satisfy a provider policy that requires "a credential-backed, verifiable request before fulfilling data delivery" -- meaning attaching it is not universal practice but something a specific provider's offer can mandate.

This document explains the **MeterDataRequestCredential v0.1** schema. It does not define a new schema; it explains the existing one.

## 2. What It Records / Covers

The credential records:

- the **identity** of the requesting entity -- a DID at both `issuer.id` and `credentialSubject.id` -- plus, inherited from EnergyCredential, the issuer's human-readable `name` and a regulatory `licenseNumber` (the worked example uses `KERC-DISCOM-2025-001`, a Karnataka Electricity Regulatory Commission licence format);
- the **scoped data request** it is authorising, expressed as an embedded `MeterDataRequest` object (from the separate MeterDataRequest v0.6 family) rather than redefined inline. That embedded object can carry: which `consumers` and which `resources` (meter or feeder DIDs) the request covers; a hierarchical `scope` over those resources; the `from`/`duration` time window; `consumerConsent` references; an `authorisation` (inline `MeterDataAuthorisation` object or a URI to one); the `capabilitiesRequested` (which profile types and registers are being asked for, and in what telemetry mode); and an optional `maxRecordsShared` cap;
- the standard verifiable-credential **envelope** it inherits from EnergyCredential v2.0 rather than redefining -- `issuer`, `validFrom`/`validUntil`, `credentialStatus`, and `proof`.

It does not carry the telemetry itself. It only authorises a request for that telemetry.

The worked example in `examples/example.json` grounds this concretely: BESCOM (Bangalore Electricity Supply Company, `did:web:bescom.karnataka.gov.in`, licence `KERC-DISCOM-2025-001`) issues a credential valid for the single month `2026-04-01` to `2026-04-30`, whose embedded `MeterDataRequest` asks -- for feeder `did:dedi:ies:feeder:IN-KA-BLR-ZONE-A` and everything under it (`scope: ResourceAndChildren`) over a three-month window (`from: 2026-01-01`, `duration: P3M`) -- for four profile types at once: `CustomerProfile` (no reading restriction, i.e. all registers), `IntervalProfile` restricted to `kWh imp block` in `USAGE` mode, `DailyProfile` restricted to `kWh imp` in `READING` mode, and `MonthlyProfile` restricted to `kWh imp` in `USAGE` mode -- capped at `maxRecordsShared: 10000`. This shows the credential's core discipline in miniature: a short, hard-expiring validity window (30 days) authorising a much longer historical query (three months of data), scoped down to named registers and explicit reading modes rather than "give me everything."

## 3. How Each Item is Identified

The requesting entity is identified by a DID, carried both as the credential's `issuer.id` (inherited from EnergyCredential) and as `credentialSubject.id`; `attributes.yaml` marks `credentialSubject.id` with `format: uri` and an explicit description, "DID of the requesting entity (e.g., the DISCOM)." The issuer also carries a `licenseNumber` (inherited from EnergyCredential) alongside its DID, so a provider can tie the DID back to a recognised, licensed entity -- in the example, a KERC DISCOM licence number.

Consumers and meter/feeder resources referenced inside the embedded `MeterDataRequest` are identified as DIDs too: `consumers` and `resources` are both typed `array` of `string, format: uri` in the MeterDataRequest v0.6 `attributes.yaml`, and the example instantiates `resources` with a feeder DID (`did:dedi:ies:feeder:IN-KA-BLR-ZONE-A`) rather than an individual meter DID, relying on `scope: ResourceAndChildren` to sweep in every meter under that feeder. `consumerConsent` is typed as an array of plain strings (not `format: uri`), so it is meant to carry consent references or receipt identifiers rather than necessarily being a DID.

This schema does not introduce its own identifier scheme -- it reuses the DID-based identifiers already defined for the entities and resources it references. Revocation status is checked against a DeDi registry referenced in `credentialStatus`; the example's `credentialStatus.type` is `dediregistry` and both `id` and `statusListCredential` point at `https://dedi.global/dedi/query/...` and `https://dedi.global/dedi/lookup/...` endpoints scoped to the issuer's own DID (`did:web:bescom.karnataka.gov.in/vc-revocation-registry`), meaning each issuer maintains its own revocation list rather than a shared central one.

## 4. Definitions

- **DID (Decentralised Identifier)** -- a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **Verifiable Credential (VC)** -- a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer.
- **DeDi** -- the decentralised registry infrastructure (dedi.global) used for Beckn subscriber registries and credential revocation registries; not an identifier method itself. Each issuer's revocation registry is addressed by its own DID (e.g. `.../did:web:bescom.karnataka.gov.in/vc-revocation-registry`).
- **Beckn Protocol** -- the open interaction protocol IES uses for discovery, negotiation and confirmation between parties (search / select / init / confirm / status and their `on_` callbacks).
- **DISCOM** -- a distribution licensee (electricity distribution company) serving retail consumers.
- **AMISP** -- an Advanced Metering Infrastructure Service Provider, the metering agency that operates smart-meter data collection on a DISCOM's behalf.
- **MDM** -- a Meter Data Management system; `attributes.yaml` names it alongside AMISP as an example data provider.
- **TSP (Technical Service Provider)** -- a third-party aggregator that can also act as a requester under this credential per the schema's own description ("e.g., DISCOM, third-party aggregator"); the sibling MeterDataRequest schema's own worked `Authorisation_Example.json` shows a DISCOM (`did:dedi:ies:discom:BESCOM`) as grantor authorising a TSP (`did:dedi:ies:tsp:ACME-TSP`) as grantee, for the stated purpose "ESG Carbon Accounting & Trend Analysis" -- illustrating the kind of downstream delegation this credential's `authorisation` field is built to carry.
- **OBIS code** -- an IEC-standard register-naming scheme (see Section 5) used inside the embedded `MeterDataRequest.capabilitiesRequested` to name specific meter registers, e.g. `1.0.1.8.0.255` for cumulative imported active energy; the schema also accepts a "short code" alias such as `kWh imp` for the same register.
- **Scope (`ResourceOnly` / `ResourceAndChildren` / `ChildrenOnly`)** -- the three-value enum (`ScopeType` in MeterDataRequest v0.6) controlling whether a request against a hierarchy node (e.g. a feeder or DISCOM) covers only that node, that node and everything beneath it, or only the children and not the node itself.
- **Telemetry mode (`READING` / `USAGE`)** -- the two-value enum (`TelemetryMode` in MeterDataRequest v0.6) distinguishing a raw register reading (a cumulative meter dial value) from a derived usage/consumption figure (a difference between two readings over an interval).

## 5. Basis of Standards

The IES order of preference is fixed:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

MeterDataRequestCredential v0.1 does not itself define new engineering or metering standards to place against this order -- it is a credential envelope. It follows the **W3C Verifiable Credential Data Model 2.0** directly, as a subclass of the DEG-published **EnergyCredential v2.0** (`https://schema.beckn.io/EnergyCredential/v2.0`, expressed in `attributes.yaml` as `allOf: - $ref: https://schema.beckn.io/EnergyCredential/v2.0`), from which it inherits the issuer, validity window, revocation status and proof structure rather than redefining them. The schema's own README notes this is the same inheritance pattern used by sibling DEG energy credentials `ConsumptionProfileCredential` and `GenerationProfileCredential`, so MeterDataRequestCredential is one instance of a general IES/DEG convention rather than a one-off design.

The engineering substance this credential authorises access to -- registers, profile types, telemetry modes -- lives in the wrapped **MeterDataRequest v0.6** schema, and it is there that IEC alignment becomes concrete: `ValueCapability.value` is described as "The OBIS code (e.g. 1.0.1.8.0.255) or short code (e.g. kWh imp) representing the register," which is the object-identification system standardised in **IEC 62056** (Companion Specification for Energy Metering / DLMS-COSEM). The `MeterDataRequest` validator (`schemas/MeterDataRequest/v0.6/validation/validator.py`) enforces this at runtime: it resolves every requested register string (OBIS or short code) against a project-maintained `IES codes.json` lookup (held in the sibling `schemas/MeterData/v0.6/` directory, not duplicated here), checks that a register requested under a given `profileType` is actually permitted for that profile group (its worked test case: `kWh imp` must not be requested under `IntervalProfile`), and checks that the requested `TelemetryMode` (`READING`/`USAGE`) is among the modes the register supports. The reason that particular combination is invalid is visible in `IES codes.json` itself: `kWh imp` is defined there with `accumulationBehaviour: CUMULATIVE` (a running meter-dial total, category `energyCumulative`), whereas `IntervalProfile` expects a per-interval figure -- which is what the sibling register `kWh imp block` provides, defined with `accumulationBehaviour: DELTA` (category `energyIncremental`). So the profile-type restriction is not arbitrary; it follows from whether the register is a cumulative reading or an incremental delta. None of this validation logic lives inside MeterDataRequestCredential itself -- it is inherited by reference, since the credential only wraps the `MeterDataRequest` object rather than re-specifying its rules.

No IS or CEA/IEGC citation appears anywhere in this schema family's `attributes.yaml`, vocab.jsonld, or README files -- the credential envelope is pure W3C/DEG, and the wrapped request payload's only cited standard is the IEC OBIS/DLMS-COSEM register scheme.

## 6. Where Indian Standards Do Not Yet Exist

No gap is currently documented for the credential envelope itself: it is built on the W3C Verifiable Credential Data Model and the DEG EnergyCredential v2.0 base, neither of which has an Indian-standard counterpart to compare against because they are protocol/format concerns, not engineering ones.

The wrapped **MeterDataRequest v0.6** payload is where a gap is more visible on inspection, even though the schema's own files do not name it as an open item: its `ProfileCapability.profileType` enum (`CustomerProfile`, `IntervalProfile`, `DailyProfile`, `MonthlyProfile`, `BillDetails`, `InstantaneousProfile`, `EventProfile`, `AlarmProfile`) and its register-naming convention (OBIS codes per IEC 62056) are drawn entirely from the international DLMS-COSEM metering data model. No IS standard is cited for these profile classes or register codes in the schema source; Indian metering practice (e.g. CEA's Smart Meter functional/communication requirements) is referenced elsewhere in the IES documentation set for meter-side data, but this credential-and-request pairing does not itself point to an IS equivalent for the specific profile/register taxonomy it uses.

## 7. The Record(s)

MeterDataRequestCredential defines a single record: a signed, time-bounded Verifiable Credential that changes with every request it authorises -- it is not a long-lived static record like a connection credential. It is issued by the data requester (e.g. the DISCOM) at the point it wants to ask a provider (e.g. an AMISP or MDM system) for telemetry, and it is presented, not re-issued, each time that same authorisation is used within its validity window. The worked example shows a deliberately short window -- 30 days (`2026-04-01` to `2026-04-30`) -- authorising a request against a substantially longer historical span (three months back to `2026-01-01`), which illustrates that the credential's *validity* period and the *data window* it requests are two independent time ranges that must both be checked.

It relates to other IES records in two ways:

1. **It wraps** a `MeterDataRequest` object inside `credentialSubject.meterDataRequest` -- the actual scoped, time-bounded ask. That object is itself one of three composable models the MeterDataRequest v0.6 schema defines (its root schema is a `oneOf` over `MeterDataRequestObject`, `MeterDataAuthorisation`, and `MeterDataCapabilities`): the request specifies `consumers`/`resources`/`scope`/`from`/`duration`/`consumerConsent`/`authorisation`/`capabilitiesRequested`/`maxRecordsShared`; the `authorisation` field can itself be an inline `MeterDataAuthorisation` object (grantor, grantee, purpose, validity window, granted capabilities) or a URI reference to one, giving MeterDataRequestCredential an optional second, nested layer of delegation evidence beyond its own VC proof.
2. **It is the request-side counterpart to MeterDataCredential.** The MeterDataCredential v0.6 README states this relationship explicitly in its own comparison table: MeterDataRequestCredential is issued by the requester and wraps a `MeterDataRequest`, used at Beckn `confirm` to prove the right to ask, with the requesting entity as its subject; MeterDataCredential is issued by the provider and wraps a `MeterData` payload, used at Beckn `on_status` to attest what was delivered, with the consumer/asset as its subject. The two credentials bracket the same exchange from opposite ends.

## 8. Schedule I — Field Reference (summary)

The schema is built from these logical blocks:

- the inherited **EnergyCredential v2.0 envelope** -- `issuer` (`id`, `name`, `licenseNumber`), `validFrom`/`validUntil`, `credentialStatus` (DeDi registry reference), and `proof` (the worked example uses `Ed25519Signature2020`);
- **credentialSubject** (`MeterDataRequestCredentialSubject`) -- the DID of the requesting entity (`id`) and its one required, substantive field, `meterDataRequest`;
- the embedded **MeterDataRequest object** (defined in the separate MeterDataRequest v0.6 family, required fields `from`, `duration`, `capabilitiesRequested`) -- `consumers`, `resources`, `scope`, `from`/`duration`, `consumerConsent`, `authorisation`, `capabilitiesRequested` (itself built from `MeterDataCapabilities` → `ProfileCapability` → `ValueCapability`, down to individual OBIS/short-code registers and telemetry modes), and the optional `maxRecordsShared` cap.

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) for this credential is at [MeterDataRequestCredential v0.1 -- Field reference](../../schemas/MeterDataRequestCredential/v0.1/README.md#field-reference); the fields of the object it wraps are documented at [MeterDataRequest v0.6 -- Field reference](../../schemas/MeterDataRequest/v0.6/README.md#field-reference).

## 9. Schedule II

MeterDataRequestCredential does not stand alone in either direction. It **wraps** a `MeterDataRequest` payload inside its `credentialSubject`, and it is itself **wrapped by** (a subclass of) the DEG-published EnergyCredential v2.0, from which it inherits its envelope rather than redefining it. There is no separate Schedule II report template for this schema.

## 10. How It Fits Together

MeterDataRequestCredential is the optional authorisation attachment on the request leg of the Beckn data-exchange flow described in [Smart Meter Data Exchange](../../use-cases/smart-meter-data-exchange/README.md). Concretely, per the schema's own README:

- **Provider side, `catalog/publish`**: the provider advertises `ies:dataSchema` (a URL to the MeterData schema used for response payloads), `ies:capabilityProfile` (a `MeterDataRequest`-shaped object describing the maximum scope the provider can serve -- its own data-access envelope), and `offerAttributes.policy.requiredCredentials` declaring that a valid `MeterDataRequestCredential` must be attached at `confirm`.
- **Seeker side, `confirm`**: the seeker includes the signed credential in `commitmentAttributes.ies:meterDataRequest`. The embedded `MeterDataRequest` must be a subset of the provider's advertised `capabilityProfile` -- e.g. a seeker cannot request `EventProfile` registers if the provider's capability profile never listed `EventProfile` among its `profiles`.
- **Provider verification**: the provider checks that the credential's type is `MeterDataRequestCredential`, that `validUntil` has not passed, that its status is not revoked (via the DeDi registry named in `credentialStatus`), and that the embedded `MeterDataRequest.resources` and requested registers fall within the scope and register set the provider has actually agreed to serve.
- **Provider side, `on_status`**: the response is attested separately by **MeterDataCredential**, whose embedded `meterData` payload must cover the profile types and time window originally requested. So the two credentials bracket the same exchange from opposite ends: MeterDataRequestCredential proves the right to ask, MeterDataCredential attests what was delivered.

## 11. Points for Confirmation

1. The schema's own changelog records v0.1 (2026-05-26) as an initial draft; confirmation of stable status is still outstanding.
2. This credential is optional in the Smart Meter Data Exchange use case -- when a provider's offer policy requires it versus when a request may proceed without it is a per-provider policy decision that this document does not resolve.
3. The `consumerConsent` field is typed as a plain string array (not `format: uri`), unlike `consumers` and `resources` which are DIDs -- the schema does not specify whether consent entries must be DIDs, opaque receipt hashes, or some other format, leaving consent-evidence interoperability between DISCOMs and TSPs undefined at the schema level.
4. `authorisation` may be an inline `MeterDataAuthorisation` object or a bare URI reference to one; the schema does not specify how a provider is expected to dereference and independently verify a URI-referenced authorisation (e.g. whether it must itself be signed, or how staleness/revocation of that referenced grant is checked), which matters once a TSP-style delegation chain (DISCOM → TSP) is involved rather than a direct DISCOM-to-provider request.
5. Register-level validation (OBIS/short-code resolution, profile-type restriction, telemetry-mode compatibility) is enforced entirely by the separate `MeterDataRequest v0.6` validator against an `IES codes.json` lookup that lives outside this credential's own files -- so a reader of MeterDataRequestCredential alone cannot see which specific registers or profile-mode combinations are actually valid without also consulting the MeterDataRequest v0.6 validation tooling.
6. No IS or CEA/IEGC standard is cited anywhere in this schema family for the profile-type taxonomy or register-naming scheme it relies on (both are IEC/DLMS-COSEM-derived); whether an Indian-specific smart-meter data standard should eventually take precedence per the IES order of preference is not addressed in the source.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| W3C Verifiable Credential Data Model 2.0 | The credential format MeterDataRequestCredential is expressed in |
| DEG EnergyCredential v2.0 | The base schema MeterDataRequestCredential subclasses for its envelope (issuer, validity, status, proof) |
| IEC 62056 (DLMS-COSEM object identification / OBIS codes) | The register-naming scheme used by the wrapped MeterDataRequest's `ValueCapability.value` field (e.g. `1.0.1.8.0.255`) |

### Annexure B — Example Payloads

A complete example instance is at [schemas/MeterDataRequestCredential/v0.1/examples](../../schemas/MeterDataRequestCredential/v0.1/examples) (BESCOM requesting Q1 2026 customer, interval, daily and monthly profiles for all meters under feeder `IN-KA-BLR-ZONE-A`). The wrapped `MeterDataRequest` object's own worked examples -- covering a plain request, an inline authorisation grant, and provider capability declarations -- are at [schemas/MeterDataRequest/v0.6/examples](../../schemas/MeterDataRequest/v0.6/examples).

### Annexure C — JSON Schema

The machine-readable definitions are at [schema.json](../../schemas/MeterDataRequestCredential/v0.1/schema.json) and [attributes.yaml](../../schemas/MeterDataRequestCredential/v0.1/attributes.yaml). The wrapped object's own definitions are at [MeterDataRequest v0.6 schema.json](../../schemas/MeterDataRequest/v0.6/schema.json) and [attributes.yaml](../../schemas/MeterDataRequest/v0.6/attributes.yaml).
