# Checklist — DISCOM Regulatory Filing

*A plain-English, conceptual checklist for a DISCOM (and the receiving SERC) standing up the [DISCOM Regulatory Filing use case](./README.md) — submitting ARR, true-up, FPPCA, and other compliance filings as structured, signed objects instead of PDFs. Use it to brief leadership and align finance, regulatory affairs, and IT teams.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ DISCOM (filing) &nbsp; ☐ SERC (receiving) &nbsp; ☐ Both

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Decide which filings to start with

Pick the filing types you will publish (or receive) in Phase 1 — typically the annual ARR is the first candidate, followed by true-up, FPPCA, and compliance returns.

- [ ] Filing types selected
- [ ] Source systems identified for each (financial system, regulatory-affairs spreadsheet, etc.)
- [ ] Native vs OpenADR-3 representation decision agreed with the counterparty

### 2. Register the DISCOM and the SERC on the IES network

Both parties need an entry in the relevant IES reference registry, with a signing key the other party can verify.

- [ ] DISCOM registered in the DISCOMs reference registry
- [ ] SERC registered in the Regulators reference registry
- [ ] Signing key pairs generated and stored securely

### 3. Agree the cost-category mapping

The `IES_ARR_Filing` schema uses a standard cost-category enumeration that is a superset of what most SERCs use. Map your finance system's category names to the IES enumeration once.

- [ ] Cost categories mapped to IES enumeration
- [ ] Mapping reviewed and signed off by regulatory affairs and finance
- [ ] Tariff-order references (`policyID`) tracked, so each filing can cite the order it responds to

### 4. Generate a sample filing as structured data

Convert one prior-year filing into the `IES_ARR_Filing` shape. Validate it against the schema and review the cost line items against the original PDF for parity.

- [ ] Sample filing generated and schema-validated
- [ ] Line-item parity confirmed against the source PDF
- [ ] Workbook attachments policy decided (separate dataset, embedded, or omitted)

### 5. Stand up the data-exchange adapters

The DISCOM runs the provider-side adapter; the SERC runs the consumer-side adapter. Start on the local devkit sandbox to prove the plumbing, then point at the IES network for production.

- [ ] Adapters running on the devkit sandbox
- [ ] Test exchange (`confirm` → `on_status`) with the sample filing succeeds
- [ ] Both sides verify each other's signature against the registry

### 6. Catalogue the filing and submit

The DISCOM publishes the filing through its catalogue with the right category (`ARR` / `TRUE_UP` / `FPPCA` / `COMPLIANCE`). The SERC submits `confirm` against it; the signed envelope received is what should be archived.

- [ ] Catalogue entry published per filing
- [ ] SERC archive stores the original signed envelope as the non-repudiation record
- [ ] Re-submission policy agreed (`updatedAt` on the envelope, same `filingId`)

### 7. (Optional) Open the filing for public consumption

If the SERC mandates public disclosure, the same dataset is republished from the SERC's catalogue under public-disclosure norms (settlement value `0`).

- [ ] Public-disclosure catalogue entry published (if in scope)
- [ ] Consumer-rep parties and researchers onboarded as BAPs against it

### 8. Production deployment and go-live

Deploy with the basics any production service needs and run one real submission before the next filing window.

- [ ] HTTPS endpoint live; signing keys in a secrets manager
- [ ] Monitoring and alerting active
- [ ] One real production submission completed and verified
- [ ] Operations runbook in place (key rotation, late-amendment handling)

### 9. Nominate your team

Identify three roles: a **Regulatory affairs / finance point of contact** for the filing content, an **IT point of contact** for the technical integration, and an **Authorised Signatory** who approves what your organisation files.

- [ ] Regulatory / finance SPOC nominated (name, email, phone)
- [ ] IT SPOC nominated (name, email, phone)
- [ ] Authorised Signatory nominated (name, email, phone)

---

*Once these nine items are in place, regulatory filings between the DISCOM and the SERC flow as signed, machine-verifiable objects with a non-repudiable audit trail. See the [DISCOM Regulatory Filing use case](./README.md) for the detailed setup and the [Data Exchange — Checklist](../../data-exchange/README.md#checklist) for the underlying network-onboarding steps.*
