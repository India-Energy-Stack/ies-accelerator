# Register

> **Step 1 of the three IES steps.** Verifiable digital identity. Every participant gets a digital identity and is listed in a shared directory. *Done once.*

Register is the foundation. Before any two systems can exchange data, both must be able to **name** each other and **prove** they are who they claim to be. IES does this with two cooperating pieces:

| Piece | What it is | Standard |
|---|---|---|
| **Identifier** | A cryptographic name for an organisation, a regulator, a meter, a consumer, an asset, a credential or a dataset. | [W3C Decentralised Identifiers (DIDs)](https://www.w3.org/TR/did-core/) |
| **Directory** | A public, append-only registry that lists those identifiers — together with the keys, callback URLs, and revocation status that go with them. | [DeDi](glossary.md#dedi) (Decentralised Directory Protocol) |

Anyone can resolve an IES identifier in milliseconds, with no callback to the publisher, and check that a signature matches the registered key.

---

## What you set up under Register

For an organisation joining IES, **Register** is one step but produces two artefacts:

1. **Your organisation's `did:web`** — a small JSON file (`did.json`) published on a domain you control. This is what every credential you sign and every Beckn message you send is verified against. See [Identifiers and Addressing](identifiers/README.md).

2. **Your DeDi namespace** — a public registry container under your verified domain. Inside it sit the records that other IES participants look up — your Beckn subscriber record (for the Discover step), your revocation list (for credentials), your asset registry where applicable. See [Registries and Directories](registries/README.md).

For the step-by-step setup, follow **[How you implement IES → Setup Register](implementation/setup-identity.md)**.

---

## Why a verifiable identity, not a username

A username on a central platform is only as trustworthy as the platform. IES has no central platform. Every IES identifier is a **`did:web`** anchored to a domain the participant controls — verifiers fetch the public key directly from that domain, check signatures locally, and never need to call IES to confirm identity.

The same model covers the consumer (`did:key` in a wallet), the asset (a `did:web` path under the issuer's domain that reuses the existing meter serial), and the dataset (a `did:web` under the publisher's domain). One method, one resolution flow, every actor.

---

## Detail pages

- **[Identifiers and Addressing](identifiers/README.md)** — DID methods used, ID patterns, where each ID goes in a credential or a Beckn message.
- **[Registries and Directories](registries/README.md)** — DeDi mechanics, the IES network registries, the curated allow-lists, OpenCred's auto-created registries.

---

## Where this fits

| Step | Page |
|---|---|
| Step 1 — Register *(this page)* | — |
| Step 2 — [Discover](discover.md) | Beckn-protocol interaction |
| Step 3 — [Exchange](exchange.md) | Schemas, credentials, taxonomy |

To set up your organisation's identity hands-on: **[Setup Register](implementation/setup-identity.md)**.
