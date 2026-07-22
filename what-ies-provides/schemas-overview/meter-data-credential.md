# MeterDataCredential v0.6

*A signed, tamper-evident wrapper that attests who delivered a set of smart-meter readings, and that the readings have not been altered since.*

| Field | Value |
|---|---|
| Document | IES/MDC/0.6 |
| Status | Draft for technical review — initial version (dated 2026-06-06 per the schema changelog), aligned with MeterData v0.6 |
| Applicability | Issued by data providers (AMISPs, MDM systems, or a DISCOM acting in that role); consumed by DISCOMs, consumers' wallets, and any downstream verifier of delivered telemetry |
| This version | Wraps a `MeterData v0.6` payload (single profile or array of profiles) inside a W3C Verifiable Credential envelope, defined in [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/schema.json) |

---

## 1. Scope and Purpose

The stakeholders are the parties on either side of a smart-meter data exchange: a provider — an AMISP or MDM system (or a DISCOM performing that role) — that has telemetry to deliver, and a receiver — a DISCOM, a consumer's wallet, or any other downstream system — that needs to trust it. Once meter readings leave the metering system and travel over a network as a message payload, the receiver has no inherent way to know who actually produced the data, whether it arrived unaltered, or whether the provider has since withdrawn it (for example after a meter fault or a privacy request). Without a mechanism for this, every data exchange has to fall back on trusting the channel itself, which does not scale across many providers and receivers.

This document explains the **MeterDataCredential v0.6** schema — it does not define a new schema; it describes the existing one, which wraps a MeterData v0.6 payload in a verifiable envelope so its authenticity and provenance can be checked independently of the channel it travelled over. The schema's own description (in `attributes.yaml`) is explicit that it is used specifically in Beckn **`on_status`** flows: the provider attaches the credential in `dataPayload`, "cryptographically binding the delivered meter data to the provider's identity and the originating `MeterDataRequest`."

## 2. What It Records / Covers

MeterDataCredential does not itself record meter readings. Structurally it is thin by design — the entire schema-specific surface is one object, `MeterDataCredentialSubject`, with exactly two properties (`id` and `meterData`); everything else is inherited from EnergyCredential v2.0. What it records:

| Records | Detail | Source |
|---|---|---|
| Issuing provider identity | The `issuer` block (id, name, `licenseNumber`, e.g. `SERC-AMISP-2025-007`), inherited wholesale from EnergyCredential | `EnergyCredential/v2.0` |
| Subject identity | `credentialSubject.id`, a DID naming the consumer or asset entity the data is about (e.g. `did:web:discom.example:consumers:RR-1234`) | `EnergyCredential/v2.0` |
| Validity window | `validFrom` / `validUntil`, inherited from EnergyCredential (worked examples use a one-year window) | `EnergyCredential/v2.0` |
| Revocation status | `credentialStatus`, a pointer to a registry where the provider can mark the credential invalid if the data is later recalled | `EnergyCredential/v2.0` |
| Attested payload | `credentialSubject.meterData` — the one field the subject object `require`s — carrying the real MeterData v0.6 profile or set of profiles | MeterData v0.6 |
| Cryptographic proof | `proof`, binding all of the above together so any change to the payload invalidates the signature | W3C VC Data Model |

A short illustrative snippet from the customer-profile example makes the wrapping concrete — this is the whole schema-specific contribution, everything above and below it is inherited envelope:

```json
"credentialSubject": {
  "id": "did:web:discom.example:consumers:RR-1234",
  "meterData": {
    "@type": "CustomerProfile",
    "profileType": "CUSTOMER",
    "customer": { "name": "Acme Industries Pvt Ltd", "consumerCategory": "NDS", "sanctionedLoadKw": 15.0 },
    "meters": [ { "meterType": "AMI", "meterCategory": "B", "serviceKind": "ELECTRICITY" } ]
  }
}
```

