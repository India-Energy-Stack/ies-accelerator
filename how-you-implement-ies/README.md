# Before you build

Every IES participant completes the same setup once, before any use case ships. It is deliberately small — a domain, a few keys, Docker containers, one sign-off — and everything you build afterwards reuses it. The sequence:

1. **Register your organisation.** Claim and domain-verify a namespace in the DeDi directory, and publish a `did:web` identity — the cryptographic name counterparties and verifiers resolve to check your signatures. Beckn participants also publish a subscriber record. → **[Setting up Register](setup-register.md)**
2. **Stand up the Beckn ONIX adapter.** Deploy the ready-made adapter that signs, verifies, and routes messages, and complete a signed `confirm` → `on_confirm` round-trip on the IES network. → **[Setting up Discover & Exchange](setup-exchange.md)**
3. **Pass the conformance check.** Run the conformance checks end-to-end and sign off — that page states exactly what a self-run sign-off does and doesn't prove. → **[Conformance Checklist](conformance.md)**

Two more pieces slot in between, depending on what you're building:

- **[Issuing Credentials](issue-credentials.md)** — for consumer-facing (B2C) credential use cases: run OpenCred and issue, verify, and revoke W3C Verifiable Credentials. A credential is signed once by you and verified by *any* third party against your published `did:web`, over any delivery channel — no network membership involved. A credentials-only participant can defer the ONIX step until a data-exchange use case calls for it; a pure Beckn participant (e.g. a trading platform) skips this one.
- **[Build your Internal-facing Adapter](build-adapter.md)** — the only place you write code: a small mapping (typically 200–1,000 lines per use case) between your internal systems and the IES schemas, feeding OpenCred and/or ONIX. Your existing CIS / MDM / billing / DERMS / ERP stays exactly as it is.

**How this section is organised.** The "Setting up …" pages (and Issuing Credentials) are do-guides — prerequisites first, then numbered copy-pasteable steps, then a checklist. Nested under each is an *in depth* page — [Register & Identifiers](../what-ies-provides/register.md), [Discover](../what-ies-provides/discover.md), [Exchange](../what-ies-provides/exchange.md), [Verifiable Credentials](../what-ies-provides/energy-credentials/README.md) — that explains the concepts behind the steps: what a DID is, how the DeDi directory is structured, why Beckn, the credential trust model. Work through the setup page; open the in-depth page when you want to know why a step is what it is.

| Setup | Page | Time | What you get |
|---|---|---|---|
| **Register** *(everyone)* | [Setting up Register](setup-register.md) | 1–2 days | A verifiable `did:web`, a verified DeDi namespace — plus, for Beckn participants, a published subscriber record and an IES network reference |
| **Exchange** *(B2B use cases)* | [Setting up Discover & Exchange](setup-exchange.md) | 1–2 days | A running Beckn adapter (ONIX) exchanging signed messages on the IES network |
| **Credentials** *(B2C use cases)* | [Issuing Credentials](issue-credentials.md) | ½ day | A running OpenCred signing service: issue, verify, revoke W3C Verifiable Credentials |
| **Adapter** | [Build your Internal-facing Adapter](build-adapter.md) | 1–3 weeks | Small mapping layers between your internal systems and the IES schemas |
| **Conformance** | [Conformance Checklist](conformance.md) | 1 day | A self-run conformance sign-off, end-to-end — scope explained on that page |

---

## What you need

- **A domain you control.** Most DISCOMs use a dedicated subdomain like `ies.<discom>.in`. A bare apex domain works too.
- **DNS access.** To add a TXT record once (DeDi namespace verification).
- **One Linux host** that can run Docker (for OpenCred and/or ONIX) and serve HTTPS. Cloud VM is fine. Air-gapped works too.
- **One engineer.** Total effort is small; you do not need a team.
- **A vendor or in-house developer** to write the adapter mapping. The same person can do everything above.

## What you do NOT need

- ❌ A new database. Your existing CIS / MDM / billing / DERMS / ERP stays exactly as is.
- ❌ A new compliance filing.
- ❌ A new procurement contract.
- ❌ A licence fee.
- ❌ Approval from anyone before starting on the sandbox. Get something working, then talk to the IES Secretariat about going to production.

## Who needs to be involved

| Role | Why | Time commitment |
|---|---|---|
| **DNS / web admin** | Publish `did.json` on your domain; add DeDi TXT record | 15 minutes, once |
| **IT / security admin** | Generate signing keys (KMS preferred); deploy Docker containers | A few hours, once |
| **Application developer / vendor** | Write the mapping (your data → IES schema) | The bulk of the work |
| **Authorised signatory** | Submit your subscriber record for IES network whitelisting | Email/form, once |
| **Customer-ops / compliance** | (For consumer credentials only) Identity-proofing procedure and privacy review | One review pass |

---

## How long the whole thing takes

The four pilot DISCOMs each went from cold start to four demonstrated use cases in **30 days** during the (now completed) DISCOM Challenge. The bulk of that time went into the adapter mapping and the customer-ops procedures for consumer-facing credentials.

| Phase | Calendar time (typical) |
|---|---|
| Register (identity + directory) | 1–2 days |
| Engines (OpenCred and/or ONIX) | 1–3 days |
| Adapter for the first use case | 1–3 weeks |
| Conformance | 1–2 days |
| Each subsequent use case | A few days to a week |

## After you're set up

You only do the setup once. Adding new use cases on top only adds a small bit to the adapter mapping — the identity, the engines, the network membership are all reused. Pick your first from the Use Case Implementation Guides: [Consumer Energy Passport](../use-cases/consumer-energy-passport/README.md), [Consumer Meter Digest](../use-cases/consumer-meter-digest/README.md), [Smart Meter Data Exchange](../use-cases/smart-meter-data-exchange/README.md), [DER Visibility](../use-cases/der-visibility/README.md), or [P2P Energy Transaction](../use-cases/p2p-energy-trading/README.md).
