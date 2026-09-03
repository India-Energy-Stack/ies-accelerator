# IES Term Taxonomy

*Every term published by the seven IES schema families, at their current reference versions — 368 in total: 278 attributes and 90 named types. Terms are reused from the published schema sources rather than redefined here.*

| Field | Value |
|---|---|
| Applicability | All seven IES schema families at their current reference versions |
| This version | Compiled from `schemas/<Family>/<reference version>/` in this repository. Attributes and named types only — glossary concepts, superseded-version fields and external DEG schema terms are out of scope. |

Concepts and abbreviations — DISCOM, DER, Beckn, DeDi and the like — are not schema terms and live in the [Glossary](../glossary.md).

## Schema families and codes

| Code | Schema family | Code | Schema family |
|---|---|---|---|
| ARR | ArrFiling v0.5 | MDR | MeterDataRequest v0.6 |
| EC | ElectricityCredential v1.2 | MDRC | MeterDataRequestCredential v0.6 |
| MD | MeterData v0.6 | ON | OutageNotification v0.1 |
| MDC | MeterDataCredential v0.6 | — | — |

<div id="tax-filter-wrap" style="margin:1.5rem 0">
  <input id="tax-filter" type="search" placeholder="Filter terms — type a name, type, schema code or word from a definition"
         style="width:100%;padding:.6rem .8rem;font-size:1rem;border:1px solid #ccc;border-radius:6px;box-sizing:border-box" />
  <div id="tax-count" style="margin-top:.4rem;font-size:.85rem;opacity:.7"></div>
</div>

<script>
(function () {
  var box = document.getElementById('tax-filter');
  if (!box) return;
  var tables = [].slice.call(document.querySelectorAll('table')).filter(function (t) {
    var h = t.querySelector('thead tr, tr');
    return h && /Term/i.test(h.cells[0] ? h.cells[0].textContent : '');
  });
  var out = document.getElementById('tax-count');
  function run() {
    var q = box.value.trim().toLowerCase(), shown = 0, total = 0;
    tables.forEach(function (t) {
      [].slice.call(t.tBodies[0] ? t.tBodies[0].rows : []).forEach(function (r) {
        total++;
        var hit = !q || r.textContent.toLowerCase().indexOf(q) !== -1;
        r.style.display = hit ? '' : 'none';
        if (hit) shown++;
      });
    });
    out.textContent = q ? shown + ' of ' + total + ' terms' : '';
  }
  box.addEventListener('input', run);
})();
</script>

> The filter above is active on the GitHub Pages build. On GitBook and on GitHub.com it is not rendered — use the site search, or your browser's find-on-page.

## Table D.1 — Attributes (278)

