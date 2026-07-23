# Consumer Energy Passport

*The IES [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2), issued holder-bound to a consumer's wallet (W3C Verifiable Credential).*

**[Implementation Guide →](../use-cases/consumer-energy-passport/README.md)**

| Field | Value |
|---|---|
| Document | IES/CEP-PROFILE/1.2 |
| Status | Live in pilot (four pilot DISCOMs; one staged) |
| Applicability | All distribution licensees |
| This version | Consumer Energy Passport *variant* of ElectricityCredential v1.2. Static credential only; live interval data uses MeterData, separately. |

---

## 1. Scope and Purpose

The stakeholder is the distribution licensee (DISCOM) and the consumer it serves. As rooftop solar, batteries and EV charging grow behind consumers' meters, the licensee often cannot see what's connected, at what capacity, or where; and the consumer cannot prove their connection and assets to a bank, subsidy portal or marketplace without a manual DISCOM letter.

This document defines the **Consumer Energy Passport** — the holder-bound issuance of the ElectricityCredential v1.2, carrying the static facts of a consumer's connection and the energy resources behind their meter. It does not define a new schema: ElectricityCredential v1.2 is the schema; the Passport profiles how it's shaped, issued and delivered when the consumer is the audience (`credentialSubject.id` = wallet DID; `customerProfile.idRef` = a government-ID reference).

## 2. What It Records / Covers

| Records | Detail | Source |
|---|---|---|
| Consumer & issuing licensee | The consumer and the DISCOM that issues the credential | ElectricityCredential v1.2 (`customerProfile`, `issuer`) |
| Service connection | Tariff category and sanctioned load | ElectricityCredential v1.2 (`consumptionProfiles[]`) |
| Meters | The net meter, and a generation meter where used | ElectricityCredential v1.2 (`energyResources[]`, type `METER`) |
| Distribution transformer | Where known | ElectricityCredential v1.2 (`energyResources[]`, network equipment) |
| Energy resources behind the meter | Solar, battery, EV charger, inverter, controllable load — with capacity, inspection status and equipment details | ElectricityCredential v1.2 (`energyResources[]`) |

It records identity, capacity and status — **not live readings**, which are the [MeterData](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) record, linked by asset identifier (see [Consumer Meter Digest](consumer-meter-digest.md)).

## 3. How Each Item is Identified

