# Consumer Energy Passport

**In a hurry?** Jump to the [Checklist](#checklist). For the standards basis and full field schedule, see the **[Overview](../../use-cases-overview/consumer-energy-passport.md)**.

**The Consumer Energy Passport is an [ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md) issued holder-bound to a consumer's wallet.** It is not a new credential type — it is *how* the existing v1.2 credential is shaped, issued, and delivered when the consumer is the audience.

A DISCOM signs it. The consumer carries it in DigiLocker or a DID wallet. Banks, marketplaces, regulators, subsidy portals, and consented apps verify it offline using the DISCOM's published `did.json`.

---

## Why this use case exists

Consumers carry paper attestations of their connection details — sanctioned load, tariff category, asset list — for KYC at banks, rooftop-solar marketplaces, EV-charger installers, housing societies, and subsidy portals. Every recipient calls or emails the DISCOM to confirm. The Passport replaces that loop with a credential the verifier checks offline, without contacting you.

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

## DigiLocker integration (DocType `NYCER`)

For Indian consumers, DigiLocker is the bulk delivery channel. The Passport travels as DocType **`NYCER`** through the DigiLocker **Pull URI** mechanism: the consumer searches for the credential, DigiLocker calls your endpoint, your endpoint calls OpenCred to issue the signed v1.2 credential, and DigiLocker stores it. The structures below are the current NYCER shapes; the full delivery flow (API Setu registration, HMAC verification, CIS lookup, the OpenCred issue and package calls, error handling) is in [DigiLocker delivery](../../how-you-implement-ies/digilocker.md).

### Endpoint

```
POST https://{your-domain}/digilocker/pulluri
Content-Type: application/xml
x-digilocker-hmac: <Base64(HMAC-SHA256(api_key, request_body))>
```

Verify the HMAC before any processing; reject with HTTP 401 if invalid. Register the endpoint on API Setu with DocType `NYCER`, `UDF1 Label = Consumer Number`, `UDF2 Label = Registered Mobile Number`.

### Inbound request — `PullURIRequest` (NYCER)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIRequest ver="3.0"
                ts="2026-04-01T10:30:00+05:30"
                txn="TXN-20260401-001"
                orgId="discom">
  <DocDetails>
    <DocType>NYCER</DocType>
    <DigiLockerId>7a3f9b2c-1e4d-4f8a-b6c2-0d5e8f1a2b3c</DigiLockerId>
    <UDF1>DISCOM-2025-001234567</UDF1>   <!-- consumer number -->
    <UDF2>9876543210</UDF2>             <!-- registered mobile number -->
    <FullName>Priya Sharma</FullName>    <!-- optional, from DigiLocker profile -->
  </DocDetails>
</PullURIRequest>
```

Echo `ts` and `txn` in the response. `UDF1` is the primary CIS lookup key; `UDF2` is secondary verification; DigiLocker validates `FullName` against your response's `IssuedTo`.

### Identity binding — the DigiLocker ID

NeGD requires the `DigiLockerId` from the request to be carried inside the issued credential's identity binding. Populate `customerProfile.idRef`:

```python
holder_idref = {
    "issuedBy":  "did:web:digilocker.gov.in",
    "subjectId": f"digilocker.gov.in:{digilocker_id}",   # the <DigiLockerId> from the request
}
```

This is exactly the identity-proofing step from the setup list above — for DigiLocker delivery, the Aadhaar-backed pull *is* the proofing.

### Outbound response — `PullURIResponse`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIResponse ver="3.0" ts="{ts}" txn="{txn}" orgId="discom">
  <ResponseStatus Status="1" ts="{ts}" txn="{txn}"/>
  <DocDetails>
    <DocType>NYCER</DocType>
    <URI>{uri}</URI>
    <IssuedTo>{issued_to}</IssuedTo>
    <ValidFrom>{valid_from}</ValidFrom>
    <ValidTo>{valid_to}</ValidTo>
    <DocContent format="pdf">{pdf_b64}</DocContent>
    <VcContent format="json-ld">{vc_b64}</VcContent>
    <VcType>application/ld+json</VcType>
  </DocDetails>
</PullURIResponse>
```

| Field | Description |
|---|---|
| `URI` | `{issuer_id}-NYCER-{consumerNo}` — e.g. `in.gov.discom-NYCER-100000012345`. The trailing doc-id segment is required (NeGD rejects a URI ending at the DocType), and the org segment must equal your registered API Setu `issuer_id`. Keyed on consumer number alone, so a refresh overwrites the last — correct for a slow-changing connection credential. |
| `DocContent` | Base64-encoded PDF — rendered with a **separate** `POST /v1/credentials/package` call (`formats: ["pdf"]`); an inline `packageFormats` field on the issue body is silently ignored |
| `VcContent` | Base64-encoded W3C VC JSON-LD — the signed ElectricityCredential v1.2 as issued, proof intact |
| `VcType` | `application/ld+json` — required by NeGD immediately after `VcContent`; a response without it is rejected |

For a full, validated v1.2 payload (the `credentialSubject` that goes inside `VcContent`), see the [Schedule I example](examples/schedule-i-example.json). For errors, return `Status="0"` with a message in `ResponseStatus` — see [DigiLocker delivery — error format](../../how-you-implement-ies/digilocker.md#error-response-format).

## Selective disclosure

The Passport is a regular VC, so any selective-disclosure profile your wallet supports (SD-JWT-VC is the typical choice) works. The DISCOM is not in the disclosure loop — the wallet chooses which fields to present to each verifier.

## Checklist

**Step 0 — Prerequisites**

- [ ] Register your organisation in the DeDi directory and create your `did:web` identity — see [Setting up Register](../../how-you-implement-ies/setup-register.md)
- [ ] Stand up your Beckn ONIX adapter and connect it to the network — see [Setting up Discover & Exchange](../../how-you-implement-ies/setup-exchange.md)
- [ ] Pass the basic conformance check — see [Conformance Checklist](../../how-you-implement-ies/conformance.md)

**Step 1 — base issuance in place.**

- [ ] Complete the [Issuing Credentials setup checklist](../../how-you-implement-ies/issue-credentials.md#checklist)

**Step 2 — identity proofing.**

- [ ] Method chosen (DigiLocker pull / AADHAAR_OFFLINE_KYC / in-person / DISCOM record match)
- [ ] Privacy review completed; procedure tested with one consumer

**Step 3 — wallet delivery.**

- [ ] DigiLocker Pull URI registered for DocType `NYCER` → [DigiLocker integration](#digilocker-integration-doctype-nycer) above and [DigiLocker delivery](../../how-you-implement-ies/digilocker.md)
- [ ] Direct DID-push tested for one non-DigiLocker wallet (where relevant)
- [ ] A freshly issued Passport reaches a wallet end-to-end

**Step 4 — issuance shape.**

- [ ] `credentialSubject.id` = wallet DID; `customerProfile.idRef` = verified government-ID *reference* (not the raw number)
- [ ] `validUntil` set to a sensible horizon (re-issued on material change)
- [ ] Schema validation passes against [ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md)

**Step 5 — verifier interop.**

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
