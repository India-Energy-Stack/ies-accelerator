# Registry Creation — Step by Step

This page is the hands-on walkthrough for standing up a registry on DeDi. By the end of it you will have:

1. A DeDi account.
2. A **verified namespace** anchored to a domain you control.
3. One or more **registries** (using a built-in schema tag or a custom JSON Schema).
4. **Records** published and resolvable via `https://api.dedi.global/dedi/lookup/...`.

Everything is reproducible via either the publish console UI or the HTTP API. Both flows are covered.

If you have not read [DeDi Primer](./dedi-primer.md), skim it first — the three-coordinate model and proof structure are assumed knowledge here.

---

## Step 0 — Decide what you are about to publish

Before you click anything, write down:

| Decision | Example |
|---|---|
| **Namespace name** | The short, stable name of your organisation. Lowercase, hyphens, no spaces. Example: `tpddl`, `bescom`, `india-energy-stack`. |
| **Domain to verify** | A DNS domain you control and want to bind to the namespace. Example: `tpddl.in`. |
| **Registries you need** | E.g. `vc-revocation-registry`, `assets`, `subscribers`. See [Required Registries](./required-registries.md) for the IES baseline set. |
| **Who controls the writing key** | An individual or a service account. The Bearer API token from this account is what authorises every write. Treat it like an HSM-grade secret. |

**Naming conventions used across IES** (and recommended for new participants):

- Namespace = `<discom-id>` (or `india-energy-stack` for the network operator).
- Registry name = kebab-case, function-first: `vc-revocation-registry`, `subscribers-prod`, `assets-transformers`.
- Record name = the **DISCOM's internal identifier verbatim** (consumer number, asset SAP code, credential UUID). This preserves your existing numbering — see [Identifiers and Addressing](../identifiers/README.md#appendix-c--identifying-assets-meters-connections-datasets).

---

## Step 1 — Create a DeDi account

