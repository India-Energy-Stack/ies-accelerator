# MeterDataRequestCredential

*A W3C Verifiable Credential a data requester attaches to a Beckn request to prove it is authorised to ask for smart-meter telemetry.*

**Status:** Draft for technical review (current: **v0.1**) · **Issued by** the requester (a DISCOM, or a third-party aggregator/TSP) · **Consumed by** the data provider (AMISP or MDM system)

## What it records

The requester's identity (DID at `issuer.id` and `credentialSubject.id`, plus a regulatory licence number inherited from **EnergyCredential v2.0**) bound to a scoped, time-bounded query: the embedded `credentialSubject.meterDataRequest` is a [MeterDataRequest](../MeterDataRequest/README.md) object (targets, scope, window, consent references, backing authorisation, requested capability slice). It carries no telemetry — it only authorises a request for it. The credential's validity window and the historical data window it requests are two independent time ranges; both must be checked.

```
beckn:Credential └── EnergyCredential └── MeterDataRequestCredential
```

## Standards basis

- **W3C VC Data Model 2.0** and **W3C DID Core**, as a subclass of DEG **EnergyCredential v2.0** — the same inheritance pattern as its sibling energy credentials.
- The engineering substance (registers, profile types, modes) lives in the wrapped MeterDataRequest, anchored to the OBIS register space (**IEC 62056**, via IS 15959 citations in the MeterData code registry).

## How it fits together

The optional authorisation attachment on the request leg of **[Smart Meter Data Exchange](../../use-cases/smart-meter-data-exchange/README.md)**. A provider's offer policy (`offerAttributes.policy.requiredCredentials`) can require it at Beckn `confirm`; the seeker attaches the signed credential, and the provider verifies the type, validity window, revocation status (DeDi registry in `credentialStatus`), and that the embedded request is a subset of the provider's advertised capability profile. Its delivery-side counterpart is [MeterDataCredential](../MeterDataCredential/README.md) — the two bracket the same exchange from opposite ends.

## Open points

- When a provider requires this credential versus accepting a plain request is a per-provider policy decision.
- `consumerConsent` entries are plain strings; the expected format (DID, receipt hash, other) is undefined at the schema level.

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.1](v0.1/README.md) | **Current** | Initial release; wraps MeterDataRequest v0.6 |
