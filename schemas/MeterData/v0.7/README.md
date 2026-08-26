> **Files** — [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.7/attributes.yaml) · [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.7/schema.json) · [context.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.7/context.jsonld) · [vocab.jsonld](https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.7/vocab.jsonld) · [examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterData/v0.7/examples)

# Meter Data Compact Profiles (v0.7)

> ⚠️ **DRAFT — proposed additive release, under review.** v0.7 adds optional itemised bill components to the `BILL_DETAILS` profile and changes nothing else. Every v0.6 payload is a valid v0.7 payload. Until accepted by the IES Cell, **v0.6 remains the current published version**; do not pin v0.7 in production integrations. See [CHANGELOG.md](./CHANGELOG.md), [PROPOSAL.md](./PROPOSAL.md) and the [BBPS Bill Post v1.3 crosswalk](./CROSSWALK_BBPS_BILLPOST_V1.3.md).

This directory contains the **Meter Data Compact Profiles** (v0.7) schema definitions and semantic models for telemetry data exchange. It is tailored for high-efficiency, data-only transmissions of smart meter readings and events, omitting heavy cryptographic wrapping when only raw telemetry payload is being exchanged.

The `MeterData` schema standardizes telemetry exchanges into **eight compact profile shapes** representing different read cadences and data structures from smart meters:

1. **`CUSTOMER`** — Slow-changing customer metadata, service points, and meter installations.
2. **`INTERVAL`** — Block load survey profile at high-resolution intervals (e.g., 15-minute or 30-minute blocks).
3. **`DAILY`** — Daily accumulated load survey profiles.
4. **`MONTHLY`** — Monthly billing resets (billing history cumulative total energy registers, ToU buckets, and Maximum Demand).
5. **`BILL_DETAILS`** — Utility billing computed details (billing amount, bill number, due dates, currency, prepaid balance, and payment status). **v0.7** adds optional itemised components: taxes and duties, subsidy, arrears / advance / security deposit, open-access charges, time-of-use billed adjustment, early/late-payment terms, bill version and cycle, and a coarse non-PII `serviceLocation` for aggregation.
6. **`INSTANTANEOUS`** — Real-time snapshots of electrical quantities (voltages, currents, active/reactive powers) at a specific moment.
7. **`EVENT`** — Event logs matching standard IS 15959 diagnostic codes and tamper events.
8. **`ALARM`** — Real-time active alerts representing immediate state conditions (tamper, low prepayment credit, voltage sag, overload) from the meter.

---

## Directory Structure and Files

| File | Description |
|------|-------------|
| [`attributes.yaml`](./attributes.yaml) | Canonical OpenAPI schema source of truth, describing all attributes, models, and types. |
| [`schema.json`](./schema.json) | Compiled Draft 2020-12 JSON Schema for standard validation of data payloads. |
| [`context.jsonld`](./context.jsonld) | Compiled JSON-LD context mapping telemetry attributes to semantic terms under `ies:` or `schema:` namespaces. |
| [`vocab.jsonld`](./vocab.jsonld) | Compiled JSON-LD vocabulary (ontology graph) defining all classes and properties. |
| [`IES codes.json`](./IES%20codes.json) | Canonical registry of OBIS and Short Codes mapping physical quantities to units, categories, and categories of meters. |
| [`examples/`](./examples) | Standard, JSON-LD augmented telemetry payload example files for all profile types. |

### Documentation Guides
* [User Guide](../v0.6/UserGuide.md) *(unchanged from v0.6)*: Detailed guidelines on HES, MDM, and Billing system interactions, advertising system capabilities via request mechanisms, and verification scenarios.
* [Reference Guide](../v0.6/ReferenceGuide.md) *(unchanged from v0.6)*: Top-down reference documentation detailing different profile roles, centralised codes, and telemetry vs. non-telemetry handling.

---

## Data Descriptor Engine & The Array Envelope

In v0.6, the telemetry architecture uses an optimized, strict inheritance structure powered by the **Data Descriptor Engine**. 

Instead of transmitting bulky metadata inline with every physical reading, telemetry can be wrapped in a **JSON Array**.

