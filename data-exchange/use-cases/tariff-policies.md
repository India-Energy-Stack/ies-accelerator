# Use Case 3 — Tariff Policies

**A State Electricity Regulatory Commission (SERC) publishes machine-readable retail tariff policies to a distribution licensee (DISCOM).**

Shipped in the devkit at [`uc3-tariff-policy/`](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc3-tariff-policy).

---

## Scenario

After a tariff order is issued, DISCOMs must implement the new rate structures in their billing systems. Today this means manually interpreting a PDF tariff order and re-keying energy slabs, time-of-day surcharges, and category definitions — a process prone to interpretation drift and errors.

With IES Data Exchange, the SERC publishes a machine-readable `IES_Policy` artefact alongside the regulatory order. DISCOMs consume it directly into their billing systems — no re-keying, no ambiguity. The transfer is free under public-disclosure norms (settlement value `0` in the example payloads).

---

## Roles

| Role | Organisation | What they do |
|---|---|---|
| BAP (consumer) | MeraShehar DISCOM | Subscribes to the tariff policy feed |
| BPP (provider) | MERC — Maharashtra Electricity Regulatory Commission | Publishes the machine-readable `IES_Policy` |

---

## Dataset — `IES_Policy`

A single `IES_Policy` object captures the tariff. The schema (canonical: [`beckn/DEG ies-specs core/attributes.yaml`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/attributes.yaml)) carries:

