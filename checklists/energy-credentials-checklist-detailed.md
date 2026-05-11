# India Energy Stack
## IES Energy Credentials — Implementation Checklist
### Detailed Technical Reference for DISCOM Integration Teams

**Name of DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Technical Lead:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Credential types:**
&nbsp; ☐ Consumer Profile &nbsp; ☐ Consumption Profile &nbsp; ☐ Generation Profile
&nbsp; ☐ Storage Profile &nbsp; ☐ Composite Profile &nbsp; ☐ Recurring Meter Data

---

## Phase 0 — Pre-requisites

- [ ] **0.a** Docker Engine (v24+) and Docker Compose installed
- [ ] **0.b** `openssl` and `curl` available in the terminal
- [ ] **0.c** OpenCred Desktop Client installed on the operator workstation ([opencred.gitbook.io/docs/desktop-app/installation](https://opencred.gitbook.io/docs/desktop-app/installation))
- [ ] **0.d** Access to CIS / billing database for consumer data lookups
- [ ] **0.e** Access to MDMS / AMISP system for meter reading data (required for Recurring Meter Data credential)
- [ ] **0.f** DeDi namespace registration initiated at `dedi.global`

---

## Phase 1 — OpenCred Infrastructure

### 1.1 Deploy OpenCred Docker Service

- [ ] **1.1.a** Generate a secure API key:
  ```bash
  openssl rand -base64 32   # → store as OPENCRED_API_KEY in secrets manager
  ```
- [ ] **1.1.b** Start OpenCred container with security hardening:
  ```bash
  docker run -d --name opencred -p 3100:3100 \
    -e OPENCRED_API_KEY=$OPENCRED_API_KEY \
    -e OPENCRED_KEY_PATH=/secrets/issuer-key.pem \
    -v /path/to/issuer-key.pem:/secrets/issuer-key.pem:ro \
    --read-only \
    --tmpfs /tmp:noexec,nosuid,size=64m \
    --cap-drop ALL \
    --security-opt no-new-privileges:true \
    opencred:latest
  ```
- [ ] **1.1.c** Health check passes and signing key is loaded:
  ```bash
  curl http://localhost:3100/v1/health
  # Expected: { "status": "ok", "ready": true, "signingKeyLoaded": true, "dediConfigured": true }
  ```
- [ ] **1.1.d** Image pinned to a SHA digest in production (not `latest`)
- [ ] **1.1.e** TLS terminated upstream (nginx / Caddy / cloud load balancer) — OpenCred itself serves HTTP only

### 1.2 Signing Key Setup

Choose one trust type based on your organisation's PKI posture. Refer to [trust chains docs](https://opencred.gitbook.io/docs/concepts/trust-chains).

**Type 1 — Import existing DSC (government agencies, regulated entities with existing certificates)**
- [ ] Import via OpenCred Desktop → Settings → Import File
- [ ] Supported formats: PFX, PEM, JWK, PKCS#8 DER
- [ ] OpenCred derives `did:key` from the certificate's public key automatically
- [ ] Trust chain: VC → DSC public key → CSCA root (verifiers trust the root)

**Type 2 — Hardware token (PKCS#11)**
- [ ] OpenCred Desktop → Settings → Hardware Token
- [ ] Select PKCS#11 library path, slot index, and enter PIN
- [ ] PIN is never persisted — entered each session

**Type 3 — Self-published key / `did:web` (recommended for new DISCOM deployments)**
- [ ] OpenCred Desktop → Settings → Generate Key → Generate ECDSA P-256 Key
- [ ] Enter domain (e.g. `ies.tpddl.in`)
- [ ] Download DID document from OpenCred Desktop
- [ ] Upload to `https://{domain}/.well-known/did.json`
- [ ] Confirm resolution:
  ```bash
  curl https://{domain}/.well-known/did.json
  # Expected: DID document with publicKeyMultibase
  ```
- [ ] Issuer DID noted: `did:web:{domain}` → \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] Trust chain: VC → published public key → DID document → domain TLS certificate

**Key Storage Verification (all types)**
- [ ] Private key material never stored in config, logs, or error responses (enforced by OpenCred invariant)
- [ ] Config file at `~/.config/opencred/opencred-config.json` stores only metadata and key path — not key material
- [ ] Host key file permissions set to `0600`:
  ```bash
  chmod 0600 /path/to/issuer-key.pem
  ```

### 1.3 DeDi Namespace Setup

- [ ] **1.3.a** DeDi namespace registered at `dedi.global` for your DISCOM
- [ ] **1.3.b** Namespace name noted (e.g. `tpddl`, `bescom`): \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **1.3.c** DeDi write credentials stored in secrets manager
- [ ] **1.3.d** DeDi namespace URL will appear in `credentialStatus` of all issued VCs:
  ```json
  {
    "credentialStatus": {
      "id": "https://dedi.global/dedi/lookup/{namespace}/vc-revocation-registry/<hash>",
      "type": "dedi",
      "statusPurpose": "revocation",
      "statusListCredential": "https://dedi.global/dedi/query/{namespace}/vc-revocation-registry"
    }
  }
  ```
- [ ] **1.3.e** `dediConfigured: true` confirmed in `/v1/health` response

---

## Phase 2 — Credential Schema Design

Define a custom JSON Schema for each credential type. Use `POST /v1/schemas/generate` to generate from field definitions, or import via URL.

### 2.1 Consumer Profile Credential

*Attests a consumer's identity, service details, and tariff classification. The foundational credential — other profiles reference it.*

- [ ] **2.1.a** Schema fields defined:

  ```json
  {
    "credentialType": "ConsumerProfileCredential",
    "fields": [
      { "name": "consumerNumber",       "type": "string", "required": true },
      { "name": "fullName",             "type": "string", "required": true },
      { "name": "serviceAddress",       "type": "string", "required": true },
      { "name": "district",             "type": "string", "required": true },
      { "name": "state",                "type": "string", "required": true },
      { "name": "serviceConnectionDate","type": "string", "required": true },
      { "name": "meterNumber",          "type": "string", "required": true },
      { "name": "consumerCategory",     "type": "string", "required": true },
      { "name": "sanctionedLoadKW",     "type": "number", "required": true },
      { "name": "tariffPlan",           "type": "string", "required": true },
      { "name": "connectionStatus",     "type": "string", "required": true },
      { "name": "maskedIdNumber",       "type": "string", "required": false }
    ]
  }
  ```

- [ ] **2.1.b** Schema registered with OpenCred:
  ```bash
  curl -X POST http://localhost:3100/v1/schemas/generate \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{ "name": "ConsumerProfileCredential", "fields": [ ... ] }'
  ```
- [ ] **2.1.c** Schema ID saved: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **2.1.d** Proof format chosen: ☐ `data-integrity` (recommended) &nbsp; ☐ `vc-jwt` &nbsp; ☐ `sd-jwt-vc`
- [ ] **2.1.e** Validity period defined: \_\_\_\_ months (recommended: 12 months; reissue annually)

### 2.2 Consumption Profile Credential

*Attests a consumer's energy consumption pattern over a defined billing or reporting period.*

- [ ] **2.2.a** Schema fields defined:

  ```json
  {
    "credentialType": "ConsumptionProfileCredential",
    "fields": [
      { "name": "consumerNumber",           "type": "string", "required": true },
      { "name": "meterNumber",              "type": "string", "required": true },
      { "name": "reportPeriodFrom",         "type": "string", "required": true },
      { "name": "reportPeriodTo",           "type": "string", "required": true },
      { "name": "totalConsumptionKWh",      "type": "number", "required": true },
      { "name": "peakConsumptionKWh",       "type": "number", "required": false },
      { "name": "offPeakConsumptionKWh",    "type": "number", "required": false },
      { "name": "averageDailyKWh",          "type": "number", "required": false },
      { "name": "maxDemandKW",              "type": "number", "required": false },
      { "name": "dataSource",              "type": "string", "required": true }
    ]
  }
  ```

- [ ] **2.2.b** Schema registered and schema ID saved: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **2.2.c** Validity period defined (recommended: matches the report period, e.g. 1 month)
- [ ] **2.2.d** Selective disclosure configured if using `sd-jwt-vc` — mark sensitive fields (e.g. `maxDemandKW`) as disclosable

### 2.3 Generation Profile Credential

*Attests a prosumer asset's renewable energy generation characteristics. Issued per generation asset.*

- [ ] **2.3.a** Schema fields defined:

  ```json
  {
    "credentialType": "GenerationProfileCredential",
    "fields": [
      { "name": "assetERA",                "type": "string", "required": true },
      { "name": "assetType",               "type": "string", "required": true },
      { "name": "installedCapacityKW",     "type": "number", "required": true },
      { "name": "commissioningDate",       "type": "string", "required": true },
      { "name": "reportPeriodFrom",        "type": "string", "required": false },
      { "name": "reportPeriodTo",          "type": "string", "required": false },
      { "name": "totalGenerationKWh",      "type": "number", "required": false },
      { "name": "gridExportKWh",           "type": "number", "required": false },
      { "name": "selfConsumptionKWh",      "type": "number", "required": false },
      { "name": "certificationStandard",   "type": "string", "required": false },
      { "name": "gridInterconnectionApproval", "type": "string", "required": true },
      { "name": "netMeteringEnabled",      "type": "boolean","required": true }
    ]
  }
  ```

- [ ] **2.3.b** Schema registered and schema ID saved: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **2.3.c** Issuer decided: ☐ DISCOM &nbsp; ☐ Renewable Energy Authority &nbsp; ☐ Both (different claims)

### 2.4 Storage Profile Credential

*Attests battery or other storage asset characteristics and current operational status.*

- [ ] **2.4.a** Schema fields defined:

  ```json
  {
    "credentialType": "StorageProfileCredential",
    "fields": [
      { "name": "assetERA",                "type": "string", "required": true },
      { "name": "assetType",               "type": "string", "required": true },
      { "name": "installedCapacityKWh",    "type": "number", "required": true },
      { "name": "chargeRateKW",            "type": "number", "required": true },
      { "name": "dischargeRateKW",         "type": "number", "required": true },
      { "name": "roundTripEfficiencyPct",  "type": "number", "required": false },
      { "name": "commissioningDate",       "type": "string", "required": true },
      { "name": "gridConnectionApproval",  "type": "string", "required": true },
      { "name": "certificationStandard",   "type": "string", "required": false },
      { "name": "operationalStatus",       "type": "string", "required": true }
    ]
  }
  ```

- [ ] **2.4.b** Schema registered and schema ID saved: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### 2.5 Composite Profile Credential

*A single credential that bundles consumer, consumption, generation, and storage profiles for a prosumer. Used where a counterparty needs the full picture in one presentation.*

- [ ] **2.5.a** Schema designed to embed all four sub-profiles as nested objects within `credentialSubject`:

  ```json
  {
    "credentialType": "CompositeEnergyProfileCredential",
    "fields": [
      { "name": "consumerNumber",    "type": "string", "required": true },
      { "name": "consumerProfile",   "type": "object", "required": true,
        "description": "Matches ConsumerProfileCredential subject fields" },
      { "name": "consumptionProfile","type": "object", "required": true,
        "description": "Matches ConsumptionProfileCredential subject fields" },
      { "name": "generationProfile", "type": "object", "required": false,
        "description": "Present only for prosumers with generation assets" },
      { "name": "storageProfile",    "type": "object", "required": false,
        "description": "Present only for prosumers with storage assets" },
      { "name": "profileAsOf",       "type": "string", "required": true,
        "description": "ISO 8601 timestamp of when this composite was assembled" }
    ]
  }
  ```

- [ ] **2.5.b** Schema registered and schema ID saved: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **2.5.c** Assembly process defined — which system triggers composite issuance and how sub-profile data is gathered
- [ ] **2.5.d** `sd-jwt-vc` considered for composite — allows counterparties to request only the sub-profiles they need

### 2.6 Recurring Meter Data Credential

*A time-series credential issued periodically (monthly, quarterly, or on-demand) attesting actual meter readings for a consumer. Allows consumers to portably share verified energy usage data.*

- [ ] **2.6.a** Schema designed to carry interval reading data in IES_Report / OpenADR 3.1.0 structure:

  ```json
  {
    "credentialType": "MeterDataCredential",
    "fields": [
      { "name": "consumerNumber",    "type": "string", "required": true },
      { "name": "meterNumber",       "type": "string", "required": true },
      { "name": "reportPeriodFrom",  "type": "string", "required": true },
      { "name": "reportPeriodTo",    "type": "string", "required": true },
      { "name": "intervalMinutes",   "type": "number", "required": true,
        "description": "15 for AMI smart meters, 60 for conventional" },
      { "name": "totalKWh",          "type": "number", "required": true },
      { "name": "intervals",         "type": "array",  "required": true,
        "description": "Array of { start, duration, kWh } — OpenADR 3.1.0 interval format" },
      { "name": "dataSource",        "type": "string", "required": true,
        "description": "MDMS system identifier or AMISP name" },
      { "name": "meterReadingMethod","type": "string", "required": true,
        "description": "AMI_AUTOMATIC | MANUAL | ESTIMATED" }
    ]
  }
  ```

- [ ] **2.6.b** Schema registered and schema ID saved: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **2.6.c** Issuance trigger defined: ☐ Monthly billing cycle &nbsp; ☐ On consumer request &nbsp; ☐ Both
- [ ] **2.6.d** MDMS / AMISP data pipeline to OpenCred issuance call automated
- [ ] **2.6.e** Large interval array handling tested — verify `OPENCRED_SESSION_TTL` (default 4 hours) is sufficient for batch jobs

---

## Phase 3 — Credential Issuance

### 3.1 Single Credential Issuance (API)

For each credential type, the issuance call follows this pattern:

```bash
curl -X POST http://localhost:3100/v1/credentials/issue \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "schemaId": "<schema-id-for-type>",
    "issuerDid": "did:web:ies.{discom}.in",
    "proofFormat": "data-integrity",
    "credentialSubject": { /* type-specific fields */ },
    "validFrom": "2026-04-01T00:00:00Z",
    "validUntil": "2027-04-01T00:00:00Z",
    "additionalTypes": ["<CredentialTypeName>"]
  }'
```

- [ ] **3.1.a** Consumer Profile credential issued and signed VC JSON received
- [ ] **3.1.b** Consumption Profile credential issued for a test consumer and billing period
- [ ] **3.1.c** Generation Profile credential issued for a test prosumer asset
- [ ] **3.1.d** Storage Profile credential issued for a test storage asset
- [ ] **3.1.e** Composite Profile credential issued — all four sub-profiles present in `credentialSubject`
- [ ] **3.1.f** Recurring Meter Data credential issued for a test consumer with at least one month of interval data

For each issued credential, confirm:
- [ ] `proof` block present with correct `verificationMethod` pointing to your issuer DID
- [ ] `credentialStatus` block present with `type: "dedi"` and correct namespace URL
- [ ] `validFrom` and `validUntil` set correctly
- [ ] `maskedIdNumber` used — full Aadhaar/ID never in credential payload

### 3.2 Single Issuance via CLI

For scripted / offline issuance using the OpenCred CLI:

```bash
# Build the CLI first
cd apps/server && pnpm build

# Issue a credential
node dist/cli.js issue \
  --schema ConsumerProfileCredential \
  --input consumer-subject.json \
  --key /path/to/issuer-key.pem \
  --proof-format data-integrity \
  --output consumer-profile-vc.json
```

- [ ] **3.2.a** CLI issuance tested for at least one credential type
- [ ] **3.2.b** Output file is a valid W3C VC JSON — same format as API output

### 3.3 Single Issuance via Desktop Client

For ad-hoc issuance by non-technical staff:

- [ ] **3.3.a** Custom schemas for all 6 types visible on OpenCred Desktop Home screen
- [ ] **3.3.b** Staff trained on: selecting schema → filling fields → choosing signing key → Build & Sign → export
- [ ] **3.3.c** Export formats tested: JSON (for API consumers), PDF (for printing/emailing to consumer), QR code (for scanning)

### 3.4 Batch Issuance

For issuing credentials to a large number of consumers at once:

```bash
# Via API
curl -X POST http://localhost:3100/v1/credentials/batch \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "csvContent": "<base64-encoded-CSV>",
    "schemaId": "ConsumerProfileCredential",
    "issuerDid": "did:web:ies.{discom}.in",
    "validFrom": "2026-04-01T00:00:00Z"
  }'
# Response: { "jobId": "...", "validCount": N, "invalidCount": M }

# Poll for job completion
curl http://localhost:3100/v1/credentials/batch/{jobId} \
  -H "Authorization: Bearer $OPENCRED_API_KEY"

# Download results
curl http://localhost:3100/v1/credentials/batch/{jobId}/results \
  -H "Authorization: Bearer $OPENCRED_API_KEY"
```

- [ ] **3.4.a** Batch issuance tested for Consumer Profile — CSV prepared with one consumer per row
- [ ] **3.4.b** Column mapping verified — CSV headers match schema field names (or `columnMapping` provided)
- [ ] **3.4.c** Job polling implemented — application waits for `status: completed` before downloading results
- [ ] **3.4.d** Results ZIP downloaded and individual VC JSON files validated
- [ ] **3.4.e** Batch size limit noted: default 1,000 rows; increase via `OPENCRED_BATCH_ROW_LIMIT` env var if needed
- [ ] **3.4.f** Batch issuance tested for Recurring Meter Data — one row per consumer per billing period
- [ ] **3.4.g** CSV delimiter confirmed (auto-detected: comma, semicolon, or tab)

### 3.5 Packaging and Delivery

- [ ] **3.5.a** `POST /v1/credentials/package` used to render delivery formats:
  ```bash
  curl -X POST http://localhost:3100/v1/credentials/package \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -d '{ "credential": { ... }, "format": "pdf" }'
  ```
- [ ] **3.5.b** PDF output reviewed — DISCOM branding (logo, primary colour) configured via `--logo` and `--primary-color` options
- [ ] **3.5.c** QR code output tested — QR encodes the full VC JSON and is scannable by a verifier app

---

## Phase 4 — Credential Verification

### 4.1 API Verification

```bash
curl -X POST http://localhost:3100/v1/credentials/verify \
  -H "Authorization: Bearer $OPENCRED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "credential": "<JSON-stringified VC>" }'
```

Expected response:
```json
{
  "valid": true,
  "code": "VALID",
  "checks": [
    { "name": "signature",      "passed": true },
    { "name": "notBefore",      "passed": true },
    { "name": "expiry",         "passed": true },
    { "name": "keyResolution",  "passed": true }
  ]
}
```

- [ ] **4.1.a** Verification tested for each of the 6 credential types — `valid: true` for all
- [ ] **4.1.b** Expired credential test — `validUntil` in the past → `code: "EXPIRED"`
- [ ] **4.1.c** Tampered credential test — modify `credentialSubject` field → `code: "INVALID"` (signature check fails)
- [ ] **4.1.d** Unresolvable DID test — delete or corrupt DID document → `code: "UNRESOLVABLE"`
- [ ] **4.1.e** All result codes handled in application: `VALID`, `INVALID`, `REVOKED`, `EXPIRED`, `UNRESOLVABLE`

### 4.2 Desktop Client Verification

- [ ] **4.2.a** OpenCred Desktop → Verify page — paste VC JSON → Verify → all four checks shown as passed
- [ ] **4.2.b** Offline verification confirmed for `did:key` credentials (no network, JSON-LD contexts are bundled)
- [ ] **4.2.c** `did:web` credential verification confirmed — requires network to fetch DID document from `/.well-known/did.json`

### 4.3 CLI Verification

```bash
node dist/cli.js verify --input consumer-profile-vc.json
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
    -d '{ "credential": { /* VC JSON without proof block */ } }'
  # Returns: { "hash": "sha256hex..." }
  ```
- [ ] **5.1.b** Hash is deterministic — same input always produces same output (JCS canonicalization via RFC 8785)
- [ ] **5.1.c** Batch hash computation tested for multiple credentials:
  ```bash
  POST /v1/credentials/revocation-hash/batch
  ```

### 5.2 Publishing Revocation

- [ ] **5.2.a** Revocation published to DeDi for a test credential:
  ```bash
  curl -X POST http://localhost:3100/v1/credentials/revoke \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{ "credential": { /* VC JSON */ } }'
  ```
  > Note: OpenCred computes the hash and publishes to your DeDi namespace. It does **not** publish on your behalf without this explicit call.

- [ ] **5.2.b** Revocation status confirmed — query DeDi for the hash and confirm it is present:
  ```bash
  POST /v1/credentials/revocation-status
  ```
- [ ] **5.2.c** Post-revocation verification returns `code: "REVOKED"` — not `VALID`

### 5.3 Revocation Runbook

- [ ] **5.3.a** Runbook written for each revocation scenario:
  - Connection terminated → revoke Consumer Profile + Consumption Profile + Composite
  - Meter replaced → revoke and reissue Consumer Profile (new meter number)
  - Data correction → revoke old credential, issue corrected version
  - Asset decommissioned → revoke Generation Profile or Storage Profile
  - Recurring Meter Data correction → revoke period credential, reissue corrected
- [ ] **5.3.b** Internal process defined for bulk revocation (batch hash endpoint used for efficiency)

---

## Phase 6 — Consumer Delivery Channels

Delivery is a separate concern from issuance. Choose the right channel for each credential type.

| Credential Type | Recommended Channel | Notes |
|---|---|---|
| Consumer Profile | DigiLocker (NYCER) | Consumer-facing identity proof; shareable with banks, societies |
| Consumption Profile | Direct VC (app / email) | Periodic delivery; consumer shares for energy audits, loans |
| Generation Profile | Direct VC + Registry | Presented during P2P trades; also registered on IES network |
| Storage Profile | Direct VC + Registry | Presented during P2P trades |
| Composite Profile | Direct VC | On-demand for prosumers needing full profile for a counterparty |
| Recurring Meter Data | Direct VC (app) | Monthly push; consumer presents to service providers |

### 6.1 Direct VC Delivery (all credential types)

- [ ] **6.1.a** Consumer-facing delivery mechanism built — VC JSON emailed, pushed via app, or downloadable from DISCOM portal
- [ ] **6.1.b** QR code (PNG) delivery tested — consumer scans to obtain VC on mobile wallet
- [ ] **6.1.c** Recurring Meter Data automated delivery confirmed — triggered monthly after billing cycle close

### 6.2 DigiLocker Integration (Consumer Profile / NYCER only)

*DigiLocker is one delivery channel for the Consumer Profile credential. It is not required for other credential types.*

- [ ] **6.2.a** Organisation registered on [API Setu](https://apisetu.gov.in) as DigiLocker issuer
- [ ] **6.2.b** `NYCER` document type configured: Pull URI endpoint, DocType, UDF1 = Consumer Number, UDF2 = Mobile
- [ ] **6.2.c** Pull URI endpoint built at `https://{domain}/digilocker/pulluri`:
  - HMAC verification (`x-digilocker-hmac`) — using `hmac.compare_digest`, not `==`
  - CIS lookup by consumer number
  - `POST /v1/credentials/issue` called on OpenCred to produce signed VC
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
- [ ] **8.e** All 6 credential types issued, verified, and revoked in staging — sign-off by technical lead
- [ ] **8.f** Consumer communication ready — inform consumers which credentials are available and how to access them
- [ ] **8.g** Key rotation runbook written:
  - Generate new key → update secrets manager → restart OpenCred container
  - For `did:web`: update `/.well-known/did.json` with new public key before revoking old one
  - Re-verify a test credential after rotation to confirm new key is active

---

*Reference: [OpenCred Docs](https://opencred.gitbook.io/docs) · [OpenCred API Reference](https://github.com/nfh-trust-labs/opencred/blob/new-opencred-dev/docs/api-reference.md) · [OpenCred Deployment Guide](https://github.com/nfh-trust-labs/opencred/blob/new-opencred-dev/docs/deployment-guide.md) · [IES Energy Credentials Documentation](https://india-energy-stack.gitbook.io/docs/energy-credentials)*
