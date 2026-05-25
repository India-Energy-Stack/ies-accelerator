# MeterData v0.6 User Guide

This user guide explains how to design, exchange, and process `MeterData` v0.6 payloads within modern utility architectures, including Head-End Systems (HES), Meter Data Management (MDM) platforms, and Billing systems.

---

## 1. Architectural Roles & Telemetry Exchange

In standard smart metering infrastructure, data flows from the physical meters up to business applications. The `MeterData` schema maps to each interface:

```mermaid
graph TD
    M[Smart Meter] -->|DLMS/COSEM| HES[Head-End System]
    HES -->|Compact IntervalProfile| MDM[Meter Data Management]
    MDM -->|Elaborated MonthlyProfile| Billing[Billing System]
    MDM -->|EventProfile| Analytics[Tamper Analytics]
```

### A. Head-End System (HES) to MDM
- **Use Case**: Periodic collection of daily load profiles or raw 15-minute load survey intervals.
- **Recommended Profile**: [`IntervalProfile`](./examples/IntervalProfile.json) or [`DailyProfile`](./examples/DailyProfile.json) using **Form B (Compact Matrix)**.
- **Why**: Head-End systems handle millions of meters. Emitting compact arrays of numbers with a single shared descriptor set minimises network ingress, compression overhead, and database insertion time.

### B. MDM to Billing System / CIS
- **Use Case**: Handing off the monthly billing determinants (active/apparent energy, peak demand, Time-of-Use buckets) to generate customer bills.
- **Recommended Profile**: [`MonthlyProfile`](./examples/MonthlyProfile.json) or [`MDM_MonthlyProfile`](./examples/MDM_MonthlyProfile.json) using **Form A (Elaborated)**.
- **Why**: Billing systems process records once a month per customer. Clarity, auditability, and validation state are critical. Utilizing Elaborated representations with explicit modes (`USAGE` mode for energy delta readings) and mathematical proofs (`openingValue` / `closingValue`) prevents billing errors and maintains an auditable trail.

### C. Billing / CIS to Consumer Applications
- **Use Case**: Presenting computed billing details, prepaid balances, and historical consumption summaries to customer portals or mobile apps.
- **Recommended Profile**: [`BillDetails`](./examples/BillDetails.json) (often referred to as commercial billing profile details) or [`CustomerBillingSummary`](./examples/CustomerBillingSummary.json).

---

## 2. Capability Advertisement with `MeterDataRequest`

To establish a contract of what telemetry data can be shared or requested, systems use the [`MeterDataRequest`](../../MeterDataRequest/v0.5/README.md) schema.

* **Capability Advertising**: A Data Provider (BPP, such as an MDM or HES) advertises the profile types, cadences, and OBIS registries it supports by publishing query allowance templates.
  * For example, the BPP can publish a capability profile for billing determinants ([`MeterDataRequest_Billing_Capability.json`](../../MeterDataRequest/v0.5/examples/MeterDataRequest_Billing_Capability.json)) or load survey limits ([`MeterDataRequest_MDM_Capability.json`](../../MeterDataRequest/v0.5/examples/MeterDataRequest_MDM_Capability.json)).
* **Precise Scoping**: Data Consumers query BPP data exchange nodes with a matching request specifying target meters, parameters, and time ranges. This ensures access control is enforced based on consent policies.

---

## 3. Integration Guidelines and Key Scenarios

### Scenario A: Periodic Load Surveys (HES / MDM)
For high-frequency load surveys (e.g. 15-minute intervals), use [`IntervalProfile`](./examples/IntervalProfile.json) with block incremental codes:
- Map the code to `reportedMode: "USAGE"` in the compact sequence.
- Ensure that the intervals are sequential by validating their `id`.
- The duration (e.g., `PT30M`) is declared in `intervalPeriod.duration`.

### Scenario B: Monthly Billing Determinant Handoff (MDM to Billing)
When mapping a billing handoff:
1. Include the cumulative energy usage reading with `reportedMode: "USAGE"` in [`MonthlyProfile`](./examples/MonthlyProfile.json) and populate the `openingValue` and `closingValue` properties so billing calculators can verify the calculation.
2. For Maximum Demand registers, use `reportedMode: "USAGE"`, specify the `integrationPeriod` (typically `PT30M`), and provide the peak timestamp in `occurredAt`.
3. Highlight multiple resets or ad-hoc demand clears occurring within the same month using [`MonthlyProfile_MultipleResets.json`](./examples/MonthlyProfile_MultipleResets.json).

