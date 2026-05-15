# Basic Checklist — Energy Credentials

*A plain-English, conceptual checklist for a DISCOM rolling out Energy Credentials. Use it to brief leadership and align your IT and commercial teams. The [simple technical checklist](./energy-credentials-checklist.md) and [detailed checklist](./energy-credentials-checklist-detailed.md) cover exactly how each step is done.*

---

**DISCOM:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Set up your DISCOM as a credential issuer

Your IT team configures a secure issuer identity (a digital seal tied to your DISCOM's domain) that will sign every credential you issue. This is what proves a credential genuinely came from your DISCOM.

- [ ] Issuer identity set up and registered in the IES directory

### 2. Decide which credentials you will issue in Phase 1

Pick the customer and asset facts you want to make machine-verifiable — for example, a customer's connection details, their sanctioned load and tariff category, a rooftop-solar generation profile, a battery storage profile, or enrollment in a utility programme. Start with one or two and expand from there.

- [ ] Phase 1 credential types selected
- [ ] Source systems (CIS / NMS / MDM) identified for each type

### 3. Map your existing data to the standard credential format

Work with your commercial team to map the relevant fields from your existing systems into the standard IES credential structure. This does not change your internal systems — it produces a signed, shareable view on top of them.

- [ ] Field mapping completed for each Phase 1 credential type
- [ ] Sample credential issued and reviewed internally

### 4. Set up a way to revoke credentials when facts change

Customers move, meters get replaced, tariffs change, accounts are closed. Set up a simple revocation registry so that any verifier checking a credential can see whether it is still valid.

- [ ] Revocation registry set up
- [ ] Operational triggers documented (disconnection, meter swap, tariff change, fraud)

### 5. Decide how credentials reach the consumer

Choose how end-users receive their credentials — typically via DigiLocker, but a direct app or email channel is also supported. Confirm the integration with your chosen channel.

- [ ] Delivery channel chosen
- [ ] Integration with the chosen channel tested end-to-end

### 6. Test the full loop, then go live

Before launch, confirm that a credential can be issued, verified by an external party, and revoked — all in a working end-to-end test. Then turn it on for real consumers.

- [ ] Issue → Verify → Revoke loop tested in staging
- [ ] Monitoring and incident response in place
- [ ] Consumer communication ready

### 7. Nominate your team

Identify three roles: an **IT point of contact** for the technical build, a **Commercial point of contact** for the credential content, and an **Authorised Signatory** who approves credentials and revocations.

- [ ] IT SPOC nominated (name, email, phone)
- [ ] Commercial SPOC nominated (name, email, phone)
- [ ] Authorised Signatory nominated (name, email, phone)

---

*Once these seven items are in place, your DISCOM is ready to issue tamper-evident, machine-verifiable credentials that consumers and ecosystem participants can rely on. See the [simple](./energy-credentials-checklist.md) and [detailed](./energy-credentials-checklist-detailed.md) checklists for the technical execution path.*
