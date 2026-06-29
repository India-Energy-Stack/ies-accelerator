# What IES Provides

The specifications. What is published. Organised by the three IES steps — **Register**, **Discover**, **Exchange** — plus a master **Taxonomy** that ties everything together.

| Page | What's in it |
|---|---|
| **[What IES Is](../concepts/what-ies-is.md)** | The intro. Problem, UPI analogy, what IES is and is not, the four pilots, common questions. *Lives under [`../concepts/`](../concepts/) — supporting concept pages stay there for less link churn.* |
| **[Register](register.md)** | Verifiable digital identity (W3C DIDs) and the shared directory (DeDi). Detail under [Identifiers](identifiers/README.md), [Registries](registries/README.md). |
| **[Discover](discover.md)** | Beckn-protocol interaction. Detail under [Data Exchange](data-exchange/README.md). |
| **[Exchange](exchange.md)** | Schemas, taxonomy and verifiable credentials. Detail under [Energy Credentials](energy-credentials/README.md), [Schemas](../schemas/README.md). |
| **[Taxonomy](taxonomy.md)** | Master schema map, standards precedence, versioning, how to propose a new schema. |

---

## Why this organisation

The IES Technical Note defines three steps that every interaction follows:

> *"IES tells any two systems in the power sector how to share data with each other. It works in three steps. (a) **Register** — verifiable digital identity. (b) **Discover** — interaction protocol. (c) **Exchange** — schema, taxonomy and verifiable credentials."*

This Part 1 publishes those specifications. **[Part 2 — How you implement IES](../how-you-implement-ies/README.md)** turns each specification into an action: Setup Register, Setup Discovery, Build your Internal-facing Adapter. **[Part 3 — Use Case Implementation Guides](../use-cases/README.md)** combines them into shippable outcomes.

---

## Schemas

The schema files (JSON Schema, JSON-LD context, RDF vocabulary, example payloads) live at the repository root in **[`../schemas/`](../schemas/)** so that their canonical published URLs (`https://india-energy-stack.github.io/ies-accelerator/schemas/...`) stay stable for external consumers. The [Exchange](exchange.md) page and the [Taxonomy](taxonomy.md) page both link down into them.
