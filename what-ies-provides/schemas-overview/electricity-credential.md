# ElectricityCredential v1.2

*A W3C Verifiable Credential, issued per meter or connection by a distribution licensee, that carries the static facts of a consumer's connection and the energy resources behind the meter.*

| Field | Value |
|---|---|
| Document | IES/EC/1.2 |
| Status | Stable (mirrored verbatim from upstream `beckn/DEG`; v1.2 is the current version, v1.1 and v1.0 are previous/deprecated) |
| Applicability | Issued by distribution licensees (DISCOMs); consumed by consumers (holder-bound variant), grid operators and aggregators (bearer variant), banks, subsidy portals and DER marketplaces (as verifiers) |
| This version | v1.2 replaces every power/energy/voltage scalar field with a `QuantitativeValue {value, unit}` pair and introduces the composable `energyResources[]` hierarchy of seven discriminated kinds, documented in [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json) |

---

## 1. Scope and Purpose

The stakeholder is the distribution licensee (DISCOM) and whoever needs a trustworthy, checkable record of one electricity connection and the assets behind it. Without this schema, a licensee has no common, machine-checkable way to state what is connected at a premises, at what capacity, in what condition — and a consumer, grid operator or aggregator has no way to verify those facts except by trusting an unstructured letter or a manual site visit.

This document explains the ElectricityCredential v1.2 schema. It does not define a new schema — it explains the existing one, which is authoritative and IES-hosted (a verbatim mirror of the upstream `beckn/DEG` specification).

The schema itself is deliberately thin at the top: `attributes.yaml` defines only the credential envelope and the `CustomerProfile` / `CustomerDetails` container shapes directly. Everything else — the `EnergyResource` discriminated union, the `ConsumptionProfile` tariff block, the `IdRef` identity reference, and the base `EnergyCredential` — is pulled in by reference from five sibling schemas (`EnergyCredential/v2.0`, `EnergyResource/v2.1`, `MeterServiceProfile/v1.1`, `CustomerDetails/v1.0`, `IdRef/v1.0`). ElectricityCredential v1.2 is best understood as the assembly point where those building blocks are composed for the electricity distribution use case, not as a monolith that defines every field itself.

## 2. What It Records / Covers

For one connection, the credential records:

- the **customer profile** (`customerProfile`, required, non-PII) — a utility customer account (CA) number (`customerNumber`), an optional external identity reference (`idRef`), the `energyResources[]` array (required, minimum one entry), and an optional `consumptionProfiles[]` array;
- one or more **energy resources** behind the meter (`energyResources[]`) — the meter itself, generators (solar, wind, hydro, biogas, CHP, fuel cell), storage (battery/BESS), EV chargers (including vehicle-to-grid), inverters, controllable loads (smart HVAC, water heaters, generic controllable loads), and network equipment (distribution transformers, busbars, feeders, microgrids) — each with make, model, rated and maximum import/export power, commissioning date, location, serial number, an inspection/safety record, and, where relevant, a third-party aggregator enrolment;
- **consumption profiles** (`consumptionProfiles[]`, one entry per meter, linked by `meterId`) — tariff category code, sanctioned load and sanctioned export load, contract maximum demand, billing cycle day, premises type, connection type (single-/three-phase), payment mode (postpaid/prepaid) and service status (active/suspended/closed);
- optionally, **customer details** (`customerDetails`) — the personally identifiable facts (full name, an optional care-of reference for disambiguating people who share a name in a locality, installation address, service connection date) — present only when the credential is issued to the consumer.

The attribute bag shared by every energy-resource kind (`EnergyResourceCommonAttributes`) explicitly distinguishes `ratedPower` (manufacturer nameplate value, kept only for backward compatibility) from `maxExport` (maximum power injected to the grid — for a BESS or V2G charger, its maximum discharge rate) and `maxImport` (maximum power drawn from the grid — for a BESS or V2G charger, its maximum charge rate). Both `maxExport` and `maxImport` are defined as always non-negative, so direction is carried by which field is populated, not by a signed value. A real meter entry, for example, carries no power rating at all — only capability and protocol fields — because a meter measures rather than converts power:

