# India Energy Stack
## IES Energy Credentials — Implementation Checklist
### Detailed Technical Reference for DISCOM Integration Teams

**Name of DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Technical Lead:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Phase 0 — Pre-requisites

- [ ] **0.a** Docker Engine (v24+) and Docker Compose installed on the server that will host OpenCred
- [ ] **0.b** Outbound HTTPS access from that server to `dedi.global` (revocation registry) and issuer DID domains
- [ ] **0.c** An HTTPS domain with a valid TLS certificate available for your Pull URI endpoint (e.g. `https://ies.{discom}.in`)
- [ ] **0.d** Read access to CIS / billing database from the server hosting the Pull URI endpoint
- [ ] **0.e** OpenCred Desktop Client installed on the operator workstation used for key management ([opencred.gitbook.io/docs](https://opencred.gitbook.io/docs/desktop-client/installation))

---

## Phase 1 — OpenCred Deployment

### 1.1 Deploy the OpenCred Docker Service

- [ ] **1.1.a** Generate a secure API key and store in your secrets manager:
  ```bash
  openssl rand -base64 32   # → save as OPENCRED_API_KEY
  ```
- [ ] **1.1.b** Obtain or generate the DISCOM signing key (PEM/PKCS#8/PFX). Options:
  - Import existing DSC: OpenCred Desktop → Settings → Import File
  - Generate new ECDSA P-256: OpenCred Desktop → Settings → Generate Key
- [ ] **1.1.c** Mount the key and start the container:
  ```bash
  docker run -d -p 3100:3100 \
    -e OPENCRED_API_KEY=$OPENCRED_API_KEY \
    -e OPENCRED_KEY_PATH=/secrets/issuer-key.pem \
    -v /path/to/issuer-key.pem:/secrets/issuer-key.pem:ro \
    --read-only --cap-drop ALL \
    opencred:latest
  ```
- [ ] **1.1.d** Health check passes:
  ```bash
  curl http://localhost:3100/v1/health
  # Expected: HTTP 200
  ```
- [ ] **1.1.e** Confirm signing key is loaded:
  ```bash
  curl -H "Authorization: Bearer $OPENCRED_API_KEY" \
    http://localhost:3100/v1/keys
  # Expected: JSON array with at least one key entry
  ```
- [ ] **1.1.f** Docker Compose file committed to internal source control with secrets injected via environment (not hardcoded)

### 1.2 Establish the Issuer DID

- [ ] **1.2.a** Decide on DID method:
  - `did:web` — recommended for production (supports key rotation, domain-anchored trust)
  - `did:key` — acceptable for testing (no rotation, offline-resolvable)
- [ ] **1.2.b** If using `did:web`:
  - [ ] Domain chosen (e.g. `ies.tpddl.in`)
  - [ ] ECDSA P-256 keypair generated via OpenCred Desktop
  - [ ] DID document downloaded from OpenCred Desktop
  - [ ] DID document uploaded to `https://{domain}/.well-known/did.json`
  - [ ] Resolution confirmed: `curl https://{domain}/.well-known/did.json` returns the DID document
  - [ ] Issuer DID noted: `did:web:{domain}` → \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **1.2.c** If using `did:key`:
  - [ ] Key generated, `did:key:...` string noted → \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Phase 2 — DigiLocker Registration

- [ ] **2.a** DISCOM account registered on [API Setu](https://apisetu.gov.in) as a document issuer
  - If already registered for ELBIL (electricity bill): contact NeGD/Chikan to add `NYCER` document type to existing account — do **not** re-register
- [ ] **2.b** `NYCER` document type registered with:
  - Endpoint URL: `https://{your-domain}/digilocker/pulluri`
  - HTTP Method: `POST`
  - Content-Type: `application/xml`
  - DocType: `NYCER`
  - UDF1 label: `Consumer Number`
  - UDF2 label: `Registered Mobile Number`
- [ ] **2.c** `issuer_id` received from API Setu (e.g. `in.gov.tpddl`) → noted: \_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **2.d** `api_key` received from API Setu → stored in secrets manager (never in code)
- [ ] **2.e** If sharing endpoint with ELBIL: confirmed that existing Pull URI handler dispatches on `DocType` field

---

## Phase 3 — Pull URI Endpoint Implementation

### 3.1 Inbound HMAC Verification

- [ ] **3.1.a** Raw request body captured **before** any parsing (bytes, not string)
- [ ] **3.1.b** `x-digilocker-hmac` header extracted from inbound request
- [ ] **3.1.c** HMAC verified using constant-time comparison:
  ```python
  import hmac, hashlib, base64

  def verify_hmac(body: bytes, api_key: str, received: str) -> bool:
      expected = base64.b64encode(
          hmac.new(api_key.encode(), body, hashlib.sha256).digest()
      ).decode()
      return hmac.compare_digest(expected, received)
  ```
  - [ ] Using `hmac.compare_digest` (not `==`) to prevent timing attacks
  - [ ] Returning HTTP 401 immediately if HMAC fails — no further processing
- [ ] **3.1.d** `keyhash` field (SHA-256 of `api_key + ts`) validated as secondary check

### 3.2 Request Parsing

- [ ] **3.2.a** `PullURIRequest` XML v3.0 parsed — fields extracted:
  - `ts` (timestamp — echo in response)
  - `txn` (transaction ID — echo in response)
  - `DocType` (should be `NYCER`)
  - `UDF1` → consumer number (primary CIS lookup key)
  - `UDF2` → registered mobile number (secondary verification)
  - `FullName` (optional — DigiLocker validates name match on response)
- [ ] **3.2.b** `DocType` checked — handler returns error if unexpected type received

### 3.3 CIS Consumer Lookup

- [ ] **3.3.a** Consumer looked up by `UDF1` (consumer number) in CIS/billing database
- [ ] **3.3.b** `UDF2` (mobile number) cross-checked against CIS record for secondary verification
- [ ] **3.3.c** Error response returned (`Status=0`) if consumer not found — correct XML format:
  ```xml
  <PullURIResponse ver="3.0" ts="{ts}" txn="{txn}" orgId="{issuer_id}">
    <ResponseStatus Status="0" ts="{ts}" txn="{txn}">Consumer not found</ResponseStatus>
  </PullURIResponse>
  ```
- [ ] **3.3.d** Full Aadhaar number **never** stored, logged, or transmitted — only masked form (`XXXX-XXXX-1234`)

### 3.4 OpenCred Credential Issuance Call

- [ ] **3.4.a** `POST /v1/credentials/issue` called on OpenCred with correct payload:
  ```json
  {
    "issuer": "did:web:{your-domain}",
    "credentialType": "ElectricityConnectionCredential",
    "proofFormat": "data-integrity",
    "credentialSubject": {
      "fullName": "<consumer full name>",
      "consumerNumber": "<UDF1>",
      "serviceAddress": "<full service address from CIS>",
      "serviceConnectionDate": "<ISO date>",
      "meterNumber": "<meter number>",
      "maskedIdNumber": "XXXX-XXXX-<last 4>"
    },
    "validFrom": "<today ISO 8601>",
    "validUntil": "<today + 365 days ISO 8601>",
    "revocationRegistryUrl": "https://dedi.global/dedi/query/<namespace>/vc-revocation-registry"
  }
  ```
- [ ] **3.4.b** `Authorization: Bearer $OPENCRED_API_KEY` header included on every call
- [ ] **3.4.c** Response validated — `proof` block is present in the returned VC JSON
- [ ] **3.4.d** Full signed VC JSON stored (needed for revocation hash computation later)
- [ ] **3.4.e** Timeout handling implemented — DigiLocker expects response within ~10 seconds; async pattern used if OpenCred call is slow

### 3.5 PDF Rendering

- [ ] **3.5.a** PDF generated from the signed VC JSON using your template engine (OpenCred does not produce PDFs)
- [ ] **3.5.b** Signed VC JSON embedded as QR code on the PDF
- [ ] **3.5.c** PDF binary base64-encoded for `DocContent` field

### 3.6 PullURIResponse Assembly

- [ ] **3.6.a** VC JSON base64-encoded for `VcContent` field
- [ ] **3.6.b** `URI` constructed as `{issuer_id}-NYCER-{consumerNumber}`
- [ ] **3.6.c** `IssuedTo` field matches `FullName` from DigiLocker request (DigiLocker validates name match)
- [ ] **3.6.d** `ValidFrom` and `ValidTo` dates match credential validity period
- [ ] **3.6.e** Full response:
  ```xml
  <PullURIResponse ver="3.0" ts="{ts}" txn="{txn}" orgId="{issuer_id}">
    <ResponseStatus Status="1" ts="{ts}" txn="{txn}"/>
    <DocDetails>
      <DocType>NYCER</DocType>
      <URI>{issuer_id}-NYCER-{consumerNumber}</URI>
      <IssuedTo>{fullName}</IssuedTo>
      <ValidFrom>{validFrom}</ValidFrom>
      <ValidTo>{validUntil}</ValidTo>
      <DocContent format="pdf">{base64PDF}</DocContent>
      <VcContent format="json-ld">{base64VC}</VcContent>
    </DocDetails>
  </PullURIResponse>
  ```

---

## Phase 4 — Testing

### 4.1 Unit Tests

- [ ] **4.1.a** HMAC verification tested with a known `api_key` + body → expected HMAC computed and matched
- [ ] **4.1.b** HMAC rejection tested — modified body → `hmac.compare_digest` returns false → HTTP 401 returned
- [ ] **4.1.c** Consumer-not-found path tested — `Status=0` XML returned
- [ ] **4.1.d** OpenCred mock tested — handler correctly assembles `PullURIResponse` from mock VC response

### 4.2 End-to-End Tests

- [ ] **4.2.a** Simulated DigiLocker `PullURIRequest` sent to endpoint:
  ```bash
  curl -X POST https://{your-domain}/digilocker/pulluri \
    -H "Content-Type: application/xml" \
    -H "x-digilocker-hmac: <computed-hmac>" \
    -d @test-pulluri-request.xml
  ```
- [ ] **4.2.b** Response is a valid `PullURIResponse` XML with `Status=1`
- [ ] **4.2.c** `DocContent` decodes to a valid PDF
- [ ] **4.2.d** `VcContent` decodes to a valid W3C VC JSON-LD with a `proof` block
- [ ] **4.2.e** DigiLocker sandbox test completed — credential visible in sandbox DigiLocker environment under DISCOM name

### 4.3 Credential Verification Test

- [ ] **4.3.a** Extracted VC JSON passed to OpenCred verify endpoint:
  ```bash
  curl -X POST http://localhost:3100/v1/credentials/verify \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"credential": <VC JSON>}'
  ```
- [ ] **4.3.b** Response shows `"isValid": true` with all checks passing:
  - `signature: passed`
  - `notBefore: passed`
  - `expiry: passed`
  - `revocation: passed`

### 4.4 Revocation Test

- [ ] **4.4.a** Revocation hash computed for a test credential:
  ```bash
  curl -X POST http://localhost:3100/v1/credentials/revocation-hash \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -d '{"credential": <VC JSON>}'
  ```
- [ ] **4.4.b** Credential revoked via OpenCred:
  ```bash
  curl -X POST http://localhost:3100/v1/credentials/revoke \
    -H "Authorization: Bearer $OPENCRED_API_KEY" \
    -d '{"credential": <VC JSON>}'
  ```
- [ ] **4.4.c** Verify call on revoked credential returns `"isValid": false` with `revocation: failed`

---

## Phase 5 — Security Review

- [ ] **5.a** `OPENCRED_API_KEY` not present in source code, Docker image, or logs — injected via secrets manager
- [ ] **5.b** Signing key file mounted as read-only volume in Docker (`ro` flag)
- [ ] **5.c** Pull URI endpoint accessible only over HTTPS (TLS 1.2+); HTTP redirects to HTTPS or is blocked
- [ ] **5.d** Rate limiting applied to Pull URI endpoint (recommended: 10 req/s per IP)
- [ ] **5.e** No full Aadhaar/ID numbers appear in application logs or database
- [ ] **5.f** OpenCred container runs with `--cap-drop ALL`, `--read-only`, `no-new-privileges`
- [ ] **5.g** DID document at `/.well-known/did.json` is static and served over HTTPS — no server-side generation

---

## Phase 6 — Go-Live

- [ ] **6.a** Production Pull URI endpoint registered on API Setu and marked active
- [ ] **6.b** Load test completed against Pull URI endpoint (DigiLocker can send concurrent requests during peak)
- [ ] **6.c** Monitoring and alerting configured:
  - HTTP 5xx rate on Pull URI endpoint
  - OpenCred `/v1/health` monitored — alert on non-200
  - Response time > 8 seconds (DigiLocker timeout risk)
- [ ] **6.d** Consumer-facing communication ready (SMS / IVR / website) — consumers notified that NYCER credential is available in DigiLocker
- [ ] **6.e** Internal runbook prepared:
  - How to revoke a credential (connection termination / meter replacement)
  - How to rotate the signing key and update the DID document
  - How to handle DigiLocker support escalations
- [ ] **6.f** Log retention policy confirmed (no VC payload or PII in logs; only transaction IDs and status codes)

---

*Reference: [IES Energy Credentials Documentation](https://india-energy-stack.gitbook.io/docs/energy-credentials) · [OpenCred Docs](https://opencred.gitbook.io/docs) · [API Setu DigiLocker Partner Portal](https://partners.digitallocker.gov.in)*
