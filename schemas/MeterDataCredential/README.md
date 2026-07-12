# MeterDataCredential

*A signed, tamper-evident wrapper that attests who delivered a set of smart-meter readings, and that the readings have not been altered since.*

**Status:** Draft for technical review (current: **v0.6**, aligned with MeterData v0.6) · **Issued by** data providers (AMISPs, MDM systems, or a DISCOM in that role) · **Consumed by** DISCOMs, consumers' wallets, and downstream verifiers

## What it records

Structurally thin by design: the schema-specific surface is one object, `credentialSubject`, with `id` (DID of the consumer or asset the data is about) and `meterData` (the attested [MeterData](../MeterData/README.md) payload — a single profile or an array opening with a descriptor). Everything else — `issuer` (DID, name, licence number), `validFrom`/`validUntil`, `credentialStatus`, `proof` — is inherited from **EnergyCredential v2.0**. A new instance is issued per delivery, superseded rather than amended.

```
beckn:Credential └── EnergyCredential └── MeterDataCredential
```

## How things are identified

The issuer is a DID (a `did:web` in the worked examples), with the signing key referenced from `proof.verificationMethod`. Revocation is a DeDi registry (`credentialStatus.type: dediregistry`) namespaced under the issuer's own DID — each provider runs its own revocation list. Meters, service points and readings inside the payload use MeterData's own `Identifier` scheme.

## Standards basis

- **W3C VC Data Model 2.0** and **W3C DID Core** for the envelope (no Indian standard governs the VC envelope itself).
- The wrapped payload transitively carries MeterData's **IS 15959** / OBIS (IEC 62056) basis.

## How it fits together

The credential stands on its own: issued, held and verified against the provider's published key over any channel — a wallet (DigiLocker), a portal, a file. A verifier checks type, validity window, revocation, the `proof` signature, and that the embedded profiles fall within the originally contracted scope. In the **[Consumer Meter Digest](../../use-cases/consumer-meter-digest/README.md)** use case it is issued holder-bound to the consumer's wallet DID, so the consumer can re-present verified meter history without returning to the DISCOM. Its request-side counterpart is [MeterDataRequestCredential](../MeterDataRequestCredential/README.md) (proves the right to ask; this credential attests what was delivered).

## Open points

- `credentialSubject.id` is optional at the schema level; whether an unscoped-subject credential (e.g. feeder-level aggregate data) is an intended case is not stated.
- Expected revocation timelines after a meter fault or privacy request, and holder notification, are not detailed in the schema files.

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.6](v0.6/README.md) | **Current** | Wraps MeterData v0.6; DeDi-registry revocation (`credentialStatus.type: dediregistry`) |
