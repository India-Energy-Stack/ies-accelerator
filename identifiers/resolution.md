# Resolution and Routing

A DID is only useful if a client can turn it into something actionable — a public key, an endpoint, a record. This page is the **request-time** companion to [Registries](./registries.md): for each kind of identifier IES uses, what does a client *do* with it?

---

## The resolver

Every IES SDK ships (or expects) a **resolver** with three methods:

```python
class IesResolver:
    def resolve_did(self, did: str) -> DidDocument: ...
    def resolve_record(self, did_dedi: str) -> dict: ...
    def resolve_endpoint(self, did: str, service_type: str) -> str: ...
```

| Method | Handles |
|---|---|
| `resolve_did` | `did:web`, `did:key`, `did:jwk` — returns a DID Document |
| `resolve_record` | `did:dedi:…` — returns the JSON record from DeDi |
| `resolve_endpoint` | Either form — returns a URL from `service[]` (or its DeDi-record equivalent) |

The resolver is the **only** place that knows how to talk to `api.dedi.global`, `*.well-known/did.json`, and any private DeDi mirrors. Everything above it consumes records, not URLs.

---

## Resolution by DID method

### `did:web`

```
did:web:ies.tpddl.in
   →  HTTPS GET https://ies.tpddl.in/.well-known/did.json
   →  parse as DID Document
```

#### Illustrative `did.json` Document for a Utility

When a resolver requests your utility's DID document, your web server must serve a valid JSON document exposing your public P-256 key (JWK) for signature validation. Here is a standard reference example:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/jws-2020/v1"
  ],
  "id": "did:web:ies.tpddl.co.in",
  "verificationMethod": [
    {
      "id": "did:web:ies.tpddl.co.in#key-1",
      "type": "JsonWebKey2020",
      "controller": "did:web:ies.tpddl.co.in",
      "publicKeyJwk": {
        "kty": "EC",
        "crv": "P-256",
        "x": "f83OJ3D2xF1Bg8vub9tLe1gHMzV76e8Tus9uPHvRVEU",
        "y": "x_FEzRu9m36HLN_tue659LNpXW6pCyStikYjKIWI5a0"
      }
    }
  ],
  "assertionMethod": ["did:web:ies.tpddl.co.in#key-1"],
  "authentication": ["did:web:ies.tpddl.co.in#key-1"]
}
```

Path-suffixed:

```
did:web:example.gov.in:agency:branch
   →  HTTPS GET https://example.gov.in/agency/branch/did.json
```

**Hardening rules (OpenCred enforces these — your resolver must too):**

- HTTPS only.
- No redirects.
- No resolution to private IPs (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, link-local, loopback).
- 10-second timeout.
- Reject if the served `id` field doesn't match the requested DID.

### `did:key` and `did:jwk`

No network call. Decode the multibase / JWK from the identifier and synthesise a DID Document with a single `verificationMethod`.

### `did:dedi:<ns>:<reg>:<id>`

Translate to a URL and GET:

```
did:dedi:tpddl:vc-revocation-registry:e5f6a7b8-...
   →  GET https://api.dedi.global/dedi/lookup/tpddl/vc-revocation-registry/e5f6a7b8-...
```

If you've configured a private resolver, the namespace map decides which host:

```
namespace → host
─────────────────────────────────────────
india-energy-stack    → api.dedi.global
tpddl                 → api.dedi.global
tpddl-private         → internal-dedi.tpddl.in   (with mTLS)
```

This means the **same identifier** resolves through the right host based on its namespace — calling code doesn't need to know whether a record is public or private.

---

## Workflow 1 — Verifying a credential

Given a signed credential JSON, the verifier walks this path:

```
1. Parse credential.
2. Read issuer.id and issuer.idRef.subjectId.
3. resolve_record(issuer.idRef.subjectId)
   → registry entry for the DISCOM
4. Assert: registry_entry.did == credential.issuer.id
5. publicKey = registry_entry.publicKeys[active]
6. Verify proof using publicKey
7. resolve_record(credentialStatus.id)
   → 404  → valid
   → 200  → revoked
8. Validate validFrom / validUntil
9. Validate schema (resolve schemaId)
```

Steps 3, 7, and 9 are DeDi lookups. Steps 5 and 6 use cryptography only — no network.

A verifier that caches the IES DISCOMs Reference Registry (say, refresh every 10 minutes) can complete verification entirely offline except for the revocation check.

---

## Workflow 2 — Issuing a credential

The issuer flow uses identifiers to *locate the holder* and *route the issued credential*. From `digilocker-integration.md`:

```
DigiLocker → POST /pullURIRequest → DISCOM webhook
   │
   ▼
UDF1 = consumer-number (e.g. TPDDL-2025-001234567)
UDF2 = mobile

Look up consumer in CIS.

Construct identifiers:
   issuerDid           = did:web:ies.tpddl.in
   issuerIdRef.subject = india-energy-stack:tpddl
   holderDid           = did:key:...                   (from request)
   customerReference   = did:dedi:tpddl:consumers:TPDDL-2025-001234567

