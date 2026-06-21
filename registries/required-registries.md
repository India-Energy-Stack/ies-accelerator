# Required Registries for IES Onboarding

To plug a new participant — a DISCOM, a regulator, an AMISP, a third-party application — into the IES network, a specific set of registries needs to exist on DeDi. Some are operated by the IES network operator and you only need to **be referenced into** them. Others you operate yourself, under your own namespace, and IES (or counterparties) reads from them.

This page is the **complete catalogue** of those registries: what each one is for, who owns it, what its records look like, and the minimum subset you need to be onboarded for each use case (credentials, Beckn data exchange, etc.).

If you have not read [DeDi Primer](./dedi-primer.md) and [Registry Creation](./registry-creation.md), do those first.

---

## Map at a glance

```
india-energy-stack            (operated by IES network operator)
├── ies-discoms-reference-registry        ← who is a DISCOM
├── ies-regulators-reference-registry     ← who is a regulator
├── ies-schemas                           ← canonical schemas (forthcoming)
└── ies-data-sharing-network              ← Beckn prod network reference
    test-ies-data-sharing-network         ← Beckn test  network reference

indiaenergystack.in           (NFO namespace for Beckn, same operator)
├── ies-data-sharing-network              ← Beckn prod NPs
└── test-ies-data-sharing-network         ← Beckn test  NPs

<discom-id>                   (operated by you, the DISCOM)
├── vc-revocation-registry                ← credential revocation
├── public-keys                           ← issuer signing keys (versioned)
├── assets/...                            ← public asset metadata (optional)
├── datasets                              ← Beckn DatasetItem discovery
└── subscribers-test, subscribers-prod    ← your Beckn BAP/BPP subscriber records
```

