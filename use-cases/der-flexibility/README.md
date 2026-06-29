# DER Flexibility

A DISCOM (or aggregator on its behalf) procures **demand-side flexibility** — load curtailment, load shift, or local generation — from a cohort of behind-the-meter resources, with **measurement and verification** flowing back per meter, per interval, as a signed time series.

| | |
|---|---|
| **Document** | IES/DERF-PROFILE/2.0 |
| **Status** | In progress (schema stable in DEG `demand-flex` devkit; pilot integrations being staged) |
| **Applicability** | DISCOMs, aggregators, flex-capable consumers |
| **This version** | Built on the DEG `DemandFlexNeed` / `DemandFlexBuyOffer` / `DemandFlexPerformance` family (canonical at [schema.beckn.io](https://schema.beckn.io)) over Beckn. Reuses the shared `EnergyResource`, `DEGContract`, `RevenueFlow` and `BecknTimeSeries` primitives. Mirrored in [External Schemas — Demand Flexibility](../../schemas/external/README.md#demand-flexibility). |

---

## 1. Scope and Purpose

The **stakeholders** are the DISCOM (need-publisher), one or more **aggregators** (sellers — they enrol cohorts of behind-the-meter resources), and the **end consumers / prosumers** whose resources participate. Today, flexibility programmes run as bespoke contracts with named vendors, with M&V (Measurement and Verification) flowing back as spreadsheets and a hand-stitched baseline calculation per programme.

This document defines **DER Flexibility** — the DISCOM advertises a `DemandFlexNeed` (direction, window, capacity, location), aggregators respond with a `DemandFlexBuyOffer` binding a cohort of meters and resources, and per-meter performance flows back as `DemandFlexPerformance` (each meter's `BecknTimeSeries` with `BASELINE` and `USAGE` payloads, aligned to the same interval grid).

The protocol scales from a handful of meters to large cohorts via on-protocol tamper-evidence anchors (`participatingMetersDigest`) and off-protocol bundle refs (`participatingMetersRef`).

## 2. What It Records / Covers

For one flex programme the records carry:

- the **need** — `direction` (`INCREASE` / `REDUCE`), `capacityType` (`CURTAILMENT` / `SHIFT` / `GENERATION`), `eventWindow` (UTC start / end), `maxCapacityKw`, `location` (GeoJSON);
- the **offer** — buyer inputs (incentive per kWh, currency, penalty rate, baseline methodology), seller inputs (planned demand change, cohort of participating meters, energy resources behind them, M&V report descriptors);
- the **cohort identity** — `participatingMetersDigest` (SHA-256 of sorted meter IDs); permanently committed by Beckn signing of the `confirm` payload;
- per-meter **performance** — `meters[]` each with `meterId` and `telemetry` (a `BecknTimeSeries` carrying `BASELINE` always, plus `USAGE` once the event completes, on the same interval grid);
- the **revenue flows** — computed by the settlement policy from baseline-vs-usage delta × incentive.

`BecknResourceRef` is used to deliver large cohorts off-protocol when the inline payload would be too heavy; `participatingMetersDigest` is the on-protocol tamper-evidence anchor that survives even if the ref URL later 404s.

## 3. How Each Item is Identified

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (buyer) | `did:web` on owned domain | `did:web:ies.tpddl.in` |
| Aggregator (seller) | `did:web` on owned domain | `did:web:aggregator.example.com` |
| Programme | DISCOM-minted ID | `TPDDL-FLEX-SUMMER-2026` |
| Event | DISCOM-minted ID per fired event | `TPDDL-FLEX-EVT-2026-06-29-1900` |
| Participating meter | `did:web` reused from existing IDs (per [SMDX](../smart-meter-data-exchange/README.md#id-3.-how-each-item-is-identified)) | `did:web:ies.tpddl.in:assets:meter:NM-44091234` |
| Cohort | `participatingMetersDigest` (SHA-256, count) | `sha256:abc…` over the sorted meter IDs, count 10 042 |
| Energy resource enrolled | `EnergyResource.id` per the shared resource schema | per [External — Energy Trading](../../schemas/external/README.md#energy-trading-p2p) |

## 4. Definitions

- **Baseline** — the consumption profile a meter would have followed in the absence of the flex event; computed per a declared `methodology` (e.g. `5of10`: average of the 5 highest-consumption days out of the last 10).
- **Usage** — the actual consumption during the event window.
- **Delta** — baseline − usage (for `REDUCE`) or usage − baseline (for `INCREASE`); the basis for incentive computation.
- **Cohort** — the set of meters enrolled in one offer; committed by the `participatingMetersDigest`.
- **M&V** — Measurement and Verification — the per-meter telemetry that proves performance against the baseline.
- **Off-protocol bundle** — large cohort or telemetry payloads carried as a separate fetched resource (`BecknResourceRef`), anchored by a digest.
- **Paged inline delivery** — splitting `meters[]` across multiple `on_status` messages, assembled by `pageInfo.sequence` until `isLast == true`.

## 5. Basis of Standards

IES order of preference: **IS → CEA → IEC → IEEE**. Indian standards for demand-side flexibility procurement do not yet exist; the IES choices are:

- **OpenADR 3.0 / 3.1** — the international demand-flex protocol; informs the `DemandFlexNeed` shape and the `BASELINE` / `USAGE` payload semantics.
- **IEEE 2030.5** — Smart Energy Profile; DER communications and aggregator roles.
- **IS 16444 / IS 15959** — the smart meter and its data model; the same meter that backs all other IES use cases.
- **Beckn Protocol v2** — the discovery / contracting / status lifecycle.
- **DEG schema family** — `DemandFlexNeed`, `DemandFlexBuyOffer`, `DemandFlexPerformance`, plus the shared `EnergyResource`, `DEGContract`, `RevenueFlow`, `BecknTimeSeries`.
- **W3C VC Data Model 2.0** / **W3C DID Core** — issuer keys, signing.
- **SHA-256 (FIPS 180-4)** — cohort digest.
- **JSON-LD 1.1** — wire format and semantic resolution.

## 6. Where Indian Standards Do Not Yet Exist

The procurement protocol (one-to-many discovery, signed binding of a cohort, per-meter M&V back) is an IES choice with no Indian standard predating it. CEA / CERC standards for behind-the-meter flexibility procurement are expected and will inform future versions.

The baseline `methodology` enum (e.g. `5of10`) is currently a free-text field; standardisation is on the roadmap.

## 7. The Records

The DER Flexibility flow produces three distinct kinds of signed artefact:

1. The **need** — `DemandFlexNeed` published in the DISCOM's catalogue.
2. The **contract** — `DEGContract` carrying a `DemandFlexBuyOffer` body, with both buyer and seller bound. The cohort is permanently committed by Beckn signing of this payload.
3. The **per-meter M&V** — `DemandFlexPerformance` delivered as one or more `on_status` callbacks (inline, paged, or off-protocol-ref), each carrying a per-meter `BecknTimeSeries`.

`RevenueFlow` is computed by the settlement policy after M&V finalises and flows through the same `Contract.consideration[0].considerationAttributes` as the other contract-bearing use cases.

## 8. Schedule I — Static Fields

The full, authoritative field tables are in the external schemas:

→ **[External Schemas — Demand Flexibility](../../schemas/external/README.md#demand-flexibility)**

Three primary tables — `DemandFlexNeed`, `DemandFlexBuyOffer` (+ `DemandFlexRoleInput`), `DemandFlexPerformance` — and the shared primitives (`EnergyResource`, `DEGContract`, `RevenueFlow`, `BecknTimeSeries`, `BecknResourceRef`, `BecknPageInfo`).

## 9. Schedule II — Report Templates

The **per-event settlement report** is derived from the signed contract and the assembled per-meter M&V — it is not a separate IES schema. The settlement policy bundle computes `RevenueFlow` over `meters[].telemetry[BASELINE] − meters[].telemetry[USAGE]` (or the reverse for `INCREASE`).

A second derived report is the **programme-level performance summary** — aggregate kWh delivered, % of cohort responding, average per-meter delta — typically computed by the DISCOM for regulatory reporting.

## 10. How It Fits Together

```
DISCOM                          Aggregator (seller)              End consumer / prosumer
──────                          ─────────────                    ──────────────────────

1. publishes ─► DemandFlexNeed
   (catalogue)                  2. discovers, enrols cohort      3. opts-in (consent)
                                   binds meters + EnergyResources
                                3. ───► DemandFlexBuyOffer
                                   (BAP /init, /confirm
                                    — cohort digest committed)
                                                                 4. event fires
                                                                    aggregator dispatches
                                                                    consumer's flex
                                                                    asset(s)
                                5. M&V per meter
                                   DemandFlexPerformance
                                   (on_status — paged inline
                                    or off-protocol bundle)
                                ───►
6. settlement policy
   computes RevenueFlow
   from per-meter delta
   × incentivePerKwh
```

The cohort-digest mechanic (Beckn-signing the `confirm` commits the seller to that exact set of meters) is the trust anchor. Off-protocol bundles can be GC'd or revoked later — the digest in the signed contract still proves what was contracted.

## 11. Points for Confirmation

1. **Baseline methodology enum** — currently free-text; a controlled vocabulary aligned with the SERC's M&V guidance is on the roadmap.
2. **Cohort-size threshold for inline vs ref** — the wave-2 recommendation is "switch to ref above ~10k meters"; the exact threshold per implementation needs to be set.
3. **Consumer consent path** — the wire is the aggregator↔DISCOM contract. The aggregator↔consumer consent layer is out of scope for the schema and being addressed in the consent profile.
4. **Settlement policy bundle** — the Rego rules for computing RevenueFlow under different baseline methodologies are being formalised.
5. **Telemetry granularity** — 15-min is the default; minute-level is possible for fast-DR programmes; pilot data will set the recommendation.

---

## Schemas Used in This Use Case

| Schema | Role |
|---|---|
| **[DemandFlexNeed](https://schema.beckn.io/DemandFlexNeed/)** | DISCOM's catalogue entry — direction, window, capacity, location |
| **[DemandFlexBuyOffer](https://schema.beckn.io/DemandFlexBuyOffer/)** | Aggregator's offer binding a cohort and resources |
| **[DemandFlexPerformance](https://schema.beckn.io/DemandFlexPerformance/)** | Per-meter M&V telemetry |
| **[DEGContract](https://schema.beckn.io/DEGContract/)** | The contract envelope (shared with [P2P Energy Exchange](../p2p-energy-exchange/README.md)) |
| **[BecknTimeSeries](https://schema.beckn.io/BecknTimeSeries/)** | Per-interval telemetry carrier inside `meters[].telemetry` |
| **[EnergyResource](https://schema.beckn.io/EnergyResource/)** | The shared resource model (EV charger, battery, PV, …) |
| **[RevenueFlow](https://schema.beckn.io/RevenueFlow/)** | Settlement-time per-role flows |

A consolidated field reference is in **[External Schemas — Demand Flexibility](../../schemas/external/README.md#demand-flexibility)**.

## Value Unlock

**For DISCOMs** — flex procurement becomes a one-to-many catalogue operation, not a vendor-by-vendor negotiation. M&V is in by construction.

**For aggregators** — one integration; the same `DemandFlexBuyOffer` shape works across DISCOMs that have adopted IES. Large cohorts are first-class through the ref mechanic.

**For consumers / prosumers** — flex participation is settled cryptographically against signed telemetry, not a vendor spreadsheet.

**For regulators** — programme-level performance is computable from signed records; cross-DISCOM comparison becomes possible.

---

## Setup: Register → Discover → Exchange

Built on the four implementation steps in **[How you implement IES](../../how-you-implement-ies/README.md)**. Use-case-specific items only below.

### Register — parties on the network

- [ ] [Identity setup](../../how-you-implement-ies/setup-register.md) complete for your role (DISCOM / aggregator)
- [ ] DeDi subscriber record under the correct namespace
- [ ] (DISCOM) programme identifier convention adopted (e.g. `<DISCOM>-FLEX-<TAG>-<FY>`)

### Discover — flex catalogue

- [ ] [Discovery setup](../../how-you-implement-ies/setup-discovery.md) complete
- [ ] (DISCOM) BPP catalogue entry published per programme — `DemandFlexNeed` with location polygon and event window
- [ ] (Aggregator) BAP discovery tested against the catalogue

### Exchange — offer, contract, M&V

- [ ] [Adapter built](../../how-you-implement-ies/build-adapter.md) for the `DemandFlexNeed` / `DemandFlexBuyOffer` / `DemandFlexPerformance` family
- [ ] (Aggregator) cohort assembly tested — inline for small cohorts, `participatingMetersRef` + `participatingMetersDigest` for large
- [ ] Baseline `methodology` agreed and configured (e.g. `5of10`)
- [ ] Devkit walk-through completed
  - `git clone https://github.com/beckn/DEG.git && cd DEG/devkits/demand-flex/install && docker compose up -d`
- [ ] Per-meter telemetry path tested — paged-inline (`pageInfo`) and off-protocol-ref (`metersRef`) variants
- [ ] Settlement policy bundle URL resolves and signature verifies
- [ ] One full event fired end-to-end — need → offer → confirm → fire → M&V → settlement
- [ ] Runbook in place (key rotation, ref-bundle rotation, dispute handling)

### Team

- [ ] (DISCOM) Operations / planning SPOC
- [ ] (Aggregator) Programme manager
- [ ] (Both) IT / data SPOC
- [ ] (Both) Authorised Signatory

---

## Dev kits and code

- **Devkit** — [`devkits/demand-flex`](https://github.com/beckn/DEG/tree/main/devkits/demand-flex)
- **Implementation guide** — [`docs/implementation-guides/v2/Demand_Flexibility`](https://github.com/beckn/DEG/tree/main/docs/implementation-guides/v2/Demand_Flexibility)
- **External field reference** — [External Schemas — Demand Flexibility](../../schemas/external/README.md#demand-flexibility)

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| OpenADR 3.0 / 3.1 | International demand-flex protocol; informs need-shape and BASELINE / USAGE semantics |
| IEEE 2030.5 | Smart Energy Profile; DER communications / aggregator roles |
| IS 16444 (Parts 1, 2) | AC smart meter — specification |
| IS 15959 (Parts 1–3) | DLMS/COSEM data-exchange companion specification; OBIS codes |
| Beckn Protocol v2 | Discovery, contracting, status, signed audit |
| DEG `DemandFlex*` family | Payload schemas on the wire |
| W3C VC Data Model 2.0; W3C DID Core | Issuer keys; signing |
| SHA-256 (FIPS 180-4) | Cohort digest |
| JSON-LD 1.1 | Wire format and semantic resolution |

## Annexure B — Example Payloads

The demand-flex devkit ships example payloads for every phase:

→ **[`devkits/demand-flex/`](https://github.com/beckn/DEG/tree/main/devkits/demand-flex)**

## Annexure C — JSON Schema

Canonical references at **[schema.beckn.io](https://schema.beckn.io)**:

- **[DemandFlexNeed/v2.0](https://schema.beckn.io/DemandFlexNeed/v2.0)**
- **[DemandFlexBuyOffer/v2.0](https://schema.beckn.io/DemandFlexBuyOffer/v2.0)**
- **[DemandFlexPerformance/v2.0](https://schema.beckn.io/DemandFlexPerformance/v2.0)**
- Shared: **[DEGContract/v2.0](https://schema.beckn.io/DEGContract/v2.0)**, **[BecknTimeSeries/v1.0](https://schema.beckn.io/BecknTimeSeries/v1.0)**, **[EnergyResource/v1.0](https://schema.beckn.io/EnergyResource/v1.0)**

A consolidated field reference for all of the above is in **[External Schemas — Demand Flexibility](../../schemas/external/README.md#demand-flexibility)**.
