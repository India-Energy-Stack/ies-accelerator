# India Energy Stack
## IES Electricity Credentials
### DISCOM Readiness Checklist

**Name of DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Sub-profiles being populated (single `CustomerCredential` per meter):**
&nbsp; ☐ `customerProfile` (always) &nbsp; ☐ `customerDetails` &nbsp; ☐ `consumptionProfiles[]`
&nbsp; ☐ `generationProfiles[]` &nbsp; ☐ `storageProfiles[]`

---

### 1. Infrastructure Setup (OpenCred + DeDi combo)

- [ ] **1.a** DeDi namespace credentials in hand (base URL, `OPENCRED_DEDI_AUTH_TYPE`, API key or bearer pair, namespace ID) — this is part of the default setup, not an optional later phase
- [ ] **1.b** OpenCred service deployed (`ghcr.io/nfh-trust-labs/opencred/opencred-server:latest`) with `OPENCRED_DEDI_*` env vars set, and `/v1/health` returns `ready: true, signingKeyLoaded: true, dediConfigured: true`
- [ ] **1.c** Signing key configured — method chosen: ☐ Self-generated ECDSA P-256 PEM (recommended for dev) &nbsp; ☐ DSC import (PFX/PEM) &nbsp; ☐ Cloud KMS (AWS/Azure/GCP) &nbsp; ☐ Hardware token
- [ ] **1.d** Issuer DID established and noted (with the `#fragment` stripped from `GET /v1/keys`): \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  - For dev: `did:key` derived from a self-generated PEM
  - For production: `did:web:<your-domain>` with `.well-known/did.json` published over HTTPS, or `OPENCRED_DEDI_HOST_DID_DOC=true` to let DeDi host the DID document
- [ ] **1.e** (Optional) DID document published to DeDi via `POST /v1/keys/publish` — confirms `did:web` discovery fallback works for verifier partners
- [ ] **1.f** `credentialStatus` block embedding confirmed — revocation hash included in issued VCs with `type: "dedi"`, `statusPurpose: "revocation"`, and `statusListCredential` set

### 2. Credential Schema

- [ ] **2.a** Built-in `electricity/v1` schema confirmed available in `GET /v1/schemas`
- [ ] **2.b** Field mapping completed from CIS / NMS / MDM into `credentialSubject`:
  - `customerProfile` (required): `customerNumber`, `meterNumber`, `meterType` (enum), optional `idRef`
  - `customerDetails`: `fullName`, `installationAddress` (beckn Location shape), `serviceConnectionDate` (ISO 8601 with timezone)
  - `consumptionProfiles[]`: `premisesType`, `connectionType`, `sanctionedLoadKW`, `tariffCategoryCode`
  - `generationProfiles[]`: `generationType`, `capacityKW`, `commissioningDate`, optional `assetId` / `manufacturer` / `modelNumber`
  - `storageProfiles[]`: `storageCapacityKWh`, `powerRatingKW`, `commissioningDate`, optional `storageType` / `assetId`
- [ ] **2.c** *(Optional — only if you cite a regulator)* Regulator's licensing pointer obtained — the regulator's `did:web` (for `issuer.idRef.issuedBy`) and your regulator-issued licence identifier (for `issuer.idRef.subjectId`). `issuer.idRef` is optional per the v1.2 schema and W3C VC 2.0; omit for pilots or non-regulated issuers. No IES-side DISCOM registry entry is required to issue credentials. (Joining the inter-DISCOM data exchange network separately requires a DISCOM-reference-registry entry — see [Identifiers and Addressing → Appendix E](../identifiers/README.md#appendix-e--joining-a-beckn-network-subscriber-registry-on-the-beckn-fabric).)
- [ ] **2.d** Issuer object enrichment configured in integration service — `issuer.name` always injected on egress (OpenCred only emits the DID string); `issuer.idRef` (`issuedBy: <regulator-did-web>`, `subjectId: <regulator-domain>:<discom-licence-id>`) injected only when you cite a regulator.
- [ ] **2.e** Customer external ID strategy decided — `customerProfile.idRef` uses `issuedBy` (DID of authority, e.g. `did:web:uidai.gov.in`) + masked `subjectId`. Full Aadhaar / ID number is **never** in the payload.
- [ ] **2.f** Proof format chosen: ☐ `vc-jwt` (recommended for built-in `electricity/v1`) &nbsp; ☐ `data-integrity` (only with a custom-registered clean-context schema) &nbsp; ☐ `sd-jwt-vc` (selective disclosure)

### 3. Credential Issuance

- [ ] **3.a** Single-credential issuance tested (`POST /v1/credentials/issue`) — returns `HTTP 200` with a signed VC carrying `type: ["VerifiableCredential", "CustomerCredential"]`
- [ ] **3.b** Signed VC validated — `proof` block present, `credentialStatus` embedded when `revocationRegistryUrl` is passed
- [ ] **3.c** Re-issue + revoke flow tested for material changes (tariff change, DER commissioning, meter swap, etc.)
- [ ] **3.d** Batch issuance working — CSV upload, column mapping into sub-profiles, ZIP output (`POST /v1/credentials/batch`)
- [ ] **3.e** Export formats tested: ☐ JSON &nbsp; ☐ PDF &nbsp; ☐ QR code (PNG)

### 4. Credential Verification

- [ ] **4.a** Verification tested (`POST /v1/credentials/verify`). The `credential` field is always a string: for `vc-jwt` send the **compact JWS string** (`.proof.jwt`), **not** the stringified envelope; for `data-integrity` send the JSON-stringified VC; for `sd-jwt-vc` send the compact `~`-separated token. PDF input also supported via `Content-Type: application/pdf` (v1.3.0+).
- [ ] **4.b** Response checks all `passed: true`. Treat `valid: true` + `code: "VALID"` as the contract. The advisory `keyRotation` and `registryAnchor` checks (when present) do not flip `valid` and should not gate acceptance.
- [ ] **4.c** Verification result codes handled: `VALID`, `INVALID`, `REVOKED`, `EXPIRED`, `UNRESOLVABLE`, `CONTEXT_MISSING`
- [ ] **4.d** Offline verification confirmed for `did:key` credentials (no network required)
- [ ] **4.e** Tamper test executed — flipping a character of the JWS signature (or editing a field for data-integrity) returns `valid: false`
- [ ] **4.f** Verifier partners know about the **silent-skip-on-revocation** behaviour — a verifier without DeDi configured will not check revocation and a revoked VC will verify as `VALID`

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
