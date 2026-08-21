# Crosswalk — BBPS Bill Post API v1.3 → IES (MeterData v0.7 · MeterDataCredential · ElectricityCredential v1.2)

> **Draft, for review.** Field inventory transcribed from the BBPS Bill Post v1.3 data dictionary as presented at the 12 Aug 2026 NPCI/REC review; rows marked **verify** should be re-checked against the v1.3 PDF before this crosswalk is treated as normative. This document is informative; the schemas are normative.

**Which record carries what.** One **ElectricityCredential** (Consumer Energy Passport, v1.2) per meter carries the slow-changing connection facts. One **MeterDataCredential** per billing cycle wraps a **MeterData v0.7** payload — a `BILL_DETAILS` profile (optionally with a `MONTHLY` profile) — carrying the per-bill facts. Slow-changing facts are never repeated in MeterData; the two are joined on the consumer / meter identifier.

Legend — **Credential**: EC = ElectricityCredential v1.2 · MD = MeterData v0.7 (`BillDetails` unless stated) · MDC = MeterDataCredential envelope. **Status**: Match = existed in v0.6 · **New** = added in v0.7 · Derived = not stored · Guidance = mapping rule only.

## A. Envelope, identity, dates, headline amounts

| BBPS field | IES path | Credential | Status | Transform / note |
|---|---|---|---|---|
| `head.origInst` / `billerDetails.billerId` | `issuer.id` (did:web) | MDC | Match | Issuer DID + `issuer.licenseNumber` |
| `customerIdentifiers[CA Number]` | `customerRefs[]{scheme: CONSUMER_NUMBER}` | MD | Match | Also `credentialSubject.id` DID on the MDC |
| `billNumber` | `billNumber` | MD | Match | |
| `billVersion` | `billVersion` | MD | **New** | integer ≥ 1; increments on BILL_UPDATE |
| `billDate` | `billDate` | MD | Match | date |
| `billGenerationTs` | `billGeneratedAt` | MD | **New** | date-time |
| `billPeriod` (enum) | `billingFrequency` | MD | **New** | same enum values; `timePeriod{start,duration}` carries the actual span |
| `dueDate` | `dueDate` | MD | Match | |
| `nextBillDate` | `nextBillDate` | MD | **New** | |
| `currency` | `currency` | MD | Match | ISO 4217 |
| `dueAmount` | `amountDue` | MD | Match | |
| `netBilledAmount` | — | MD | Derived | `= arrearsAmount + currentBillAmount`; not stored (Decision 2) |
| `totalEnergyCharge` | `currentBillAmount` | MD | **New** | mapped on the basis of the BBPS derivation `netBilledAmount = arrears + totalEnergyCharge`; **verify** that it includes taxes/duties |
| `paymentStatus` | `paymentStatus` | MD | Match | free text in v0.6/v0.7 |
| `advancePayment` | `advancePayment` | MD | **New** | |
| `meterBalance` (prepaid) | `prepaidBalance` | MD | Match | v0.6 field; absent for postpaid |

## B. Charges

| BBPS field | IES path | Credential | Status | Note |
|---|---|---|---|---|
| `energyCharge` | `energyCharges` | MD | Match | |
| `fixedCharge` | `fixedCharges` | MD | Match | |
| `fppcaCharge` | `fppcaCharges` | MD | **New** | negative = credit |
| `otherCharges` | `otherCharges` | MD | Match | |
| `slabRate` | `slabRate` | MD | **New** | `currency` per kWh |

## C. Taxes, duties, subsidy

| BBPS field | IES path | Status | Note |
|---|---|---|---|
| `electricityDuty` | `taxElectricityDuty` | **New** | |
| `GST` | `taxGst` | **New** | |
| `TDS/TCS` | `taxTdsTcs` | **New** | |
| `subsidyAmount` | `subsidyAmount` | **New** | 0 when N/A |
| `subsidyUnits` | `subsidyKwh` | **New** | kWh |

## D. Account position

| BBPS field | IES path | Status | Note |
|---|---|---|---|
| `arrearsAmount` | `arrearsAmount` | **New** | ± |
| `securityDeposit` | `securityDeposit` | **New** | as at `billDate` |
| `enforcementAmount` | `enforcementAmount` | **New** | |

## E. Consumption and metering

