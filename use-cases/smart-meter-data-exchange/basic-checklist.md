# Basic Checklist — Smart Meter Data Exchange

*A plain-English, conceptual checklist for an AMISP, DISCOM, or SERC standing up the [Smart Meter Data Exchange use case](./README.md). Use it to brief leadership and align operations, IT, and metering teams. The detailed setup steps live on the use case page itself.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ AMISP (data provider) &nbsp; ☐ DISCOM (data consumer / re-provider) &nbsp; ☐ SERC / Third-party (downstream consumer)

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Decide the scope of the meter data flow

Pick the meter population, geography, and granularity (15-minute, daily, monthly) you will exchange in Phase 1. Decide who the counterparties will be (AMISP→DISCOM only, DISCOM→SERC, or DISCOM→consented third party).

- [ ] Meter scope defined (count, geography, meter type)
- [ ] Granularity and refresh cadence agreed with the counterparty
- [ ] Counterparty list confirmed

### 2. Register your organisation on the IES network

The AMISP, DISCOM, and any downstream consumer each need an entry in the relevant IES reference registry, with a signing key your counterparties can verify.

- [ ] Organisation registered in the IES DISCOMs / AMISP / Regulators registry as applicable
- [ ] Signing key pair generated and stored securely

### 3. Issue identifiers for every meter and asset

Every meter referenced in the exchange must carry a stable IES identifier. Distribution Transformer, feeder, and substation IDs follow the same scheme so analytics consumers can correlate readings to physical assets.

- [ ] Meter ID scheme adopted and minted into a utility-scoped registry
- [ ] DT / feeder / substation IDs aligned with the IES identifier patterns

### 4. Stand up the data-exchange adapter

The AMISP runs the provider-side adapter; the DISCOM runs the consumer-side adapter. Start on the local devkit sandbox to prove the plumbing, then point at the IES network for production.

- [ ] Adapter running on the devkit sandbox
- [ ] Test exchange (`confirm` → `on_status`) succeeds end-to-end
- [ ] Output validated against the `IES_Report` (OpenADR 3) format

### 5. Connect the real metering system

Replace the sandbox response with a connection to the AMISP's MDMS / head-end system. Confirm the OBIS-code-to-OpenADR mapping for the readings you ship.

- [ ] Live MDMS connection established
- [ ] OBIS → OpenADR mapping verified for each reported quantity
- [ ] Data quality flags (missing / estimated) handled per the IES profile

### 6. Publish your dataset catalogue

The AMISP publishes a catalogue entry the DISCOM can `discover` and `confirm` against. Pre-agreed bilateral subscriptions can skip discovery and go straight to `confirm`.

- [ ] Catalogue entry published
- [ ] Access policy documented (who can request, what credentials are required)

### 7. (Optional) Enable consented third-party access

When a consumer-authorised third party is the consumer, they present a [Consumer Meter Digest](../consumer-meter-digest/README.md) authorisation alongside `confirm`. The provider verifies the credential before delivery.

- [ ] Third-party consent model agreed (if in scope)
- [ ] Credential check wired into the provider adapter

### 8. Production deployment and go-live

Deploy with the basics any production service needs and run one real end-to-end exchange before turning on the bulk feed.

- [ ] HTTPS endpoint live; signing keys in a secrets manager
- [ ] Monitoring, alerting, and on-call set up
- [ ] One real production exchange completed and verified
- [ ] Operations runbook in place (key rotation, incident response, MDMS outage handling)

### 9. Nominate your team

Identify two roles: an **IT / data point of contact** for the technical integration and an **Authorised Signatory** who approves what your organisation publishes.

- [ ] IT/data SPOC nominated (name, email, phone)
- [ ] Authorised Signatory nominated (name, email, phone)

---

*Once these nine items are in place, your organisation is exchanging smart-meter data on IES in a standardised, signed, auditable way. See the [Smart Meter Data Exchange use case](./README.md) for the detailed setup, and the [data-exchange basic checklist](../../checklists/data-exchange-basic-checklist.md) for the underlying network-onboarding steps.*