### Scenario C: Meter Swaps & Replacements Mid-Cycle
When a physical meter is changed during a billing period:
1. Generate two [`MonthlyProfile`](./examples/MonthlyProfile.json) records within the dataset – one containing the final readings of the old meter serial number, and one containing the initial readings of the new meter serial.
2. Link them together under the consumer account reference in a single payload.
3. *See the [`Billing_MeterChange.json`](./examples/Billing_MeterChange.json) example for structural implementation.*

### Scenario D: Tamper and Diagnostic Logs
Tamper and diagnostic events (e.g. cover open, magnetic influence) are reported using the [`EventProfile`](./examples/EventProfile.json).
- Use the standard IS 15959 event codes in `eventId`.
- Do not transmit empty telemetry blocks in an Event profile; the `events` array should only contain diagnosed instances with precise timestamps.

## 4. Technical Service Provider (TSP) Integration & Value-Added Services

Integrating third-party Technical Service Providers (TSPs) or internal analytical engines enables utilities to offer advanced Value-Added Services (VAS) and optimize grid operations. The `MeterData` v0.6 schema supports these integrations through several distinct patterns:

### A. Near Real-Time Grid Performance & Planning
- **The Challenge**: Monitoring grid congestion, identifying transformer overloading, and managing load-generation balancing.
- **The Solution**: TSPs ingest near real-time active/reactive power intervals using `IntervalProfile` (Form B). By analyzing load survey trends, utilities can detect over-generation or excessive localized demand, triggering demand response events or planning infrastructure reinforcements.
- **Key Fields**: Use `IntervalProfile` with block energy or average power values, mapping parameters (e.g., `kW imp`, `kvarh Q1`) to index-based compact sequences.

### B. Rooftop Solar & Third-Party (3P) Integration
- **The Challenge**: Correlating utility meters with 3P rooftop solar generation systems to manage feed-in tariffs and grid stability.
- **The Solution**: Both utility meters and 3P solar inverters can publish telemetry using the same `MeterData` v0.6 architecture. Whether the data originates from a utility revenue meter or a third-party solar monitoring gateway, it uses a unified descriptor-based schema. This provides a unified framework for TSPs to calculate net consumer contribution per interval.
- **Key Fields**: Define two separate descriptors under the same `PayloadDescriptorSet` – one for `flowDirection: IMPORT` and another for `flowDirection: EXPORT`.
- **Unified Ingestion Flow**:
```mermaid
graph TD
    subgraph Data Sources
        UM[Utility Smart Meter] -->|Import/Export Telemetry| MD1[MeterData Payload]
        3P[3P Solar Inverter] -->|Generation Telemetry| MD2[MeterData Payload]
    end
    MD1 -->|Unified Schema v0.6| TSP[TSP Analytics / Netting Engine]
    MD2 -->|Unified Schema v0.6| TSP
```

### C. Theft & Incident Detection
- **The Challenge**: Detecting unauthorized meter bypasses, cover-open tampers, or phase failures to prevent revenue loss.
- **The Solution**: Combine diagnostic alerts in `EventProfile` (Form A) with electrical parameters in `InstantaneousProfile`. For example, a sudden drop in voltage on one phase (`V_R` in `InstantaneousProfile`) occurring concurrently with a `phase-failure` event in `EventProfile` indicates a service incident or potential tamper.
- **Key Fields**: `eventId` and `occurredAt` in `EventProfile` mapped to standard IS 15959 event groups.

### D. Analytics & Visualization Dashboards
- **The Challenge**: Powering customer portals or executive dashboards with consumption charts and generation profiles.
- **The Solution**: TSPs parse compact arrays from `IntervalProfile` or `DailyProfile` and project them into time-series databases to render load curves and energy usage charts.

