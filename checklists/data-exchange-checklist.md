# Data Exchange — Checklist

*One staged checklist from devkit sandbox to production go-live. Each item links to the section in [Data Exchange](../data-exchange/README.md) (or the foundational chapters) that walks the step. No field-level detail is duplicated here — follow the link if you need depth.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ BAP (Data Consumer) &nbsp; ☐ BPP (Data Provider) &nbsp; ☐ Both

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Use Case(s):** &nbsp; ☐ Meter telemetry &nbsp; ☐ ARR filings &nbsp; ☐ Tariff policies &nbsp; ☐ Other: \_\_\_\_\_\_\_\_\_\_

---

## Stage 0 — Scope and team

*Decide what you'll exchange and who owns it. Start with one or two datasets.*

- [ ] Datasets identified (meter telemetry, ARR filings, tariff policies, …) → [What you can exchange](../data-exchange/README.md#what-you-can-exchange-schema-families)
- [ ] Source system mapped for each dataset (MDMS / billing / regulatory filing system)
- [ ] IT/data point of contact nominated
- [ ] Authorised signatory nominated — approves what your organisation publishes

## Stage 1 — Devkit validation (local sandbox)

*Goal: prove the wiring and your application's handling of the payload shape — no real identity, no real network.*

- [ ] [Step 1 — clone and start the stack](../data-exchange/README.md#1-clone-and-start-the-stack); all 7 containers healthy
- [ ] [Step 2 — Postman collection imported](../data-exchange/README.md#2-import-the-postman-collection-for-your-use-case) for your role + use case (defaults left intact)
- [ ] [Step 3 — `confirm` sent](../data-exchange/README.md#3-send-confirm); ACK received
- [ ] [Step 4 — `on_confirm` landed](../data-exchange/README.md#4-watch-on_confirm-land) in `sandbox-bap` (BAP) or `sandbox-bpp` (BPP)
- [ ] (BAP) Your application consumes the `dataPayload` body ([MeterData](../schemas/MeterData/README.md) / [ArrFiling](../schemas/ArrFiling/README.md) / tariff policy)
- [ ] (BPP) Your provider handles inbound `confirm` and emits `on_confirm` (or `on_status` for async / paged delivery)
- [ ] *(Optional)* Interop over a public tunnel with another participant — [Go over the public internet (ngrok)](../data-exchange/README.md#go-over-the-public-internet-ngrok)

## Stage 2 — Network identity (DeDi)

*Goal: self-owned identity that counterparties can resolve and verify.*

- [ ] DeDi account created; namespace claimed and domain-verified → [Registries — Step-by-step](../registries/README.md#step-by-step-claim-your-dedi-namespace-and-create-registries)
- [ ] Ed25519 signing keypair generated (`tools/sign` in beckn-onix) → [Identifiers — Step 2 (Beckn keypair)](../identifiers/README.md#step-2--generate-your-beckn-signing-keypair)
- [ ] Beckn subscriber registry created (tag `beckn_subscriber`) under your namespace
- [ ] Subscriber record published (`subscriber_id`, `subscriber_url`, `type`, `signing_public_key`, `countries`)
- [ ] Lookup verified at `https://fabric.nfh.global/registry/dedi/lookup/<subscriber_id>/subscribers.beckn.one/<record_id>`
- [ ] DeDi values noted: `subscriber_id`, `record_id` (= ONIX `keyId`), Ed25519 keypair

## Stage 3 — Test-network certification

*Goal: appear in `indiaenergystack.in/test-ies-data-sharing-network` and run end-to-end exchanges with another participant.*

- [ ] ONIX config updated with your real identity → [Swap in your real identity](../data-exchange/README.md#swap-in-your-real-identity) (`networkParticipant`, `keyId`, `signingPrivateKey`, `signingPublicKey`)
- [ ] `allowedNetworkIDs` set to `indiaenergystack.in/test-ies-data-sharing-network`
- [ ] IES Secretariat emailed with your DeDi lookup URL → [Registries — How to apply](../registries/README.md#how-to-apply-for-an-ies-listing)
- [ ] Confirmed your subscriber appears under `indiaenergystack.in/test-ies-data-sharing-network` (re-query the namespace)
- [ ] End-to-end `confirm` → `on_confirm` round-trip with at least one other participant on the test network
- [ ] *(If applicable)* [Pagination](../data-exchange/README.md#pagination--large-datasets-across-multiple-status--on_status-messages) flow tested — BAP-PULL or BPP-PUSH per your use case

## Stage 4 — Production deployment

*Goal: live exchange with real DISCOMs / regulators / AMISPs on `indiaenergystack.in/ies-data-sharing-network`.*

- [ ] Second ONIX deployment stood up on production hostname with TLS termination (separate keypair, separate DeDi subscriber record) → [Two registries, two ONIX deployments](../data-exchange/README.md#two-registries-two-onix-deployments)
- [ ] Prod ONIX `allowedNetworkIDs` set narrowly to `indiaenergystack.in/ies-data-sharing-network`
- [ ] IES Secretariat re-applied for the **prod** network reference
- [ ] First prod exchange completed end-to-end
- [ ] Test ONIX kept running for ongoing certification / staging traffic

## Stage 5 — Operational hardening

*Goal: graduate from one-off success to a maintainable production deployment.*

- [ ] Reverse proxy + TLS in front of ONIX (never expose `:8081` / `:8082` directly)
- [ ] Signing key in a secret manager (Vault, AWS Secrets Manager, Azure Key Vault)
- [ ] Schema validation enabled and tested → [Appendix C — Schema validation](../data-exchange/README.md#appendix-c--schema-validation)
- [ ] Monitoring / alerting on ONIX health, signature-verification failures, and registry lookups
- [ ] Key-rotation runbook in place
- [ ] On-call rota for inbound message handling on the BAP / BPP webhooks
- [ ] *(BAP)* Your own application has replaced `sandbox-bap` → [Make the sandbox your own](../data-exchange/README.md#make-the-sandbox-your-own)
- [ ] *(BPP)* Your provider has replaced `sandbox-bpp`

---

*Once Stages 0–4 are complete, you're a live participant on the IES inter-DISCOM data exchange network. Stage 5 is ongoing operational discipline.*
