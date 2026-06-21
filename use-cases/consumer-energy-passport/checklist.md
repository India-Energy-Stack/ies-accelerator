# Consumer Energy Passport — Use-case Checklist

*The Passport is a holder-bound [ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md). Run the base credential-issuance checklist first; this page captures the use-case-specific items on top.*

---

## Step 0 — Base credential issuance is in place

Complete [Energy Credentials — Onboarding Checklist](../../checklists/energy-credentials-checklist.md) Phases 1–2 (foundations, issue / verify / revoke).

## Step 1 — Identity proofing decided and documented

The Passport sets `credentialSubject.id` to the consumer's wallet DID and populates `customerProfile.idRef` with a government-ID reference. Both must be vouched for at issuance time — see [Identifiers — Identity-proofing at issuance](../../identifiers/README.md#before-you-bind-anything-identity-proofing-at-issuance).

- [ ] Identity-proofing method chosen — DigiLocker pull, AADHAAR_OFFLINE_KYC, in-person verification, or DISCOM record match
- [ ] Privacy review for the chosen method completed
- [ ] Procedure tested end-to-end with one consumer

## Step 2 — Wallet delivery wired

- [ ] DigiLocker Pull URI registered for the Passport → [DigiLocker delivery](../../energy-credentials/digilocker.md)
- [ ] Direct DID-push delivery tested for at least one non-DigiLocker wallet (where relevant)
- [ ] Wallet receives a freshly-issued Passport end-to-end

## Step 3 — Issuance shape

- [ ] Integration service sets `credentialSubject.id` to the consumer's wallet DID
- [ ] Integration service populates `customerProfile.idRef` with the verified government-ID reference (the reference, **not** the raw number)
- [ ] `validUntil` set to a sensible horizon (years, re-issued on material change)
- [ ] Schema validation passes against [`ElectricityCredential/v1.2`](../../schemas/ElectricityCredential/v1.2/README.md)

## Step 4 — Verifier interop

- [ ] Selective-disclosure presentation profile agreed with the first set of verifiers (SD-JWT-VC is the typical 2026 choice)
- [ ] Sample verification flow rehearsed with at least one verifier (a bank, marketplace, or subsidy portal)
- [ ] Revocation tested: revoking a Passport invalidates all presentations within minutes

## Team

- [ ] **Customer ops SPOC** — owns identity-proofing rollout
- [ ] **IT SPOC** — owns wallet-delivery integration
- [ ] **Governance / Compliance SPOC** — owns the identity-proofing privacy review

---

*Once these steps are complete, your DISCOM is issuing wallet-held, holder-bound ElectricityCredential v1.2 credentials that consumers can present anywhere on the IES network.*
