# MeterDataCredential v0.6

*A signed, tamper-evident wrapper that attests who delivered a set of smart-meter readings, and that the readings have not been altered since.*

| Field | Value |
|---|---|
| Document | IES/MDC/0.6 |
| Status | Draft for technical review — initial version, aligned with MeterData v0.6 |
| Applicability | Issued by data providers (AMISPs, MDM systems, or a DISCOM acting in that role); consumed by DISCOMs, consumers' wallets, and any downstream verifier of delivered telemetry |
| This version | Wraps a `MeterData v0.6` payload (single profile or array of profiles) inside a W3C Verifiable Credential envelope, defined in [`schema.json`](../../schemas/MeterDataCredential/v0.6/schema.json) |

---

## 1. Scope and Purpose

The stakeholders are the parties on either side of a smart-meter data exchange: a provider — an AMISP or MDM system (or a DISCOM performing that role) — that has telemetry to deliver, and a receiver — a DISCOM, a consumer's wallet, or any other downstream system — that needs to trust it. Once meter readings leave the metering system and travel over a network as a message payload, the receiver has no inherent way to know who actually produced the data, whether it arrived unaltered, or whether the provider has since withdrawn it (for example after a meter fault or a privacy request). Without a mechanism for this, every data exchange has to fall back on trusting the channel itself, which does not scale across many providers and receivers.

This document explains the **MeterDataCredential v0.6** schema — it does not define a new schema; it describes the existing one, which wraps a MeterData v0.6 payload in a verifiable envelope so its authenticity and provenance can be checked independently of the channel it travelled over.

## 2. What It Records / Covers

MeterDataCredential does not itself record meter readings. It records:

- **identity of the issuing provider** — who is attesting to this data, with a licence reference where applicable;
- **identity of the subject** — the consumer or asset entity the data is about;
- **the validity window** — from when, and until when, this attestation can be relied on;
- **revocation status** — a pointer to a registry where the provider can mark the credential invalid if the data is later recalled;
- **the attested payload itself** — the actual MeterData v0.6 profile or set of profiles (customer details, interval readings, daily or monthly readings, billing details, instantaneous snapshots, events, alarms, or payload descriptors), carried inside the credential rather than described by it;
- **a cryptographic proof** — binding all of the above together so any change to the payload invalidates the signature.

It covers identity, provenance, validity and tamper-evidence of delivered telemetry. It does not cover the meaning of the readings themselves — that is the concern of the MeterData schema it wraps.

## 3. How Each Item is Identified

The credential's `issuer` is identified by a DID (Decentralised Identifier) — the provider's verifiable digital identifier, resolvable to confirm the issuer and detect tampering. The `credentialSubject.id` is a DID naming the consumer or asset entity the delivered data is about. Revocation status is tracked through a DeDi-hosted revocation registry referenced in `credentialStatus`, rather than through any bespoke IES revocation mechanism.

The credential does not mint new identifiers for meters, service points, or readings — those are carried inside the wrapped MeterData payload using whatever identifier scheme that schema defines. MeterDataCredential's own identification responsibility is limited to naming the issuer and the subject of the attestation.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **Verifiable Credential (VC)** — a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer.
- **DeDi** — the decentralised registry infrastructure (dedi.global) used for Beckn subscriber registries and credential revocation registries; not an identifier method itself.
- **Beckn Protocol** — the open interaction protocol IES uses for discovery, negotiation and confirmation between parties (search / select / init / confirm / status and their `on_` callbacks).
- **AMISP** — an Advanced Metering Infrastructure Service Provider, the metering agency that operates smart-meter data collection on a DISCOM's behalf.
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers.
- **IES Cell** — the governance body being constituted under the Central Electricity Authority (CEA) with representation from across the sector; owns the schema specifications and their versioning.

## 5. Basis of Standards

The IES order of preference is fixed, always the same:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

MeterDataCredential itself is a subclass of the DEG-published **EnergyCredential v2.0** specification and follows the **W3C Verifiable Credential Data Model 2.0** for its envelope (issuer, validity period, credential status, proof) and **W3C DID Core** for identifying issuer and subject. It inherits this envelope rather than redefining it, so the credential-level standard is the W3C VC framework; any Indian- or IEC-standard references for the metering data itself belong to the wrapped MeterData v0.6 schema, not to this wrapper.

## 6. Where Indian Standards Do Not Yet Exist

