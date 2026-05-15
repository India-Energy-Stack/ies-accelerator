# Registries — Public and Private

> **Looking for hands-on instructions?** This page is the conceptual overview of the public/private split. For a self-contained DeDi reference, see [DeDi Primer](./dedi-primer.md). For step-by-step setup, see [Registry Creation](./registry-creation.md). For the catalogue of registries you need to be onboarded, see [Required Registries for Onboarding](./required-registries.md).

A DID resolves to a record. **Registries are where records live.** This page covers:

1. The structure of a DeDi registry — namespaces, registries, records.
2. The **public IES registries** every participant uses.
3. How a DISCOM operates **its own public registries** (per-DISCOM revocation, asset, consumer registries on the public DeDi network).
4. How a DISCOM operates a **private registry** inside its own network — when to do it, what to put there, and how to keep it interoperable with the public side.

---

## DeDi registry model in 30 seconds

```
api.dedi.global
└── namespace                  ← owned by one DID; only that DID's key can write
    └── registry               ← a typed collection of records
        └── record-id          ← a specific record (the resolvable end-point)
            └── { record JSON }
```

Three coordinates: **namespace / registry / record-id**. The namespace is the unit of governance — whoever controls the namespace's DID key controls everything under it.

Verbs:

| Operation | Endpoint shape |
|---|---|
| Resolve a record | `GET /dedi/lookup/<namespace>/<registry>/<record-id>` |
| List records in a registry | `GET /dedi/query/<namespace>/<registry>?filter=...` |
| Create / update a record | Signed write by the namespace controller (out of scope for verifiers) |

---

## The public IES registries

These are network-level registries operated by the IES network operator. They live under the `india-energy-stack` namespace, whose namespace DID is:

```
did:web:did.cord.network:76EU9AJNL25X4LAxgb92rA8op4co7n892oeySAuEk9gAay2N28ctma
```

### IES DISCOMs Reference Registry

| Property | Value |
|---|---|
| Path | `india-energy-stack/ies-discoms-reference-registry/<discom-id>` |
| Written by | IES network operator |
| Read by | Every verifier of an electricity credential |

A record holds:

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

The registry is the trust anchor. A `did:web` not in this list cannot be trusted as a DISCOM, no matter how valid the signature is.

### IES Regulators Reference Registry

Same shape, different list. Path:

```
india-energy-stack/ies-regulators-reference-registry/<regulator-id>
```

Used when verifying credentials signed by a regulator (tariff orders, licences) and when validating Beckn messages that originate from a regulator role.

### IES Schemas Registry (forthcoming)

Versioned JSON Schemas for credentials and DDM `DatasetItem`s. Paths like `india-energy-stack/ies-schemas/electricity/v1`. Until this is live, schema IDs are URLs hosted by `nfh-trust-labs`.

---

## Per-DISCOM public registries

A DISCOM that joins the IES network gets (or requests) **its own DeDi namespace** — typically `<discom-id>`. Inside that namespace it can stand up registries the IES network expects, plus optional ones.

### Required: revocation registry

```
<discom>/vc-revocation-registry/<credential-id>
```

This is non-negotiable — every credential's `credentialStatus.id` points into this registry. The DISCOM publishes credential hashes here on revocation. Only the DISCOM's namespace key can write.

### Recommended: asset registry

```
<discom>/assets/<asset-class>/<internal-id>
```

Putting transformers, feeders, substations into a DeDi registry makes them addressable for:

