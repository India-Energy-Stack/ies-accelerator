# Consumer Energy Passport

**In a hurry?** Jump to the [Checklist](#checklist). For the standards basis and full field schedule, see the **[Overview](../../use-cases-overview/consumer-energy-passport.md)**.

**The Consumer Energy Passport is an [ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md) issued holder-bound to a consumer's wallet.** It is not a new credential type — it is *how* the existing v1.2 credential is shaped, issued, and delivered when the consumer is the audience.

A DISCOM signs it. The consumer carries it in [DigiLocker](../../glossary.md#digilocker) or a DID wallet. Banks, marketplaces, regulators, subsidy portals, and consented apps verify it offline using the DISCOM's published `did.json`.

---

## Why this use case exists

Consumers carry paper attestations of their connection details — sanctioned load, tariff category, asset list — for KYC at banks, rooftop-solar marketplaces, EV-charger installers, housing societies, and subsidy portals. Every recipient calls or emails the DISCOM to confirm. The Passport replaces that loop with a credential the verifier can check in milliseconds, without ever contacting you.

## How it differs from a bearer ElectricityCredential

Same schema, same issuance pipeline. Two issuance-time differences:

| Concern | Bearer ElectricityCredential v1.2 | Consumer Energy Passport |
|---|---|---|
| `credentialSubject.id` | absent — bearer; whoever holds the JSON is treated as the subject | **set** to the consumer's wallet DID (`did:key` or `did:jwk`) |
| `customerProfile.idRef` | optional | **populated** with a verifiable government-ID reference (e.g. masked Aadhaar, DigiLocker pull receipt) |

Everything else (`customerProfile`, `customerDetails`, `energyResources[]`, `consumptionProfiles[]`, `issuer`, `proof`, revocation) is identical to any other ElectricityCredential v1.2. The `type` array stays `["VerifiableCredential", "ElectricityCredential"]` — no new VC type is introduced.

## Actors and flow

| Role | Who | What they do |
|---|---|---|
| **Issuer** | DISCOM | Signs the Passport once the consumer has been identity-proofed |
| **Holder** | Consumer | Stores the Passport in DigiLocker / a DID wallet; chooses when and to whom to present |
| **Verifier** | Bank, marketplace, regulator, subsidy portal, housing society, EV-charger installer | Reads the Passport from the wallet; verifies the issuer's signature, revocation status, and the holder-binding proof |

A typical issuance happens once at customer onboarding (and then is re-issued on material change — meter swap, sanctioned-load change, DER commissioning).

## Building blocks

| Block | Used for |
|---|---|
| [Identifiers and Addressing](../../what-ies-provides/register.md) | DISCOM's `did:web`; consumer's wallet `did:key`; asset / meter / connection DIDs that appear inside the credential |
| [Energy Credentials](../../what-ies-provides/energy-credentials/README.md) | The single home for signing, verifying, and revoking — including the [Consumer Energy Passport variant](../../what-ies-provides/energy-credentials/README.md#credential-variants) under "Credential variants" |
| [Holder binding](../../how-you-implement-ies/issue-credentials.md#appendix-binding-the-credential-to-a-holder-identity) | Wallet-DID binding pattern; presentation-time challenge / VP proof |
| [DigiLocker delivery](../../how-you-implement-ies/digilocker.md) | The bulk delivery channel for Indian consumers; for many use cases DigiLocker's Aadhaar pull also acts as the identity-binding step |

## Setup: Register → Discover → Exchange

1. **Register** — set up the DISCOM `did:web` and run OpenCred → [Setup Register](../../how-you-implement-ies/setup-register.md); [Energy Credentials — Set up OpenCred](../../how-you-implement-ies/setup-register.md#id-1.2-generate-your-credential-signing-keypair).
2. Decide your identity-proofing method (DigiLocker pull, offline-KYC XML, in-person KYC, record-match) and document it for privacy review — see [Identifiers — Identity-proofing at issuance](../../how-you-implement-ies/issue-credentials.md#before-you-bind-anything-identity-proofing-at-issuance).
3. **Exchange** — issue the Passport via [Energy Credentials — Issue your first credential](../../how-you-implement-ies/issue-credentials.md#id-2.6-issue-your-first-credential), setting `credentialSubject.id` to the wallet DID and populating `customerProfile.idRef` with the government-ID reference.
4. Deliver into the consumer's DigiLocker or wallet → [DigiLocker delivery](../../how-you-implement-ies/digilocker.md).
5. Wire revocation into the same flow you use for any v1.2 credential.

## Selective disclosure

The Passport is a regular VC, so any selective-disclosure profile your wallet supports (SD-JWT-VC is the typical choice) works. The DISCOM is not in the disclosure loop — the wallet chooses which fields to present to each verifier.

## Checklist

Use-case-specific items on top of base credential issuance.

**Step 0 — base issuance in place.** Complete [Energy Credentials → Setup checklist](../../how-you-implement-ies/issue-credentials.md#checklist).

**Step 1 — identity proofing.**

- [ ] Method chosen (DigiLocker pull / AADHAAR_OFFLINE_KYC / in-person / DISCOM record match)
- [ ] Privacy review completed; procedure tested with one consumer

**Step 2 — wallet delivery.**

- [ ] DigiLocker Pull URI registered → [DigiLocker delivery](../../how-you-implement-ies/digilocker.md)
- [ ] Direct DID-push tested for one non-DigiLocker wallet (where relevant)
- [ ] A freshly issued Passport reaches a wallet end-to-end

**Step 3 — issuance shape.**

- [ ] `credentialSubject.id` = wallet DID; `customerProfile.idRef` = verified government-ID *reference* (not the raw number)
- [ ] `validUntil` set to a sensible horizon (re-issued on material change)
- [ ] Schema validation passes against [ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md)

**Step 4 — verifier interop.**

- [ ] Selective-disclosure profile agreed with the first verifiers (SD-JWT-VC typical)
- [ ] Verification rehearsed with one verifier (bank / marketplace / subsidy portal)
- [ ] Revocation tested — revoking invalidates all presentations within minutes

**Team.** [ ] Customer-ops SPOC (identity proofing) · [ ] IT SPOC (wallet delivery) · [ ] Governance / Compliance SPOC (privacy review)

## References

- [ElectricityCredential v1.2 schema](../../schemas/ElectricityCredential/v1.2/README.md) — the schema this use case rides on
- [Overview — Consumer Energy Passport](../../use-cases-overview/consumer-energy-passport.md) — standards basis, definitions, full field schedule
- [Energy Credentials — Credential variants](../../what-ies-provides/energy-credentials/README.md#credential-variants) — where the Passport variant is documented
- [Identifiers — Holder binding patterns](../../how-you-implement-ies/issue-credentials.md#appendix-binding-the-credential-to-a-holder-identity)
- [DigiLocker delivery](../../how-you-implement-ies/digilocker.md)
