# Consumer Energy Passport

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

Everything else (`customerProfile`, `customerDetails`, `energyResources[]`, `consumptionProfiles[]`, `issuer`, `proof`, revocation) is identical to any other ElectricityCredential v1.2.

The `type` array stays `["VerifiableCredential", "ElectricityCredential"]` — no new VC type is introduced.

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
| [Identifiers and Addressing](../../identifiers/README.md) | DISCOM's `did:web`; consumer's wallet `did:key`; asset / meter / connection DIDs that appear inside the credential |
| [Energy Credentials](../../energy-credentials/README.md) | The single home for signing, verifying, and revoking — including the [Consumer Energy Passport variant](../../energy-credentials/README.md#credential-variants) under "Credential variants" |
| [Holder binding](../../identifiers/README.md#appendix-f--binding-the-credential-to-a-holder-identity) | Wallet-DID binding pattern; presentation-time challenge / VP proof |
| [DigiLocker delivery](../../energy-credentials/digilocker.md) | The bulk delivery channel for Indian consumers; for many use cases DigiLocker's Aadhaar pull also acts as the identity-binding step |

## What you actually do

1. Set up the DISCOM `did:web` and run OpenCred → [Identifiers — Step-by-step](../../identifiers/README.md#step-by-step-publish-your-didweb-and-run-opencred-locally).
2. Decide your identity-proofing method (DigiLocker pull, offline-KYC XML, in-person KYC, record-match) and document it for privacy review.
3. Issue the Passport via [Energy Credentials — Issue your first credential](../../energy-credentials/README.md#issue-your-first-credential), setting `credentialSubject.id` to the wallet DID and populating `customerProfile.idRef` with the government-ID reference.
4. Deliver into the consumer's DigiLocker or wallet → [DigiLocker delivery](../../energy-credentials/digilocker.md).
5. Wire revocation into the same flow you use for any v1.2 credential.

## Selective disclosure

The Passport is a regular VC, so any selective-disclosure profile your wallet supports (SD-JWT-VC is the typical choice in 2026) works. The DISCOM is not in the disclosure loop — the wallet chooses which fields to present to each verifier.

## Operational checklist

See [Energy Credentials — Onboarding checklist](../../checklists/energy-credentials-checklist.md). The Passport adds:

- [ ] Identity-proofing-at-issuance procedure documented and approved
- [ ] Wallet/DigiLocker integration tested end-to-end
- [ ] Selective-disclosure presentation profile agreed with the first set of verifiers

## References

- [ElectricityCredential v1.2 schema](../../schemas/ElectricityCredential/v1.2/README.md) — the schema this use case rides on
- [Energy Credentials — Credential variants](../../energy-credentials/README.md#credential-variants) — where the Passport variant is documented
- [Identifiers — Holder binding patterns](../../identifiers/README.md#appendix-f--binding-the-credential-to-a-holder-identity)
- [DigiLocker delivery](../../energy-credentials/digilocker.md)
