# How you implement IES

A pragmatic, step-by-step path from zero to a working IES adapter — the same path the four [pilot DISCOMs](../concepts/what-ies-is.md#pilots-and-status) followed in the 30-day Challenge.

The work follows the **[Register → Discover → Exchange](../concepts/what-ies-is.md#how-it-works-three-steps)** spine — the same three steps that organise every IES interaction. There are three setup steps and one conformance check.

| Step | Page | Time | What you get |
|---|---|---|---|
| **1. Setup Register** | [Setup Register](setup-register.md) | 1–2 days | A verifiable `did:web` for your organisation and a published DeDi namespace |
| **2. Setup Discovery** | [Setup Discovery](setup-discovery.md) | 1–2 days | A running Beckn adapter (ONIX) registered as a subscriber on the IES network |
| **3. Build your Internal-facing Adapter(s)** | [Build your Internal-facing Adapter](build-adapter.md) | 1–4 weeks | Small mapping layers between your internal systems and the IES schemas — feeding ONIX and/or OpenCred |
| **4. Conformance Check** | [Conformance Checklist](conformance.md) | 1 day | A signed-off, IES-ready interface, end-to-end |

Step 2 sets up the Beckn network membership used for **B2B data exchange**. In Step 3 you build an internal-facing adapter per engine your use cases need: one feeding **ONIX** for use cases that run over a Beckn network (e.g. Smart Meter Data Exchange, Regulatory Filing), and one feeding **[OpenCred](../glossary.md#opencred)** for credential-only use cases (e.g. Consumer Energy Passport, Consumer Meter Digest). If your first use case is credentials only, you can start with Steps 1 and 3 ([Energy Credentials](../what-ies-provides/energy-credentials/README.md) needs no Beckn network) and add Step 2 when a data-exchange use case calls for it.

---

## Before you start

### What you need

- **A domain you control.** Most DISCOMs use a dedicated subdomain like `ies.<discom>.in`. A bare apex domain works too.
- **DNS access.** To add a TXT record once (DeDi namespace verification).
- **One Linux host** that can run Docker (for ONIX) and serve HTTPS. Cloud VM is fine. Air-gapped works too.
- **One engineer.** Total effort is small; you do not need a team.
- **A vendor or in-house developer** to write the Part-2 adapter mapping (Step 3). The same person can do all of 1–3.

### What you do NOT need

- ❌ A new database. Your existing CIS / MDM / billing / DERMS / ERP stays exactly as is.
- ❌ A new compliance filing.
- ❌ A new procurement contract.
- ❌ A licence fee.
- ❌ Approval from anyone before starting on the sandbox. Get something working, then talk to the IES Secretariat about going to production.

### Who needs to be involved

| Role | Why | Time commitment |
|---|---|---|
| **DNS / web admin** | Publish `did.json` on your domain; add DeDi TXT record | 15 minutes, once |
| **IT / security admin** | Generate signing keys (KMS preferred); deploy Docker containers | A few hours, once |
| **Application developer / vendor** | Write the Part-2 mapping (your data → IES schema) | The bulk of the work |
| **Authorised signatory** | Submit your subscriber record for IES network whitelisting | Email/form, once |
| **Customer-ops / compliance** | (For consumer credentials only) Identity-proofing procedure and privacy review | One review pass |

For the full department-by-department mapping see the **[utility pathway prework matrix](../pathways/utility.md#prework-pre-alignment-matrix)**.

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
│  Step 3 — Build your Internal-facing Adapter(s) (the Part-2 mapping)        │
│  ────────────────────────────────────────────────────────────────────       │
│  • Map your data → IES schema fields (CIS↔customerProfile, MDM↔MeterData…)  │
│  • Plug the mapping into ONIX as a BPP handler (Beckn-network use cases)    │
│    and/or into OpenCred as an issuance feed (credential-only use cases)     │
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

You only do steps 1–4 once. Adding new use cases on top — Consumer Energy Passport, Smart Meter Data Exchange, DER Visibility — only adds a small bit to the Part-2 mapping. The identity, the adapter, the network membership, the trust foundation are all reused.

Go to **[Use Case Implementation Guides](../use-cases/README.md)** and pick the one you want to ship first.

---

## How long does the whole thing take?

The four pilot DISCOMs each went from cold start to four demonstrated use cases in **30 days** (21 May – 21 June 2026). The bulk of that time was the Part-2 mapping (Step 3) and customer-ops procedures for the consumer-facing credentials.

| Phase | Calendar time (typical) |
|---|---|
| Steps 1–2 (identity + discovery) | 2–4 days |
| Step 3 (adapter for first use case) | 1–3 weeks |
| Step 4 (conformance) | 1–2 days |
| Each subsequent use case | A few days to a week |