- Beckn data exchange (telemetry tied to a transformer DID).
- Outage notifications (a `did:dedi:tpddl:assets:feeder:FDR-XYZ` is a stable handle for an outage event).
- Regulator queries (DERC fetches a feeder's commissioning record).

Treat this as **the source of truth for asset-level public metadata** — geo location, ratings, commissioning state. Operational details (loading, alarms) stay in internal systems.

### Optional: consumer reference registry

```
<discom>/consumers/<consumer-number>
```

**Do not put PII in a public registry.** A public consumer reference record should contain only:

- The DID.
- City + state (no street address).
- Tariff category.
- Connection status (active / closed).
- Hashes of issued credentials (so a verifier can confirm a presented credential was actually issued).

If the DISCOM is unwilling to publish even this, run the consumer registry on a **private DeDi mirror** (see below). The DID grammar stays the same; only the resolver host changes.

### Optional: dataset registry

```
<discom>/datasets/<class>/<id>
```

Used by Beckn search to discover what datasets the DISCOM offers.

---

## Private registries inside the DISCOM

For data that must not leave the DISCOM — consumer PII, billing detail, internal asset attributes — run a **private registry that mirrors the DeDi shape but is hosted inside your network**.

### What to host privately

| Data | Why private |
|---|---|
| Consumer name, address, phone, email | Personal data; DPDP compliance |
| Bill amounts, tariff calculations | Commercial sensitivity |
| Asset capex, vendor contracts | Procurement sensitivity |
| Internal SCADA / SCO endpoints | Operational security |

### Structure

Use the same three-coordinate model, just behind your private DNS:

```
https://internal-dedi.tpddl.in/dedi/lookup/tpddl-private/consumers-full/TPDDL-2025-001234567
```

The record at this URL is the **full** consumer record (name, address, all fields). The public DID `did:dedi:tpddl:consumers:TPDDL-2025-001234567` is the **same identifier**, but it resolves on the public network to the **redacted** record.

Two resolvers, same identifier grammar, different views.

### Implementation options

You do not need to run the DeDi codebase to have a "DeDi-shaped" private registry. Any HTTP server that:

1. Accepts `GET /lookup/<namespace>/<registry>/<record-id>` and returns JSON.
2. Accepts `GET /query/<namespace>/<registry>?filter=...` and returns a list.
3. Enforces authn (mTLS, API key, IAM token) for read access.

…can serve as a private mirror. Common backings: PostgreSQL behind a thin FastAPI, or your existing CIS database wrapped with a DeDi-shaped read API.

### Promotion: private → public

When a record should move from private to public (e.g. a new transformer is commissioned and you want it discoverable via Beckn), publication is a **redaction + write**:

```
private record  →  filter to public fields  →  write to public DeDi namespace
```

Because both registries share the record schema, this is a projection — not a translation.

### Linkage between private and public records

The public record holds a pointer to the private one, but **only resolvable inside the DISCOM**:

```json
{
  "id": "did:dedi:tpddl:consumers:TPDDL-2025-001234567",
  "publicFields": { "city": "Delhi", "tariff": "DS-1A", "status": "active" },
  "privateRef": "https://internal-dedi.tpddl.in/dedi/lookup/tpddl-private/consumers-full/TPDDL-2025-001234567"
}
```

A public verifier ignores `privateRef`. An internal client follows it.

---

## Governance and key management for namespaces

A DeDi namespace is controlled by **its namespace DID**. Whoever holds the private key for that DID can write to any registry under the namespace.

### Recommended posture

| Namespace | Controller | Key storage |
|---|---|---|
| `india-energy-stack` | IES network operator | HSM, multi-sig if available |
| `<discom>` (public) | DISCOM IT | Cloud KMS (AWS / Azure / GCP) |
| `<discom>-private` | DISCOM IT | On-prem HSM or cloud KMS in the DISCOM's tenant |

The signing key for **credentials** is separate from the signing key for **namespace writes**. Compromising the credential key forces credential revocation; compromising the namespace key forces re-issuance of every record under the namespace.

### Key rotation

For `did:web` — replace `.well-known/did.json` with a new `verificationMethod`. The old key is preserved in the DID Document with `validUntil`, so historical credentials still verify.

For the DeDi reference registry entry — the IES network operator updates the entry to add the new key alongside the old one. Verifiers always check against the registry's current list.

---

## Operational guidance

| Concern | What to do |
|---|---|
| **Latency** | Cache resolutions for 5–15 minutes at verifiers. DeDi records are write-rare. |
| **Availability** | Verifiers must tolerate transient DeDi unavailability — cache at minimum the IES DISCOMs registry locally. |
| **Audit** | DeDi records carry creation and update timestamps; keep an append-only audit log of namespace writes for your own compliance. |
| **PII** | Never publish PII to the public namespace. Use the private mirror. |
| **Backup** | Treat private-mirror data as part of your CIS backup scope. The public DeDi side is re-derivable from internal state. |

Next: [Resolution](./resolution.md) — the request-time workflows that consume these registries.
