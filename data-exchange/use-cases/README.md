# Use Cases

IES Data Exchange currently supports three dataset types, each corresponding to a distinct regulatory or operational data flow in the Indian power sector.

---

## Overview

| # | Use Case | BAP (Consumer) | BPP (Provider) | Dataset | Description |
|---|---|---|---|---|---|
| 1 | [Meter Telemetry](./meter-telemetry.md) | DISCOM (BESCOM) | AMISP (IntelliGrid) | `IES_Report` | 15-minute AMI meter readings in OpenADR 3.1.0 format |
| 2 | [ARR Filings](./arr-filings.md) | SERC (APERC) | DISCOM (BESCOM) | `IES_ARR_Filing` | Aggregate Revenue Requirement — fiscal year cost line items |
| 3 | [Tariff Policies](./tariff-policies.md) | DISCOM (MeraShehar) | SERC (KERC) | `IES_Policy` + `IES_Program` | Machine-readable tariff rate structures and energy slabs |

All three use cases share the same Docker infrastructure, ONIX adapter configs, and Beckn transaction lifecycle (select → init → confirm → status).

---

## What Makes Each Use Case Different

The Beckn message envelope is identical across use cases. What differs is:

1. **The roles** — who is the BAP and who is the BPP
2. **The dataset schema** — `IES_Report` vs `IES_ARR_Filing` vs `IES_Policy`+`IES_Program`
3. **The resource identifiers** — meter IDs, DISCOM names, SERC names in the `select` request
4. **The `dataPayload` structure** in `on_status`

---

## Common Transaction Lifecycle

```
BAP sends select   → on_select returns available dataset catalog
BAP sends init     → on_init confirms readiness
BAP sends confirm  → on_confirm activates the contract
BAP sends status   → on_status delivers the data inline in dataPayload
```

Each step is a separate HTTP POST to the ONIX BAP adapter. ONIX signs, routes, and delivers the messages. Responses arrive asynchronously at your BAP webhook.

---

## Running All Use Cases

```bash
# Start the bootcamp stack
cd DEG/devkits/data-exchange/install
docker compose -f docker-compose-bootcamp.yml up -d --build

# Run all three
cd ..
./scripts/test-workflow.sh all
```

See the [Quick Start](../quick-start.md) for step-by-step instructions.
