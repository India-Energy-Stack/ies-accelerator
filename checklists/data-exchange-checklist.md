# Data Exchange — Onboarding Checklist

*One staged checklist from devkit sandbox to production go-live. Stage 1 is the [Quick Start](../data-exchange/quick-start.md); Stages 2–3 are [Registry Setup](../data-exchange/registry-setup.md). Use the early stages to brief leadership and align IT/data teams; the later stages are the technical execution path.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ BAP (Data Consumer) &nbsp; ☐ BPP (Data Provider) &nbsp; ☐ Both

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Use Case(s):** &nbsp; ☐ Meter telemetry &nbsp; ☐ ARR filings &nbsp; ☐ Tariff policies &nbsp; ☐ Other: \_\_\_\_\_\_\_\_\_\_

---

## Stage 0 — Scope and team

*Decide what you'll exchange and who owns it. Start with one or two datasets.*

- [ ] Datasets identified (meter telemetry, ARR filings, tariff policies, …)
- [ ] Source system mapped for each dataset (MDMS / billing / regulatory filing system)
- [ ] IT/data point of contact nominated (name, email, phone)
- [ ] Authorised Signatory nominated — approves what your organisation publishes

## Stage 1 — Devkit validation (local sandbox)

*Goal: prove the wiring and your application's handling of the payload shape — no real identity, no real network. This is [Quick Start](../data-exchange/quick-start.md) Phases A–C.*

- [ ] Devkit cloned, stack up (`docker compose up -d` in `install/`), all containers healthy
- [ ] Postman collection for your role and use case imported (defaults left intact)
- [ ] `confirm` → `on_confirm` round-trip succeeds against the sandbox
- [ ] (BAP) Your application consumes the `dataPayload` body ([MeterData](../schemas/MeterData/README.md) / [ArrFiling](../schemas/ArrFiling/README.md) / tariff policy)
- [ ] (BPP) Your provider handles inbound `confirm` and emits `on_confirm` (or `on_status` for async delivery); wire format matches `uc*/examples/`
- [ ] *(Optional)* Interop over a public tunnel (ngrok) with another participant's stack

## Stage 2 — Network identity (DeDi)

*Goal: self-owned identity that counterparties can resolve and verify. Full steps: [Registry Setup](../data-exchange/registry-setup.md).*

- [ ] DeDi namespace verified for a domain you control (DNS TXT record)
- [ ] Subscriber registry created under your namespace (type `beckn-subscriber`; separate test/prod registries recommended)
- [ ] Ed25519 signing key pair generated; private key stored in a secrets manager — never in config files or the repo
- [ ] Subscriber record published (`subscriber_id`, `subscriber_url`, `type`, public key); `recordId` noted
- [ ] DeDi lookup URL sent to the IES Secretariat ([IES.Secretariat@fsrglobal.org](mailto:IES.Secretariat@fsrglobal.org)); reference entry confirmed in the **test** network registry (`indiaenergystack.in/test-ies-data-sharing-network`)

## Stage 3 — Test network validation

*Goal: same flows as Stage 1, now with your real identity on the IES test network.*

- [ ] ONIX config updated: `allowedNetworkIDs` (test network), `networkParticipant`, `keyId`, signing keys ([Quick Start § Swap in your real identity](../data-exchange/quick-start.md#swap-in-your-real-identity))
- [ ] End-to-end exchange completes with another participant on the test network
- [ ] Delivered `dataPayload` validates against the declared schema family

## Stage 4 — Real data integration

*Goal: replace sandbox containers and example payloads with your production logic and live sources.*

- [ ] (BPP) Live connection to source system (MDMS / AMISP, ARR filing system, tariff management system)
- [ ] (BPP) `on_confirm` / `on_status` carries real, schema-valid `dataPayload` — not example data
- [ ] (BPP) Catalogue published (`publish-catalog`) and access policy documented (who can request, under what conditions)
- [ ] (BAP) `dataPayload` ingested into downstream systems; duplicate callbacks for the same `transactionId` handled idempotently
- [ ] Data refresh cadence confirmed (annual / quarterly / per tariff order, as applicable)

## Stage 5 — Production infrastructure

*Goal: production-grade deployment. Recommended pattern: [two ONIX deployments, test and prod](../data-exchange/registry-setup.md#two-registries-two-onix-deployments).*

- [ ] Separate **production** ONIX deployment — own hostname, own TLS cert, own keypair, own DeDi subscriber record
- [ ] `subscriber_url` published in DeDi is the TLS-terminated public URL
- [ ] `allowedNetworkIDs` narrowed per deployment (test ONIX accepts only test; prod only prod)
- [ ] Secrets (signing keys) injected from a secrets manager at runtime
- [ ] Monitoring and alerting active for adapter health and callback delivery

## Stage 6 — Go-live

- [ ] Prod DeDi lookup URL referenced by IES into `indiaenergystack.in/ies-data-sharing-network`
- [ ] End-to-end production exchange completed with a real counterpart (not a sandbox)
- [ ] Data integrity spot-checked — delivered `dataPayload` matches the source system
- [ ] Operations runbook ready: key rotation, incident response, dataset/catalogue updates

---

*Reference: [Data Exchange docs](../data-exchange/README.md) · [Quick Start](../data-exchange/quick-start.md) · [Registry Setup](../data-exchange/registry-setup.md) · [DEG Devkit](https://github.com/beckn/DEG/tree/main/devkits/data-exchange)*
