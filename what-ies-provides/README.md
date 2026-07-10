# What IES Provides

Specifications for **Register**, **Discover**, **Exchange**, plus a master **Taxonomy**.

| Page | What's in it |
|---|---|
| **[What IES Is](../concepts/what-ies-is.md)** | The intro. Problem, UPI analogy, what IES is and is not, the four pilots, common questions. *Lives under [`concepts/`](../concepts/README.md) — supporting concept pages stay there for less link churn.* |
| **[Register](register.md)** | Verifiable digital identity (W3C DIDs) and the shared directory (DeDi). Detail under [Identifiers](identifiers/README.md), [Registries](registries/README.md). |
| **[Discover](discover.md)** | Beckn-protocol interaction. Detail under [Data Exchange](data-exchange/README.md). |
| **[Exchange](exchange.md)** | Schemas, taxonomy and verifiable credentials. Detail under [Energy Credentials](energy-credentials/README.md), [Schemas Overview](schemas-overview/README.md), [Schemas](../schemas/README.md). |
| **[Taxonomy](taxonomy.md)** | Master schema map, standards precedence, versioning, how to propose a new schema. |

---

## Why this organisation

The IES Technical Note defines three steps:

> *"IES tells any two systems in the power sector how to share data with each other. It works in three steps. (a) **Register** — verifiable digital identity. (b) **Discover** — interaction protocol. (c) **Exchange** — schema, taxonomy and verifiable credentials."*

**[How you implement IES](../how-you-implement-ies/README.md)** turns each into action; **[Use Case Implementation Guides](../use-cases/README.md)** ships them.

---

## Schemas

Schema files (JSON Schema, JSON-LD context, RDF vocabulary, examples) live at the repo root under **[`schemas/`](../schemas/README.md)**, keeping canonical URLs (`https://india-energy-stack.github.io/ies-accelerator/schemas/...`) stable — linked from [Exchange](exchange.md) and [Taxonomy](taxonomy.md).
