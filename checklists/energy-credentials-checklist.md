# India Energy Stack
## IES Energy Credentials
### DISCOM Readiness Checklist

**Name of DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Infrastructure Setup

- [ ] **1.a** OpenCred credential service deployed (Docker) and health check passing
- [ ] **1.b** Signing key configured — ECDSA P-256 keypair generated or existing DSC imported
- [ ] **1.c** Issuer DID established (`did:web` or `did:key`) and confirmed

### 2. DigiLocker Registration

- [ ] **2.a** Organisation registered on API Setu as a DigiLocker document issuer
- [ ] **2.b** `NYCER` document type registered with UDF1 = Consumer Number, UDF2 = Registered Mobile Number
- [ ] **2.c** API key received from API Setu and stored securely
- [ ] **2.d** Pull URI endpoint URL registered on API Setu

### 3. Pull URI Endpoint

- [ ] **3.a** HTTPS endpoint built at `https://{domain}/digilocker/pulluri`
- [ ] **3.b** Inbound HMAC verification (`x-digilocker-hmac`) implemented
- [ ] **3.c** Consumer lookup against CIS / billing database integrated
- [ ] **3.d** OpenCred issuance API call integrated (`POST /v1/credentials/issue`)
- [ ] **3.e** PDF rendering of signed credential implemented
- [ ] **3.f** `PullURIResponse` XML (with `DocContent` + `VcContent`) returning correctly

### 4. Credential Issuance Testing

- [ ] **4.a** Single credential issuance tested end-to-end via OpenCred
- [ ] **4.b** Signed VC JSON verified — proof block present and valid
- [ ] **4.c** DigiLocker sandbox test passed — credential visible in test environment
- [ ] **4.d** Revocation flow implemented (`POST /v1/credentials/revoke`) and tested
- [ ] **4.e** Revocation status confirmed via DeDi registry lookup

### 5. Verification

- [ ] **5.a** Credential verification tested via OpenCred (`POST /v1/credentials/verify`)
- [ ] **5.b** DigiLocker OAuth sharing flow tested — third-party verifier can receive and verify credential
- [ ] **5.c** HMAC on DigiLocker response verified at verifier side

### 6. Go-Live

- [ ] **6.a** Production Pull URI endpoint registered and active on API Setu
- [ ] **6.b** Consumer communication / awareness material ready
- [ ] **6.c** Monitoring and error alerting in place for the Pull URI endpoint
- [ ] **6.d** Runbook prepared for credential revocation requests

---

*Reference: [IES Energy Credentials Documentation](https://india-energy-stack.gitbook.io/docs/energy-credentials) · [OpenCred Docs](https://opencred.gitbook.io/docs)*
