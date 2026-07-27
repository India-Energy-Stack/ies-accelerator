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
| Publisher & signature | Publisher identity and cryptographic proof are carried by the signed publication/exchange envelope; they are not fields in the current upstream `IES_Policy` source | Beckn signing / DID resolution |

## 3. How Each Item is Identified

| Subject | Identifier method | Example |
|---|---|---|
| Publisher (SERC / DISCOM) | `did:web` on owned domain | `did:web:ies.serc.example` |
| Policy (stable handle) | `policyID` — issuer-minted | `RES-T1` |
| Policy (version) | `id` — URN, unique per version | `urn:ies:policy:serc:RES-T1:2026-04` |
| Prior version this amends | No current `IES_Policy` field; publication metadata may carry the predecessor ID | `urn:ies:policy:serc:RES-T1:2025-04` |

A new amendment is a new `id` with the same `policyID`; downstream systems reference by `policyID`, pin the version on `id`, and retain any predecessor relationship as publication metadata until the upstream schema governs one.

## 4. Definitions

- **Policy-as-code** — a rule authored, signed and distributed as structured, machine-evaluable data rather than prose.
- **`policyID`** — the stable handle that survives amendments; **`id`** — the per-version URN.
- **`samplingInterval`** — ISO 8601 recurrence defining re-evaluation frequency.
- **Slab** — one tier in a telescopic tariff; **surcharge** — a time-of-day adder/subtractor on the slab rate.

## 5. Basis of Standards

Fixed order of preference: **IS → CEA → IEC → IEEE** — none apply directly, as tariffs are SERC instruments. IES adds:

| Standard | Role here |
|---|---|
| **Electricity Act 2003, §61–62** | Statutory basis |
| **SERC tariff orders** | Source (`IES_Policy` is a faithful signed restatement) |
| **ISO 8601** | Recurrence semantics |
| **Beckn Protocol v2** | The wire |
| **W3C VC / DID Core** | Issuer key, signature |

## 6. Where Indian Standards Do Not Yet Exist

The shape carrying a tariff or any policy is an IES specification — `IES_Policy` / `IES_Program` / `EnergySlab` / `SurchargeTariff` is an IES decision, not a sector-mandated one.

## 7. The Record

Each policy version is a separate payload, addressable by `policyID` and pinned by `id`. The current upstream `IES_Policy` source defines neither an issuer/proof block nor a `replaces` field. Authenticity comes from the signed publication or exchange envelope. An amendment keeps the same `policyID` but receives a new `id` and modification timestamp. Any explicit predecessor link remains delivery metadata until the upstream schema governs one. A policy may also ride inline inside a private data exchange, for example as terms attached to a BPP catalogue offer.

## 8. Schedule I — Static Fields of the Policy

Schedule I reflects the current upstream [`IES_Policy` / `IES_Program` / `EnergySlab` / `SurchargeTariff`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/attributes.yaml) source on the DEG `ies-specs` branch. These are **upstream WIP fields, not a locally frozen IES schema**. **Upstream Requires** follows that source; the policy guidance is informative. Once an approved schema moves to `schemas/Tariff/v0.x/`, its generated field reference supersedes this table.

### 8.1 Policy Identity, Type and Applicability

| **Upstream Field** | **Type / Allowed Value** | **Upstream Requires** | **Policy Guidance** *(informative)* |
|---|---|---|---|
| `id` | OpenADR object ID | Required on `IES_Policy` | Unique identifier for this policy version |
| `createdDateTime` | date-time | Required on `IES_Policy` | Creation timestamp |
| `modificationDateTime` | date-time | Required on `IES_Policy` | Changes with each published version |
| `objectType` | constant `POLICY` | Required through `IES_PolicyRequest` | Identifies the object family |
| `@context` | context URI text | Optional | Use the context published with the upstream policy family |
| `programID` | OpenADR object ID | Required | Links the policy to its governing programme |
| `policyID` | text | Required | Stable handle retained across amendments |
| `policyName` | text | Optional | Human-readable authority title |
| `policyType` | `TARIFF` or `DISPATCH_GUIDE` | Required | These are the only values in the current upstream enum; other sub-use-cases remain draft until the schema expands |
| `samplingInterval` | ISO 8601 recurrence text | Optional | Defines recurring evaluation/application cadence |
| `targets` | OpenADR programme targets | Optional | Narrows applicability to the intended participant/resource segment |

