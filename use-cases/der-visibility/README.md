# DER Visibility

**In a hurry?** Jump to the [Checklist](#checklist). For the standards basis and full field schedule, see the **[Overview](../../use-cases-overview/der-visibility.md)**.

**A DISCOM's future, illustrative per-feeder view of every distributed energy resource (rooftop solar, battery, EV charger) behind its meters — PII-free, conceptually reusing the same `EnergyResource` and `ConsumptionProfile` building blocks that the consumer's [Energy Passport](../consumer-energy-passport/README.md) ([ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md)) composes. The only currently executable EC v1.2 path is the per-consumer Energy Passport itself.**

---

## Scenario

As rooftop solar, batteries and EV charging spread, a DISCOM often cannot answer the basic question: what is connected on feeder F-02, at what capacity, where on the network, and is it controllable?

**What is executable today.** The only currently executable ElectricityCredential v1.2 path is the per-consumer credential — the [Consumer Energy Passport](../consumer-energy-passport/README.md) — whose `credentialSubject.customerProfile.customerNumber` is a required field. See the validated [Schedule I example](../consumer-energy-passport/examples/schedule-i-example.json). A grid operator or aggregator wanting per-connection detail today would consume that credential, with consumer consent, via the same [Setup Exchange](../../how-you-implement-ies/setup-exchange.md) flow.

**A note on the aggregate (illustrative, future).** ElectricityCredential is issued per consumer connection — one `customerProfile`, one customer number — so it cannot combine multiple consumers into a feeder- or substation-level record. Each consumer keeps their own Energy Passport. A PII-free, per-locus view — an array of `EnergyResource` and `ConsumptionProfile` entries for the locus, subject to the feeder / substation / licensee DID — is described below as an **illustrative future profile**. It may conceptually reuse the same building blocks the Passport composes, but it **does not validate as EC v1.2** (which requires a single `customerProfile` / `customerNumber`), is **not a signed EC v1.2 credential**, and has **no canonical executable example** today — see [Open Items](#open-items).

## How it differs from the Consumer Energy Passport

The "DER Visibility" column below describes the illustrative future aggregate (see Scenario, above) — not an executable credential today.

| Concern | Consumer Energy Passport | DER Visibility |
|---|---|---|
| Shape | Full `ElectricityCredential v1.2`, one consumer per credential | PII-free arrays of `EnergyResource` + `ConsumptionProfile` entries, one locus per record |
| Subject | Consumer's wallet DID | The feeder / substation / licensee DID |
| `customerProfile`, `customerDetails` | Populated | **Omitted entirely** — no consumer PII, and consumers are never merged together |

## Actors and Roles

| Role | Who | What they do |
|---|---|---|
| **Issuer** | DISCOM | Publishes the aggregated record per locus (feeder / substation / licensee-wide), on a refresh cadence or on material change |
| **Consumer (BAP)** | Grid operator | Ingests for forecasting, planning, dispatch, outage analysis |
| **Consumer (BAP)** | Aggregator | Ingests as a discovery surface for controllable resources |

Unlike the Passport, the DER Visibility record is **published, not held** — consumed from the DISCOM's BPP catalogue, not carried in a wallet.

## Building Blocks Used

| Block | Role in this use case |
|---|---|
| [Identifiers](../../what-ies-provides/register.md) | Same `did:web` as the Passport; subject set to a feeder / substation / licensee DID instead of a consumer DID |
| [Energy Credentials](../../what-ies-provides/energy-credentials/README.md) | Same signing / verification / revocation pipeline used for any ElectricityCredential v1.2 building block |
| [Data Exchange](../../what-ies-provides/discover.md) | BPP catalogue entries published per locus; grid operators and aggregators consume as BAPs |

---

## The Dataset — `EnergyResource[]` + `ConsumptionProfile[]` (grid-side publication)

*Illustrative / non-normative — describes the future per-locus aggregate (see Scenario, above), not an executable credential today.*

`energyResources[]` would be populated per locus — solar, battery, EV charger, inverter, controllable load — with capacity, inspection status, equipment details, and the parent/sub-resource topology (PV and BESS → Inverter → Meter → DT). `consumptionProfiles[]` would be included where sanctioned-load / export-limit context is needed. No `customerProfile`, no `customerDetails` — these fields would never be populated for this issuance.

```
Feeder F-02
 ├── DT F02-DT-15 ── 14 consumers ──┐
 ├── DT F02-DT-16 ── 22 consumers ──┤ aggregated into one
 └── DT F02-DT-17 ── 31 consumers ──┘ future PII-free aggregate record
                                         (illustrative — energyResources[] + consumptionProfiles[], no PII)
```

The subject scopes by locus:

| Scope | Subject DID example |
|---|---|
| Per feeder | `did:web:ies.discom.example:assets:feeder:F02` |
| Per substation | `did:web:ies.discom.example:assets:substation:SS-11KV-12` |
| Licensee-wide | `did:web:ies.discom.example` |

---

## Setup: Register → Discover → Exchange

*The steps below describe the future implementation path for the illustrative per-locus aggregate, once its credential-subject shape is formalised (see Open Items). They are not executable today; for the currently executable path, follow [Issue Credentials](../../how-you-implement-ies/issue-credentials.md) for the per-consumer Energy Passport.*

### 1. Register — identity reused

Same `did:web` as the Energy Passport — no new identity setup if you already issue Passports → **[Setup Register](../../how-you-implement-ies/setup-register.md)**.

### 2. Discover — grid-side catalogue

Publish a BPP catalogue entry per locus (feeder / substation / licensee-wide), `accessMethod: INLINE` → **[Setup Exchange](../../how-you-implement-ies/setup-exchange.md)**. Test grid-operator and aggregator consumers as BAPs.

### 3. Exchange — issuance shape

- Exclude PII at issuance time — no `customerDetails`, no customer numbers; one consumer's data is never merged with another's
- Populate `energyResources[]` from CIS / DERMS / inspection register
- Populate `consumptionProfiles[]` only where sanctioned-load / export-limit context is needed
- Populate topology links (`parentResources`, `subResources`) where the DT mapping is known
- Validate against the aggregate's own credential-subject schema once formalised (not ElectricityCredential v1.2 — see Open Items)
- Agree and schedule a refresh cadence (typical: weekly for an active growth area, monthly otherwise, or on material change)

---

## Checklist

*Tracks the future implementation path for the illustrative aggregate (see Scenario, above) — not applicable until its credential-subject shape is formalised.*

- [ ] Same `did:web` as the Energy Passport confirmed working
- [ ] Feeder / substation identifier convention confirmed (existing IDs wrapped in `did:web`)
- [ ] BPP catalogue entries published per locus
- [ ] Grid-operator and aggregator consumers tested as BAPs
- [ ] PII excluded at issuance — no `customerDetails`, no customer numbers; no merging across consumers
- [ ] `energyResources[]` populated from CIS / DERMS / inspection register
- [ ] `consumptionProfiles[]` included only where sanctioned-load / export-limit context is needed
- [ ] Topology links populated where known
- [ ] Schema validation passes against the aggregate's own credential-subject schema (once formalised)
- [ ] Refresh cadence agreed and scheduled
- [ ] Revocation tested

**Team.** [ ] Network / planning SPOC · [ ] IT SPOC · [ ] Inspection / commissioning SPOC

---

## Open Items

- **Refresh cadence per locus** — weekly vs monthly vs on-material-change — to be tuned per pilot.
- **Aggregator binding** — the exact field and credential proof an aggregator presents to claim a resource.
- **Privacy review** — confirmation that the aggregated, PII-free issuance meets DPDP grid-side disclosure norms; `consumptionProfiles[]` entries are keyed by meter id (pseudonymous, not anonymous), so their inclusion belongs behind the authenticated tier where required.
- **Aggregate record shape** — ElectricityCredential requires a single `customerProfile` with one customer number, so it cannot represent a PII-free, multi-consumer aggregate. The aggregate needs its own credential-subject shape, formalised upstream through separate governance; until then it remains an illustrative future profile with no canonical executable example.

---

## References

- [ElectricityCredential v1.2 schema](../../schemas/ElectricityCredential/v1.2/README.md)
- [Overview — DER Visibility](../../use-cases-overview/der-visibility.md) — standards basis, definitions, full field schedule
- [Consumer Energy Passport](../consumer-energy-passport/README.md) — the currently executable per-consumer EC v1.2 issuance
- [Consumer Energy Passport Schedule I example](../consumer-energy-passport/examples/schedule-i-example.json) — the validated, executable EC v1.2 payload
- [Energy Credentials](../../what-ies-provides/energy-credentials/README.md)
