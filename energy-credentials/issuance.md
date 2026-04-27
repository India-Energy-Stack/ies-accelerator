# Issuing Credentials

IES Energy Credentials are issued using the **OpenCred** credential service — an open-source W3C VC platform available as a desktop application or a self-hosted Docker API. This page covers both paths.

> Full OpenCred documentation: [https://opencred.gitbook.io/docs](https://opencred.gitbook.io/docs)

---

## Two Ways to Issue

| Method | Best for |
|---|---|
| [Desktop Client](#desktop-client) | One-off issuance, testing, small batches |
| [Docker API](#docker-api) | Production — DISCOM systems calling programmatically |

---

## Desktop Client

### Install

| Platform | Package |
|---|---|
| macOS | `.dmg` → drag to Applications |
| Windows | `.exe` installer |
| Linux | `.AppImage` (chmod +x) or `.deb` |

Download from the [OpenCred releases page](https://opencred.gitbook.io/docs).

### First Launch — Set Up Your Signing Key

On first launch, the onboarding wizard asks you to configure a signing key. You have three options:

**Option A — Import an existing Digital Signature Certificate (DSC)**
- Import a PFX, PEM file, hardware token, or OS certificate store (macOS Keychain / Windows CNG)
- OpenCred derives a `did:key` from your certificate's public key

**Option B — Generate a fresh ECDSA P-256 keypair**
1. Settings → Generate Key → **Generate ECDSA P-256 Key**
2. Enter your domain (e.g. `ies.tpddl.in`)
3. Download the generated DID document
4. Upload it to `https://<your-domain>/.well-known/did.json`
5. Your issuer DID becomes `did:web:<your-domain>`

**Option C — Hardware token (PKCS#11)**
1. Settings → Hardware Token
2. Select your PKCS#11 library
3. Enter slot index and PIN (PIN is never persisted)

> OpenCred never stores private key material or PINs. Config lives at `~/.config/opencred/opencred-config.json`.

### Issue a Single Credential

1. Select a schema from the Home screen (use a custom IES schema for energy credentials)
2. Fill in the credential subject fields (consumer number, address, meter number, etc.)
3. Configure:
   - **Signing key** — select from your imported keys
   - **Valid from / Valid until** — ISO 8601 dates
   - **Proof format** — `data-integrity` recommended for IES (JSON-LD embedded proof)
4. Click **Build & Sign**
5. Export as JSON, PDF, or QR code

### Issue in Bulk (Batch)

1. Prepare a CSV with one row per credential (max 1,000 rows)
2. Upload CSV — OpenCred auto-detects delimiter (comma, semicolon, tab)
3. Map CSV columns to schema fields
4. Configure validity dates, signing key, output formats
5. Export results as ZIP (one file per credential)

---

## Docker API

For production DISCOM systems, deploy OpenCred as a Docker container and call its REST API.

### Deploy

```bash
# Build the image
docker build -f apps/server/Dockerfile -t opencred:latest .

# Run with a signing key mounted
docker run -p 3100:3100 \
  -e OPENCRED_API_KEY=sk_prod_change_me \
  -e OPENCRED_KEY_PATH=/secrets/issuer-key.pem \
  -v /path/to/issuer-key.pem:/secrets/issuer-key.pem:ro \
  opencred:latest
```

Or with Docker Compose:

```yaml
services:
  opencred:
    image: opencred:latest
    ports:
      - "3100:3100"
    environment:
      OPENCRED_API_KEY: ${OPENCRED_API_KEY}
      OPENCRED_KEY_PATH: /app/keys/issuer-key.pem
      OPENCRED_LOG_LEVEL: info
    volumes:
      - ./keys/issuer-key.pem:/app/keys/issuer-key.pem:ro
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
```

Generate a secure API key:
```bash
openssl rand -base64 32
```

Verify the service is up:
```bash
curl http://localhost:3100/v1/health
# → 200 (ready) or 503 (signing key not loaded)
```

### Core Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENCRED_API_KEY` | Yes | Bearer token for all protected endpoints |
| `OPENCRED_KEY_PATH` | Yes* | Path to signing key (PEM, JWK, PKCS#8, PFX) |
| `OPENCRED_KEY_PASSWORD` | No | Password for PFX files |
| `OPENCRED_PORT` | No (default 3100) | HTTP listen port |
| `OPENCRED_LOG_LEVEL` | No (default `info`) | `fatal/error/warn/info/debug/trace` |

*Or configure a Cloud KMS provider (AWS KMS, Azure Key Vault, GCP Cloud KMS) instead of a file.

### Issue a Credential

```http
POST http://localhost:3100/v1/credentials/issue
Authorization: Bearer sk_prod_change_me
Content-Type: application/json
```

```json
{
  "issuer": "did:web:ies.tpddl.in",
  "credentialType": "ElectricityConnectionCredential",
  "proofFormat": "data-integrity",
  "credentialSubject": {
    "id": "did:key:z6Mk...",
    "fullName": "Priya Sharma",
    "consumerNumber": "TPDDL-2025-001234567",
    "serviceAddress": "Flat 4B, Sector 12, Rohini, New Delhi – 110085",
    "serviceConnectionDate": "2019-03-15",
    "meterNumber": "MTR-98765432",
    "maskedIdNumber": "XXXX-XXXX-1234"
  },
  "validFrom": "2026-04-01T00:00:00Z",
  "validUntil": "2027-04-01T00:00:00Z",
  "revocationRegistryUrl": "https://dedi.global/dedi/query/<namespace>/vc-revocation-registry"
}
```

| Field | Description |
|---|---|
| `issuer` | Your DID — `did:key:...` or `did:web:<domain>` |
| `credentialType` | The IES credential type name |
| `proofFormat` | `data-integrity` (JSON-LD embedded proof), `vc-jwt`, or `sd-jwt-vc` (selective disclosure) |
| `credentialSubject.id` | The holder's DID |
| `maskedIdNumber` | Masked Aadhaar — never pass or store the full number |
| `revocationRegistryUrl` | Include to embed a `credentialStatus` block for revocation support |

**Response** — signed credential with proof block:

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://ies.energy/credentials/v1"
  ],
  "id": "urn:uuid:4b3a1c9e-...",
  "type": ["VerifiableCredential", "ElectricityConnectionCredential"],
  "issuer": "did:web:ies.tpddl.in",
  "validFrom": "2026-04-01T00:00:00Z",
  "validUntil": "2027-04-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:key:z6Mk...",
    "fullName": "Priya Sharma",
    "consumerNumber": "TPDDL-2025-001234567",
    "serviceAddress": "Flat 4B, Sector 12, Rohini, New Delhi – 110085",
    "serviceConnectionDate": "2019-03-15",
    "meterNumber": "MTR-98765432"
  },
  "credentialStatus": {
    "id": "https://dedi.global/dedi/lookup/<namespace>/vc-revocation-registry/<hash>",
    "type": "dedi",
    "statusPurpose": "revocation",
    "statusListCredential": "https://dedi.global/dedi/query/<namespace>/vc-revocation-registry"
  },
  "proof": {
    "type": "DataIntegrityProof",
    "cryptosuite": "ecdsa-2019",
    "created": "2026-04-01T10:00:00Z",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:web:ies.tpddl.in#key-1",
    "proofValue": "z3FXQ...signature...kKJh6"
  }
}
```

Store the full signed credential JSON — you need it for the DigiLocker `PullURIResponse`.

### Batch Issuance

```http
POST http://localhost:3100/v1/credentials/batch
Authorization: Bearer sk_prod_change_me
Content-Type: application/json
```

```json
{
  "csvData": "<base64-encoded-csv>",
  "credentialType": "ElectricityConnectionCredential",
  "proofFormat": "data-integrity",
  "validFrom": "2026-04-01T00:00:00Z",
  "validUntil": "2027-04-01T00:00:00Z"
}
```

Returns a session ID for progress tracking. Max 1,000 rows per batch (configurable via `OPENCRED_BATCH_ROW_LIMIT`).

---

## Proof Formats

| Format | Description | Use when |
|---|---|---|
| `data-integrity` | JSON-LD embedded proof | Default for IES — human-readable, inspectable |
| `vc-jwt` | JWT-wrapped VC | Interop with JWT-native verifiers |
| `sd-jwt-vc` | Selective disclosure JWT | When holders need to reveal only specific fields |

---

## Revoking a Credential

Revocation uses the **DeDi** hash registry. OpenCred computes a SHA-256 hash of the canonicalised credential; publishing that hash to DeDi marks it as revoked.

```bash
# Step 1 — compute the revocation hash
POST http://localhost:3100/v1/credentials/revocation-hash
Authorization: Bearer sk_prod_change_me
Content-Type: application/json

{ "credential": { /* full VC JSON */ } }

# Step 2 — publish the hash to your DeDi namespace
POST http://localhost:3100/v1/credentials/revoke
Authorization: Bearer sk_prod_change_me
Content-Type: application/json

{ "credential": { /* full VC JSON */ } }
```

Any verifier that subsequently checks this credential will find its hash in the DeDi registry and return `revoked: true`.

---

## Available API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `GET /v1/health` | GET | Liveness probe (no auth) |
| `GET /v1/keys` | GET | List loaded signing keys |
| `POST /v1/credentials/issue` | POST | Issue a single credential |
| `POST /v1/credentials/batch` | POST | Batch issue from CSV |
| `POST /v1/credentials/verify` | POST | Verify a credential |
| `POST /v1/credentials/revoke` | POST | Publish revocation |
| `POST /v1/credentials/revocation-hash` | POST | Compute revocation hash |
| `GET /v1/credentials/revocation-status` | GET | Check revocation status |
| `GET /v1/schemas` | GET | List available schemas |
| `GET /v1/metrics` | GET | Prometheus metrics (no auth) |
