# Basic Checklist — Consumer Meter Digest

*A plain-English, conceptual checklist for a DISCOM enabling the [Consumer Meter Digest use case](./consumer-meter-digest.md) — the consumer-pull flow where a consumer requests their own meter readings as a signed credential they can hand to any third party. Use it to brief leadership and align IT, MDMS, and consumer-experience teams.*

---

**DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Confirm the foundational pieces are in place

The Consumer Meter Digest sits on top of three things you already have or are setting up: a credential issuer (OpenCred), a data-exchange adapter, and a connection to your MDMS. Confirm each is ready before scoping this use case.

- [ ] DISCOM registered in the IES DISCOMs reference registry
- [ ] OpenCred issuer service running (used for `CustomerCredential` already)
- [ ] Data-exchange adapter (BPP) live or sandboxed
- [ ] MDMS read access available to the BPP

### 2. Decide what consumers can request

Pick the granularities you will offer in Phase 1 — typically a 12-month **monthly summary** is the simplest starting point. Decide the maximum periods (e.g. 90 days for raw 15-minute readings, 24 months for monthly).

- [ ] Granularity options decided (raw / daily / monthly / summary types)
- [ ] Maximum period per granularity decided
- [ ] Refusal cases documented (suspended account, fraud hold, etc.)

### 3. Define how the consumer authorises the request

A consumer's request must be authenticated. Choose what proof of identity / right-to-the-meter the consumer presents — typically the [Consumer Energy Passport](./consumer-energy-passport.md) or a basic `CustomerCredential` issued by you.

- [ ] Required-credential type decided
- [ ] Wallet (DigiLocker or DID-enabled app) recommended to consumers

### 4. Publish the consumer-pull catalogue entry

Publish a catalogue entry the consumer's wallet can target with `confirm`, declaring the supported granularities, the maximum period, and the required credential.

- [ ] Catalogue entry published
- [ ] Per-request rate limits / fair-use policy documented

### 5. Wire up Digest minting

When a request arrives, the BPP queries MDMS for the requested period and asks OpenCred to mint a short-lived `ConsumerMeterDigest` credential. Decide the validity window for the issued Digest (typically 1 to 7 days).

- [ ] BPP → MDMS query path tested
- [ ] OpenCred issues the Digest with correct subject DID, period, and granularity
- [ ] `validUntil` policy decided (e.g. 7 days for monthly summary)
- [ ] Data quality block populated correctly (coverage %, estimated %)

### 6. Test the end-to-end flow

Run the full loop: a wallet sends `confirm`, the BPP issues the Digest, the wallet receives it, and a sample verifier validates the signature against your registry entry.

- [ ] End-to-end test from wallet to Digest delivery succeeds
- [ ] Sample verifier validates issuer signature and DeDi revocation status
- [ ] Refusal paths tested (no credential, expired credential, out-of-scope meter, period exceeds max)

### 7. Production deployment

Deploy with the basics any production service needs — HTTPS, secrets management for signing keys, monitoring, on-call.

- [ ] HTTPS endpoint live; signing keys in a secrets manager
- [ ] Monitoring of issuance volume, error rates, and average latency
- [ ] Operations runbook in place (key rotation, MDMS outage, surge handling)

### 8. Consumer communication and rollout

Most of the consumer's experience happens in their wallet, but they need to know the Digest exists and what it's for. Plan rollout messaging and a help path.

- [ ] Consumer-facing explainer published (website / app / bill insert)
- [ ] Customer-care team trained on common questions
- [ ] Phased rollout plan agreed (pilot consumer cohort → full rollout)

### 9. Nominate your team

Identify three roles: an **IT point of contact** for the technical build, a **Commercial / consumer-experience point of contact** for the rollout, and an **Authorised Signatory** who approves the Digest issuance policy.

- [ ] IT SPOC nominated (name, email, phone)
- [ ] Commercial SPOC nominated (name, email, phone)
- [ ] Authorised Signatory nominated (name, email, phone)

---

*Once these nine items are in place, consumers can pull their own meter data on demand as a signed, wallet-shareable credential. See the [Consumer Meter Digest use case](./consumer-meter-digest.md) for the detailed setup and the [credential schema](../energy-credentials/consumer-meter-digest.md) for the data shape.*
