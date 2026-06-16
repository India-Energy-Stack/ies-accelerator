# Smart Meter Data Exchange

**A standard, audit-trailed way to exchange smart-meter telemetry between an AMISP, a DISCOM, a state regulator, and consented third parties — over [IES Data Exchange](../../data-exchange/README.md), carrying the [MeterData](../../schemas/MeterData/README.md) payload (currently `v0.6`).**

You replace bespoke FTP drops, proprietary MDMS APIs, and CSV email attachments with one signed, schema-validated flow. The same surface area works AMISP→DISCOM, DISCOM→SERC, and DISCOM→consented-third-party.

> For consumer-pull of *their own* meter data (one-meter, on-demand, wallet-shareable), see [Consumer Meter Digest](../consumer-meter-digest/README.md). This guide is the bulk, scheduled, machine-to-machine flow.

---

## Building blocks used

This use case is a thin composition over four existing building blocks. The setup steps below map one-to-one to them — read the building-block pages for the detail; come back here for what changes for the meter-data case.

| What you need | Building block | What it gives you |
|---|---|---|
| A name and a signing key your counterparties can verify | [Identifiers & Addressing](../../identifiers/README.md), [Registries](../../registries/README.md) | Your `did:web`, your public key in a DeDi runtime, your namespace |
| A trust boundary — "who can transact on this network" | [Required Registries — Network Reference Registry](../../registries/required-registries.md#network-reference-registry) | Your subscriber record in the IES network reference registry |
| The transport that carries discovery, contract, audit, and the payload | [Data Exchange](../../data-exchange/README.md) | The Beckn lifecycle + ONIX adapter; the same `accessMethod` covers inline payloads and signed-URL handoff |
| (Optional) Cryptographic proof that the requester is authorised | [MeterDataRequestCredential](../../schemas/MeterDataRequestCredential/README.md) | A signed credential the seeker attaches at `confirm`; provider verifies offline |

---

## The dataset — `MeterData/v0.6`

The payload is the [MeterData](../../schemas/MeterData/README.md) compact-profile schema (currently `v0.6`). v0.6 standardises eight profile shapes covering every smart-meter cadence:

| Profile | Carries |
|---|---|
| `CUSTOMER` | Slow-changing customer / service-point / meter installation metadata |
| `INTERVAL` | Block load survey at 15- or 30-minute resolution |
| `DAILY` | Daily accumulated load survey |
| `MONTHLY` | Monthly billing resets (cumulative kWh, ToU buckets, MD) |
| `BILL_DETAILS` | Utility-side billing computed details |
| `INSTANTANEOUS` | Real-time snapshot of V / A / P / Q |
| `EVENT` | IS 15959 diagnostic / tamper events |
| `ALARM` | Real-time active alerts |

For the Indian-terminology mapping (OBIS codes, IS 15959 event IDs, CIM master-data fields) see the companion page [IES Meter Data Model](./ies-meter-data-model.md).

> **MeterData v0.6 supersedes the earlier `IES_Report` working name.** Any older docs or devkits referencing `IES_Report` should be read as `MeterData/v0.6`.

---

## Optional consent — `MeterDataRequestCredential`

When a third party (a consented app, a researcher, sometimes a regulator) is the BAP, the provider's offer policy can require an authorisation credential at `confirm` time. IES uses [`MeterDataRequestCredential`](../../schemas/MeterDataRequestCredential/README.md) — a W3C VC 2.0 that wraps a [`MeterDataRequest`](../../schemas/MeterDataRequest/README.md) and identifies the requester, scopes the request (which meters, which time window, which profile), and is signed by the authoriser (typically the DISCOM, sometimes the consumer themselves via OpenCred).

```
Seeker (BAP)                                       Provider (BPP)
e.g. consented app, SERC                           e.g. AMISP, DISCOM

  │── confirm  ─── { MeterDataRequest } ───
  │                + MeterDataRequestCredential ──>│
  │                                                ├─ verify VC: type ✓
  │                                                │            validUntil ✓
  │                                                │            DeDi status ✓
  │                                                │            scope ⊆ contract
  │<── on_confirm / on_status — MeterData/v0.6 ────│
```

The provider checks credential type, expiry, DeDi revocation status, and that the embedded request scope is within the contracted scope — no callback to the issuer.

---

## Setup steps

The order below takes you from zero to a working AMISP → DISCOM flow on the local devkit, then upgrades to the real IES network.

### 1. Decide scope

Meter population, geography, granularity (15-min / daily / monthly), counterparties (AMISP→DISCOM only, DISCOM→SERC, DISCOM→third-party). Phase 1 should be one cadence and one counterparty.

### 2. Get a network identity

Both BAP and BPP need a DeDi subscriber record with a published signing key. If you have one already (any other Beckn flow on this network), reuse it. If not, follow [Required Registries — minimum to get started](../../registries/required-registries.md#onboarding-quick-guide-minimum-to-get-started).

You do **not** need to rename anything in your CIS, MDMS, or asset registers. Your existing IDs are reused as the tail of the DID.

### 3. Stand up the Data Exchange adapters

Both sides run an [ONIX](../../glossary.md#onix) adapter. The fastest start is the devkit sandbox:

```bash
git clone https://github.com/beckn/DEG.git
cd DEG/devkits/data-exchange/install
docker compose up -d
```

This brings up `sandbox-bap`, `sandbox-bpp`, and `beckn-router` pre-wired with placeholder identities. End-to-end network onboarding is the [Data Exchange — Onboarding Checklist](../../checklists/data-exchange-checklist.md); don't duplicate the steps here — read that page.

### 4. Publish your dataset catalogue (BPP)

Publish a Beckn catalogue entry for the `MeterData/v0.6` dataset you offer — `programID`, geographic scope, refresh cadence, [`accessMethod`](../../data-exchange/concepts.md#the-datasetitem-schema) (`INLINE` for ≤MB-scale chunks; `SIGNED_URL` for daily/monthly bulk), and any required credentials (point at `MeterDataRequestCredential` if you require one). Pre-agreed bilateral subscriptions can skip `discover` and go straight to `confirm`.

### 5. Exercise the flow

The minimal lifecycle is `confirm` → `on_confirm` → (`status` → `on_status` if delivery is asynchronous):

| Step | Sender | What happens |
|---|---|---|
| `confirm` | BAP | Requests data for a meter list + date range. Optionally attaches a `MeterDataRequestCredential`. |
| `on_confirm` | BPP | Acknowledges; declares whether delivery is inline or async. |
| `on_status` | BPP | Delivers `MeterData/v0.6` inline or returns a signed-URL pointer. |

The payload sits inside `message.contract.commitments[].resources[].resourceAttributes` qualified with the DDM `DatasetItem/v1.1` context — see [Data Exchange — Core Concepts](../../data-exchange/concepts.md#the-datasetitem-schema).

### 6. Connect your real metering system

Replace the sandbox response with a live connection to your HES / MDMS. Verify the Indian-OBIS → `MeterData/v0.6` mapping for every reading you ship — [IES Meter Data Model](./ies-meter-data-model.md) is the reference.

### 7. (Optional, at the end) Issue stable IDs for every meter and asset

Once Phase 1 is flowing, you can mint stable DIDs for each meter, DT, feeder, and substation referenced in the exchange. **Your existing CA numbers and meter SLNOs work as-is** — the DID is just `did:dedi:<your-namespace>:meters:<meter-serial>` (and the same pattern for DT, feeder, substation). See [Identifiers → ID Patterns](../../identifiers/id-patterns.md). This step is *nice to have*, not a blocker for first deployment — initial flows can use bare IDs inside `MeterData/v0.6` payloads and add DIDs incrementally.

---

## Checklist for your meter-data rollout

For the **underlying network onboarding** (DeDi subscriber, ONIX, signing keys, sandbox→test→prod cut-over), follow the canonical [Data Exchange — Onboarding Checklist](../../checklists/data-exchange-checklist.md). Don't duplicate those items here.

The items below are **meter-data-specific** additions on top of that checklist:

- [ ] Meter population, geography, granularity, and counterparty for Phase 1 agreed
- [ ] Source system mapped (HES / MDMS endpoint, owner team, SLA)
- [ ] Indian-OBIS → `MeterData/v0.6` mapping verified for every reading and event you ship (see [IES Meter Data Model](./ies-meter-data-model.md))
- [ ] Data-quality flags (missing / estimated) handled per the v0.6 `validationStatus` enum
- [ ] Catalogue entry published (`programID`, geographic scope, refresh cadence, `accessMethod`, credential requirements)
- [ ] (If third-party access in scope) `MeterDataRequestCredential` verification wired into the BPP — type, validity, DeDi status, scope ⊆ contract
- [ ] (Optional) Stable DIDs minted for meters / DTs / feeders, reusing existing internal numbers
- [ ] IT/data SPOC nominated; Authorised Signatory nominated

---

## Open items

- **Chunking convention** for bulk historical pulls (daily / monthly / quarterly) is being agreed across deployments.
- **Quality flags** — the v0.6 `validationStatus` enum is stable; the recommended profile of allowed values per cadence is being tightened.

---

## References

- [MeterData — schema and examples](../../schemas/MeterData/README.md) (current: `v0.6`)
- [MeterDataRequest — request payload schema](../../schemas/MeterDataRequest/README.md) (current: `v0.6`)
- [MeterDataRequestCredential — authorisation VC](../../schemas/MeterDataRequestCredential/README.md) (current: `v0.1`)
- [IES Meter Data Model](./ies-meter-data-model.md) — OBIS / IS 15959 / CIM → MeterData v0.6 mapping
- [Data Exchange chapter](../../data-exchange/README.md)
- [Data Exchange — Onboarding Checklist](../../checklists/data-exchange-checklist.md)
- [Registries — Required for onboarding](../../registries/required-registries.md)
- [Identifiers — ID Patterns](../../identifiers/id-patterns.md)
