# Consumer Meter Digest

**In a hurry?** Jump to the [Checklist](#checklist). For the standards basis and full field schedule, see the **[Overview](../../use-cases-overview/consumer-meter-digest.md)**.

**The Consumer Meter Digest is a [MeterDataCredential v0.6](../../schemas/MeterDataCredential/v0.6/README.md) issued, on consumer demand, holder-bound to the consumer's wallet, carrying their own meter readings for a specified period.** It is not a new credential type — it is *how* an existing MeterDataCredential is configured when a consumer (rather than another DISCOM or AMISP) is the audience.

The Digest gives a consumer a portable, signed, verifier-friendly bundle of their telemetry — for a loan application, a rooftop-solar quote, a tariff comparison, a marketplace listing, a housing-society compliance check — without those parties having to phone the DISCOM.

---

## Why this use case exists

Consumers regularly need to share their actual electricity-consumption pattern. Today they print PDFs of monthly bills and email scans. Verifiers have no way to confirm the bill is real and unaltered, so most of them call the DISCOM anyway. The Digest replaces that loop with a credential the verifier can check offline against the DISCOM's published key.

## How it differs from a B2B MeterDataCredential

Same schema, same issuance pipeline. Three issuance-time differences:

| Concern | B2B MeterDataCredential v0.6 | Consumer Meter Digest |
|---|---|---|
| Triggered by | Beckn `confirm` from a DISCOM consumer-pull | Consumer request (often via DigiLocker or a consented wallet app) |
| `credentialSubject.id` | absent — bearer; the receiving DISCOM is the implicit subject | **set** to the consumer's wallet DID |
| `validUntil` | days to weeks | **hours to days** — Digests are point-in-time snapshots |

The schema body — `profileType`, `meterRefs`, `intervalPeriod` / `timePeriod`, `intervals` / `readings` (raw `INTERVAL`/`DAILY`/`MONTHLY` profiles), `validationStatus`, issuer, proof — is identical to any other MeterDataCredential v0.6. Derived summary aggregates are downstream analytics, not schema fields. The `type` array stays `["VerifiableCredential", "MeterDataCredential"]` — no new VC type is introduced.

## Actors and flow

| Role | Who | What they do |
|---|---|---|
| **Holder** | Consumer | Initiates the request from their wallet / DigiLocker; stores the returned Digest; presents it to verifiers of their choosing |
| **Issuer** | DISCOM | Pulls the relevant readings from its MDM, signs the Digest, delivers it back into the consumer's wallet |
| **Verifier** | Bank, marketplace, energy app, housing society, EV-charger installer | Reads the Digest; resolves the DISCOM's `did:web` and (if cited) the regulator's licensing pointer to validate; reads the `intervals`/`readings` (any summary is downstream analytics, not part of the credential) |

Granularity options today: `DAILY`, `MONTHLY`, or `INTERVAL` (15-minute data, expressed as `profileType: INTERVAL` with `intervalPeriod.duration: PT15M`). Derived summary aggregates, where offered, are downstream analytics rather than schema fields. Maximum period typically 24 months for `MONTHLY`, 90 days for 15-minute `INTERVAL` data.

## Building blocks

| Block | Used for |
|---|---|
| [Identifiers and Addressing](../../what-ies-provides/register.md) | DISCOM's `did:web`; consumer's wallet `did:key`; meter and connection DIDs that anchor the Digest |
| [Energy Credentials](../../what-ies-provides/energy-credentials/README.md) | Issuance, signing, verification, revocation — including the [Consumer Meter Digest variant](../../what-ies-provides/energy-credentials/README.md#credential-variants) under "Credential variants" |
| [Data Exchange](../../what-ies-provides/exchange.md) | If the consumer-pull endpoint is fronted by your BPP over Beckn, the BAP/BPP machinery is the same as [Smart Meter Data Exchange](../smart-meter-data-exchange/README.md) — only the trigger (consumer, not DISCOM) and the `validUntil` differ |
| [DigiLocker delivery](../../how-you-implement-ies/digilocker.md) | The dominant delivery channel into the consumer's wallet |

## Setup: Register → Discover → Exchange

1. **Register.** The consumer must hold a credential proving the right to request data for this meter — typically a [Consumer Energy Passport](../consumer-energy-passport/README.md) (holder-bound ElectricityCredential v1.2) or a minimal customer credential.
2. **Discover.** Catalogue a "consumer-pull" endpoint on your BPP that accepts a request bearing that credential and returns a MeterDataCredential v0.6 → [Setup Exchange](../../how-you-implement-ies/setup-exchange.md).
3. **Exchange.** Issue the Digest via [Energy Credentials — Issue your first credential](../../how-you-implement-ies/issue-credentials.md#id-2.6-issue-your-first-credential), setting `credentialSubject.id` to the consumer's wallet DID, `schemaId` to `ies/meter-data-credential/v0.6`, and `validUntil` to a short window matching the use case (24h for loan portals, up to 7d for non-time-sensitive flows).
4. Deliver to the consumer's wallet — [DigiLocker delivery](../../how-you-implement-ies/digilocker.md), or directly to a known DID inbox if the wallet exposes one.
5. Revocation rarely matters in practice (Digests typically expire faster than they would need revocation), but the same DeDi-hash revocation flow is available if you need it.

## DigiLocker integration (DocType `MPLTR`)

For Indian consumers, DigiLocker is the dominant delivery channel. NeGD has allotted **`MPLTR`** (Meter Document) as the DocType for the Consumer Meter Digest; it registers as an additional record on the **same Pull URI endpoint** a DISCOM already runs for the Consumer Energy Passport (`NYCER`) — one handler, branched by `DocType`. The structures below are the current MPLTR shapes; the full delivery flow (API Setu registration, HMAC verification, the OpenCred issue and package calls, the open asks to DigiLocker) is in [DigiLocker delivery](../../how-you-implement-ies/digilocker.md).

### Endpoint

```
POST https://{your-domain}/digilocker/pulluri
Content-Type: application/xml
x-digilocker-hmac: <Base64(HMAC-SHA256(api_key, request_body))>
```

Verify the HMAC before any processing; reject with HTTP 401 if invalid. Register the DocType on API Setu with `UDF1 Label = Consumer Number`, `UDF2 Label = Statement Period` (e.g. `2026-05` or `last-12-months`), `UDF3 Label = Registered Mobile Number`.

### Inbound request — `PullURIRequest` (MPLTR)

The period travels as a UDF, so the consumer can pull a chosen window:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIRequest ver="3.0"
                ts="2026-05-15T10:00:00+05:30"
                txn="TXN-20260515-042"
                orgId="discom">
  <DocDetails>
    <DocType>MPLTR</DocType>
    <DigiLockerId>7a3f9b2c-1e4d-4f8a-b6c2-0d5e8f1a2b3c</DigiLockerId>
    <UDF1>DISCOM-2025-001234567</UDF1>   <!-- consumer number -->
    <UDF2>last-12-months</UDF2>          <!-- statement period: YYYY-MM, a range, or a keyword -->
    <UDF3>9876543210</UDF3>             <!-- registered mobile number -->
    <FullName>Priya Sharma</FullName>
  </DocDetails>
</PullURIRequest>
```

`UDF2` accepts `YYYY-MM`, a range, or a keyword like `last-12-months`; a recurring pull with the current month fetches the latest statement. Validate the period and bound it to the scope the originating request authorised.

### Outbound response — `PullURIResponse`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<PullURIResponse ver="3.0" ts="{ts}" txn="{txn}" orgId="discom">
  <ResponseStatus Status="1" ts="{ts}" txn="{txn}"/>
  <DocDetails>
    <DocType>MPLTR</DocType>
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

`DocContent` is the base64 rendered statement PDF (produced with a separate `POST /v1/credentials/package` call, `formats: ["pdf"]`); `VcContent` is the base64 signed `MeterDataCredential` JSON-LD, proof intact; `VcType` must be `application/ld+json`, immediately after `VcContent` — NeGD rejects a response without it.

### The document key — period in the URI

This is the one structural difference from the Passport. `NYCER` is keyed on the consumer number alone, so a refresh overwrites the last — correct for a connection credential. The Digest is a statement series: put the **period into the URI** so every statement coexists as a distinct document:

```python
# NYCER — overwrite on refresh (correct for a connection credential)
uri = f"in.gov.discom-NYCER-{consumer.consumer_number}"

# MPLTR — period in the key, so every statement coexists
uri = f"in.gov.discom-MPLTR-{consumer.consumer_number}-{period}"   # period e.g. "2026-05" or "2025-05_2026-04"
```

URI uniqueness is managed issuer-side; treating each period-keyed URI as a distinct, independently listable/deletable document was agreed in principle with DigiLocker on the 12 June 2026 call, with written confirmation still owed — see [DigiLocker delivery — the ask to DigiLocker](../../how-you-implement-ies/digilocker.md#the-ask-to-digilocker-mpltr).

### The `VcContent` payload — example twelve-month statement

The JSON-LD that travels in `VcContent` for a twelve-month `MONTHLY`-profile Digest, following the canonical [MeterDataCredential v0.6 monthly example](https://github.com/India-Energy-Stack/ies-accelerator/tree/main/schemas/MeterDataCredential/v0.6/examples) — one `MonthlyProfile` object per month, carried as an array in `meterData` (trimmed proof; first month shown in full):

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://schema.beckn.io/EnergyCredential/v2.0/context.jsonld",
    "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterDataCredential/v0.6/context.jsonld"
  ],
  "id": "urn:uuid:9b3c1f0a-2d4e-4ba8-9f1c-1e7a90c8a5d2",
  "type": ["VerifiableCredential", "MeterDataCredential"],
  "issuer": {
    "id": "did:web:ies.discom.example",
    "name": "Example State Distribution Company Limited",
    "licenseNumber": "SERC-DISCOM-2025-007"
  },
  "validFrom": "2026-05-15T10:00:00+05:30",
  "validUntil": "2027-05-15T10:00:00+05:30",
  "credentialStatus": {
    "id": "https://dedi.global/dedi/query/did:web:ies.discom.example/vc-revocation-registry",
    "type": "dediregistry",
    "statusPurpose": "revocation",
    "statusListCredential": "https://dedi.global/dedi/lookup/did:web:ies.discom.example/vc-revocation-registry"
  },
  "credentialSubject": {
    "id": "did:key:z6MkjVQ8r4f3rPuY7CG2D6Lf8WJxJBs5sjkR8d3v2Bv4nP4Z",
    "meterData": [
      {
        "@context": "https://india-energy-stack.github.io/ies-accelerator/schemas/MeterData/v0.6/context.jsonld",
        "@type": "MonthlyProfile",
        "profileType": "MONTHLY",
        "meterRefs": [
          { "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }
        ],
        "serviceDeliveryPointRefs": [
          { "scheme": "DID", "value": "did:web:ies.discom.example:connections:SDP-A-12345" }
        ],
        "timePeriod": { "start": "2025-05-01T00:00:00+05:30", "duration": "P1M" },
        "readings": [
          { "readingType": "kWh imp", "value": 391.0, "validationStatus": "VALID", "source": "METER" }
        ]
      },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-06-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 412.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-07-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 478.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-08-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 463.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-09-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 421.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-10-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 384.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-11-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 352.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2025-12-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 339.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2026-01-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 367.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2026-02-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 358.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2026-03-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 405.0 }] },
      { "@type": "MonthlyProfile", "profileType": "MONTHLY", "meterRefs": [{ "scheme": "DID", "value": "did:web:ies.discom.example:assets:meter:DISCOM-SM-2025-654321" }], "timePeriod": { "start": "2026-04-01T00:00:00+05:30", "duration": "P1M" }, "readings": [{ "readingType": "kWh imp", "value": 437.0 }] }
    ]
  },
  "proof": { "type": "Ed25519Signature2020", "proofValue": "z5wQ…" }
}
```

For raw analytics data, the same wrapper carries an `INTERVAL` profile (`PT15M` blocks, ~96 readings a day), typically preceded by a `DESCRIPTOR` profile referenced via `payloadDescriptorSetRef` — `meterData` becomes an array of profiles. Both shapes, and the full `handle_mpltr` issuance code, are in [DigiLocker delivery — issuing the Digest](../../how-you-implement-ies/digilocker.md#issuing-the-digest-meterdatacredential-v0.6).

Two open schema/rendering notes, tracked in [DigiLocker delivery](../../how-you-implement-ies/digilocker.md): `MeterDataCredential` v0.6 has no `idRef` field on `credentialSubject` yet, so NeGD's DigiLocker-ID identity binding can be rendered only into `DocContent`, not carried as a structured VC field; and configurable rendering of the statement card remains an open ask to DigiLocker.

## Checklist

**Step 0 — Prerequisites**

- [ ] Register your organisation in the DeDi directory and create your `did:web` identity — see [Setting up Register](../../how-you-implement-ies/setup-register.md)
- [ ] Stand up your Beckn ONIX adapter and connect it to the network — see [Setting up Discover & Exchange](../../how-you-implement-ies/setup-exchange.md)
- [ ] Pass the basic conformance check — see [Conformance Checklist](../../how-you-implement-ies/conformance.md)

**Step 1 — base issuance in place.**

- [ ] Complete the [Issuing Credentials setup checklist](../../how-you-implement-ies/issue-credentials.md#checklist)

**Step 2 — MDM read path.**

- [ ] Read access tested for the granularities you'll support (`DAILY`, `MONTHLY`, `INTERVAL` at `intervalPeriod.duration: PT15M`, and any downstream summary analytics)
- [ ] Max-range policy decided (e.g. 24 months for `MONTHLY`, 90 days for 15-minute `INTERVAL` data)
- [ ] Latency budget understood — consumer flows need a Digest in seconds

**Step 3 — consumer-pull endpoint.**

- [ ] Beckn `DatasetItem` for the pull endpoint published on your BPP (`accessMethod: INLINE`)
- [ ] `offerAttributes.policy.requiredCredentials` restricts callers to a valid [Consumer Energy Passport](../consumer-energy-passport/README.md) (or minimal customer credential)
- [ ] Supported granularities and maximum request range match Step 2's policy

**Step 4 — issuance shape.**

- [ ] `credentialSubject.id` = wallet DID; `schemaId` = `ies/meter-data-credential/v0.6`
- [ ] `validUntil` short — 24h for loan portals, up to 7d for less time-sensitive flows
- [ ] Schema validation passes against [MeterDataCredential v0.6](../../schemas/MeterDataCredential/v0.6/README.md) — this is repository-local structural validation; see [Conformance Checklist — What this checklist proves](../../how-you-implement-ies/conformance.md#what-this-checklist-proves-and-what-it-doesnt) for what it does and doesn't establish

**Step 5 — wallet delivery.**

- [ ] DigiLocker pull tested end-to-end for DocType `MPLTR`, period-keyed URI verified → [DigiLocker integration](#digilocker-integration-doctype-mpltr) above and [DigiLocker delivery](../../how-you-implement-ies/digilocker.md)
- [ ] One direct DID-push path tested for non-DigiLocker wallets
- [ ] Consumer sees the Digest within the Step 2 latency budget

**Step 6 — verifier interop.**

- [ ] Verification rehearsed with one verifier (bank / marketplace / housing society / EV installer)
- [ ] If you emit derived summary analytics alongside the Digest, share their schema + description with verifiers up front — these are downstream outputs, not part of the MeterDataCredential/v0.6 schema
- [ ] Revocation flow tested (even though Digests usually expire before needing it)

**Team.** [ ] IT SPOC (MDM read path + BPP catalogue) · [ ] Customer-ops SPOC (wallet support) · [ ] Governance / Compliance SPOC (data-disclosure policy)

## References

- [MeterDataCredential v0.6 schema](../../schemas/MeterDataCredential/v0.6/README.md) — the schema this use case rides on
- [Overview — Consumer Meter Digest](../../use-cases-overview/consumer-meter-digest.md) — standards basis, definitions, full field schedule
- [Energy Credentials — Credential variants](../../what-ies-provides/energy-credentials/README.md#credential-variants) — where the Digest variant is documented
- [Smart Meter Data Exchange use case](../smart-meter-data-exchange/README.md) — the B2B sibling of this consumer flow
- [DigiLocker delivery](../../how-you-implement-ies/digilocker.md)
