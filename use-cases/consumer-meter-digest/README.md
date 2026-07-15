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

The schema body — `meterReference`, `period`, `readings` (raw `INTERVAL`/`DAILY`/`MONTHLY` profiles) or `summary` (aggregates), `dataQuality`, issuer, proof — is identical to any other MeterDataCredential v0.6. The `type` array stays `["VerifiableCredential", "MeterDataCredential"]` — no new VC type is introduced.

## Actors and flow

| Role | Who | What they do |
|---|---|---|
| **Holder** | Consumer | Initiates the request from their wallet / DigiLocker; stores the returned Digest; presents it to verifiers of their choosing |
| **Issuer** | DISCOM | Pulls the relevant readings from its MDM, signs the Digest, delivers it back into the consumer's wallet |
| **Verifier** | Bank, marketplace, energy app, housing society, EV-charger installer | Reads the Digest; resolves the DISCOM's `did:web` and (if cited) the regulator's licensing pointer to validate; reads the readings or summary |

Granularity options today: `RAW_15M` (15-minute interval data), `DAILY`, `MONTHLY`, plus derived summaries (`SUMMARY_TOTAL`, `SUMMARY_PEAK`, `SUMMARY_TOD`). Maximum period typically 24 months for `MONTHLY`, 90 days for `RAW_15M`.

## Building blocks

| Block | Used for |
|---|---|
| [Identifiers and Addressing](../../what-ies-provides/register.md) | DISCOM's `did:web`; consumer's wallet `did:key`; meter and connection DIDs that anchor the Digest |
| [Energy Credentials](../../what-ies-provides/energy-credentials/README.md) | Issuance, signing, verification, revocation — including the [Consumer Meter Digest variant](../../what-ies-provides/energy-credentials/README.md#credential-variants) under "Credential variants" |
| [Data Exchange](../../what-ies-provides/discover.md) | If the consumer-pull endpoint is fronted by your BPP over Beckn, the BAP/BPP machinery is the same as [Smart Meter Data Exchange](../smart-meter-data-exchange/README.md) — only the trigger (consumer, not DISCOM) and the `validUntil` differ |
| [DigiLocker delivery](../../how-you-implement-ies/digilocker.md) | The dominant delivery channel into the consumer's wallet |

## Setup: Register → Discover → Exchange

1. **Register.** The consumer must hold a credential proving the right to request data for this meter — typically a [Consumer Energy Passport](../consumer-energy-passport/README.md) (holder-bound ElectricityCredential v1.2) or a minimal customer credential.
2. **Discover.** Catalogue a "consumer-pull" endpoint on your BPP that accepts a request bearing that credential and returns a MeterDataCredential v0.6 → [Setup Exchange](../../how-you-implement-ies/setup-exchange.md).
3. **Exchange.** Issue the Digest via [Energy Credentials — Issue your first credential](../../how-you-implement-ies/issue-credentials.md#id-2.6-issue-your-first-credential), setting `credentialSubject.id` to the consumer's wallet DID, `schemaId` to `MeterDataCredential/v0.6`, and `validUntil` to a short window matching the use case (24h for loan portals, up to 7d for non-time-sensitive flows).
4. Deliver to the consumer's wallet — [DigiLocker delivery](../../how-you-implement-ies/digilocker.md), or directly to a known DID inbox if the wallet exposes one.
5. Revocation rarely matters in practice (Digests typically expire faster than they would need revocation), but the same DeDi-hash revocation flow is available if you need it.

## Checklist

Use-case-specific items on top of base credential issuance.

**Step 0 — base issuance in place.** Complete [Energy Credentials → Setup checklist](../../how-you-implement-ies/issue-credentials.md#checklist).

**Step 1 — MDM read path.**

- [ ] Read access tested for the granularities you'll support (`RAW_15M`, `DAILY`, `MONTHLY`, derived summaries)
- [ ] Max-range policy decided (e.g. 24 months for `MONTHLY`, 90 days for `RAW_15M`)
- [ ] Latency budget understood — consumer flows need a Digest in seconds

**Step 2 — consumer-pull endpoint.**

- [ ] Beckn `DatasetItem` for the pull endpoint published on your BPP (`accessMethod: INLINE`)
- [ ] `requiredCredential` restricts callers to a valid [Consumer Energy Passport](../consumer-energy-passport/README.md) (or minimal customer credential)
- [ ] `granularityOptions` / `maxRange` match Step 1's policy

**Step 3 — issuance shape.**

- [ ] `credentialSubject.id` = wallet DID; `schemaId` = `MeterDataCredential/v0.6`
- [ ] `validUntil` short — 24h for loan portals, up to 7d for less time-sensitive flows
- [ ] Schema validation passes against [MeterDataCredential v0.6](../../schemas/MeterDataCredential/v0.6/README.md)

**Step 4 — wallet delivery.**

- [ ] DigiLocker pull tested end-to-end → [DigiLocker delivery](../../how-you-implement-ies/digilocker.md)
- [ ] One direct DID-push path tested for non-DigiLocker wallets
- [ ] Consumer sees the Digest within the Step 1 latency budget

**Step 5 — verifier interop.**

- [ ] Verification rehearsed with one verifier (bank / marketplace / housing society / EV installer)
- [ ] If you emit derived `summary` outputs, share the schema + description with verifiers up front
- [ ] Revocation flow tested (even though Digests usually expire before needing it)

**Team.** [ ] IT SPOC (MDM read path + BPP catalogue) · [ ] Customer-ops SPOC (wallet support) · [ ] Governance / Compliance SPOC (data-disclosure policy)

## References

- [MeterDataCredential v0.6 schema](../../schemas/MeterDataCredential/v0.6/README.md) — the schema this use case rides on
- [Overview — Consumer Meter Digest](../../use-cases-overview/consumer-meter-digest.md) — standards basis, definitions, full field schedule
- [Energy Credentials — Credential variants](../../what-ies-provides/energy-credentials/README.md#credential-variants) — where the Digest variant is documented
- [Smart Meter Data Exchange use case](../smart-meter-data-exchange/README.md) — the B2B sibling of this consumer flow
- [DigiLocker delivery](../../how-you-implement-ies/digilocker.md)
