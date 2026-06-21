# Energy Credentials — Onboarding Checklist

*A practical sequence for getting from zero to issuing your first signed credential. Each item links to the section in [Energy Credentials](../energy-credentials/README.md) (or its sister chapters) that walks the step. There is no separate field-level checklist; if you need field detail, follow the link.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Phase 1 — Foundations

- [ ] Domain selected; decision made on apex vs. subdomain and on path layout → [Identifiers — What you'll need](../identifiers/README.md#what-youll-need)
- [ ] OpenCred-friendly signing key generated; private key in KMS / HSM (software PEM only for dev) → [Energy Credentials — Signing-key sources](../energy-credentials/README.md#signing-key-sources)
- [ ] OpenCred container running; `/v1/health` returns `signingKeyLoaded: true` → [Identifiers — Run OpenCred](../identifiers/README.md#3-run-opencred-in-didweb-mode)
- [ ] `did.json` published at `https://<your-domain>/.well-known/did.json`; `curl` returns the expected DID → [Identifiers — Publish the file](../identifiers/README.md#5-publish-the-file)
- [ ] DeDi namespace claimed and **domain-verified** → [Registries — Step-by-step](../registries/README.md#step-by-step-claim-your-dedi-namespace-and-create-registries)
- [ ] OpenCred has auto-created its four registries; `/v1/health` reports `dediConfigured: true` → [Energy Credentials — Prerequisites](../energy-credentials/README.md#prerequisites)

## Phase 2 — Issue and revoke

- [ ] Confirm the issuer DID OpenCred reports → [Step 1](../energy-credentials/README.md#1-confirm-the-issuer-did-opencred-reports)
- [ ] First ElectricityCredential v1.2 issued (bearer style) → [Step 2](../energy-credentials/README.md#2-issue)
- [ ] Verify returns `valid: true` → [Step 3](../energy-credentials/README.md#3-verify)
- [ ] Revocation publishes; status flips → [Step 4](../energy-credentials/README.md#4-revoke)
- [ ] Smoke test wired into CI → [Step 5](../energy-credentials/README.md#5-smoke-test)
- [ ] Integration service appends `issuer.name` (and `issuer.idRef` if you cite a regulator) on egress; re-signs if your flow needs a single signed artefact → [Step 2 — three things worth noting](../energy-credentials/README.md#2-issue)

## Phase 3 — Decide variant(s) you'll issue

- [ ] Decide which credential variants you will issue → [Credential variants](../energy-credentials/README.md#credential-variants)
  - Bearer ElectricityCredential v1.2
  - Consumer Energy Passport (ElectricityCredential v1.2 + holder binding + `customerProfile.idRef`) → [Use case](../use-cases/consumer-energy-passport/README.md)
  - B2B MeterDataCredential v0.6 (telemetry to a DISCOM)
  - Consumer Meter Digest (MeterDataCredential v0.6 + holder binding, short `validUntil`) → [Use case](../use-cases/consumer-meter-digest/README.md)
  - MeterDataRequestCredential v0.1 (right-to-ask credential at Beckn `confirm`)
- [ ] For holder-bound variants: choose binding pattern → [Identifiers — Appendix F](../identifiers/README.md#appendix-f--binding-the-credential-to-a-holder-identity)
- [ ] Identity-proofing-at-issuance procedure documented (challenge-sign for wallet DIDs, OTP for phone, DigiLocker grant otherwise)

## Phase 4 — Production hardening

- [ ] Signing key in HSM / Cloud KMS (AWS / Azure / GCP) → [Energy Credentials — Signing-key sources](../energy-credentials/README.md#signing-key-sources)
- [ ] Schema validation in your integration service before `POST /v1/credentials/issue` → [Schema validation](../energy-credentials/README.md#schema-validation)
- [ ] Key-rotation runbook in place → [Key rotation](../energy-credentials/README.md#key-rotation)
- [ ] Reverse-proxy + TLS in front of OpenCred (never expose `:3100` directly) → [Reverse proxy + TLS](../energy-credentials/README.md#reverse-proxy--tls)
- [ ] Backups of `did.json`, KMS key handle, and DeDi credentials
- [ ] DigiLocker delivery configured if applicable → [DigiLocker delivery](../energy-credentials/digilocker.md)

## Phase 5 — Data exchange (optional, only if joining Beckn)

- [ ] Beckn subscriber registry published → [Identifiers — Appendix E](../identifiers/README.md#appendix-e--joining-a-beckn-network-subscriber-registry-on-the-beckn-fabric)
- [ ] IES Secretariat has referenced your subscriber into the relevant network registry → [Registries — How to apply](../registries/README.md#how-to-apply-for-an-ies-listing)
- [ ] ONIX configured with `allowedNetworkIDs` for the right environment → [Identifiers — Step 7](../identifiers/README.md#step-7--configure-your-onix-to-accept-the-right-networks-allowednetworkids)

## Team

- [ ] **IT SPOC** nominated (name, email, phone) — operates OpenCred, owns key rotation
- [ ] **Governance / Compliance SPOC** nominated — approves what gets published, owns regulator-pointer setup

---

*Once these phases are complete, your organisation is issuing signed, revocable credentials that any standards-compliant verifier on the IES network can validate offline.*
