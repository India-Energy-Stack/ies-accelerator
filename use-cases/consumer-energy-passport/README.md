# Consumer Energy Passport

**A wallet-held credential, signed by the DISCOM, that binds the consumer's identity to their electricity connection, meter, sanctioned load, tariff category, and DER / storage assets — verifiable anywhere, by anyone, with no callback to the DISCOM.**

---

## Scenario

A consumer in India needs to prove "facts about their electricity service" in countless settings: opening a green-loan account at a bank, registering their rooftop solar with a marketplace, claiming a subsidy, signing up for a DR program, listing energy attributes when selling their flat, registering as an EV charging host. Today this means PDFs of electricity bills, scanned sanctioned-load letters, screenshots from DISCOM portals — each verifier has to trust the document and the consumer has to chase the DISCOM for fresh paperwork.

The Consumer Energy Passport replaces this paperwork with a single signed credential the consumer holds in their wallet (DigiLocker or a DID-enabled app). It composes the consumer's identity reference, customer profile, address, consumption profile, generation assets, and storage assets into one verifiable object. Any verifier resolves the DISCOM's public key from a public registry and validates the signature in milliseconds — no DISCOM API call, no shared database.

---

## Actors and Roles

| Role | Organisation | What they do |
|---|---|---|
| **Issuer** | DISCOM | Signs and emits the `ConsumerEnergyPassport` |
| **Holder** | Consumer | Stores it in DigiLocker or a DID wallet; presents it to verifiers |
| **Verifier** | Bank, marketplace, regulator, society, app | Validates the signature against the IES DISCOMs Reference Registry |

The Passport is fundamentally a **composite** of the existing `CustomerCredential` sub-profiles, plus a binding to the consumer's identity reference. The DISCOM does not need to deploy new infrastructure beyond what [Energy Credentials](../../energy-credentials/README.md) already prescribes.

---

## Building Blocks Used

| Block | Role in this use case |
|---|---|
| [Identifiers](../../identifiers/README.md) | The Passport carries the consumer's DID, the meter ID, the connection ID, asset IDs for each DER/battery, and an `idRef` to a government identity (Aadhaar reference, never the raw number). |
| [Registries](../../registries/README.md) | The DISCOM's `did:web` and public key are resolved through the [IES DISCOMs Reference Registry](../../registries/required-registries.md#discoms-registry). Revocation is checked via DeDi. |
| [Energy Credentials](../../energy-credentials/README.md) | The Passport schema lives here — see [Consumer Energy Passport credential](../../energy-credentials/consumer-energy-passport.md) for the full schema. Issuance and verification reuse the OpenCred service the DISCOM already runs. |
| [Data Exchange](../../data-exchange/README.md) | *Not used for issuance.* Comes in only when a third-party app pulls the Passport over Beckn from the DISCOM's BPP (an alternative to wallet pull). |

---

## What's in the Passport

The Consumer Energy Passport is a W3C Verifiable Credential 2.0 of type `ConsumerEnergyPassport`. It is a **composite** credential: its `credentialSubject` carries the same five sub-profiles as a `CustomerCredential` (customer, details, consumption, generation, storage) plus an explicit `identityBinding` linking the consumer's DID to a verifiable government-ID reference.

| Block | What it attests |
|---|---|
| `identityBinding` | Consumer DID ↔ government-ID reference (e.g. masked Aadhaar via `idRef`) |
| `customerProfile` | Customer number, meter number, meter type |
| `customerDetails` | Full name, installation address (Beckn Location shape with Open Location Code), service-connection date |
| `consumptionProfiles[]` | Premises type, connection type, sanctioned load (kW), tariff category |
| `generationProfiles[]` | DER assets — solar / wind / micro-hydro, capacity, commissioning date |
| `storageProfiles[]` | Batteries — kWh capacity, kW power rating, technology |

The full schema and a worked example live in [Energy Credentials → Consumer Energy Passport](../../energy-credentials/consumer-energy-passport.md).

---

## Setup Steps

### 1. Be a registered DISCOM issuer