POST to OpenCred /v1/credentials/issue
→ signed credential
→ inject issuer block (name, idRef)
→ return to DigiLocker
```

The DISCOM never has to look up the holder's wallet endpoint — the wallet pulls. But for **push-issuance** flows (e.g. directly to an agentic wallet), the holder DID can carry a `service` block in the DID Document; `resolve_endpoint(holderDid, "WalletInbox")` returns where to POST.

---

## Workflow 3 — Routing a Beckn message

A Beckn `search` for "TPDDL meter telemetry for January 2026" eventually resolves to a `DatasetItem` whose `id` is, say:

```
did:dedi:tpddl:datasets:meter-telemetry:2026-01
```

The Beckn BAP wants to fetch this dataset. Routing:

```
resolve_record(did:dedi:tpddl:datasets:meter-telemetry:2026-01)
  → record contains becknBPP = "did:web:ies.tpddl.in#beckn-bpp"
resolve_endpoint(did:web:ies.tpddl.in, "beckn-bpp")
  → https://ies.tpddl.in/beckn/bpp
POST /select to that URL with the DatasetItem in the message.
```

The BAP never hard-codes URLs. Every routing decision is a resolution.

---

## Workflow 4 — Cross-DISCOM consumer move

A consumer with `did:dedi:tpddl:consumers:TPDDL-2025-001234567` moves to BESCOM territory.

```
1. BESCOM CIS creates new consumer: BESCOM-2026-009876543
   New reference: did:dedi:bescom:consumers:BESCOM-2026-009876543

2. Consumer's wallet holds an old TPDDL credential.
   Holder DID (did:key:...) is unchanged.

3. BESCOM issues a new credential, credentialSubject.id = same did:key
   (consumer doesn't need a new wallet)

4. TPDDL marks old reference as closed in its DeDi consumer registry:
   PATCH did:dedi:tpddl:consumers:TPDDL-2025-001234567
     status → "closed"
     closedAt → 2026-05-12
   And revokes the old credential (publish hash to vc-revocation-registry).

5. Old credential continues to verify cryptographically forever, but
   credentialStatus check now returns "revoked".
```

Two DISCOMs, two reference IDs, one wallet, no national consumer registry. This is the architectural payoff of preserving internal numbering inside DIDs.

---

## Workflow 5 — Resolving an asset for an outage notification

Field ops at TPDDL declare a feeder outage:

```
event: feeder-outage
asset: did:dedi:tpddl:assets:feeder:FDR-11KV-NDL-072
window: 2026-05-12T14:00Z/2026-05-12T17:00Z
```

A consumer-facing app receives this event. To turn it into "your area is affected":

```
1. resolve_record(asset DID)
   → feeder record (geo, substation, served areas)
2. For each connection in the consumer's wallet:
   resolve_record(connection DID)
   → check if connection.feeder == asset DID
3. If match, notify.
```

No CIS round-trip. Asset and connection DIDs carry enough metadata to do the join client-side.

---

## Caching strategy

| Record type | TTL | Why |
|---|---|---|
| DISCOM reference entry | 10 min | Rare changes; verifiers need freshness for key rotations |
| Regulator reference entry | 10 min | Same |
| `did:web` DID Document | 10 min | Rare changes |
| Asset record | 1 hr | Geo and ratings are slow-changing |
| Consumer reference record | 5 min | Status changes (active/closed) drive revocation timing |
| Revocation entry | 0 (never cache "absent") | A negative cache hides a fresh revocation |
| Revocation entry — positive (found) | Forever | A revoked credential stays revoked |

The asymmetric revocation TTL is important: cache *known revocations* aggressively (they never un-revoke), but never cache "not revoked yet".

---

## Error handling

| Failure | What it means | What to do |
|---|---|---|
| `did:web` resolves but `id` field mismatches | Domain hijack or misconfig | Reject; do not fall back |
| `did:dedi` record 404 | Issuer not registered, or wrong subjectId | Reject as untrusted |
| `did:dedi` record `status: revoked` (for a DISCOM entry) | DISCOM's registration suspended by network operator | Reject all credentials from that DISCOM |
| Revocation lookup times out | DeDi unavailable | Surface as "verification incomplete" — do not silently accept |
| Asset record `decommissionedAt` is in the past | Decommissioned asset | Treat as invalid subject for new credentials; existing credentials remain valid up to validUntil |

A verifier MUST distinguish "cryptographically invalid" from "trust state unknown". Conflating them weakens the system.

---

## SDK shape

A minimal IES resolver SDK exposes:

```python
ies = IesClient(
    cache_ttl="default",
    private_namespaces={"tpddl-private": "https://internal-dedi.tpddl.in"},
)

# Resolve
disc = ies.resolve_record("did:dedi:india-energy-stack:ies-discoms-reference-registry:tpddl")

# Verify
result = ies.verify_credential(vc_json)
# result.ok, result.issuer, result.subject, result.revoked, result.errors

# Route
endpoint = ies.resolve_endpoint("did:web:ies.tpddl.in", "beckn-bpp")
```

This is the shape every IES integration should converge on. Implementation language is incidental; the contract is what matters.

Next: [Issuance Reference](./issuance-reference.md) — a worked, runnable example of minting all of these IDs.
