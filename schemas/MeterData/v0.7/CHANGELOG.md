# MeterData v0.7 Changelog

> **Status: DRAFT — proposed additive release, under review.** v0.6 remains the current published version until the IES Cell accepts this release.

v0.7 is a **purely additive** release. It extends the `BILL_DETAILS` profile with optional, itemised bill components so that a `BillDetails` record can carry a complete consumer electricity bill — taxes, subsidy, account position, open-access charges, time-of-use billed adjustment, payment terms and coarse location — without any change to the other profiles, the Data Descriptor Engine, `IES codes.json` or the validator.

* No field is renamed, removed, re-typed or re-ordered. Every v0.6 payload validates unchanged against v0.7 (all 25 v0.6 examples are carried forward verbatim and pass).
* Every new field is **optional**. Not every utility bills every component; a field is present only when it appears on the bill. Where an upstream source treats a component as mandatory-but-zero, `0` is a valid value.
* All monetary fields are bare decimals in the record's existing `currency` (ISO 4217), matching `energyCharges` / `fixedCharges` / `otherCharges`. Energy quantities carry a `Kwh` suffix and power a `Kw` suffix, matching `sanctionedLoadKw` / `contractMaxDemandKw`. Dates use `date`; instants use `date-time`.

## What's new in v0.7 (vs v0.6)

### 1. `BillDetails` — new optional fields (flat, alongside the existing charge fields)

| Group | Field | Type | Meaning |
|---|---|---|---|
| Lifecycle | `billVersion` | integer ≥ 1 | Revision of this bill for the same `billNumber`; increments on a revised bill |
| | `billingFrequency` | `BillingFrequency` enum | Cycle class (`DAILY` … `YEARLY`); `timePeriod` still carries the actual dates |
| | `billGeneratedAt` | date-time | When the billing system generated the bill (`billDate` stays the printed date) |
| | `nextBillDate` | date | Expected next bill date |
| Charges | `fppcaCharges` | number | Fuel & power purchase cost adjustment; negative when a credit |
| | `slabRate` | number ≥ 0 | Applicable energy slab rate, `currency` per kWh |
| Taxes & duties | `taxElectricityDuty` | number | Electricity duty |
| | `taxGst` | number | GST charged |
| | `taxTdsTcs` | number | Tax deducted / collected at source shown on the bill |
| Subsidy | `subsidyAmount` | number ≥ 0 | Subsidy credited |
| | `subsidyKwh` | number ≥ 0 | Energy covered by subsidy |
| Totals & account position | `currentBillAmount` | number | Current period total (charges + taxes − subsidy − incentives), before arrears / advance |
| | `arrearsAmount` | number (±) | Carried-forward unpaid (+) or credit (−) |
| | `advancePayment` | number ≥ 0 | Advance adjusted against this bill |
| | `securityDeposit` | number ≥ 0 | Deposit held as at `billDate` |
| | `enforcementAmount` | number ≥ 0 | Assessment / penalty from enforcement action |
| Metering | `assessedKwh` | number ≥ 0 | Energy assessed when the reading could not be used (faulty / tampered) |
| Time of use | `touAdjustmentAmount` | number (±) | Net billed effect of the ToU tariff (the `touBuckets` are readings; this is the money) |
| Open access | `openAccessKwh` | number ≥ 0 | Energy drawn under open access |
| | `openAccessTerm` | `OpenAccessTerm` enum | `LTOA` / `MTOA` / `STOA` |
| | `openAccessContractDemandKw` | number ≥ 0 | Contracted demand under open access |
| | `wheelingCharges`, `crossSubsidySurcharge`, `additionalSurcharge` | number | Open-access charge components |
| Payment terms | `earlyPaymentAmount` / `earlyPaymentDate` | number ≥ 0 / date | Amount if paid by the early date |
| | `latePaymentAmount` | number ≥ 0 | Amount if paid after `dueDate` |
| | `incentiveAmount` | number ≥ 0 | Rebate / incentive credited |
| | `discountExpiryDate` | date | Last date a shown discount can be availed |
| Location | `serviceLocation` | `ServiceLocation` | Coarse, non-PII location for aggregation (see §2) |

Relationship between the totals (documented, not enforced by schema): `amountDue = currentBillAmount + arrearsAmount − advancePayment` (± any early/late adjustment actually applied). Worked in [`examples/BillDetails_Domestic_NetMetered.json`](./examples/BillDetails_Domestic_NetMetered.json).

