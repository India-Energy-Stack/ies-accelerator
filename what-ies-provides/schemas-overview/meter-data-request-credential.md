# MeterDataRequestCredential v0.1

*A W3C Verifiable Credential that a data requester attaches to a Beckn request to prove it is authorised to ask for smart-meter telemetry.*

| Field | Value |
|---|---|
| Document | IES/MDRC/0.1 |
| Status | Draft for technical review -- schema version v0.1 is recorded as an initial draft; not yet confirmed stable |
| Applicability | Issued by a data requester (e.g. a DISCOM); consumed by the metering data provider (e.g. an AMISP) that receives it at Beckn `confirm` |
| This version | Covers the credential envelope and its one defined field, `credentialSubject`, wrapping a `MeterDataRequest` object, as specified in [schema.json](../../schemas/MeterDataRequestCredential/v0.1/schema.json) |

## 1. Scope and Purpose

The stakeholders are a data requester -- typically a DISCOM -- and a metering data provider -- typically an AMISP. In a Beckn data-exchange flow, the provider cannot safely hand over smart-meter telemetry to a seeker based on an unverified claim of identity and scope: it needs to know, cryptographically and without a call back to anyone, who is asking, whether they are still authorised, and exactly what they are allowed to ask for. Without this credential, the provider has no signed, revocable proof of the requester's authorisation to attach to the request itself.

This document explains the **MeterDataRequestCredential v0.1** schema. It does not define a new schema; it explains the existing one.

## 2. What It Records / Covers

The credential records:

- the **identity** of the requesting entity (the DID of the party asking for the data, such as the DISCOM);
- the **scoped data request** it is authorising -- which consumers and which meter/feeder resources the request covers, the hierarchical scope of that coverage, the time window the request applies to, the consumer consent and authorisation backing it, the capabilities being requested, and any cap on the number of records that may be shared;
- the standard verifiable-credential **envelope** it inherits rather than redefines -- who issued the credential and their licence number, when it is valid from and until, its revocation status, and its cryptographic proof.

It does not carry the telemetry itself. It only authorises a request for that telemetry.

## 3. How Each Item is Identified

The requesting entity is identified by a DID, carried both as the credential's `issuer.id` (inherited from EnergyCredential) and as `credentialSubject.id`. The issuer also carries a regulatory licence number (inherited from EnergyCredential) alongside its DID, so a provider can tie the DID back to a recognised, licensed entity. Consumers and meter/feeder resources referenced inside the embedded `MeterDataRequest` are identified as DIDs as well (`consumers`, `resources`, and optionally `consumerConsent`). This schema does not introduce its own identifier scheme -- it reuses the DID-based identifiers already defined for the entities and resources it references, and revocation status is checked against the DeDi registry referenced in `credentialStatus`.

## 4. Definitions

- **DID (Decentralised Identifier)** -- a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **Verifiable Credential (VC)** -- a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer.
- **DeDi** -- the decentralised registry infrastructure (dedi.global) used for Beckn subscriber registries and credential revocation registries; not an identifier method itself.
- **Beckn Protocol** -- the open interaction protocol IES uses for discovery, negotiation and confirmation between parties (search / select / init / confirm / status and their `on_` callbacks).
- **DISCOM** -- a distribution licensee (electricity distribution company) serving retail consumers.
- **AMISP** -- an Advanced Metering Infrastructure Service Provider, the metering agency that operates smart-meter data collection on a DISCOM's behalf.

## 5. Basis of Standards

The IES order of preference is fixed:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

MeterDataRequestCredential v0.1 does not itself define new engineering or metering standards to place against this order -- it is a credential envelope. It follows the **W3C Verifiable Credential Data Model 2.0** directly, as a subclass of the DEG-published **EnergyCredential v2.0**, from which it inherits the issuer, validity window, revocation status and proof structure rather than redefining them.

## 6. Where Indian Standards Do Not Yet Exist

