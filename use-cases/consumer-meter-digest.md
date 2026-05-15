# Consumer Meter Digest

**The consumer pulls their own granular meter readings on demand from their DISCOM as a signed credential, and shares it with a third party of their choice — bank, marketplace, energy app, society — directly from their wallet.**

---

## Scenario

Smart-meter data flows freely between the AMISP and the DISCOM. But the consumer who actually pays the bill — and whose data it is — has no clean way to put that data in front of a third party they trust. Today they screenshot bills, download messy CSVs from DISCOM portals, or grant blanket account access to apps via screen-scraping.

The Consumer Meter Digest replaces this with a request the consumer initiates from their wallet. The DISCOM returns the consumer's own meter readings (or a derived summary — monthly bill ladder, peak-time profile, last-12-months consumption) as a signed credential the consumer can hand to anyone. The recipient verifies the DISCOM's signature against the public registry and consumes the data with full confidence in its provenance.

This is the **consumer-facing dual** of [Smart Meter Data Exchange](smart-meter-data-exchange/README.md). Where that flow is bulk, machine-to-machine, and DISCOM-internal, this flow is one-meter, on-demand, consumer-mediated, wallet-shareable.

---

## Actors and Roles

| Role | Organisation | What they do |
|---|---|---|
| **Issuer** | DISCOM | Holds the canonical meter data; issues the signed Digest on consumer request |
| **Holder** | Consumer | Initiates the request from their wallet; stores the Digest; presents it to verifiers of their choosing |
| **Verifier** | Bank, marketplace, energy app, housing society, EV-charger installer | Receives the Digest from the consumer's wallet; validates the signature against the IES DISCOMs Reference Registry; consumes the data |

---

## Building Blocks Used