`meterData` accepts either a single profile object or — as in the interval-profile example — an array that opens with a `PayloadDescriptorProfile` (the dictionary defining `readingType`, `unit`, `flowDirection`, `obis` code and column layout for the dense numeric payload that follows) and then one or more data profiles that reference it via `payloadDescriptorSetRef`/`compactSequenceRef`. MeterData v0.6 itself defines **nine** discriminated profile shapes reachable this way (`profileType` is the discriminator): `PayloadDescriptorProfile`, `CustomerProfile`, `IntervalProfile`, `DailyProfile`, `MonthlyProfile`, `BillDetails`, `InstantaneousProfile`, `EventProfile`, and `AlarmProfile` — one more than the eight the MeterData README's prose enumerates, because the descriptor profile itself is also a valid array member, not just supporting metadata.

It covers identity, provenance, validity and tamper-evidence of delivered telemetry. It does not cover the meaning of the readings themselves — that is the concern of the MeterData schema it wraps.

## 3. How Each Item is Identified

The credential's `issuer` is identified by a DID (Decentralised Identifier) — the provider's verifiable digital identifier, resolvable to confirm the issuer and detect tampering. In every worked example this is a `did:web` identifier (`did:web:amisp.discom.example`), with the actual signing key referenced from `proof.verificationMethod` as a DID URL fragment (`did:web:amisp.discom.example#key-1`).

The `credentialSubject.id` is a DID naming the consumer or asset entity the delivered data is about — in the examples, a `did:web` identifier scoped under the issuing DISCOM's own domain (`did:web:discom.example:consumers:RR-1234`), using the same path-based convention as the issuer's own `did:web`.

Revocation status is tracked through a DeDi-hosted registry referenced in `credentialStatus`, rather than through any bespoke IES revocation mechanism. Concretely, the examples show `credentialStatus.type` as `"dediregistry"`, with `id` and `statusListCredential` both pointing at `https://dedi.global/dedi/query|lookup/<issuer-did>/vc-revocation-registry` and `statusPurpose` set to `"revocation"` — i.e. the registry entry is namespaced under the *issuer's* own DID, so each provider effectively runs its own revocation list.