Every item — consumer, connection, each meter, each asset — carries a [DID](../glossary.md#did). Existing licensee numbers are reused as aliases inside identifiers.

| Subject | Identifier method | Example |
|---|---|---|
| DISCOM (issuer) | `did:web` on owned domain | `did:web:ies.discom.example` |
| Regulator | `did:web` on owned domain | `did:web:ies.serc.example` |
| Consumer (holder) | `did:key` (wallet) or `tel:` URI | `did:key:z6MkjVQ8r4f3rPuY…` |
| Meter / inverter / DER / transformer | `did:web` under issuer domain | `did:web:ies.discom.example:assets:meter:NM-44091234` |
| Existing CIS consumer number | Plain string, kept verbatim | `1102004567` → `customerProfile.customerNumber` |

[DeDi](../glossary.md#dedi) is used only for Beckn subscriber registries and credential revocation — not as an identifier method for consumers, meters or assets.

## 4. Definitions

- **DER** — any device behind a meter that generates (solar, wind), stores (battery) or controllably consumes (EV charger) electricity.
- **DID** — verifiable digital identifier (W3C DID Core), detailed in §3.
- **Verifiable Credential (VC)** — a tamper-evident, signed document (W3C VC Data Model 2.0) a verifier checks offline against the issuer's published key.
- **Energy Resource** — any physical asset in the credential, one typed entry in `energyResources[]`.
- **QuantitativeValue** — a `{value, unit}` pair for every power/energy/capacity figure, mapped to QUDT.
- **Holder-bound** — issued to a specific holder's wallet, vs. a bearer credential.
- **Net Meter** — the bidirectional billing meter; the source of truth.
- **Aggregator** — a third party enrolling controllable resources for demand response.

## 5. Basis of Standards

Fixed order of preference: **IS → CEA Regulations / IEGC → IEC → IEEE**, recorded in the field tables below.

| Standard | Role here |
|---|---|
| **IS 16444** | Smart meter specification |
| **IS 15959** | DLMS/COSEM; OBIS codes for metering |
| **CEA (Installation and Operation of Meters) Regulations, 2006** | The net meter as the source of truth |

## 6. Where Indian Standards Do Not Yet Exist

- **Grid asset data model** — IEC CIM (IEC 61970-301, IEC 61968-11) underlies the `energyResources[]` kinds.
- **DER electrical attributes** — IEEE 1547-2018 (ride-through, anti-islanding, volt-var, freq-watt); CEA's own limits are retained where CEA sets them (harmonics per IEEE 519-2014; DC injection ≤0.5% under CEA Connectivity Regs 2013, am. 2019).
- **PV module rating** — DC array capacity (kWp) follows **IS 14286** (= IEC 61215).

## 7. The Record

One record: a static Verifiable Credential, changed only on commissioning, capacity change or ownership transfer, and re-issued (with revocation of the old) on material change. It is holder-bound — the consumer holds it in DigiLocker or a DID wallet and discloses fields selectively. Live interval data is a separate [MeterData](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) record, linked by identifier.

## 8. Schedule I — Static Fields of the Credential

Schedule I summarizes the ElectricityCredential v1.2 fields used by this Passport profile; the canonical schema remains the complete constraint set.
`Required` means required whenever the enclosing object/profile applies. `Conditional` means required only under the stated condition. `Optional` means not schema-required. `—` means no field-level standard annotation. In Schedule I only: an unqualified Standard/basis citation reproduces that field's schema `x-standard` exactly; any citation that is not itself a field-level `x-standard` is labelled *(profile basis)*, *(schema type/format basis)*, *(editorial basis)*, or *(inherited from parent x-standard)*, as applicable. This labelling convention applies to Schedule I only and does not govern Schedule II.

### 8.1 Passport Envelope, Holder, and Issuer

| Field path | Type / allowed values | Standard / basis | Status |
|---|---|---|---|
| `@context` | array of text; required contains `https://www.w3.org/ns/credentials/v2` | W3C VC Data Model 2.0 *(profile basis)* | Required |
| `id` | uri with pattern `urn:uuid:<UUID>` (lowercase hex UUID) | W3C VC Data Model 2.0 *(profile basis)* | Required |
| `type` | list of text containing `ElectricityCredential` | W3C VC Data Model 2.0 *(profile basis)* | Required |
| `issuer` | object (`id`, `name`, optional `idRef`) | ElectricityCredential v1.2 *(schema type/format basis)* | Required |
| `issuer.id` | uri | ElectricityCredential v1.2 *(schema type/format basis)* | Required |
| `issuer.name` | text | ElectricityCredential v1.2 *(schema type/format basis)* | Required |
| `issuer.idRef` | IdRef object (`issuedBy`, `subjectId`) | IdRef/v1.0 *(profile basis)* | Optional |
| `issuer.idRef.issuedBy` | uri | IdRef/v1.0 *(profile basis)* | Conditional — required when `issuer.idRef` exists |
| `issuer.idRef.subjectId` | text matching `authority-domain:id-value` | IdRef/v1.0 *(profile basis)* | Conditional — required when `issuer.idRef` exists |
| `validFrom` | date-time | W3C VC Data Model 2.0 *(profile basis)* | Required |
| `validUntil` | date-time | W3C VC Data Model 2.0 *(profile basis)* | Optional |
| `credentialStatus` | object (`id`, `type`, `statusPurpose`, `statusListCredential`) | DeDi revocation-registry status mechanism *(profile basis)* | Optional |
| `credentialStatus.id` | uri | DeDi revocation-registry status mechanism *(profile basis)* | Conditional — required when `credentialStatus` exists |
| `credentialStatus.type` | `dediregistry` | DeDi revocation-registry status mechanism *(profile basis)* | Conditional — required when `credentialStatus` exists |
| `credentialStatus.statusPurpose` | `revocation`, `suspension` | DeDi revocation-registry status mechanism *(profile basis)* | Conditional — required when `credentialStatus` exists |
| `credentialStatus.statusListCredential` | uri | DeDi revocation-registry status mechanism *(profile basis)* | Conditional — required when `credentialStatus` exists |
| `proof` | object | W3C VC Data Model 2.0 *(profile basis)* | Optional |
| `proof.type` | text | W3C VC Data Model 2.0 *(profile basis)* | Conditional — required when `proof` exists |
| `proof.created` | date-time | W3C VC Data Model 2.0 *(profile basis)* | Conditional — required when `proof` exists |
| `proof.verificationMethod` | uri | W3C VC Data Model 2.0 *(profile basis)* | Conditional — required when `proof` exists |
| `proof.proofPurpose` | `assertionMethod`, `authentication` | W3C VC Data Model 2.0 *(profile basis)* | Conditional — required when `proof` exists |
| `proof.proofValue` | text | W3C VC Data Model 2.0 *(profile basis)* | Conditional — required when `proof` exists |
| `credentialSubject` | object | W3C VC Data Model 2.0 *(profile basis)* | Required |
| `credentialSubject.id` | uri | Holder wallet DID/URI | Optional |
| `credentialSubject.customerProfile` | CustomerProfile object | ElectricityCredential v1.2 *(schema type/format basis)* | Required |

### 8.2 Consumer and Service Connection

| Field path | Type / allowed values | Standard / basis | Status |
|---|---|---|---|
| `credentialSubject.customerProfile.customerNumber` | text | utility customer account (CA) number | Required |
| `credentialSubject.customerProfile.idRef` | IdRef | — | Optional |
| `credentialSubject.customerProfile.idRef.issuedBy` | uri | IdRef/v1.0 *(profile basis)* | Conditional — required when `credentialSubject.customerProfile.idRef` exists |
| `credentialSubject.customerProfile.idRef.subjectId` | text matching `authority-domain:id-value` | IdRef/v1.0 *(profile basis)* | Conditional — required when `credentialSubject.customerProfile.idRef` exists |
| `credentialSubject.customerDetails` | object | — | Optional |
| `credentialSubject.customerDetails.fullName` | text | CIM (IEC 61968-1 Customer.name) | Conditional — required when `credentialSubject.customerDetails` is present |
| `credentialSubject.customerDetails.installationAddress` | object | GeoJSON RFC 7946; schema.org PostalAddress; CIM (IEC 61968-1 ServiceLocation) | Conditional — required when `credentialSubject.customerDetails` is present |
| `credentialSubject.customerDetails.careOf` | object (`name`, optional `relationship`) | — | Optional |
| `credentialSubject.customerDetails.careOf.name` | text | — | Conditional — required when `credentialSubject.customerDetails.careOf` exists |
| `credentialSubject.customerDetails.careOf.relationship` | enum `parent`, `spouse`, `guardian`, `sibling`, `child`, `other` | — | Optional |
| `credentialSubject.customerDetails.installationAddress.geo` | GeoJSON Geometry | GeoJSON RFC 7946, EPSG:4326 *(schema type/format basis)* | Conditional — required when `credentialSubject.customerDetails.installationAddress` is present |
| `credentialSubject.customerDetails.installationAddress.address` | schema.org PostalAddress-aligned object | schema.org PostalAddress *(schema type/format basis)* | Optional |
| `credentialSubject.customerDetails.serviceConnectionDate` | date-time | CIM (IEC 61968-1 ServiceLocation activation date) | Conditional — required when `credentialSubject.customerDetails` is present |

### 8.3 Energy Resources and Common Attributes

| Field path | Type / allowed values | Standard / basis | Status |
|---|---|---|---|
| `credentialSubject.customerProfile.energyResources` | list of EnergyResource | CIM-aligned ElectricityCredential resource model *(editorial basis)* | Required |
| `credentialSubject.customerProfile.energyResources[].id` | text (stable identifier) | Passport profile uses DID pattern in §3; base schema also permits meter serial-number style identifiers | Required |
| `credentialSubject.customerProfile.energyResources[].type` | `METER`, `SOLAR_PV`, `SOLAR` (deprecated alias), `WIND`, `HYDRO`, `BIOGAS`, `CHP`, `FUEL_CELL`, `BESS`, `BATTERY` (deprecated alias), `EV_CHARGER`, `EV_V2G`, `INVERTER`, `SMART_HVAC`, `SMART_WATER_HEATER`, `CONTROLLABLE_LOAD`, `DT`, `BUS`, `FEEDER`, `MICROGRID` | CIM discriminator per kind *(editorial basis)* | Required |
| `credentialSubject.customerProfile.energyResources[].subResources` | list of text or inline EnergyResource | Topology (child refs or embedded items) | Optional |
| `credentialSubject.customerProfile.energyResources[].parentResources` | list of text | Topology (parent refs) | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes` | object | EnergyResourceCommonAttributes *(schema type/format basis)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.make` | text | CIM asset metadata *(editorial basis)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.model` | text | CIM asset metadata *(editorial basis)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.ratedPower` | QuantitativeValue `{value, unit}`; unit ∈ W, kW, MW | CIM (IEC 61968-9 EndDeviceInfo.ratedPower; IEC 61970 GeneratingUnit.maxOperatingP) | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.maxExport` | QuantitativeValue `{value, unit}`; unit ∈ W, kW, MW | CIM (IEC 61970 GeneratingUnit.maxOperatingP; IEC 61970-302 PowerElectronicsConnection.maxP, injection) | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.maxImport` | QuantitativeValue `{value, unit}`; unit ∈ W, kW, MW | CIM (IEC 61970-302 PowerElectronicsConnection.maxP, absorption) | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.telemetryProvider` | text | Local integration metadata | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.commissioningDate` | date-time | ISO 8601 *(schema type/format basis)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.location` | Location | GeoJSON RFC 7946 *(schema type/format basis)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.serialNumber` | text | CIM (IEC 61968-9 EndDeviceInfo.serialNumber) | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.inspection` | object | IEEE 1547-2018 Cl. 11 (commissioning); CEA Connectivity Regs 2013 (amended 2018) | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.inspection.date` | date | Inherited from `inspection` *(inherited from parent x-standard)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.inspection.result` | `pass`, `fail`, `conditional` | Inherited from `inspection` *(inherited from parent x-standard)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.inspection.inspectorId` | text | Inherited from `inspection` *(inherited from parent x-standard)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.aggregator` | object | IEEE 2030.5; IEC 61850-7-420 (DER control roles) | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.aggregator.id` | uri | Inherited from `aggregator` *(inherited from parent x-standard)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.aggregator.name` | text | Inherited from `aggregator` *(inherited from parent x-standard)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.aggregator.controllable` | boolean (`true`, `false`) | Inherited from `aggregator` *(inherited from parent x-standard)* | Optional |
| `credentialSubject.customerProfile.energyResources[].attributes.aggregator.enrolledOn` | date | Inherited from `aggregator` *(inherited from parent x-standard)* | Optional |

### 8.4 Resource-Specific Attributes

| Resource kind | Field path | Type / allowed values | Standard / basis | Status |
|---|---|---|---|---|
| Meter | `credentialSubject.customerProfile.energyResources[].attributes.meterCapability` | `Electromechanical`, `CMRI`, `AMR`, `AMI` | CIM (IEC 61968-9 `AmiBillingReadyKind`) | Optional |
| Meter | `credentialSubject.customerProfile.energyResources[].attributes.energyDirection` | `Forward`, `Reverse`, `Bidirectional`, `Net` | CIM (FlowDirectionKind); ESPI NAESB REQ.21 | Optional |
| Meter | `credentialSubject.customerProfile.energyResources[].attributes.functions` | list of `ToU`, `NetMetering`, `MaxDemand`, `LoadControl`, `TamperDetection`, `PowerQuality`, `EventLogging` | CIM (IEC 61968-9 EndDeviceFunction) | Optional |
| Meter | `credentialSubject.customerProfile.energyResources[].attributes.feeder` | text | Utility topology metadata | Optional |
| Meter | `credentialSubject.customerProfile.energyResources[].attributes.bus` | text | Utility topology metadata | Optional |
| Meter | `credentialSubject.customerProfile.energyResources[].attributes.communicationTechnology` | `PLC`, `RF_Mesh`, `GPRS`, `NB-IoT`, `LoRa`, `ZigBee`, `Other` | Deployment metadata | Optional |
| Meter | `credentialSubject.customerProfile.energyResources[].attributes.applicationProtocol` | `DLMS_COSEM`, `ANSI_C12_18`, `IEC_61850`, `Modbus`, `Other` | DLMS/IEC application protocol layer *(editorial basis)* | Optional |
| Generator | `credentialSubject.customerProfile.energyResources[].attributes.dcArrayCapacity` | QuantitativeValue `{value, unit}`; unit ∈ W, kW, MW | IS 16221 (PV module qualification); IEC 61727 (PV grid interface) | Optional |
| Generator | `credentialSubject.customerProfile.energyResources[].attributes.nominalPower` | QuantitativeValue `{value, unit}`; unit ∈ W, kW, MW | CIM (IEC 61970 GeneratingUnit.nominalP) | Optional |
| Generator | `credentialSubject.customerProfile.energyResources[].attributes.efficiency` | number (0 to 100) | Resource-specific | Optional |
| Storage | `credentialSubject.customerProfile.energyResources[].attributes.storageCapacity` | QuantitativeValue `{value, unit}`; unit ∈ kWh, MWh | CIM (IEC 61970-302 BatteryUnit.ratedE) | Optional |
| Storage | `credentialSubject.customerProfile.energyResources[].attributes.storageType` | `LithiumIon`, `LeadAcid`, `FlowBattery`, `NaS`, `NiCd`, `Flywheel`, `Other` | BESS taxonomy | Optional |
| Storage | `credentialSubject.customerProfile.energyResources[].attributes.stateOfHealthPct` | number (0 to 100) | BESS state health metadata | Optional |
| Storage | `credentialSubject.customerProfile.energyResources[].attributes.roundTripEfficiencyPct` | number (0 to 100) | IEC 62933-2-1 (performance test method) | Optional |
| EV charger | `credentialSubject.customerProfile.energyResources[].attributes.connectorType` | `Type1`, `Type2`, `CCS1`, `CCS2`, `CHAdeMO`, `GB_T`, `NACS`, `Other` | IEC 62196 / IS 17017 *(editorial basis)* | Optional |
| EV charger | `credentialSubject.customerProfile.energyResources[].attributes.controlProtocol` | `OCPP_1.6`, `OCPP_2.0.1`, `OCPP_2.1`, `ISO_15118_2`, `ISO_15118_20`, `Other` | OCPP / ISO 15118 *(editorial basis)* | Optional |
| EV charger | `credentialSubject.customerProfile.energyResources[].attributes.v2xProtocol` | `CHAdeMO_V2G`, `CCS_BPT`, `ISO_15118_20_AC_BPT`, `ISO_15118_20_DC_BPT`, `Other` | ISO 15118-20 *(editorial basis)* | Optional |
| Inverter | `credentialSubject.customerProfile.energyResources[].attributes.ratedApparentPower` | QuantitativeValue (`kVA`, `MVA`) | SunSpec DER Model 702 (maxVA); CIM (IEC 61970-302 PowerElectronicsConnection.ratedS) | Optional |
| Inverter | `credentialSubject.customerProfile.energyResources[].attributes.maxReactivePower` | QuantitativeValue (`kVAR`, `MVAR`) | SunSpec DER Model 702 (maxVar); CIM (IEC 61970-302 PowerElectronicsConnection.maxQ) | Optional |
| Inverter | `credentialSubject.customerProfile.energyResources[].attributes.minReactivePower` | QuantitativeValue (`kVAR`, `MVAR`) | SunSpec DER Model 702 (maxVarNeg); CIM (IEC 61970-302 PowerElectronicsConnection.minQ) | Optional |
| Inverter | `credentialSubject.customerProfile.energyResources[].attributes.rideThroughCategory` | `CategoryI`, `CategoryII`, `CategoryIII` | IEEE 1547-2018 (ride-through category) | Optional |
| Inverter | `credentialSubject.customerProfile.energyResources[].attributes.operatingMode` | `GridFollowing`, `GridForming`, `Standby` | CIM (IEC 61970-302 PowerElectronicsConnection.inverterMode) | Optional |
| Inverter | `credentialSubject.customerProfile.energyResources[].attributes.voltVarEnabled` | boolean (`true`, `false`) | IEEE 2030.5 (opModVoltVar); SunSpec DER Model 705 | Optional |
| Inverter | `credentialSubject.customerProfile.energyResources[].attributes.freqDroopEnabled` | boolean (`true`, `false`) | IEEE 1547-2018; SunSpec DER Model 711 | Optional |
| Inverter | `credentialSubject.customerProfile.energyResources[].attributes.enterServiceRampTimeSec` | number (minimum 0) | SunSpec DER Model 703 (ESRmpTms) | Optional |
| Controllable load | `credentialSubject.customerProfile.energyResources[].attributes.controlProtocol` | `OpenADR_2.0b`, `OCPP_2.0.1`, `SunSpec_Modbus`, `EEBus`, `Modbus`, `Other` | DR protocol metadata | Optional |
| Controllable load | `credentialSubject.customerProfile.energyResources[].attributes.loadCategory` | `Heating`, `Cooling`, `WaterHeating`, `Lighting`, `EV`, `Industrial`, `Other` | CIM (IEC 61970-301 ConformLoad classification) | Optional |
| Network resource | `credentialSubject.customerProfile.energyResources[].attributes.nominalVoltage` | QuantitativeValue (`V`, `kV`) | CIM (IEC 61970-301 BaseVoltage.nominalVoltage) | Optional |
| Network resource | `credentialSubject.customerProfile.energyResources[].attributes.zone` | text | Utility topology metadata | Optional |
| Network resource | `credentialSubject.customerProfile.energyResources[].attributes.substationId` | text | Utility topology metadata | Optional |
| Network resource | `credentialSubject.customerProfile.energyResources[].attributes.feederCode` | text | Utility topology metadata | Optional |

Standards caveat: ElectricityCredential v1.2 annotates `dcArrayCapacity` with `IS 16221` / `IEC 61727`; §6 and Annexure A cite `IS 14286` (= `IEC 61215`) for PV module rating. These references are not interchangeable.

### 8.5 Tariff and Sanctioned-load Profile

| Field path | Type / allowed values | Standard / basis | Status |
|---|---|---|---|
| `credentialSubject.customerProfile.consumptionProfiles` | list of ConsumptionProfile | MeterServiceProfile v1.1 *(profile basis)* | Optional |
| `credentialSubject.customerProfile.consumptionProfiles[].meterId` | text | CIM UsagePoint linkage *(editorial basis)* | Conditional — required in each ConsumptionProfile item |
| `credentialSubject.customerProfile.consumptionProfiles[].sanctionedLoad` | QuantitativeValue `{value, unit}`; unit ∈ W, kW, MW | CIM (IEC 61968-9 UsagePoint); service limit metadata *(editorial basis)* | Conditional — required in each ConsumptionProfile item |
| `credentialSubject.customerProfile.consumptionProfiles[].tariffCategoryCode` | text | CIM (IEC 61968-9 UsagePoint.serviceCategory) | Conditional — required in each ConsumptionProfile item |
| `credentialSubject.customerProfile.consumptionProfiles[].sanctionedExportLoad` | QuantitativeValue `{value, unit}`; unit ∈ W, kW, MW | Utility export policy metadata | Optional |
| `credentialSubject.customerProfile.consumptionProfiles[].contractMaxDemand` | QuantitativeValue `{value, unit}`; unit ∈ W, kW, MW | CIM contract demand metadata *(editorial basis)* | Optional |
| `credentialSubject.customerProfile.consumptionProfiles[].billingCycleDay` | integer (1–31) | Billing profile metadata | Optional |
| `credentialSubject.customerProfile.consumptionProfiles[].connectionType` | `Single-phase`, `Three-phase` | CIM (IEC 61968-9 UsagePoint.phaseCode) | Optional |
| `credentialSubject.customerProfile.consumptionProfiles[].premisesType` | `Residential`, `Commercial`, `Industrial`, `Agricultural` | Domain/editorial premises classification *(editorial basis)* | Optional |
| `credentialSubject.customerProfile.consumptionProfiles[].paymentMode` | `POSTPAID`, `PREPAID` | CIM (IEC 61968-9 AmiBillingReadyKind, ESPI) | Optional |
| `credentialSubject.customerProfile.consumptionProfiles[].serviceStatus` | `active`, `suspended`, `closed` | CIM (IEC 61968-9 UsagePoint.status) | Optional |

Use the corresponding `METER` `EnergyResource` `id` as `meterId`; JSON Schema does not enforce the match.

## 9. Schedule II — Separate MeterData v0.6 Reference

Schedule II is not part of the Consumer Energy Passport; the Passport remains the single ElectricityCredential in Schedule I. MeterData is exchanged separately for meter, billing, event, and alarm data. For this profile, carry the Passport meter's `energyResources[].id` in `meterRefs` with scheme: `DID`; `METER_SERIAL` may also be carried as an alias. The schemas do not enforce the match, so exchange validation must. The tables below cover the MeterData v0.6 fields relevant to Passport linkage; they are not a complete MeterData field catalogue.

**Metered profiles** means `INTERVAL`, `DAILY`, `MONTHLY`, `BILL_DETAILS`, `INSTANTANEOUS`, `EVENT`, and `ALARM` — the seven profiles that inherit `BaseProfile` — as distinct from `CUSTOMER` and `DESCRIPTOR`, which do not.

### 9.1 Identification and Linkage

| Field path | Type / allowed values | Standard / basis | Status |
|---|---|---|---|
| `profileType` | one of `CUSTOMER`, `INTERVAL`, `DAILY`, `MONTHLY`, `BILL_DETAILS`, `INSTANTANEOUS`, `EVENT`, `ALARM`, `DESCRIPTOR` | `EnergyData.oneOf` profile dispatch | Required |
| `meterRefs` | list of Identifier | MeterData v0.6 `BaseProfile` requirement | Required for metered profiles (inherited via `BaseProfile`); not a defined field for CUSTOMER (which carries `meters` instead) or DESCRIPTOR |
| `meterRefs[].scheme` | enum including `METER_SERIAL`, `METER_BADGE`, `MRID`, `OBIS`, `SHORT_CODE`, `CONSUMER_NUMBER`, `SERVICE_DELIVERY_POINT`, `DID`, `ORG`, `OTHER` | IES identifier scheme enum | Conditional — required per Identifier item, in the profiles where `meterRefs` applies |
| `meterRefs[].value` | text | IES identifier value | Conditional — required per Identifier item, in the profiles where `meterRefs` applies |
| `customerRefs` | list of Identifier | Customer linkage metadata | Optional for metered profiles (inherited via `BaseProfile`); also optional for CUSTOMER (defined separately, same `IdentifierList` shape, not via `BaseProfile`); not a defined field for DESCRIPTOR |
| `serviceDeliveryPointRefs` | list of Identifier | Service delivery point linkage | Optional for metered profiles (inherited via `BaseProfile`); not a defined field for CUSTOMER (which carries `serviceDeliveryPoints` instead) or DESCRIPTOR |
| `payloadDescriptorSetRef` | text | Descriptor set reference for compact matrix mode | Optional for metered profiles (inherited via `BaseProfile`); not a defined field for CUSTOMER or DESCRIPTOR (which carries `payloadDescriptorSets` instead) |

### 9.2 MeterData Profile Shapes

| Profile | `profileType` const | Required fields |
|---|---|---|
| Customer profile | `CUSTOMER` | `profileType`, `customer`, `serviceDeliveryPoints`, `meters`, `associations` |
| Descriptor profile | `DESCRIPTOR` | `profileType`, `id`, `payloadDescriptorSets` |
| Interval profile | `INTERVAL` | `profileType`, `meterRefs`, `intervalPeriod` |
| Daily profile | `DAILY` | `profileType`, `meterRefs`, `intervalPeriod` |
| Monthly profile | `MONTHLY` | `profileType`, `meterRefs`, `timePeriod`, `readings` |
| Bill details profile | `BILL_DETAILS` | `profileType`, `meterRefs`, `timePeriod`, `amountDue` |
| Instantaneous profile | `INSTANTANEOUS` | `profileType`, `meterRefs`, `timestamp`, `readings` |
| Event profile | `EVENT` | `profileType`, `meterRefs`, `timePeriod`, `events` |
| Alarm profile | `ALARM` | `profileType`, `meterRefs`, `timestamp`, `alarms` |

### 9.3 Readings, Intervals, and Descriptors

| Field path | Type / allowed values | Standard / basis | Status |
|---|---|---|---|
| `intervalPeriod` | object (`start`, `duration`) | MeterData v0.6 `IntervalPeriod` object *(schema type/format basis)* | Required for `INTERVAL` and `DAILY` |
| `intervalPeriod.start` | date-time | ISO 8601 `date-time` format *(schema type/format basis)* | Required where `intervalPeriod` is present |
| `intervalPeriod.duration` | duration | ISO 8601 `duration` format *(schema type/format basis)* | Required where `intervalPeriod` is present |
| `compactSequenceRef` | text | Name of the compact sequence to use from `payloadDescriptorSets[].compactSequences[]` | Optional for `INTERVAL` and `DAILY` |
| `intervals` | list of Interval | compact sequence interval rows | Optional for metered profile `INTERVAL` and `DAILY`; not defined by other profile schemas |
| `intervals[].id` | integer | Compact sequence row index | Conditional — required in each Interval item |
| `intervals[].intervalPeriod` | object (`start`, `duration`) | ISO 8601 and per-interval overrides | Optional |
| `intervals[].payloads` | list of number/string/boolean | compact sequence cell values by descriptor index, positionally aligned with the referenced `CompactSequence.sequenceItems[]` | Optional |
| `intervals[].readings` | list of Reading | inline detailed reading alternative to `payloads` for this interval row | Optional |
| `intervals[].overrides` | list of Override | interval-specific overrides | Optional |
| `readings` | list of Reading | inline reading alternatives | Conditional — required for `MONTHLY` and `INSTANTANEOUS`; optional for `INTERVAL`, `DAILY`, `BILL_DETAILS` |
| `readings[].readingType` | text | Reading metadata | Conditional — required in each Reading item |
| `readings[].value` | number | Numeric measured value | Conditional — required in each Reading item |
| `readings[].openingValue` | number | USAGE-mode usage provenance | Optional |
| `readings[].closingValue` | number | USAGE-mode usage provenance | Optional |
| `readings[].occurredAt` | date-time | Event timing | Optional |
| `readings[].integrationPeriod` | duration | Demand-averaging window for this reading (for example `PT15M` or `PT30M`); distinct from `readings[].timePeriod` | Optional |
| `readings[].timePeriod` | TimePeriod (`start`, `duration`) | Start/duration span covered by the reading; not the demand-averaging window | Optional |
| `readings[].changeMethod` | text | Change-method metadata | Optional |
| `readings[].failCode` | text | Failure-code metadata | Optional |
| `readings[].validationStatus` | `VALID`, `ESTIMATED`, `MANUAL`, `SUSPECT`, `REJECTED` | Validation state | Optional |
| `readings[].source` | `METER`, `HES`, `ESTIMATED`, `MANUAL`, `IMPORT`, `MDM_COMPUTED`, `CIS_COMPUTED` | provenance source | Optional |
| `touBuckets` | list of TouBucket | Time-of-Use bucket grouping for billing-period readings | Optional for `MONTHLY` and `BILL_DETAILS`; not defined by other profile schemas |
| `touBuckets[].zone` | integer (1–8) | MeterData v0.6 `TouBucket.zone` integer range *(schema type/format basis)* | Conditional — required in each TouBucket item |
| `touBuckets[].readings` | list of Reading | Readings within this TOU zone bucket | Conditional — required in each TouBucket item |
| `payloadDescriptorSets` | list of PayloadDescriptorSet | descriptor dictionary | Required for DESCRIPTOR |
| `payloadDescriptorSets[].name` | text | Descriptor label | Conditional — required in each descriptor set |
| `payloadDescriptorSets[].payloadDescriptors` | list of PayloadDescriptor | descriptor detail list | Conditional — required in each descriptor set |
| `payloadDescriptorSets[].payloadDescriptors[].readingType` | text | Descriptor key | Conditional — required in each payload descriptor |
| `payloadDescriptorSets[].payloadDescriptors[].name` | text | Optional descriptor label | Optional |
| `payloadDescriptorSets[].payloadDescriptors[].category` | text | Optional descriptor category | Optional |
| `payloadDescriptorSets[].payloadDescriptors[].touZone` | integer 0-8 | Optional TOU zone | Optional |
| `payloadDescriptorSets[].payloadDescriptors[].obis` | text | Optional OBIS mapping | Optional |
| `payloadDescriptorSets[].payloadDescriptors[].unit` | `kWh`, `kVAh`, `kvarh`, `kW`, `kvar`, `kVA`, `V`, `A`, `Hz`, `PF`, `NONE`, `INR`, `USD` | Optional unit annotation | Optional |
| `payloadDescriptorSets[].payloadDescriptors[].flowDirection` | `IMPORT`, `EXPORT`, `NONE` | Flow direction metadata | Optional |
| `payloadDescriptorSets[].payloadDescriptors[].reportedMode` | `READING`, `USAGE` | Reporting mode metadata | Optional |
| `payloadDescriptorSets[].payloadDescriptors[].multiplier` | number (default 1) | Optional scaling | Optional |
| `payloadDescriptorSets[].payloadDescriptors[].accuracy` | number | Optional precision metadata | Optional |
| `payloadDescriptorSets[].compactSequences` | list of CompactSequence | Named compact-sequence definitions for this descriptor set, referenced by `compactSequenceRef` | Optional |
| `payloadDescriptorSets[].compactSequences[].name` | text | Compact sequence name, matched by `compactSequenceRef` | Conditional — required in each CompactSequence item |
| `payloadDescriptorSets[].compactSequences[].sequenceItems` | list of SequenceItem | Ordered reading-type positions making up this compact sequence; `intervals[].payloads[k]` aligns positionally with `sequenceItems[k]` | Conditional — required in each CompactSequence item |
| `payloadDescriptorSets[].compactSequences[].sequenceItems[].readingType` | text | Reading type key for this sequence position | Conditional — required in each SequenceItem |
| `payloadDescriptorSets[].compactSequences[].sequenceItems[].attribute` | `value`, `occurredAt`, `openingValue`, `closingValue`, `validationStatus` (default `value`) | Which Reading attribute this sequence position carries | Optional |

### 9.4 Canonical Electrical Registers (IES Codes)

The examples below reproduce the profiles and supported modes assigned in IES codes.json.

| OBIS / short label | Unit | Profiles | Supported modes | Standard / source | Notes |
|---|---|---|---|---|---|
| `1.0.1.8.0.255` / `kWh imp` | kWh | `DAILY`, `MONTHLY`, `INSTANTANEOUS` | `READING`, `USAGE` | IS 15959 Part 1 Table 22; Part 2 Table A14; Part 3 Table 1 | Cumulative energy import |
| `1.0.2.8.0.255` / `kWh exp` | kWh | `DAILY`, `MONTHLY`, `INSTANTANEOUS` | `READING`, `USAGE` | IS 15959 Part 2 Table A1 | Cumulative energy export |
| `1.0.9.8.0.255` / `kVAh imp` | kVAh | `DAILY`, `MONTHLY` | `READING`, `USAGE` | IS 15959 Part 2 Table A1 | Cumulative apparent import |
| `1.0.10.8.0.255` / `kVAh exp` | kVAh | `DAILY`, `MONTHLY` | `READING`, `USAGE` | IS 15959 Part 2 Table A1 | Cumulative apparent export |
| `1.0.1.29.0.255` / `kWh imp block` | kWh | `INTERVAL` | `USAGE` | IS 15959 Part 2 Table A15; Part 3 Table 2 | Block incremental import |
| `1.0.2.29.0.255` / `kWh exp block` | kWh | `INTERVAL` | `USAGE` | IS 15959 Part 2 Table A15; Part 3 Table 2 | Block incremental export |
| `1.0.1.6.0.255` / `MD kW` | kW | `DAILY`, `MONTHLY`, `INSTANTANEOUS` | `USAGE` | IS 15959 Part 1 Table 29; Part 2 Table A14; Part 3 Table 1 | Max demand with peak timestamp |
| `1.0.9.6.0.255` / `MD kVA` | kVA | `MONTHLY` | `USAGE` | IS 15959 Part 2 Table A1 | Max apparent demand (peak) |
| `1.0.1.7.0.255` / `P_Import` | kW | `INSTANTANEOUS` | `READING` | IS 15959 Part 2 Table A1 | Active import power |
| `1.0.2.7.0.255` / `P_Export` | kW | `INSTANTANEOUS` | `READING` | IS 15959 Part 2 Table A1 | Active export power |
| `1.0.3.7.0.255` / `Q_Lag` | kvar | `INSTANTANEOUS` | `READING` | IS 15959 Part 2 Table A1 | Reactive power lag |
| `1.0.9.7.0.255` / `S_Total` | kVA | `INSTANTANEOUS` | `READING` | IS 15959 Part 2 Table A1 | Apparent power total |
| `1.0.13.7.0.255` / `PF_3P` | — | `INSTANTANEOUS` | `READING` | IS 15959 Part 2 Table A1 | Power factor |
| `1.0.14.7.0.255` / `Freq` | Hz | `INSTANTANEOUS` | `READING` | IS 15959 Part 2 Table A1 | Grid frequency |
| `1.0.32.7.0.255` / `V_R` | V | `INSTANTANEOUS` | `READING` | IS 15959 Part 2 Table A14; Part 3 Table 1 | Voltage (R-phase) |
| `1.0.31.7.0.255` / `I_R` | A | `INSTANTANEOUS` | `READING` | IS 15959 Part 2 Table A1 | Current (R-phase) |

### 9.5 Events and Alarms

| Field path | Type / allowed values | Profile | Status |
|---|---|---|---|
| `events` | list of `MeterEvent` | `EVENT` | Required for EVENT |
| `events[].timestamp` | date-time | `EVENT` | Conditional — required in each MeterEvent item |
| `events[].eventId` | integer | `EVENT` | Conditional — required in each MeterEvent item |
| `events[].eventName` | text | `EVENT` | Optional |
| `events[].phase` | `NONE`, `R`, `Y`, `B`, `ABC` | `EVENT` | Optional |
| `events[].sequence` | integer | `EVENT` | Optional |
| `events[].magnitude` | number | `EVENT` | Optional |
| `events[].duration` | duration | `EVENT` | Optional |
| `alarms` | list of `MeterAlarm` | `ALARM` | Required for ALARM |
| `alarms[].timestamp` | date-time | `ALARM` | Conditional — required in each MeterAlarm item |
| `alarms[].alarmId` | integer | `ALARM` | Conditional — required in each MeterAlarm item |
| `alarms[].alarmName` | text | `ALARM` | Optional |
| `alarms[].status` | `ACTIVE`, `CLEARED` | `ALARM` | Conditional — required in each MeterAlarm item |
| `alarms[].severity` | `CRITICAL`, `WARNING`, `INFO` | `ALARM` | Optional |

## 10. How It Fits Together

```
                      ┌── Solar array
Grid ──[ Net Meter ]──┼── (Generation Meter *) ── Inverter ** ──┬── Solar array
   (billing meter,    │                                          └── Battery
    source of truth)  └── Inverter ** ── EV charger
  *  used by some licensees, not others.  ** may serve more than one asset.
  Topology: parentResources / subResources — PV and BESS → Inverter → Meter → DT.
```

Generation is measured at the net meter, a generation meter, or the inverter's own live data (MeterData). All assets live in one `energyResources[]` array; the credential carries identity and ratings, MeterData carries live readings.

## 11. Points for Confirmation

1. **Holder-binding method.** Confirmed for the DigiLocker Pull URI channel: the `DigiLockerId` from the pull request is carried into `customerProfile.idRef` as the identity binding (see [DigiLocker Integration — Identity Binding](../how-you-implement-ies/digilocker.md#identity-binding-the-digilocker-id)). Non-DigiLocker methods (offline-KYC XML, in-person) remain open, to be documented for privacy review.
2. **Selective-disclosure profile** with first verifiers (SD-JWT-VC typical).
3. **Re-issuance triggers** on material change, and revocation into the DeDi registry.
4. **Schema-host provenance** — served from `india-energy-stack.github.io/ies-accelerator`; a custom IES/gov domain is a governance decision.

---

## Schemas Used in This Use Case

A single schema — **[ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2)** (W3C VC). No additional schemas. Live readings use [MeterData](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) separately — see [Consumer Meter Digest](consumer-meter-digest.md).

## Value Unlock

The consumer gains a portable, tamper-evident proof of their connection and assets, verifiable offline by banks, subsidy portals and marketplaces in seconds — no DISCOM callback. The DISCOM cuts verification load and fraud and gets a clean asset register as a by-product. Regulators get a consistent, auditable asset record across licensees. Selective disclosure lets the consumer reveal only what a verifier needs.

---

## Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 16444 (Parts 1, 2) | AC smart meter — specification |
| IS 15959 (Parts 1–3) | DLMS/COSEM companion spec; OBIS codes |
| IS 14286 (= IEC 61215) | PV module design qualification and type approval |
| IS 16221 (Parts 1, 2) (= IEC 62109-1/-2) | Inverter safety (inverter resource only) |
| IS 16270 | Solar PV batteries |
| IS 17017 (series) (from IEC 61851 / 62196) | EV conductive charging |
| CEA (Installation and Operation of Meters) Regs, 2006 | Metering legal framework; net meter as source of truth |
| CEA (Connectivity of DG Resources) Regs, 2013, am. 2019 | Connectivity below 33 kV; PCC; DC-injection; harmonics |
| IEC 61968-1 / -9 / -11 | CIM — customer, metering, distribution model |
| IEC 61970-301 / -302 | CIM — network model; DER / power-electronics / battery |
| IEC 61850-7-420 | DER control roles |
| IEC 61727 / IEC 62116 | PV utility interface; anti-islanding |
| IEC 62933 / 62933-2-1 / IEC 62619 | Storage systems; performance test; battery safety |
| IEC 62196 | EV connectors |
| IEC 62056 | DLMS/COSEM; OBIS |
| IEEE 1547-2018 | DER interconnection and interoperability |
| IEEE 519-2014 | Harmonic control (CEA-referenced) |
| IEEE 2030.5 | DER communications / aggregator roles |
| W3C VC Data Model 2.0; W3C DID Core | Credential envelope; identifiers |
| GeoJSON (RFC 7946); schema.org PostalAddress | Location and postal address |
| OCPP; ISO 15118 | EV charger control / V2G |

## Annexure B — Example Payload

A single-phase LT-Domestic connection with a 5 kW PV array on a 5 kVA inverter and a 6 kWh aggregator-enrolled battery, fed from one DT. Holder-bound; identifiers illustrative.

- **[`examples/example.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/ElectricityCredential/v1.2/examples/example.json)**
- **[`example-submetering.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/ElectricityCredential/v1.2/examples/example-submetering.json)** — building main meter + tenant sub-meters + rooftop solar
- **[`example-parallel-metering.json`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/schemas/ElectricityCredential/v1.2/examples/example-parallel-metering.json)** — import + export meter (solar FIT)

## Annexure C — JSON Schema

Canonical: `https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/` — [`schema.json`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json) (Draft 2020-12), [`context.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/context.jsonld), [`vocab.jsonld`](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/vocab.jsonld). ElectricityCredential v1.2 is one of two schema-version directories (of eleven across IES) that annotates individual fields with their governing standard, via the singular `x-standard` property; the §5 order of preference (`IS → CEA Regulations / IEGC → IEC → IEEE`) applies regardless of whether a given schema carries that annotation.
