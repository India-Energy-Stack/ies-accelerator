# Schemas

> **The master vocabulary of IES.** Every domain object, what it is for, which use cases combine it, how versions evolve, and how a new object is proposed and accepted. The shape of each object is described by its **schema** — and this section is the canonical home of those schema files: each family below carries its machine-readable reference (`schema.json`, `context.jsonld`, examples) alongside a plain-language overview.

This section answers the practical questions an implementer asks:

1. *"For my use case, which schemas do I need?"* — the **schema map** below.
2. *"What is this schema, in plain words, and what do I validate against?"* — each family page below opens with a concise overview, ahead of the versioned field reference.
3. *"My system has a domain object IES doesn't yet cover. How do I propose a new schema?"* — the **proposal flow** below.
4. *"Who owns these schemas, who can change them, and when?"* — **Stewardship**.

Every schema stands on its own: a complete, self-describing data shape (JSON Schema + JSON-LD context + RDF vocabulary + worked examples) that is valid wherever the payload travels — over the IES Beckn network, through a wallet such as DigiLocker, on a web portal, or as a plain signed file. IES recommends the [Beckn data-exchange flow](../what-ies-provides/discover.md) for organisation-to-organisation (B2B) exchange; consumer-facing (B2C) delivery can use any channel the issuer already runs.

---

## Schema map

Every IES schema, the domain it covers, the use cases that combine it, and its current version.

### Verifiable Credentials

W3C VC payloads — signed, durable records the holder keeps and verifies independently of any network. Issuance, verification and revocation operations are in **[Energy Credentials](../what-ies-provides/energy-credentials/README.md)**.

| Schema | Domain | Used in | Reference |
|---|---|---|---|
| [ElectricityCredential](ElectricityCredential/README.md) | Static facts of a consumer connection — sanctioned load, tariff, assets behind the meter | [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md) · [DER Visibility](../use-cases/der-visibility/README.md) | **[v1.2](ElectricityCredential/v1.2/README.md)** |
| [MeterDataCredential](MeterDataCredential/README.md) | Signed envelope around a MeterData payload — attests who produced the readings | [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) | **[v0.6](MeterDataCredential/v0.6/README.md)** |
| [MeterDataRequestCredential](MeterDataRequestCredential/README.md) | Signed proof-of-right-to-ask that a seeker presents to a meter-data provider | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) (optional) | **[v0.1](MeterDataRequestCredential/v0.1/README.md)** |

### Data Exchange payloads

Structured, non-credential payload schemas.

| Schema | Domain | Used in | Reference |
|---|---|---|---|
| [MeterData](MeterData/README.md) | Smart-meter telemetry (8 compact profiles: CUSTOMER, INTERVAL, DAILY, MONTHLY, BILL_DETAILS, INSTANTANEOUS, EVENT, ALARM) | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) · [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md) (payload) | **[v0.6](MeterData/v0.6/README.md)** |
| [MeterDataRequest](MeterDataRequest/README.md) | Query / capabilities / authorisation shapes for meter-data requests | [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) | **[v0.6](MeterDataRequest/v0.6/README.md)** |
| [ArrFiling](ArrFiling/README.md) | Aggregate Revenue Requirement filings — DISCOM to SERC | [DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md) | **[v0.5](ArrFiling/v0.5/README.md)** |
| [OutageNotification](OutageNotification/README.md) | Planned + unplanned outage notices — pull feed (outage map) and push alert (CAP). **WIP** | — no IES use-case guide yet | **[v0.1](OutageNotification/v0.1/README.md)** |
| `IES_Policy` *(upstream)* | Tariffs and policy-as-code | [Policy as Code](../use-cases/tariff-intelligence/README.md) | in progress |

### External — DEG schemas IES uses

