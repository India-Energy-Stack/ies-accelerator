# ElectricityCredential

*A W3C Verifiable Credential, issued per meter or connection by a distribution licensee, that carries the static facts of a consumer's connection and the energy resources behind the meter.*

> **Mirror.** This directory is a verbatim mirror of the Beckn DEG [`ElectricityCredential`](https://github.com/beckn/DEG/tree/main/specification/schema/ElectricityCredential) specification. Upstream is authoritative; open an issue if you find a discrepancy.

> **Flat context (temporary).** `v1.2/context.jsonld` pulls `EnergyResource`, `MeterServiceProfile` and `CustomerDetails` in with `@import` and scoped contexts. Verifiers that do not resolve either (DigiLocker's credential checker among them) report every imported term as missing. [`v1.2/context.inline.jsonld`](v1.2/context.inline.jsonld) is the shape that checker expects: one level, every field name once, mapped to its IRI as a plain string, with no `@import`, no nesting and no `@type`/`@container` wrappers. Every IRI in it resolves: `schema.org` and `qudt.org` terms keep their upstream IRIs; IES/DEG terms, whose `https://schema.nfh.global/deg#…` namespace serves no page, point back at this file as `…/context.inline.jsonld#<term>`. That makes the file self-describing for a reviewer clicking through it, and it also means a credential issued against it uses different term IRIs from one issued against `context.jsonld`. Also lost: the typing and structure the nested wrappers carried (`type` overrides for resources and geo, `xsd` datatypes, `@id` coercion, list order on `coordinates`). Credentials must be issued against the file they are verified with. Published at `https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.inline.jsonld`; local to this repository, not part of the upstream mirror, and to be retired once the verifier resolves standard JSON-LD 1.1 contexts.

**Status:** Stable — In Pilot (current: **v1.2**) · **Issued by** DISCOMs · **Consumed by** consumers (holder-bound), grid operators and aggregators (bearer), banks / subsidy portals / DER marketplaces (as verifiers)

## What it records

For one connection: the non-PII **customer profile** (utility CA number, tariff and load terms per meter via `consumptionProfiles[]`), the **energy resources behind the meter** (`energyResources[]` — a discriminated union of seven kinds: meter, generator, storage, EV charger, inverter, controllable load, network equipment, each with make, ratings, commissioning and inspection facts), and optionally the PII **customer details** (name, installation address) when issued to the consumer. It records static, structural facts only — live readings belong to [MeterData](../MeterData/README.md).

Two issuance variants of the same record: **bearer** (no `credentialSubject.id`; grid-side, non-PII issuance) and **holder-bound** (`credentialSubject.id` = the consumer's wallet DID; the Consumer Energy Passport pattern).

## How things are identified

The issuer is a `did:web` on the DISCOM's domain, optionally paired with a regulator licensing reference (`issuer.idRef`). Assets carry `did:web` paths under the issuer's domain (e.g. `did:web:ies.discom.example:assets:meter:<slno>`) — existing serial numbers are preserved, never replaced. Topology is expressed through `parentResources[]` / `subResources[]` links, which lets one credential cover anything from a single domestic meter to a multi-meter building with tenant sub-metering or parallel import/export metering.

The schema is a **composition**: its own `attributes.yaml` defines only the envelope and profile containers, pulling in `EnergyCredential/v2.0` (base), `EnergyResource/v2.1`, `MeterServiceProfile/v1.1`, `CustomerDetails/v1.0` and `IdRef/v1.0` by reference.

## Standards basis

- **IS 16444** (smart meter spec; DLMS/COSEM per IS 15959) for meter protocol fields; **IS 16221** / IEC 61727 for PV capacity.
- **CEA Connectivity Regulations 2013 (amended 2018)** with **IEEE 1547-2018 Cl. 11** for the per-asset inspection record.
- **IEC 61968 / 61970 (CIM)** class-level alignment for every resource kind; **IEEE 2030.5**, SunSpec DER models, OCPP / ISO 15118 for DER, inverter and V2G attributes.
- Where no Indian standard exists (aggregator enrolment, ride-through categories, DR control protocols), international standards fill the gap — flagged per field in the reference.

## How it fits together

One schema behind two use cases: as the **[Consumer Energy Passport](../../use-cases/consumer-energy-passport/README.md)** it is issued holder-bound into the consumer's wallet — one credential per consumer connection, never combining consumers. For **[DER Visibility](../../use-cases/der-visibility/README.md)**, its `EnergyResource` and `ConsumptionProfile` building blocks are published PII-free as per-feeder arrays, giving operators a checkable view of what is connected. It inherits its envelope from `EnergyCredential`:

```
beckn:Credential └── EnergyCredential └── ElectricityCredential
```

## Open points

- Deprecated type aliases `SOLAR` → `SOLAR_PV` and `BATTERY` → `BESS` remain valid during transition; `ratedPower` is kept for backward compatibility, with `maxExport` / `maxImport` preferred.
- The composition pins five sibling schemas; confirm exact sibling versions before treating "v1.2" as a complete wire-format spec.

## Versions

| Version | Status | Notes |
|---------|--------|-------|
| [v1.2](v1.2/README.md) | **Current** | Composable EnergyResource kinds (7 typed discriminants); directional power fields; EV charger kind |
| [v1.1](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ElectricityCredential/v1.1) | Previous | Unified `energyResources[]`, multi-meter topology support |
| [v1.0](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ElectricityCredential/v1.0) | Deprecated | Separate consumption/generation/storage profile arrays |
