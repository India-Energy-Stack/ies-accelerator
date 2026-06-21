# Consumer Energy Passport

**A wallet-held credential, signed by you (the DISCOM), that binds a consumer's identity to their connection, meter, sanctioned load, tariff category, and DER / storage assets. Any verifier validates it offline — no callback to you.**

You issue it. The consumer carries it in [DigiLocker](../../glossary.md#digilocker) or a DID wallet. Banks, marketplaces, regulators, subsidy portals, and consented apps verify it from your published public key.

---

## What you build, end-to-end

Six concrete steps take a DISCOM from "no Passport today" to "issuing Passports to every customer":

1. **Publish your issuer identity** — your `did:web` and signing key are published as `did.json` on a domain you control. You also need the regulator's licensing pointer (for `issuer.idRef`). Listing in the [IES DISCOMs Reference Registry](../../registries/README.md#reference-allow-lists-industry-coordination) is **not** required for credential issuance; it is the trust boundary for the inter-DISCOM data exchange network and becomes relevant when you join that network.
2. **Run OpenCred** — the same service you run for any electricity credential.
3. **Map your CIS / billing / DER register** to the [ElectricityCredential v1.2](../../schemas/ElectricityCredential/README.md) shape — this is the schema underneath the Passport.
4. **Decide your identity-binding method** — how you link the consumer's wallet DID to a verifiable government-ID reference.
5. **Issue Passports** through OpenCred's `POST /v1/credentials/issue`.
6. **Deliver to wallets** — DigiLocker Pull URI for the bulk of customers; direct DID-push for the rest.

Each step links into the building block that owns the detail.

---

## Building blocks used

| Block | What it does for this use case | Where it lives |
|---|---|---|
| [Identifiers and Addressing](../../identifiers/README.md) | The Passport carries the consumer's wallet DID, your asset/meter/connection DIDs, and an `idRef` to a government identity reference (never the raw number). Your existing CA numbers stay as-is — they appear as the tail of the consumer DID. | `did:web:<dedi-host>:<your-namespace>:consumers:<CA-number>` |
| [Registries and Directories](../../registries/README.md) | Your `did:web` and current public key are resolved through DeDi. Revocation status lives in your `vc-revocation-registry`. | `dedi.global` / your namespace |
| [Energy Credentials](../../energy-credentials/README.md) | OpenCred signs, verifies, and revokes the Passport. The Passport is a W3C VC 2.0 carrying the [ElectricityCredential v1.2](../../schemas/ElectricityCredential/README.md) subject plus an `identityBinding` block. | OpenCred + `ElectricityCredential/v1.2` |
| [Data Exchange](../../data-exchange/README.md) | **Optional.** Not used for wallet delivery. Comes in only when a third-party app pulls the Passport over Beckn from your BPP — same flow you use for [Smart Meter Data Exchange](../smart-meter-data-exchange/README.md). | Only when a third party pulls |

---

## What's in the Passport

A W3C Verifiable Credential 2.0 of type `["VerifiableCredential", "ConsumerEnergyPassport"]`. Its subject is the [ElectricityCredential v1.2](../../schemas/ElectricityCredential/README.md) shape plus the Passport's identity-binding block:

```
credentialSubject
├── id                  (consumer wallet DID — did:key / did:jwk)
├── identityBinding     (Passport-specific — see below)
├── customerProfile     (customerNumber, idRef, energyResources[])
├── customerDetails     (PII — fullName, installationAddress, serviceConnectionDate)
└── consumptionProfiles[] (per-meter sanctionedLoad, tariffCategoryCode, ...)
```

`energyResources[]` covers the meter and every asset behind it (solar, battery, EV charger, inverter, DT). `consumptionProfiles[]` carries the per-meter regulatory profile (`sanctionedLoad`, `tariffCategoryCode`, `serviceStatus`, ...). Full field tables and a worked example live in the [ElectricityCredential v1.2 README](../../schemas/ElectricityCredential/README.md).

### identityBinding (Passport-specific)

Elevates the consumer's identity reference to first-class status. Always present in the Passport (optional in plain `ElectricityCredential`).

| Field | What it is |
|---|---|
| `subjectDid` | The consumer's wallet DID — must equal `credentialSubject.id` |
| `idRef` | Reference to a government identity (e.g. masked Aadhaar) — see [IdRef](../../schemas/ElectricityCredential/README.md). Carry the **reference**, never the raw ID number. |
| `bindingMethod` | `AADHAAR_OFFLINE_KYC` / `DIGILOCKER_PULL` / `IN_PERSON_VERIFICATION` / `DISCOM_RECORD_MATCH` |
| `bindingDate` | When the binding was established |

---

## Steps in detail

### 1. Publish your issuer identity

**Minimum bar.** Host your DID document (`did.json`) at a URL you control — either on your own website (e.g. `https://ies.<discom-domain>/.well-known/did.json`) or on a DeDi runtime. Domain ownership is what proves you are the DISCOM; the document carries your current public key.

**Recommended only when joining the inter-DISCOM data exchange network.** Cross-list your identity in the [IES DISCOMs Reference Registry](../../registries/README.md#reference-allow-lists-industry-coordination). The Passport works without this row — credential trust flows from your `did:web` signature plus the regulator's `issuer.idRef`. The IES-registry entry is what places you inside that network's trust boundary (cross-DISCOM portability lookups, network-policy allowlists). [Registries — step-by-step](../../registries/README.md#step-by-step-claim-your-dedi-namespace-and-create-registries) is the how-to.

### 2. Run OpenCred

Single Docker container (`ghcr.io/nfh-trust-labs/opencred/opencred-server`) holding your signing key, plus a thin integration service you write that pulls from CIS, billing, and your DER register. If you have followed the [Energy Credentials Deployment](../../energy-credentials/onboarding.md) guide, skip this step.

### 3. Map your existing systems to the Passport shape

You do not need new tables. You need read access from your integration service to the systems that already hold this data:

| Where in the Passport | Pulled from |
|---|---|
| `customerProfile.customerNumber` | CIS / billing — your existing CA number |
| `customerProfile.energyResources[]` (METER) | CIS / billing for the meter |
| `customerProfile.energyResources[]` (SOLAR_PV / BESS / EV_CHARGER / …) | Your DER, net-metering, and storage registers |
| `customerDetails` (PII) | CIS — name, installation address |
| `consumptionProfiles[]` | CIS — sanctioned load, tariff category, premises/connection type |
| `identityBinding` | DigiLocker pull or your existing KYC record |

The [ElectricityCredential v1.2](../../schemas/ElectricityCredential/README.md) schema lists every field and its CIM alignment. v1.2 also accepts optional admin fields on each `energyResources[]` entry (`serialNumber`, `inspection`, `aggregator`) and on each `consumptionProfile` (`serviceStatus`) — use them if you already maintain the data.

### 4. Decide your identity-binding method

Pick one (or several) and document it for your privacy review:

| Method | What it looks like |
|---|---|
| `DIGILOCKER_PULL` | Consumer logs into DigiLocker; you mint a wallet DID from the verified Aadhaar pull. Simplest for new consumers. |
| `AADHAAR_OFFLINE_KYC` | Consumer-supplied offline-KYC XML; you verify the UIDAI signature. |
| `IN_PERSON_VERIFICATION` | Branch-counter or doorstep verification; the binding record names the verifying officer. |
| `DISCOM_RECORD_MATCH` | Back-fill from your existing KYC on the CA — useful for bulk first issuance. |

Only carry the `idRef` (masked Aadhaar reference). Never carry the raw 12-digit number.

### 5. Issue the Passport

```
POST /v1/credentials/issue
{
  "type": ["VerifiableCredential", "ConsumerEnergyPassport"],
  "credentialSubject": { ...  /* see schema link above */ }
}
```

Post-process the returned credential to inject the full `issuer` block (`id` + `name` + `idRef`) per the [issuance pattern](../../energy-credentials/issuance.md). Use `proofFormat: "vc-jwt"` (the bootcamp default).

### 6. Deliver

| Channel | When | Status |
|---|---|---|
| **DigiLocker Pull URI** | The bulk of Indian customers. You publish a Pull URI; DigiLocker fetches the Passport when the consumer logs in. See [DigiLocker Integration](../../energy-credentials/digilocker-integration.md). | Available |
| **Direct DID push** | Consumers using non-DigiLocker wallets — you push to their DID service endpoint. | Available |
| **Direct download from your website** | Consumer signs into your portal and downloads the Passport JSON / VC-JWT. Simplest path for self-serve consumers who do not have a wallet handy. | Available |
| **In-app download** | The DISCOM's mobile or web app fetches and stores the Passport on behalf of the consumer. | To come — UX, signing-key custody, and re-issuance triggers still being worked out |

---

## Lifecycle

Re-issue the Passport and revoke the previous one when a material fact changes. Revocation is hash-based via your DeDi `vc-revocation-registry` — see [Core Concepts → Revocation](../../energy-credentials/concepts.md).

| Trigger | What changes |
|---|---|
| Tariff category change | `consumptionProfiles[].tariffCategoryCode` |
| Sanctioned-load revision | `consumptionProfiles[].sanctionedLoad` |
| Rooftop solar / battery / EV charger commissioned | New `energyResources[]` entry (with topology via `parentResources[]`) |
| Asset decommissioned | Entry removed |
| Address change | `customerDetails.installationAddress` |
| Connection suspended | `consumptionProfiles[].serviceStatus = "suspended"` and re-issue |
| Connection closed | Revoke; do not re-issue |

---

## How a verifier uses it

A verifier (bank, marketplace, subsidy portal) receives the Passport JSON from the consumer's wallet, then:

1. Reads `issuer.id` and resolves your `did:web` to your current public key.
2. Reads `issuer.idRef` (the regulator's licensing pointer) and confirms with the regulator that the licence is valid.
3. Verifies the `proof` locally — no network call to you.
4. Checks `credentialStatus` against your DeDi revocation registry.
5. Reads only the fields it needs (see [Selective Disclosure](#appendix-selective-disclosure)).

Walkthrough for verifier integrators: [Energy Credentials → Verification](../../energy-credentials/verification.md).

---

## Optional: third-party pull over Beckn

When a third-party app needs the Passport on the consumer's behalf without going through the wallet, it becomes a [Smart Meter Data Exchange](../smart-meter-data-exchange/README.md)-style BAP and pulls from your BPP — the same Beckn flow, with the consumer's [Consumer Meter Digest](../consumer-meter-digest/README.md) (or a `MeterDataRequestCredential`-shaped consent) attached at `confirm`. No new protocol surface.

---

## References

- [Checklist](./checklist.md) — plain-English rollout checklist for leadership
- [ElectricityCredential v1.2 — schema](../../schemas/ElectricityCredential/README.md) — the subject shape underneath the Passport
- [Energy Credentials chapter](../../energy-credentials/README.md) — OpenCred, issuance, verification, DigiLocker
- [Data Exchange chapter](../../data-exchange/README.md) — used only for the optional third-party pull
- [Identifiers and Addressing](../../identifiers/README.md) — DID grammar, how your CA numbers stay intact

---

## Appendix

### A1. Why a wallet-held credential

Today a consumer who needs to prove "facts about their electricity service" — opening a green-loan account, registering a rooftop installation, claiming a subsidy, listing a flat, signing up as an EV charging host — chases PDF bills, sanctioned-load letters, and portal screenshots. Each verifier has to trust the document; the consumer has to chase you for fresh paperwork.

The Passport replaces that loop with one signed credential. Verifiers check your signature against your published public key in milliseconds — no DISCOM API call, no shared database. The consumer presents only the fields a given verifier needs.

### A2. Identifier reuse — your CA number stays intact

Issuing Passports does **not** require renumbering anything. The consumer's existing CA number stays as the literal `customerNumber` string inside the credential; asset codes (meters, transformers) are wrapped as path segments on your DISCOM's own `did:web` — e.g. `did:web:ies.tpddl.in:assets:meter:<meter-slno>`. See [Identifiers and Addressing](../../identifiers/README.md).

### A3. Selective disclosure

SD-JWT-VC lets a verifier ask for, and the wallet release, only specific claims. Three minimum-disclosure presentations are being formalised in the IES profile:

| Presentation | Reveals | Use case |
|---|---|---|
| `passport-loan` | `identityBinding`, `customerDetails.fullName`, `consumptionProfiles[].sanctionedLoad`, generation assets | Green-loan / energy-efficiency loan |
| `passport-marketplace` | Meter ID, DER assets, storage assets | DER / V2G marketplace |
| `passport-subsidy` | `identityBinding`, `consumptionProfiles[].tariffCategoryCode`, `premisesType` | Government subsidy portal |

OpenCred ships SD-JWT-VC; see the [OpenCred docs](https://opencred.gitbook.io/docs).

### A4. Open items

- The exact SD-JWT-VC claim grouping for the three presentations is being finalised in the IES profile.
- Cross-DISCOM portability when a consumer moves between licence areas — the agreed pattern is: the new DISCOM issues a fresh Passport, the old DISCOM revokes the prior one. Cross-DISCOM linking is intentionally out of scope.