No gap is currently documented for this schema. It is a credential-envelope schema built on the W3C Verifiable Credential Data Model and the DEG EnergyCredential v2.0 base; it does not carry engineering or metering data of the kind for which an Indian-versus-international standards gap would arise.

## 7. The Record(s)

MeterDataRequestCredential defines a single record: a signed, time-bounded Verifiable Credential that changes with every request it authorises -- it is not a long-lived static record like a connection credential. It is issued by the data requester (e.g. the DISCOM) at the point it wants to ask a provider (e.g. an AMISP) for telemetry, and it is presented, not re-issued, each time that same authorisation is used within its validity window.

It relates to other IES records in two ways. First, it wraps a `MeterDataRequest` object inside `credentialSubject.meterDataRequest` -- the actual scoped, time-bounded ask (consumers, resources, scope, time window, consent, authorisation, requested capabilities, and any cap on records shared). Second, it is the request-side counterpart to **MeterDataCredential**: this credential is issued by the requester and used at Beckn `confirm` time to prove the right to ask; MeterDataCredential is issued by the provider and used at Beckn `on_status` time to attest what was actually delivered.

## 8. Schedule I — Field Reference (summary)

The schema is built from these logical blocks:

- the inherited **EnergyCredential v2.0 envelope** -- issuer (id, name, licence number), validity window, credential status, and proof;
- **credentialSubject** -- the DID of the requesting entity and its one substantive field, `meterDataRequest`;
- the embedded **MeterDataRequest object** -- consumers, resources, scope, time window (`from`/`duration`), consumer consent, authorisation, requested capabilities, and the optional cap on records shared.

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [MeterDataRequestCredential v0.1 -- Field reference](../../schemas/MeterDataRequestCredential/v0.1/README.md#field-reference).

## 9. Schedule II

MeterDataRequestCredential does not stand alone. It wraps a `MeterDataRequest` payload inside its `credentialSubject`, and it is itself a subclass of the DEG-published EnergyCredential v2.0, from which it inherits its envelope rather than redefining it. There is no separate Schedule II report template for this schema.

## 10. How It Fits Together

MeterDataRequestCredential is the optional authorisation attachment on the request leg of the Beckn data-exchange flow described in [Smart Meter Data Exchange](../../use-cases/smart-meter-data-exchange/README.md). A seeker (e.g. a DISCOM) discovers a metering dataset offered by a provider (e.g. an AMISP); the provider's offer policy can require the seeker to attach a MeterDataRequestCredential at Beckn `confirm` time. The provider checks that the credential's type is MeterDataRequestCredential, that `validUntil` has not passed, that its status is not revoked, and that the embedded `MeterDataRequest.resources` fall within the scope the provider has actually agreed to serve (its own capability profile). Once the exchange completes, the provider's response at `on_status` is attested separately by **MeterDataCredential** -- so the two credentials bracket the same exchange from opposite ends: MeterDataRequestCredential proves the right to ask, MeterDataCredential attests what was delivered.

## 11. Points for Confirmation

1. The schema's own changelog records v0.1 as an initial draft; confirmation of stable status is still outstanding.
2. This credential is optional in the Smart Meter Data Exchange use case -- when a provider's offer policy requires it versus when a request may proceed without it is a per-provider policy decision that this document does not resolve.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| W3C Verifiable Credential Data Model 2.0 | The credential format MeterDataRequestCredential is expressed in |
| DEG EnergyCredential v2.0 | The base schema MeterDataRequestCredential subclasses for its envelope (issuer, validity, status, proof) |

### Annexure B — Example Payloads

A complete example instance is at [schemas/MeterDataRequestCredential/v0.1/examples](../../schemas/MeterDataRequestCredential/v0.1/examples).

### Annexure C — JSON Schema

The machine-readable definitions are at [schema.json](../../schemas/MeterDataRequestCredential/v0.1/schema.json) and [attributes.yaml](../../schemas/MeterDataRequestCredential/v0.1/attributes.yaml).