### 2. New components

* **`BillingFrequency`** (enum): `DAILY | WEEKLY | MONTHLY | BIMONTHLY | QUARTERLY | HALFYEARLY | YEARLY`.
* **`OpenAccessTerm`** (enum): `LTOA | MTOA | STOA`.
* **`ServiceLocation`** (object): `postalCode`, `city`, `district`, `state`, `substation`, `region` — all optional strings. Deliberately has **no street-level fields**; a full address stays on `CustomerProfile.serviceDeliveryPoints[].address` (PII-bearing, omissible).

### 3. Housekeeping (non-normative)

* `info.version` in `attributes.yaml` now reads `0.7.0` (v0.6's still read `0.5.0` — a recorded labelling lag) and `info.description` names the eight profiles + `DESCRIPTOR`.
* Compiled `schema.json`, `context.jsonld`, `vocab.jsonld` regenerated with `scripts/generate_schema_permissive.py`; the diff against v0.6 is additive only (37 new `ies:` terms; `$id` bumped).
* Examples: the 25 v0.6 examples carried forward unchanged (the four bulk examples' embedded `@context` URL bumped to v0.7); three new `BillDetails_*` examples added.
* `IES codes.json`, `validation/` and the user/reference guides are unchanged (guides linked from v0.6 rather than copied).

## Design decisions recorded for review

1. **Geography lives in `BILL_DETAILS.serviceLocation`, not in ElectricityCredential.** Per-bill aggregation is a bill-record concern; keeping it in one schema keeps this a one-release change; the granularity chosen (PIN / city / district / state / substation / region) is non-PII. Note: MeterData's own `CUSTOMER` profile already carries a full `address` and feeder/DT `parentResources`; when both are exchanged the coarse fields MUST agree with them. A future ElectricityCredential release may become the normative slow-changing home, at which point `serviceLocation` becomes informative.
2. **`netBilledAmount` is derived, not stored.** The upstream definition (`arrears + current-period total`) is computable from `arrearsAmount + currentBillAmount`; storing it invites a value that contradicts its components. Recorded in the crosswalk.
3. **`voltageCategory` is mapping guidance, not a field.** ElectricityCredential v1.2 already models voltage via `EnergyResourceNetwork.nominalVoltage` on the DT/feeder; the LT/HT/EHT classification is stated in the crosswalk. Flagged: if the per-bill dashboard needs it without network entries being present, an additive enum on the upstream `MeterServiceProfile` is the follow-up — not a MeterData field.
4. **Grouping follows v0.6's flat style.** `BillDetails` charges are flat (`energyCharges` …), so new monetary fields are flat with grouping prefixes (`tax*`, `openAccess*`, `subsidy*`). `serviceLocation` is the one nested value object, mirroring how `address` / `geo` are value objects on `ServiceDeliveryPoint`.
5. **Optionality.** All new fields optional (see top). Upstream "mandatory" components are usually mandatory-with-zero; the IES contract is "present when on the bill".
6. **Names that differ from the upstream field dictionary** — chosen for repo convention or precision, mapped in the crosswalk: `billPeriod → billingFrequency` (avoids clash with `timePeriod`), `todAmount → touAdjustmentAmount` (repo uses ToU; it is the billed effect, not a reading), `*Units → *Kwh` (unit-suffix convention), `contractDemand → openAccessContractDemandKw`, `billGenerationTs → billGeneratedAt`, `totalEnergyCharge → currentBillAmount`, `meterBalance → prepaidBalance` (already existed in v0.6), `assesedUnits → assessedKwh` (spelling corrected).
7. **Slow-changing facts carried per bill.** `openAccessTerm`, `openAccessContractDemandKw` and `securityDeposit` are contract/account terms rather than cycle facts. They are carried here because ElectricityCredential v1.2 has no open-access or deposit model (so nothing is duplicated); flagged as candidates for a future ElectricityCredential/MeterServiceProfile release.

## Follow-ups (out of this release)

* `MeterDataCredential` v0.7: bump the `credentialSubject.meterData` `$ref` from MeterData v0.6 to v0.7 on acceptance (the v0.6 wrapper already validates a v0.7 payload; only the pinned reference changes).
* Whether `paymentStatus` should become an enum — untouched here (would be a v0.6-behaviour change).