```json
{
  "id": "did:web:ies.discom.example:assets:meter:MET-UNIT-101",
  "type": "METER",
  "attributes": {"meterCapability": "AMR", "energyDirection": "Forward", ...},
  "parentResources": ["did:web:ies.discom.example:assets:meter:MET-BLDG-001"]
}
```

It records identity, capacity, ratings, status and installation facts. It does not record live meter readings — those belong to a separate telemetry schema.

## 3. How Each Item is Identified

The credential itself carries an `id` that is a `urn:uuid`. The issuer is identified by `issuer.id`, a `did:web` anchored to the DISCOM's own domain — the examples use both a generic form (`did:web:example-utility.com`) and DISCOM-style domains (`did:web:ies.discom.example`), each paired in `issuer.idRef` with a reference to the state regulator that licensed it (for example `{"issuedBy": "did:web:serc.example", "subjectId": "serc.example:AABPC12345"}` for the DISCOM under the SERC).

Two issuance variants use `credentialSubject.id` differently:

- in the **bearer** variant, `credentialSubject.id` is absent — whoever holds the signed JSON is treated as the subject, so no consumer identifier appears at all;
- in the **holder-bound** variant, `credentialSubject.id` is the consumer's own DID (the shipped examples use a `did:example:` placeholder for the wallet-generated identifier), and `customerProfile.idRef` carries a reference to a separate identity authority (one example references `did:web:ssa.gov` as the issuing authority for a government ID, illustrating the pattern rather than prescribing a specific Indian identity source).

Each entry in `energyResources[]` carries its own `id` — either a `did:web` path under the issuer's domain (for example `did:web:ies.discom.example:assets:meter:MET-UNIT-101`, or `did:web:example-utility.com:assets:solar-plant:DER-SOLAR-001` for a generator) or, where that is more conventional, the meter's own serial number. The schema documents this explicitly as convention rather than a hard rule: "for METER resources the meter serial number is conventional," leaving DISCOMs latitude in how they mint identifiers. Either way, the DISCOM's existing numbering — CIS/CA account numbers, meter serial numbers — is always preserved as an alias inside or alongside the identifier; it is never replaced. `serialNumber` (the manufacturer nameplate value) and `id` (the network-issued identifier) are kept as two distinct fields precisely so one substitution does not erase the other.

Topology between resources is carried by two link arrays rather than by nesting: `parentResources[]` (ids of resources upstream, e.g. the meter or feeder a DER sits behind) and `subResources[]` (child resources, which may be given either as bare id strings or as fully inline `EnergyResource` objects). The shipped submetering example shows this in practice: a building's main meter (`MET-BLDG-001`) is the `parentResources` target for two tenant sub-meters (`MET-UNIT-101`, `MET-UNIT-102`), and a rooftop solar DER in turn names one tenant's sub-meter as its own parent — a three-level chain expressed entirely through parent references, with no nested object structure required.

## 4. Definitions

- **DID (Decentralised Identifier)** — a W3C-standard verifiable digital identifier (W3C DID Core) that names one thing (an organisation, a person, an asset) and can be checked electronically to confirm the issuer and that it has not been altered.
- **did:web** — a DID method anchored to a domain the participant controls; the DID document (`did.json`) is fetched over HTTPS from that domain.
- **Verifiable Credential (VC)** — a tamper-evident, cryptographically signed digital document (W3C VC Data Model 2.0) that a verifier checks offline using the issuer's published key, with no callback to the issuer.
- **DeDi** — the decentralised registry infrastructure (dedi.global) referenced by the shipped examples' `credentialStatus` block as a revocation registry (`type: dediregistry`), queried by the credential's own UUID.
- **DISCOM** — a distribution licensee (electricity distribution company) serving retail consumers; the example payloads name illustrative DISCOMs rather than real ones.
- **QuantitativeValue** — a `{value, unit}` pair used for every power, energy, apparent-power, reactive-power and voltage field in this schema (`QVPower`, `QVEnergy`, `QVApparentPower`, `QVReactivePower`, `QVVoltage` in the field reference), each mapped to QUDT IRIs via the JSON-LD context (e.g. `kW` → `qudt:KiloW`, `kWh` → `qudt:KiloW-HR`).
- **CIM (Common Information Model)** — the IEC data model (IEC 61968 for distribution/metering, IEC 61970 for transmission/generation/DER) that every `energyResources[]` kind is explicitly aligned to at the class level, down to individual attributes (for example `GeneratingUnit.maxOperatingP`, `BatteryUnit.ratedE`, `PowerElectronicsConnection.maxQ`).
- **Bearer credential** — the issuance variant with no `credentialSubject.id`; whoever holds the signed document is treated as its subject.
- **Holder-bound credential** — the issuance variant where `credentialSubject.id` is set to a specific holder's wallet DID.
- **SunSpec DER Model** — a numbered family of standard Modbus/point-map definitions for distributed energy resources (SunSpec Alliance); this schema cites specific model numbers (702, 703, 705, 711) as the source for individual inverter fields.
- **ESPI** — the Energy Services Provider Interface (NAESB REQ.21), a US utility-data standard cited here for the shape of two fields (`energyDirection`, `paymentMode`) where no equivalent Indian standard is named.

