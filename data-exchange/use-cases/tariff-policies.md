# Use Case 3 — Tariff Policies

> **Status: planned.** The schema and scenario below describe the target shape. There is no implementation in the devkit yet — no `uc3-*` directory, no example payloads, no Postman collection. The page is retained for design alignment; expect changes when the devkit ships UC3.

**A State Electricity Regulatory Commission (SERC) publishes machine-readable tariff rate structures to DISCOMs.**

---

## Scenario

After a tariff order is issued, DISCOMs must implement the new rate structures in their billing systems. Today this means manually interpreting a PDF tariff order and re-keying energy slabs, time-of-day surcharges, and category definitions — a process prone to interpretation drift and errors.

With IES Data Exchange, the SERC publishes a machine-readable `IES_Policy` + `IES_Program` dataset alongside the tariff order. DISCOMs consume it directly into their billing systems — no re-keying, no ambiguity.

---

## Roles

| Role | Organisation | What they do |
|---|---|---|
| BAP (consumer) | MeraShehar DISCOM | Requests the tariff rate structure |
| BPP (provider) | KERC / SERC | Publishes machine-readable tariff policies and programs |

---

## Dataset — IES_Policy + IES_Program

Two schemas combine to represent a complete tariff structure:

- **`IES_Program`** — defines the tariff programs (consumer categories: residential, commercial, agricultural, industrial)
- **`IES_Policy`** — defines the rate rules for each program (energy slabs, fixed charges, time-of-day surcharges)

The combined payload is called `IES_TariffIntelligence` in the mock BPP.

### Structure

```json
{
  "programs": [
    {
      "id": "residential-2026-27",
      "name": "Residential LT-2 Tariff 2026-27",
      "regulatoryOrder": "KERC/T/2026/001",
      "effectiveFrom": "2026-04-01",
      "effectiveTo": "2027-03-31",
      "consumerCategory": "residential",
      "currency": "INR"
    },
    {
      "id": "commercial-2026-27",
      "name": "Commercial LT-5 Tariff 2026-27",
      "regulatoryOrder": "KERC/T/2026/001",
      "effectiveFrom": "2026-04-01",
      "consumerCategory": "commercial",
      "currency": "INR"
    }
  ],
  "policies": [
    {
      "id": "residential-2026-27-policy",
      "programId": "residential-2026-27",
      "fixedChargePerMonth": 35.00,
      "energySlabs": [
        {
          "slabNumber": 1,
          "fromKWh": 0,
          "toKWh": 100,
          "ratePerKWh": 3.50,
          "description": "First 100 units"
        },
        {
          "slabNumber": 2,
          "fromKWh": 101,
          "toKWh": 200,
          "ratePerKWh": 5.75,
          "description": "101–200 units"
        },
        {
          "slabNumber": 3,
          "fromKWh": 201,
          "toKWh": null,
          "ratePerKWh": 7.20,
          "description": "Above 200 units"
        }
      ],
      "surchargeTariffs": [
        {
          "type": "time_of_day",
          "period": "peak",
          "timeRange": "18:00–22:00",
          "surchargePercent": 20,
          "applicableDays": ["weekdays"]
        },
        {
          "type": "time_of_day",
          "period": "off_peak",
          "timeRange": "22:00–06:00",
          "surchargePercent": -10,
          "applicableDays": ["all"]
        }
      ]
    }
  ]
}
```

| Field | Description |
|---|---|
| `programs[]` | One per consumer category. References the regulatory order. |
| `policies[].energySlabs[]` | Progressive rate bands — `toKWh: null` means open-ended (above last threshold) |
| `policies[].surchargeTariffs[]` | Time-of-day pricing adjustments — percent on top of base slab rate |
| `fixedChargePerMonth` | Monthly fixed/demand charge regardless of consumption |

---

## Transaction Flow

### 1. Select

The DISCOM (BAP) requests the tariff policy for its state:

```json
{
  "context": {
    "action": "select",
    "domain": "deg:data-exchange",
    "bap_id": "merashehar.discom.ies.in",
    "bpp_id": "kerc.regulator.karnataka.ies.in",
    "transaction_id": "txn-tariff-2026-27-001"
  },
  "message": {
    "order": {
      "items": [
        {
          "id": "kerc-tariff-order-2026-27",
          "descriptor": { "code": "IES_Policy" }
        }
      ],
      "fulfillments": [
        {
          "tags": [
            { "code": "fiscal_year", "value": "2026-27" },
            { "code": "regulatory_order", "value": "KERC/T/2026/001" }
          ]
        }
      ]
    }
  }
}
```

### 4. Status — Inline Delivery

```json
{
  "message": {
    "order": {
      "status": "DELIVERY_COMPLETE",
      "items": [
        {
          "id": "kerc-tariff-order-2026-27",
          "accessMethod": "INLINE",
          "dataPayload": {
            "programs": [ /* ... */ ],
            "policies": [ /* ... */ ]
          }
        }
      ]
    }
  }
}
```

---

## Why Machine-Readable Tariffs Matter

| Current State | With IES Tariff Policies |
|---|---|
| Tariff orders published as PDFs | Machine-readable JSON alongside PDF |
| Each DISCOM interprets slabs independently | Single authoritative structured definition |
| Billing system updates take days/weeks | Billing systems can ingest the policy directly |
| TOU surcharges manually configured | Surcharge rules machine-parseable by smart meters / home energy managers |
| Comparison across SERCs is manual | Structured format enables automated cross-state analysis |

---

## Consuming the Policy in a Billing System

```python
import requests

# After on_status arrives at your webhook
def apply_tariff(consumption_kwh: float, hour_of_day: int, policy: dict) -> float:
    # Find applicable energy slab
    base_rate = 0
    for slab in policy["energySlabs"]:
        if slab["fromKWh"] <= consumption_kwh:
            if slab["toKWh"] is None or consumption_kwh <= slab["toKWh"]:
                base_rate = slab["ratePerKWh"]
                break

    # Apply time-of-day surcharge
    surcharge_pct = 0
    for tod in policy["surchargeTariffs"]:
        start, end = tod["timeRange"].split("–")
        start_h = int(start.split(":")[0])
        end_h = int(end.split(":")[0])
        if start_h <= hour_of_day < end_h:
            surcharge_pct = tod["surchargePercent"]
            break

    effective_rate = base_rate * (1 + surcharge_pct / 100)
    return consumption_kwh * effective_rate
```

---

## Running This Use Case

Not yet runnable — the devkit does not ship a tariff-policies use case. Track [beckn/DEG](https://github.com/beckn/DEG) for when `uc3-tariff-policies/` (or equivalent) lands.

---

## Reference

- [IES Core Schemas — `IES_Policy` + `IES_Program`](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core) *(currently on the `ies-specs` branch; will move to India-Energy-Stack — see [Concepts § IES Data Schemas](../concepts.md#ies-data-schemas))*