| Registry | Operator | Purpose | Required for |
|---|---|---|---|
| [DISCOM reference registry](#discom-reference-registry) | IES | Curated allow-list of DISCOMs (inter-DISCOM data exchange network's trust boundary) | Joining the inter-DISCOM data exchange network (not credential issuance) |
| [Regulator reference registry](#regulator-reference-registry) | IES | Curated allow-list of regulators | Joining the inter-DISCOM data exchange network; optional sanity-check on `issuer.idRef.issuedBy` |
| [Schemas registry](#schemas-registry) | IES | Canonical credential / DDM schemas | Schema-validated flows (forthcoming) |
| [Network reference registry](#network-reference-registry) | IES | Beckn network membership | Beckn data exchange |
| [Subscriber registry](#beckn-subscriber-registry) | You (NP) | Your BAP/BPP identity + signing key | Beckn data exchange |
| [Public-keys registry](#public-keys-registry) | You (issuer) | Versioned issuer keys | Credential issuance |
| [Revocation registry](#revocation-registry) | You (issuer) | Per-credential revocation status | Credential issuance |
| [Asset registry](#asset-registry-optional) | You (DISCOM) | Public asset metadata | Beckn search of physical assets |
| [Dataset registry](#dataset-registry-optional) | You (DISCOM) | Beckn `DatasetItem` discovery | Beckn data discovery |

> **Credential trust does not require any IES-operated registry.** Verifiers trust an ElectricityCredential by resolving the issuer's `did:web` for the signing key and the regulator's `did:web` (cited in `issuer.idRef.issuedBy`) for the licensing assertion. The IES DISCOMs and Regulator reference registries above are Beckn-side / industry-coordination tools; they are the trust boundary for **data exchange over Beckn**, not for credential issuance.

---

## Onboarding-quick guide — minimum to get started

Pick the row that describes your situation. The **bold** registries are what you need to have in place; the rest can come later.

| You are… | Need referenced into | Need to operate yourself |
|---|---|---|
| **A DISCOM issuing electricity credentials** | (nothing IES-operated) — credential trust flows from your `did:web` + the regulator's `idRef`. IES schemas registry (when live) for schema validation. | **`vc-revocation-registry`**, **`public-keys`** |
| **A DISCOM joining the inter-DISCOM data exchange network** | **DISCOM reference** (network trust boundary), **Network reference** (test + prod) | **`subscribers-test`**, **`subscribers-prod`** (`beckn_subscriber` tag) |
| **A regulator publishing tariff orders** | Regulator reference, IES schemas | **`public-keys`**, **`vc-revocation-registry`** |
| **An AMISP / aggregator BAP** | Network reference | **`subscribers-test`**, **`subscribers-prod`** |
| **An application / verifier** | (nothing — read-only) | (nothing) |

The three sections below cover the IES-operated registries you get **referenced into**; the rest cover what you have to **operate yourself**.

---

## DISCOM reference registry

The IES network operator's curated list of recognised DISCOMs. It is the **trust boundary for the inter-DISCOM data exchange network** — the NFO references DISCOM records from here into the network's subscriber registry so other nodes treat the DISCOM as in-network. **Credential issuance does not require an entry here**: an ElectricityCredential is trusted via the issuer's `did:web` signature and the regulator's licensing assertion in `issuer.idRef`.

| Property | Value |
|---|---|
| Path | `india-energy-stack/ies-discoms-reference-registry/<discom-id>` |
| Tag | `membership` |
| Written by | IES network operator |
| Read by | NFO (to compose Beckn network registries); Beckn counterparties for trust-boundary checks |

### Record shape

```json
{
  "id": "tpddl",
  "did": "did:web:ies.tpddl.in",
  "legalName": "Tata Power Delhi Distribution Limited",
  "publicKeys": [{
    "id": "did:web:ies.tpddl.in#key-1",
    "type": "JsonWebKey2020",
    "publicKeyJwk": { "kty": "EC", "crv": "P-256", "x": "...", "y": "..." },
    "validFrom": "2025-01-01T00:00:00Z",
    "validUntil": null
  }],
  "x5c": ["MIID...", "MIIE..."],
  "serviceAreas": ["DL"],
  "endpoints": {
    "opencred": "https://ies.tpddl.in/v1/credentials",
    "becknBPP": "https://ies.tpddl.in/beckn/bpp"
  },
  "registeredAt": "2025-01-01T00:00:00Z",
  "status": "active"
}
```

### How to get added

You do not write to this registry. You **request inclusion** from the IES Secretariat:

| Channel | Address |
|---|---|
| Email (primary) | [IES.Secretariat@fsrglobal.org](mailto:IES.Secretariat@fsrglobal.org) |
| Email (alternate) | [ies@recindia.com](mailto:ies@recindia.com) |
| Web | [ies.fsrglobal.org](https://ies.fsrglobal.org/#footer) |

Send: your DISCOM short-code (`<discom-id>`), `did:web` domain, legal name, public key (JWK), x5c chain if you have a DSC, service area codes, and the URLs of your OpenCred / Beckn endpoints.

The Secretariat creates the record under the IES network operator's namespace.

---

## Regulator reference registry

Same shape, different list — recognised regulators (DERCs, KERCs, CERC, MERC, …).

| Property | Value |
|---|---|
| Path | `india-energy-stack/ies-regulators-reference-registry/<regulator-id>` |
| Tag | `membership` |
| Written by | IES network operator |
| Read by | Verifiers of regulator-signed credentials and Beckn messages |

Onboarding is the same as the DISCOM reference registry — contact the IES Secretariat.

---

## Schemas registry

**Forthcoming.** Path will be `india-energy-stack/ies-schemas/<domain>/<version>`, e.g. `india-energy-stack/ies-schemas/electricity/v1`. Until it is live, schema IDs are URLs hosted by `nfh-trust-labs`. New IES schemas will be published here so verifiers can resolve and pin to a versioned, anchored definition.

---

## Network reference registry

This is what makes a Beckn Network Participant (BAP or BPP) **part of an IES Beckn network**. The IES Network Facilitator Organisation (NFO) runs two networks under its DeDi namespace `indiaenergystack.in`:

| Network | `networkId` | Purpose |
|---|---|---|
| Test | `indiaenergystack.in/test-ies-data-sharing-network` | Pre-production exchange — onboarding, certification, ongoing staging traffic. |
| Production | `indiaenergystack.in/ies-data-sharing-network` | Live exchange between real DISCOMs, regulators, AMISPs. |

Each network is its own DeDi registry under the `indiaenergystack.in` namespace. Records in the network reference registry use the `beckn_subscriber_reference` tag and point at either:

- **A single subscriber record** you publish under your own namespace, or
- **A whole subscriber registry** of yours — which brings every present and future record in that registry into the network.

Membership in test does **not** imply membership in production. ONIX enforces this on every inbound message via `allowedNetworkIDs`.

### How to get referenced in

1. Stand up your own [Beckn subscriber registry](#beckn-subscriber-registry) under your namespace (see below).
2. Email the IES Secretariat (addresses above) with the **DeDi lookup URL** of either your individual subscriber record or your whole subscriber registry, and specify whether to include as **Registry** (registry-level reference) or **Record** (single record reference).
3. IES adds it to the network reference registry. Other participants' ONIX adapters can now resolve your signing key and validate your messages.
4. When you are ready to go production-live, repeat for the prod network. **It is conventional to keep separate test and prod subscriber registries** under your namespace; that way each is referenced into the correct network and there is no risk of test identities leaking into prod.

---

## Beckn subscriber registry

Operated by **you** (the Network Participant — your BAP or BPP). Holds the subscriber records that the IES Beckn network references.

| Property | Value |
|---|---|
| Path | `<your-namespace>/subscribers-{test,prod}/<subscriber-id>` |
| Tag | `beckn_subscriber` |
| Written by | You |
| Read by | Counterparties' ONIX (via the network reference registry) |

### Record shape

```json
{
  "subscriber_id": "np.example.com",
  "subscriber_url": "https://np.example.com/bap/beckn",
  "type": "BAP",
  "signing_public_key": "BASE64_ED25519_PUBLIC_KEY",
  "encr_public_key": "BASE64_OPTIONAL",
  "valid_from": "2026-05-01T00:00:00Z",
  "valid_until": null,
  "status": "active"
}
```

| Field | What to fill |
|---|---|
| `subscriber_id` | Your unique identifier — typically your domain (`np.example.com`) |
| `subscriber_url` | Your ONIX receiver endpoint (`https://np.example.com/bap/beckn`) |
| `type` | `BAP` or `BPP`. If you do both, publish two records. |
| `signing_public_key` | Base64-encoded Ed25519 public key (no PEM header/footer). Generate the keypair with the helper script in [beckn-onix](https://github.com/beckn/beckn-onix) — raw 32-byte seed + 32-byte public key, both Base64 RFC 4648 with padding. |

### Conventional layout

- One subscriber registry per environment: `subscribers-test` and `subscribers-prod`. Their records live in clearly separated registries, and each registry is referenced into the matching IES network.
- One ONIX deployment per environment, with `allowedNetworkIDs` set narrowly:
  - Test ONIX: `allowedNetworkIDs: "indiaenergystack.in/test-ies-data-sharing-network"`
  - Prod ONIX: `allowedNetworkIDs: "indiaenergystack.in/ies-data-sharing-network"`
- After you publish a subscriber record, **note the `recordId`** that DeDi assigns. It is your `keyId` in ONIX (`plugins.keyManager.config.keyId`).

The public key never leaves DeDi; the private key never leaves your ONIX deployment.

A fuller walkthrough of the Beckn-side onboarding (ONIX configuration, hosting, two-stack rollout) lives in [Data Exchange — Registry Setup](../data-exchange/registry-setup.md).

---

## Public-keys registry

Operated by **you** (the issuer). Holds your signing keys with explicit `validFrom` / `validUntil` so verifiers can confirm a credential was signed by a key that was valid at the time of issuance.

| Property | Value |
|---|---|
| Path | `<your-namespace>/public-keys/<key-id>` |
| Tag | `public_key` |
| Written by | You |
| Read by | Credential verifiers |

### Record shape

```json
{
  "id": "did:web:ies.tpddl.in#key-1",
  "type": "JsonWebKey2020",
  "controller": "did:web:ies.tpddl.in",
  "publicKeyJwk": {
    "kty": "EC", "crv": "P-256",
    "x": "f83OJ3D2xF1Bg8vub9tLe1gHMzV76e8Tus9uPHvRVEU",
    "y": "x_FEzRu9m36HLN_tue659LNpXW6pCyStikYjKIWI5a0"
  },
  "validFrom": "2025-01-01T00:00:00Z",
  "validUntil": null,
  "status": "active"
}
```

### Key rotation

Don't replace the record — **add a new record** for the new key with `validFrom: now`, and update the old record's `validUntil` to the cut-over instant. Credentials signed by the old key still verify against the historical state of the registry (use `?as_on=` on lookup).

---

## Revocation registry

Operated by **you** (the issuer). Non-negotiable for any participant issuing W3C Verifiable Credentials — every credential's `credentialStatus.id` points into this registry.

| Property | Value |
|---|---|
| Path | `<your-namespace>/vc-revocation-registry/<credential-id>` |
| Tag | `revoke` |
| Written by | You |
| Read by | Every credential verifier |

### Record shape

```json
{
  "credential_id": "urn:uuid:6b3e...-...-...",
  "credential_hash": "sha256:abcdef...",
  "revoked": false,
  "revoked_at": null,
  "reason": null
}
```

To revoke, update the record (new version) with `revoked: true`, `revoked_at: <ISO timestamp>`, and an optional `reason`. The verifier dereferences `credentialStatus.id`, fetches the record, and checks `revoked`.

Because the registry's `tag` is `revoke`, the built-in schema handles the standard fields; you can extend `meta` for issuer-specific annotations.

---

## Asset registry (optional)

Operated by **you** (the DISCOM). Public metadata for transformers, feeders, substations, meters — anything that needs an addressable, stable handle on the IES network.

| Property | Value |
|---|---|
| Path | `<your-namespace>/assets/<asset-class>/<internal-id>` (or one registry per class: `assets-transformers`, `assets-feeders`, …) |
| Tag | Custom schema (no built-in `asset` tag) |
| Written by | You |
| Read by | Beckn BAPs (data discovery), regulators, internal apps |

Use when you want:

- Beckn telemetry messages to reference a transformer by DID.
- Outage notifications to use a stable feeder DID.
- Regulators to query commissioning records by feeder ID.

**Keep operational details out.** Loading, alarms, SLD diagrams stay in internal systems. Only public metadata — geo, ratings, commissioning state — belongs here.

---

## Dataset registry (optional)

Operated by **you**. Used by Beckn `search` to discover what datasets you offer.

| Property | Value |
|---|---|
| Path | `<your-namespace>/datasets/<class>/<id>` |
| Tag | Custom schema |
| Written by | You |
| Read by | Beckn BAPs running data discovery |

A record describes a `DatasetItem` — its schema, its provider DID, its sampling cadence, who can subscribe.

---

## Private registries (PII, billing, internal asset attributes)

For data that must not leave the DISCOM — consumer PII, bill amounts, internal SCADA endpoints — **do not publish to public DeDi**. Either:

1. Run a **DeDi-shaped private registry** behind your own DNS (any HTTP server that accepts `GET /lookup/<ns>/<reg>/<rec>` and returns JSON, with mTLS/IAM auth on reads), or
2. Stand up a **self-hosted DDP node** (Option C in [DeDi Primer](./dedi-primer.md#deployment-options)) under your control.

The public DID `did:dedi:<discom>:consumers:CN-...` is the **same identifier** in both worlds; it resolves on the public network to a **redacted** record (city, tariff category, status) and on the private resolver to the **full** record (name, address, all fields).

The public record may carry a `privateRef` pointing at the private resolver:

```json
{
  "id": "did:dedi:tpddl:consumers:TPDDL-2025-001234567",
  "publicFields": { "city": "Delhi", "tariff": "DS-1A", "status": "active" },
  "privateRef": "https://internal-dedi.tpddl.in/dedi/lookup/tpddl-private/consumers-full/TPDDL-2025-001234567"
}
```

External verifiers ignore `privateRef`; internal clients follow it (for details on the runtime resolver lookup mechanics, see [Unification of Public vs. Private Resolution Details](./resolution.md#unification-of-public-vs-private-resolution-details)).

---

## Governance and key custody

A DeDi namespace is controlled by **its namespace DID** (i.e. the account/keys at `publish.dedi.global` that own it). Whoever holds those credentials can write to any registry under the namespace.

| Namespace | Controller | Key storage |
|---|---|---|
| `india-energy-stack` / `indiaenergystack.in` | IES network operator (NFO) | HSM, multi-sig where available |
| `<discom-id>` (public) | DISCOM IT | Cloud KMS (AWS / Azure / GCP) |
| `<discom-id>-private` | DISCOM IT | On-prem HSM or KMS in the DISCOM's tenant |

**The signing key for credentials is separate from the namespace API token.** Compromise of the credential-signing key forces revocation; compromise of the namespace token forces rebuild of every record under the namespace. Treat both as HSM-grade secrets.

---

## End-to-end onboarding checklist

For a DISCOM that wants to be fully onboarded for credentials + the inter-DISCOM data exchange network. Steps 6–8 are needed **only for joining the inter-DISCOM data exchange network**; a DISCOM that is only issuing credentials can stop after Step 4 plus the regulator-issued licensing pointer for `issuer.idRef`.

1. [ ] DeDi account created (role mailbox, MFA, API token in your secret manager). → [Registry Creation §1](./registry-creation.md#step-1--create-a-dedi-account)
2. [ ] Namespace `<discom-id>` created and **domain-verified** against `<discom>.in`. → [§2](./registry-creation.md#step-2--create-a-namespace), [§3](./registry-creation.md#step-3--verify-the-namespace-against-a-domain)
3. [ ] `vc-revocation-registry` registry created (tag `revoke`). → [Revocation registry](#revocation-registry)
4. [ ] `public-keys` registry created (tag `public_key`), with at least one active key record. → [Public-keys registry](#public-keys-registry)
5. [ ] (Beckn) `subscribers-test` registry created (tag `beckn_subscriber`), with one BAP and/or BPP record per ONIX deployment. → [Beckn subscriber registry](#beckn-subscriber-registry)
6. [ ] (Beckn) Email IES Secretariat with: DISCOM short-code, `did:web` domain, public key, x5c, service areas, endpoints. → [DISCOM reference registry](#discom-reference-registry)
7. [ ] (Beckn) Email IES Secretariat with: DeDi URL of `subscribers-test` registry (or a single record), specifying Registry vs Record. → [Network reference registry](#network-reference-registry)
8. [ ] (Beckn) Confirm both references appear: lookup `india-energy-stack/ies-discoms-reference-registry/<discom-id>` and the relevant network registry.
9. [ ] Run end-to-end test transactions over the test network.
10. [ ] Repeat steps 5–8 against `subscribers-prod` and the prod network when ready to go live.

That sequence is the minimum to be a fully participating, credentialled, Beckn-reachable IES participant.

---

Next: [Resolution and Routing](./resolution.md) — once these registries are in place, how requests are resolved against them.
