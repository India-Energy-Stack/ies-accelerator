# Basic Checklist — Consumer Energy Passport

*A plain-English, conceptual checklist for a DISCOM rolling out the [Consumer Energy Passport use case](./README.md) — the wallet-held credential that binds a consumer's identity to their connection, meter, sanctioned load, tariff category, and DER / storage assets. Use it to brief leadership and align IT, commercial, and consumer-experience teams.*

---

**DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Confirm the foundational pieces are in place

The Passport is issued by the same OpenCred service used for `CustomerCredential`. If you're already issuing customer credentials, no new infrastructure is needed — only a new credential type and an explicit identity binding.

- [ ] DISCOM registered in the IES DISCOMs reference registry
- [ ] OpenCred issuer service running
- [ ] DigiLocker (or alternative wallet) integration in place

### 2. Decide how you will bind consumer identity

The Passport requires an explicit binding between the consumer's wallet identity (DID) and a verifiable government-ID reference (e.g. masked Aadhaar). Choose how this binding is established for new and existing consumers.

- [ ] Binding method chosen (DigiLocker pull / offline KYC / in-person / DISCOM record match)
- [ ] Binding policy approved (what evidence is acceptable for each method)
- [ ] Privacy review completed — only references stored, never raw IDs

### 3. Map your existing data into the Passport

Work with your commercial team to map the relevant fields from CIS, billing, and the DER / storage register into the Passport's sub-profiles. The data sources are the same as for `CustomerCredential`.

- [ ] Field mapping completed (customer profile, address, consumption profile, generation profile, storage profile)
- [ ] Sample Passport issued and reviewed internally
- [ ] Address enrichment (Open Location Code, GIS) confirmed where available

### 4. Decide which consumers get a Passport in Phase 1

Decide the rollout cohort — for example, all rooftop-solar consumers first (where the Passport unlocks marketplace and loan use cases), then expand to wider segments.

- [ ] Phase 1 consumer cohort defined
- [ ] Issuance triggers agreed (new connection, DER commissioning, on consumer request, bulk back-fill)

### 5. Set up the lifecycle triggers

Set up operational triggers so the Passport is automatically re-issued and the previous one revoked when material facts change — tariff change, sanctioned-load revision, new DER, decommissioning, address change, disconnection.

- [ ] Re-issuance triggers wired to billing / DER / connection systems
- [ ] Revocation registry in DeDi configured
- [ ] Disconnection / closure path triggers revocation without re-issue

### 6. Decide delivery to the consumer's wallet

Choose how Passports reach consumers — typically DigiLocker Pull URI for the bulk of customers, with direct DID-to-DID push as a path for those using a non-DigiLocker wallet.

- [ ] Delivery channel(s) chosen
- [ ] DigiLocker Pull URI live and tested
- [ ] Notification message to the consumer drafted (SMS / email / app)

### 7. Test the full loop, then go live

Confirm a Passport can be issued, retrieved by the consumer in their wallet, presented to a sample verifier (bank or marketplace), and revoked when triggered.

- [ ] Issue → Wallet receipt → Verify → Revoke loop tested in staging
- [ ] Selective-disclosure presentation works for the verifier kinds you care about (loan / marketplace / subsidy / society)
- [ ] Monitoring and incident response in place

### 8. Production deployment and rollout

Deploy with the basics any production service needs and roll out to consumers in phases.

- [ ] HTTPS endpoint live; signing keys in a secrets manager
- [ ] Monitoring of issuance, revocation, and verifier-side errors
- [ ] Consumer communication and customer-care training ready
- [ ] Phased rollout plan agreed

### 9. Nominate your team

Identify three roles: an **IT point of contact** for the technical build, a **Commercial point of contact** for the credential content and consumer experience, and an **Authorised Signatory** who approves the Passport issuance and revocation policy.

- [ ] IT SPOC nominated (name, email, phone)
- [ ] Commercial SPOC nominated (name, email, phone)
- [ ] Authorised Signatory nominated (name, email, phone)

---

*Once these nine items are in place, consumers in your service area hold a wallet-shareable, tamper-evident Passport that any verifier can validate without contacting you. See the [Consumer Energy Passport use case](./README.md) for the detailed setup and the [Energy Credentials chapter](../../energy-credentials/README.md) for the credential infrastructure.*
