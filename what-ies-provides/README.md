# What IES Provides

The specifications — a broad view of the technology stack, organised by the three IES steps (**Register**, then **Discover** and **Exchange** presented together), plus the **Taxonomy** that ties every schema together. Hands-on, step-by-step guides live separately in **[How you implement IES](../how-you-implement-ies/README.md)**.

| Page | What's in it |
|---|---|
| **[What IES Is](../concepts/what-ies-is.md)** | The intro, on one page. Problem, UPI analogy, how it works, what IES is not, sector impact, pilots, common questions. |
| **[Register](register.md)** | Verifiable digital identity (W3C DIDs) and the shared directory (DeDi) — the two identities a participant sets up, identifier patterns, and the registries IES uses. |
| **[Discover+Exchange](discover-exchange.md)** | How data moves once participants are registered: Beckn-protocol interaction for B2B data exchange, and where B2C verifiable credentials fit. |
| **[Schemas Overview](schemas-overview/README.md)** | One plain-language page per schema family — what it is, who issues it, which standards it follows — the *why* before the field-level reference. |
| **[Taxonomy](taxonomy.md)** | The master vocabulary: the schema map (which schema for which use case), standards precedence, versioning, and how to propose a new object. The field-by-field reference is the [Taxonomy chapter](../schemas/README.md) near the end of the book. |

---

## Why this organisation

The IES Technical Note defines three steps that every interaction follows:

> *"IES tells any two systems in the power sector how to share data with each other. It works in three steps. (a) **Register** — verifiable digital identity. (b) **Discover** — interaction protocol. (c) **Exchange** — schema, taxonomy and verifiable credentials."*

This section publishes those specifications — deliberately broad and shallow, so a regulator or a CTO can understand the whole stack in one sitting. **[How you implement IES](../how-you-implement-ies/README.md)** turns each specification into end-to-end, copy-pasteable action: Setup Register, Issue Credentials, Setup Discovery+Exchange, Build your Internal-facing Adapter. **[Use Case Implementation Guides](../use-cases/README.md)** combine them into shippable outcomes.

## Two capabilities on one foundation

**Register** is the shared foundation: every participant, whatever it does, gets a verifiable identity and a directory entry. On top of it sit two capabilities with **two different trust models**, and a participant adopts whichever its use cases need:

- **Data exchange (B2B)** — structured payloads (meter telemetry, regulatory filings, tariff data, trades) moving between **registered organisations**. Trust here is *bilateral*: each side looks the other up in the DeDi directory, verifies its signature, and checks that both belong to the same curated network — so the exchange must ride a trust-bounded open network, and IES uses **Beckn** for it. See [Discover+Exchange](discover-exchange.md).
- **Energy credentials (B2C)** — signed W3C Verifiable Credentials (a consumer's connection record, a meter digest). Trust here is *unilateral*: the issuer signs once against its published **`did:web`**, and any third party the issuer has never met — a bank, a marketplace — can verify it independently. Because the trust travels inside the credential, delivery can use **any channel**: DigiLocker, a web portal, email, SMS, chat. No Beckn network involved. See [Energy Credentials](../how-you-implement-ies/energy-credentials/README.md).

The same [Taxonomy](../schemas/README.md) backs both: the Taxonomy is the vocabulary of IES domain objects, and the shape of each object is described by its **schema** — a self-contained, machine-readable definition that is valid whether or not the payload ever travels over Beckn.

---

## Where the schema files live

The Taxonomy's schema files (JSON Schema, JSON-LD context, RDF vocabulary, example payloads) live at the repository root in **[`schemas/`](../schemas/README.md)** so that their canonical published URLs (`https://india-energy-stack.github.io/ies-accelerator/schemas/...`) stay stable for external consumers.
