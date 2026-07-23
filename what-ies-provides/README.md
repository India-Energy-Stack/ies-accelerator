# What IES Provides

The specifications — a broad view of the technology stack, organised by the three IES steps (**Register**, then **Discover** and **Exchange** presented together, with **Verifiable Credentials** alongside as the B2C half of Exchange), plus the **[Schemas](../schemas/README.md)** reference that underpins every object. Hands-on, step-by-step guides live separately in **[How you implement IES](../how-you-implement-ies/README.md)**. New to IES? Start at **[Home](../README.md)** for the plain-language intro, then read the pages below in order.

| Page | What's in it |
|---|---|
| **[Register](register.md)** | Verifiable digital identity (W3C DIDs) and the shared directory (DeDi) — the two identities a participant sets up, identifier patterns, and the registries IES uses. |
| **[Discover](discover.md)** | Beckn-protocol interaction — how two registered organisations find each other, agree terms and sign, without a bilateral arrangement. |
| **[Exchange](exchange.md)** | How data moves once discovered: the schemas, and where B2C verifiable credentials fit. |
| **[Verifiable Credentials](energy-credentials/README.md)** | The B2C rail — credential lifecycle, the variants IES uses, the trust model, and DigiLocker delivery. No Beckn network involved. |
| **[Schemas Overview](schemas-overview/README.md)** | One plain-language page per schema family — what it is, who issues it, which standards it follows — the *why* before the field-level reference. |

---

## Why this organisation

The IES Technical Note defines three steps that every interaction follows:

> *"IES tells any two systems in the power sector how to share data with each other. It works in three steps. (a) **Register** — verifiable digital identity. (b) **Discover** — interaction protocol. (c) **Exchange** — schema, taxonomy and verifiable credentials."*

This section publishes those specifications — deliberately broad and shallow, so a regulator or a CTO can understand the whole stack in one sitting. **[How you implement IES](../how-you-implement-ies/README.md)** turns each specification into end-to-end, copy-pasteable action: Setup Register, Issue Credentials, Setup Exchange, Build your Internal-facing Adapter. **[Use Case Implementation Guides](../use-cases/README.md)** combine them into shippable outcomes.

## Two capabilities on one foundation

**Register** is the shared foundation: every participant, whatever it does, gets a verifiable identity and a directory entry. On top of it sit two capabilities with **two different trust models**, and a participant adopts whichever its use cases need:

- **Data exchange (B2B)** — structured payloads (meter telemetry, regulatory filings, tariff data, trades) moving between **registered organisations**. Trust here is *bilateral*: each side looks the other up in the DeDi directory, verifies its signature, and checks that both belong to the same curated network — so the exchange must ride a trust-bounded open network, and IES uses **Beckn** for it. See [Discover](discover.md) and [Exchange](exchange.md).
- **Verifiable credentials (B2C)** — signed W3C Verifiable Credentials (a consumer's connection record, a meter digest). Trust here is *unilateral*: the issuer signs once against its published **`did:web`**, and any third party the issuer has never met — a bank, a marketplace — can verify it independently. Because the trust travels inside the credential, delivery can use **any channel**: DigiLocker, a web portal, email, SMS, chat. No Beckn network involved. See [Verifiable Credentials](energy-credentials/README.md).

The same [Schemas](../schemas/README.md) reference backs both: the schemas are the vocabulary of IES domain objects, and the shape of each object is described by its **schema** — a self-contained, machine-readable definition that is valid whether or not the payload ever travels over Beckn.

---

## Where the schema files live

The schema files (JSON Schema, JSON-LD context, RDF vocabulary, example payloads) live at the repository root in **[`schemas/`](../schemas/README.md)** so that their canonical published URLs (`https://india-energy-stack.github.io/ies-accelerator/schemas/...`) stay stable for external consumers.
