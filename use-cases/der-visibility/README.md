# DER Visibility

**In a hurry?** Jump to the [Checklist](#checklist). For the standards basis and full field schedule, see the **[Overview](../../use-cases-overview/der-visibility.md)**.

**A DISCOM publishes a per-feeder view of every distributed energy resource (rooftop solar, battery, EV charger) behind its meters — the same [ElectricityCredential v1.2](../../schemas/ElectricityCredential/v1.2/README.md) the consumer's [Energy Passport](../consumer-energy-passport/README.md) is built on, issued grid-side instead of consumer-side.**

---

## Scenario

As rooftop solar, batteries and EV charging spread, a DISCOM often cannot answer the basic question: what is connected on feeder F-02, at what capacity, where on the network, and is it controllable? DER Visibility publishes the aggregated `energyResources[]` view of one feeder, substation, or the whole licensee as a signed credential that grid operators and aggregators ingest directly — with **no consumer PII**, only the asset facts the grid needs.

It is not a new schema. ElectricityCredential v1.2 is the schema; DER Visibility is how that schema is issued when the audience is the grid, not the consumer.

## How it differs from the Consumer Energy Passport

Same schema, same issuance pipeline. Two differences:

| Concern | Consumer Energy Passport | DER Visibility |
|---|---|---|
| `credentialSubject.id` | consumer's wallet DID | the feeder / substation / licensee DID |
| `customerProfile`, `customerDetails` | populated | **omitted** — no consumer PII |

## Actors and Roles

| Role | Who | What they do |
|---|---|---|
| **Issuer** | DISCOM | Publishes the aggregated credential per locus (feeder / substation / licensee-wide), on a refresh cadence or on material change |
| **Consumer (BAP)** | Grid operator | Ingests for forecasting, planning, dispatch, outage analysis |
| **Consumer (BAP)** | Aggregator | Ingests as a discovery surface for controllable resources |

Unlike the Passport, the DER Visibility credential is **published, not held** — consumed from the DISCOM's BPP catalogue, not carried in a wallet.

## Building Blocks Used

| Block | Role in this use case |
|---|---|
| [Identifiers](../../what-ies-provides/identifiers/README.md) | Same `did:web` as the Passport; `credentialSubject.id` set to a feeder / substation / licensee DID instead of a consumer DID |
| [Energy Credentials](../../what-ies-provides/energy-credentials/README.md) | Same signing / verification / revocation pipeline as any ElectricityCredential v1.2 |
| [Data Exchange](../../what-ies-provides/data-exchange/README.md) | BPP catalogue entries published per locus; grid operators and aggregators consume as BAPs |

---

## The Dataset — `ElectricityCredential v1.2` (grid-side issuance)

`energyResources[]` populated per locus — solar, battery, EV charger, inverter, controllable load — with capacity, inspection status, equipment details, and the parent/sub-resource topology (PV and BESS → Inverter → Meter → DT). `customerProfile` and `customerDetails` are blanked.

```
Feeder F-02
 ├── DT F02-DT-15 ── 14 consumers ──┐
 ├── DT F02-DT-16 ── 22 consumers ──┤ aggregated into one
 └── DT F02-DT-17 ── 31 consumers ──┘ ElectricityCredential v1.2
                                         (energyResources[] only, no PII)
```

The credential subject scopes by locus:

| Scope | `credentialSubject.id` example |
|---|---|
| Per feeder | `did:web:ies.discom.example:assets:feeder:F02` |
| Per substation | `did:web:ies.discom.example:assets:substation:SS-11KV-12` |
| Licensee-wide | `did:web:ies.discom.example` |

---

## Setup: Register → Discover → Exchange

### 1. Register — identity reused

Same `did:web` as the Energy Passport — no new identity setup if you already issue Passports → **[Setup Register](../../how-you-implement-ies/setup-register.md)**.

### 2. Discover — grid-side catalogue

Publish a BPP catalogue entry per locus (feeder / substation / licensee-wide), `accessMethod: INLINE` → **[Setup Discovery](../../how-you-implement-ies/setup-discovery.md)**. Test grid-operator and aggregator consumers as BAPs.

### 3. Exchange — issuance shape

- Blank `customerProfile` / `customerDetails` at issuance time
- Populate `energyResources[]` from CIS / DERMS / inspection register
- Populate topology links (`parentResources`, `subResources`) where the DT mapping is known
- Validate against [ElectricityCredential v1.2 schema.json](../../schemas/ElectricityCredential/v1.2/schema.json)
- Agree and schedule a refresh cadence (typical: weekly for an active growth area, monthly otherwise, or on material change)

---

## Checklist

- [ ] Same `did:web` as the Energy Passport confirmed working
- [ ] Feeder / substation identifier convention confirmed (existing IDs wrapped in `did:web`)
- [ ] BPP catalogue entries published per locus
- [ ] Grid-operator and aggregator consumers tested as BAPs
- [ ] `customerProfile` / `customerDetails` blanked at issuance
- [ ] `energyResources[]` populated from CIS / DERMS / inspection register
- [ ] Topology links populated where known
- [ ] Schema validation passes
- [ ] Refresh cadence agreed and scheduled
- [ ] Revocation tested

**Team.** [ ] Network / planning SPOC · [ ] IT SPOC · [ ] Inspection / commissioning SPOC

---

## Open Items

- **Refresh cadence per locus** — weekly vs monthly vs on-material-change — to be tuned per pilot.
- **Aggregator binding** — the exact field and credential proof an aggregator presents to claim a resource.
- **Privacy review** — confirmation that the aggregated, PII-free issuance meets DPDP grid-side disclosure norms.

---

## References

- [ElectricityCredential v1.2 schema](../../schemas/ElectricityCredential/v1.2/README.md)
- [Overview — DER Visibility](../../use-cases-overview/der-visibility.md) — standards basis, definitions, full field schedule
- [Consumer Energy Passport](../consumer-energy-passport/README.md) — the consumer-side sibling issuance
- [Energy Credentials](../../what-ies-provides/energy-credentials/README.md)
