# Tariff Intelligence

Tariff orders, time-of-day surcharges, deviation penalties, and data-exchange rules **published once, as code, by the issuing authority** — and consumed directly by billing systems, consumer apps, smart meters and analytics agents over **[IES Data Exchange](../../what-ies-provides/data-exchange/README.md)**.

| | |
|---|---|
| **Document** | IES/TI-PROFILE/0.5 |
| **Status** | Live or staged |
| **Applicability** | All SERCs and DISCOMs publishing tariff or programme rules |
| **This version** | Tariff Intelligence built on the `IES_Policy` family ([upstream](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core)) carried over Beckn. Live for `TARIFF` and `DISPATCH_GUIDE` policy types. A first-class `Tariff/v0.x` schema in this repository is in progress. |

> The IES-hosted schema for tariffs is in progress; this guide tracks the canonical [`beckn/DEG ies-specs`](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core) shape while it moves under `schemas/Tariff/`.

---

## 1. Scope and Purpose

The **stakeholders** are the SERC (or any policy authority — a utility, a regulator), and every downstream system that has to interpret the rule. Today a SERC issues a tariff order as a PDF; every DISCOM in the state then manually transcribes the rate slabs, time-of-day surcharges, fixed charges and category definitions into its billing system. Consumer-side apps (bill estimators, EV charging planners, rooftop-solar payback calculators) each interpret the same order independently. Drift, ambiguity and bugs are inevitable.

This document defines **Tariff Intelligence** — the SERC (or any policy authority) publishes machine-readable `IES_Policy` artefacts alongside the regulatory order. DISCOMs, apps and meters ingest the same signed object directly. No re-keying. No interpretation drift.

The same envelope generalises beyond tariffs — sanctioned-load deviation penalties, DR programme participation rules, data-quality SLAs for AMISP reporting, public-disclosure thresholds. Anything that benefits from being published once by the issuing authority and consumed mechanically downstream.

## 2. What It Records / Covers

For one policy the record carries:

