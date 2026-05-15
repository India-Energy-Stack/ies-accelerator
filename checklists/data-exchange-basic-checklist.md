# Basic Checklist — Data Exchange

*A plain-English, conceptual checklist for a DISCOM (or any organisation) joining the IES Data Exchange. Use it to brief leadership and align your IT and data teams. The [simple technical checklist](./data-exchange-checklist.md) and [detailed checklist](./data-exchange-checklist-detailed.md) cover exactly how each step is done.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ Data Consumer &nbsp; ☐ Data Provider &nbsp; ☐ Both

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Decide which datasets you will publish (or consume)

Pick the data flows that apply to your organisation — for example, meter telemetry, ARR filings, tariff policies, or the regulatory datapoints (energy sales, ABR/ACoS, losses, RPO, source-wise purchase, etc.). Start with one or two.

- [ ] Datasets identified
- [ ] Source systems mapped for each dataset (MDMS / billing / regulatory filing system)

### 2. Set up your network identity

Your IT team generates a signing key pair and registers your organisation on the IES Data Exchange network. This identity is how counterparties confirm requests and responses genuinely came from you.

- [ ] Signing key pair generated and stored securely
- [ ] Organisation registered on the network and a participant ID assigned

### 3. Try it on the test network first

Before connecting any production system, run the full request–response loop on the IES test network using a mock dataset. This confirms the plumbing works.

- [ ] Test-network credentials received
- [ ] Full exchange (select → init → confirm → status) succeeds with mock data
- [ ] Output validated against the standard IES data format

### 4. Connect your real data systems

Replace the mock data with a connection to your real source system. Make sure the output matches the agreed IES data format — definitions, units, frequency (annual / quarterly / per tariff order, as applicable).

- [ ] Live connection to source system established
- [ ] Output validated against IES schema
- [ ] Data refresh cadence confirmed

### 5. Make your data discoverable

Publish a simple catalogue entry so other participants can find your datasets and request them. This is the data-exchange equivalent of being listed in a directory.

- [ ] Catalogue entry published on the network
- [ ] Access policy documented (who can request, under what conditions)

### 6. Production deployment

Deploy with the basics any production service needs: HTTPS, secret management for signing keys, monitoring, and an on-call process.

- [ ] HTTPS endpoint live
- [ ] Signing keys held in a secrets manager (not in config files)
- [ ] Monitoring and alerting active

### 7. Go-live verification

Run one end-to-end exchange on the production network with a real counterpart — not a mock. Confirm data integrity end-to-end and have an operations runbook ready.

- [ ] End-to-end production exchange completed with a real counterpart
- [ ] Data integrity verified against the source
- [ ] Operations runbook prepared (key rotation, incident response, dataset updates)

### 8. Nominate your team

Identify two roles: an **IT / data point of contact** for the technical integration, and an **Authorised Signatory** who approves what your organisation publishes.

- [ ] IT/data SPOC nominated (name, email, phone)
- [ ] Authorised Signatory nominated (name, email, phone)

---

*Once these eight items are in place, your organisation is exchanging energy data on IES in a standardised, secure, auditable way. See the [simple](./data-exchange-checklist.md) and [detailed](./data-exchange-checklist-detailed.md) checklists for the technical execution path.*
