# Registries and Directories

The discovery and revocation layer. DeDi is the open registry runtime IES uses to anchor namespaces, publish subscriber records for Beckn participants, and check credential revocation — without any IES participant having to call the issuer.

> **First-time setup** — to claim a namespace, publish your trust anchor, and create the registries you need, follow **[Setup Register](../../how-you-implement-ies/setup-register.md)**. This page is the reference for *which* registries IES uses, what each one contains, and how the curated IES allow-lists are organised.

Upstream protocol documentation lives at [DeDi developer documentation](https://docs.nfh.global/dedi/dedi.global-developers/developer-documentation) and [Setting up a Beckn network](https://docs.nfh.global/beckn/creating-an-open-network/setting-up-the-network-environment).

---

## Why DeDi (and the three questions it answers)

When two organisations exchange data without trusting a central middleman, the receiver needs to answer three questions about the data — and DeDi is designed to answer all three through cryptography rather than calls to the publisher.

| Question | What DeDi gives you |
|---|---|
| **Integrity** — has this data changed since it was published? | Every record carries a BLAKE2 H256 digest anchored on the CORD blockchain. Recompute the digest, compare with the on-chain proof, done. Tampering is detectable. |
| **Validity** — is this data still current? | Version history per record, optional `valid_till`, a `state` field (`live` / `inactive` / `draft`), and dedicated revocation registries with `as_on=<date>` time-travel. |
| **Authenticity** — is the publisher who they claim to be? | A namespace is bound to a domain via a DNS TXT-record proof. Only the namespace controller's DID key can write under that namespace, and that DID resolves to the same domain. |

A verifier never has to call the publisher; they call DeDi. That is the whole reason IES routes trust through public registries — revocation, public-key lookup, network membership — instead of phoning the issuer every time.

DeDi itself is open-source ([Linux Foundation Decentralized Trust labs](https://github.com/LF-Decentralized-Trust-labs/decentralized-directory-protocol)); the default hosted runtime is [`dedi.global`](https://dedi.global).

---

## Registry tags used in IES

The IES-relevant tags. The first two come from DeDi's built-in templates; the others are custom shapes managed by OpenCred.

| Built-in tag | What it's for | Who creates it |
|---|---|---|
| `beckn_subscriber` | A Beckn participant's identity + signing key | You (any NP joining a Beckn network) |
| `beckn_subscriber_reference` | A pointer to another subscriber record or registry — the membership primitive NFOs use | The NFO |
| `public_key` | Versioned issuer public keys | OpenCred (or you, manually) |
| `revocation` | Per-credential revocation hashes | OpenCred (or you, manually) |

A practical rule of thumb: **create one registry per environment** (`subscribers-test`, `subscribers-prod`) so a misconfigured test run can't pollute a production lookup.

> **If you run OpenCred, four of these registries are managed for you on first boot** — `vc-revocation-registry`, `opencred-key-registry`, `schema_registry`, `context_registry`. The OpenCred container auto-creates them if missing and reuses them if they exist. Details: [Appendix A — OpenCred auto-creates four registries](#opencred-auto-creates-four-registries).

---

## The registries you'll touch in IES, by role

Pick the row that describes you. Each row tells you the **minimum** registries to operate yourself and which IES-side registries to ask to be **referenced into**.

### As a DISCOM / issuer running OpenCred

| Registry | Who creates | Purpose |
|---|---|---|
| `<discom>/vc-revocation-registry` | OpenCred (auto) | Per-credential revocation status |
| `<discom>/opencred-key-registry` | OpenCred (auto) | Your versioned signing keys |
| `<discom>/schema_registry` | OpenCred (auto) | JSON Schemas you use |
| `<discom>/context_registry` | OpenCred (auto) | JSON-LD contexts |

To **issue credentials**, that's all you need on the registry side. The credential's trust chain is your `did:web` plus, optionally, the regulator's `issuer.idRef` — no IES-curated registry entry required. See [Identifiers and Addressing](../identifiers/README.md).

To also **exchange data over Beckn**, add the Beckn-participant rows below.

### As a Beckn Network Participant (BAP / BPP, aggregator, AMISP, trading platform)

| Registry | Who creates | Purpose |
|---|---|---|
| `<your-namespace>/subscribers-test` | You | Your BAP/BPP subscriber record (test environment) |
| `<your-namespace>/subscribers-prod` | You | Same, production |
| **IES network registry** | NFO writes a reference pointing at your record | Marks you as in-network for a specific IES Beckn network |

The IES network registries — `ies-data-sharing-network`, `ies-p2p-trading-network`, `ies-der-integration-network` (plus their `test-` variants) — are operated by the IES network operator (acting as [NFO](../../glossary.md#nfo)). You don't write to them directly; the NFO references your record after a short onboarding review. See [IES networks and registries today](#ies-networks-and-registries-today) below for the names and how to apply.

The end-to-end "publish your subscriber details + get added to a network" walkthrough is in [Identifiers and Addressing — Appendix E](../identifiers/README.md#appendix-e-joining-a-beckn-network-subscriber-registry-on-the-beckn-fabric).

### As an NFO

*([Network Facilitator Organisation](../../glossary.md#nfo) — the organisation that curates a Beckn network.)*

| Registry | Who creates | Purpose |
|---|---|---|
| `<nfo-namespace>/<network-name>` (tag `beckn_subscriber_reference`) | You (the NFO) | The curated network — references to NP-owned subscriber records or whole subscriber registries |

The `network_id` is `<nfo-domain>/<network-name>`. One registry per network you facilitate (typically separate `test-` and `prod` variants per sector). Membership is curated by **writing reference records that point at NP-owned subscriber records on DeDi** — you do not copy NP data into the network registry.

For the NFO operational details (manifest, network policies, key rotation), refer to the NFH docs on [setting up the network environment](https://docs.nfh.global/beckn/creating-an-open-network/setting-up-the-network-environment) and [configuring network policies](https://docs.nfh.global/beckn/creating-an-open-network/configuring-network-policies).

### As a verifier or wallet

You don't write to anything; you only read. Two registries matter:

| When you want to … | Read |
|---|---|
| Verify a credential's signature | The issuer's own `did:web` (`.well-known/did.json`) — and, if you cache, the issuer's `opencred-key-registry` for key history |
| Check revocation status | The issuer's `vc-revocation-registry` |

A worked verification walkthrough is in [Appendix B](#appendix-b-verifying-a-credential-end-to-end).

---

## IES networks and registries today

The IES network operator publishes its registries under the namespace `india-energy-stack`, anchored to the domain `indiaenergystack.in`, with namespace DID:

```
did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma
```

You can list everything in the namespace at any time:

```bash
curl https://api.dedi.global/dedi/query/indiaenergystack.in | jq '.data.registries[] | {registry_name, description, tag, record_count}'
```

At time of writing the namespace holds **14 registries**, grouped below:

### Beckn networks (NFO-operated reference registries)

| Registry | Env | Purpose |
|---|---|---|
| `ies-data-sharing-network` | prod | Network for energy data sharing (DISCOM ↔ DISCOM, regulators, aggregators) |
| `test-ies-data-sharing-network` | test | Same, for evaluation and conformance |
| `ies-p2p-trading-network` | prod | P2P energy trading between consumers, prosumers, and aggregators |
| `test-ies-p2p-trading-network` | test | Same, test |
| `ies-der-integration-network` | prod | DER (rooftop solar, BESS, EV) integration with DISCOMs |
| `test-ies-der-integration-network` | test | Same, test |

All carry the `beckn_subscriber_reference` tag and are curated by the [NFO](../../glossary.md#nfo) (the IES network operator). To get a participant listed in any of them, see [How to apply](#how-to-apply-for-an-ies-listing) below.

### Reference allow-lists (industry coordination)

| Registry | Tag | Purpose |
|---|---|---|
| `ies-discoms-reference-registry` | `beckn_subscriber_reference` | Curated allow-list of recognised DISCOMs |
| `ies-regulators-reference-registry` | `beckn_subscriber_reference` | Curated allow-list of recognised regulators (SERCs, CERC) |
| `ies-service-providers-reference-registry` | `beckn_subscriber_reference` | Curated allow-list of service providers (consultancies, integrators) |
| `test-ies-discoms-reference-registry` | `beckn_subscriber_reference` | Test variant of the DISCOMs list |

These are the curated industry-coordination lists that NFOs (including the IES NFO) reference into network registries to enforce a trust boundary. Credential issuance does **not** require an entry here — see [Identifiers and Addressing — Two identities](../identifiers/README.md#two-identities-youll-set-up-and-why).

### How to apply for an IES listing

Send an email with the fields below to the IES Secretariat. They write the reference record once they've verified you:

| Channel | Address |
|---|---|
| Email (primary) | [IES.Secretariat@fsrglobal.org](mailto:IES.Secretariat@fsrglobal.org) |
| Email (alternate) | [ies@recindia.com](mailto:ies@recindia.com) |
| Web | [ies.fsrglobal.org](https://ies.fsrglobal.org/#footer) |

What to send (fields the Secretariat needs to write your reference record):

- Your short identifier (`<discom-short-code>` for DISCOMs, FQDN for NPs).
- Your verified DeDi namespace (e.g. `tpddl`, `np.example.com`).
- The DeDi lookup URL of either your **whole subscriber registry** (typically `subscribers-prod`) or a **single record** inside it — your choice depends on whether all your subscribers belong to the network or only some.
- Whether the URL is a `Registry` or a `Record` (one of those two values).
- Which IES network(s) you want to join (`ies-data-sharing-network` and/or `ies-p2p-trading-network` and/or `ies-der-integration-network`, plus the `test-` variant if you want sandbox first).
- Role: `BAP`, `BPP`, or both.
- Service areas / countries (`IND` for India).
- A point of contact (name, email, phone).

Before approving, the Secretariat validates: your namespace is domain-verified, your callback URL is reachable, your signing public key is present and valid, and the role you've declared matches your network entitlement.

---

## Setup

The step-by-step to claim a namespace, verify your domain and create the registries you need is in **[Setup Register](../../how-you-implement-ies/setup-register.md)**. Step-by-step Beckn subscriber registration is in **[Setup Discovery](../../how-you-implement-ies/setup-discovery.md)**.

---

## Appendix A — DeDi primer (just enough to navigate)

This appendix is a condensed orientation. For the full developer reference, go to the [NFH DeDi docs](https://docs.nfh.global/dedi/dedi.global-developers/developer-documentation).

### The three-coordinate model

```
api.dedi.global
└── <namespace>              ← owned by one verified domain; only the controller's DID key can write
    └── <registry>           ← a typed collection of records (schema = built-in tag or custom JSON Schema)
        └── <record-id>      ← a specific record — the resolvable end-point
            └── { record JSON }
```

Three things uniquely address any record: **namespace + registry + record-id**. The namespace is the unit of governance; the registry is the unit of schema; the record is the unit of data.

### Built-in schema tags used in IES

| Tag | Required fields | Used for |
|---|---|---|
| `beckn_subscriber` | `subscriber_id`, `url`, `type` (BAP/BPP), `countries`, `signing_public_key` | A participant's identity on a Beckn network |
| `beckn_subscriber_reference` | `subscriber_id`, `url`, `type` (Registry/Record) | A pointer that includes another subscriber record or registry into a network |
| `public_key` | Key id, JWK, validity window | Versioned signing keys for an issuer |
| `revocation` | Credential hash, status | Per-credential revocation entries |

### OpenCred auto-creates four registries

If you run [OpenCred](../../glossary.md#opencred), it manages four of these registries for you on first boot:

| Registry | Tag | OpenCred behaviour |
|---|---|---|
| `vc-revocation-registry` | `revocation` | Auto-created if missing; reused if it already exists |
| `opencred-key-registry` | `public_key` | Auto-created if missing; reused if it already exists |
| `schema_registry` | custom | Auto-created if missing; reused if it already exists |
| `context_registry` | custom | Auto-created if missing; reused if it already exists |

OpenCred's startup hook calls `ensureRegistries()` on first boot; idempotent restarts log "already published" and continue. Required env vars: `OPENCRED_DEDI_BASE_URL`, `OPENCRED_DEDI_AUTH_TYPE` (`api-key` or `bearer`), `OPENCRED_DEDI_NAMESPACE`, plus matching credentials. See the [OpenCred deployment docs](https://opencred.gitbook.io/docs/docker-image/deployment).

A caveat from OpenCred's docs: if those registries pre-exist with **schemas that don't match OpenCred's expectations** (e.g. DeDi's built-in `public_key` tag with a different shape), `/v1/keys/publish` will fail validation. So either let OpenCred create them, or pre-create them with OpenCred's exact schemas — don't mix.

### API at a glance

| Operation | Endpoint shape |
|---|---|
| Resolve a record | `GET /dedi/lookup/<namespace>/<registry>/<record-id>` |
| List records in a registry | `GET /dedi/query/<namespace>/<registry>?filter=...` |
| List registries in a namespace | `GET /dedi/query/<namespace>` |
| Time-travel | append `?as_on=YYYY-MM-DD` |
| Pin a version | append `?version_id=<id>` |
| Create / update a record | signed write by the namespace controller |

### Deployment options

Two practical options today:

| Option | What it is | When to choose |
|---|---|---|
| **Hosted on `dedi.global`, embedded in your site** | You publish on `dedi.global`; your own site surfaces the data via the public API or a widget. Zero infra cost, you keep human-facing branding. | Default for institutional publishers (DISCOMs, regulators) who already operate a public website. |
| **Hosted on `dedi.global` only** | Same publish flow; consumers query `api.dedi.global` directly, no embedding. | Simplest path — appropriate when there is no public site to embed in, or the registry is purely machine-to-machine. |

A self-hosted DDP node is technically possible (the protocol is open-source) but no IES participant operates one today; revisit only if you have a hard requirement.

### State, versioning, time-travel

A record never disappears silently — DeDi tracks the full history.

| Concept | Behaviour |
|---|---|
| **Versions** | Every update creates a new version. `version_count` and `version` returned on lookups. |
| **Historical lookup** | `?as_on=YYYY-MM-DD` returns the version current on that date. |
| **Version pin** | `?version_id=<id>` returns one specific version. |
| **Registry state** | `live` (queryable) or `inactive` (disabled, recoverable). |
| **Record state** | `draft` (saved, unpublished) or `live` (published, queryable). |
| **TTL** | Optional time-to-live in seconds; default 600. |

---

## Appendix B — Verifying a credential, end-to-end

This is the one worked workflow worth carrying inline; everything else hangs off it.

A wallet hands a verifier a signed ElectricityCredential. The verifier:

1. **Parse** the credential JSON. Read `issuer.id` (e.g. `did:web:ies.tpddl.in`).
2. **Resolve `issuer.id`** over HTTPS — fetch `https://ies.tpddl.in/.well-known/did.json` and extract the `verificationMethod` public key.
3. **Verify the credential's `proof`** signature against that key. If it fails, stop — the credential is forged or corrupted.
4. **(Optional) Check `issuer.idRef`** if present. Resolve `issuer.idRef.issuedBy` (the regulator's `did:web`) and confirm the regulator vouches for this DISCOM under the cited `subjectId`. This is the licensing leg of the trust chain; skip when `idRef` is absent.
5. **Check revocation.** GET the URL in `credentialStatus.id` — typically `https://api.dedi.global/dedi/lookup/<discom>/vc-revocation-registry/<credential-id>`. A `404` (or `status: not_revoked`) means valid; a record with `status: revoked` means rejected.
6. **Check validity window.** Confirm `validFrom <= now <= validUntil`.

A verifier that caches the issuer's `did.json` and the regulator's `did.json` (e.g. refresh every 10 minutes) can complete steps 2–4 entirely offline; only step 5 needs a live DeDi lookup.

---

## Appendix C — Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| `404` on `GET /dedi/lookup/<namespace>/<registry>/<record-id>` | Wrong record-id (case-sensitive), or the record was never published (left as `draft`) | Verify in the DeDi console; re-issue with the correct id |
| `403 / signature invalid` on write | Namespace controller key changed, or you're signing with the wrong key | Confirm you are using the key currently bound to the namespace |
| DNS TXT verification stuck on "pending" for > 1 hour | Propagation delay (normal up to 48 h) or wrong record in zone | Check with `dig +short TXT <your-domain>`; ensure the record matches what DeDi issued |
| OpenCred `/v1/keys/publish` returns a validation error | A pre-existing registry has a schema OpenCred does not recognise | Either delete and let OpenCred recreate, or align the registry's schema to OpenCred's expectations — see [OpenCred deployment](https://opencred.gitbook.io/docs/docker-image/deployment) |
| Beckn counterparty cannot find your subscriber | Network reference not yet written, or you're looking at the wrong env | Verify the lookup URL the NFO wrote; check that `test-` vs prod matches the network you're targeting |
