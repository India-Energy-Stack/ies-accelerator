# India Energy Stack
## IES Energy Credentials
### DISCOM Readiness Checklist

**Name of DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Credential types being implemented:**
&nbsp; ☐ Consumer Profile &nbsp; ☐ Consumption Profile &nbsp; ☐ Generation Profile
&nbsp; ☐ Storage Profile &nbsp; ☐ Composite Profile &nbsp; ☐ Recurring Meter Data

---

### 1. Infrastructure Setup

- [ ] **1.a** OpenCred service deployed (Docker) and health check passing
- [ ] **1.b** Signing key configured — method chosen: ☐ DSC import &nbsp; ☐ Generated ECDSA P-256 &nbsp; ☐ Hardware token
- [ ] **1.c** Issuer DID established and noted (`did:web` or `did:key`): \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **1.d** DeDi namespace registered and accessible (`dedi.global`)
- [ ] **1.e** `credentialStatus` block embedding confirmed — revocation hash included in issued VCs

### 2. Credential Schema Design

- [ ] **2.a** **Consumer Profile** schema defined — consumer identity, service address, connection details, tariff plan
- [ ] **2.b** **Consumption Profile** schema defined — billing period, total/peak/off-peak kWh, average daily consumption
- [ ] **2.c** **Generation Profile** schema defined — asset ERA, installed capacity, generation period, grid export, certification standard
- [ ] **2.d** **Storage Profile** schema defined — asset ERA, capacity kWh, charge/discharge rate, round-trip efficiency
- [ ] **2.e** **Composite Profile** schema defined — single credential containing consumer, consumption, generation, and storage subjects
- [ ] **2.f** **Recurring Meter Data** schema defined — meter ID, report period, interval readings (15-min or hourly), total kWh
- [ ] **2.g** All schemas registered with OpenCred (`POST /v1/schemas/generate` or custom JSON Schema URL)
- [ ] **2.h** Proof format chosen for each credential type: ☐ `data-integrity` &nbsp; ☐ `vc-jwt` &nbsp; ☐ `sd-jwt-vc` (selective disclosure)

### 3. Credential Issuance

- [ ] **3.a** Single credential issuance tested for each of the 6 types (`POST /v1/credentials/issue`)
- [ ] **3.b** Signed VC JSON validated — `proof` block present, `credentialStatus` embedded
- [ ] **3.c** Batch issuance working — CSV upload, column mapping, ZIP output (`POST /v1/credentials/batch`)
- [ ] **3.d** Recurring Meter Data credential issuance automated — triggered monthly or per reporting period
- [ ] **3.e** Composite Profile credential assembled and issued — all sub-profiles present and consistent
- [ ] **3.f** Export formats tested: ☐ JSON &nbsp; ☐ PDF &nbsp; ☐ QR code (PNG)

### 4. Credential Verification

- [ ] **4.a** Verification tested for each credential type (`POST /v1/credentials/verify`)
- [ ] **4.b** All four checks passing: signature, `validFrom`, `validUntil`, key resolution
- [ ] **4.c** Verification result codes handled: `VALID`, `INVALID`, `REVOKED`, `EXPIRED`, `UNRESOLVABLE`
- [ ] **4.d** Offline verification confirmed for `did:key` credentials (no network required)

### 5. Revocation

- [ ] **5.a** Revocation hash computation tested (`POST /v1/credentials/revocation-hash`)
- [ ] **5.b** Revocation publish working — hash appears in DeDi namespace (`POST /v1/credentials/revoke`)
- [ ] **5.c** Post-revocation verification returns `REVOKED` status
- [ ] **5.d** Revocation runbook prepared — process for connection termination, meter replacement, data correction

### 6. Consumer Delivery

- [ ] **6.a** Consumer Profile credential delivery channel decided: ☐ DigiLocker (NYCER) &nbsp; ☐ Direct VC (email/app) &nbsp; ☐ Both
- [ ] **6.b** Recurring Meter Data credential delivery to consumer confirmed and tested
- [ ] **6.c** Composite Profile delivery mechanism in place for prosumers
- [ ] **6.d** (If DigiLocker) Pull URI endpoint built, HMAC-verified, and registered on API Setu

### 7. Go-Live

- [ ] **7.a** All 6 credential types issued, verified, and revoked in staging environment
- [ ] **7.b** Monitoring active — OpenCred health, issuance error rate, DeDi publish failures alerted
- [ ] **7.c** Consumer communication ready — consumers informed of credential availability
- [ ] **7.d** Operations runbook complete — key rotation, revocation process, incident response

---

*Reference: [IES Energy Credentials Documentation](https://india-energy-stack.gitbook.io/docs/energy-credentials) · [OpenCred Docs](https://opencred.gitbook.io/docs)*
