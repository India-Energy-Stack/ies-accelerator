# External Schemas (DEG)

Field references for schemas that are **authored in the [DEG repo](https://github.com/India-Energy-Stack/DEG)**, not in this repository. They are surfaced here so the GitBook and the printed PDF carry a complete field reference for the deployable DEG devkits without leaving the accelerator book.

## Provenance

These pages are **generated**, not hand-written. `scripts/generate_external_field_tables.py` reads each schema's `attributes.yaml` from the DEG repo (version `v2.0`) and renders the same Field / Type / Description tables used elsewhere in this book. DEG is the source of truth; if a table looks stale, re-run the generator against the current DEG checkout (`--deg-repo /path/to/DEG`). Where a field derives from a recognised standard, its description begins with **Based on** and the standard reference (from the source's `x-standard` annotation).

## Pages

| Domain | DEG devkit | Schemas |
|--------|-----------|---------|
| [Energy Trading (P2P, wave2)](energy-trading.md) | `devkits/p2p-trading-ies-wave2` | `P2PTrade`, `EnergyTradeOffer`, `EnergyCustomer`, `EnergyOrderItem`, `RevenueFlow`, `DEGContract`, `EnergyResource` |
| [Demand Flexibility](demand-flex.md) | `devkits/demand-flex` | `DemandFlexNeed`, `DemandFlexBuyOffer`, `DemandFlexPerformance` |

