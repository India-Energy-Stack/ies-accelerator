# Tariff Intelligence

**In a hurry?** Jump to the [Checklist](#checklist). For the standards basis and full field schedule, see the **[Overview](../../use-cases-overview/tariff-intelligence.md)**.

**Tariff orders, time-of-day surcharges, deviation penalties, and data-exchange rules published as machine-readable *policy-as-code* — consumable by billing systems, consumer apps, smart meters, and analytics agents directly.**

---

## Scenario

A SERC issues a tariff order today as a PDF. Every DISCOM in that state then manually transcribes the rate slabs, time-of-day surcharges, fixed charges, and category definitions into its billing system. Consumer-side apps (bill estimators, EV charging planners, rooftop-solar payback calculators) each interpret the same order independently. Drift, ambiguity, and bugs are inevitable.

The same problem applies more broadly than tariff orders. Any **policy** the sector needs to interpret consistently — sanctioned-load deviation penalties, peak-hour incentives, DR programme rules, data-quality SLAs, public-disclosure thresholds — benefits from being published once, as code, by the issuing authority.

Tariff Intelligence packages this as `IES_Policy` artefacts. The SERC (or any policy issuer) publishes machine-readable policy alongside the regulatory order; DISCOMs, apps, and meters ingest it directly, with no re-keying and no interpretation drift. Issuers may publish policy in the public data exchange, or hand it inline during a private data exchange to set the terms of that exchange.

---

## Actors and Roles

| Role | Organisation (example) | What they do |
|---|---|---|
| **BPP** — policy publisher | SERC, or any policy authority | Publishes the signed `IES_Policy` artefact |
| **BAP** — policy consumer | DISCOM billing system, app developer, smart meter firmware, analytics agent | Subscribes to and ingests the policy |
| **Identity authority** | IES registries | The publisher's `did:web` is the trust anchor for the signed policy |

Publication is typically open under public-disclosure norms (settlement value `0`), so the policy consumer set is unrestricted — every billing implementation in the state can subscribe.

---

## Building Blocks Used

| Block | Role in this use case |
|---|---|
| [Identifiers](../../what-ies-provides/register.md) | The `policyID` (e.g. `MUM-RES-T1`) is an IES identifier; the policy binds to the publisher's `did:web` and references the `programID` it belongs to. |
| [Registries](../../what-ies-provides/register.md#the-directory-dedi) | The publishing SERC/utility is looked up in the [IES Regulators or DISCOMs reference registry](../../what-ies-provides/register.md#the-directory-dedi) for its public key. |
| [Data Exchange](../../what-ies-provides/discover.md) | Policies are distributed over the same Beckn-based protocol used for telemetry and filings — publicly, or carried inline as part of a private data exchange to negotiate that exchange's terms. |

---

## The Dataset — `IES_Policy`

The `IES_Policy` schema captures policy as structured, signed JSON-LD. For tariffs, one object carries:

- **Identity** — `id`, `policyID`, `policyName`, `policyType` (`TARIFF` or `DISPATCH_GUIDE`), `programID`.
- **Validity** — `samplingInterval` as an ISO 8601 recurrence pattern (e.g. `R/2026-04-10T00:00:00Z/P1M`).
- **`energySlabs[]`** — progressive consumption tiers, each `{ id, start (kWh), end (kWh or null), price }`.
- **`surchargeTariffs[]`** — time-of-day adjustments, each `{ id, recurrence, interval, value, unit (PERCENT | INR_PER_KWH) }`.

```json
{
  "@type": "IES_Policy",
  "id": "policy-mumbai-res-001",
  "policyID": "MUM-RES-T1",
  "policyName": "Mumbai Residential Telescopic 2026",
  "policyType": "TARIFF",
  "programID": "program-merashehar-001",
  "samplingInterval": "R/2026-04-10T00:00:00Z/P1M",
  "energySlabs": [
    { "id": "slab-0-100",   "start": 0,   "end": 100,  "price": 4.5 },
    { "id": "slab-301-plus", "start": 301, "end": null, "price": 9.8 }
  ],
  "surchargeTariffs": [
    { "id": "surcharge-evening-peak", "recurrence": "P1D",
      "interval": { "start": "T18:00:00Z", "duration": "PT4H" }, "value": 20, "unit": "PERCENT" }
  ]
}
```

The same envelope, with a different `policyType`, expresses deviation penalties, data-quality SLAs, DR programme rules, and public-disclosure thresholds.

> **Status.** The schema currently lives upstream at [`beckn/DEG ies-specs`](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core) and is moving to `schemas/Tariff/v0.x/` in this repository. Integrators against the upstream shape will not see breaking changes — only a new canonical URL.

---

## Setup: Register → Discover → Exchange

### 1. Register — publisher identity

- Publisher (SERC / DISCOM) in the appropriate [reference registry](../../what-ies-provides/register.md#the-directory-dedi) → **[Setup Register](../../how-you-implement-ies/setup-register.md)**.
- Mint a canonical `policyID` per policy (the stable handle every downstream system references) and a `programID` grouping related policies — see [Identifiers — Appendix C](../../what-ies-provides/register.md#identifier-patterns).

### 2. Discover — publish via the data exchange

Publisher's BPP exposes one catalogue entry per policy → **[Setup Exchange](../../how-you-implement-ies/setup-exchange.md)**. Public-disclosure policies typically use `accessMethod: INLINE` and settlement value `0` — anyone can pull them without a contract.

### 3. Exchange — author, sign, evaluate

Author the policy directly in `IES_Policy` JSON-LD against the [upstream schema](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/attributes.yaml); validate before signing. The publisher's BPP signs with its `did:web` private key. A billing system's consumer-side logic collapses to a small evaluator: look up the applicable slab, look up the matching time-of-day surcharge, apply.

A BPP may also attach a policy alongside its catalogue offer to set the **terms of a private data exchange** — e.g. a refresh-rate or retention SLA a consumer must commit to. The consumer's `confirm` is then evaluated against the inline policy.

---

## Checklist

For a SERC, DISCOM, or other policy authority. Role: ☐ Publisher ☐ Consumer.

**1. Decide which policies to publish** — usually residential and LT-commercial tariff orders first.

- [ ] Policy types selected (`TARIFF`, `DISPATCH_GUIDE`, …); source documents identified

**2. Register on the IES network.**

- [ ] Publisher registered in the appropriate reference registry (Regulators / DISCOMs)

**3. Mint stable identifiers.**

- [ ] `policyID` scheme adopted; `programID`s defined

**4. Author the policy as structured data.**

- [ ] Authored in `IES_Policy` JSON-LD; schema validation passes; parity with the order PDF confirmed

**5. Sign with the publisher's key.**

- [ ] Signing pipeline tested
- [ ] Amendment convention agreed — new `id` per amendment, same `policyID`, `replaces` link

**6. Publish via the data exchange.**

- [ ] Catalogue entry published; public-disclosure access policy documented

**7. Sample-consume in a billing system.**

- [ ] Sample consumer ingests the policy and computes a bill
- [ ] Edge cases tested (open-ended top slab, surcharge-window wrap-around, percent vs absolute adders)

**8. Production deployment and go-live.**

- [ ] First real tariff published alongside the SERC order; amendment / republication runbook in place

**9. Team.** [ ] Legal / regulatory SPOC (publisher) · [ ] IT SPOC (publisher) · [ ] IT SPOC (consumer)

---

## Open Items

- **Policy types beyond `TARIFF` / `DISPATCH_GUIDE`** — deviation-penalty and data-quality-SLA shapes are in draft.
- **Amendment convention** — new `id` per amendment, same `policyID`, `replaces` link — to be formalised once the schema lands in this repository.
- **Policy bundles** — shipping a related set (e.g. all categories for one FY) as one signed package is being discussed.

---

## References

- [`IES_Policy`, `IES_Program`, `EnergySlab`, `SurchargeTariff` (upstream)](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core)
- [Example payloads (devkit)](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc3-tariff-policy/examples)
- [Overview — Tariff Intelligence](../../use-cases-overview/tariff-intelligence.md) — standards basis, definitions, full field schedule
- [Data Exchange chapter](../../what-ies-provides/discover.md)
- [Identifiers and Addressing](../../what-ies-provides/register.md)