No Indian standard governs the verifiable-credential envelope, so the W3C VC Data Model 2.0 and W3C DID Core are used directly for issuer identity, signing, validity and revocation. This is the only gap documented for this schema; the standards applicable to the metering content itself are addressed in the MeterData v0.6 schema, not here.

## 7. The Record(s)

MeterDataCredential defines one record: a Verifiable Credential instance that is issued each time a provider delivers a batch of meter data. It is not a static, long-lived record like a connection or asset credential — a new instance is issued for each delivery, with a validity window scoped to that delivery, and it is superseded rather than amended when fresh data is needed.

It is issued by the provider — an AMISP, an MDM system, or a DISCOM performing that role — as the response to a confirmed request. Its counterpart on the request side is **MeterDataRequestCredential**: MeterDataRequestCredential is issued by the requester (typically the DISCOM) to prove authorisation to ask for the data, and is used at `confirm` time in the Beckn exchange; MeterDataCredential is issued by the provider to attest what was actually delivered, and is used at `on_status` time. Downstream, MeterDataCredential can be re-issued holder-bound to a consumer's own wallet, so the consumer can hold and re-present their verified meter history without going back to the DISCOM each time.

## 8. Schedule I — Field Reference (summary)

MeterDataCredential is built from two logical blocks:

- the **credential envelope** — inherited from EnergyCredential v2.0: `issuer` (id, name, licence number), `validFrom`/`validUntil`, `credentialStatus`, and `proof`;
- **`credentialSubject`** — defined by this schema: the subject `id` (DID of the consumer or asset entity) and `meterData`, the attested MeterData v0.6 payload (a single profile object or an array of profile objects).

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [MeterDataCredential v0.6 — Field reference](../../schemas/MeterDataCredential/v0.6/README.md#field-reference).

## 9. Schedule II

MeterDataCredential is not stand-alone. It wraps a MeterData v0.6 payload inside `credentialSubject.meterData`: the credential provides the verifiable envelope (identity, validity, proof, revocation), and the MeterData schema provides the substance (customer, interval, daily, monthly, billing, instantaneous, event, alarm, or descriptor profiles). Validating a MeterDataCredential instance requires checking both — the credential envelope and the embedded MeterData payload against its own schema.

## 10. How It Fits Together

In a Beckn data-exchange flow, a receiver first sends a confirmed request carrying a **MeterDataRequestCredential** to prove it is authorised to ask for specific meter data. The provider (an AMISP, MDM system, or DISCOM) then responds at `on_status` with the requested telemetry wrapped in a **MeterDataCredential**, binding the data to its own identity, a validity window, and a revocation path through the DeDi registry. The receiving party checks that the credential type is `MeterDataCredential`, that `validUntil` has not passed, that the credential has not been revoked, and that the embedded `meterData` profiles fall within the scope originally contracted in the MeterDataRequest. In the **Consumer Meter Digest** use case, this same schema is re-issued holder-bound to the consumer's own wallet DID, letting the consumer re-present their verified meter history to a third party (a bank, marketplace, or installer) without the DISCOM being asked again. More generally, it is the provenance-attestation layer for any Smart Meter Data Exchange flow where the receiver needs proof of where delivered telemetry came from.

## 11. Points for Confirmation

1. This schema is at **draft** maturity (v0.6, initial draft aligned with MeterData v0.6) and has not yet completed technical review.
2. The revocation flow in practice — how quickly a provider is expected to revoke a MeterDataCredential after a meter fault or privacy request, and how downstream holders (including consumer wallets in the Consumer Meter Digest use case) are notified — is not detailed in the facts available for this page.
3. Provenance scope-checking (that embedded `meterData` profiles fall within what was originally requested) is described as a receiver-side responsibility; how strictly this is enforced, and by whom, is not yet specified.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| W3C VC Data Model 2.0 | Verifiable Credential envelope — issuer, validity, credential status, proof |
| W3C DID Core | Decentralised identifiers for issuer and credential subject |

### Annexure B — Example Payloads

Example credential instances (a customer-profile attestation, an interval-profile attestation, and a monthly-profile attestation) are in [schemas/MeterDataCredential/v0.6/examples](../../schemas/MeterDataCredential/v0.6/examples).

### Annexure C — JSON Schema

The authoritative machine-readable definitions are [schema.json](../../schemas/MeterDataCredential/v0.6/schema.json) and [attributes.yaml](../../schemas/MeterDataCredential/v0.6/attributes.yaml).