- **Identity** — `id`, `policyID` (e.g. `MUM-RES-T1`), `policyName`, `policyType` (`TARIFF` or `DISPATCH_GUIDE`), `programID` linking it to an [`IES_Program`](https://github.com/beckn/DEG/blob/ies-specs/specification/external/schema/ies/core/attributes.yaml).
- **Validity** — `samplingInterval` as an ISO 8601 recurrence pattern (`R/2024-04-10T00:00:00Z/P1M`).
- **`energySlabs[]`** — progressive consumption tiers, each `{ id, start (kWh, inclusive), end (kWh, exclusive or null for open-ended), price }`.
- **`surchargeTariffs[]`** — time-of-day adjustments, each `{ id, recurrence (ISO duration, e.g. `P1D`), interval (Time-of-Day start + ISO duration), value, unit (`PERCENT` or `INR_PER_KWH`) }`.

### Example — Mumbai Residential Telescopic Tariff

```json
{
  "@context": "https://raw.githubusercontent.com/beckn/DEG/ies-specs/specification/external/schema/ies/core/context.jsonld",
  "@type": "IES_Policy",
  "id": "policy-mumbai-res-001",
  "objectType": "POLICY",
  "policyID": "MUM-RES-T1",
  "policyName": "Mumbai Residential Telescopic 2024",
  "policyType": "TARIFF",
  "programID": "program-merashehar-001",
  "samplingInterval": "R/2024-04-10T00:00:00Z/P1M",
  "energySlabs": [
    { "id": "slab-0-100",     "@type": "EnergySlab", "start": 0,   "end": 100,  "price": 4.5 },
    { "id": "slab-101-300",   "@type": "EnergySlab", "start": 101, "end": 300,  "price": 7.2 },
    { "id": "slab-301-plus",  "@type": "EnergySlab", "start": 301, "end": null, "price": 9.8 }
  ],
  "surchargeTariffs": [
    {
      "id": "surcharge-evening-peak",
      "@type": "SurchargeTariff",
      "recurrence": "P1D",
      "interval": { "start": "T18:00:00Z", "duration": "PT4H" },
      "value": 20,
      "unit": "PERCENT"
    },
    {
      "id": "discount-night-offpeak",
      "@type": "SurchargeTariff",
      "recurrence": "P1D",
      "interval": { "start": "T23:00:00Z", "duration": "PT6H" },
      "value": -10,
      "unit": "PERCENT"
    }
  ]
}
```

Source: [India-Energy-Stack/ies-docs `tariff_specification_example.jsonld`](https://github.com/India-Energy-Stack/ies-docs/blob/main/implementation-guides/data_exchange/examples/tariff_specification_example.jsonld). The `@type: "IES_Policy"` matters — ONIX's Extended Schema validator dispatches by `@type` against the schema name in `attributes.yaml`.

---

## Transaction Flow

UC3 exercises **`confirm` → `on_confirm` → `status` → `on_status`**. The tariff is delivered inside `message.contract.commitments[].resources[].resourceAttributes` at contract time and inside `message.contract.performance[].performanceAttributes.dataPayload` on the final `on_status` callback:

```json
"performance": [{
  "id": "perf-tariff-policy-delivery-001",
  "status": { "code": "DELIVERY_COMPLETE" },
  "commitmentIds": ["commitment-tariff-policy-001"],
  "performanceAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/DDM/main/specification/schema/DatasetItem/v1/context.jsonld",
    "@type": "DatasetItem",
    "dataset:accessMethod": "INLINE",
    "dataPayload": { /* IES_Policy — see above */ }
  }
}]
```

Full request/response examples (publish-catalog, discover, confirm, on-confirm, status, on-status × 3) live in [uc3-tariff-policy/examples/](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc3-tariff-policy/examples).

---

## Why Machine-Readable Tariffs Matter

| Current State | With IES Tariff Policies |
|---|---|
| Tariff orders published as PDFs | Machine-readable JSON-LD alongside the PDF order |
| Each DISCOM interprets slabs independently | Single authoritative structured definition |
| Billing system updates take days/weeks | Billing systems ingest the policy directly via Beckn |
| TOU surcharges manually configured | Surcharge rules machine-parseable by smart meters / home energy managers |
| Comparison across SERCs is manual | Structured format enables automated cross-state analysis |

---

## Consuming the Policy in a Billing System

```python
from datetime import time

def apply_tariff(consumption_kwh: float, hour_of_day: int, policy: dict) -> float:
    """
    Compute the bill for `consumption_kwh` units consumed at `hour_of_day`,
    given an IES_Policy dict. Real billing iterates over actual usage
    intervals; this is the rate-lookup core.
    """
    # 1. Find the applicable energy slab. `end` is exclusive; `null` = open-ended.
    base_rate = 0.0
    for slab in policy["energySlabs"]:
        end = slab.get("end")
        if slab["start"] <= consumption_kwh and (end is None or consumption_kwh < end):
            base_rate = slab["price"]
            break

    # 2. Apply the first matching time-of-day surcharge.
    surcharge_value = 0.0
    surcharge_unit  = "PERCENT"
    for tod in policy.get("surchargeTariffs", []):
        start_h = int(tod["interval"]["start"][1:3])     # "T18:00:00Z" -> 18
        # ISO 8601 duration parsing kept minimal here; production code should use
        # `isodate.parse_duration`.
        dur_h = int(tod["interval"]["duration"].split("PT")[1].rstrip("H")) \
                if tod["interval"]["duration"].endswith("H") else 0
        end_h = (start_h + dur_h) % 24
        in_window = (start_h <= hour_of_day < end_h) if start_h < end_h \
                    else (hour_of_day >= start_h or hour_of_day < end_h)
        if in_window:
            surcharge_value = tod["value"]
            surcharge_unit  = tod.get("unit", "PERCENT")
            break

    if surcharge_unit == "PERCENT":
        effective_rate = base_rate * (1 + surcharge_value / 100)
    else:  # INR_PER_KWH (absolute adder)
        effective_rate = base_rate + surcharge_value

    return consumption_kwh * effective_rate
```

---

## Running This Use Case

```bash
cd DEG/devkits/data-exchange/install
docker compose up -d
```

Then import the BAP collection at `uc3-tariff-policy/postman/data-exchange-uc3-tariff-policy.BAP-DEG.postman_collection.json` into Postman, set `bap_host_root` and `bpp_host_root` to `http://beckn-router:9000`, and fire `confirm`. Inspect callbacks:

```bash
docker logs sandbox-bap 2>&1 | grep -E 'on_(confirm|status)' | tail -10
```

To run the workflows in one shot via the Arazzo runner:

```bash
cd DEG/devkits/data-exchange/uc3-tariff-policy/workflows
./run-arazzo.sh                                     # publish-catalog + discover
./run-arazzo.sh -w confirm-through-delivery -v      # end-to-end confirm→on_status
```

See the [Quick Start](../quick-start.md) for the full step-by-step.

---

## Reference

- [IES Core Schemas — `IES_Policy`, `IES_Program`, `EnergySlab`, `SurchargeTariff`](https://github.com/beckn/DEG/tree/ies-specs/specification/external/schema/ies/core) *(currently on the `ies-specs` branch; will move to India-Energy-Stack — see [Concepts § IES Data Schemas](../concepts.md#ies-data-schemas))*
- [IES tariff specification example (ies-docs)](https://github.com/India-Energy-Stack/ies-docs/blob/main/implementation-guides/data_exchange/examples/tariff_specification_example.jsonld) — source for the example payload above
- [Example payloads in the devkit](https://github.com/beckn/DEG/tree/main/devkits/data-exchange/uc3-tariff-policy/examples)
