# India Energy Stack
## IES Electricity Credentials — Implementation Checklist
### Detailed Technical Reference for DISCOM Integration Teams

**Name of DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Technical Lead:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Sub-profiles being populated (single `CustomerCredential` per meter):**
&nbsp; ☐ `customerProfile` (always) &nbsp; ☐ `customerDetails` &nbsp; ☐ `consumptionProfiles[]`
&nbsp; ☐ `generationProfiles[]` &nbsp; ☐ `storageProfiles[]`

---

## Phase 0 — Pre-requisites

- [ ] **0.a** Docker Engine (v24+) and Docker Compose installed (or Docker Desktop on Windows / macOS for dev evaluation). The OpenCred image is multi-arch (linux/amd64 + linux/arm64) since v1.2.0 — no `--platform` flag needed on Apple Silicon.
- [ ] **0.b** `openssl`, `curl`, and `jq` available in the terminal
- [ ] **0.c** OpenCred Desktop Client installed on the operator workstation ([opencred.gitbook.io/docs/desktop-app/installation](https://opencred.gitbook.io/docs/desktop-app/installation))
- [ ] **0.d** Access to CIS / billing database for consumer data lookups
- [ ] **0.e** Access to MDMS / AMISP system for meter type and connection data
- [ ] **0.f** **DeDi namespace credentials** in hand (base URL, auth type, API key or bearer pair, namespace ID) — part of the default OpenCred + DeDi combo from day one

---

## Phase 1 — OpenCred Infrastructure

### 1.1 Deploy OpenCred Docker Service

- [ ] **1.1.a** Generate a secure API key:
  ```bash
  openssl rand -base64 32   # → store as OPENCRED_API_KEY in secrets manager
  ```
- [ ] **1.1.b** Start OpenCred container with security hardening **and DeDi env vars** in the same `docker run`:
  ```bash
  docker run -d --name opencred -p 3100:3100 \
    -e OPENCRED_PORT=3100 \
    -e OPENCRED_API_KEY=$OPENCRED_API_KEY \
    -e OPENCRED_KEY_PATH=/secrets/issuer-key.pem \
    -e OPENCRED_DEDI_BASE_URL=$OPENCRED_DEDI_BASE_URL \
    -e OPENCRED_DEDI_AUTH_TYPE=$OPENCRED_DEDI_AUTH_TYPE \
    -e OPENCRED_DEDI_API_KEY=$OPENCRED_DEDI_API_KEY \
    -e OPENCRED_DEDI_NAMESPACE=$OPENCRED_DEDI_NAMESPACE \
    -v /path/to/issuer-key.pem:/secrets/issuer-key.pem:ro \
    --read-only \
    --tmpfs /tmp:noexec,nosuid,size=64m \
    --cap-drop ALL \
    --security-opt no-new-privileges:true \
    ghcr.io/nfh-trust-labs/opencred/opencred-server:latest
  ```
  > The public image lives on GitHub Container Registry; no auth is needed for `pull`. There is no `opencred:latest` on Docker Hub. For bearer DeDi auth, replace `OPENCRED_DEDI_API_KEY` with `OPENCRED_DEDI_EMAIL` + `OPENCRED_DEDI_PASSWORD`.
- [ ] **1.1.c** Health check passes — signing key loaded **and** DeDi configured:
  ```bash
  curl -s http://localhost:3100/v1/health | jq
  # Expected: { "status": "ok", "ready": true, "signingKeyLoaded": true, "dediConfigured": true }
  ```
  > If you intentionally skip DeDi (no creds yet), `dediConfigured: false` is acceptable — but `/v1/credentials/revoke`, `/revocation-status`, `/keys/publish`, `/keys/resolve` will all return `503 DEDI_NOT_CONFIGURED`.
- [ ] **1.1.d** Image pinned to a SHA digest in production (not `latest`)
- [ ] **1.1.e** TLS terminated upstream (nginx / Caddy / cloud load balancer) — OpenCred itself serves HTTP only

### 1.2 Signing Key Setup

Choose one based on your organisation's posture. Refer to [trust chains docs](https://opencred.gitbook.io/docs/concepts/trust-chains).

**Option A — `did:key` from a self-generated software PEM (recommended for dev / first deploy)**
- [ ] Generate an ECDSA P-256 key: `openssl ecparam -name prime256v1 -genkey -noout -out issuer-key.pem`
- [ ] Mount at `OPENCRED_KEY_PATH`; OpenCred derives a stable `did:key` automatically
- [ ] Read the DID via `GET /v1/keys` — the same PEM always yields the same DID
- [ ] Trust model: verifier extracts the public key directly from the DID string — no external lookup

**Option B — `did:web` from a self-generated key (recommended for production)**
- [ ] Generate the key as in Option A
- [ ] Download or compose the DID document
- [ ] Upload to `https://{domain}/.well-known/did.json`
- [ ] Confirm resolution:
  ```bash
  curl https://{domain}/.well-known/did.json
  # Expected: DID document with publicKeyMultibase or publicKeyJwk
  ```
- [ ] Issuer DID noted: `did:web:{domain}` → \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] Trust chain: VC → published public key → DID document → domain TLS certificate

**Option C — Import existing CCA-issued DSC**
- [ ] Import via OpenCred Desktop → Settings → Import File
- [ ] Supported formats: PFX, PEM, JWK, PKCS#8 DER
- [ ] OpenCred derives `did:key` from the certificate's public key automatically
- [ ] Trust chain: VC → DSC public key → CSCA root (verifiers trust the root)

**Option D — Hardware token (PKCS#11)**
- [ ] OpenCred Desktop → Settings → Hardware Token
- [ ] Select PKCS#11 library path, slot index, and enter PIN
- [ ] PIN is never persisted — entered each session

**Key Storage Verification (all options)**
- [ ] Private key material never stored in config, logs, or error responses (enforced by OpenCred invariant)
- [ ] Config file at `~/.config/opencred/opencred-config.json` stores only metadata and key path — not key material
- [ ] Host key file permissions set to `0600` (Linux/macOS) or restricted via `icacls` (Windows):
  ```bash
  chmod 0600 /path/to/issuer-key.pem
  # Windows PowerShell:
  # icacls issuer-key.pem /inheritance:r /grant:r "$($env:USERNAME):(R)"
  ```

### 1.3 DeDi Namespace Setup

- [ ] **1.3.a** DeDi namespace credentials received from your DeDi operator (base URL, auth type, API key or bearer pair, namespace ID)
- [ ] **1.3.b** Namespace name / ID noted (e.g. `tpddl`, `bescom`, or `did:web:did.cord.network:xyz`): \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **1.3.c** DeDi write credentials stored in secrets manager (never committed to git, mounted via Docker secrets / SSM / Key Vault in production)
- [ ] **1.3.d** `OPENCRED_DEDI_*` env vars passed into the container in Phase 1.1.b — `/v1/health` reports `dediConfigured: true`
- [ ] **1.3.e** First-boot registries ensured. OpenCred calls `ensureRegistries()` automatically on startup. To re-run mid-session (e.g. when adding a second namespace):
  ```bash
  curl -X POST http://localhost:3100/v1/dedi/namespace/ensure \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"namespace": "tpddl"}'
  # → {"namespace":"tpddl","registries":["vc-revocation-registry","public_key_registry","schema_registry","context_registry"]}
  ```
- [ ] **1.3.f** DeDi namespace URL appears in `credentialStatus` of all issued VCs:
  ```json
  {
    "credentialStatus": {
      "id": "https://<your-dedi>/dedi/lookup/{namespace}/vc-revocation-registry/<credential-id>",
      "type": "dedi",
      "statusPurpose": "revocation",
      "statusListCredential": "https://<your-dedi>/dedi/query/{namespace}/vc-revocation-registry"
    }
  }
  ```

### 1.4 (Optional) DID-document discovery via DeDi

For DISCOMs using `did:web` who'd rather not host `.well-known/did.json` themselves — or want DeDi as a fallback for transient `.well-known` outages — publish the DID document to DeDi:

- [ ] **1.4.a** Either set `OPENCRED_DEDI_HOST_DID_DOC=true` on the container (auto-publishes at boot), or call `POST /v1/keys/publish` manually with your DID + DID Core document. Returns `{published: true, recordName, namespace}`.
- [ ] **1.4.b** Confirm with `POST /v1/keys/resolve` — the response carries `document`, `keyStatus: "current"`, and (when the DeDi instance anchors) a `DediRecordProof2026` block.
- [ ] **1.4.c** Verifier partners who rely on the DeDi fallback are running OpenCred (or any verifier that wires `createDeDiDIDWebFallback` into its DID resolver) — pure off-the-shelf `did:web` resolvers without DeDi awareness will still need the canonical HTTPS endpoint.

> Note on `/v1/keys/resolve`: requires DeDi to be configured, even for `did:key`. If you skipped DeDi setup, this endpoint returns `503 DEDI_NOT_CONFIGURED` — it does not block issuance or verification, only the standalone resolve endpoint. With DeDi wired in, the response also carries `keyStatus` and (when CORD-anchored) a `proof` block (see [Concepts → keyStatus rotation](../energy-credentials/concepts.md#keystatus-rotation-flag-and-the-cord-anchor-proof)).

---

## Phase 2 — Credential Schema

### 2.1 Use the built-in `electricity/v1` schema

The OpenCred image ships `electricity/v1` as a built-in `schemaId`. It implements the IES `ElectricityCredential` v1.0 family — a single per-meter credential (`type: "CustomerCredential"`) with five sub-profiles. Canonical schema files: [`/schemas/ElectricityCredential/v1.0/`](../schemas/ElectricityCredential/v1.0/README.md) in this repo (root: [`India-Energy-Stack/ies-accelerator`](https://github.com/India-Energy-Stack/ies-accelerator)).

- [ ] **2.1.a** Confirm `electricity/v1` appears in `GET /v1/schemas`
- [ ] **2.1.b** `credentialSubject` shape understood:

  ```json
  {
    "credentialSubject": {
      "id": "<consumer DID, optional>",
      "customerProfile":      { "customerNumber": "...", "meterNumber": "...", "meterType": "AMI", "idRef": {...} },
      "customerDetails":      { "fullName": "...", "installationAddress": { /* beckn Location */ }, "serviceConnectionDate": "..." },
      "consumptionProfiles":  [{ "premisesType": "Residential", "connectionType": "Single-phase", "sanctionedLoadKW": 5, "tariffCategoryCode": "..." }],
      "generationProfiles":   [{ "generationType": "Solar", "capacityKW": 4.5, "commissioningDate": "...", "manufacturer": "...", "modelNumber": "..." }],
      "storageProfiles":      [{ "storageCapacityKWh": 13.5, "powerRatingKW": 5, "commissioningDate": "...", "storageType": "LithiumIon" }]
    }
  }
  ```

  > Only `customerProfile` is required. The other four sub-profiles are optional. `consumptionProfiles`, `generationProfiles`, and `storageProfiles` are **arrays** with `minItems: 1` when present — multiple assets of the same kind go in as separate array entries.

- [ ] **2.1.c** `customerProfile.meterType` is required and must be one of: `AMR | AMI | Electromechanical | Forward | Reverse | Bidirectional | Prepaid | NetMeter | Other` (Green Button / ESPI meter-kind values)
- [ ] **2.1.d** `installationAddress` shape matches the beckn Location schema — `country` is required and uses `{name, code}` (ISO 3166-1 alpha-2); `area_code` and `address` are required strings; `city` / `state` are `{name, code}` objects when present
- [ ] **2.1.e** All date-time fields use ISO 8601 with an explicit timezone offset (e.g. `2019-03-15T00:00:00+05:30`)

### 2.2 Issuer object enrichment

The schema requires `issuer.id` and `issuer.name`; `issuer.idRef` is **optional**. OpenCred only accepts the DID string as `issuerDid` — your integration service must replace the returned `issuer` field with the full object before delivery. If you have a regulator to cite, set `idRef` to the **regulator's licensing assertion**: `issuedBy` is the regulator's `did:web`, `subjectId` is the regulator-issued licence identifier for your DISCOM. Omit `idRef` for pilots or non-regulated issuers. No IES-side DISCOM registry entry is required for credential issuance either way.

- [ ] **2.2.a** *(Optional)* Regulator's licensing pointer obtained, if you cite a regulator (regulator's `did:web` and the regulator-issued licence ID for your DISCOM). The IES-operated DISCOMs Reference Registry is **not** a prerequisite for credentials; it is a Beckn-side trust-boundary list — see [Identifiers and Addressing → Appendix E](../identifiers/README.md#appendix-e--joining-a-beckn-network-subscriber-registry-on-the-beckn-fabric).
- [ ] **2.2.b** `issuer.name` configured — legal name of the utility
- [ ] **2.2.c** *(If citing a regulator)* `issuer.idRef.issuedBy` set to the regulator's `did:web` (e.g. `did:web:derc.delhi.gov.in`)
- [ ] **2.2.d** *(If citing a regulator)* `issuer.idRef.subjectId` set to `<regulator-domain>:<discom-licence-id>` (e.g. `derc.delhi.gov.in:TPDDL-REG-0042`)
- [ ] **2.2.e** Post-process step in integration service rewrites the `issuer` field after each `POST /v1/credentials/issue`. Note: this invalidates the original `proof` — either re-sign in your service, or send the patched fields back through OpenCred for re-signing.

### 2.3 Customer external ID

The customer's external government ID (Aadhaar, etc.) is carried via `customerProfile.idRef`, never as the raw number.

- [ ] **2.3.a** External authority DID identified (e.g. `did:web:uidai.gov.in` for Aadhaar)
- [ ] **2.3.b** `subjectId` format uses **masked** identifier: `uidai.gov.in:XXXX-XXXX-1234`
- [ ] **2.3.c** Confirmed: full Aadhaar / ID number is never in any credential payload

### 2.4 Proof format

- [ ] **2.4.a** Proof format chosen: ☐ `vc-jwt` (recommended) &nbsp; ☐ `data-integrity` &nbsp; ☐ `sd-jwt-vc` (selective disclosure)

  > **Why `vc-jwt` is recommended:** the bundled `electricity/v1` JSON-LD context currently collides with the W3C VC v2 protected terms when `additionalTypes` is passed together with `proofFormat: "data-integrity"`, returning `CRYPTO_ERROR: Invalid JSON-LD syntax; tried to redefine a protected term`. `data-integrity` works against schemas you register yourself with a clean context.

- [ ] **2.4.b** Validity period defined: `validFrom` ≤ now ≤ `validUntil`, both with timezone offsets

---

## Phase 3 — Credential Issuance

### 3.1 Single Credential Issuance (API)

Validated working call against `ghcr.io/nfh-trust-labs/opencred/opencred-server:latest`:

```bash
curl -X POST http://localhost:3100/v1/credentials/issue \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "issuerDid": "did:web:ies.tpddl.in",
    "schemaId":  "electricity/v1",
    "additionalTypes": ["CustomerCredential"],
    "proofFormat": "vc-jwt",
    "validFrom":  "2026-05-01T00:00:00+05:30",
    "validUntil": "2031-05-01T00:00:00+05:30",
    "subjectDid": "did:key:z6MkjVQ...",
    "credentialSubject": {
      "id": "did:key:z6MkjVQ...",
      "customerProfile": {
        "customerNumber": "TPDDL-2025-001234567",
        "meterNumber":    "MTR-98765432",
        "meterType":      "AMI"
      },
      "customerDetails": {
        "fullName": "Priya Sharma",
        "installationAddress": {
          "address":   "Flat 4B, Sector 12, Rohini",
          "city":      {"name": "New Delhi", "code": "DEL"},
          "state":     {"name": "Delhi",     "code": "DL"},
          "country":   {"name": "India",     "code": "IN"},
          "area_code": "110085"
        },
        "serviceConnectionDate": "2019-03-15T00:00:00+05:30"
      },
      "consumptionProfiles": [{
        "premisesType":       "Residential",
        "connectionType":     "Single-phase",
        "sanctionedLoadKW":   5,
        "tariffCategoryCode": "DOM-A2"
      }]
    },
    "revocationRegistryUrl": "https://dedi.global/dedi/query/tpddl/vc-revocation-registry"
  }'
```

- [ ] **3.1.a** Issuance returns `HTTP 200` and a signed VC with `type: ["VerifiableCredential", "CustomerCredential"]`
- [ ] **3.1.b** Re-issue with a `generationProfiles[]` entry (new DER asset) tested
- [ ] **3.1.c** Re-issue with a `storageProfiles[]` entry (new battery) tested
- [ ] **3.1.d** Re-issue with updated `consumptionProfiles[]` (tariff change) tested
- [ ] **3.1.e** Re-issue with multiple sub-profiles populated tested

For each issued credential, confirm:
- [ ] `proof` block present. For `vc-jwt` the proof is `{ "type": "JsonWebSignature2020", "jwt": "<compact-JWS>" }`. For `data-integrity` look for `verificationMethod` pointing to your issuer DID.
- [ ] `credentialStatus` block present (only when `revocationRegistryUrl` was passed). All four fields populated: `id`, `type: "dedi"`, `statusPurpose: "revocation"`, `statusListCredential`.
- [ ] `validFrom` and `validUntil` set correctly with timezone offsets
- [ ] `customerProfile.idRef.subjectId` is masked — full Aadhaar / ID never in payload
- [ ] Integration service injects the full `issuer` object (with `name` and `idRef`) before delivery

### 3.2 Single Issuance via CLI

For scripted / offline issuance using the OpenCred CLI:

```bash
# Build the CLI first
cd apps/server && pnpm build

# Issue a credential
node dist/cli.js issue \
  --schema electricity/v1 \
  --input customer-subject.json \
  --key /path/to/issuer-key.pem \
  --proof-format vc-jwt \
  --output customer-credential.json
```

- [ ] **3.2.a** CLI issuance tested — output file is a valid W3C VC JSON matching the API output

### 3.3 Single Issuance via Desktop Client

For ad-hoc issuance by non-technical staff:

- [ ] **3.3.a** `electricity/v1` schema visible on OpenCred Desktop Home screen
- [ ] **3.3.b** Staff trained on: selecting `electricity/v1` → filling sub-profile fields → choosing signing key → Build & Sign → export
- [ ] **3.3.c** Export formats tested: JSON (for API consumers), PDF (for printing/emailing), QR code (for scanning)

### 3.4 Batch Issuance

For issuing credentials to a large number of consumers at once:

```bash
curl -X POST http://localhost:3100/v1/credentials/batch \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "csvContent": "<base64-encoded-CSV>",
    "schemaId":  "electricity/v1",
    "issuerDid": "did:web:ies.{discom}.in",
    "additionalTypes": ["CustomerCredential"],
    "proofFormat": "vc-jwt",
    "validFrom": "2026-04-01T00:00:00+05:30"
  }'
# Response: { "jobId": "...", "validCount": N, "invalidCount": M }

curl http://localhost:3100/v1/credentials/batch/{jobId} \
  -H "Authorization: Bearer $OPENCRED_API_KEY"

curl http://localhost:3100/v1/credentials/batch/{jobId}/results \
  -H "Authorization: Bearer $OPENCRED_API_KEY"
```

- [ ] **3.4.a** CSV prepared with one row per consumer — flat columns map into the nested `customerProfile` / `customerDetails` / `consumptionProfiles[0]` shape via the configured column mapping
- [ ] **3.4.b** Column mapping verified
- [ ] **3.4.c** Job polling implemented — application waits for `running: false` before downloading results
- [ ] **3.4.d** Results ZIP downloaded and individual VC JSON files validated
- [ ] **3.4.e** Batch size limit noted: default 1,000 rows; increase via `OPENCRED_BATCH_ROW_LIMIT` if needed
- [ ] **3.4.f** CSV delimiter confirmed (auto-detected: comma, semicolon, or tab)

### 3.5 Packaging and Delivery

- [ ] **3.5.a** `POST /v1/credentials/package` used to render delivery formats:
  ```bash
  curl -X POST http://localhost:3100/v1/credentials/package \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -d '{ "credential": { ... }, "format": "pdf" }'
  ```
- [ ] **3.5.b** PDF output reviewed — DISCOM branding (logo, primary colour) configured via `--logo` and `--primary-color` options
- [ ] **3.5.c** QR code output tested — QR encodes the full VC and is scannable by a verifier app

---

## Phase 4 — Credential Verification

### 4.1 API Verification

```bash
# vc-jwt credential — pass the compact JWT string from proof.jwt:
curl -X POST http://localhost:3100/v1/credentials/verify \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "credential": "eyJhbGciOi...<jwt-from-proof.jwt>...sig" }'

# data-integrity credential — pass the JSON-stringified VC object:
curl -X POST http://localhost:3100/v1/credentials/verify \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "credential": "<JSON-stringified VC>" }'
```

> The `credential` field is **always a string**. For `vc-jwt`, extract `proof.jwt` from your stored credential and send only that string — sending the credential object returns `INVALID` (the verifier expects to parse a JWT).

Expected response (vc-jwt):
```json
{
  "valid": true,
  "code": "VALID",
  "message": "Credential is valid.",
  "checks": [
    { "name": "signature",      "passed": true },
    { "name": "vc-jwt-claims",  "passed": true },
    { "name": "date",           "passed": true }
  ]
}
```

Expected response (data-integrity): the `checks` array names differ — typically `signature`, `notBefore`, `expiry`, `keyResolution`. Treat `valid: true` and `code: "VALID"` as the contract; do not pattern-match on specific check names.

- [ ] **4.1.a** Verification of a freshly issued credential returns `valid: true`
- [ ] **4.1.b** Expired credential test — `validUntil` in the past → `code: "EXPIRED"`
- [ ] **4.1.c** Tampered credential test — modify any `credentialSubject` field → `code: "INVALID"` (signature fails)
- [ ] **4.1.d** Unresolvable DID test — delete or corrupt DID document → `code: "UNRESOLVABLE"`
- [ ] **4.1.e** All result codes handled in application: `VALID`, `INVALID`, `REVOKED`, `EXPIRED`, `UNRESOLVABLE`

### 4.2 Desktop Client Verification

- [ ] **4.2.a** OpenCred Desktop → Verify page — paste VC JSON → Verify → all checks shown as passed
- [ ] **4.2.b** Offline verification confirmed for `did:key` credentials (no network, JSON-LD contexts are bundled)
- [ ] **4.2.c** `did:web` credential verification confirmed — requires network to fetch DID document from `/.well-known/did.json`

### 4.3 CLI Verification

```bash
node dist/cli.js verify --input customer-credential.json
# Exit code 0 = valid, exit code 1 = invalid
```

- [ ] **4.3.a** CLI verification tested — exit code 0 for valid credential, exit code 1 for tampered

---

## Phase 5 — Revocation

Revocation uses DeDi hash-lookup. The registry stores only revoked hashes. A credential is valid if its hash is **absent** from the registry; revoked if **present**.

### 5.1 Hash Computation

- [ ] **5.1.a** Revocation hash computed for a test credential:
  ```bash
  curl -X POST http://localhost:3100/v1/credentials/revocation-hash \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{ "credential": { /* full signed VC, INCLUDING the proof block */ } }'
  # Returns: { "hash": "sha256hex..." }
  ```
  > Pass the credential **as you stored it** (signed, with `proof`). `/v1/credentials/revoke` recomputes the hash from the same shape — stripping `proof` here would produce a hash that does not match the one revocation publishes. See `energy-credentials/issuance.md` § "Hash stability rules".
- [ ] **5.1.b** Hash is deterministic — same input always produces same output (`SHA-256(JCS(credential))` via RFC 8785)
- [ ] **5.1.c** Batch hash computation tested for multiple credentials (`POST /v1/credentials/revocation-hash/batch`)

### 5.2 Publishing Revocation

- [ ] **5.2.a** Revocation published to DeDi for a test credential:
  ```bash
  curl -X POST http://localhost:3100/v1/credentials/revoke \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{ "credential": { /* VC JSON */ } }'
  ```
- [ ] **5.2.b** Revocation status confirmed via `POST /v1/credentials/revocation-status`
- [ ] **5.2.c** Post-revocation verification returns `code: "REVOKED"` — not `VALID`

### 5.3 Revocation Runbook

Every material change is a **re-issue + revoke previous**. The runbook covers each trigger:

- [ ] **5.3.a** Runbook written for each scenario:
  - Connection terminated → revoke the active credential; do not re-issue
  - Meter replaced → re-issue with new `customerProfile.meterNumber` / `meterType`; revoke previous
  - Tariff / load change → re-issue with updated `consumptionProfiles`; revoke previous
  - DER commissioned / decommissioned → re-issue with updated `generationProfiles`; revoke previous
  - Battery commissioned / decommissioned → re-issue with updated `storageProfiles`; revoke previous
  - Address / name correction → re-issue with updated `customerDetails`; revoke previous
- [ ] **5.3.b** Bulk revocation process defined (batch hash endpoint used for efficiency)

---

## Phase 6 — Consumer Delivery Channels

Delivery is a separate concern from issuance.

| Channel | When to use |
|---|---|
| DigiLocker (NYCER) | Consumer-facing identity proof; shareable with banks, societies |
| Direct VC (app / email) | App-native delivery; consumer presents at counterparty's verifier |
| QR code | On-the-spot presentation; printed on paper or rendered on a portal |
| Wallet (DID-to-DID) | When the consumer's wallet performs a request-credential handshake |

### 6.1 Direct VC Delivery

- [ ] **6.1.a** Consumer-facing delivery mechanism built — VC JSON emailed, pushed via app, or downloadable from DISCOM portal
- [ ] **6.1.b** QR code (PNG) delivery tested — consumer scans to obtain VC on mobile wallet

### 6.2 DigiLocker Integration

*See [DigiLocker Integration](../energy-credentials/digilocker-integration.md) for full implementation.*

- [ ] **6.2.a** Organisation registered on [API Setu](https://apisetu.gov.in) as DigiLocker issuer
- [ ] **6.2.b** `NYCER` document type configured: Pull URI endpoint, DocType, UDF1 = Consumer Number, UDF2 = Mobile
- [ ] **6.2.c** Pull URI endpoint built at `https://{domain}/digilocker/pulluri`:
  - HMAC verification (`x-digilocker-hmac`) — using `hmac.compare_digest`, not `==`
  - CIS lookup by consumer number
  - `POST /v1/credentials/issue` called on OpenCred to produce signed VC
  - Integration service injects full `issuer` object before delivery
  - PDF rendered and base64-encoded
  - `PullURIResponse` XML returned with `DocContent` + `VcContent`
- [ ] **6.2.d** DigiLocker sandbox test passed — credential visible under DISCOM name
- [ ] **6.2.e** Production endpoint registered on API Setu

---

## Phase 7 — Security Review

These are the seven invariants OpenCred enforces. Confirm they hold in your deployment too.

- [ ] **7.a** No endpoint in your application accepts or transmits issuer private keys
- [ ] **7.b** Private keys, signing buffers, and PINs never appear in any log output
- [ ] **7.c** Credential payloads are ephemeral — not stored in the database beyond `OPENCRED_SESSION_TTL` (default 4 hours)
- [ ] **7.d** All key generation uses CSPRNG (`openssl rand` or `crypto.randomBytes`) — never `Math.random()`
- [ ] **7.e** Error responses never leak key material, internal paths, or stack traces
- [ ] **7.f** JSON-LD contexts are bundled — OpenCred never fetches remote contexts at runtime
- [ ] **7.g** `did:web` resolution configured with SSRF protection — HTTPS only, no redirects, 10-second timeout, private-IP blocking

---

## Phase 8 — Observability and Go-Live

- [ ] **8.a** OpenCred health polled every 30 seconds — alert on `ready: false` or `signingKeyLoaded: false`
- [ ] **8.b** Prometheus metrics scraped from `GET /v1/metrics` — dashboard for issuance rate, error rate, batch job queue
- [ ] **8.c** JSON structured logs from OpenCred stdout ingested into log aggregator — `OPENCRED_LOG_LEVEL=info`
- [ ] **8.d** `OPENCRED_API_KEY` rotation schedule established (recommended: every 90 days)
- [ ] **8.e** End-to-end issue → verify → revoke loop confirmed in staging — sign-off by technical lead
- [ ] **8.f** Consumer communication ready
- [ ] **8.g** Key rotation runbook written:
  - Generate new key → update secrets manager → restart OpenCred container
  - For `did:web`: update `/.well-known/did.json` with new public key before revoking old one
  - Re-verify a test credential after rotation to confirm new key is active

---

*Reference: [OpenCred Docs](https://opencred.gitbook.io/docs) · [OpenCred API Reference](https://github.com/nfh-trust-labs/opencred/blob/new-opencred-dev/docs/api-reference.md) · [OpenCred Deployment Guide](https://github.com/nfh-trust-labs/opencred/blob/new-opencred-dev/docs/deployment-guide.md) · [IES Electricity Credentials Documentation](https://india-energy-stack.gitbook.io/docs/energy-credentials)*
