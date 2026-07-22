# Policy as Code

*Any authority policy — tariff orders, time-of-day surcharges, dispatch guides, deviation penalties, and data-exchange rules — published once, as signed machine-readable code by the issuing authority, and consumed directly by billing systems, consumer apps, smart meters and analytics agents over [IES Data Exchange](../what-ies-provides/discover.md).*

{% hint style="warning" %}
🚧 **Work in progress.** This section is still being finalised and may change before sign-off.
{% endhint %}

**[Implementation Guide →](../use-cases/tariff-intelligence/README.md)**

| Field | Value |
|---|---|
| Document | IES/TI-PROFILE/0.5 |
| Status | 🚧 Work in progress (WIP) |
| Applicability | All SERCs and DISCOMs publishing tariff or programme rules |
| This version | Built on the `IES_Policy` family ([upstream](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core)) over Beckn. Live for `TARIFF` and `DISPATCH_GUIDE` types. A first-class `Tariff/v0.x` schema in this repo is in progress. |

---

## 1. Scope and Purpose

The stakeholders are the policy authority (a SERC, the CEA, a load-despatch centre or a programme administrator) and every downstream system that must interpret its rules. Today an authority issues a policy — most commonly a tariff order — as a PDF; every DISCOM transcribes rate slabs, surcharges and category definitions by hand into billing systems, and consumer apps each interpret the order independently. Drift and bugs are inevitable.

This document defines **Policy as Code** — the authority publishes machine-readable, signed `IES_Policy` artefacts alongside the order; DISCOMs, apps and meters ingest the same object and evaluate it locally. The same envelope carries any policy the sector must apply consistently.

### Sub-use-cases

Policy as Code is a family; each sub-use-case publishes a different kind of authority policy through the same `IES_Policy` envelope, identity and signing.

| Sub-use-case | Policy published as code | Status |
|---|---|---|
| **Tariff Intelligence** *(flagship)* | Tariff orders, telescopic slabs, time-of-day surcharges (`policyType: TARIFF`) | Live or staged |
| **Dispatch guides** | Merit-order / dispatch rules (`policyType: DISPATCH_GUIDE`) | Live or staged |
| **Deviation penalties** | Sanctioned-load / schedule deviation charges | Draft |
| **DR programme rules** | Demand-response participation and incentive rules | Draft |
| **Data-exchange SLAs** | Data-quality and public-disclosure thresholds | Draft |

The rest of this page details the **Tariff Intelligence** sub-use-case — the first published; the other policy types reuse the same envelope and identity described below.

## 2. What It Records / Covers

| Records | Detail | Source |
|---|---|---|
| Policy identity | `id`, `policyID` (stable handle), `policyName`, `policyType` (`TARIFF` / `DISPATCH_GUIDE` / …), `programID` | IES_Policy |
| Validity window | `samplingInterval` as an ISO 8601 recurrence (e.g. `R/2026-04-10T00:00:00Z/P1M`) | IES_Policy (ISO 8601) |
| Energy slabs | For a tariff, `energySlabs[]` — progressive tiers `{ id, start, end, price }` | IES_Policy |
| Surcharge tariffs | For a tariff, `surchargeTariffs[]` — time-of-day adjustments `{ id, recurrence, interval, value, unit }` | IES_Policy |
| Issuer & proof | The issuer block and cryptographic proof | IES_Policy (W3C VC) |

## 3. How Each Item is Identified

| Subject | Identifier method | Example |
|---|---|---|
| Publisher (SERC / DISCOM) | `did:web` on owned domain | `did:web:ies.serc.example` |
| Policy (stable handle) | `policyID` — issuer-minted | `RES-T1` |
| Policy (version) | `id` — URN, unique per version | `urn:ies:policy:serc:RES-T1:2026-04` |
| Prior version this amends | `replaces` link | `urn:ies:policy:serc:RES-T1:2025-04` |

A new amendment is a new `id` with the same `policyID`; downstream systems reference by `policyID` and pin the version on `id`.

## 4. Definitions

- **Policy-as-code** — a rule authored, signed and distributed as structured, machine-evaluable data rather than prose.
- **`policyID`** — the stable handle that survives amendments; **`id`** — the per-version URN.
- **`samplingInterval`** — ISO 8601 recurrence defining re-evaluation frequency.
- **Slab** — one tier in a telescopic tariff; **surcharge** — a time-of-day adder/subtractor on the slab rate.