1. Go to [`publish.dedi.global`](https://publish.dedi.global).
2. Register with a working email address. The account belongs to **one entity** — use a role mailbox (`registry-admin@tpddl.in`) rather than a personal one for institutional registries.
3. Verify the email via the link sent.
4. Complete MFA setup.
5. Under **Profile / Settings**, generate an **API key** (Bearer token). Copy and store it in your secret manager — it cannot be retrieved later.

All HTTP examples on this page assume the token is in an `Authorization: Bearer $DEDI_TOKEN` header.

---

## Step 2 — Create a namespace

You can create the namespace either via UI or API. The namespace is created first; verification is a separate step.

### UI

1. Dashboard → **Namespaces** → **Create Namespace**.
2. Provide a `name` (e.g. `tpddl`) and a one-line `description`.
3. Save. The namespace exists in `live` state immediately. It is **not yet verified** against a domain.

### API

```bash
curl -X POST https://api.dedi.global/dedi/create-namespace \
  -H "Authorization: Bearer $DEDI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "tpddl",
    "description": "Tata Power Delhi Distribution Limited — IES public namespace",
    "meta": {
      "operator": "TPDDL IT",
      "contact": "registry-admin@tpddl.in"
    }
  }'
```

Response:

```json
{
  "message": "Namespace created",
  "data": {
    "namespace_id": "01J6X..."
  }
}
```

Keep the `namespace_id` — some API calls accept either the human name or the id.

---

## Step 3 — Verify the namespace against a domain

Domain verification is what makes a namespace authoritative. After it passes, the namespace can be addressed by domain name (`/dedi/lookup/<domain>/...`) and proof responses include `is_verified: true`.

### How it works

1. In the UI, **Namespaces → tpddl → Verify domain**, submit the domain (e.g. `tpddl.in`).
2. DeDi issues a **DNS TXT record** to add to the domain. The record's name and value are displayed in the console; copy both.
3. Add the TXT record to your authoritative DNS. Wait for propagation (typically 1–5 minutes; can be longer on slow registrars).
4. Click **Verify**. DeDi performs the DNS lookup, confirms the value, and flips `is_verified` to `true`.

Requests are processed within ~5 minutes if there are no adverse signals. Manual review may be triggered for domains where DeDi cannot automatically corroborate ownership; in that case wait for a confirmation email.

### Why this matters

- The verified domain is what appears in user-facing URLs and certificates.
- IES verifier code (and ONIX) cross-checks that the domain in the namespace matches the issuer's `did:web` domain. An unverified namespace will not be accepted as a trust anchor by IES validators.
- The verification status is part of the namespace's signed digest — a relying party can confirm cryptographically that the domain binding existed when a record was anchored.

---

## Step 4 — Create a registry

A registry lives under a namespace and has a schema. You either pick a **built-in schema tag** or supply a custom JSON Schema.

### Built-in tags

| Tag | Purpose |
|---|---|
| `membership` | Lists of recognised entities (reference / allow-list) |
| `public_key` | Versioned signing keys |
| `revoke` | Credential revocation entries |
| `beckn_subscriber` | A Beckn BAP/BPP subscriber record |
| `beckn_subscriber_reference` | A pointer that brings an external registry/record into a Beckn network reference |

### UI

1. **Namespaces → tpddl → Create Registry**.
2. Provide `registry_name`, `description`, and pick a **template** (the tag) **or** paste a JSON Schema.
3. Save. The registry is now in `live` state.

### API — using a built-in tag

```bash
curl -X POST https://api.dedi.global/dedi/tpddl/create-registry \
  -H "Authorization: Bearer $DEDI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "registry_name": "vc-revocation-registry",
    "description": "Revocation status entries for credentials issued by TPDDL",
    "tag": "revoke"
  }'
```

### API — using a custom schema

```bash
curl -X POST https://api.dedi.global/dedi/tpddl/create-registry \
  -H "Authorization: Bearer $DEDI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "registry_name": "assets-transformers",
    "description": "Public metadata for TPDDL distribution transformers",
    "schema": {
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "type": "object",
      "required": ["asset_id", "rating_kva", "commissioned_at", "service_area"],
      "properties": {
        "asset_id":        { "type": "string" },
        "rating_kva":      { "type": "number" },
        "commissioned_at": { "type": "string", "format": "date" },
        "service_area":    { "type": "string" },
        "geo": {
          "type": "object",
          "properties": {
            "lat": { "type": "number" },
            "lon": { "type": "number" }
          }
        },
        "status": { "enum": ["active", "decommissioned"] }
      }
    },
    "meta": { "owner_team": "Asset Management" }
  }'
```

Response:

```json
{
  "message": "Registry created",
  "data": {
    "registry_id": "01J7..."
  }
}
```

---

## Step 5 — Add records

A record is one JSON document conforming to the registry's schema. It can be saved as a **draft** first, or published in one shot.

### Save and publish in one call

```bash
curl -X POST "https://api.dedi.global/dedi/tpddl/assets-transformers/save-record-as-draft?publish=true" \
  -H "Authorization: Bearer $DEDI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "record_name": "TX-DELHI-001234",
    "description": "11 kV distribution transformer, North Delhi",
    "details": {
      "asset_id": "TX-DELHI-001234",
      "rating_kva": 630,
      "commissioned_at": "2019-08-14",
      "service_area": "DL-North",
      "geo": { "lat": 28.7041, "lon": 77.1025 },
      "status": "active"
    },
    "valid_till": null
  }'
```

Response (published):

```json
{
  "message": "record created",
  "data": { "record_id": "01J7..." }
}
```

### Two-step: draft then batch-publish

```bash
# 1. Save a draft (omit publish=true)
curl -X POST "https://api.dedi.global/dedi/tpddl/assets-transformers/save-record-as-draft" \
  -H "Authorization: Bearer $DEDI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "record_name": "TX-DELHI-001235", "description": "...", "details": { ... } }'

# 2. Publish one or many drafts together
curl -X POST "https://api.dedi.global/dedi/tpddl/assets-transformers/publish-records" \
  -H "Authorization: Bearer $DEDI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "records": ["TX-DELHI-001235", "TX-DELHI-001236"] }'
```

Drafts let you stage a batch, get internal review, and then go live atomically.

### Bulk CSV upload

For tens of thousands of records, use the bulk endpoint.

```bash
curl -X POST https://api.dedi.global/dedi/bulk-upload \
  -H "Authorization: Bearer $DEDI_TOKEN" \
  -F "namespace=tpddl" \
  -F "registry_name=assets-transformers" \
  -F "record_name_field=asset_id" \
  -F "file=@./transformers.csv"
```

CSV format:

- UTF-8 encoding.
- First row is field names matching the registry schema.
- Nested objects use **dot notation**: `geo.lat`, `geo.lon`.
- Arrays use comma-separated values inside quotes: `"a,b,c"`.
- Dates in ISO 8601.
- Booleans as `true`/`false` or `1`/`0`.
- Maximum 100 MB per upload.

Example:

```csv
asset_id,rating_kva,commissioned_at,service_area,geo.lat,geo.lon,status
TX-DELHI-001234,630,2019-08-14,DL-North,28.7041,77.1025,active
TX-DELHI-001235,400,2020-02-03,DL-North,28.7102,77.1198,active
```

Response is a `jobId`; poll:

```bash
curl -H "Authorization: Bearer $DEDI_TOKEN" \
  https://api.dedi.global/dedi/bulk-upload/status/<jobId>
```

The status payload reports `totalEntries`, `validEntries`, `failedEntries`, and a `downloadFailedEntriesCsvUrl` so you can fix and retry only the rows that failed.

---

## Step 6 — Look up and verify

Every read is public; no Bearer token needed.

### Resolve a single record

```bash
curl https://api.dedi.global/dedi/lookup/tpddl/assets-transformers/TX-DELHI-001234
```

Response shape (abridged):

```json
{
  "message": "Resource retrieved successfully",
  "data": {
    "namespace": "tpddl",
    "namespace_id": "01J6X...",
    "registry_id": "01J7...",
    "registry_name": "assets-transformers",
    "registry_state": "live",
    "record_id": "01J7...",
    "record_name": "TX-DELHI-001234",
    "description": "11 kV distribution transformer, North Delhi",
    "digest": "0x...",
    "schema": { "...": "..." },
    "version_count": 1,
    "version": "1",
    "details": {
      "asset_id": "TX-DELHI-001234",
      "rating_kva": 630,
      "commissioned_at": "2019-08-14",
      "service_area": "DL-North",
      "geo": { "lat": 28.7041, "lon": 77.1025 },
      "status": "active"
    },
    "meta": {},
    "genesis": "0x...",
    "created_at": "2026-05-14T09:31:22Z",
    "updated_at": "2026-05-14T09:31:22Z",
    "created_by": "did:web:did.cord.network:76EU9...",
    "state": "live",
    "ttl": 600,
    "proof": {
      "type": "DediRecordProof2025",
      "namespace_did": "did:dedi:ns:tpddl",
      "registry_identifier": "registry:tpddl.assets-transformers",
      "record_identifier": "record:tpddl.assets-transformers.TX-DELHI-001234",
      "creator_did": "did:web:did.cord.network:76EU9...",
      "digest": "0x...",
      "network_genesis": "0x..."
    }
  }
}
```

### List records in a registry

```bash
# All live records
curl "https://api.dedi.global/dedi/query/tpddl/assets-transformers?state=live"

# Paginated, filtered, sorted
curl "https://api.dedi.global/dedi/query/tpddl/assets-transformers?state=live&name=TX-DELHI&sort=date&page=1&page_size=50"
```

Supported query parameters: `from`, `to` (date range, YYYY-MM-DD), `state` (`live`), `name` (min 3 chars, substring match), `sort` (`date|status|name|id`), `page`, `page_size`, `as_on`.

### List registries under a namespace

```bash
curl "https://api.dedi.global/dedi/query/tpddl?status=active&sort=name"
```

### Historical state — `as_on`

```bash
# Was this transformer's record different on 1 Jan 2025?
curl "https://api.dedi.global/dedi/lookup/tpddl/assets-transformers/TX-DELHI-001234?as_on=2025-01-01"
```

### Version pin

```bash
curl "https://api.dedi.global/dedi/lookup/tpddl/assets-transformers/TX-DELHI-001234?version_id=2"
```

### Export everything as CSV

```bash
curl -H "Authorization: Bearer $DEDI_TOKEN" \
  https://api.dedi.global/dedi/tpddl/assets-transformers/export-as-csv \
  -o transformers-snapshot.csv
```

---

## Step 7 — Day-2 operations

| Operation | How |
|---|---|
| **Update a record** | Save-as-draft (a new version) for an existing `record_name`, then `publish-records`. Old versions remain available via `?version_id=`. |
| **Mark a record invalid** | Set `valid_till` on update, or transition state. Verifier code checks `valid_till` < now. |
| **Revoke a credential** | If the registry has `tag: revoke`, add or update a record keyed by the credential ID. Verifier code dereferences `credentialStatus.id` to this registry. |
| **Rotate a signing key** | If the registry has `tag: public_key`, add a new key record (or new version) with `validFrom` set; keep the old one with `validUntil` so historical signatures still verify. |
| **Deactivate a registry** | Move state `live → inactive`. Records stay readable; new writes are blocked. Recoverable within the restore window (default 7 days). |
| **Restore a deleted entity** | Within the restore window, recover via the UI. After it expires, archival is permanent. |

---

## Authorisation model — what to remember

- **Reads** are public for live registries; no token required.
- **Writes** require a Bearer token from the namespace owner's account. There is no per-registry sharing — owning the namespace = owning every registry and record under it.
- **Domain ownership** (the DNS TXT) is what binds a namespace's authority to a real-world organisation. Treat the DNS records and the namespace API token as part of the same blast radius.
- If you must delegate write capability, do it inside your organisation (a service account with the token), not across organisations. For cross-organisation referencing, see [Required Registries — Network Reference](./required-registries.md#network-reference-registry).

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `401 unauthorized` on write | Bearer token missing, expired, or wrong account |
| `403 forbidden` on write | Token is valid but does not own the namespace |
| `400 validation error` | Record `details` does not match the registry schema. Check field names and types. |
| `404 not found` on lookup | Namespace / registry / record name mis-typed; or registry is `inactive`. |
| `subscriber not found` from a Beckn counterparty | Your subscriber record is not yet referenced into the network registry (see [Required Registries](./required-registries.md#network-reference-registry)). |
| DNS verification fails | TXT record not yet propagated, value mismatched, or your DNS has CNAME flattening that strips TXT. Re-check via `dig TXT <domain>`. |
| CSV bulk job has `failedEntries > 0` | Download the failed-rows CSV from `downloadFailedEntriesCsvUrl`, fix, re-upload only those rows. |

---

Next: [Required Registries](./required-registries.md) — the baseline set of registries an IES participant needs in place to be onboarded.