Canonical at [schema.beckn.io](https://schema.beckn.io); the field reference is mirrored in **[External Schemas](external/README.md)**.

| Schema family | Domain | Used in |
|---|---|---|
| `P2PTrade` / `DEGContract` / `EnergyTradeOffer` / `EnergyTradeDelivery` / `DiscomLedgerProvider` / `BecknTimeSeries` (mirror covers the core trade tables; `EnergyTradeDelivery` and `DiscomLedgerProvider` are defined only at schema.beckn.io) | Peer-to-peer energy trade | [P2P Energy Transaction](../use-cases/p2p-energy-trading/README.md) |
| `DemandFlexNeed` / `DemandFlexBuyOffer` / `DemandFlexPerformance` + shared `EnergyResource` / `DEGContract` / `RevenueFlow` / `BecknTimeSeries` | Demand-side flexibility procurement and M&V | — not yet an IES use case |

---

## How the schemas fit together

Each schema is a self-contained record: it validates, signs and verifies the same way whether or not it is ever carried over the Beckn network. What differs per schema is the typical channel:

- **MeterData** and **MeterDataRequest** are exchanged over Beckn in B2B flows (the [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md) use case), with the optional **MeterDataRequestCredential** attached at `confirm` to prove the right to ask. Consumer-facing delivery of the same payloads can happen over any channel.
- **ElectricityCredential** and **MeterDataCredential** are credentials the holder keeps and any verifier checks offline against the issuer's published key. They are issued and delivered through the credential rails — DigiLocker, a wallet, a DISCOM portal.
- **ArrFiling** is delivered DISCOM-to-SERC over Beckn in the [DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md) use case.
- **OutageNotification** is published as a web / outage-map pull feed and a CAP-shaped push alert.

Each family page carries the per-schema detail.

## Versioning

Every schema lives at `schemas/<Family>/v<version>/` with its own:

- `attributes.yaml` — the OpenAPI 3.1 source of truth (hand-edited).
- `schema.json` — compiled JSON Schema (Draft 2020-12) for validation.
- `context.jsonld` — JSON-LD context for semantic resolution.
- `vocab.jsonld` — RDF vocabulary with CIM alignments.
- `examples/` — worked payloads.
- `README.md` — auto-generated field reference.

A change is **non-breaking** (additive, optional fields, new enum values) if it keeps backward compatibility — the same minor version may absorb it. A change is **breaking** (field rename, removal, type change, semantics change) if it doesn't — a new version is published in a sibling directory (e.g. `v1.1/` next to `v1.0/`, never overwriting it). Old versions stay reachable; clients pin a version explicitly.

### Canonical hosting and mirrors

The schema files are served by GitHub Pages at stable URLs of the form `https://india-energy-stack.github.io/ies-accelerator/schemas/...`. This matters beyond documentation: JSON-LD `@context` URLs inside credentials must **resolve at runtime** for verifiers to validate, so the canonical URLs cannot depend on a third-party host. DISCOMs running air-gapped can sync this directory once and verify credentials without outbound HTTPS.

Families whose source of truth is upstream (e.g. `beckn/DEG` for ElectricityCredential) are mirrored **verbatim** — the files are never edited in place, each family's `README.md` names the upstream source and version, and upstream is authoritative if a discrepancy is found (open an issue so the mirror can be refreshed).

---

## Standards precedence

Every schema in IES records, per field, the standard that governs it. The IES order of preference is fixed:

1. **Bureau of Indian Standards (IS)** — e.g. IS 16444 for smart meters, IS 15959 for DLMS/COSEM.
2. **CEA Regulations** and the **Indian Electricity Grid Code (IEGC)**.
3. **International Electrotechnical Commission (IEC)** — CIM (IEC 61968 distribution, IEC 61970 transmission/DER), IEC 62056 (DLMS/COSEM).
4. **Institute of Electrical and Electronics Engineers (IEEE)** — IEEE 1547 (DER interconnection), IEEE 2030.5 (Smart Energy Profile), IEEE 1366 (SAIDI/SAIFI), IEEE 1782 (outage causes).

The precedence is recorded as the machine-readable `x-standards-precedence` map at the root of every JSON Schema: `{ IS:1, CEA:2, IEGC:2, IEC:3, IEEE:4 }`. Per-field standard provenance is in the `x-standard` annotation on every property.

Where no Indian standard applies, an international one is used and the gap is recorded — see the standards-basis notes on each family page and the **§6 Where Indian Standards Do Not Yet Exist** section in every use-case guide.

---

## Proposing a new schema (or a change)

When your use case has a domain object IES doesn't cover yet, the path is:

1. **Check the map above** — confirm no existing schema (with optional extension) already covers it.
2. **Draft the schema** in `attributes.yaml` shape following the **[IES Documentation Template](../use-cases/README.md#how-each-guide-is-organised)**.
3. **Open a PR** against this repository. Include: scope statement, basis of standards (with the IS → CEA → IEC → IEEE precedence), example payloads.
4. **Review by the IES Cell** — the governance body under the Central Electricity Authority. Reviews check standards alignment, field overlap with existing schemas, and use-case fit.
5. **Acceptance** publishes a versioned `v0.1` and adds the schema to the map above.

The detailed governance framework will be notified by the IES Cell separately. For interim questions, contact the [IES Secretariat](../how-you-implement-ies/setup-register.md#id-1.7-beckn-participants-get-referenced-into-an-ies-network).

---

## Stewardship

The schemas are stewarded by the **IES Cell**, the governance body being constituted under the Central Electricity Authority with representation from across the sector. The Cell owns the specifications, decides what is added or changed, and publishes each version. Operationally:

- **Schema source of truth** — this repository, under `schemas/`.
- **Canonical hosting** — `india-energy-stack.github.io/ies-accelerator/schemas/...`.
- **Versioning policy** — semver-light (`v<major>.<minor>`), with non-breaking changes within a minor version and breaking changes triggering a new minor.
- **Deprecation** — old versions stay queryable; the schema map and the canonical URL flag the active version.

---

## Where this fits

The Schemas section is the master view of **Exchange**. To see how the three IES steps fit together: **[Register](../what-ies-provides/register.md)** → **[Discover](../what-ies-provides/discover.md)** → **[Exchange](../what-ies-provides/exchange.md)**.

To pick a use case to ship first: **[Use Case Implementation Guides](../use-cases/README.md)**.