| Block | Role in this use case |
|---|---|
| [Identifiers](../identifiers/README.md) | The Digest references the consumer's DID, the meter ID, and the time-range it covers. The DISCOM's `did:web` is the issuer ID. |
| [Registries](../registries/README.md) | The DISCOM is looked up in the [IES DISCOMs Reference Registry](../registries/required-registries.md#discoms-registry); revocation is checked via DeDi. |
| [Energy Credentials](../energy-credentials/README.md) | The Digest is a `ConsumerMeterDigest` Verifiable Credential — see [Consumer Meter Digest credential](../energy-credentials/consumer-meter-digest.md) for the schema. Issued by the same OpenCred service the DISCOM already runs. |
| [Data Exchange](../data-exchange/README.md) | The consumer's request to the DISCOM travels over the IES Data Exchange protocol — a `confirm` from the consumer's wallet (acting as a BAP) to the DISCOM (BPP). The Digest credential rides back inside `on_status`. Same protocol surface as Smart Meter Data Exchange; only the actors and the carried payload differ. |

---

## What's in the Digest

The `ConsumerMeterDigest` is a W3C Verifiable Credential 2.0 of type `ConsumerMeterDigest`. Its `credentialSubject` carries:

| Block | What it contains |
|---|---|
| `meterReference` | Meter ID, customer number, DISCOM ID — links the Digest unambiguously to the meter |
| `period` | ISO 8601 start / end of the readings range |
| `granularity` | `RAW_15M` (raw 15-minute readings), `DAILY`, `MONTHLY`, or a derived summary type |
| `readings` | An OpenADR 3 `REPORT` block — same envelope as Smart Meter Data Exchange — when raw readings are returned |
| `summary` | Aggregates (total kWh, peak demand, ToD breakdown, monthly ladder) when a derived summary is returned |
| `dataQuality` | Coverage % and flag for any estimated/missing intervals in the range |

The full schema and a worked example live in [Energy Credentials → Consumer Meter Digest](../energy-credentials/consumer-meter-digest.md).

The Digest is a credential, not just a data dump: the DISCOM signs it, the consumer holds it, and any verifier can confirm both the readings and the issuer with no callback to the DISCOM.

---

## Setup Steps

### 1. DISCOM-side prerequisites

The DISCOM must already have:

- A registry entry in the [IES DISCOMs Reference Registry](../registries/required-registries.md#discoms-registry).
- An OpenCred service running (per [Energy Credentials Deployment](../energy-credentials/onboarding.md)) — the same instance that issues `CustomerCredential` and the Consumer Energy Passport.
- A BPP adapter exposing a "consumer-pull" catalogue entry on the IES Data Exchange (per [Data Exchange Quick Start](../data-exchange/quick-start.md)).
- A connection from the BPP to its MDMS so a consumer-pull can resolve to actual meter readings.

### 2. Wallet-side prerequisites

Consumers need a wallet that can act as a BAP — either DigiLocker (if it offers Beckn-BAP issuance flows), or a DID-enabled wallet app the DISCOM recommends. The wallet holds the consumer's DID and the keypair that authenticates them to the DISCOM.

The first time the consumer uses the wallet against the DISCOM, the consumer's [Consumer Energy Passport](consumer-energy-passport.md) (or a minimal `CustomerCredential`) is what proves they have the right to request data for that meter.

### 3. Catalogue the consumer-pull endpoint

The DISCOM publishes a catalogue entry for the Digest service:

- `descriptor.name` — e.g. *"BESCOM Consumer Meter Digest"*
- `accessMethod` — `INLINE` (Digests are small)
- `requiredCredential` — type `CustomerCredential` or `ConsumerEnergyPassport` issued by this DISCOM, with the meter ID matching the request
- `granularityOptions` — supported `granularity` values (`RAW_15M`, `DAILY`, `MONTHLY`, `SUMMARY_*`)
- `maxRange` — typically 24 months for `MONTHLY`, 90 days for `RAW_15M`

### 4. The consumer makes a request

From the wallet:

1. Consumer selects the meter and the period (e.g. *"last 12 months, monthly"*).
2. Wallet builds a Beckn `confirm` against the DISCOM's catalogue entry, including:
   - The consumer's `CustomerCredential` (or Passport) presentation as proof of right.
   - The requested `granularity` and `period`.
3. Wallet signs the message with the consumer's DID key and sends it.

### 5. The DISCOM responds

DISCOM-side:

1. BPP verifies the consumer's credential — issuer is this DISCOM, subject DID matches the BAP signer, meter is in scope, credential not revoked.
2. BPP queries MDMS for the requested period and granularity.
3. BPP calls OpenCred to mint a `ConsumerMeterDigest` credential whose `credentialSubject` is the consumer DID, populated with the requested readings or summary.
4. BPP returns `on_confirm` (acknowledgement) and then `on_status` carrying the signed Digest inline.

### 6. The consumer presents the Digest

The Digest now lives in the consumer's wallet. They share it with a verifier — bank, marketplace, society — who:

1. Resolves the DISCOM's `did:web` from the IES DISCOMs Reference Registry.
2. Verifies the Digest's signature.
3. Checks the DeDi revocation status.
4. Reads the readings or summary and proceeds.

For larger operations (e.g. a marketplace pulling Digests for many consumers), the verifier may also become a BAP against the DISCOM — but only when presenting a Digest authorisation credential issued by the consumer to the marketplace.

---

## Why a Credential, Not Just an API Pull

A bank could in principle hit a DISCOM API directly with the consumer's consent token and read CSV. Returning the data **inside a signed credential** instead gives:

- **Portability** — the Digest moves with the consumer; no per-verifier integration with each DISCOM.
- **Provenance** — every verifier sees the DISCOM's signature; the data cannot be silently altered after issue.
- **Time-bound caching** — the Digest carries `validFrom`/`validUntil`; verifiers can cache without staleness anxiety.
- **Selective disclosure** — SD-JWT-VC presentation lets the consumer reveal *"my last-12-months total kWh"* without exposing the per-interval profile.

---

## Open Items

- **`ConsumerMeterDigest` credential schema** is in draft. The envelope and the `meterReference`/`period`/`granularity` fields are stable; the summary-type taxonomy (`SUMMARY_MONTHLY_LADDER`, `SUMMARY_TOD_PROFILE`, `SUMMARY_PEAK_DEMAND`) is being formalised. See [Energy Credentials → Consumer Meter Digest](../energy-credentials/consumer-meter-digest.md).
- **Wallet UX patterns.** The agreed wallet flow (consent screens, period selectors, scope display) for triggering a Digest pull is being documented in DigiLocker integration notes.
- **Bulk / batch Digests.** A marketplace pattern for "100 consumers each authorise me to pull their Digests" is being designed; the per-consumer credential model is the foundation.
- **`IES_Report` schema finalisation** (see [Smart Meter Data Exchange § Open Items](smart-meter-data-exchange/README.md#open-items)) flows directly into this use case — the `readings` block of the Digest reuses the same OpenADR 3 envelope.

---

## References

- [Energy Credentials → Consumer Meter Digest (schema)](../energy-credentials/consumer-meter-digest.md)
- [Energy Credentials → Core Concepts](../energy-credentials/concepts.md)
- [Energy Credentials → Issuance](../energy-credentials/issuance.md)
- [Energy Credentials → Verification](../energy-credentials/verification.md)
- [Smart Meter Data Exchange](smart-meter-data-exchange/README.md) — the bulk M2M dual of this use case
- [Consumer Energy Passport](consumer-energy-passport.md) — the identity / asset Passport the consumer presents to authorise the Digest
