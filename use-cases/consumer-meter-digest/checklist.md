# Consumer Meter Digest — Use-case Checklist

*The Digest is a holder-bound [MeterDataCredential v0.6](../../schemas/MeterDataCredential/v0.6/README.md) issued on consumer demand. Run the base credential-issuance checklist first; this page captures the use-case-specific items on top.*

---

## Step 0 — Base credential issuance is in place

Complete [Energy Credentials — Onboarding Checklist](../../checklists/energy-credentials-checklist.md) Phases 1–2 (foundations, issue / verify / revoke).

## Step 1 — MDM read path

- [ ] Read access to your MDM tested for the granularities you intend to support (`RAW_15M`, `DAILY`, `MONTHLY`, derived summaries)
- [ ] Maximum-range policy decided (e.g. 24 months for `MONTHLY`, 90 days for `RAW_15M`)
- [ ] Latency budget understood — most consumer use cases need a Digest in seconds, not minutes

## Step 2 — Consumer-pull endpoint catalogued

- [ ] A Beckn `DatasetItem` describing the consumer-pull endpoint published on your BPP (`accessMethod: INLINE`, the Digest delivered inline)
- [ ] `requiredCredential` set so only consumers holding a valid [Consumer Energy Passport](../consumer-energy-passport/README.md) (or a minimal customer credential) can call it
- [ ] `granularityOptions` and `maxRange` populated to match Step 1's policy

## Step 3 — Issuance shape

- [ ] Integration service sets `credentialSubject.id` to the consumer's wallet DID
- [ ] `schemaId` is `MeterDataCredential/v0.6`
- [ ] `validUntil` set short — 24h for loan portals, up to 7d for less time-sensitive flows
- [ ] Schema validation passes against [`MeterDataCredential/v0.6`](../../schemas/MeterDataCredential/v0.6/README.md)

## Step 4 — Wallet delivery wired

- [ ] DigiLocker pull tested end-to-end → [DigiLocker delivery](../../energy-credentials/digilocker.md)
- [ ] At least one direct DID-push path tested for non-DigiLocker wallets
- [ ] Consumer sees the Digest in their wallet within the latency budget from Step 1

## Step 5 — Verifier interop

- [ ] Verification flow rehearsed with at least one verifier (bank / marketplace / housing society / EV-charger installer)
- [ ] If you support derived `summary` outputs, the schema and human-readable description shared with verifiers up front
- [ ] Revocation flow tested — even though Digests typically expire faster than they would need revocation

## Team

- [ ] **IT SPOC** — owns MDM read path and BPP catalogue entry
- [ ] **Customer ops SPOC** — owns wallet support and consumer experience
- [ ] **Governance / Compliance SPOC** — owns the data-disclosure policy (what the consumer can pull, with what granularity, and how often)

---

*Once these steps are complete, consumers can pull a signed, verifier-friendly snapshot of their own meter data into their wallet on demand — and any third party can verify it offline against your published key.*