| Term | Type | Definition | Schema | Source standard |
|---|---|---|---|---|
| @context † | array; string | JSON-LD context URI(s) binding the document's terms to the published IES vocabulary. | ARR, EC, ON | W3C VC / JSON-LD |
| accumulationBehaviour | AccumulationBehaviour | CUMULATIVE / DELTA / INSTANTANEOUS / SUMMATION / INDICATING | MD | — |
| accuracy | number | Accuracy class or precision value, applied after the multiplier. | MD, MDR | — |
| actualRestoration | string | Set when status=RESTORED; feeds IEEE 1366 indices. | ON | — |
| address † | Address | Postal address of the service delivery point (Address object). | EC, MD | — |
| addressCountry | string | Country name or ISO-3166-1 alpha-2 code. | EC | — |
| addressLocality | string | City/locality. | EC | — |
| addressRegion | string | State/region/province. | EC | — |
| adminAreas | array | Named localities / wards / villages. | ON | — |
| affectedArea | OutageAffectedArea | OutageAffectedArea | ON | — |
| affectedAssets † | array | Network assets affected by the outage, as OutageAsset entries. | ON | — |
| aggregator | object | Third-party flexibility / demand-response enrolment for this asset. Present when an aggregator is authorised to dispatch or observe the resource. Controllability flag is asset-level; the asset may still be observable even when controllable is false. | EC | IEEE 2030.5; IEC 61850-7-420 (DER control roles) |
| alarmId † | integer | Numeric identifier of the alarm raised by the meter or head-end system. | MD, ON | — |
| alarmName † | string | Human-readable name of the alarm. | MD | — |
| alarmRefs | array | References into MeterData AlarmProfile records. | ON | — |
| alarms † | array | Alarm records carried in an ALARM profile (MeterAlarm entries). | MD | — |
| amispCode | string | AMI Service Provider that supplied the detection signal (feeder-status ingest API). | ON | — |
| amount | number/null | Amount in the filing's currency and unitScale. Null means the line item exists in the form but was not filed / not applicable. Negative values represent credits, deductions, or adjustments that reduce ARR. | ARR | — |
| amountBasis | string | AUDITED - actual costs verified by auditors APPROVED - amounts approved by the SERC in a tariff order PROPOSED - amounts requested by the DISCOM, pending SERC approval TRUED_UP - reconciled amounts after comparing actuals to approved NOT_FILED - placeholder year in a control period, no data yet | ARR | — |
| amountDue † | number | Total amount payable on the bill. | MD | — |
| applicationProtocol | string | Application-layer protocol for meter data. DLMS_COSEM: IEC 62056, mandatory for India AMI per BIS IS 16444. ANSI_C12_18: North American. Orthogonal to communicationTechnology (physical layer). | EC | — |
| assetLevel | string | Network level of the affected asset (local enum; aligns with CIM Equipment/UsagePoint). | ON | — |
| associations † | array | Meter-to-service-point associations for the customer (Association entries). | MD | — |
| attribute | string | value / occurredAt / openingValue / closingValue / validationStatus | MD | — |
| attributes | EnergyResourceEVChargerAttributes; EnergyResourceGeneratorAttributes; EnergyResourceInverterAttributes; EnergyResourceLoadAttributes; EnergyResourceMeterAttributes; EnergyResourceNetworkAttributes; EnergyResourceStorageAttributes; object | Attribute bag. Inherits EnergyResourceCommonAttributes via allOf plus kind-specific fields. | EC | — |
| authorisation | oneOf | Inline authorization object or URI reference to it. | MDR | — |
| backFeedGiven | boolean | Partial restoration via alternate feed (OMS "Back-Feed given"). | ON | — |
| bbox | array | Optional bounding box `[west, south, east, north]` in degrees. | EC | — |
| billDate † | string | Date the bill was generated. | MD | — |
| billingCycleDay | integer | Day of month on which the billing cycle resets. | EC, MD | — |
| billNumber † | string | Bill or invoice number issued by the utility. | MD | — |
| bus | string | Busbar identifier at the meter's connection point. | EC | — |
| capabilities † | MeterDataCapabilities | Capability set granted by this authorisation (MeterDataCapabilities). | MDR | — |
| capabilitiesRequested † | MeterDataCapabilities | Capability set the requester asks for (MeterDataCapabilities). | MDR | — |
| careOf | object | Care-of (c/o) reference person used to uniquely identify / disambiguate a customer who may share the same fullName with others in a locality (e.g. a village). Pairs a name with an optional, gender-neutral relationship. | EC | — |
| category | string | VARIABLE - costs varying with energy volume (power purchase) FIXED - costs independent of volume (O&M, depreciation, interest, return) INCOME - revenue credits that reduce the ARR (negative amounts) SUB_TOTAL - computed aggregation of other line items ARR - the final net/aggregate revenue requirement ADJUSTMENT - true-up corrections, pass-throughs, FPPCA adjustments | ARR, MD, ON | IEEE 1782-2022 §4.4 (with IEEE 1366) |
| cause † | OutageCause | Cause of the outage (OutageCause: category, subcategory, code, free text). | ON | — |
| changeMethod † | string | How the value was changed or derived when validated, estimated or overridden. | MD | — |
| circle † | string | Circle (organisational unit) in the DISCOM network hierarchy: Discom > Zone > Circle > Division > Subdivision > Substation. | ON | — |
| closingValue | number | MUST ONLY be provided when the associated payload descriptor specifies reportedMode=USAGE. | MD | — |
| code | string | Vendor/OMS fault-reason code, carried verbatim (e.g. a DISCOM FAULT_REASON) — not standardized; map to `category`/`subcategory` for interoperability (see fault_reason_crosswalk.json). Set `codeNamespace` where the code's authority matters. | ON | — |
| codeNamespace | string | Authority/vendor that defines `code` (e.g. the OMS vendor or DISCOM). | ON | — |
| commissioningDate | string | ISO 8601 date-time the asset was commissioned. | EC, MD | — |
| communicationTechnology | string | Last-mile physical-layer communication technology. | EC | — |
| compactSequenceRef | string | Name of the compact sequence to use from the payloadDescriptorSets. | MD | — |
| compactSequences | array | list of CompactSequence | MD | — |
| complaintCount | integer | Linked consumer complaints (OMS "No. of Complaints"). | ON | — |
| componentOf | string | lineItemId of the parent subtotal this item contributes to. | ARR | — |
| connectionType | string | Type of connection (Single-phase or Three-phase). | EC, MD | CIM (IEC 61968-9 UsagePoint.phaseCode) |
| connectorType | string | Physical connector standard. Type1: IEC 62196-2 Type 1 (J1772). Type2: IEC 62196-2 Type 2 (Mennekes). CCS1/CCS2: Combined Charging System DC fast charge. CHAdeMO: CHAdeMO DC fast charge. GB_T: GB/T 20234. NACS: SAE J3400. | EC | — |
| consumerCategory | string | Consumer mix on the asset (local enum; DISCOM "Feeder Type"). | MD, ON | — |
| consumerConsent | array | Consent references/receipts proving authorization (optional). | MDR | — |
| consumers | array | List of consumer URIs/DIDs for whom the data is requested (optional). | MDR | — |
| consumptionProfiles | array | Tariff and load characteristics per meter connection. Each entry links to a METER via meterId. | EC | — |
| contact | string | Phone/email/URL for queries (e.g. 1912). | ON | — |
| contractMaxDemand | QVPower | Maximum demand contracted with the utility for this connection. | EC | — |
| contractMaxDemandKw | number | Maximum demand contracted with the utility for this connection, in kW. | MD | — |
| controllable | boolean | True if the aggregator is authorised to issue dispatch / curtailment instructions. False = observation-only. | EC | — |
| controlPeriodEnd | string | End fiscal year of MYT control period. | ARR | — |
| controlPeriodStart | string | Start fiscal year of MYT control period (only for MYT filings). | ARR | — |
| controlProtocol | string | Demand-response / control protocol supported by this load device. | EC | — |
| coordinates | array | Coordinates per RFC 7946 for all types **except** GeometryCollection. Order is **[lon, lat, (alt)]**. For Polygons, this is an array of linear rings; each ring is an array of positions. | EC | — |
| created † | string | Timestamp at which the cryptographic proof was created. | EC | W3C VC Data Integrity |
| credentialStatus † | object | Revocation/suspension status information for the credential. | EC | W3C VC Status List |
| credentialSubject | MeterDataCredentialSubject; MeterDataRequestCredentialSubject; object | The subject of the credential: the consumer or asset entity whose meter data is attested, plus the MeterData payload. | EC, MDC, MDRC | — |
| currency | string | ISO 4217 (INR, USD, ...). | ARR, MD | — |
| customer † | Customer | Customer identity and connection master data (Customer object). | MD | — |
| customerDetails | CustomerDetails | CustomerDetails | EC, MD | — |
| customerNumber | string | Utility customer account (CA) number. | EC | — |
| customerProfile † | CustomerProfile | The credential subject's customer profile (CustomerProfile). | EC | — |
| customerRefs | IdentifierList | IdentifierList | MD | — |
| customersAffected † | integer | Number of consumers affected by the outage. | ON | — |
| date | string | ISO 8601 date the inspection was performed. | EC | — |
| dcArrayCapacity | QVPower | DC-side nameplate capacity of a photovoltaic array at Standard Test Conditions (industry term: "kWp"). For PV systems this is typically larger than the AC-side maxExport because of inverter clipping and DC-to-AC ratios. Relevant for SOLAR_PV resources. The unit is the standard QUDT power alias kW — the STC/peak semantic is documented here, not encoded in the unit string. | EC | IS 16221 (PV module qualification); IEC 61727 (PV grid interface) |
| deEnergized | array | Optional SDP/UsagePoint refs (authenticated tier). | ON | CIM (IEC 61968-3 UsagePoint) |
| defaultMode † | TelemetryMode | Default telemetry mode (READING or USAGE) applied when a request does not specify one. | MD | — |
| description † | string | Free-text description shown to consumers in the public outage information. | ON | — |
| descriptorIndex † | integer | Index of the payload descriptor this override applies to. | MD | — |
| detectedAt | string | When MDMS/SCADA first detected the outage (unplanned). | ON | — |
| detectionRef | Identifier | Reference to the real-time detection record that raised the outage (e.g. a DISCOM RTDAS_DATA_ID). Absence or a "0" sentinel indicates a manually entered outage (source=MANUAL). | ON | — |
| diPort | string | Digital-input port on the substation meter that carried the signal. | ON | — |
| discom † | Identifier | DISCOM identifier in the outage's network-context hierarchy (Identifier: namespace + value). | ON | — |
| district † | string | District or administrative area of the affected network context. | ON | — |
| division † | string | Division (organisational unit) in the DISCOM network hierarchy. | ON | — |
| dueDate † | string | Payment due date of the bill. | MD | — |
| duration | string | ISO 8601 duration string representing the length of the requested data window (e.g., PT15M, P1D, P30D). | MD, MDR, ON | — |
| efficiency | number | Conversion efficiency as a percentage (0–100). Most relevant for FUEL_CELL and CHP resources. | EC | — |
| energized | array | Optional points confirmed still energized. | ON | CIM (IEC 61968-3 UsagePoint) |
| energyCharges | number | Charges for active/reactive energy consumption. | MD | — |
| energyDirection | string | Energy flow direction metered at this point. | EC | CIM (FlowDirectionKind); ESPI NAESB REQ.21 |
| energyResources | array | All physical energy assets for this account. Each entry is discriminated by 'type' into one of seven composable kinds. | EC | — |
| enrolledOn | string | ISO 8601 date the asset was enrolled with the aggregator. | EC | — |
| enterServiceRampTimeSec | number | Seconds to ramp from 0 to rated power after reconnection. | EC | SunSpec DER Model 703 (ESRmpTms) |
| estimatedRestoration | string | ETR (OMS "Estimated Time"). | ON | — |
| eventId | integer; string | Idempotency key of the originating feeder-status event. | MD, ON | — |
| eventName † | string | Human-readable name of the meter event. | MD | — |
| events † | array | Meter event records carried in an EVENT profile (MeterEvent entries). | MD | — |
| extendedAddress | string | Address extension (apt/suite/floor, C/O). | EC | — |
| extensions | object | Namespaced DISCOM-specific fields, e.g. { "discom": { "breakdownId": "6357257", "downType": "FEEDER" } }. | ON | — |
| failCode † | string | Failure/validation code recorded when a reading fails validation. | MD | — |
| faultType | string | Vendor asset/voltage level of the fault, e.g. 33KV, 11KV, DT, LT. | ON | — |
| feeder | string | Feeder identifier this meter is supplied from. | EC | — |
| feederCode | string | Feeder code per utility records. Relevant for FEEDER and DT resources. | EC | — |
| feederStatus | string | Normalized feeder status (local enum); raw vendor code in `rawCode`. Energized/de-energized align with CIM UsagePoint semantics. | ON | — |
| filingDate † | string | Date the filing was submitted to the regulatory commission. | ARR | — |
| filingId | string | Regulatory filing reference number. | ARR | — |
| filingType | string | MYT - Multi-Year Tariff control period filing (multiple years, mix of actual/proposed) ANNUAL - single year or historical year-by-year approved data TRUE_UP - reconciliation of actuals vs previously approved amounts REVISED - amended filing with corrections | ARR | — |
| fiscalYear | string | Fiscal year label. | ARR | — |
| fiscalYears † | array | Fiscal-year blocks of the filing, each carrying its line items (ArrFiscalYear entries). | ARR | — |
| fixedCharges | number | Fixed charges/demand charges. | MD | — |
| flowDirection | string | IMPORT / EXPORT / NONE | MD | — |
| forceMajeure | boolean | OMS "Force Majeure" flag. | ON | — |
| formReference | string | Reference to the supporting sub-form or schedule. | ARR | — |
| formula | string | Human-readable computation formula expressed as references to other lineItemIds. Only present on SUB_TOTAL and ARR items. | ARR | — |
| freqDroopEnabled | boolean | Frequency-Watt droop active. | EC | IEEE 1547-2018; SunSpec DER Model 711 |
| from | string | ISO 8601 UTC date-time indicating the start time of the requested data window. | MDR | — |
| fullName | string | Full name of the customer as per ID proof. | EC | CIM (IEC 61968-1 Customer.name) |
| functions | array | Active meter capabilities. | EC | CIM (IEC 61968-9 EndDeviceFunction) |
| generationCapacityKw | number | Rated power generation capacity (e.g. solar PV inverter capacity) in kW. | MD | — |
| geo | GeoJSONGeometry | Optional inline geometry (WGS84): Point (substation/DT), LineString (feeder route), Polygon (service area). | EC, MD, ON | GeoJSON (RFC 7946), WGS84; GeoJSON (RFC 7946); CAP area |
| geometries | array | Member geometries when `type` is **GeometryCollection**. | EC | — |
| grantee | string | URI/DID of the authorized entity. | MDR | — |
| grantor | string | URI/DID of the entity authorizing access. | MDR | — |
| head | string | Short heading as used in the regulatory form. Varies by DISCOM — use the original text from the filing. | ARR | — |
| headline † | string | Short public-facing headline of the outage notice. | ON | — |
| id | Identifier; integer; string | Stable identifier for this resource. For METER resources the meter serial number is conventional. | ARR, EC, MD, MDC, MDRC, ON | — |
| idRef † | IdRef | External identity reference (IdRef) for the customer or issuer. | EC | — |
| impact † | OutageImpact | Impact of the outage (OutageImpact: customers affected, assets, area). | ON | — |
| inspection | object | Commissioning / safety inspection record for the asset. Captured by the distribution licensee at energisation and on re-certification events. | EC | IEEE 1547-2018 Cl. 11 (commissioning); CEA Connectivity Regs 2013 (amended 2018) |
| inspectorId | string | Identifier of the inspector or inspecting body, as recorded by the licensee. | EC | — |
| installationAddress | Location | Physical location of the metered installation. geo (GeoJSON Point, coordinates [longitude, latitude]) is required; address (schema.org PostalAddress fields) is optional. | EC | GeoJSON RFC 7946; schema.org PostalAddress; CIM (IEC 61968-1 ServiceLocation) |
| instruction | string | What the consumer should do. | ON | — |
| integrationPeriod | string | Demand integration period, e.g. PT30M or PT15M. | MD | — |
| intervalPeriod | IntervalPeriod | IntervalPeriod | MD | — |
| intervals | array | list of Interval | MD | — |
| issuedAt † | string | Date-time at which the notice was first issued. | ON | — |
| issuedBy | Party; string | DID or URI of the issuing authority. | EC, ON | — |
| issuer † | object | DID/URI (with optional external identity reference) of the DISCOM issuing the credential. | EC | W3C Verifiable Credentials |
| language | string | BCP-47, e.g. en, hi. | ON | — |
| lastUpdatedAt † | string | Date-time at which the notice was last updated. | ON | — |
| licensee | string | Full name of the distribution licensee. | ARR | — |
| licenseeCode | string | Short code for the licensee. | ARR | — |
| lineItemId | string | Stable identifier for this line item across years. Use kebab-case, e.g., "power-purchase-cost", "interest-working-cap". | ARR | — |
| lineItems † | array | Cost and revenue line items of the fiscal year (ArrLineItem entries). | ARR | — |
| loadCategory | string | Functional category of this load. | EC | CIM (IEC 61970-301 ConformLoad classification) |
| location | Location | Physical location of this asset. | EC | — |
| magnitude † | number | Measured magnitude associated with the event (e.g. voltage during a sag). | MD | — |
| make | string | Manufacturer (free text). | EC, MD | — |
| maxExport | QVPower | Maximum power this resource injects to the grid (generates/discharges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max discharge rate. Supersedes ratedPower. | EC | CIM (IEC 61970 GeneratingUnit.maxOperatingP; IEC 61970-302 PowerElectronicsConnection.maxP, injection) |
| maxHistoryDuration | string | Maximum length of historical data window supported by the provider. | MDR | — |
| maxImport | QVPower | Maximum power this resource draws from the grid (absorbs/charges). Always ≥0. For bidirectional resources (BESS, V2G) this is the max charge rate. | EC | CIM (IEC 61970-302 PowerElectronicsConnection.maxP, absorption) |
| maxReactivePower | QVReactivePower | Maximum reactive power injection (leading / over-excited). Replaces maxReactivePowerKvar from v1.0. | EC | SunSpec DER Model 702 (maxVar); CIM (IEC 61970-302 PowerElectronicsConnection.maxQ) |
| maxRecordsShared | integer | Maximum number of records that should be shared or returned in a single batch/page. | MDR | — |
| meterCapability | string | Communication/automation generation. Electromechanical: induction-disc. CMRI: manual optical-port (India legacy). AMR: one-way automated read. AMI: two-way smart meter. | EC | CIM (IEC 61968-9 AmiBillingReadyKind) |
| meterCategory | MeterCategory | A / B / C / D1 / D2 / D3 / D4 | MD | — |
| meterData | schema.json | The attested meter data payload. May be a single EnergyData profile or an array of profiles per MeterData v0.6. | MDC | — |
| meterDataRequest | schema.json | The scoped, time-bounded data request. Specifies the meter resources, hierarchical scope, time window, and profile types being requested. The provider validates this against its capability profile before fulfilling delivery. | MDRC | — |
| meterId | string | Matches the id of a METER entry in customerProfile.energyResources[]. | EC | — |
| meterRef | Identifier | Feeder/substation smart-meter number — join key to MDMS/MeterData. | ON | — |
| meterRefs † | IdentifierList | References to the meters (IdentifierList) this profile or association covers. | MD | — |
| meters † | array | Meter device inventory for the customer (Meter entries). | MD | — |
| meterType | MeterType | AMR / AMI / Electromechanical / Forward / Reverse / Bidirectional / Prepaid / NetMeter / Other | MD | — |
| minReactivePower | QVReactivePower | Maximum reactive power absorption (lagging / under-excited). Value is typically negative. Replaces minReactivePowerKvar from v1.0. | EC | SunSpec DER Model 702 (maxVarNeg); CIM (IEC 61970-302 PowerElectronicsConnection.minQ) |
| mode | TelemetryMode | The telemetry mode (READING, USAGE) supported or requested for this register. | MDR | — |
| model | string | Model of the meter. | EC, MD | — |
| msgType | string | Message type; UPDATE/CANCEL refer to a prior notice via `references`. | ON | OASIS CAP v1.2 (alert/msgType) |
| multiplier | number | Decimal scaling factor (e.g. 0.001 for milli, 1000 for kilo). Default value is 1. | MD, MDR | — |
| name | string | Name of the care-of / reference person used to disambiguate the customer. | EC, MD, ON | — |
| namespace † | string | Authority or namespace that scopes the identifier value. | MD, ON | — |
| network | OutageNetworkContext | OutageNetworkContext | ON | — |
| nominalPower | QVPower | Nominal (nameplate) power output. Use when distinct from maxExport (peak). | EC | CIM (IEC 61970 GeneratingUnit.nominalP) |
| nominalVoltage | QVVoltage | Nominal operating voltage. Replaces nominalVoltageKv from v1.0. | EC | CIM (IEC 61970-301 BaseVoltage.nominalVoltage) |
| notes | array | Footnotes, regulatory order references, and explanatory notes. | ARR | — |
| obis | string | Optional canonical OBIS code when readingType uses a short code. | MD | — |
| objectType † | string | Discriminator constant naming the payload type (ARR_FILING / OUTAGE_NOTIFICATION). | ARR, ON | — |
| occurredAt † | string | Timestamp at which the reading or override took effect. | MD | — |
| openingValue | number | MUST ONLY be provided when the associated payload descriptor specifies reportedMode=USAGE. | MD | — |
| operatingMode | string | Inverter grid-interaction mode. GridFollowing: PLL-based sync. GridForming: own V/f reference (microgrid islanding, black-start). Standby: energised but not injecting. | EC | CIM (IEC 61970-302 PowerElectronicsConnection.inverterMode) |
| otherCharges | number | Other taxes, duties, surcharges, or adjustments. | MD | — |
| outageClass | string | Outage class, from the DISCOM OMS "Down Info" set (local, additive enum). Rostering = rotational load-shedding (scheduled vs emergency). Restoration is a status transition (status=RESTORED), not a class. | ON | — |
| overrides | array | list of Override | MD | — |
| parentRef | Identifier | Parent asset (e.g. a feeder's substation, a DT's feeder). | ON | — |
| parentResources | array | List of parent resources (such as feeders or DTs) for this association, replacing feederId and dtId. | EC, MD | — |
| particulars | string | Detailed description or the "Particulars" column value. Useful when head alone is ambiguous (e.g., "Others" head with "Incentive/Disincentive on achievement of norms" as particulars). | ARR | — |
| payloadDescriptors † | array | Column definitions (PayloadDescriptor entries) in this descriptor set. | MD | — |
| payloadDescriptorSetRef | string | Reference ID matching a previously exchanged PayloadDescriptorProfile's payloadDescriptorSet. | MD | — |
| payloadDescriptorSets † | array | Descriptor sets published in a PAYLOAD_DESCRIPTOR profile. | MD | — |
| payloads | array | list of number / string / boolean | MD | — |
| paymentMode | string | Billing/payment modality. POSTPAID: consume now, pay later. PREPAID: pay-before-use. | EC, MD | CIM (IEC 61968-9 AmiBillingReadyKind, ESPI) |
| paymentStatus | string | Status of the payment, e.g. PAID, UNPAID, PARTIAL. | MD | — |
| period | TimePeriod | Outage window (Down From + duration). | ON | — |
| phase | Phase | NONE / R / Y / B / ABC | MD | — |
| postalCode | string | Postal/ZIP code. | EC | — |
| premisesType | string | Type of premises at the metering point. | EC | — |
| prepaidBalance | number | Prepaid remaining balance/credit amount on the account/meter, if applicable. | MD | — |
| profiles | array | List of profiles and their specific values/modes. | MDR | — |
| profileType † | string | Discriminator naming the profile (CUSTOMER, INTERVAL, DAILY, MONTHLY, BILL_DETAILS, INSTANTANEOUS, EVENT, ALARM, PAYLOAD_DESCRIPTOR). | MD, MDR | — |
| proof † | object | Cryptographic proof that makes the credential tamper-evident and verifiable. | EC | W3C VC Data Integrity |
| proofPurpose † | string | Purpose of the proof: assertionMethod or authentication. | EC | W3C VC Data Integrity |
| proofValue † | string | Encoded signature value of the proof. | EC | W3C VC Data Integrity |
| provenance | OutageProvenance | OutageProvenance | ON | — |
| publicInfo | OutagePublicInfo | OutagePublicInfo | ON | — |
| purpose | string | Reason/purpose for data access. | MDR | — |
| ratedApparentPower | QVApparentPower | Rated apparent power. Replaces ratedApparentPowerKva from v1.0. | EC | SunSpec DER Model 702 (maxVA); CIM (IEC 61970-302 PowerElectronicsConnection.ratedS) |
| ratedPower | QVPower | Manufacturer-rated peak power (nameplate value in principal direction). Kept for backward compatibility — prefer maxExport. | EC | CIM (IEC 61968-9 EndDeviceInfo.ratedPower; IEC 61970 GeneratingUnit.maxOperatingP) |
| rawCode | string | Vendor-native status code as received (e.g. FEEDER_STATUS=102), for traceability. | ON | — |
| readings | array | Granular capabilities for specific registers and metrics. If omitted, all readings under this profile are supported. | MD, MDR | — |
| readingType † | string | OBIS code or short code identifying the measured quantity. | MD | IEC 62056 / DLMS |
| references | array | Prior notice ids this message updates or cancels (CAP `references`). | ON | OASIS CAP v1.2 (alert/references) |
| regulatoryCommission | string | SERC or Joint ERC that receives the filing. | ARR | — |
| relationship | string | Gender-neutral relationship of the reference person to the customer. | EC | — |
| reportedMode | TelemetryMode | READING / USAGE | MD | — |
| resources | array | List of resource URIs/DIDs (e.g. meter DIDs, service point IDs) to query (optional). | MDR | — |
| resourceStatus | string | e.g. PENDING, RESOURCE_ALLOCATED, IN_PROGRESS. | ON | — |
| response | OutageResponse | OutageResponse | ON | — |
| result | string | Inspection outcome. 'conditional' indicates pass subject to remedial action. | EC | — |
| rideThroughCategory | string | Abnormal operating performance category. CategoryI: basic. CategoryII: enhanced for distribution-connected DER. CategoryIII: advanced for large/transmission-connected DER. | EC | IEEE 1547-2018 (ride-through category) |
| roundTripEfficiencyPct | number | AC-to-AC round-trip efficiency as a percentage (0–100): the fraction of energy returned to the grid relative to energy drawn during a full charge/discharge cycle. Distinct from stateOfHealthPct (cumulative life indicator) and from inverter conversion efficiency. | EC | IEC 62933-2-1 (performance test method) |
| sanctionedExportLoad | QVPower | Sanctioned/approved grid export limit. | EC | — |
| sanctionedExportLoadKw | number | Sanctioned/approved grid export limit in kW. | MD | — |
| sanctionedLoad | QVPower | Sanctioned/approved import load. | EC | CIM (IEC 61968-9 UsagePoint) |
| sanctionedLoadKw † | number | Sanctioned/approved electrical load for the connection, in kW. | MD | — |
| scheme | IdentifierScheme; string | Identifier scheme (mixed provenance). MRID and DID are borrowed from their standards; the rest are local vendor/DISCOM master keys. | MD, ON | MRID: CIM (IEC 61968/61970); DID: W3C DID Core |
| scope | ScopeType | ResourceOnly / ResourceAndChildren / ChildrenOnly | MDR | — |
| sequence † | integer | Sequence number of the event within its timestamp. | MD | — |
| sequenceItems † | array | Ordered columns of the compact sequence (SequenceItem entries). | MD | — |
| serialNumber | integer; string | Manufacturer-assigned device serial number from the equipment nameplate. Distinct from id (which is the network-issued DID). | ARR, EC | CIM (IEC 61968-9 EndDeviceInfo.serialNumber) |
| serviceConnectionDate | string | Date and time the service connection was activated, with timezone offset (ISO 8601). | EC | CIM (IEC 61968-1 ServiceLocation activation date) |
| serviceDeliveryPointRefs | IdentifierList | IdentifierList | MD | — |
| serviceDeliveryPoints † | array | Service delivery points of the customer (ServiceDeliveryPoint entries). | MD | — |
| serviceKind | ServiceKind | ELECTRICITY / GAS / WATER / HEAT | MD | — |
| serviceStatus | string | Lifecycle state of the service connection (the UsagePoint), not of the meter device itself. 'active' = currently energised and billable; 'suspended' = temporarily disconnected (non-payment, inspection, fault) with the contract still on record; 'closed' = permanently terminated. Distinct from the meter device's operational state. | EC | CIM (IEC 61968-9 UsagePoint.status) |
| severity | string | Severity of the outage. | MD, ON | OASIS CAP v1.2 (info/severity) |
| shortLabel † | string | Short display label for the reading. | MD | — |
| signal † | OutageSignal | Real-time detection signal behind the outage record (OutageSignal). | ON | — |
| slaTargetMinutes | integer | SLA target, e.g. 240 (4 hrs). | ON | — |
| source | ReadingSource; string | System that raised this notice (local enum; RTDAS = Real-Time Data Acquisition System). | MD, ON | — |
| start † | string | Start of the time period (ISO 8601 date-time). | MD, ON | ISO 8601 |
| stateOfHealthPct | number | Battery state-of-health as a percentage (0–100). | EC | — |
| stateProvince † | string | State or union territory of the filing licensee. | ARR | — |
| status | string | Outage lifecycle state. LOCAL enum (not from a published standard); loosely aligned with the CIM Outage lifecycle. | ARR, MD, ON | — |
| statusListCredential † | string | URI of the status-list credential used to check revocation or suspension. | EC | W3C VC Status List |
| statusPurpose † | string | Whether the status entry expresses revocation or suspension. | EC | W3C VC Status List |
| storageCapacity | QVEnergy | Rated stored-energy capacity. Replaces storageCapacityKwh from v1.0. | EC | CIM (IEC 61970-302 BatteryUnit.ratedE) |
| storageCapacityKw | number | Rated energy storage capacity in kWh. | MD | — |
| storageType | string | Battery storage technology type. | EC | — |
| streetAddress | string | Street address (building name/number and street). | EC | — |
| subCategory | string | Functional sub-classification for analysis and comparison across DISCOMs. | ARR | — |
| subcategory | string | Standardized cause subcategory; must be valid for the chosen `category` (see $comment for the mapping). Leave unset if the field finding is inconclusive. | ON | IEEE 1782-2022 §4.5 |
| subdivision † | string | Subdivision (organisational unit) in the DISCOM network hierarchy. | ON | — |
| subjectId | string | Subject identifier in authority-domain:id-value format. | EC | — |
| subResources | array | Topology — child resources. Each item is EITHER a bare id string OR an inline EnergyResource object. | EC | — |
| substation † | Identifier | Substation identifier in the network context (Identifier: namespace + value). | ON | — |
| substationId | string | Parent substation identifier per utility records. | EC | — |
| supportedModes † | array | Telemetry modes (READING/USAGE) this reading supports. | MD | — |
| supportedScopes | array | Hierarchical scopes supported by the query processor. | MDR | — |
| tariffCategoryCode | string | Billing/tariff category code assigned by the utility. | EC, MD | CIM (IEC 61968-9 UsagePoint.serviceCategory) |
| telemetryProvider | string | Telemetry provider for this meter-service association. | EC, MD | — |
| text | string | Free-text localities (CAP areaDesc), e.g. "SEC-14, 9, 11 Rajnagar". | ON | — |
| timePeriod † | TimePeriod | Time period the record covers (TimePeriod: start/end). | MD | ISO 8601 |
| timestamp † | string | Timestamp of the record (ISO 8601 date-time). | MD, ON | ISO 8601 |
| timeZone | string | IANA time-zone, e.g. Asia/Kolkata. | MD | — |
| timing † | OutageTiming | Outage timing (OutageTiming: detection, outage window, estimated and actual restoration). | ON | — |
| touBuckets | array | list of TouBucket | MD | — |
| touZone † | integer | Time-of-use zone number the reading belongs to. | MD | — |
| type | array; string | Asset-class discriminator. DT → PowerTransformer, BUS → BusbarSection, FEEDER → Feeder (EquipmentContainer), MICROGRID → Substation / microgrid container (IEC 61970-301). | EC | — |
| unit | UnitOfMeasure; string | kWh / kVAh / kvarh / kW / kvar / kVA / V / A / Hz / PF / NONE / INR / USD | EC, MD | — |
| unitScale | string | Scale of all amounts in the filing. | ARR | — |
| v2xProtocol | string | Vehicle-to-Grid / V2X protocol. Present only for EV_V2G resources. | EC | — |
| validationStatus | ValidationStatus | VALID / ESTIMATED / MANUAL / SUSPECT / REJECTED | MD | — |
| validFrom | string | ISO 8601 UTC date-time indicating when the authorization becomes valid. | EC, MDR | — |
| validUntil | string | ISO 8601 UTC date-time indicating when the authorization expires. | EC, MDR | — |
| value | number; string | The OBIS code (e.g. 1.0.1.8.0.255) or short code (e.g. kWh imp) representing the register. | EC, MD, MDR, ON | — |
| verificationMethod † | string | URI of the key / verification method used to verify the proof. | EC | W3C VC Data Integrity |
| voltageLevel | string | e.g. 33kV, 11kV, LT, DT. | ON | — |
| voltVarEnabled | boolean | Volt-VAr curve active. | EC | IEEE 2030.5 (opModVoltVar); SunSpec DER Model 705 |
| yearType | string | BASE_YEAR - reference year in an MYT filing (typically the year before the control period) CONTROL_PERIOD - a year within the MYT control period being filed for HISTORICAL - a past year with finalized data (used in annual/historical filings) | ARR | — |
| zone | integer; string | Operating zone or region identifier used by the utility. | EC, MD, ON | — |

## Table D.2 — Named types (90)

| Term | Type | Definition | Schema | Source standard |
|---|---|---|---|---|
| AccumulationBehaviour † | string | How a reading value accumulates over time: CUMULATIVE, DELTA, INSTANTANEOUS, SUMMATION or INDICATING. | MD | — |
| Address | Address; object | **Postal address** aligned with schema.org `PostalAddress`. Use for human-readable addresses. Geometry lives in `Location.geo` as GeoJSON. | EC, MD | — |
| AlarmProfile | object | Real-time active indicators/alerts representing immediate state conditions from the meter. | MD | — |
| ArrFiscalYear | object | ARR data for a single fiscal year. The combination of yearType + amountBasis captures what the numbers represent: e.g., a BASE_YEAR with AUDITED amounts, or a PROJECTION year with PROPOSED amounts. | ARR | — |
| ArrLineItem | object | A single cost, income, subtotal, or adjustment line item. The schema accommodates varying granularity across DISCOMs: - O&M may be one line (consolidated) or split into Employee Costs, Admin & General, Repair & Maintenance - Return may appear as Return on NFA, Return on Equity, or Return on Capital Base depending on SERC regulations - Some years may have items not present in others (e.g., Incentive/Disincentive, DSM Provision, O&M sharing gains) | ARR | — |
| Association † | object | Links a customer's service delivery points, meters and parent network resources, with telemetry provider, commissioning date and generation/storage capacity. | MD | — |
| BaseProfile | object | Root base profile carrying common identifiers across all shapes. | MD | — |
| BillDetails | object | Utility billing computed details, such as billing amount, bill number, due dates, and prepaid balance. | MD | — |
| CompactSequence † | object | Named, ordered list of readingType/attribute pairs enabling compact array-form telemetry rows. | MD | — |
| ConsumptionProfile | object | Tariff and regulatory load profile for one meter connection. meterId links to a METER entry in customerProfile.energyResources[]. Uses MeterServiceProfile/v1.1 (sanctionedLoad, contractMaxDemand as QuantitativeValue). | EC | — |
| Customer † | object | Customer master record: id, name, consumer category, sanctioned load, billing cycle, payment mode, connection type, contract demand, tariff category. | MD | — |
| CustomerDetails | object | PII section — fullName, installationAddress, serviceConnectionDate. fullName appears ONLY here — never in customerProfile or resource entries. Defined in CustomerDetails/v1.0. | EC, MD | — |
| CustomerProfile | object | Non-PII customer identity and asset list. Supports arbitrary topologies: a single customerNumber may span multiple METER entries (different premises, sub-meters, parallel meters) each with child DERs. | EC, MD | — |
| DailyProfile | object | Daily Load Profile — P1D intervalBlocks. Same per-meter shape as IntervalProfile. | MD | — |
| EnergyData | object | A single compact data-only profile record. Must be one of the eight standard types. | MD | — |
| EnergyResource | oneOf | Discriminated union of all seven typed EnergyResource kinds, each inheriting id, type, subResources, parentResources, and attributes from EnergyResourceCommon/v1.1. All power/capacity fields use QuantitativeValue. Defined in EnergyResource/v2.1. | EC | — |
| EnergyResourceCommon | object | Structural envelope inherited by every typed EnergyResource kind via allOf. Defines top-level fields common to all kinds: id, type, topology (subResources, parentResources), and the attributes bag. | EC | — |
| EnergyResourceCommonAttributes | object | Dimensioning and provenance fields shared by all resource kinds. Inherited inside each kind's attributes bag via allOf. No field is required at this level. | EC | — |
| EnergyResourceEVCharger | EnergyResourceCommon | An EV charging station (EVSE) energy resource. EV_V2G adds bidirectional Vehicle-to-Grid capability per ISO 15118-20 / OCPP 2.1 BPT. CIM: ElectricVehicleChargingStation (CIM17+). | EC | — |
| EnergyResourceEVChargerAttributes | EnergyResourceCommonAttributes | Attributes for EV_CHARGER and EV_V2G resources. Common fields (make, model, ratedPower, maxExport, maxImport, telemetryProvider, commissioningDate, location) are inherited from EnergyResourceCommon/v1.1 via allOf. | EC | — |
| EnergyResourceGenerator | EnergyResourceCommon | A generation DER energy resource (SOLAR_PV, WIND, HYDRO, BIOGAS, CHP, FUEL_CELL). CIM: GeneratingUnit subtypes (IEC 61970-301). | EC | — |
| EnergyResourceGeneratorAttributes | EnergyResourceCommonAttributes | Attributes for generation DER resources. Common fields inherited from EnergyResourceCommon/v1.1 via allOf. | EC | — |
| EnergyResourceInverter | EnergyResourceCommon | A grid-connected power-electronics inverter energy resource. Captures IEEE 1547-2018 ride-through categories, operating mode, and reactive / frequency-support capabilities. CIM: PowerElectronicsConnection (IEC 61970-302). | EC | — |
| EnergyResourceInverterAttributes | EnergyResourceCommonAttributes | Attributes for INVERTER resources. Common fields (make, model, ratedPower, maxExport, maxImport, telemetryProvider, commissioningDate, location) are inherited from EnergyResourceCommon/v1.1 via allOf. | EC | — |
| EnergyResourceLoad | EnergyResourceCommon | A controllable load energy resource (smart HVAC, smart water heater, or generic controllable load). CIM: EnergyConsumer / ConformLoad (IEC 61970-301). | EC | — |
| EnergyResourceLoadAttributes | EnergyResourceCommonAttributes | Attributes for controllable load resources. Common fields (make, model, ratedPower, maxExport, maxImport, telemetryProvider, commissioningDate, location) are inherited from EnergyResourceCommon/v1.1 via allOf. | EC | — |
| EnergyResourceMeter | EnergyResourceCommon | A metering-point energy resource. Anchors all DER sub-resources behind it in the topology tree. CIM: cim:Meter (IEC 61968-9). | EC | — |
| EnergyResourceMeterAttributes | EnergyResourceCommonAttributes | Attributes for METER resources. Common power fields (ratedPower, maxExport, maxImport, make, model, telemetryProvider, commissioningDate, location) inherited from EnergyResourceCommon/v1.1 via allOf. | EC | — |
| EnergyResourceNetwork | EnergyResourceCommon | A grid-network infrastructure energy resource (distribution transformer, busbar, feeder, or microgrid). Topology containers that anchor metering points and DER resources. CIM: PowerTransformer, BusbarSection, Feeder, Substation (IEC 61970-301). | EC | — |
| EnergyResourceNetworkAttributes | EnergyResourceCommonAttributes | Attributes for grid-network infrastructure resources. Common fields (make, model, ratedPower, maxExport, maxImport, telemetryProvider, commissioningDate, location) are inherited from EnergyResourceCommon/v1.1 via allOf. | EC | — |
| EnergyResourceStorage | EnergyResourceCommon | A stationary battery energy storage resource (BESS). CIM: BatteryUnit (IEC 61970-302). | EC | — |
| EnergyResourceStorageAttributes | EnergyResourceCommonAttributes | Attributes for BESS resources. Common fields (make, model, ratedPower, maxExport, maxImport, telemetryProvider, commissioningDate, location) are inherited from EnergyResourceCommon/v1.1 via allOf. | EC | — |
| EventProfile | object | IS 15959 event log for one meter over a coverage period. | MD | — |
| GeoJSONGeometry | GeoJSONGeometry; object | **GeoJSON geometry** per RFC 7946. Coordinates are in **EPSG:4326 (WGS-84)** and MUST follow **[longitude, latitude, (altitude?)]** order. Supported types: - Point, LineString, Polygon - MultiPoint, MultiLineString, MultiPolygon - GeometryCollection (uses `geometries` instead of `coordinates`) Notes: - For rectangles, use a Polygon with a single linear ring where the first and last positions are identical. - Circles are **not native** to GeoJSON. For circular searches, use `SpatialConstraint` with `op: s_dwithin` and a Point + `distanceMeters`, or approximate the circle as a Polygon. - Optional `bbox` is `[west, south, east, north]` in degrees. | EC, MD | — |
| Identifier | object | Canonical {scheme, value} reference. Used for customer/meter/SDP/OBIS references. | MD, ON | — |
| IdentifierList | array | Non-empty list of Identifiers for the same underlying entity. First element is the primary; additional elements are alternates under different schemes. | MD | — |
| IdentifierScheme † | string | Naming scheme of an identifier: METER_SERIAL, METER_BADGE, MRID, OBIS, SHORT_CODE, CONSUMER_NUMBER, SERVICE_DELIVERY_POINT, DID, ORG or OTHER. | MD | — |
| IdRef | object | External identity reference for the customer. Defined in IdRef/v1.0. | EC | — |
| InstantaneousProfile | object | Snapshot of a meter's electrical quantities at one captured moment. | MD | — |
| Interval | object | One time-series interval row. payloads[k] is the value for compactSequence[k]. | MD | — |
| IntervalPeriod | object | Period defined by a start time and a duration. | MD | — |
| IntervalProfile | object | Block Load Survey — PT15M / PT30M cadence intervalBlocks for one meter. | MD | — |
| Location | object | A place represented by GeoJSON geometry and optional address. Source: main/schema/core/v2/attributes.yaml#Location | EC | — |
| Meter † | object | Meter device record: id, make, model, meterType, meterCategory, serviceKind. | MD | — |
| MeterAlarm † | object | Single alarm record: timestamp, alarmId, alarmName, status, severity. | MD | — |
| MeterCategory † | string | Indian meter category: A, B, C, D1, D2, D3 or D4. | MD | BIS / IS |
| MeterDataAuthorisation | object | Attestation details authorizing an entity to access specific capabilities. | MDR | — |
| MeterDataCapabilities | object | Capabilities of a meter data provider, detailing supported profiles, values, scopes, and durations. | MDR | — |
| MeterDataCredentialSubject | object | The subject of the credential: the consumer or asset entity whose meter data is attested. | MDC | — |
| MeterDataRequestCredentialSubject | object | The subject of the credential: the requesting entity and the specific MeterDataRequest they are authorised to make. | MDRC | — |
| MeterDataRequestObject | object | Request parameters for selecting smart meter telemetry and profiles. | MDR | — |
| MeterEvent † | object | Single event record: timestamp, eventId, eventName, phase, sequence, magnitude, duration. | MD | — |
| MeterType | string | Type of electricity meter. Shared with ElectricityCredential schema. | MD | — |
| MonthlyProfile | object | Monthly profile readings from the meter at billing reset time (billing history). | MD | — |
| OutageAffectedArea | object | CAP area block — free text plus structured admin areas plus GIS geometry. | ON | — |
| OutageAlarmRef | object | Pointer to a MeterData AlarmProfile entry (meter + alarmId + timestamp). | ON | — |
| OutageAsset | object | A network asset affected by the outage. Generic across feeder, DT, substation, and line so new asset levels are additive. | ON | — |
| OutageCause | object | Three-layer cause: a `category` + `subcategory` aligned to IEEE 1782-2022 (the standardized, cross-DISCOM dimension) plus the vendor/OMS `code` carried verbatim (for fidelity) and free-text `text` (ODIN-style). | ON | — |
| OutageImpact | object | CIM-aligned affected service points and customer counts (feeds SAIDI/SAIFI). | ON | — |
| OutageNetworkContext | object | DISCOM org hierarchy: Discom > Zone > Circle > Division > Subdivision > Substation. All optional for flat utilities. | ON | — |
| OutageProvenance | object | Link to the smart-meter alarm(s)/signal that triggered or confirmed the outage. | ON | — |
| OutagePublicInfo | object | CAP info block — human-readable text for web publishing and push. | ON | — |
| OutageResponse | object | Field-response and consumer-impact tracking from the OMS. | ON | — |
| OutageSignal | object | Raw real-time feeder-status signal that triggered detection. | ON | — |
| OutageTiming | object | Outage window and restoration timing. One canonical TimePeriod; end is derived. | ON | — |
| Override | object | Sparse — inject timestamps, zones, or validation states into specific interval cells. | MD | — |
| Party | object | An organisation or contact (e.g. the issuing DISCOM). | ON | — |
| PayloadDescriptor | object | One quantity declared once per block; rows' values[] align positionally with descriptors[]. | MD | — |
| PayloadDescriptorProfile | object | Configuration profile representing a collection of Payload Descriptor Sets exchanged out-of-band or embedded in an array. | MD | — |
| PayloadDescriptorSet † | object | Named set of payload descriptors plus compact sequences describing the layout of telemetry rows. | MD | — |
| Phase † | string | Electrical phase indicator: NONE, R, Y, B or ABC. | MD | — |
| ProfileCapability | object | Declares capabilities for a specific profile class. | MDR | — |
| QVApparentPower | object | Apparent-power quantity {value, unit}. unit is a QUDT apparent-power alias (kVA, MVA) expanded to a QUDT IRI via the JSON-LD context. | EC | — |
| QVEnergy | object | Energy quantity {value, unit}. unit is a QUDT energy alias (kWh, MWh) expanded to a QUDT IRI via the JSON-LD context. | EC | — |
| QVPower | object | Active-power quantity {value, unit}. unit is a QUDT power alias (W, kW, MW) expanded to a QUDT IRI via the JSON-LD context. | EC | — |
| QVReactivePower | object | Reactive-power quantity {value, unit}. unit is a QUDT reactive-power alias (kVAR, MVAR) expanded to a QUDT IRI via the JSON-LD context. value may be negative (absorption). | EC | — |
| QVVoltage | object | Voltage quantity {value, unit}. unit is a QUDT voltage alias (V, kV) expanded to a QUDT IRI via the JSON-LD context. | EC | — |
| Reading | object | Detailed, self-contained inline reading with full metadata support. | MD | — |
| ReadingDefinition † | object | Declares one supported reading: readingType, supported modes, default mode, unit, phase, flow direction, accumulation behaviour, ToU zone. | MD | — |
| ReadingSource † | string | Origin of a reading: METER, HES, ESTIMATED, MANUAL, IMPORT, MDM_COMPUTED or CIS_COMPUTED. | MD | — |
| ScopeType † | string | Hierarchical query scope: ResourceOnly, ResourceAndChildren or ChildrenOnly. | MDR | — |
| SequenceItem † | object | One column of a compact sequence: a readingType plus the attribute it maps to. | MD | — |
| ServiceDeliveryPoint † | object | Service delivery point: id, postal address and geographic location. | MD | — |
| ServiceKind † | string | Metered commodity: ELECTRICITY, GAS, WATER or HEAT. | MD | — |
| TelemetryMode † | string | Telemetry mode of a value: READING (register snapshot) or USAGE (consumption over an interval). | MD, MDR | — |
| TimePeriod | object | Period defined by a start time and an ISO-8601 duration. | MD, ON | — |
| TouBucket | object | Time of Use bucket separating readings by zone. | MD | — |
| UnitOfMeasure † | string | Unit of a reported value: kWh, kVAh, kvarh, kW, kvar, kVA, V, A, Hz, PF, NONE, INR or USD. | MD | — |
| ValidationStatus † | string | Validation state of a reading: VALID, ESTIMATED, MANUAL, SUSPECT or REJECTED. | MD | — |
| ValueCapability | object | Declares capabilities for a specific register/reading within a profile. | MDR | — |

† Definition supplied editorially from the schema structure — field context, enumerations, referenced types. The published source defines the shape but carries no prose definition for the term.

## Notes on specific terms

| Term | Note |
|---|---|
| `discom` vs `DISCOM` | Lowercase `discom` is the published OutageNotification network-context field and is retained. Uppercase DISCOM is a glossary concept and is not a schema term. |
| `circle` | The Circle organisational unit of the DISCOM network hierarchy — not the retired Beckn geo-fence shape. |
| `subCategory` / `subcategory` | Both retained: `subCategory` (ArrFiling v0.5) and `subcategory` (OutageNotification v0.1) are distinct fields of different families. |
| Unit-suffixed fields | ElectricityCredential v1.2 renamed eleven of them — `ratedPowerKw` to `ratedPower`, `storageCapacityKwh` to `storageCapacity`, `sanctionedLoadKw` to `sanctionedLoad`, and others. Only the current names appear above. |
| `storageCapacityKw` (MeterData v0.6) | Known defect in the source schema: the field name says kW while the published definition reads "Rated energy storage capacity in kWh". Carried as published. |
