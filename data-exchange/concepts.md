# Core Concepts — Data Exchange

This page explains the conceptual foundations of IES Data Exchange before you start integrating.

---

## The Digital Energy Grid (DEG) Primitives

IES Data Exchange is built on the **Digital Energy Grid (DEG)** architecture, which defines six primitives for energy transactions. Understanding these helps you model your data correctly.

### 1. Energy Resource

Any physical or logical entity that produces, consumes, stores, or manages energy. This includes:
- Generators (solar plants, wind farms)
- Storage systems (batteries)
- Consumption devices (EVs, appliances)
- Infrastructure (smart meters, transformers)
- Service providers (DISCOMs, AMISPs, SERCs)

In a data exchange, the **data provider (BPP)** and **data consumer (BAP)** are both Energy Resources.

### 2. Energy Resource Address (ERA)

A globally unique digital identifier for any Energy Resource — analogous to a domain name or IP address. ERAs enable discovery and addressing across federated networks.

```
meter-KA-98765432.amisp.bescom.in        ← smart meter
bescom.discom.karnataka.ies.in           ← DISCOM
aperc.regulator.andhra.ies.in           ← state regulator
```

### 3. Energy Credentials

Verifiable attestations about Energy Resources. In data exchange, credentials may gate access — a BPP can require the BAP to present a valid credential (e.g. a regulatory mandate credential) before delivering a dataset.

### 4. Energy Intent

A digital expression of what data a consumer needs — what dataset, from what source, for what time range, under what access terms.

### 5. Energy Catalogue

A structured listing of available datasets published by a BPP — including dataset type, time coverage, delivery mode, and pricing/terms.

### 6. Energy Contract

The formalized agreement that results from a BAP's intent matching a BPP's catalogue — the confirmed data exchange order.

---

## Beckn Protocol Lifecycle

IES Data Exchange uses the **Beckn Protocol v2.0** interaction model. Every data exchange follows a four-step lifecycle:

| Step | BAP calls | BPP responds | Purpose |
|---|---|---|---|
| 1 | `select` | `on_select` | Browse available datasets and terms |
| 2 | `init` | `on_init` | Activate the contract |
| 3 | `confirm` | `on_confirm` | Lock the contract |
| 4 | `status` | `on_status` | Get the data |

Beckn is **asynchronous**: every call returns an immediate `ACK`, and the actual response arrives as a callback (`on_*`) to the BAP's webhook URL. The ONIX adapter manages this asynchrony transparently.

### Message Structure

Every Beckn message shares the same envelope:

```json
{
  "context": {
    "domain": "deg:data-exchange",
    "version": "2.0.0",
    "action": "select",
    "bap_id": "bap.example.com",
    "bap_uri": "http://onix-bap:8081/bap/receiver",
    "bpp_id": "bpp.example.com",
    "bpp_uri": "http://onix-bpp:8082/bpp/receiver",
    "transaction_id": "txn-550e8400-e29b-41d4-a716",
    "message_id": "msg-f47ac10b-58cc-4372",
    "timestamp": "2026-04-01T10:00:00.000Z",
    "ttl": "PT30S"
  },
  "message": {
    /* action-specific payload */
  }
}
```

---

## The DatasetItem Schema

IES uses the **DDM DatasetItem schema** from [beckn/DDM](https://github.com/beckn/DDM) to describe exchangeable datasets. The key fields:

```json
{
  "id": "amisp-meter-data-ka-2026-q1",
  "descriptor": {
    "name": "AMI Meter Telemetry Q1 2026",
    "code": "IES_Report"
  },
  "dataPayload": {
    /* inline IES data — IES_Report, IES_ARR_Filing, etc. */
  },
  "accessMethod": "INLINE"
}
```

The `accessMethod` field declares how data is delivered:

| Mode | Description |
|---|---|
| `INLINE` | Data embedded directly in the `on_status` Beckn message |
| `DOWNLOAD` | BPP provides a signed download URL |
| `DATA_ENCLAVE` | Data accessible only within a secure compute environment |
| `OFF_CHANNEL` | Delivery through an agreed out-of-band channel |

IES Data Exchange primarily uses `INLINE` delivery — data arrives as part of the protocol message, making the exchange end-to-end verifiable.

---

## IES Data Schemas

### IES_Report (Meter Telemetry)

Based on **OpenADR 3.1.0**, carries 15-minute interval smart meter readings:

```json
{
  "payloadDescriptors": [
    { "payloadType": "USAGE", "units": "KWH", "accuracy": 0.01 }
  ],
  "resources": [
    {
      "resourceName": "meter-KA-98765432",
      "intervals": [
        {
          "id": 0,
          "intervalPeriod": {
            "start": "2026-04-01T00:00:00+05:30",
            "duration": "PT15M"
          },
          "payloads": [{ "type": "USAGE", "values": [1.23] }]
        }
      ]
    }
  ]
}
```

### IES_ARR_Filing (Regulatory Filing)

Carries Aggregate Revenue Requirement data with fiscal year line items:

```json
{
  "licensee": "BESCOM",
  "state": "Karnataka",
  "regulatoryCommission": "KERC",
  "fiscalYears": [
    {
      "year": "2025-26",
      "lineItems": [
        { "category": "Power Purchase Cost", "amountCrINR": 12450.5 },
        { "category": "Transmission Charges", "amountCrINR": 1823.2 },
        { "category": "O&M Expenses", "amountCrINR": 892.7 }
      ]
    }
  ]
}
```

### IES_Policy + IES_Program (Tariff Data)

Carries machine-readable tariff rate structures:

```json
{
  "programs": [
    { "id": "residential-2026", "name": "Residential Tariff 2026-27" }
  ],
  "policies": [
    {
      "programId": "residential-2026",
      "energySlabs": [
        { "upToKWh": 100, "ratePerKWh": 3.50 },
        { "upToKWh": 200, "ratePerKWh": 5.75 },
        { "upToKWh": null, "ratePerKWh": 7.20 }
      ],
      "surchargeTariffs": [
        { "period": "peak", "surchargePercent": 20 },
        { "period": "off-peak", "surchargePercent": -10 }
      ]
    }
  ]
}
```

---

## ONIX Adapter

**ONIX** is the Beckn protocol adapter used by IES. It handles:
- Request signing (Ed25519)
- Routing between BAP and BPP
- Schema validation (checks that `dataPayload` conforms to the declared IES schema)
- Async callback delivery

ONIX runs as a Docker container. You interact with it through its REST API:
- BAP calls go to `http://localhost:8081/bap/caller`
- BPP receives calls from `http://localhost:8082/bpp/caller`
- Callbacks arrive at your registered webhook URL

You do not need to implement Beckn signing or routing yourself — ONIX handles it.

---

## Network

All IES Data Exchange participants connect through the IES testnet:

| Parameter | Value |
|---|---|
| Network ID | `nfh.global/testnet-deg` |
| Domain | `deg:data-exchange` |

For production deployments, contact the IES team for mainnet network credentials.
