# How you implement IES

**Start here to implement IES.** A pragmatic, step-by-step path from zero to a working IES adapter — the same path the four [pilot DISCOMs](../README.md#pilots-and-status) followed in the 30-day Challenge. Each page is an end-to-end do-guide: prerequisites first, then numbered copy-pasteable steps, then a checklist. The concepts behind the steps live in **[What IES Provides](../what-ies-provides/README.md)**; if you want the plain-language intro first, read **[Home](../README.md)**.

## Getting-started checklist

Work top to bottom. Set up only the rails your use cases need (see the two-rails note below).

- [ ] **Read the concepts.** Skim **[What IES Provides](../what-ies-provides/README.md)** — Register, Discover, Exchange, Verifiable Credentials — so the steps below have context.
- [ ] **Line up the prerequisites** — a domain you control, DNS access, one Linux host that runs Docker, one engineer (see [Before you start](#before-you-start)).
- [ ] **Step 1 — [Setup Register](setup-register.md)** *(everyone)*: publish a `did:web`, claim and verify a DeDi namespace; Beckn participants also publish a subscriber record.
- [ ] **Step 2 — [Issue Credentials](issue-credentials.md)** *(B2C credential use cases)*: run OpenCred; issue, verify and revoke W3C Verifiable Credentials.
- [ ] **Step 3 — [Setup Exchange](setup-exchange.md)** *(B2B data-exchange use cases)*: run the ONIX Beckn adapter and complete a signed round-trip on the IES network.
- [ ] **Step 4 — [Build your Internal-facing Adapter](build-adapter.md)**: map your internal systems to the IES schemas, feeding OpenCred and/or ONIX.
- [ ] **Step 5 — [Conformance Checklist](conformance.md)**: run the conformance suite end-to-end and sign off as IES-ready.
- [ ] **Ship a use case.** Pick your first from the **[Use Case Implementation Guides](../use-cases/README.md)**.

The rest of this page expands each step.

| Step | Page | Time | What you get |
|---|---|---|---|
| **1. Setup Register** *(everyone)* | [Setup Register](setup-register.md) | 1–2 days | A verifiable `did:web`, a verified DeDi namespace — plus, for Beckn participants, a published subscriber record and an IES network reference |
| **2. Issue Credentials** *(B2C — credential use cases)* | [Issue Credentials](issue-credentials.md) | ½ day | A running OpenCred signing service: issue, verify, revoke W3C Verifiable Credentials |
| **3. Setup Exchange** *(B2B — data-exchange use cases)* | [Setup Exchange](setup-exchange.md) | 1–2 days | A running Beckn adapter (ONIX) exchanging signed messages on the IES network |
| **4. Build your Internal-facing Adapter(s)** | [Build your Internal-facing Adapter](build-adapter.md) | 1–4 weeks | Small mapping layers between your internal systems and the IES schemas — feeding OpenCred and/or ONIX |
| **5. Conformance Check** | [Conformance Checklist](conformance.md) | 1 day | A signed-off, IES-ready interface, end-to-end |

Steps 2 and 3 are the two independent rails, and you only set up the ones your use cases need:

- **Step 2 — credentials (B2C).** You sign a record once; *any* third party — a bank, a marketplace, a housing society — can verify it against your published `did:web`, and it can be delivered over any channel (DigiLocker, web portal, email, SMS, chat). No network membership involved. Use cases: Consumer Energy Passport, Consumer Meter Digest.
- **Step 3 — data exchange (B2B).** Structured datasets move between *registered organisations* over a Beckn network, with DeDi-anchored membership as the bilateral trust layer. Use cases: Smart Meter Data Exchange, Regulatory Filing, P2P Trading.

A credentials-only DISCOM can ship its first use case with just steps 1, 2, 4, 5 — and add step 3 later when a data-exchange use case calls for it. A pure Beckn participant (e.g. a trading platform) skips step 2.

---

## Before you start

### What you need

- **A domain you control.** Most DISCOMs use a dedicated subdomain like `ies.<discom>.in`. A bare apex domain works too.
- **DNS access.** To add a TXT record once (DeDi namespace verification).
- **One Linux host** that can run Docker (for OpenCred and/or ONIX) and serve HTTPS. Cloud VM is fine. Air-gapped works too.
- **One engineer.** Total effort is small; you do not need a team.
- **A vendor or in-house developer** to write the Part-2 adapter mapping (Step 4). The same person can do all of 1–4.

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

---

## The path in one diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 1 — Setup Register                                    (everyone)      │
│  • Pick a domain; generate signing keypair; publish did.json                │
│  • Claim a DeDi namespace; verify it with a DNS TXT record                  │
│  • (Beckn participants) Ed25519 keypair + subscriber record + IES network   │
│  → Output: did:web resolvable from anywhere; directory entries published    │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                                     │
        credential use cases                    data-exchange use cases
                    ▼                                     ▼
┌───────────────────────────────────┐   ┌───────────────────────────────────┐
│  Step 2 — Issue Credentials (B2C) │   │  Step 3 — Setup Exchange (B2B)    │
│  • Run OpenCred with DeDi config  │   │                                    │
│  • Issue → verify → revoke        │   │  • Run ONIX sandbox; confirm →    │
│  • Deliver via DigiLocker / any   │   │    on_confirm round-trip          │
│    channel                        │   │  • Swap in your identity;         │
│  → Output: production credential  │   │    set allowedNetworkIDs          │
│    issuance                       │   │  → Output: live on IES network    │
└───────────────────────────────────┘   └───────────────────────────────────┘
                    │                                     │
                    └──────────────────┬──────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 4 — Build your Internal-facing Adapter(s) (the Part-2 mapping)        │
│  • Map your data → IES schema fields (CIS↔customerProfile, MDM↔MeterData…)  │
│  • Plug the mapping into OpenCred (credential feeds) and/or ONIX (BPP       │
│    handler / BAP callback)                                                  │
│  → Output: a working IES interface to your internal systems                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 5 — Conformance Check                                                 │
│  • Run the conformance suite end-to-end; sign off                           │
│  → Output: your organisation is IES-ready                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## After you're set up

You only do the setup once. Adding new use cases on top — Consumer Energy Passport, Smart Meter Data Exchange, DER Visibility — only adds a small bit to the Part-2 mapping. The identity, the adapters, the network membership, the trust foundation are all reused.

Go to **[Use Case Implementation Guides](../use-cases/README.md)** and pick the one you want to ship first.

---

## How long does the whole thing take?

The four pilot DISCOMs each went from cold start to four demonstrated use cases in **30 days**. The bulk of that time was the Part-2 mapping (Step 4) and customer-ops procedures for the consumer-facing credentials.

| Phase | Calendar time (typical) |
|---|---|
| Step 1 (identity + directory) | 1–2 days |
| Steps 2–3 (engines: OpenCred and/or ONIX) | 1–3 days |
| Step 4 (adapter for first use case) | 1–3 weeks |
| Step 5 (conformance) | 1–2 days |
| Each subsequent use case | A few days to a week |