### E. Multi-System Data Convergence
- **The Challenge**: Serving use cases that require data from different systems (e.g., connecting billing data from CIS with hourly telemetry from HES).
- **The Solution**: The `MeterData` envelope uses explicit metadata boundaries: `meterRefs` identifies the physical hardware, `serviceDeliveryPointRefs` identifies the grid connection node, and `customerRefs` (when permitted) links to the commercial account. TSPs can query the utility's DeDi registries to resolve these identifiers and correlate data across siloed utility databases.

---

## 5. Energy Credentials: Energy Passport & Energy Digest

Utilities can package verified metering data into cryptographically signed W3C Verifiable Credentials to facilitate secure, consumer-permissioned sharing with third parties:

### A. Energy Passport (Identity & Reference)
- **Purpose**: Verifies that a consumer has an active, valid connection with the utility without sharing granular consumption data.
- **Content**: Contains account metadata, service delivery point (SDP) details, and meter serial numbers.
- **Typical Use Case**: Used for customer onboarding, KYC, or address verification for banking and public services.

### B. Energy Digest (Consumption & Billing Summary)
- **Purpose**: Attests to historical consumption, solar generation, and billing figures over a specific billing cycle.
- **Content**: Combines a simplified bill summary (amounts, tariffs) with block-load granularity telemetry (e.g., daily totals or 15-minute intervals).
- **Typical Use Case**: Used by corporate consumers for ESG carbon accounting, or by financial institutions for green lending audits.

---

## 6. Data Lakes and On-Demand Sharing Architecture

{% hint style="info" %}
To prevent high-volume sharing requests from impacting operational databases (HES and MDM), utilities could consider a **data lake** architecture. The IES architecture fully supports offloading historical data to support on-demand queries.
{% endhint %}

```mermaid
graph LR
    HES[HES / MDM] -->|Batch Push| DL[(Data Lake)]
    DL -->|Query| Auth[Consent & Sign Service]
    Auth -->|Signed v0.6 VC| TSP[Third-Party TSP]
```

1. **Analytical Offloading**: Operational systems push telemetry data to a scalable data lake (e.g., PostgreSQL, BigQuery, or Parquet stores) in the compact `MeterData` v0.6 format.
2. **On-Demand Generation**: When a consumer grants consent to a TSP, the utility's consent service queries the data lake, packages the telemetry into the requested `MeterData` profile, signs it as a credential, and delivers it. This prevents analytical queries from degrading real-time metering operations.

---

## 7. Security, Privacy, and Safety Considerations

When exposing smart meter data, safeguarding consumer privacy and utility grid security is critical. Implement the following guidelines:

> [!IMPORTANT]
> **Data Minimization**
> Always restrict shared telemetry to the minimum granularity required. For example, if a third party only needs to verify monthly consumption, share a `MonthlyProfile` instead of an `IntervalProfile` containing hourly load surveys.

> [!WARNING]
> **PII Redaction & Naming Grammars**
> Never bundle personally identifiable information (PII) – such as customer names, phone numbers, or billing addresses – directly with high-frequency telemetry. Use public-key identifiers or standard DeDi naming grammars (e.g., `did:dedi:<discom>:consumers:CN-123`). Keep sensitive details in private registries that require explicit consumer authorization to resolve.

### Key Practices:
1. **Consent-Driven Routing**: Expose data exclusively via authenticated gateways (e.g., Beckn adapters or OpenCred portals) that validate a consumer's active cryptographic consent.
2. **Endpoint mTLS**: Secure internal API mirrors and data lake lookup routes using mutual TLS (mTLS) to prevent unauthorized internal leaks.
3. **Attribute Permissibility**: Restrict the attributes attached to readings (e.g., ensuring `openingValue` and `closingValue` are omitted from raw `READING` profiles to limit unnecessary data leakage).

---

## 8. Quality Indications & Validation

For all profile shapes, verifying data quality and formatting before ingestion is recommended.

### Encouraging the Validator
The India Energy Stack provides a validator tool located at `validation/validate_v06.py`. Developers and system administrators are encouraged to integrate this validator into their ingestion pipelines (e.g., as a CI step or pre-write database trigger) to assert both schema compliance and semantic constraints (e.g., validating usage calculation math and ensuring `openingValue`/`closingValue` are never attached to `READING` mode profiles).

Run the validator on your payload files:
```bash
python validation/validate_v06.py <path_to_payload.json>
```
