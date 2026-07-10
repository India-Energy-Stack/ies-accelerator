# Register

> **Step 1 of the three IES steps.** Every participant gets a verifiable digital identity, listed once in a shared directory.

Before two systems exchange data, each must **name** the other and **prove** identity — via two cooperating pieces:

| Piece | What it is | Standard |
|---|---|---|
| **Identifier** | A cryptographic name for an organisation, a regulator, a meter, a consumer, an asset, a credential or a dataset. | [W3C Decentralised Identifiers (DIDs)](https://www.w3.org/TR/did-core/) |
| **Directory** | A public, append-only registry that lists those identifiers — together with the keys, callback URLs, and revocation status that go with them. | [DeDi](../glossary.md#dedi) (Decentralised Directory Protocol) |

Anyone can resolve an IES identifier in milliseconds and verify its signature — no callback needed.

---

## What you set up under Register

**Register** produces two artefacts for a joining organisation:

1. **Your organisation's `did:web`** — a small JSON file (`did.json`) on a domain you control, verified against every credential and Beckn message you sign. See [Identifiers and Addressing](identifiers/README.md).

2. **Your DeDi namespace** — a public registry under your verified domain, holding records other participants look up: Beckn subscriber record (Discover), revocation list (credentials), asset registry where applicable. See [Registries and Directories](registries/README.md).

Step-by-step: **[How you implement IES → Setup Register](../how-you-implement-ies/setup-register.md)**.

---

## Why a verifiable identity, not a username

IES has no central platform to trust — every identifier is a **`did:web`** anchored to a domain the participant controls, so verifiers fetch the key and check signatures locally, no call back to IES. The same model covers the consumer (`did:key` in a wallet), the asset (a `did:web` path under the issuer's domain reusing the meter serial), and the dataset (a `did:web` under the publisher's domain) — one method, one flow, every actor.

---

## Detail pages

- **[Identifiers and Addressing](identifiers/README.md)** — DID methods, ID patterns, where each ID goes in a credential or Beckn message.
- **[Registries and Directories](registries/README.md)** — DeDi mechanics, the IES network registries, the curated allow-lists, OpenCred's auto-created registries.

---

## Where this fits

| Step | Page |
|---|---|
| Step 1 — Register *(this page)* | — |
| Step 2 — [Discover](discover.md) | Beckn-protocol interaction |
| Step 3 — [Exchange](exchange.md) | Schemas, credentials, taxonomy |

Hands-on: **[Setup Register](../how-you-implement-ies/setup-register.md)**.