Pre-requisite: the DISCOM is registered in the [IES DISCOMs Reference Registry](../../registries/required-registries.md#discoms-registry) with its `did:web` and current public key. If you are not yet registered, follow [Registry Creation](../../registries/registry-creation.md).

### 2. Run OpenCred

The Passport is issued by the same OpenCred service used for `CustomerCredential`. If you've already followed the [Energy Credentials Deployment](../../energy-credentials/onboarding.md) guide, no additional service is needed. If not, stand up OpenCred per that guide (a single Docker container holding your signing key plus a thin integration service you write).

### 3. Map your CIS + DER systems to the Passport sub-profiles

The integration service pulls:

- **Identity binding** — the consumer's DID (issued at first onboarding) plus their masked-Aadhaar `idRef`. If you don't yet capture consumer DIDs, the DigiLocker path will mint one on first delivery.
- **Customer profile** — from your CIS / billing
- **Address** — from your CIS, enriched with Open Location Code if you maintain GIS
- **Consumption profile** — sanctioned load, tariff category — from CIS / billing
- **Generation profiles** — from your DER / net-metering register
- **Storage profiles** — from your battery / storage register (if maintained; otherwise empty)

These are the same data sources you use for `CustomerCredential`. The Passport adds the explicit identity binding and the wider `type` array.

### 4. Issue the Passport

Call OpenCred's `POST /v1/credentials/issue` with the composite `credentialSubject`, then post-process the returned credential to inject the full `issuer` block (name + `idRef`) — see the issuance pattern documented at [Issuing Credentials](../../energy-credentials/issuance.md).

### 5. Deliver to the wallet

Two delivery paths:

- **DigiLocker Pull URI** — the DISCOM publishes a Pull URI; DigiLocker fetches the credential when the consumer logs in. See [DigiLocker Integration](../../energy-credentials/digilocker-integration.md).
- **Direct DID-to-DID push** — for consumers using a non-DigiLocker wallet, push the credential to their DID endpoint.

### 6. Re-issue on material change

Re-issue and revoke the previous Passport when:

| Trigger | What changes |
|---|---|
| Tariff category change | `consumptionProfiles[].tariffCategoryCode` |
| Sanctioned-load revision | `consumptionProfiles[].sanctionedLoadKW` |
| Rooftop solar commissioned | New entry in `generationProfiles[]` |
| Battery commissioned | New entry in `storageProfiles[]` |
| Asset decommissioned | Entry removed |
| Address change | `customerDetails.installationAddress` |
| Connection closure | Revoke; do not re-issue |

Revocation is hash-based via DeDi — see [Core Concepts § DeDi Revocation](../../energy-credentials/concepts.md).

---

## How a Verifier Uses It

A verifier (bank, marketplace, society) receives the Passport JSON from the consumer's wallet, then:

1. Reads `issuer.idRef` and looks up the entry in the IES DISCOMs Reference Registry.
2. Resolves the DISCOM's `did:web` to its currently published public key.
3. Verifies the `proof` signature locally — no network call to the DISCOM.
4. Checks `credentialStatus` against DeDi to confirm the credential is not revoked.
5. Reads the specific sub-profile fields it needs and proceeds.

For the verifier walkthrough, see [Energy Credentials → Verification](../../energy-credentials/verification.md).

---

## Selective Disclosure

The Passport supports SD-JWT-VC presentation so the consumer can disclose only the fields a verifier needs:

- A green-loan bank may need `consumptionProfiles[].sanctionedLoadKW` and `generationProfiles[]` only — not name or address.
- A society registering a member's rooftop solar may need `customerProfile.meterNumber` and `generationProfiles[]` only.
- A government subsidy portal may need `identityBinding` and `consumptionProfiles[].tariffCategoryCode` only.

OpenCred ships SD-JWT-VC support; see the [OpenCred docs](https://opencred.gitbook.io/docs).

---

## Open Items

- **`ConsumerEnergyPassport` credential schema** is in draft — the composite type is defined as a superset of `CustomerCredential` with an explicit `identityBinding` block. See [Energy Credentials → Consumer Energy Passport](../../energy-credentials/consumer-energy-passport.md) for the working schema.
- **Selective-disclosure profile.** The agreed set of "minimum-disclosure presentations" (loan, marketplace, subsidy, society) is being formalised — they shape the SD-JWT-VC claim grouping.
- **Cross-DISCOM portability.** Behaviour when a consumer moves between DISCOMs (issue a new Passport from the new DISCOM and revoke the prior one) is the agreed pattern; cross-DISCOM linking is intentionally not in scope.

---

## References

- [Basic Checklist](./basic-checklist.md) — plain-English rollout checklist

- [Energy Credentials → Consumer Energy Passport (schema)](../../energy-credentials/consumer-energy-passport.md)
- [Energy Credentials → Core Concepts](../../energy-credentials/concepts.md)
- [Energy Credentials → Issuance](../../energy-credentials/issuance.md)
- [Energy Credentials → DigiLocker Integration](../../energy-credentials/digilocker-integration.md)
- [Energy Credentials → Verification](../../energy-credentials/verification.md)
- [W3C VC Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/)
- [SD-JWT-VC](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/)