- the **policy identity** — `id` (URN), `policyID` (stable handle, e.g. `RES-T1`), `policyName`, `policyType` (`TARIFF` / `DISPATCH_GUIDE` / …), `programID` linking to an `IES_Program`;
- the **validity window** — `samplingInterval` as an ISO 8601 recurrence pattern (e.g. `R/2026-04-10T00:00:00Z/P1M` — re-evaluated monthly from 10 April 2026);
- for a tariff, **`energySlabs[]`** — progressive consumption tiers, each `{ id, start (kWh, inclusive), end (kWh, exclusive or null for open-ended), price }`;
- for a tariff, **`surchargeTariffs[]`** — time-of-day adjustments, each `{ id, recurrence, interval (ToD start + duration), value, unit (`PERCENT` or `INR_PER_KWH`) }`;
- the **issuer** block and the **proof** (issuer's `did:web`; signed).

The same envelope with a different `policyType` carries deviation penalties, DR participation rules, data-quality SLAs and public-disclosure thresholds — the structure is the same, the typed payload differs.

## 3. How Each Item is Identified

| Subject | Identifier method | Example |
|---|---|---|
| Publisher (SERC / DISCOM) | `did:web` on owned domain | `did:web:ies.serc.example` |
| Policy (stable handle) | `policyID` — issuer-minted, stable across amendments | `RES-T1` |
| Policy (version) | `id` — URN, unique per version | `urn:ies:policy:serc:RES-T1:2026-04` |
| Programme this policy belongs to | `programID` | `program-merashehar-001` |
| Prior version this amends | `replaces` link to a prior `id` | `urn:ies:policy:serc:RES-T1:2025-04` |

A new amendment is a **new `id` with the same `policyID`** and an explicit `replaces` link. Downstream systems reference by `policyID` and pin the version on `id`.

## 4. Definitions

- **Policy-as-code** — a rule (tariff, penalty, SLA) authored, signed and distributed as structured, machine-evaluable data rather than as prose.
- **`policyID`** — the stable handle every downstream system references; survives amendments.
- **`id`** — the per-version URN; changes on every amendment.
- **`programID`** — groups related policies (e.g. all categories for one tariff scheme).
- **`samplingInterval`** — ISO 8601 recurrence string defining how often the policy is re-evaluated.
- **Slab** — one tier in a telescopic tariff (e.g. 0–100 kWh at ₹4.5/kWh).
- **Surcharge / discount** — a time-of-day adder (or subtractor) applied to the slab rate.

## 5. Basis of Standards

IES order of preference: **IS → CEA → IEC → IEEE**. None apply to a tariff order — tariffs are SERC instruments, not standards. The IES choices on top are:

- **Electricity Act 2003, Sections 61–62** — statutory basis for tariff determination.
- **SERC tariff orders** — the authoritative source document for each policy; the `IES_Policy` JSON-LD is a faithful, signed restatement.
- **ISO 8601** — recurrence and interval semantics (`samplingInterval`, `interval.start`, `duration`).
- **Beckn protocol v2** — the wire (public-disclosure catalogue, signed delivery, audit).
- **W3C VC Data Model 2.0** / **W3C DID Core** — issuer key (`did:web`); signature on the policy.
- **JSON-LD 1.1** — wire format and semantic resolution.

## 6. Where Indian Standards Do Not Yet Exist

The shape that carries a tariff (or any policy) is an IES specification — no Indian or international standard predates it. The choice of `IES_Policy` / `IES_Program` / `EnergySlab` / `SurchargeTariff` as the typed envelope is an IES decision, not a sector-mandated one.

## 7. The Record

The Tariff Intelligence flow produces **one signed artefact** per policy: a signed `IES_Policy` JSON-LD object, addressable by `policyID` and pinned by `id`. The signature is by the issuer's `did:web`. Verification is offline — every downstream system holds the issuer's public key from the registry and checks the signature locally; no callback to the issuer at evaluation time.

When a policy is amended, a **new signed object** is published — same `policyID`, new `id`, `replaces` link pointing to the prior version. Downstream systems update on next fetch.

A policy may also ride **inline inside a private data exchange** — e.g. a BPP attaches a data-quality SLA to its catalogue offer to set the terms of consuming the offer. Same schema, different carriage.

## 8. Schedule I — Static Fields of the Policy

The full field tables are defined upstream in the [`IES_Policy`, `IES_Program`, `EnergySlab`, `SurchargeTariff`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/attributes.yaml) source. Once the schema moves to `schemas/Tariff/v0.x/` in this repository, the generated field reference will be the canonical place to look.

Four tables in total: `IES_Policy` (envelope), `IES_Program` (grouping), `EnergySlab` (rate tiers), `SurchargeTariff` (ToD adjustments).

## 9. Schedule II — Report Templates

Not applicable as a populated downstream template. A tariff is consumed by computation (the billing engine), not by templating into a report.

The closest analogue is a **derived rate card** — a flattened view of slab × ToD outputs at fixed consumption levels — produced by a billing implementation for display. It is not a separate IES schema.

## 10. How It Fits Together

```
Today                                        With IES

SERC ──► PDF ──► DISCOM-1 billing            SERC ──► signed IES_Policy ──► Beckn ──┬── DISCOM-1 billing
            ──► DISCOM-2 billing                                                      ├── DISCOM-2 billing
            ──► consumer app A                                                        ├── consumer app A
            ──► consumer app B                                                        ├── consumer app B
            ──► smart meter firmware                                                  └── smart meter firmware
            ──► analytics agent
                                             every consumer evaluates the same
each consumer re-keys the same rules         signed object — no re-keying, no drift
```

In the IES flow, the SERC is the **BPP** (publisher); downstream systems are **BAPs** (consumers). Publication is typically open under public-disclosure norms — `accessMethod: INLINE`, settlement value `0`. Anyone with the issuer's public key can pull and verify the policy.

A billing system's job collapses to a small evaluator: look up the slab for the consumption point; look up the matching ToD surcharge; apply. The rate table that used to live in the billing code now lives in the signed policy.

## 11. Points for Confirmation

1. **Schema home** — `IES_Policy` and its companions are moving from [`beckn/DEG ies-specs`](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core) to `schemas/Tariff/v0.x/` in this repository. Integrators against the upstream shape will not see breaking changes — only a new canonical URL.
2. **Policy types beyond `TARIFF` / `DISPATCH_GUIDE`** — deviation-penalty and data-quality-SLA shapes are in draft, reusing the `IES_Policy` envelope with new `policyType` values.
3. **Amendment convention** — new `id` per amendment, same `policyID`, explicit `replaces` link. To be formalised once the schema lands in this repository.
4. **Policy bundles** — a bundle envelope to ship a related set (e.g. all categories for an FY) as one signed package is being discussed.

---

## Schemas Used in This Use Case

| Schema | Role |
|---|---|
| **`IES_Policy`** (upstream → `schemas/Tariff/v0.x/`) | The signed envelope — identity, type, validity, payload |
| **`IES_Program`** | The programme grouping the policy belongs to |
| **`EnergySlab`** | One slab tier inside a `TARIFF` policy |
| **`SurchargeTariff`** | One ToD adjustment inside a `TARIFF` policy |
| **[DatasetItem](../../what-ies-provides/data-exchange/README.md)** (DDM) | The Beckn envelope on the wire (`accessMethod: INLINE`, settlement `0` for public disclosure) |

## Value Unlock

**For SERCs** — publish once; every downstream interpretation is the same. Amendments are a new signed object, not a fresh round of memos.

**For DISCOMs** — the billing system stops carrying a state-coded rate table. The same evaluator works against any state's signed policy.

**For app developers** — bill estimators, EV charge planners, rooftop-solar payback calculators all read from one canonical source. No more "best-effort PDF parsing".

**For smart meters** — local time-of-day evaluation can pull from a signed policy bundle. The meter and the bill agree by construction.

---

## Setup: Register → Discover → Exchange

Built on the four implementation steps in **[How you implement IES](../../how-you-implement-ies/README.md)**. Use-case-specific items only below.

### Register — publisher identity

- [ ] [Identity setup](../../how-you-implement-ies/setup-register.md) complete for the publisher (SERC / DISCOM)
- [ ] Publisher in the appropriate IES reference registry — [Regulators](../../what-ies-provides/registries/README.md#reference-allow-lists-industry-coordination) or [DISCOMs](../../what-ies-provides/registries/README.md#reference-allow-lists-industry-coordination)
- [ ] `policyID` minting scheme adopted (e.g. `<STATE>-<CAT>-T<N>`); `programID`s defined

### Discover — public-disclosure catalogue

- [ ] [Discovery setup](../../how-you-implement-ies/setup-discovery.md) complete
- [ ] Publisher BPP exposes one catalogue entry per policy — `accessMethod: INLINE`, settlement `0`
- [ ] Subscribers (DISCOMs, app developers) tested as BAPs

### Exchange — authoring, signing, evaluating

- [ ] [Adapter built](../../how-you-implement-ies/build-adapter.md) for the `IES_Policy` family
- [ ] Tariff authored as `IES_Policy` JSON-LD; schema validation passes; parity with the order PDF confirmed by regulatory affairs
- [ ] Signing pipeline tested (key access, sign, verify round-trip)
- [ ] Amendment convention agreed — new `id`, same `policyID`, `replaces` link
- [ ] One sample consumer (a DISCOM billing module or app) ingests the policy and computes a bill
- [ ] Edge cases tested — open-ended top slab, surcharge-window wrap-around, percent vs absolute adders
- [ ] (If using inline-on-private-exchange) BPP attaches the policy to its private catalogue offer; consumer's `confirm` is evaluated against it
- [ ] First real tariff published alongside the SERC order
- [ ] Amendment / republication runbook in place

### Team

- [ ] Legal / regulatory SPOC (publisher)
- [ ] IT SPOC (publisher)
- [ ] IT SPOC (consumer — e.g. DISCOM billing)
- [ ] Authorised Signatory (publisher)

---

## Dev kits and code

- **Schema source** (upstream) — [`beckn/DEG ies-specs core/`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/attributes.yaml)
- **Example payloads** (devkit) — [`devkits/data-exchange/uc3-tariff-policy/examples`](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc3-tariff-policy/examples)
- **UC3 Postman collection** — [`devkits/data-exchange/uc3-tariff-policy/postman/`](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc3-tariff-policy/postman)
- **Arazzo lifecycle runner** — [`uc3-tariff-policy/workflows/run-arazzo.sh`](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc3-tariff-policy/workflows)
- **Architecture note** — [ies-docs `08_Energy_policy_as_code.md`](https://github.com/India-Energy-Stack/ies-docs/blob/main/architecture/08_Energy_policy_as_code.md)

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| Electricity Act 2003, Sections 61–62 | Statutory basis for tariff determination |
| SERC tariff orders (state-specific) | Authoritative source per policy; `IES_Policy` is a signed faithful restatement |
| ISO 8601 | Recurrence and interval semantics (`samplingInterval`, `interval.start`, `duration`) |
| Beckn Protocol v2 | Discovery, contracting, signed audit on the wire |
| W3C VC Data Model 2.0; W3C DID Core | Issuer key (`did:web`); signature on the policy |
| JSON-LD 1.1 | Wire format and semantic resolution |

## Annexure B — Example Payloads

Example payloads (Mumbai Residential, KA LT2 Industrial ToD, dispatch-guide variants) are in the devkit:

→ **[`devkits/data-exchange/uc3-tariff-policy/examples`](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc3-tariff-policy/examples)**

Sample reference implementation: the rate-lookup evaluator in any DISCOM billing module is a small function over `energySlabs[]` and `surchargeTariffs[]`.

## Annexure C — JSON Schema

While the schema lives upstream, the canonical references are:

- **Source** — [`beckn/DEG ies-specs core/attributes.yaml`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/attributes.yaml)
- **JSON-LD context** (canonical) — [`beckn/DEG ies-specs core/context.jsonld`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/context.jsonld)

When the schema moves to `schemas/Tariff/v0.x/` in this repository, the canonical URLs will become `https://india-energy-stack.github.io/ies-accelerator/schemas/Tariff/v0.x/`.
