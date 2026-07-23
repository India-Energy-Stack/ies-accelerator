# MeterDataRequest

*The query, capability and authorisation shapes a party uses to ask for smart-meter telemetry — not the telemetry itself.*

**Status:** Draft for technical review (current: **v0.6**) · **Published by** providers (DISCOMs, AMISPs) · **Used by** requesters (DISCOMs, TSPs, consented third parties)

## What it records

Three composable models under one `oneOf` payload root, replacing v0.5's single flat request object:

| Model | Purpose |
|-------|---------|
| `MeterDataCapabilities` | What a provider can serve — profile types (optionally down to individual registers), supported query scopes, maximum history window |
| `MeterDataAuthorisation` | Who authorised whom — grantor, grantee, purpose, validity window, and the granted capability slice (all six fields required) |
| `MeterDataRequest` | The actual query — target consumers/resources, scope (`ResourceOnly` / `ResourceAndChildren` / `ChildrenOnly`), time window, consent references, backing authorisation, requested capability slice, record cap |

## How things are identified

Consumers and resources are URIs/DIDs; the schema mints no identifier scheme of its own. Registers are named by OBIS code or short code (`kWh imp`), resolved against the MeterData family's `IES codes.json` registry. A shipped semantic validator cross-checks what JSON Schema alone cannot: that a requested register exists, is permitted under the stated profile type, supports the requested telemetry mode, and that authorisation windows are coherent.

## Standards basis

The request/authorisation envelope is IES-native. Its one standards touchpoint is the register space in `ValueCapability.value`, anchored to **IS 15959** (via the per-register part/table/clause citations in `IES codes.json`), with IEC 62056/OBIS as the second-order reference.

## How it fits together

The request leg of **[Smart Meter Data Exchange](../../use-cases/smart-meter-data-exchange/README.md)**: a provider advertises capabilities, a requester obtains an authorisation naming its slice, then issues per-query requests — answered by a separate [MeterData](../MeterData/README.md) payload. Where authorisation must be proven cryptographically, the request is wrapped in a [MeterDataRequestCredential](../MeterDataRequestCredential/README.md).

## Open points

- `authorisation` accepts an inline object or a URI reference; a documented convention for when each form is expected (and how a URI-referenced grant is verified) is pending.
- Every shipped example uses short codes; the raw-OBIS form of `ValueCapability.value` is currently unexercised.

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v0.6](v0.6/README.md) | **Current** | Split into three composable models: MeterDataCapabilities, MeterDataAuthorisation, MeterDataRequest |
| [v0.5](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterDataRequest/v0.5) | Previous | Single unified request schema |