## 5. Basis of Standards

The IES order of preference is fixed:

1. Bureau of Indian Standards (IS)
2. CEA Regulations and the Indian Electricity Grid Code (IEGC)
3. International Electrotechnical Commission (IEC)
4. Institute of Electrical and Electronics Engineers (IEEE)

This schema follows, directly, field by field:

- **IS 16444** for the meter application protocol: the field reference states plainly that `DLMS_COSEM` (IEC 62056) is "mandatory for India AMI per BIS IS 16444";
- **CEA Connectivity Regulations, 2013 (amended 2018)**, together with **IEEE 1547-2018 Clause 11**, for the `inspection` object on every energy resource (asset commissioning and safety inspection, "captured by the distribution licensee at energisation and on re-certification events");
- **IEC 61968-9** (CIM, metering) for `EnergyResourceMeter` and the common device attributes — `EndDeviceInfo.ratedPower`, `EndDeviceInfo.serialNumber`, `AmiBillingReadyKind` (for `meterCapability`), `EndDeviceFunction` (for the `functions[]` enum), and `FlowDirectionKind` (for `energyDirection`, paired with **ESPI NAESB REQ.21**);
- **IEC 61970-301/302** (CIM, transmission and DER) for generators, storage, EV chargers, inverters, controllable loads and network equipment — down to individual attributes: `GeneratingUnit.maxOperatingP` and `.nominalP`, `BatteryUnit.ratedE`, `PowerElectronicsConnection.maxP/minQ/maxQ/ratedS/inverterMode`, `EnergyConsumer`/`ConformLoad` classification, and `BaseVoltage.nominalVoltage`;
- **IS 16221** (PV module qualification), together with **IEC 61727** (PV grid interface), for `dcArrayCapacity` — the DC-side nameplate capacity of a solar array at Standard Test Conditions (the industry "kWp" figure), which the schema notes is typically larger than the AC-side `maxExport` because of inverter clipping and DC-to-AC ratio;
- **IEC 61968-1** for the PII block in `CustomerDetails` — `Customer.name` for `fullName` and `ServiceLocation` for both `installationAddress` and the activation semantics of `serviceConnectionDate` — alongside **GeoJSON RFC 7946** for the `geo` coordinate pair and **schema.org PostalAddress** for the optional `address` fields;
- **IEC 62196-2** for EV connector types `Type1` (J1772) and `Type2` (Mennekes), alongside the non-IEC industry connectors `CCS1`/`CCS2`, `CHAdeMO`, **GB/T 20234**, and **SAE J3400** (NACS) — reflecting that EVSE connector standards are a genuinely mixed international field, not an IEC monopoly;
- **ISO 15118-20** and **OCPP 2.1 Bidirectional Power Transfer (BPT)** for the `EV_V2G` kind's vehicle-to-grid control protocol.

## 6. Where Indian Standards Do Not Yet Exist