The credential does not mint new identifiers for meters, service points, or readings — those are carried inside the wrapped MeterData payload using its own `Identifier` scheme (`{scheme, value[, namespace]}`, where `scheme` is one of `METER_SERIAL`, `METER_BADGE`, `MRID`, `OBIS`, `SHORT_CODE`, `CONSUMER_NUMBER`, `SERVICE_DELIVERY_POINT`, `DID`, `ORG`, or `OTHER`). In the worked examples, meters, service delivery points and customers are all identified via `DID`-scheme references (e.g. `did:web:discom.example:assets:meter:DISCOM-SM-2025-654321`), keeping the identification model consistent end-to-end even though the credential wrapper itself only ever mints DIDs for issuer and subject.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **Verifiable Credential (VC)** — a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer.
- **DeDi** — the decentralised registry infrastructure (dedi.global) used for Beckn subscriber registries and credential revocation registries; not an identifier method itself. The schema's revocation registry is queried and looked up at `https://dedi.global/dedi/{query|lookup}/<issuer-did>/vc-revocation-registry`.
- **Beckn Protocol** — the open interaction protocol IES uses for discovery, negotiation and confirmation between parties (search / select / init / confirm / status and their `on_` callbacks). MeterDataCredential specifically rides in the `on_status` callback.
- **AMISP** — an Advanced Metering Infrastructure Service Provider, the metering agency that operates smart-meter data collection on a DISCOM's behalf. In the worked examples the issuer is "DISCOM AMISP – Smart Metering Data Platform" with regulatory licence `SERC-AMISP-2025-007`.
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers.
- **Data Descriptor Engine** — the MeterData v0.6 mechanism (described in that schema's README) that separates a `PayloadDescriptorProfile` dictionary (defining `readingType`, `unit`, `flowDirection`, `obis` code and compact-sequence column layout) from the dense numeric `payloads` arrays that follow it, avoiding repeating metadata on every interval reading.
- **IES Cell** — the governance body being constituted under the Central Electricity Authority (CEA) with representation from across the sector; owns the schema specifications and their versioning.

## 5. Basis of Standards

The IES order of preference is fixed, always the same:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

MeterDataCredential itself is declared in `attributes.yaml` as a subclass of the DEG-published **EnergyCredential v2.0** specification (`allOf: [$ref: https://schema.beckn.io/EnergyCredential/v2.0]`), which is in turn a subclass of `beckn:Credential`. It follows the **W3C Verifiable Credential Data Model 2.0** for its envelope (issuer, validity period, credential status, proof) and **W3C DID Core** for identifying issuer and subject. The `@context` chain a valid instance must declare is three deep: `https://www.w3.org/ns/credentials/v2`, then `https://schema.beckn.io/EnergyCredential/v2.0/context.jsonld`, then this schema's own `context.jsonld` — each layer adding only what it defines, nothing duplicated. The proof examples all use `Ed25519Signature2020` as `proof.type`.

It inherits this envelope rather than redefining it, so the credential-level standard is the W3C VC framework; any Indian- or IEC-standard references for the metering data itself belong to the wrapped MeterData v0.6 schema, not to this wrapper. That said, because the wrapped payload is inline (not merely referenced), a MeterDataCredential instance transitively carries MeterData's own standards basis: profile fields such as `EventProfile` are explicitly described in MeterData's `attributes.yaml` as an "**IS 15959** event log for one meter over a coverage period," and the `meterCategory` enum on `Meter` (values `A`, `B`, `C`, `D1`–`D4`) reflects the IS 15959 meter-classification scheme, per the MeterData README's own note that "`meterCategory` describes the regulatory standards category under IS 15959." OBIS codes (IEC 62056 object identification system) are the canonical reference for physical-quantity identification inside `payloadDescriptors`, resolved against the schema family's own `IES codes.json` registry.

## 6. Where Indian Standards Do Not Yet Exist

No Indian standard governs the verifiable-credential envelope itself, so the W3C VC Data Model 2.0 and W3C DID Core are used directly for issuer identity, signing, validity and revocation. This is the only gap documented for the credential wrapper; the standards applicable to the metering content itself are addressed in the MeterData v0.6 schema, not here (MeterData already anchors event logging and meter categorisation to IS 15959, and physical-quantity coding to OBIS/IEC 62056, so that layer is not a standards gap in the same sense).

One internal inconsistency surfaced by this research that is itself a kind of "standard not yet settled" signal: the MeterDataCredential family's top-level `README.md` (the version index one directory up from `v0.6/`) describes the v0.6 revocation mechanism as "**BitstringStatusListEntry** revocation" — a distinct W3C-standardised status-list credential type — while the actual `attributes.yaml`, compiled `schema.json`, and all three example payloads consistently implement `credentialStatus` as a bespoke `"dediregistry"` type pointing at a DeDi lookup URL, not a `BitstringStatusListEntry`. The two mechanisms are not interchangeable (one is a W3C-standard bitstring status list; the other is a DeDi-hosted custom registry type), so this looks like either a stale changelog note or an intended-but-unimplemented upgrade — see Section 11.

## 7. The Record(s)

MeterDataCredential defines one record: a Verifiable Credential instance that is issued each time a provider delivers a batch of meter data. It is not a static, long-lived record like a connection or asset credential — a new instance is issued for each delivery, with a validity window scoped to that delivery (one year in the worked examples), and it is superseded rather than amended when fresh data is needed.

The schema's own `required` list at the subject level is deliberately minimal: only `meterData` is required on `MeterDataCredentialSubject` (`id` — the subject DID — is optional at the schema level, though every worked example populates it). This means the schema permits, in principle, a credential attesting a meterData payload without naming a specific subject DID — useful for aggregate or feeder-level data that is not about one consumer, though none of the three example payloads exercise that case; all three show a named consumer subject.

It is issued by the provider — an AMISP, an MDM system, or a DISCOM performing that role — as the response to a confirmed request. Its counterpart on the request side is **MeterDataRequestCredential**, a separate schema (currently at v0.1, its own draft maturity) that is issued by the requester (typically the DISCOM) to prove authorisation to ask for the data, and is used at `confirm` time — specifically attached in `commitmentAttributes.ies:meterDataRequest` — in the Beckn exchange. MeterDataCredential is issued by the provider to attest what was actually delivered, and is used at `on_status` time, attached in `dataPayload`. Downstream, MeterDataCredential can be re-issued holder-bound to a consumer's own wallet, so the consumer can hold and re-present their verified meter history without going back to the DISCOM each time.

## 8. Schedule I — Field Reference (summary)

MeterDataCredential is built from two logical blocks:

- the **credential envelope** — inherited from EnergyCredential v2.0: `issuer` (id, name, licence number), `validFrom`/`validUntil`, `credentialStatus`, and `proof`; none of these are redefined in this schema's own `attributes.yaml` — they arrive entirely via the `allOf` reference;
- **`credentialSubject`** — defined by this schema: the subject `id` (DID of the consumer or asset entity, optional) and `meterData` (required), the attested MeterData v0.6 payload (a single profile object or an array of profile objects, per the `oneOf` in MeterData's own root schema).

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json) is at [MeterDataCredential v0.6 — Field reference](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6#field-reference).

## 9. Schedule II

MeterDataCredential is not stand-alone. It wraps a MeterData v0.6 payload inside `credentialSubject.meterData`: the credential provides the verifiable envelope (identity, validity, proof, revocation), and the MeterData schema provides the substance (customer, interval, daily, monthly, bill-details, instantaneous, event, alarm, or descriptor profiles). The `$ref` in `attributes.yaml` points at MeterData's own `attributes.yaml` component directly (`.../MeterData/v0.6/attributes.yaml#/components/schemas/MeterData`), so the two schemas are compiled together rather than loosely coupled. Validating a MeterDataCredential instance requires checking both — the credential envelope and the embedded MeterData payload against its own schema — and, one level up, the credential envelope itself is inherited from (wrapped by reference to) EnergyCredential v2.0, so a complete validation chain touches three schema documents: EnergyCredential v2.0, MeterDataCredential v0.6, and MeterData v0.6.

## 10. How It Fits Together

In a Beckn data-exchange flow, a receiver first sends a confirmed request carrying a **MeterDataRequestCredential** to prove it is authorised to ask for specific meter data — the provider's own catalog entry, at `catalog/publish` time, has already advertised both `ies:dataSchema` (pointing at MeterData v0.6, the schema used for response payloads) and `ies:capabilityProfile` (a `MeterDataRequest` describing the maximum scope the provider can serve), plus an `offerAttributes.policy.requiredCredentials` clause naming `MeterDataRequestCredential` as a precondition. The provider (an AMISP, MDM system, or DISCOM) then responds at `on_status` with the requested telemetry wrapped in a **MeterDataCredential**, binding the data to its own identity, a validity window, and a revocation path through the DeDi registry.

The receiving party checks that the credential type is `MeterDataCredential`, that `validUntil` has not passed, that the credential has not been revoked (per `credentialStatus`), and that the embedded `meterData` profiles fall within the scope originally contracted in the `MeterDataRequest` — concretely, per the sibling MeterDataRequestCredential's own README, this means resolving the issuer DID, retrieving the public key at `verificationMethod`, verifying the `proof` signature over the canonical serialisation, and finally validating `meterData` against the MeterData v0.6 schema itself. A monthly-profile example illustrates the kind of payload a receiver would be checking scope against — readings plus time-of-use buckets for a single billing month:

```json
"meterData": {
  "@type": "MonthlyProfile", "profileType": "MONTHLY",
  "timePeriod": { "start": "2026-01-01T00:00:00+05:30", "duration": "P1M" },
  "readings": [ { "readingType": "kWh imp", "value": 487.3, "validationStatus": "VALID", "source": "METER" } ],
  "touBuckets": [ { "zone": 1, "readings": [ { "readingType": "kWh imp", "value": 195.2 } ] } ]
}
```

In the **Consumer Meter Digest** use case, this same schema is re-issued holder-bound to the consumer's own wallet DID, letting the consumer re-present their verified meter history to a third party (a bank, marketplace, or installer) without the DISCOM being asked again. More generally, it is the provenance-attestation layer for any Smart Meter Data Exchange flow where the receiver needs proof of where delivered telemetry came from.

## 11. Points for Confirmation

1. This schema is at **draft** maturity (v0.6, dated 2026-06-06 per its changelog, "initial draft — aligns with MeterData v0.6") and has not yet completed technical review.
2. **Revocation mechanism inconsistency**: the MeterDataCredential family's top-level version-index README states v0.6 uses "BitstringStatusListEntry revocation," but the schema's own `attributes.yaml`, compiled `schema.json`, and all three example payloads implement `credentialStatus` as a `"dediregistry"` type against a DeDi lookup URL — not a W3C BitstringStatusListEntry. This should be reconciled: either the top-level README note is stale, or a BitstringStatusListEntry-based revocation path is planned but not yet reflected in the schema files.
3. The internal `title`/`version` metadata inside the *wrapped* MeterData schema's own `attributes.yaml` still reads `version: 0.5.0` even though it lives under the `MeterData/v0.6/` directory and is what MeterDataCredential v0.6 references — worth confirming whether this is a versioning oversight in MeterData's own source file (out of scope for this page to fix, since it lives in the read-only MeterData schema directory, but relevant to anyone tracing MeterDataCredential's dependency chain).
4. The revocation flow in practice — how quickly a provider is expected to revoke a MeterDataCredential after a meter fault or privacy request, and how downstream holders (including consumer wallets in the Consumer Meter Digest use case) are notified — is not detailed in the schema files.
5. Provenance scope-checking (that embedded `meterData` profiles fall within what was originally requested) is described as a receiver-side responsibility in both this schema's and MeterDataRequestCredential's documentation; how strictly this is enforced, and by whom, is not yet specified.
6. `credentialSubject.id` (the subject DID) is optional at the schema level even though every worked example populates it — whether an unscoped-subject credential (e.g. for feeder-level aggregate data with no single consumer) is an intended, exercised case, or simply an artefact of the schema not yet marking it required, is not stated.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| W3C VC Data Model 2.0 | Verifiable Credential envelope — issuer, validity, credential status, proof |
| W3C DID Core | Decentralised identifiers for issuer and credential subject |
| DEG EnergyCredential v2.0 (beckn.io) | Parent credential type MeterDataCredential subclasses; supplies `issuer`/`licenseNumber`, `validFrom`/`validUntil`, `credentialStatus`, `proof` |
| IS 15959 (via wrapped MeterData v0.6) | Event-log diagnostic/tamper codes (`EventProfile`) and meter regulatory category (`meterCategory`: A, B, C, D1–D4) |
| IEC 62056 / OBIS (via wrapped MeterData v0.6) | Object identification system for physical-quantity codes in `payloadDescriptors` |

### Annexure B — Example Payloads

Example credential instances (a customer-profile attestation, an interval-profile attestation with a `PayloadDescriptorProfile`, and a monthly-profile attestation with ToU buckets — all issued by the same worked-example issuer, "DISCOM AMISP") are in [schemas/MeterDataCredential/v0.6/examples](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterDataCredential/v0.6/examples).

### Annexure C — JSON Schema

The authoritative machine-readable definitions are [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/schema.json) and [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/attributes.yaml).
