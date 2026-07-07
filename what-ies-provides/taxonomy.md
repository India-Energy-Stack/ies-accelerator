# Taxonomy

> **The master vocabulary of IES.** What schemas exist, what each is for, how they map to use cases, how versions evolve, and how a new schema is proposed and accepted.

The Taxonomy is the answer to two practical questions an implementer asks:

1. *"For my use case, which schemas do I need?"* — covered by the **schema map** below.
2. *"My system has a domain object IES doesn't yet cover. How do I propose a new schema?"* — covered by the **proposal flow** below.

It is also the answer to a governance question: *"Who owns these schemas, who can change them, and when?"* — answered in **Stewardship**.

---

## Schema map

Every IES schema, the domain it covers, the use cases that combine it, and its current version.

### Verifiable Credentials

W3C VC payloads — signed, durable records the holder keeps independently of IES.

| Schema | Domain | Used in | Overview | Current |
|---|---|---|---|---|
| [ElectricityCredential](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) | Static facts of a consumer connection — sanctioned load, tariff, assets behind the meter | [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md) · [DER Visibility](../use-cases/der-visibility/README.md) | [Overview](schemas-overview/electricity-credential.md) | **v1.2** |
| [MeterDataCredential](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) | Signed envelope around a MeterData payload — consumer's own readings | [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) | [Overview](schemas-overview/meter-data-credential.md) | **v0.6** |
| [MeterDataRequestCredential](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequestcredential/v0.1) | Signed proof-of-right-to-ask that a seeker presents to a meter-data provider | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) (optional) | [Overview](schemas-overview/meter-data-request-credential.md) | **v0.1** |

### Data Exchange payloads

Non-credential payloads that ride on the Beckn wire.

