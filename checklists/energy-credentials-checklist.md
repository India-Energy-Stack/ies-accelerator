# India Energy Stack
## IES Electricity Credentials
### DISCOM Readiness Checklist

**Name of DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Sub-profiles being populated (single `CustomerCredential` per meter):**
&nbsp; ☐ `customerProfile` (always) &nbsp; ☐ `customerDetails` &nbsp; ☐ `consumptionProfiles[]`
&nbsp; ☐ `generationProfiles[]` &nbsp; ☐ `storageProfiles[]`

---

### 1. Infrastructure Setup

- [ ] **1.a** OpenCred service deployed (`ghcr.io/nfh-trust-labs/opencred/opencred-server:latest`) and `/v1/health` returns `ready: true, signingKeyLoaded: true`. (`dediConfigured: false` is normal until 1.d is done.)
- [ ] **1.b** Signing key configured — method chosen: ☐ Self-generated ECDSA P-256 PEM (recommended for dev) &nbsp; ☐ DSC import (PFX/PEM) &nbsp; ☐ Cloud KMS (AWS/Azure/GCP) &nbsp; ☐ Hardware token
- [ ] **1.c** Issuer DID established and noted: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  - For dev: `did:key` derived from a self-generated PEM, read via `GET /v1/keys`
  - For production: `did:web:<your-domain>` with `.well-known/did.json` published over HTTPS
- [ ] **1.d** DeDi namespace registered and accessible (`dedi.global`); `OPENCRED_DEDI_*` env vars set; `dediConfigured: true` in `/v1/health`
- [ ] **1.e** `credentialStatus` block embedding confirmed — revocation hash included in issued VCs with `type: "dedi"`, `statusPurpose: "revocation"`, and `statusListCredential` set

### 2. Credential Schema

- [ ] **2.a** Built-in `electricity/v1` schema confirmed available in `GET /v1/schemas`
- [ ] **2.b** Field mapping completed from CIS / NMS / MDM into `credentialSubject`:
  - `customerProfile` (required): `customerNumber`, `meterNumber`, `meterType` (enum), optional `idRef`
  - `customerDetails`: `fullName`, `installationAddress` (beckn Location shape), `serviceConnectionDate` (ISO 8601 with timezone)
  - `consumptionProfiles[]`: `premisesType`, `connectionType`, `sanctionedLoadKW`, `tariffCategoryCode`
  - `generationProfiles[]`: `generationType`, `capacityKW`, `commissioningDate`, optional `assetId` / `manufacturer` / `modelNumber`
  - `storageProfiles[]`: `storageCapacityKWh`, `powerRatingKW`, `commissioningDate`, optional `storageType` / `assetId`
- [ ] **2.c** Issuer object enrichment configured in integration service — `issuer.name` and `issuer.idRef` (regulatory registration) injected on egress, since OpenCred only emits the DID string
- [ ] **2.d** Customer external ID strategy decided — `customerProfile.idRef` uses `issuedBy` (DID of authority, e.g. `did:web:uidai.gov.in`) + masked `subjectId`. Full Aadhaar / ID number is **never** in the payload.
- [ ] **2.e** Proof format chosen: ☐ `vc-jwt` (recommended for built-in `electricity/v1`) &nbsp; ☐ `data-integrity` (only with a custom-registered clean-context schema) &nbsp; ☐ `sd-jwt-vc` (selective disclosure)

### 3. Credential Issuance

- [ ] **3.a** Single-credential issuance tested (`POST /v1/credentials/issue`) — returns `HTTP 200` with a signed VC carrying `type: ["VerifiableCredential", "CustomerCredential"]`
- [ ] **3.b** Signed VC validated — `proof` block present, `credentialStatus` embedded when `revocationRegistryUrl` is passed
- [ ] **3.c** Re-issue + revoke flow tested for material changes (tariff change, DER commissioning, meter swap, etc.)
- [ ] **3.d** Batch issuance working — CSV upload, column mapping into sub-profiles, ZIP output (`POST /v1/credentials/batch`)
- [ ] **3.e** Export formats tested: ☐ JSON &nbsp; ☐ PDF &nbsp; ☐ QR code (PNG)

### 4. Credential Verification

- [ ] **4.a** Verification tested (`POST /v1/credentials/verify`). The `credential` field is always a string: for `vc-jwt` send the compact JWT; for `data-integrity` send the JSON-stringified VC.
- [ ] **4.b** Response checks all `passed: true`. Names vary by proof format: `signature / vc-jwt-claims / date` for vc-jwt; `signature / notBefore / expiry / keyResolution` for data-integrity. Treat `valid: true` + `code: "VALID"` as the contract.
- [ ] **4.c** Verification result codes handled: `VALID`, `INVALID`, `REVOKED`, `EXPIRED`, `UNRESOLVABLE`
- [ ] **4.d** Offline verification confirmed for `did:key` credentials (no network required)

### 5. Revocation

- [ ] **5.a** Revocation hash computation tested (`POST /v1/credentials/revocation-hash`) — pass the **full signed VC including `proof`**, not a stripped copy
- [ ] **5.b** Revocation publish working — hash appears in DeDi namespace (`POST /v1/credentials/revoke`)
- [ ] **5.c** Post-revocation verification returns `REVOKED` status
- [ ] **5.d** Revocation runbook prepared — process for connection termination, meter replacement, asset decommissioning, data correction

### 6. Consumer Delivery

- [ ] **6.a** Delivery channel decided: ☐ DigiLocker (NYCER) &nbsp; ☐ Direct VC (email/app) &nbsp; ☐ Both
- [ ] **6.b** (If DigiLocker) Pull URI endpoint built, HMAC-verified, and registered on API Setu
- [ ] **6.c** Holder DID strategy decided — per-credential `did:key`, wallet-presented DID, or stable mapping in CIS

### 7. Go-Live

- [ ] **7.a** Issue → verify → revoke loop confirmed in staging
- [ ] **7.b** Monitoring active — OpenCred health, issuance error rate, DeDi publish failures alerted
- [ ] **7.c** Consumer communication ready — consumers informed of credential availability
- [ ] **7.d** Operations runbook complete — key rotation, revocation process, incident response

---

*Reference: [IES Electricity Credentials Documentation](https://india-energy-stack.gitbook.io/docs/energy-credentials) · [OpenCred Docs](https://opencred.gitbook.io/docs)*