### 8.2 Tariff Energy Slabs

| **Upstream Field** | **Type** | **Upstream Requires** | **Tariff Guidance** *(informative)* |
|---|---|---|---|
| `energySlabs[]` | array of `EnergySlab` | Optional on the policy | Populate for a `TARIFF` policy using progressive energy tiers |
| `energySlabs[].id` | text | Required per slab | Stable slab identifier within the policy version |
| `energySlabs[].start` | number (kWh, inclusive) | Required per slab | Lower bound of the tier |
| `energySlabs[].end` | number or `null` (kWh, exclusive) | Optional | `null` represents an unbounded final tier |
| `energySlabs[].price` | number | Required per slab | Base energy price; the upstream field currently has no separate currency/unit property |

### 8.3 Time-of-day Surcharges and Discounts

| **Upstream Field** | **Type / Allowed Value** | **Upstream Requires** | **Tariff Guidance** *(informative)* |
|---|---|---|---|
| `surchargeTariffs[]` | array of `SurchargeTariff` | Optional on the policy | Populate for recurring ToD adjustments |
| `surchargeTariffs[].id` | text | Required per entry | Stable adjustment identifier |
| `surchargeTariffs[].recurrence` | ISO 8601 duration | Required per entry | Recurrence cadence, e.g. `P1D` |
| `surchargeTariffs[].interval` | relative interval object | Required per entry | Time-of-day window for the adjustment |
| `interval.start` / `.duration` | ISO 8601 local-time text / duration | Both required | Defines the start and width of the ToD window |
| `surchargeTariffs[].value` | number | Required per entry | Signed adjustment value |
| `surchargeTariffs[].unit` | `PERCENT` or `INR_PER_KWH` | Optional; default `PERCENT` | Makes percentage versus absolute adjustment explicit |

### 8.4 Fields Not Present in the Current Upstream Policy Object

| **Concept Used by This Page** | **Current Upstream Status** | **Treatment** |
|---|---|---|
| Publisher / issuer DID | No `issuer` field in `IES_Policy` | Resolve the signer from the signed publication/exchange envelope |
| Cryptographic `proof` | No W3C VC proof block in `IES_Policy` | Verify the Beckn/catalogue or dataset-envelope signature; do not insert an ungoverned proof field |
| Prior-version `replaces` link | No such field in the current source | Carry as publication metadata until a governed upstream field exists |
| Currency for `EnergySlab.price` | No slab-level currency/unit field | The profile assumes the authority's tariff context; a future schema should make currency explicit |
| First-class local `Tariff/v0.x` schema | Not yet present | Keep this page WIP and do not claim local schema validation |

## 9. Schedule II — Report Templates

A policy is consumed by computation. Schedule II lists derived views, not additional schema objects.

| **Derived View** | **Schedule I Inputs** | **Schema Status** | **Treatment** |
|---|---|---|---|
| Flattened rate card | `energySlabs[]` × applicable `surchargeTariffs[]` | Derived | Render for humans; retain the exact policy `id` and `policyID` used |
| Bill-calculation trace | usage quantities, selected slab and ToD adjustment | Derived | Explain each applied rule and preserve the input MeterData reference |
| Consumer tariff comparison | multiple policy versions/categories | Derived | Compare only policies with compatible targets, units and effective periods |
| Billing-engine configuration | policy fields transformed to implementation rules | Derived deployment artefact | Version and test against the source policy; it is not the authority's signed record |
| Amendment history | same `policyID`, successive `id`/timestamps | Derived until a predecessor field is governed | Never overwrite the prior signed publication |
| Non-tariff policy view | `DISPATCH_GUIDE` or a future governed `policyType` | Depends on upstream enum | Do not encode draft policy types as if the current schema accepts them |

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
