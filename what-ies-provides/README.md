# What IES Provides

The specifications. What is published. Organised by the three IES steps — **Register**, **Discover**, **Exchange** — plus the **Taxonomy** that ties every schema together.

| Page | What's in it |
|---|---|
| **[What IES Is](../concepts/what-ies-is.md)** | The intro, on one page. Problem, UPI analogy, how it works, what IES is not, sector impact, pilots, common questions. |
| **[Register](register.md)** | Verifiable digital identity (W3C DIDs) and the shared directory (DeDi). Detail under [Identifiers](identifiers/README.md), [Registries](registries/README.md). |
| **[Discover](discover.md)** | Beckn-protocol interaction for data exchange. Detail under [Data Exchange](data-exchange/README.md). |
| **[Exchange](exchange.md)** | The Taxonomy and verifiable credentials. Detail under [Energy Credentials](energy-credentials/README.md) and the [Taxonomy](../schemas/README.md). |
| **[Taxonomy](../schemas/README.md)** | The master vocabulary of IES — every domain object, its plain-language overview, and the schema that describes its shape. Standards precedence, versioning, how to propose a new object. *Its own chapter near the end of this book.* |

---

## Why this organisation

The IES Technical Note defines three steps that every interaction follows:

> *"IES tells any two systems in the power sector how to share data with each other. It works in three steps. (a) **Register** — verifiable digital identity. (b) **Discover** — interaction protocol. (c) **Exchange** — schema, taxonomy and verifiable credentials."*

This section publishes those specifications. **[How you implement IES](../how-you-implement-ies/README.md)** turns each specification into an action: Setup Register, Setup Discovery, Build your Internal-facing Adapter. **[Use Case Implementation Guides](../use-cases/README.md)** combines them into shippable outcomes.

## Two capabilities on one foundation

**Register** is the shared foundation: every participant, whatever it does, gets a verifiable identity and a directory entry. On top of it, IES publishes two capabilities that a participant adopts as its use cases need them:

- **Data exchange** — [Discover](discover.md) and the exchange of structured payloads (meter telemetry, regulatory filings, tariff data) between organisations. This is the Beckn use of IES: discovery, terms, consent, signed contract and audit trail. IES recommends Beckn for **B2B** data exchange.
- **Energy credentials** — signed W3C Verifiable Credentials (a consumer's connection record, a meter digest) issued with [OpenCred](../glossary.md#opencred) and verified against the issuer's published key. Credentials stand on their own: they **may or may not involve a Beckn network**. Consumer-facing (**B2C**) delivery happens over [DigiLocker](../glossary.md#digilocker), a web portal, or any channel the issuer already runs.

The same [Taxonomy](../schemas/README.md) backs both: the Taxonomy is the vocabulary of IES domain objects, and the shape of each object is described by its **schema** — a self-contained, machine-readable definition that is valid whether or not the payload ever travels over Beckn.

---

## Where the schema files live

The Taxonomy's schema files (JSON Schema, JSON-LD context, RDF vocabulary, example payloads) live at the repository root in **[`schemas/`](../schemas/README.md)** so that their canonical published URLs (`https://india-energy-stack.github.io/ies-accelerator/schemas/...`) stay stable for external consumers.
