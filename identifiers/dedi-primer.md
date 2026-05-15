# DeDi Primer

This page is a self-contained reference for **DeDi** — the registry layer that every IES public registry is built on. Read it before [Registry Creation](./registry-creation.md) and [Required Registries](./required-registries.md). You should not need to leave this page (or follow links to external docs) to understand what DeDi is and what shape a DeDi registry has.

---

## What DeDi is

**DeDi (Decentralised Directory / Decentralised Data Infrastructure)** is an open protocol and a hosted platform for publishing **public registries** as machine-readable, cryptographically verifiable JSON directories accessible over a standard HTTP API.

The protocol is open (Linux Foundation Decentralized Trust, "DDP" — Decentralised Directory Protocol). The default hosted platform is operated by Networks for Humanity Foundation and lives at:

| Surface | URL |
|---|---|
| Publish console (UI) | [`publish.dedi.global`](https://publish.dedi.global) |
| Read API | `https://api.dedi.global` |
| DID host (auto-generated DID Documents) | `https://did.cord.network` |
| Anchoring blockchain | CORD (`apps.cord.network`) — BLAKE2 H256 hashing |

You can equivalently run a **self-hosted DDP node** on your own infrastructure and remain interoperable with `api.dedi.global` and every other DDP node. The protocol guarantees portability — registries published on one node can be migrated to another.

---

## The three-coordinate model

DeDi organises everything as a **three-level tree**. This is the single mental model you need.

```
namespace
└── registry
    └── record
        └── { JSON payload + cryptographic proof }
```

| Level | What it is | Governance |
|---|---|---|
| **Namespace** | The trust anchor for an organisation. Owned by exactly one creator account. Optionally bound to a DNS domain via TXT-record verification. | Only the namespace owner's account/keys can create registries or write records under it. |
| **Registry** | A typed collection of records inside a namespace. Has a schema (custom JSON Schema or a built-in template) and a `tag` that classifies it. | Inherits from the namespace owner. |
| **Record** | A single entry inside a registry. Conforms to the registry's schema. Has a stable `record_name` and `record_id`, plus a version history. | Inherits from the namespace owner. |

Every level has a deterministic resolver URL:

```
GET  /dedi/lookup/<namespace>
GET  /dedi/lookup/<namespace>/<registry>
GET  /dedi/lookup/<namespace>/<registry>/<record>
```

Every response includes a **cryptographic proof** anchored on CORD.

---

## Identifiers and proofs

Each level gets an auto-generated DID. The platform publishes the DID Document at `https://did.cord.network/{id}/did.json`, and the DID itself takes the form:

```
did:web:did.cord.network:<id>
```

For example, the IES network operator's namespace DID is:

```
did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma
```

Every read response carries a `proof` block. The three proof types are:

```json
// Namespace
{
  "type": "DediNamespaceProof2025",
  "namespace_did": "did:dedi:namespace:acme-org",
  "creator_did": "did:web:acme.org#admin",
  "digest": "0x8f3c91a2b7d4e918c0d55eab3c1a9e4e21e9f8c3d7c6b1a2f4c9d88e1a7b3f22",
  "network_genesis": "0x93abf42c1d77e8f0a928f31fd29d77bd73cd91eb99f15e41f6d39e087ac3b22c"
}

// Registry
{
  "type": "DediRegistryProof2025",
  "namespace_did": "did:dedi:ns:acme.global",
  "registry_identifier": "registry:acme.membership",
  "creator_did": "did:web:acme.org#admin",
  "digest": "0x91ef3ab2c77dd9f01892bf31cd29b8ae7f5dd321ee019ec45bd119ab4cf72d11",
  "network_genesis": "0x93abf42c1d77e8f0a928f31fd29d77bd73cd91eb99f15e41f6d39e087ac3b22c"
}

// Record
{
  "type": "DediRecordProof2025",
  "namespace_did": "did:dedi:ns:acme.global",
  "registry_identifier": "registry:acme.membership",
  "record_identifier": "record:acme.membership.member123",
  "creator_did": "did:web:acme.org#issuer1",
  "digest": "0xa17cd92be81f7c0da923ff10efa92b9b37cd10aa8e1c4ff2342dd19cbf9023af",
  "network_genesis": "0x93abf42c1d77e8f0a928f31fd29d77bd73cd91eb99f15e41f6d39e087ac3b22c"
}
```

**Verification procedure** (used by a relying party that already has a record JSON):

1. Extract the canonical fields the proof covers.
2. Serialise into a canonical JSON object.
3. `JSON.stringify()` it.
4. Compute the BLAKE2 H256 digest.
5. Compare against `proof.digest`.
6. Optionally, look up the digest on CORD explorer (`apps.cord.network`) to confirm on-chain anchoring.

`network_genesis` pins which CORD network the proof is anchored to — it is the same string for every record on the same network, and lets a verifier reject proofs from a wrong/unknown CORD network.

---

## The three trust pillars

A registry on DeDi exists to let a third party answer three questions about a piece of data, without trusting anyone but the cryptography:

| Pillar | Question | DeDi answer |
|---|---|---|
| **Integrity** | Has this data changed since it was published? | Record digest is anchored on CORD. Recompute, compare, done. |
| **Validity** | Is this data current — not expired, not revoked? | Version history, `valid_till`, `state` (`live`/`inactive`/`draft`), and revocation registries. |
| **Authenticity** | Is the publisher who they claim to be? | Namespace tied to a verified DNS domain + creator DID + on-chain proof. |

These pillars are why IES uses DeDi for things like the DISCOM reference list and revocation: the verifier never has to call the DISCOM to trust a credential — they call DeDi.

---

## Deployment options

There are three ways to run a registry on the DDP protocol. Pick once per registry — they are interoperable.

### Option A — DeDi.global hosted, embedded in your site

You publish on `dedi.global` and surface the data on your own website via the API or a widget. The records are read-anywhere; your site simply renders them. **Zero infrastructure cost**, you keep human-facing branding and full data ownership.

### Option B — DeDi.global hosted only

Same publish flow, but you do not embed anything; consumers query `api.dedi.global` directly. **Simplest path** — appropriate when there is no public website to embed in, or when the registry is purely machine-to-machine.

### Option C — Self-hosted DDP node

Deploy the open-source DDP server on your own infrastructure. Records anchored on your node are still interoperable with `api.dedi.global` and any other node. You take on uptime, patching, and CORD anchoring operations. **Choose this only if you have a hard requirement to self-host** — most IES participants do not.

For the IES public registries described in [Required Registries](./required-registries.md), the network operator currently uses Option B; individual DISCOMs typically use Option A or B for their own registries.

---

## State, versioning, and time-travel

A record never disappears silently — DeDi tracks the full history.

| Concept | Behaviour |
|---|---|
| **Versions** | Every update creates a new version. `version_count` and `version` are returned on lookups. |
| **Historical lookup** | Append `?as_on=YYYY-MM-DD` to any lookup to retrieve the version that was current on that date. |
| **Version pinning** | Append `?version_id=<id>` to retrieve a specific version. |
| **State (registry)** | `live` (active, queryable) or `inactive` (disabled but recoverable). |
| **State (record)** | `draft` (saved but unpublished) or `live` (published, queryable). |
| **TTL** | Optional time-to-live, in seconds; default 600s where unset. After TTL, a record is no longer served as current (history is preserved). |
| **`valid_till`** | Optional ISO timestamp at which a record becomes invalid (used for credential-style validity windows). |
| **Restore window** | Deleted entities are recoverable for a configurable grace period (default 7 days) before permanent archival. |

This is what lets a verifier ask: *"was the issuer's key valid on the date the credential was signed?"* — without trusting the issuer's word for it.

---

## API at a glance

The full developer reference for both Publish and Access APIs lives in the next page ([Registry Creation](./registry-creation.md)); this is a one-screen orientation.

**Read (no auth required, public registries):**

```http
GET  https://api.dedi.global/dedi/lookup/<namespace>
GET  https://api.dedi.global/dedi/lookup/<namespace>/<registry>
GET  https://api.dedi.global/dedi/lookup/<namespace>/<registry>/<record>
GET  https://api.dedi.global/dedi/query/<namespace>?status=active
GET  https://api.dedi.global/dedi/query/<namespace>/<registry>?state=live
```

**Write (Bearer token, owner-only):**

```http
POST https://api.dedi.global/dedi/create-namespace
POST https://api.dedi.global/dedi/<namespace>/create-registry
POST https://api.dedi.global/dedi/<namespace>/<registry>/save-record-as-draft
POST https://api.dedi.global/dedi/<namespace>/<registry>/publish-records
POST https://api.dedi.global/dedi/bulk-upload
```

**Error codes** follow standard HTTP: `400` validation, `401` missing/invalid token, `403` not owner, `404` not found, `429` rate-limited, `5xx` server.

---

## Built-in schema templates

DeDi ships **five pre-built schema tags** so the most common registry kinds do not require you to write a JSON Schema by hand:

| Tag | Used for | IES example |
|---|---|---|
| `membership` | "X is a recognised member of Y" lists | DISCOM/regulator reference list |
| `public_key` | Versioned signing keys with rotation history | DISCOM issuer keys |
| `revoke` | Credential revocation entries | VC revocation registry |
| `beckn_subscriber` | Beckn BAP/BPP subscriber record (subscriber_id, URL, type, signing public key) | IES test/prod NP subscriber records |
| `beckn_subscriber_reference` | A pointer that includes another subscriber registry or record into a Beckn network | IES network reference registry |

You select the tag when you create the registry. Records you then add are validated against the corresponding schema. Field-level definitions for `beckn_subscriber` / `beckn_subscriber_reference` are documented in [Required Registries](./required-registries.md#beckn-subscriber-registry).

You can also pass a fully custom `schema` (a JSON Schema object) when you do not want a built-in tag.

---

## Why a DeDi registry is not just a database

A naive way to expose a list of DISCOMs would be a JSON file on a web server. The reason IES does not do that:

| Problem with "JSON on a web server" | DeDi answer |
|---|---|
| No history — last-write-wins, you cannot prove what was true yesterday | Every version is preserved and queryable via `?as_on=` / `?version_id=` |
| Tampering is undetectable — operator can rewrite silently | Every record is hashed and anchored on a public blockchain |
| No machine-readable governance — who is allowed to write? | Namespace ownership is enforced by signed writes; DNS verification ties it to a real-world domain |
| Schema drift — fields change shape over time, breaking consumers | Registry-level schema (or a built-in tag) makes the shape contract explicit and verifiable |
| Revocation is ad-hoc — each issuer invents its own scheme | A `revoke`-tagged registry under each issuer namespace is a uniform pattern that every verifier understands |

These are the load-bearing properties; they are why the rest of the IES identifier stack uses DeDi as the trust layer.

---

Next: [Registry Creation](./registry-creation.md) — concrete step-by-step for getting a namespace verified, a registry created, and records published.