### Centralized `PayloadDescriptorProfile`
A JSON array payload can contain one or more `PayloadDescriptorProfile` objects. This serves as the dictionary for all compact profiles inside the payload array:
* **`payloadDescriptors`**: Defines the metadata for specific registers (e.g., `readingType`, `unit`, `flowDirection`, `category`, and `multiplier`).
* **`compactSequences`**: Defines the physical column layout of the dense numerical payload matrices.

### Dynamic `SequenceItem` Columns (`attribute`)
A sequence defines what each column in the `payloads` array represents using the **`attribute`** property:
* `value`: The actual meter reading number.
* `occurredAt`: The timestamp string representing exactly when a specific demand or reading occurred.
* `openingValue` / `closingValue`: To provide mathematical proofs for `USAGE` deltas.
* `validationStatus`: Standard validation flags (e.g. `ESTIMATED`, `VALID`).

Because `payloads` allows mixed arrays of `number` and `string`, metadata is mapped densely alongside values, while sparse overrides are used for quality indications (such as validation status or fail codes in specific intervals).

### Strict Derived Profiles
Inside the array, individual profiles inherit strictly from `BaseProfile`. `BaseProfile` only contains identity (`meterRefs`, `customerRefs`, `serviceDeliveryPointRefs`). Derived profiles (like `IntervalProfile`) strictly allow **only** their relevant properties (`intervals`, `payloadDescriptorSetRef`, `intervalPeriod`).

> [!NOTE]
> ### Rationale for MonthlyProfile not using the compact matrix
> The compact form is prevented natively by the schema for `MonthlyProfile`. It strictly requires `readings` and `touBuckets`, and does not permit `intervals`. The compact matrix is designed for dense, highly symmetrical time-series data. A `MonthlyProfile` typically captures a single sparse snapshot of total registers, ToU buckets, and Maximum Demand peaks at the end of the month. Encoding sparse, highly variable metadata (e.g., MD timestamps) into a flat numerical array offers negligible compression and becomes extremely brittle when dealing with ad-hoc billing resets or meter swaps mid-cycle.
> 
> *See [MonthlyProfile_MultipleResets.json](./examples/MonthlyProfile_MultipleResets.json) and [Billing_MeterChange.json](./examples/Billing_MeterChange.json) for examples of how the elaborated representation cleanly handles these edge cases.*

---

## Identifier Flexibility (OBIS vs. Short Codes)

The schema relies on [`IES codes.json`](./IES%20codes.json) as the canonical registry for interpreting physical quantities. The exact mapping of OBIS codes to physical units, phases, and categories is defined in this file.

When transmitting telemetry, you specify a simple **`readingType`** string. This can be:
* **Using OBIS Codes**: `"1.0.1.8.0.255"`
* **Using Short Names**: `"kWh imp"`
* **Using Canonical Links**: Payload descriptors can optionally include an `obis` string parameter to provide a direct physical mapping when a short name is used as the `readingType`.

*See the [MultiMeterBulkDataset.json](./examples/MultiMeterBulkDataset.json) (OBIS Codes) and [MultiMeterBulkDatasetShortCodes.json](./examples/MultiMeterBulkDatasetShortCodes.json) (Short Codes) for bulk examples of both representations.*

---

## TelemetryMode (READING vs USAGE)

The schema natively distinguishes between raw register readings and calculated usage:
- **`READING`**: Represents the physical register value at a point in time. For cumulative registers, this strictly increases dynamically.
- **`USAGE`**: Represents the delta or consumed amount over a period. Demand registers inherently use `USAGE` mode. For energy, this represents the exact block consumption.

Modes are indicated inside the payload descriptor only via the `reportedMode` property.

---

## Schema Generation and Compilation

The `schema.json`, `context.jsonld`, and `vocab.jsonld` files are compiled automatically from the core `attributes.yaml`.

### To Compile Schemas
To recompile schemas following modifications in `attributes.yaml`, run the following python scripts from the repository root:

```bash
python scripts/generate_schema_permissive.py schemas/MeterData/v0.6
```

---

## Examples

These examples cover a wide variety of scenarios, organized by the system they typically originate from:

### MDM (Meter Data Management) Examples
MDM datasets are meter-centric and intentionally omit `customerRefs` to decouple the technical metering domain from the commercial billing domain.
* [`IntervalProfile.json`](./examples/IntervalProfile.json): Block load survey.
* [`DailyProfile.json`](./examples/DailyProfile.json): Daily midnight snapshots.
* [`MDM_MonthlyProfile.json`](./examples/MDM_MonthlyProfile.json): End of billing cycle snapshots across multiple meters.
* [`InstantaneousProfile.json`](./examples/InstantaneousProfile.json): Snapshot of voltage, current, power factor, etc.
* [`EventProfile.json`](./examples/EventProfile.json): Meter tampers, diagnostics, power outages.
* [`AlarmProfile.json`](./examples/AlarmProfile.json): Critical thresholds being crossed.
* [`MultiMeterBulkDataset.json`](./examples/MultiMeterBulkDataset.json): Large scale transmission of intervals across many meters.

### CIS / Billing Examples
Billing and CIS examples enrich technical meter data with `customerRefs`, Tou buckets, and monetary calculations.
* [`Billing_MonthlyProfile.json`](./examples/Billing_MonthlyProfile.json): Usage-centric monthly consumption linked to consumers.
* [`CustomerProfile.json`](./examples/CustomerProfile.json): Linking meters, service delivery points, and customers.
* [`BillDetails.json`](./examples/BillDetails.json): Computed monetary bill with due dates and calculated consumption.
* [`BillDetails_Domestic_NetMetered.json`](./examples/BillDetails_Domestic_NetMetered.json) **(v0.7)**: Domestic net-metered ToU consumer — itemised taxes, subsidy, arrears/advance, early/late-payment terms, `serviceLocation`.
* [`BillDetails_OpenAccess_HT.json`](./examples/BillDetails_OpenAccess_HT.json) **(v0.7)**: HT industrial open-access consumer — wheeling / cross-subsidy / additional surcharge, contract demand, assessed units, revised bill (`billVersion: 2`).
* [`BillDetails_Prepaid.json`](./examples/BillDetails_Prepaid.json) **(v0.7)**: Prepaid daily settlement bill against `prepaidBalance`.
* [`CustomerBillingSummary.json`](./examples/CustomerBillingSummary.json): Historic billing trends for a consumer dashboard.

Support data used by the example-generation utility is deliberately kept out
of the schema-validated payload directory:

* [`support/CustomerMapping.json`](./support/CustomerMapping.json): illustrative mapping of meter serial numbers to commercial customer accounts used by `scripts/generate_billing_from_mdm.py`; it is not a `MeterData` payload.

### Highlighted Examples
* **Meter Swap Mid-Cycle**: [`Billing_MeterChange.json`](./examples/Billing_MeterChange.json) demonstrates how to handle a meter replacement in the middle of a billing period by chaining multiple monthly profiles under different meter serials.
* **Multiple Monthly Resets**: [`MonthlyProfile_MultipleResets.json`](./examples/MonthlyProfile_MultipleResets.json) demonstrates how to represent multiple billing resets triggered in the same calendar month.
* **Itemised Bill (v0.7)**: [`BillDetails_Domestic_NetMetered.json`](./examples/BillDetails_Domestic_NetMetered.json) shows how `currentBillAmount`, `arrearsAmount`, `advancePayment` and `amountDue` relate (`amountDue = currentBillAmount + arrearsAmount − advancePayment`), with every v0.7 field populated except the open-access group (see the HT example).
* **Identifier Representation Comparison**: Compare [`MultiMeterBulkDataset.json`](./examples/MultiMeterBulkDataset.json) (using raw OBIS codes) with [`MultiMeterBulkDatasetShortCodes.json`](./examples/MultiMeterBulkDatasetShortCodes.json) (using Short Names) to see how the payload descriptor engine abstracts identifier models.

---

## Telemetry Verification & Validation

The validator is not limited to example files; it can be used to validate any `MeterData` payload. In this repository, all example JSON files are validated for structural compliance against `schema.json` and semantic compliance against `IES codes.json` using the v0.6 validator.

### To Validate Payloads
Run the following command from the `validation/` directory:

```bash
python validator.py <path_to_json_file_or_directory>
```

The validator dynamically parses JSON files. If they are arrays containing a `PayloadDescriptorProfile`, it matches `payloadDescriptorSetRef` against the array's descriptors, and asserts both matrix arity and strict column types based on the `attribute` enum.

---

## Overlaps and Differences with ElectricityCredential

- **`meterType` vs `meterCategory`**:
  - `meterType` describes the physical communication/technology capability of the meter (e.g. `AMI`, `AMR`, `Prepaid`, `NetMeter`).
  - `meterCategory` describes the regulatory standards category under IS 15959 (e.g. `A`, `B`, `C`, `D1`–`D4`).
  - These represent distinct aspects of the physical/standard classification, and both are kept.
- **`premisesType` vs `consumerCategory`**:
  - `premisesType` (Residential, Commercial, etc. defined in `ElectricityCredential/v1.2`) classifies the physical type of the premises.
  - `consumerCategory` (LT2A, NDS, HT, etc. defined in `MeterData/v0.6`) represents the utility-specific tariff category.
  - To prevent duplication and maintain backwards compatibility, the pre-existing `consumerCategory` property was kept, and `premisesType` was excluded. This overlap is marked here for future reconciliation.
- **`energyResources` vs `meters`/`associations` (Export & Storage modeling)**:
  - `ElectricityCredential v1.2` models all physical assets (meters, solar PV arrays, battery storage) using a unified `energyResources` list of typed `EnergyResource` objects. This allows rich modeling of child DER/storage assets (`SOLAR_PV`, `BESS`) directly detailing attributes like `ratedPower` and `storageCapacity` — each a QuantitativeValue `{value, unit}` pair — linked via topology references.
  - `MeterData v0.6` retains a lightweight representation focusing strictly on billing/metering associations, lacking top-level asset representations. To bridge this gap for grid planners, three lightweight properties were introduced in `v0.6`:
    - **`sanctionedExportLoadKw`** (on the `Customer` schema) to explicitly specify approved net-metering solar export limits.
    - **`generationCapacityKw`** (on the `Association` schema) to denote the rated solar/generation inverter capacity connected.
    - **`storageCapacityKw`** (on the `Association` schema) to denote the connected battery storage energy capacity in kWh.
  - This structural divergence is documented here for future alignment in subsequent major version releases.


---

<!-- FIELD-TABLE:START — auto-generated by scripts/generate_field_tables.py from schema.json; do not edit by hand -->
## Field reference

