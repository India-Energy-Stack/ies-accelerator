# Checklist — Consumer Energy Passport

*Plain-English rollout checklist for a DISCOM standing up the [Consumer Energy Passport use case](./README.md). Use it to brief leadership and align IT, commercial, and consumer-experience teams.*

---

**DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Foundations in place

The Passport reuses the [Energy Credentials](../../energy-credentials/README.md) infrastructure. If you already issue any electricity credential, you only add a new type and the identity-binding step.

- [ ] DISCOM `did:web` published and regulator's licensing pointer obtained (for `issuer.idRef`). The [IES DISCOMs Reference Registry](../../registries/README.md#reference-allow-lists-industry-coordination) entry is required only for joining the inter-DISCOM data exchange network, not for credential issuance.
- [ ] OpenCred issuer service running
- [ ] DigiLocker (or alternative wallet) integration in place

### 2. Identity binding chosen

The Passport binds the consumer's wallet DID to a verifiable government-ID reference. Decide which methods you accept and document the policy.

- [ ] Binding method(s) chosen (DigiLocker pull / Aadhaar offline KYC / in-person / DISCOM record match)
- [ ] Privacy review completed — `idRef` only, never the raw ID number

### 3. Existing systems mapped to the Passport

Map your CIS, billing, and DER / storage register fields to the [ElectricityCredential v1.2](../../schemas/ElectricityCredential/README.md) shape. Your CA numbers stay as-is — they appear as the tail of the consumer DID.

- [ ] Field mapping completed (`customerProfile`, `customerDetails`, `energyResources[]`, `consumptionProfiles[]`)
- [ ] Sample Passport issued in staging and reviewed internally
- [ ] Address enrichment (Open Location Code, GIS) added where you maintain it

### 4. Phase 1 cohort decided

Pick a starting cohort where the Passport unlocks the highest-value verifier journeys — typically rooftop-solar consumers (loans, marketplaces) or RDSS AMI rollout cohorts.

- [ ] Phase 1 consumer cohort defined
- [ ] Issuance triggers agreed (new connection, DER commissioning, on consumer request, bulk back-fill)

### 5. Lifecycle wired up

Re-issue and revoke on material change. Without this, the Passport rots in the wallet.

- [ ] Re-issuance triggered by: tariff change, sanctioned-load revision, DER added/removed, address change, service-status change
- [ ] DeDi `vc-revocation-registry` configured under your namespace
- [ ] Connection closure triggers revocation (no re-issue)

### 6. Wallet delivery live

DigiLocker Pull URI for the bulk of consumers; direct DID push for non-DigiLocker wallets.

- [ ] DigiLocker Pull URI live and tested
- [ ] Consumer notification template ready (SMS / email / app)

### 7. End-to-end loop verified

Issue → wallet receipt → verifier presentation → revocation, exercised in staging before go-live.

- [ ] Issue → wallet receipt → verify → revoke loop tested
- [ ] Selective-disclosure presentation works for the verifier kinds you target
- [ ] Monitoring and incident response in place

### 8. Production cut-over

- [ ] HTTPS endpoint live; signing keys in a secrets manager
- [ ] Monitoring of issuance, revocation, and verifier-side errors
- [ ] Customer-care trained on consumer queries
- [ ] Phased rollout plan agreed

### 9. Team nominated

- [ ] IT SPOC (name, email, phone)
- [ ] Commercial SPOC (name, email, phone)
- [ ] Authorised Signatory (name, email, phone)

---

*Once these nine items are in place, consumers in your service area hold a wallet-shareable, tamper-evident Passport that any verifier can validate offline against your published public key. See the [Consumer Energy Passport use case](./README.md) for setup detail and the [Energy Credentials chapter](../../energy-credentials/README.md) for the underlying credential infrastructure.*
