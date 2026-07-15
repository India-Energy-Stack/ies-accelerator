# Build your Internal-facing Adapter

> **Step 4 of the implementation path.** Write the **Part-2 mapping** between your internal systems and the IES schemas. This is the only IES work where you write code — the rest is configuration. About 1–3 weeks for the first use case; subsequent use cases add only a few days each.

This is where the engines from Steps 2 and 3 get fed from your internal systems. Per-use-case adapter shapes are in **[Use Case Implementation Guides](../use-cases/README.md)**.

---

## Before you start

- Step 1 ([Setup Register](setup-register.md)) complete — your `did:web` resolves and your DeDi namespace is verified.
- The engine your first use case needs is running: **OpenCred** for credential use cases ([Issue Credentials](issue-credentials.md)) and/or **ONIX** for data-exchange use cases ([Setup Exchange](setup-exchange.md)). You wire your mapping into whichever you set up.
- Read access to the internal system that holds the data (CIS, MDM, HES, DERMS, ERP) and a developer who can write ~200–1,000 lines of glue code.

---

## What the adapter is

The IES adapter has two parts: a ready-made **engine** and your **mapping**. There is one engine per capability — **ONIX** for use cases that run over a Beckn network ([Setup Exchange](setup-exchange.md)), **[OpenCred](../glossary.md#opencred)** for credential use cases ([Issue Credentials](issue-credentials.md)) — and you build an internal-facing mapping for each engine your use cases need.

| Part | What it does | You build it? |
|---|---|---|
| **Part 1 — ONIX** *(Beckn-network use cases)* | Finds other systems, exchanges messages, signs and verifies, routes callbacks | **No** — ready-made, the same for everyone |
| **Part 1 — OpenCred** *(credential-only use cases)* | Issues, verifies and revokes W3C Verifiable Credentials with your signing key | **No** — ready-made, the same for everyone |
| **Part 2 — your mapping(s)** | Translates between your data format and the IES specs, feeding the engine(s) above | **Yes** — specific to your organisation, set up once |

The mapping is small. For a single use case it is typically 200–1,000 lines of code. It is the only piece that knows about your internal field names, your tariff codes, your meter SLNO format, your CIS schema.

---

## Where the mapping lives

For Beckn-network use cases, the mapping plugs into ONIX as one or more **BPP handlers** (provider side) and **BAP callbacks** (buyer side). ONIX delivers a typed Beckn message to your handler; your handler talks to your CIS / MDM / DERMS / ERP and returns a typed Beckn response. For credential-only use cases the same pattern applies with **OpenCred** in place of ONIX: your mapping sits between your internal systems and OpenCred's issue API (see [Task 4](#task-4-wire-into-your-engine-onix-and-or-opencred)).

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
| **[Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md)** | CIS / billing master | [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) | Smallest schema; consumer-facing value is immediate |
| **[Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md)** | HES / MDM | [MeterData v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdata/v0.6) | Solves a tangible AMISP-DISCOM pain; mostly DataOps work |
| **[Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md)** | MDM (read path) | [MeterDataCredential v0.6](https://india-energy-stack.gitbook.io/docs/schemas/meterdatacredential/v0.6) | Builds on the Passport adapter; small extra surface |
| **[DER Visibility](../use-cases/der-visibility/README.md)** | DER / inverter registration database | [ElectricityCredential v1.2](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2) energyResources | If rooftop / EV registrations are your priority |
| **[DISCOM Regulatory Filing](../use-cases/discom-regulatory-filing/README.md)** | Regulatory affairs / finance | [ArrFiling v0.5](https://india-energy-stack.gitbook.io/docs/schemas/arrfiling/v0.5) | If you have an ARR due |

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

- **Unit packaging** — your `5` becomes `{ "value": 5, "unit": "kW" }` per [QuantitativeValue](https://india-energy-stack.gitbook.io/docs/schemas/electricitycredential/v1.2#field-reference).
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

### Task 4 — Wire into your engine (ONIX and/or OpenCred)

**Beckn-network use cases — wire into ONIX.** ONIX delivers a typed Beckn message to a handler endpoint you register. The handler does Tasks 1–3 in real time:

1. Receive the inbound message.
2. Extract scope (which meter, which date range, which credential).
3. Query your internal systems.
4. Build the IES-shaped response.
5. Validate against the schema.
6. Return.

The Beckn wiring (subscriber id, callback URL, route registration) is in ONIX config; the handler endpoint is your code.

**Credential use cases — wire into OpenCred.** Your mapping assembles the credential subject from CIS / MDM data (Tasks 1–3) and POSTs it to OpenCred's `/v1/credentials/issue`; OpenCred signs with your key and returns the credential for delivery to the holder. The issue / verify / revoke walkthrough is in **[Issue Credentials](issue-credentials.md#id-2.6-issue-your-first-credential)**.

### Task 5 — Test end-to-end

**Beckn-network use cases.** Use the [Data Exchange devkit](setup-exchange.md#id-3.1-deploy-the-local-sandbox) to send your handler real Beckn messages from a sandbox counterparty. Iterate until all required schema fields are populated correctly, signatures verify on the receiving side, and the end-to-end round trip succeeds for at least one realistic record.

**Credential use cases.** There is no Beckn counterparty — test the issuance path directly: have your mapping assemble the subject from a real record and POST it to OpenCred's `/v1/credentials/issue`, then run the [§2.9 smoke test](issue-credentials.md#id-2.9-smoke-test) (issue → resolve your `did:web` → verify → revoke → re-check). Iterate until it issues a schema-valid, signature-verifiable credential for at least one realistic record.

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
- [ ] Mapping wired into its engine — BPP handler registered with ONIX (Beckn-network use case) or issuance feed calling OpenCred (credential-only use case)
- [ ] One realistic record exchanged or issued end-to-end with a counterparty / verifier

When all six are ticked, you have completed Step 4 for your first use case. Move on to **[Step 5 — Conformance Checklist](conformance.md)**, then publish.

For the second and subsequent use cases, only Tasks 1–4 repeat. The sandbox test (Task 5) reruns quickly, and conformance (Step 5) and all the identity / network setup are reused.