## 5. Basis of Standards

**IS → CEA → IEC → IEEE** — none apply directly; tariffs are SERC instruments. IES adds: **Electricity Act 2003 §61–62** (statutory basis), **SERC tariff orders** (source; `IES_Policy` is a faithful signed restatement), **ISO 8601** (recurrence semantics), **Beckn v2** (the wire), **W3C VC / DID Core** (issuer key, signature).

## 6. Where Indian Standards Do Not Yet Exist

The shape carrying a tariff or any policy is an IES specification — `IES_Policy` / `IES_Program` / `EnergySlab` / `SurchargeTariff` is an IES decision, not a sector-mandated one.

## 7. The Record

One signed artefact per policy — addressable by `policyID`, pinned by `id`, signed by the issuer's `did:web`. Verification is fully offline. Amendment publishes a new signed object — same `policyID`, new `id`, a `replaces` link. A policy may also ride inline inside a private data exchange, e.g. attached to a BPP catalogue offer to set the terms of consuming it.

## 8. Schedule I — Static Fields of the Policy

Field tables are defined upstream in [`IES_Policy` / `IES_Program` / `EnergySlab` / `SurchargeTariff`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/attributes.yaml). Once the schema moves to `schemas/Tariff/v0.x/` in this repo, the generated field reference becomes canonical.

## 9. Schedule II — Report Templates

Not applicable — a tariff is consumed by computation, not templating. The closest analogue is a derived rate card (a flattened slab × ToD view), produced by a billing implementation for display, not a separate schema.

## 10. How It Fits Together

```
Today: SERC ──► PDF ──► DISCOM-1/-2 billing, consumer apps, meter firmware, analytics — each re-keys
With IES: SERC ──► signed IES_Policy ──► Beckn ──► every consumer evaluates the same signed object
```

The SERC is the **BPP** (publisher); downstream systems are **BAPs**. Publication is typically open (`accessMethod: INLINE`, settlement `0`) — anyone with the issuer's public key can pull and verify. A billing system's job collapses to a small evaluator: find the slab, find the matching ToD surcharge, apply.

## 11. Points for Confirmation

1. **Schema home** — moving from `beckn/DEG ies-specs` to `schemas/Tariff/v0.x/`; no breaking change for integrators, only a new canonical URL.
2. **Policy types beyond `TARIFF` / `DISPATCH_GUIDE`** — deviation-penalty and data-quality-SLA shapes are in draft.
3. **Amendment convention** — new `id`, same `policyID`, explicit `replaces` link — to be formalised.
4. **Policy bundles** — shipping a related set as one signed package is being discussed.

---

## Schemas Used in This Use Case

| Schema | Role |
|---|---|
| `IES_Policy` (upstream → `schemas/Tariff/v0.x/`) | The signed envelope |
| `IES_Program` | Programme grouping |
| `EnergySlab` / `SurchargeTariff` | Tariff tiers / ToD adjustments |
| DatasetItem (DDM) | The Beckn envelope (`accessMethod: INLINE`, settlement `0` for public disclosure) |

## Value Unlock

**SERCs** — publish once; amendments are a new signed object, not a memo round. **DISCOMs** — billing stops carrying a hand-coded rate table. **App developers** — one canonical source instead of best-effort PDF parsing. **Smart meters** — local ToD evaluation from a signed policy bundle, agreeing with the bill by construction.

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| Electricity Act 2003, §61–62 | Statutory basis for tariff determination |
| SERC tariff orders (state-specific) | Authoritative source per policy |
| ISO 8601 | Recurrence and interval semantics |
| Beckn Protocol v2 | Discovery, contracting, signed audit |
| W3C VC Data Model 2.0; W3C DID Core | Issuer key; policy signature |
| JSON-LD 1.1 | Wire format and semantic resolution |

## Annexure B — Example Payloads

Mumbai Residential, KA LT2 Industrial ToD, dispatch-guide variants: **[`devkits/data-exchange/uc3-tariff-policy/examples`](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc3-tariff-policy/examples)**.

## Annexure C — JSON Schema

While the schema lives upstream: **[`beckn/DEG ies-specs core/attributes.yaml`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/attributes.yaml)** (source), [`context.jsonld`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/context.jsonld) (canonical). Once moved: `https://india-energy-stack.github.io/ies-accelerator/schemas/Tariff/v0.x/`.