| Schema | Domain | Used in | Overview | Current |
|---|---|---|---|---|
| [MeterData](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) | Smart-meter telemetry (8 compact profiles: CUSTOMER, INTERVAL, DAILY, MONTHLY, BILL_DETAILS, INSTANTANEOUS, EVENT, ALARM) | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) · [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) (payload) | [Overview](schemas-overview/meter-data.md) | **v0.6** |
| [MeterDataRequest](https://india-energy-stack.gitbook.io/docs/schemas/meterdatarequest/v0.6) | Query / capabilities shape for meter-data requests | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) | [Overview](schemas-overview/meter-data-request.md) | **v0.6** |
| [ArrFiling](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5) | Aggregate Revenue Requirement filings — DISCOM to SERC | [DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md) | [Overview](schemas-overview/arr-filing.md) | **v0.5** |
| [OutageNotification](https://india-energy-stack.gitbook.io/docs/schemas/outagenotification/v0.1) | Planned + unplanned outage notification — pull (catalogue) and push (CAP) | — no IES use-case guide yet | [Overview](schemas-overview/outage-notification.md) | **v0.1** |
| `IES_Policy` *(upstream)* | Tariffs and policy-as-code | [Tariff Intelligence](../use-cases/tariff-intelligence/README.md) | — | in progress |

### External — DEG schemas IES uses

Canonical at [schema.beckn.io](https://schema.beckn.io); the field reference is mirrored in **[External Schemas](../schemas/external/README.md)**.

| Schema family | Domain | Used in |
|---|---|---|
| `P2PTrade` / `DEGContract` / `EnergyTradeOffer` / `EnergyTradeDelivery` / `DiscomLedgerProvider` / `BecknTimeSeries` (mirror covers the core trade tables; `EnergyTradeDelivery` and `DiscomLedgerProvider` are defined only at schema.beckn.io) | Peer-to-peer energy trade | [P2P Energy Trading](../use-cases/p2p-energy-trading/README.md) |
| `DemandFlexNeed` / `DemandFlexBuyOffer` / `DemandFlexPerformance` + shared `EnergyResource` / `DEGContract` / `RevenueFlow` / `BecknTimeSeries` | Demand-side flexibility procurement and M&V | — not yet an IES use case |

---

## Standards precedence

Every schema in IES records, per field, the standard that governs it. The IES order of preference is fixed:

1. **Bureau of Indian Standards (IS)** — e.g. IS 16444 for smart meters, IS 15959 for DLMS/COSEM.
2. **CEA Regulations** and the **Indian Electricity Grid Code (IEGC)**.
3. **International Electrotechnical Commission (IEC)** — CIM (IEC 61968 distribution, IEC 61970 transmission/DER), IEC 62056 (DLMS/COSEM).
4. **Institute of Electrical and Electronics Engineers (IEEE)** — IEEE 1547 (DER interconnection), IEEE 2030.5 (Smart Energy Profile), IEEE 1366 (SAIDI/SAIFI), IEEE 1782 (outage causes).

The precedence is recorded as the machine-readable `x-standards-precedence` map at the root of every JSON Schema: `{ IS:1, CEA:2, IEGC:2, IEC:3, IEEE:4 }`. Per-field standard provenance is in the `x-standard` annotation on every property.

Where no Indian standard applies, an international one is used and the gap is recorded — see the **§6 Where Indian Standards Do Not Yet Exist** section in every schema readme and use-case guide.

---

## Versioning

Every schema lives at `schemas/<Family>/v<version>/` with its own:

- `attributes.yaml` — the OpenAPI 3.1 source of truth (hand-edited).
- `schema.json` — compiled JSON Schema (Draft 2020-12) for validation.
- `context.jsonld` — JSON-LD context for semantic resolution.
- `vocab.jsonld` — RDF vocabulary with CIM alignments.
- `examples/` — worked payloads.
- `README.md` — auto-generated field reference (sections 8–11 + annexures) following the **[IES Documentation Template](../use-cases/README.md#how-each-guide-is-organised)**.

A change is **non-breaking** (additive, optional fields, new enum values) if it keeps backward compatibility — the same minor version may absorb it. A change is **breaking** (field rename, removal, type change, semantics change) if it doesn't — a new version is published with a fresh `README.md`. Old versions stay reachable; clients pin a version explicitly.

---

## Proposing a new schema (or a change)

When your use case has a domain object IES doesn't cover yet, the path is:

1. **Check the map above** — confirm no existing schema (with optional extension) already covers it.
2. **Draft the schema** in `attributes.yaml` shape following the **[IES Documentation Template](../use-cases/README.md#how-each-guide-is-organised)**.
3. **Open a PR** against this repository. Include: scope statement, basis of standards (with the IS → CEA → IEC → IEEE precedence), example payloads.
4. **Review by the IES Cell** — the governance body under the Central Electricity Authority. Reviews check standards alignment, field overlap with existing schemas, and use-case fit.
5. **Acceptance** publishes a versioned `v0.1` and adds the schema to the map above.

The detailed governance framework will be notified by the IES Cell separately. For interim questions, contact the [IES Secretariat](registries/README.md#how-to-apply-for-an-ies-listing).

---

## Stewardship

The schemas are stewarded by the **IES Cell**, the governance body being constituted under the Central Electricity Authority with representation from across the sector. The Cell owns the specifications, decides what is added or changed, and publishes each version. Operationally:

- **Schema source of truth** — this repository, under `schemas/`.
- **Canonical hosting** — `india-energy-stack.github.io/ies-accelerator/schemas/...`.
- **Versioning policy** — semver-light (`v<major>.<minor>`), with non-breaking changes within a minor version and breaking changes triggering a new minor.
- **Deprecation** — old versions stay queryable; the schema map and the canonical URL flag the active version.

---

## Where this fits

The Taxonomy is the master view of **Exchange**. To see how the three IES steps fit together: **[Register](register.md)** → **[Discover](discover.md)** → **[Exchange](exchange.md)**.

To pick a use case to ship first: **[Use Case Implementation Guides](../use-cases/README.md)**.
