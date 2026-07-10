# Registries and Directories

DeDi is IES's open registry runtime for anchoring namespaces, publishing Beckn subscriber records, and checking credential revocation — without calling the issuer.

> **First-time setup:** claim a namespace, publish your trust anchor, and create registries via **[Setup Register](../../how-you-implement-ies/setup-register.md)**.

Upstream docs: [DeDi developer documentation](https://docs.nfh.global/dedi/dedi.global-developers/developer-documentation), [Setting up a Beckn network](https://docs.nfh.global/beckn/creating-an-open-network/setting-up-the-network-environment).

---

## Why DeDi (and the three questions it answers)

Exchanging data without a middleman, the receiver needs answers to three questions — DeDi answers all three cryptographically, so a verifier calls DeDi, never the publisher.

| Question | What DeDi gives you |
|---|---|
| **Integrity** — has this data changed since it was published? | Every record carries a BLAKE2 H256 digest anchored on the CORD blockchain. Recompute the digest, compare with the on-chain proof, done. Tampering is detectable. |
| **Validity** — is this data still current? | Version history per record, optional `valid_till`, a `state` field (`live` / `inactive` / `draft`), and dedicated revocation registries with `as_on=<date>` time-travel. |
| **Authenticity** — is the publisher who they claim to be? | A namespace is bound to a domain via a DNS TXT-record proof. Only the namespace controller's DID key can write under that namespace, and that DID resolves to the same domain. |

DeDi itself is open-source ([Linux Foundation Decentralized Trust labs](https://github.com/LF-Decentralized-Trust-labs/decentralized-directory-protocol)); the default hosted runtime is [`dedi.global`](https://dedi.global).

---

## Registry tags used in IES

The IES-relevant tags: the first two are DeDi's built-in templates; the rest are custom shapes managed by OpenCred.

| Built-in tag | What it's for | Who creates it |
|---|---|---|
| `beckn_subscriber` | A Beckn participant's identity + signing key | You (any NP joining a Beckn network) |
| `beckn_subscriber_reference` | A pointer to another subscriber record or registry — the membership primitive NFOs use | The NFO |
| `public_key` | Versioned issuer public keys | OpenCred (or you, manually) |
| `revocation` | Per-credential revocation hashes | OpenCred (or you, manually) |

**Create one registry per environment** (`subscribers-test`, `subscribers-prod`) so a misconfigured test run can't pollute production.

> **Running OpenCred auto-creates four registries on first boot** — `vc-revocation-registry`, `opencred-key-registry`, `schema_registry`, `context_registry`. See [Appendix A](#opencred-auto-creates-four-registries).

---

## The registries you'll touch in IES, by role

Pick your row: the **minimum** registries to operate yourself, and which IES-side registries to ask to be **referenced into**.

### As a DISCOM / issuer running OpenCred

| Registry | Who creates | Purpose |
|---|---|---|
| `<discom>/vc-revocation-registry` | OpenCred (auto) | Per-credential revocation status |
| `<discom>/opencred-key-registry` | OpenCred (auto) | Your versioned signing keys |
| `<discom>/schema_registry` | OpenCred (auto) | JSON Schemas you use |
| `<discom>/context_registry` | OpenCred (auto) | JSON-LD contexts |

To **issue credentials**, that's all you need — the trust chain is your `did:web` plus, optionally, the regulator's `issuer.idRef`, with no IES-curated registry entry required (see [Identifiers and Addressing](../identifiers/README.md)). To also **exchange data over Beckn**, add the rows below.

### As a Beckn Network Participant (BAP / BPP, aggregator, AMISP, trading platform)

| Registry | Who creates | Purpose |
|---|---|---|
| `<your-namespace>/subscribers-test` | You | Your BAP/BPP subscriber record (test environment) |
| `<your-namespace>/subscribers-prod` | You | Same, production |
| **IES network registry** | NFO writes a reference pointing at your record | Marks you as in-network for a specific IES Beckn network |

The IES network registries — `ies-data-sharing-network`, `ies-p2p-trading-network`, `ies-der-integration-network` (plus `test-` variants) — are operated by the network operator (the [NFO](../../glossary.md#nfo)), who references your record after a short onboarding review; see [IES networks and registries today](#ies-networks-and-registries-today) below, and the full walkthrough in [Identifiers and Addressing — Appendix E](../identifiers/README.md#appendix-e-joining-a-beckn-network-subscriber-registry-on-the-beckn-fabric).

### As an NFO

*([Network Facilitator Organisation](../../glossary.md#nfo) — the organisation that curates a Beckn network.)*

| Registry | Who creates | Purpose |
|---|---|---|
| `<nfo-namespace>/<network-name>` (tag `beckn_subscriber_reference`) | You (the NFO) | The curated network — references to NP-owned subscriber records or whole subscriber registries |

The `network_id` is `<nfo-domain>/<network-name>` (one registry per network, typically separate `test-`/`prod` variants per sector). Membership is curated by **writing reference records that point at NP-owned subscriber records on DeDi**, not by copying NP data in.

NFO operational details (manifest, network policies, key rotation) are in the NFH docs on [setting up the network environment](https://docs.nfh.global/beckn/creating-an-open-network/setting-up-the-network-environment) and [configuring network policies](https://docs.nfh.global/beckn/creating-an-open-network/configuring-network-policies).

### As a verifier or wallet

Two registries matter:

| When you want to … | Read |
|---|---|
| Verify a credential's signature | The issuer's own `did:web` (`.well-known/did.json`) — and, if you cache, the issuer's `opencred-key-registry` for key history |
| Check revocation status | The issuer's `vc-revocation-registry` |

Worked walkthrough: [Appendix B](#appendix-b-verifying-a-credential-end-to-end).

---

## IES networks and registries today

The IES network operator publishes its registries under the namespace `india-energy-stack`, anchored to the domain `indiaenergystack.in`, with namespace DID:

```
did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma
```

List everything in the namespace:

```bash
curl https://api.dedi.global/dedi/query/indiaenergystack.in | jq '.data.registries[] | {registry_name, description, tag, record_count}'
```

Currently **14 registries**, grouped below:

### Beckn networks (NFO-operated reference registries)

| Registry | Env | Purpose |
|---|---|---|
| `ies-data-sharing-network` | prod | Network for energy data sharing (DISCOM ↔ DISCOM, regulators, aggregators) |
| `test-ies-data-sharing-network` | test | Same, for evaluation and conformance |
| `ies-p2p-trading-network` | prod | P2P energy trading between consumers, prosumers, and aggregators |
| `test-ies-p2p-trading-network` | test | Same, test |
| `ies-der-integration-network` | prod | DER (rooftop solar, BESS, EV) integration with DISCOMs |
| `test-ies-der-integration-network` | test | Same, test |

All carry the `beckn_subscriber_reference` tag, curated by the [NFO](../../glossary.md#nfo); to get listed, see [How to apply](#how-to-apply-for-an-ies-listing) below.

### Reference allow-lists (industry coordination)

| Registry | Tag | Purpose |
|---|---|---|
| `ies-discoms-reference-registry` | `beckn_subscriber_reference` | Curated allow-list of recognised DISCOMs |
| `ies-regulators-reference-registry` | `beckn_subscriber_reference` | Curated allow-list of recognised regulators (SERCs, CERC) |
| `ies-service-providers-reference-registry` | `beckn_subscriber_reference` | Curated allow-list of service providers (consultancies, integrators) |
| `test-ies-discoms-reference-registry` | `beckn_subscriber_reference` | Test variant of the DISCOMs list |

NFOs (including the IES NFO) reference these curated lists into network registries to enforce a trust boundary; credential issuance does **not** require an entry here — see [Identifiers and Addressing — Two identities](../identifiers/README.md#two-identities-youll-set-up-and-why).

### How to apply for an IES listing

Email the fields below to the IES Secretariat; they write the reference record once they've verified you:

| Channel | Address |
|---|---|
| Email (primary) | [IES.Secretariat@fsrglobal.org](mailto:IES.Secretariat@fsrglobal.org) |
| Email (alternate) | [ies@recindia.com](mailto:ies@recindia.com) |
| Web | [ies.fsrglobal.org](https://ies.fsrglobal.org/#footer) |

Fields the Secretariat needs:

- Your short identifier (`<discom-short-code>` for DISCOMs, FQDN for NPs).
- Your verified DeDi namespace (e.g. `discom`, `np.example.com`).
- The DeDi lookup URL of either your **whole subscriber registry** (typically `subscribers-prod`) or a **single record** inside it.
- Whether the URL is a `Registry` or a `Record` (one of those two values).
- Which IES network(s) to join (`ies-data-sharing-network`, `ies-p2p-trading-network`, `ies-der-integration-network`, plus the `test-` variant for sandbox).
- Role: `BAP`, `BPP`, or both.
- Service areas / countries (`IND` for India).
- A point of contact (name, email, phone).

Before approving, the Secretariat checks: domain-verified namespace, reachable callback URL, valid signing public key, and declared role matching your network entitlement.

---

## Setup

Namespace, domain verification, and registries: **[Setup Register](../../how-you-implement-ies/setup-register.md)**. Beckn subscriber registration: **[Setup Discovery](../../how-you-implement-ies/setup-discovery.md)**.

---

## Appendix A — DeDi primer (just enough to navigate)

A condensed orientation; full developer reference: [NFH DeDi docs](https://docs.nfh.global/dedi/dedi.global-developers/developer-documentation).

### The three-coordinate model

```
api.dedi.global
└── <namespace>              ← owned by one verified domain; only the controller's DID key can write
    └── <registry>           ← a typed collection of records (schema = built-in tag or custom JSON Schema)
        └── <record-id>      ← a specific record — the resolvable end-point
            └── { record JSON }
```

Any record is addressed by **namespace + registry + record-id** — the namespace is the unit of governance, the registry the unit of schema, the record the unit of data.

### Built-in schema tags used in IES

| Tag | Required fields | Used for |
|---|---|---|
| `beckn_subscriber` | `subscriber_id`, `url`, `type` (BAP/BPP), `countries`, `signing_public_key` | A participant's identity on a Beckn network |
| `beckn_subscriber_reference` | `subscriber_id`, `url`, `type` (Registry/Record) | A pointer that includes another subscriber record or registry into a network |
| `public_key` | Key id, JWK, validity window | Versioned signing keys for an issuer |
| `revocation` | Credential hash, status | Per-credential revocation entries |

### OpenCred auto-creates four registries

Running [OpenCred](../../glossary.md#opencred) auto-manages four of these registries on first boot:

| Registry | Tag | OpenCred behaviour |
|---|---|---|
| `vc-revocation-registry` | `revocation` | Auto-created if missing; reused if it already exists |
| `opencred-key-registry` | `public_key` | Auto-created if missing; reused if it already exists |
| `schema_registry` | custom | Auto-created if missing; reused if it already exists |
| `context_registry` | custom | Auto-created if missing; reused if it already exists |

The startup hook calls `ensureRegistries()` on first boot (idempotent — restarts log "already published"), using env vars `OPENCRED_DEDI_BASE_URL`, `OPENCRED_DEDI_AUTH_TYPE` (`api-key`/`bearer`), `OPENCRED_DEDI_NAMESPACE`, plus matching credentials. See [OpenCred deployment docs](https://opencred.gitbook.io/docs/docker-image/deployment).

Caveat: pre-existing registries with **schemas OpenCred doesn't expect** (e.g. a differently-shaped `public_key` tag) make `/v1/keys/publish` fail validation — let OpenCred create them, or pre-create with its exact schemas; don't mix.

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

A self-hosted DDP node is possible (open-source protocol) but unused by any IES participant today.

### State, versioning, time-travel

DeDi tracks a record's full history:

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

A wallet hands a verifier a signed ElectricityCredential. The verifier:

1. **Parse** the credential JSON and read `issuer.id` (e.g. `did:web:ies.discom.example`).
2. **Resolve `issuer.id`** over HTTPS — fetch `https://ies.discom.example/.well-known/did.json` and extract the `verificationMethod` public key.
3. **Verify the credential's `proof`** signature against that key. If it fails, stop — the credential is forged or corrupted.
4. **(Optional) Check `issuer.idRef`** — resolve `issuer.idRef.issuedBy` (the regulator's `did:web`) and confirm the regulator vouches for this DISCOM under the cited `subjectId` (the licensing leg of the trust chain); skip if absent.
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
