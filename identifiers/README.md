# IES Identifiers and Addressing

Every actor, asset, document, and dataset on the India Energy Stack needs an identifier that is **globally unique, cryptographically verifiable, and resolvable to a public key or a record**. IES does this with **W3C Decentralized Identifiers (DIDs)**, anchored in the **DeDi (Decentralised Data Infrastructure)** registry network on [`dedi.global`](https://dedi.global).

This section is the developer reference for **how IDs are minted, structured, registered, resolved, and routed** across the IES platform — both for the public IES network and for a DISCOM's private internal systems.

| Capability | Used for |
|---|---|
| `did:web` | Public, domain-anchored identity for issuers (DISCOMs, regulators, aggregators) |
| `did:key` / `did:jwk` | Lightweight identities for consumers, wallets, dev/test issuers |
| `did:dedi` (DeDi-anchored) | Registry entries on `dedi.global` for trust anchors, consumer/asset records, and revocation lists |
| IES address grammar | Deterministic mapping from a DISCOM's internal numbering (consumer no., meter no., asset ID) to a network-resolvable DID |

---

## What you can do with this section

1. **Identify a DISCOM or regulator** on the IES network in a way every verifier can resolve.
2. **Identify a consumer or an asset** under a DISCOM, *without changing* the DISCOM's internal CIS / GIS / asset-management numbering.
3. **Stand up a registry** — a public one on DeDi, or a private one inside the DISCOM — and resolve identifiers to records.
4. **Route requests** (credential issuance, Beckn data exchange, verification) to the correct DISCOM endpoint using only a DID.

---

## Reading order

| Doc | Read it for |
|---|---|
| [Concepts](./concepts.md) | DID 101 — methods, structure, how `did:web` and `did:dedi` work in IES |
| [ID Patterns](./id-patterns.md) | How to ID DISCOMs, consumers, assets, meters, regulators, credentials |
| [Registries](./registries.md) | Hosting a public DeDi registry; running a parallel private registry inside the DISCOM |
| [DeDi Primer](./dedi-primer.md) | Self-contained reference for what DeDi is, its three-coordinate model, proofs, and deployment options |
| [Registry Creation](./registry-creation.md) | Hands-on walkthrough: account, domain-verified namespace, registries, records (UI + API) |
| [Required Registries for Onboarding](./required-registries.md) | The baseline set of registries an IES participant needs — DISCOM reference, Beckn subscriber, revocation, public-keys, etc. |
| [Resolution](./resolution.md) | Workflows to resolve a DID and route a request to the right endpoint |
| [Issuance Reference](./issuance-reference.md) | Reference implementation: minting and registering IDs end-to-end |

---

## Design principles

These principles drive every choice in this section. If a future identifier doesn't fit, it should still satisfy these.

1. **DIDs are the only IDs that cross trust boundaries.** Internal numbers (consumer numbers, meter SAP IDs, GIS asset codes) stay inside the DISCOM. They are *wrapped* in a DID for cross-network use, never exposed as bare strings.
2. **DISCOMs keep their numbering.** A DID for a consumer must contain (or deterministically derive from) the DISCOM's existing consumer number. No re-numbering, no parallel ID universe to maintain.
3. **One public key per DID — but key rotation is cheap.** `did:web` rotation is a file replace; DeDi entries support multiple historical keys.
4. **Resolution is offline-friendly.** A verifier with the credential JSON and HTTPS access to `did.web` hosts plus `api.dedi.global` can verify without ever calling the issuing DISCOM.
5. **Private and public registries follow the same shape.** A DISCOM can run an internal mirror with the same record schema as the public DeDi registry, so promotion from internal to public is a copy, not a translation.

---

## Quick orientation by role

**DISCOM building integration** — start with [ID Patterns](./id-patterns.md), then [Registries](./registries.md).

**Verifier or wallet developer** — start with [Resolution](./resolution.md).

**Regulator or network operator** — start with [Concepts](./concepts.md), then [Registries](./registries.md) for the governance model.