- **Asset commissioning and safety inspection across all DER kinds** — no single Indian standard covers this end-to-end; the schema falls back to IEEE 1547-2018 Clause 11 alongside the CEA Connectivity Regulations 2013 (amended 2018).
- **Third-party aggregator enrolment for flexibility/demand-response** — no Indian standard yet defines this; the `aggregator` object on every resource kind is instead based on IEEE 2030.5 and IEC 61850-7-420 (DER control roles). The schema documents that "controllability" is asset-level and independent of observability — an asset can be observable by an aggregator without being controllable by it.
- **Battery round-trip efficiency measurement** — `roundTripEfficiencyPct` uses IEC 62933-2-1 as its performance test method, and the field reference is explicit that this is distinct both from `stateOfHealthPct` (a cumulative life indicator) and from inverter conversion efficiency.
- **Inverter ride-through categorisation and advanced grid-support functions** — `rideThroughCategory` uses the IEEE 1547-2018 abnormal-operating-performance categories (Category I basic, II enhanced for distribution-connected DER, III advanced for large/transmission-connected DER); `voltVarEnabled` and `freqDroopEnabled` fall back to IEEE 2030.5 and SunSpec DER Models 705 and 711 respectively, with no Indian equivalent named.
- **Demand-response control protocols for smart loads** — `controlProtocol` on `EnergyResourceLoad` draws on OpenADR 2.0b, OCPP 2.0.1, SunSpec Modbus and EEBus — an international, vendor-driven set, not an Indian standard.
- **Prepaid/postpaid billing modality and service-connection lifecycle status** — `paymentMode` and `serviceStatus` are based on CIM's `AmiBillingReadyKind`/ESPI and `UsagePoint.status` respectively; no Indian metering-billing standard is cited as an alternative.

## 7. The Record(s)

ElectricityCredential v1.2 is a single top-level record: a W3C Verifiable Credential. It is not wrapped by any other credential. It is issued by a DISCOM per meter or connection, and it is comparatively static — it changes when an asset is commissioned, a rating changes, or the connection's tariff terms change, not on every reading.

Within the one credential, `energyResources[]` is a composable hierarchy: every entry is discriminated by its `type` field into one of seven kinds — `EnergyResourceMeter` (`METER`), `EnergyResourceGenerator` (`SOLAR_PV`, `WIND`, `HYDRO`, `BIOGAS`, `CHP`, `FUEL_CELL`, plus the deprecated `SOLAR` alias), `EnergyResourceStorage` (`BESS`, plus the deprecated `BATTERY` alias), `EnergyResourceEVCharger` (`EV_CHARGER`, `EV_V2G`), `EnergyResourceInverter` (`INVERTER`), `EnergyResourceLoad` (`SMART_HVAC`, `SMART_WATER_HEATER`, `CONTROLLABLE_LOAD`), and `EnergyResourceNetwork` (`DT`, `BUS`, `FEEDER`, `MICROGRID`) — each carrying kind-specific attributes on top of the shared `EnergyResourceCommonAttributes` set (make, model, rated/import/export power, telemetry provider, commissioning date, location, serial number, inspection record, aggregator enrolment).

The shipped `example.json` illustrates why the hierarchy needs to be a discriminated union rather than one flat shape: it carries one meter, a `SOLAR_PV` generator (with `dcArrayCapacity` distinct from `maxExport`), a `WIND` generator, and two separate `BESS` entries side by side — one fully specified with `storageType`, `stateOfHealthPct`, `roundTripEfficiencyPct` and an `aggregator` enrolment, the other with only the minimum fields populated, showing that most kind-specific attributes are optional rather than mandated even within the same kind.

Two issuance variants of this one record exist, distinguished only by whether `credentialSubject.id` is set and by what is populated in `customerDetails`:

- the **bearer** variant, used for grid-side, non-PII issuance (the DER Visibility use case);
- the **holder-bound** variant, issued to a consumer's own wallet, documented end-to-end in its own use-case guide, [Consumer Energy Passport](../../use-cases/consumer-energy-passport/README.md).

This page describes the schema and its structure; readers who need the holder-bound issuance walkthrough — identity proofing, wallet delivery, selective disclosure — should go to that use-case guide rather than this one.

## 8. Schedule I — Field Reference (summary)

The schema is built from these logical blocks:

- **Envelope** — `id`, `type`, `issuer`, `validFrom`, `validUntil`, `credentialStatus`, `credentialSubject`, `proof` — the standard W3C VC wrapper fields.
- **CustomerProfile** — the required, non-PII block: `customerNumber`, optional `idRef`, the `energyResources[]` array (minimum one entry), and optional `consumptionProfiles[]`.
- **CustomerDetails** — the optional, PII block: `fullName`, optional `careOf`, `installationAddress` (GeoJSON `geo` plus optional `address`), `serviceConnectionDate`.
- **EnergyResource kinds** — seven typed entries (`EnergyResourceMeter`, `EnergyResourceGenerator`, `EnergyResourceStorage`, `EnergyResourceEVCharger`, `EnergyResourceInverter`, `EnergyResourceLoad`, `EnergyResourceNetwork`), each inheriting `EnergyResourceCommonAttributes` and adding its own kind-specific fields, plus the `subResources[]` / `parentResources[]` topology links common to every kind.
- **ConsumptionProfile** — `meterId`, `sanctionedLoad`, optional `sanctionedExportLoad`, `billingCycleDay`, `contractMaxDemand`, `tariffCategoryCode`, `premisesType`, `connectionType`, `paymentMode`, `serviceStatus` — one entry per meter.
- **QuantitativeValue types** — `QVPower` (`W`/`kW`/`MW`), `QVEnergy` (`kWh`/`MWh`), `QVApparentPower` (`kVA`/`MVA`), `QVReactivePower` (`kVAR`/`MVAR`), `QVVoltage` (`V`/`kV`) — the `{value, unit}` pairs used throughout the other blocks.

