# How you implement IES

A step-by-step path from zero to a working IES adapter, following the **[Register → Discover → Exchange](../concepts/how-it-works.md)** spine — three setup steps plus one conformance check. Proven by the four [pilot DISCOMs](../concepts/pilots.md) in the 30-day Challenge.

| Step | Page | Time | What you get |
|---|---|---|---|
| **1. Setup Register** | [Setup Register](setup-register.md) | 1–2 days | A verifiable `did:web` for your organisation and a published DeDi namespace |
| **2. Setup Discovery** | [Setup Discovery](setup-discovery.md) | 1–2 days | A running Beckn adapter (ONIX) registered as a subscriber on the IES network |
| **3. Build your Internal-facing Adapter** | [Build your Internal-facing Adapter](build-adapter.md) | 1–4 weeks | A small mapping layer between your internal systems and the IES schemas |
| **4. Conformance Check** | [Conformance Checklist](conformance.md) | 1 day | A signed-off, IES-ready interface, end-to-end |

---

## Before you start

### What you need

- **A domain you control** — a dedicated subdomain like `ies.<discom>.in`, or a bare apex domain.
- **DNS access** for one TXT record (DeDi namespace verification).
- **One Linux host** running Docker (for ONIX) and serving HTTPS — cloud VM or air-gapped.
- **One engineer** — no team required.
- **A vendor or in-house developer** for the Part-2 adapter mapping (Step 3); can be the same person as 1–3.

### What you do NOT need

- ❌ A new database. Your existing CIS / MDM / billing / DERMS / ERP stays exactly as is.
- ❌ A new compliance filing.
- ❌ A new procurement contract.
- ❌ A licence fee.
- ❌ Approval from anyone before starting on the sandbox — get something working, then talk to the IES Secretariat about going to production.

### Who needs to be involved

| Role | Why | Time commitment |
|---|---|---|
| **DNS / web admin** | Publish `did.json` on your domain; add DeDi TXT record | 15 minutes, once |
| **IT / security admin** | Generate signing keys (KMS preferred); deploy Docker containers | A few hours, once |
| **Application developer / vendor** | Write the Part-2 mapping (your data → IES schema) | The bulk of the work |
| **Authorised signatory** | Submit your subscriber record for IES network whitelisting | Email/form, once |
| **Customer-ops / compliance** | (For consumer credentials only) Identity-proofing procedure and privacy review | One review pass |

Full department-by-department mapping: **[utility pathway prework matrix](../pathways/utility.md#prework-pre-alignment-matrix)**.

---

## The 4-step path in one diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 1 — Setup Register                                                    │
│  ───────────────────────                                                    │
│  • Pick a domain (e.g. ies.discom.example)                                  │
│  • Generate a signing keypair (KMS / HSM)                                   │
│  • Publish did.json at /.well-known/did.json                                │
│  • Claim a DeDi namespace; verify it with a DNS TXT record                  │
│  → Output: did:web:ies.discom.example resolvable from anywhere              │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 2 — Setup Discovery                                                   │
│  ────────────────────────                                                   │
│  • Deploy ONIX container (docker-compose)                                   │
│  • Generate Ed25519 keypair for Beckn message signing                       │
│  • Publish a Beckn subscriber record in your DeDi namespace                 │
│  • Ask the IES network operator to reference your subscriber                │
│  → Output: a running BAP / BPP listed on the IES network                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 3 — Build your Internal-facing Adapter (the Part-2 mapping)           │
│  ────────────────────────────────────────────────────────────────           │
│  • Map your data → IES schema fields (CIS↔customerProfile, MDM↔MeterData…)  │
│  • Plug the mapping into ONIX as a BPP handler                              │
│  • Test against the sandbox / a counterparty                                │
│  → Output: a working IES interface to your internal systems                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 4 — Conformance Check                                                 │
│  ──────────────────────────                                                 │
│  • Run the conformance suite end-to-end                                     │
│  • Sign off                                                                 │
│  → Output: your organisation is IES-ready                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## After you're set up

Steps 1–4 happen once. New use cases — Consumer Energy Passport, Smart Meter Data Exchange, DER Visibility — only extend the Part-2 mapping; identity, adapter, network membership and trust foundation are all reused.

Go to **[Use Case Implementation Guides](../use-cases/README.md)** and pick the one you want to ship first.

---

## How long does the whole thing take?

The four pilot DISCOMs went from cold start to four demonstrated use cases in **30 days** (21 May – 21 June 2026) — mostly Part-2 mapping (Step 3) and customer-ops work for consumer-facing credentials.

| Phase | Calendar time (typical) |
|---|---|
| Steps 1–2 (identity + discovery) | 2–4 days |
| Step 3 (adapter for first use case) | 1–3 weeks |
| Step 4 (conformance) | 1–2 days |
| Each subsequent use case | A few days to a week |