| BBPS field | IES path | Credential | Status | Note |
|---|---|---|---|---|
| `consumption.units` | `readings[]{readingType: "kWh imp", reportedMode USAGE}.value` | MD | Match | descriptor set declares USAGE; `openingValue`/`closingValue` give the proof |
| `assesedUnits` (sic) | `assessedKwh` | MD | **New** | spelling corrected in IES; alias recorded here |
| `meterType` | `Meter.meterType` (MD `CUSTOMER`) / `EnergyResourceMeter.attributes.meterCapability` | MD / EC | Match | |
| `meterStatus` | `readings[].validationStatus` (`ESTIMATED`) + `assessedKwh` for faulty/tampered; connection state → EC `ConsumptionProfile.serviceStatus` | MD / EC | Guidance | **verify** BBPS semantics (device health vs connection status) |
| `sanctionedLoad` | EC `ConsumptionProfile.sanctionedLoad{value,unit}` (also MD `Customer.sanctionedLoadKw`) | EC | Match | |
| `timeOfDay.todAmount` | `touAdjustmentAmount` | MD | **New** | ± ; ToU *readings* stay in `touBuckets` |
| ToU consumption by zone | `touBuckets[]{zone, readings}` | MD | Match | |

## F. Connection and supply (slow-changing — ElectricityCredential)

| BBPS field | IES path | Status | Note |
|---|---|---|---|
| `connectionDetails.tariffCategory` | EC `ConsumptionProfile.tariffCategoryCode` | Match | |
| `connectionDetails.billType` | EC `ConsumptionProfile.paymentMode` (`PREPAID`/`POSTPAID`) | Match | **verify** BBPS enum |
| `typeOfSupply` | EC `ConsumptionProfile.premisesType` / `tariffCategoryCode` | Match | **verify** |
| `connectionDetails.voltageCategory` (LT/HT/EHT) | derived from EC `EnergyResourceNetwork.attributes.nominalVoltage` on the meter's parent DT/feeder | Guidance | LT: ≤ 1 kV · HT: > 1 kV and ≤ 33 kV · EHT: > 33 kV (CEA supply-code convention; **confirm thresholds with the applicable State supply code**). Fallback: the utility's `tariffCategoryCode` usually encodes LT/HT (Decision 3) |
| `distributedEnergyResource.source` | EC `energyResources[].type` (`SOLAR_PV`, `WIND`, `BESS` …) | Match | |
| `distributedEnergyResource.importUnits` / `exportUnits` | MD `readings[]` `kWh imp` / `kWh exp` (USAGE) | Match | `flowDirection` on the descriptor |
| Connection type (1φ/3φ) | EC `ConsumptionProfile.connectionType` | Match | |

## G. Open access

| BBPS field | IES path | Status |
|---|---|---|
| `openAccess.units` | `openAccessKwh` | **New** |
| `openAccess.term` (LTOA/MTOA/STOA) | `openAccessTerm` | **New** |
| `openAccess.contractDemand` | `openAccessContractDemandKw` | **New** |
| `openAccess.wheelingCharge` | `wheelingCharges` | **New** |
| `openAccess.crossSubsidySurcharge` | `crossSubsidySurcharge` | **New** |
| `openAccess.additionalSurcharge` | `additionalSurcharge` | **New** |

## H. Payment options

| BBPS field | IES path | Status | Note |
|---|---|---|---|
| `earlyPaymentAmount` | `earlyPaymentAmount` | **New** | |
| `earlyPaymentDate` | `earlyPaymentDate` | **New** | BBPS date-time → IES `date` (truncate to the bill's local calendar date) |
| `latePaymentAmount` | `latePaymentAmount` | **New** | |
| `incentiveAmount` | `incentiveAmount` | **New** | |
| `discountExpiryDate` | `discountExpiryDate` | **New** | date-time → `date`, as above |

## I. Geography (dashboard aggregation)

| BBPS field | IES path | Status | Note |
|---|---|---|---|
| `pincode` | `serviceLocation.postalCode` | **New** | |
| `city` | `serviceLocation.city` | **New** | |
| `district` | `serviceLocation.district` | **New** | |
| `state` | `serviceLocation.state` | **New** | |
| `supplyLocation.substation` | `serviceLocation.substation` | **New** | EC `EnergyResourceNetwork.attributes.substationId` is the network-side equivalent |
| `supplyLocation.region` | `serviceLocation.region` | **New** | EC `…zone` is the network-side equivalent |

No street-level address is carried in `BILL_DETAILS` (Decision 1). PII, where needed at all, stays in `CustomerProfile.customerDetails` / EC `customerDetails`.

## Not mapped (out of scope of the schema)

Transport / protocol items — batch id, file id, sequence, record count, checksum, JWS — belong to the exchange envelope (`payloadHash`, `SIGNED_URL`, receipt) and the MDC `proof`, not to MeterData. Record-level rejection format is a separate pilot-scoping item.