The full field-by-field reference (Field / Type / Description, auto-generated from schema.json, with each standards-derived field's description prefixed "Based on") is at [ElectricityCredential v1.2 — Field reference](../../schemas/ElectricityCredential/v1.2/README.md#field-reference).

## 9. Schedule II

Not applicable as a wrapping relationship in the usual sense, but ElectricityCredential v1.2 is explicitly a **composition**, not a self-contained monolith: its own `attributes.yaml` defines only the envelope and the `CustomerProfile`/`CustomerDetails` shapes, and pulls in `EnergyCredential/v2.0` (as its base, via `allOf`), `EnergyResource/v2.1` (for the seven-kind discriminated union), `MeterServiceProfile/v1.1` (aliased as `ConsumptionProfile`), `CustomerDetails/v1.0`, and `IdRef/v1.0` by `$ref`. It does not wrap, and is not wrapped by, any other top-level *credential* — it remains the one Verifiable Credential issued and verified as a single signed document.

## 10. How It Fits Together

ElectricityCredential v1.2 is the one schema behind two different use cases, distinguished by issuance variant and audience. As the **Consumer Energy Passport**, it is issued holder-bound to a consumer's wallet, carrying `customerDetails` and a consumer-scoped `credentialSubject.id`, and gives the consumer a portable, verifiable proof of their connection and assets. As **DER Visibility**, it is issued bearer, scoped to a feeder, substation or the licensee as a whole, carrying only `energyResources[]` with no consumer PII, and gives grid operators and aggregators a checkable view of what is connected on the network.

The shipped examples show a third pattern in between: **parallel metering**, where one premises has two sibling meters under a single customer profile — an import meter (`energyDirection: Forward`) measuring grid consumption and a separate export meter (`energyDirection: Reverse`) measuring gross solar feed-in under its own tariff code (`FIT-SOLAR-01`), with the solar DER's `parentResources` pointing at the export meter rather than the import meter. This is the same credential and the same schema as the single-meter case; the topology links (`parentResources`, `meterId`) are what let one credential represent arrangements from a single domestic meter up to a multi-meter building with tenant sub-metering.

In all cases, the credential carries only static, structural facts; live interval readings are handled by a separate telemetry schema referenced by the same meter and asset identifiers, not by this credential.

## 11. Points for Confirmation

1. The choice between a `did:web` path identifier and a bare meter serial number for `energyResources[].id` is documented in the schema's own field reference as convention ("for METER resources the meter serial number is conventional") rather than a fixed rule — implementers should confirm which their DISCOM will use consistently before onboarding assets. In practice, all three shipped examples use the `did:web` path form exclusively (e.g. `did:web:ies.discom.example:assets:meter:MET-UNIT-101`), with the bare serial number appearing only as the trailing path segment (as in `did:web:example-utility.com:assets:meter:MET2025789456123`) or duplicated in the separate `serialNumber` field — none of the examples uses an unqualified serial number as the `id` on its own, so the bare-serial-as-`id` option remains a documented allowance rather than a demonstrated pattern.
2. The deprecated type aliases `SOLAR` (→ `SOLAR_PV`) and `BATTERY` (→ `BESS`) remain valid for backward compatibility; consumers of this schema should confirm their own tooling accepts both the deprecated and current values during the transition period.
3. `ratedPower` is kept on every resource kind for backward compatibility, with `maxExport` (and, for load-drawing resources, `maxImport`) preferred; implementers should confirm which field their downstream systems read until `ratedPower` is fully retired.
4. `dcArrayCapacity` on solar generators and `maxExport` are both expressed in the same `QVPower` unit family (`kW`/`MW`), but carry different physical meanings (DC nameplate at STC versus AC-side grid injection limit) — the schema notes this distinction only in prose, not in the unit string itself; implementers should confirm downstream systems do not conflate the two when only one is populated.
5. Several fields central to distributed-energy-resource management — aggregator enrolment, ride-through category, volt-VAR and frequency-droop flags, demand-response control protocol — have no Indian standard behind them at all today (Section 6); as India's own DER/DR regulatory framework matures, these fields may need a follow-up revision once a CEA regulation or BIS standard exists to reference in their place.
6. This schema is a composition over five separately versioned sibling schemas (`EnergyCredential/v2.0`, `EnergyResource/v2.1`, `MeterServiceProfile/v1.1`, `CustomerDetails/v1.0`, `IdRef/v1.0`); a version bump in any of those sibling schemas could change ElectricityCredential's effective shape without a corresponding version bump here — implementers should confirm which exact sibling versions are pinned before treating "v1.2" as a complete specification of the wire format.

### Annexure A — Standards Referenced

| Standard | Scope |
|---|---|
| IS 16444 | DLMS/COSEM (IEC 62056) meter application protocol, mandatory for India AMI |
| CEA Connectivity Regulations, 2013 (amended 2018) | Asset commissioning and safety inspection |
| IEEE 1547-2018 | DER interconnection: commissioning (Cl. 11), abnormal-operation ride-through categories |
| IEC 61968-9 | CIM — metering (EndDeviceInfo, AmiBillingReadyKind, EndDeviceFunction, FlowDirectionKind, UsagePoint) |
| IEC 61968-1 | CIM — customer and service location (Customer.name, ServiceLocation) |
| IEC 61970-301 | CIM — loads and network equipment (EnergyConsumer/ConformLoad, PowerTransformer, BusbarSection, Feeder, BaseVoltage) |
| IEC 61970-302 | CIM — generation, storage, EV chargers, inverters (GeneratingUnit, BatteryUnit, PowerElectronicsConnection) |
| IS 16221 | PV module qualification (DC array capacity, "kWp") |
| IEC 61727 | PV grid interface |
| ESPI (NAESB REQ.21) | Energy flow direction and billing modality field shapes |
| SunSpec DER Models 702, 703, 705, 711 | Inverter apparent/reactive power, ramp time, volt-VAR, frequency-droop |
| IEC 62933-2-1 | Battery round-trip efficiency test method |
| IEC 61850-7-420 | DER control roles (aggregator enrolment) |
| IEEE 2030.5 | DER aggregator/flexibility control roles; volt-VAR/frequency-droop fallback |
| IEC 62196-2 | EV connector types (Type 1/J1772, Type 2/Mennekes) |
| GB/T 20234; SAE J3400 (NACS) | Non-IEC EV connector standards in common use |
| ISO 15118-20; OCPP 2.1 BPT | Vehicle-to-grid (V2G) bidirectional charging control |
| GeoJSON RFC 7946; schema.org PostalAddress | Installation address geometry and postal fields |

### Annexure B — Example Payloads

Example payloads for this schema are at [schemas/ElectricityCredential/v1.2/examples/](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/ElectricityCredential/v1.2/examples) — a single-meter household with mixed generation and storage (`example.json`), a multi-tenant building with main-meter/sub-meter topology and tenant-level rooftop solar (`example-submetering.json`), and a parallel import/export metering arrangement for a solar feed-in tariff (`example-parallel-metering.json`).

### Annexure C — JSON Schema

The machine-readable schema definitions are at [schema.json](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/schema.json) and [attributes.yaml](https://india-energy-stack.github.io/ies-accelerator/schemas/ElectricityCredential/v1.2/attributes.yaml).
