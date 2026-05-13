# Use Cases

IES Data Exchange targets three dataset types, each corresponding to a distinct regulatory or operational data flow in the Indian power sector.

***

## Overview

| # | Use Case                              | BAP (Consumer)      | BPP (Provider)      | Dataset                      | Status | Description                                                 |
| - | ------------------------------------- | ------------------- | ------------------- | ---------------------------- | ------ | ----------------------------------------------------------- |
| 1 | [Meter Telemetry](meter-telemetry/)   | DISCOM (BESCOM)     | AMISP (IntelliGrid) | `IES_Report`                 | Shipped in devkit | 15-minute AMI meter readings in OpenADR 3.1.0 format        |
| 2 | [ARR Filings](arr-filings.md)         | SERC (APERC)        | DISCOM (BESCOM)     | `IES_ARR_Filing`             | Shipped in devkit | Aggregate Revenue Requirement — fiscal year cost line items |
| 3 | [Tariff Policies](tariff-policies.md) | DISCOM (MeraShehar) | SERC (KERC)         | `IES_Policy` + `IES_Program` | **Planned** — not yet in devkit | Machine-readable tariff rate structures and energy slabs    |

UC1 and UC2 share the same Docker infrastructure, ONIX adapter configs, and Beckn message envelope. They differ in roles, schemas carried in `dataPayload`, and the resource identifiers in each message.

***

## What Makes Each Use Case Different

The Beckn message envelope is identical across use cases. What differs is:

1. **The roles** — who is the BAP and who is the BPP
2. **The dataset schema** — `IES_Report` vs `IES_ARR_Filing` vs `IES_Policy`+`IES_Program`
3. **The resource identifiers** — meter IDs, DISCOM names, SERC names in the `select` request
4. **The `dataPayload` structure** in `on_status`

***

## Common Transaction Lifecycle

The minimal exchange is `confirm` → `on_confirm` (payload inline). UC1 and UC2 both also exercise `status` → `on_status` for asynchronous payload delivery. The full set of optional actions (`publish-catalog`/`discover`/`select`/`init`/`update`) is described in [Architecture](../architecture.md#generic-beckn-flow).

***

## Running

```bash
cd DEG/devkits/data-exchange/install
docker compose up -d
```

Then import the use-case BAP Postman collection from `uc{1,2}-*/postman/` and fire `confirm`. See the [Quick Start](../quick-start.md) for the full walkthrough.