_Auto-generated from `schema.json`. A field name in **bold** with a trailing **\*** is required; all others are optional. **Type** shows units for QuantitativeValue models. Where a field is derived from a standard, its description begins with **Based on** and the standard reference (from the field's `x-standard` annotation). One table per object._

### CustomerProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`profileType`** \* | text | — |
| `customerRefs` | IdentifierList | — |
| `timeZone` | text | IANA time-zone, e.g. Asia/Kolkata. |
| `customerDetails` | CustomerDetails | — |
| **`customer`** \* | Customer | — |
| **`serviceDeliveryPoints`** \* | list of ServiceDeliveryPoint | — |
| **`meters`** \* | list of Meter | — |
| **`associations`** \* | list of Association | — |

### BaseProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`profileType`** \* | text | — |
| `customerRefs` | IdentifierList | — |
| **`meterRefs`** \* | IdentifierList | — |
| `serviceDeliveryPointRefs` | IdentifierList | — |
| `payloadDescriptorSetRef` | text | Reference ID matching a previously exchanged PayloadDescriptorProfile's payloadDescriptorSet. |

### IntervalProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`profileType`** \* | text | — |
| `customerRefs` | IdentifierList | — |
| **`meterRefs`** \* | IdentifierList | — |
| `serviceDeliveryPointRefs` | IdentifierList | — |
| `payloadDescriptorSetRef` | text | Reference ID matching a previously exchanged PayloadDescriptorProfile's payloadDescriptorSet. |
| `compactSequenceRef` | text | Name of the compact sequence to use from the payloadDescriptorSets. |
| **`intervalPeriod`** \* | IntervalPeriod | — |
| `intervals` | list of Interval | — |
| `readings` | list of Reading | — |

### DailyProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`profileType`** \* | text | — |
| `customerRefs` | IdentifierList | — |
| **`meterRefs`** \* | IdentifierList | — |
| `serviceDeliveryPointRefs` | IdentifierList | — |
| `payloadDescriptorSetRef` | text | Reference ID matching a previously exchanged PayloadDescriptorProfile's payloadDescriptorSet. |
| `compactSequenceRef` | text | Name of the compact sequence to use from the payloadDescriptorSets. |
| **`intervalPeriod`** \* | IntervalPeriod | — |
| `intervals` | list of Interval | — |
| `readings` | list of Reading | — |

### MonthlyProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`profileType`** \* | text | — |
| `customerRefs` | IdentifierList | — |
| **`meterRefs`** \* | IdentifierList | — |
| `serviceDeliveryPointRefs` | IdentifierList | — |
| `payloadDescriptorSetRef` | text | Reference ID matching a previously exchanged PayloadDescriptorProfile's payloadDescriptorSet. |
| **`timePeriod`** \* | TimePeriod | — |
| **`readings`** \* | list of Reading | — |
| `touBuckets` | list of TouBucket | — |

### BillDetails

| Field | Type | Description |
|----|-------|-----------------|
| **`profileType`** \* | text | — |
| `customerRefs` | IdentifierList | — |
| **`meterRefs`** \* | IdentifierList | — |
| `serviceDeliveryPointRefs` | IdentifierList | — |
| `payloadDescriptorSetRef` | text | Reference ID matching a previously exchanged PayloadDescriptorProfile's payloadDescriptorSet. |
| **`timePeriod`** \* | TimePeriod | — |
| `readings` | list of Reading | — |
| `touBuckets` | list of TouBucket | — |
| `billNumber` | text | — |
| `billDate` | date | — |
| `dueDate` | date | — |
| `currency` | text | ISO 4217 (INR, USD, ...). |
| **`amountDue`** \* | number | — |
| `energyCharges` | number | Charges for active/reactive energy consumption. |
| `fixedCharges` | number | Fixed charges/demand charges. |
| `otherCharges` | number | Other taxes, duties, surcharges, or adjustments. |
| `prepaidBalance` | number | Prepaid remaining balance/credit amount on the account/meter, if applicable. |
| `paymentStatus` | text | Status of the payment, e.g. PAID, UNPAID, PARTIAL. |
| `billVersion` | integer | Revision number of this bill for the same billNumber. Starts at 1; increments each time a revised bill is issued for the same period. |
| `billingFrequency` | `DAILY` / `WEEKLY` / `MONTHLY` / `BIMONTHLY` / `QUARTERLY` / `HALFYEARLY` / `YEARLY` | — |
| `billGeneratedAt` | date-time | Date-time the bill was generated by the billing system. billDate remains the calendar date printed on the bill. |
| `nextBillDate` | date | Expected date of the next bill for this connection. |
| `fppcaCharges` | number | Fuel and power purchase cost adjustment (FPPCA / PPAC / FAC) charged on this bill, in `currency`. Negative when a refund/credit. |
| `slabRate` | number | Applicable energy slab rate for this bill, in `currency` per kWh, as printed on the bill. |
| `taxElectricityDuty` | number | Electricity duty levied on this bill, in `currency`. |
| `taxGst` | number | Goods and services tax charged on this bill, in `currency`. |
| `taxTdsTcs` | number | Tax deducted or collected at source that is shown on this bill, in `currency`. |
| `subsidyAmount` | number | Subsidy credited on this bill, in `currency`. Zero or absent when no subsidy applies. |
| `subsidyKwh` | number | Energy covered by subsidy on this bill, in kWh. Zero or absent when no subsidy applies. |
| `currentBillAmount` | number | Total charged for the current billing period (energy, fixed, other charges, taxes and duties, less subsidy and incentives), before arrears, advance payments and other prior-period adjustments, in `currency`. |
| `arrearsAmount` | number | Unpaid amount carried forward from previous bills, in `currency`. Positive when outstanding; negative when a credit balance is carried forward. |
| `advancePayment` | number | Amount received in advance and adjusted against this bill, in `currency`. |
| `securityDeposit` | number | Security deposit held against the connection as at billDate, in `currency`. Zero or absent when none is held. |
| `enforcementAmount` | number | Assessment or penalty amount raised through enforcement action (e.g. unauthorised use) included in this bill, in `currency`. |
| `assessedKwh` | number | Energy assessed (estimated) for this bill when the meter reading could not be used, e.g. faulty or tampered meter, in kWh. |
| `touAdjustmentAmount` | number | Net amount added (positive) or reduced (negative) on this bill on account of time-of-use tariff, in `currency`. The billed effect of the touBuckets, not a reading. |
| `openAccessKwh` | number | Energy drawn under open access during this bill's period, in kWh. Absent when the consumer is not an open-access consumer. |
| `openAccessTerm` | `LTOA` / `MTOA` / `STOA` | — |
| `openAccessContractDemandKw` | number | Contracted demand under the open-access arrangement, in kW. |
| `wheelingCharges` | number | Wheeling charges for open-access energy on this bill, in `currency`. |
| `crossSubsidySurcharge` | number | Cross-subsidy surcharge for open-access energy on this bill, in `currency`. |
| `additionalSurcharge` | number | Additional surcharge for open-access energy on this bill, in `currency`. |
| `earlyPaymentAmount` | number | Amount payable if paid on or before earlyPaymentDate, in `currency`. |
| `earlyPaymentDate` | date | Last date on which earlyPaymentAmount applies. |
| `latePaymentAmount` | number | Amount payable if paid after dueDate, in `currency`. |
| `incentiveAmount` | number | Rebate or incentive credited on this bill (e.g. prompt-payment or digital-payment rebate), in `currency`. |
| `discountExpiryDate` | date | Last date on which any discount or incentive shown on this bill can be availed. |
| `serviceLocation` | ServiceLocation | — |

### InstantaneousProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`profileType`** \* | text | — |
| `customerRefs` | IdentifierList | — |
| **`meterRefs`** \* | IdentifierList | — |
| `serviceDeliveryPointRefs` | IdentifierList | — |
| `payloadDescriptorSetRef` | text | Reference ID matching a previously exchanged PayloadDescriptorProfile's payloadDescriptorSet. |
| **`timestamp`** \* | date-time | — |
| **`readings`** \* | list of Reading | — |

### AlarmProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`profileType`** \* | text | — |
| `customerRefs` | IdentifierList | — |
| **`meterRefs`** \* | IdentifierList | — |
| `serviceDeliveryPointRefs` | IdentifierList | — |
| `payloadDescriptorSetRef` | text | Reference ID matching a previously exchanged PayloadDescriptorProfile's payloadDescriptorSet. |
| **`timestamp`** \* | date-time | — |
| **`alarms`** \* | list of MeterAlarm | — |

### EventProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`profileType`** \* | text | — |
| `customerRefs` | IdentifierList | — |
| **`meterRefs`** \* | IdentifierList | — |
| `serviceDeliveryPointRefs` | IdentifierList | — |
| `payloadDescriptorSetRef` | text | Reference ID matching a previously exchanged PayloadDescriptorProfile's payloadDescriptorSet. |
| **`timePeriod`** \* | TimePeriod | — |
| **`events`** \* | list of MeterEvent | — |

### Identifier

| Field | Type | Description |
|----|-------|-----------------|
| **`scheme`** \* | `METER_SERIAL` / `METER_BADGE` / `MRID` / `OBIS` / `SHORT_CODE` / `CONSUMER_NUMBER` / `SERVICE_DELIVERY_POINT` / `DID` / `ORG` / `OTHER` | — |
| **`value`** \* | text | — |
| `namespace` | text | — |

### TimePeriod

| Field | Type | Description |
|----|-------|-----------------|
| **`start`** \* | date-time | — |
| **`duration`** \* | duration | — |

### ReadingDefinition

| Field | Type | Description |
|----|-------|-----------------|
| **`readingType`** \* | text | — |
| **`supportedModes`** \* | list of `READING` / `USAGE` | — |
| **`defaultMode`** \* | `READING` / `USAGE` | — |
| `name` | text | — |
| `shortLabel` | text | — |
| `unit` | `kWh` / `kVAh` / `kvarh` / `kW` / `kvar` / `kVA` / `V` / `A` / `Hz` / `PF` / `NONE` / `INR` / `USD` | — |
| `phase` | `NONE` / `R` / `Y` / `B` / `ABC` | — |
| `flowDirection` | `IMPORT` / `EXPORT` / `NONE` | — |
| `accumulationBehaviour` | `CUMULATIVE` / `DELTA` / `INSTANTANEOUS` / `SUMMATION` / `INDICATING` | — |
| `touZone` | integer | — |

### PayloadDescriptorSet

| Field | Type | Description |
|----|-------|-----------------|
| **`name`** \* | text | — |
| **`payloadDescriptors`** \* | list of PayloadDescriptor | — |
| `compactSequences` | list of CompactSequence | — |

### CompactSequence

| Field | Type | Description |
|----|-------|-----------------|
| **`name`** \* | text | — |
| **`sequenceItems`** \* | list of SequenceItem | — |

### SequenceItem

| Field | Type | Description |
|----|-------|-----------------|
| **`readingType`** \* | text | — |
| `attribute` | `value` / `occurredAt` / `openingValue` / `closingValue` / `validationStatus` | — |

### PayloadDescriptor

| Field | Type | Description |
|----|-------|-----------------|
| **`readingType`** \* | text | — |
| `obis` | text | Optional canonical OBIS code when readingType uses a short code. |
| `name` | text | — |
| `unit` | `kWh` / `kVAh` / `kvarh` / `kW` / `kvar` / `kVA` / `V` / `A` / `Hz` / `PF` / `NONE` / `INR` / `USD` | — |
| `flowDirection` | `IMPORT` / `EXPORT` / `NONE` | — |
| `category` | text | — |
| `reportedMode` | `READING` / `USAGE` | — |
| `touZone` | integer | — |
| `multiplier` | number | Decimal scaling factor (e.g. 0.001 for milli, 1000 for kilo). Default value is 1. |
| `accuracy` | number | Accuracy class or precision value, applied after the multiplier. |

### IntervalPeriod

| Field | Type | Description |
|----|-------|-----------------|
| **`start`** \* | date-time | — |
| **`duration`** \* | duration | — |

### Interval

| Field | Type | Description |
|----|-------|-----------------|
| **`id`** \* | integer | — |
| `intervalPeriod` | IntervalPeriod | — |
| `payloads` | list of number / string / boolean | — |
| `readings` | list of Reading | — |
| `overrides` | list of Override | — |

### Override

| Field | Type | Description |
|----|-------|-----------------|
| **`descriptorIndex`** \* | integer | — |
| `occurredAt` | date-time | — |
| `zone` | integer | — |
| `validationStatus` | `VALID` / `ESTIMATED` / `MANUAL` / `SUSPECT` / `REJECTED` | — |
| `source` | `METER` / `HES` / `ESTIMATED` / `MANUAL` / `IMPORT` / `MDM_COMPUTED` / `CIS_COMPUTED` | — |
| `changeMethod` | text | — |
| `failCode` | text | — |

### Reading

| Field | Type | Description |
|----|-------|-----------------|
| **`readingType`** \* | text | — |
| **`value`** \* | number | — |
| `openingValue` | number | MUST ONLY be provided when the associated payload descriptor specifies reportedMode=USAGE. |
| `closingValue` | number | MUST ONLY be provided when the associated payload descriptor specifies reportedMode=USAGE. |
| `integrationPeriod` | duration | Demand integration period, e.g. PT30M or PT15M. |
| `timePeriod` | TimePeriod | — |
| `occurredAt` | date-time | — |
| `validationStatus` | `VALID` / `ESTIMATED` / `MANUAL` / `SUSPECT` / `REJECTED` | — |
| `source` | `METER` / `HES` / `ESTIMATED` / `MANUAL` / `IMPORT` / `MDM_COMPUTED` / `CIS_COMPUTED` | — |
| `changeMethod` | text | — |
| `failCode` | text | — |

### TouBucket

| Field | Type | Description |
|----|-------|-----------------|
| **`zone`** \* | integer | — |
| **`readings`** \* | list of Reading | — |

### Customer

| Field | Type | Description |
|----|-------|-----------------|
| **`id`** \* | Identifier | — |
| `name` | text | — |
| `consumerCategory` | text | Utility tariff category (e.g., LT2A, NDS, HT). |
| `sanctionedLoadKw` | number | — |
| `billingCycleDay` | integer | — |
| `paymentMode` | `PREPAID` / `POSTPAID` | Indicates if the connection is prepaid or postpaid. |
| `connectionType` | `Single-phase` / `Three-phase` | Type of connection (Single-phase or Three-phase). |
| `contractMaxDemandKw` | number | Maximum demand contracted with the utility for this connection, in kW. |
| `tariffCategoryCode` | text | Billing/tariff category code assigned by the utility. |
| `sanctionedExportLoadKw` | number | Sanctioned/approved grid export limit in kW. |

### ServiceDeliveryPoint

| Field | Type | Description |
|----|-------|-----------------|
| **`id`** \* | Identifier | — |
| `address` | Address | — |
| `geo` | GeoJSONGeometry | — |

### Meter

| Field | Type | Description |
|----|-------|-----------------|
| **`id`** \* | Identifier | — |
| `make` | text | Make of the meter. |
| `model` | text | Model of the meter. |
| `meterType` | `AMR` / `AMI` / `Electromechanical` / `Forward` / `Reverse` / `Bidirectional` / `Prepaid` / `NetMeter` / `Other` | — |
| `meterCategory` | `A` / `B` / `C` / `D1` / `D2` / `D3` / `D4` | — |
| `serviceKind` | `ELECTRICITY` / `GAS` / `WATER` / `HEAT` | — |

### Association

| Field | Type | Description |
|----|-------|-----------------|
| **`serviceDeliveryPointRefs`** \* | IdentifierList | — |
| **`meterRefs`** \* | IdentifierList | — |
| `parentResources` | list of Identifier | List of parent resources (such as feeders or DTs) for this association, replacing feederId and dtId. |
| `telemetryProvider` | text | Telemetry provider for this meter-service association. |
| `commissioningDate` | date-time | Commissioning date of the meter association. |
| `generationCapacityKw` | number | Rated power generation capacity (e.g. solar PV inverter capacity) in kW. |
| `storageCapacityKw` | number | Rated energy storage capacity in kWh. |

### MeterEvent

| Field | Type | Description |
|----|-------|-----------------|
| **`timestamp`** \* | date-time | — |
| **`eventId`** \* | integer | — |
| `eventName` | text | — |
| `phase` | `NONE` / `R` / `Y` / `B` / `ABC` | — |
| `sequence` | integer | — |
| `magnitude` | number | — |
| `duration` | duration | — |

### MeterAlarm

| Field | Type | Description |
|----|-------|-----------------|
| **`timestamp`** \* | date-time | — |
| **`alarmId`** \* | integer | — |
| `alarmName` | text | — |
| **`status`** \* | `ACTIVE` / `CLEARED` | — |
| `severity` | `CRITICAL` / `WARNING` / `INFO` | — |

### ServiceLocation

| Field | Type | Description |
|----|-------|-----------------|
| `postalCode` | text | Postal (PIN) code of the service address. |
| `city` | text | City / town of the service address. |
| `district` | text | Administrative district of the service address. |
| `state` | text | State or union territory of the service address. |
| `substation` | text | Supplying substation identifier per utility records. |
| `region` | text | Utility supply region / zone / circle identifier. |

### PayloadDescriptorProfile

| Field | Type | Description |
|----|-------|-----------------|
| **`profileType`** \* | text | — |
| **`id`** \* | text | Unique identifier for this specific configuration state. |
| **`payloadDescriptorSets`** \* | list of PayloadDescriptorSet | — |

### CustomerDetails

| Field | Type | Description |
|----|-------|-----------------|
| `name` | text | Full name of the customer as per ID proof. |

<!-- FIELD-TABLE:END -->
