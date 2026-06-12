# Basic Checklist — Tariff Intelligence

*A plain-English, conceptual checklist for a SERC, DISCOM, or other policy authority publishing the [Tariff Intelligence use case](./README.md) — tariffs, deviation penalties, data-quality SLAs, and other rules as machine-readable, signed `IES_Policy` artefacts. Use it to brief leadership and align legal, regulatory, and IT teams.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ Policy publisher (SERC / utility) &nbsp; ☐ Policy consumer (DISCOM billing / app developer / meter)

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Decide which policies to publish

Pick the policies you will publish in Phase 1 — typically the residential and LT-commercial tariff orders are the first candidates. The same envelope later extends to deviation penalties, DR program rules, and data-quality SLAs.

- [ ] Policy types selected (`TARIFF`, `DISPATCH_GUIDE`, etc.)
- [ ] Source documents identified (the tariff order PDF, the SERC-approved schedule)

### 2. Register your organisation on the IES network

The publisher needs an entry in the relevant IES reference registry (Regulators for SERC, DISCOMs for utilities) with a signing key consumers can verify.

- [ ] Organisation registered in the appropriate reference registry
- [ ] Signing key pair generated and stored securely

### 3. Mint stable identifiers for each policy

Each policy gets a stable `policyID` (e.g. `MUM-RES-T1`, `KA-LT2-IND-TOD-2026`) — the handle every downstream system uses to refer to it. Related policies are grouped under a `programID`.

- [ ] Policy ID scheme adopted
- [ ] Program IDs defined for the regulatory programmes that group related policies

### 4. Author the policy as structured data

Convert the tariff order into the `IES_Policy` JSON-LD shape — energy slabs, time-of-day surcharges, validity window, recurrence pattern. Validate against the schema before signing.

- [ ] Policy authored in `IES_Policy` JSON-LD shape
- [ ] Schema validation passes
- [ ] Internal review confirms parity with the tariff order PDF

### 5. Sign the policy with the publisher's key

The signed bundle is the artefact downstream systems will hash-check against the registry-published public key. The signature is what gives the policy its trust.

- [ ] Signing pipeline tested (key access, signing, signature verification round-trip)
- [ ] Versioning convention agreed (new `id` per amendment, same `policyID`, explicit `replaces` link)

### 6. Publish via the data exchange

The publisher's adapter exposes the policy through its catalogue. Public-disclosure policies typically use inline delivery and settlement value `0`, so any consumer can pull them without contract.

- [ ] Catalogue entry published
- [ ] Public-disclosure access policy documented
- [ ] (Optional) Inline-policy attachment to private exchanges supported, where the policy sets the terms of that exchange

### 7. Sample-consume the policy in a billing system

Hand the published policy to a billing system or a sample app and confirm it can compute a bill (slab lookup + ToD surcharge) directly from the JSON-LD without any re-keying.

- [ ] Sample consumer ingests the policy and computes a bill
- [ ] Edge cases tested (open-ended top slab, surcharge-window wrap-around, percent vs absolute adders)

### 8. Production deployment and go-live

Deploy with the basics any production service needs and publish one real, signed tariff alongside the corresponding regulatory order.

- [ ] HTTPS endpoint live; signing keys in a secrets manager
- [ ] Monitoring and alerting active
- [ ] First real tariff published alongside the SERC order
- [ ] Amendment / republication runbook in place

### 9. Nominate your team

Identify three roles: a **Legal / regulatory point of contact** for the policy content, an **IT point of contact** for the technical publication, and an **Authorised Signatory** who approves the signed publication.

- [ ] Legal / regulatory SPOC nominated (name, email, phone)
- [ ] IT SPOC nominated (name, email, phone)
- [ ] Authorised Signatory nominated (name, email, phone)

---

*Once these nine items are in place, your tariffs (and other policies) reach DISCOM billing systems, consumer apps, and smart meters as signed, machine-readable artefacts — no PDF re-keying, no interpretation drift. See the [Tariff Intelligence use case](./README.md) for the detailed setup and the [data-exchange onboarding checklist](../../checklists/data-exchange-checklist.md) for the underlying network-onboarding steps.*
