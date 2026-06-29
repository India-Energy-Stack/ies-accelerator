# Build your Internal-facing Adapter

> **Step 3 of the three IES steps — set up.** Write the **Part-2 mapping** between your internal systems and the IES schemas. This is the only IES work where you write code — the rest is configuration. About 1–3 weeks for the first use case; subsequent use cases add only a few days each.

This is the **action guide** for the **[Exchange](../exchange.md)** step. Per-use-case adapter shapes are in **[Use Case Implementation Guides](../use-cases/README.md)**.

---

## What the adapter is

The IES adapter has two parts. Step 2 gave you Part 1 (ready-made). Step 3 is Part 2.

| Part | What it does | You build it? |
|---|---|---|
| **Part 1 — ONIX** | Finds other systems, exchanges messages, signs and verifies, routes callbacks | **No** — ready-made, the same for everyone |
| **Part 2 — your mapping** | Translates between your data format and the IES specs | **Yes** — specific to your organisation, set up once |

The mapping is small. For a single use case it is typically 200–1,000 lines of code. It is the only piece that knows about your internal field names, your tariff codes, your meter SLNO format, your CIS schema.

---

## Where the mapping lives

The mapping plugs into ONIX as one or more **BPP handlers** (provider side) and **BAP callbacks** (buyer side). ONIX delivers a typed Beckn message to your handler; your handler talks to your CIS / MDM / DERMS / ERP and returns a typed Beckn response.

```
        ┌─────────────────────────────────────────────────────────────┐
        │                         ONIX                                │
        │  (Beckn protocol, signing, verification, routing — Part 1)  │
        └─────────────────────────────────────────────────────────────┘
                          ▲                            ▲
                          │ BPP request                │ BAP callback
                          │ (typed Beckn msg)          │ (typed Beckn msg)
                          ▼                            ▼
        ┌─────────────────────────────────────────────────────────────┐
        │                Your Part-2 mapping                          │
        │  (200–1,000 lines per use case — the only thing you write)  │
        └─────────────────────────────────────────────────────────────┘
                          ▲                            ▲
                          │ SQL / REST / SFTP          │ SQL / REST / file write
                          ▼                            ▼
        ┌─────────────────────────────────────────────────────────────┐
        │             Your internal systems (unchanged)               │
        │       CIS · MDM · HES · DERMS · ERP · billing · web         │
        └─────────────────────────────────────────────────────────────┘
```

---

## Pick your first use case

The pilot DISCOMs each picked one use case to ship first, then layered the rest on the same identity, network and adapter foundation. The natural first choice depends on what data is easiest for you to expose:

| First use case | Internal system you'll touch | Schema | Why first |
|---|---|---|---|
| **[Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md)** | CIS / billing master | [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md) | Smallest schema; consumer-facing value is immediate |
| **[Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md)** | HES / MDM | [MeterData v0.6](../schemas/MeterData/v0.6/README.md) | Solves a tangible AMISP-DISCOM pain; mostly DataOps work |
| **[Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md)** | MDM (read path) | [MeterDataCredential v0.6](../schemas/MeterDataCredential/v0.6/README.md) | Builds on the Passport adapter; small extra surface |
| **[DER Visibility](../use-cases/der-visibility/README.md)** | DER / inverter registration database | [ElectricityCredential v1.2](../schemas/ElectricityCredential/v1.2/README.md) energyResources | If rooftop / EV registrations are your priority |
| **[DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md)** | Regulatory affairs / finance | [ArrFiling v0.5](../schemas/ArrFiling/v0.5/README.md) | If you have an ARR due |

---

## The five tasks for any use case

The shape is the same regardless of which use case you pick first.

### Task 1 — Map fields

For each IES field in the schema, identify the corresponding column / API field / file format in your internal systems. Write it down as a table:

| IES field | Your source | Notes |
|---|---|---|
| `customerProfile.customerNumber` | CIS `CA_NUMBER` | Plain string, no transformation |
| `consumptionProfiles[].sanctionedLoad.value` | CIS `SANC_LOAD_KW` | Multiplied by 1.0; unit always `kW` for residential |
| `consumptionProfiles[].sanctionedLoad.unit` | hardcoded `"kW"` | LT-Domestic always reported in kW |
| `consumptionProfiles[].tariffCategoryCode` | CIS `TARIFF_CAT` → translate via a small lookup | Your codes (`LT1A`, `HT2C` etc.) → IES codes |
| `customerProfile.energyResources[].id` | `did:web:<your-domain>:assets:meter:<MET_SLNO>` | Compose at issuance time |

This table **is** the mapping. The code that follows is mechanical.

### Task 2 — Write the field transformations

Most fields are pass-through. A few need:

- **Unit packaging** — your `5` becomes `{ "value": 5, "unit": "kW" }` per [QuantitativeValue](../schemas/ElectricityCredential/v1.2/README.md#field-reference).
- **Tariff code translation** — your internal `LT1A` becomes a stable IES code; keep the lookup in one place.
- **Date formatting** — ISO 8601 with timezone offset (`2026-01-10T00:00:00+05:30`).
- **DID composition** — `did:web:<your-domain>:assets:meter:<existing-serial>` (your serial is preserved verbatim).

### Task 3 — Validate against the schema

Use the canonical JSON Schema for the use case you're shipping:

```bash
python3 scripts/validate_schema.py \
  schemas/ElectricityCredential/v1.2/schema.json \
  my-test-output.json
```

The repo ships this validator and a `make validate` target. Examples to validate against live in `schemas/<family>/<version>/examples/`.

### Task 4 — Wire into ONIX

ONIX delivers a typed Beckn message to a handler endpoint you register. The handler does Tasks 1–3 in real time:

1. Receive the inbound message.
2. Extract scope (which meter, which date range, which credential).
3. Query your internal systems.
4. Build the IES-shaped response.
5. Validate against the schema.
6. Return.

The Beckn wiring (subscriber id, callback URL, route registration) is in ONIX config; the handler endpoint is your code.

### Task 5 — Test against the sandbox

Use the [Data Exchange devkit](../data-exchange/README.md#quick-start-run-a-local-exchange-in-10-minutes) to send your handler real Beckn messages from a sandbox counterparty. Iterate until:

- All required schema fields are populated correctly
- Signatures verify on the receiving side
- The end-to-end round trip succeeds for at least one realistic record

Then graduate from sandbox → testnet → prod with the same adapter.

---

## Reuse across use cases

The biggest win comes from doing this once. After your first use case is live, adding the next typically means:

- A new mapping table (Task 1) — usually one page of YAML
- A few new transformations (Task 2) — units, codes, identifier composition
- A new handler endpoint (Task 4) — ~50 lines of code
- A new schema validator config (Task 3) — one line

No new identity. No new ONIX deployment. No new DeDi namespace. No new network onboarding.

---

## Checklist

For the first use case:

- [ ] Use case picked (from the table above)
- [ ] Schema field → internal-system mapping table written
- [ ] Field transformations implemented (units, codes, dates, DIDs)
- [ ] Output validates against the schema for at least three real records
- [ ] BPP handler registered with ONIX; round-trip works against sandbox
- [ ] One realistic record exchanged end-to-end with a counterparty

When all six are ticked, you have completed Step 3 for your first use case. Move on to **[Step 4 — Conformance Checklist](conformance.md)**, then publish.

For the second and subsequent use cases, only Tasks 1, 2, 3 and 4 (handler registration) repeat. Tasks 5 (sandbox), 6 (conformance) and all the identity / network setup are reused.
