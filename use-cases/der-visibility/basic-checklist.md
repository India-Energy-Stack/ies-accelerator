# Basic Checklist — DER Visibility

*A plain-English, conceptual checklist for a DISCOM, a TSP / inverter platform, or a downstream consumer (SERC, MNRE, aggregator) standing up the [DER Visibility use case](./README.md). Use it to brief leadership and align operations, regulatory, and IT teams. The detailed setup steps live on the use case page itself.*

---

**Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ DISCOM (issuer + data consumer) &nbsp; ☐ TSP / DER platform (data provider) &nbsp; ☐ Secondary consumer (SERC, MNRE, aggregator)

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Decide the scope of the DER population

Pick the resource types, geography, and connection threshold you will cover in Phase 1 — typically rooftop solar above a sanctioned-capacity cut-off, growing to BESS and V2G as the architecture beds in. Decide whether you will register one profile per DER (disaggregated) or one per connection point (aggregated).

- [ ] Resource types in scope (`SOLAR_PV`, `BESS`, `V2G`, others)
- [ ] Geography / DT / feeder scope defined
- [ ] Aggregated vs. disaggregated profile policy chosen
- [ ] Layer 3 (grid-behavioural) capacity threshold chosen (likely CEA-aligned)

### 2. Register your organisation on the IES network

Each participant needs an entry in the relevant IES reference registry, with a signing key that counterparties can verify.

- [ ] DISCOM registered in the IES DISCOMs Reference Registry (if not already)
- [ ] TSP / DER platform registered in the IES TSP Registry (see [Open Items](./README.md#open-items))
- [ ] SERC / MNRE registered in the Regulators / Programmes registry (if downstream consumer)
- [ ] `did:web` and signing key pair generated and stored securely

### 3. Issue identifiers for connections and DERs

Every connection point and DER referenced in the exchange must carry a stable IES identifier. DT, feeder, and substation IDs follow the same scheme so analytics consumers can correlate readings to physical assets.

- [ ] `connectionPointID` scheme adopted and minted into a utility-scoped registry
- [ ] `derID` scheme adopted (per-DER or per-connection per the Step 1 choice)
- [ ] DT / feeder / substation IDs aligned with the IES identifier patterns

### 4. Issue the DER Connection Credential

The DISCOM signs a `DERConnectionCredential` for every approved grid connection that includes one or more DERs, using the same OpenCred service that issues `CustomerCredential` and the Consumer Energy Passport.

- [ ] OpenCred integration extended to mint `DERConnectionCredential`
- [ ] Delivery to consumer wallet wired (DigiLocker Pull URI or DID push)
- [ ] TSP-provisioning UX agreed (how the consumer or installer hands the VC to the TSP)

### 5. Stand up the data-exchange adapter

The TSP runs the provider-side adapter (BPP); the DISCOM runs the consumer-side adapter (BAP). Start on the local devkit sandbox to prove the plumbing, then point at the IES network for production.

- [ ] Adapter running on the devkit sandbox
- [ ] Test exchange (`search` → `on_search` → `confirm` → `on_status`) succeeds end-to-end
- [ ] Output validated against the `IES_DER` Layer 1 / Layer 2 / Layer 3 shapes

### 6. Connect the real inverter / TSP data path

Replace the sandbox response with a connection to the TSP's inverter telemetry pipeline. Confirm Layer 2 reads emit at 15-minute cadence aligned to IST blocks and carry the OpenADR 3 envelope.

- [ ] Inverter / OEM cloud connection established to the BPP
- [ ] 15-minute OpenADR 3 `REPORT` emission verified
- [ ] Data-quality flags handled per the IES profile
- [ ] Layer 3 capture wired (firmware version, protection settings, ride-through)

### 7. Stand up the DISCOM DER Registry

The DER Registry persists Layer 1 + Layer 3, appends Layer 2 telemetry, and publishes an anonymised index entry to DeDi.

- [ ] `der_profiles`, `der_telemetry`, `subscriptions` tables provisioned
- [ ] DeDi anonymised public-index publication wired
- [ ] Dashboard / DERMS push live-update channel configured

### 8. Publish the TSP DER catalogue

The TSP publishes a catalogue entry the DISCOM can `search` and `confirm` against, filtered by `DERConnectionCredential` issuer.

- [ ] Catalogue entry published per DER (or per aggregated profile)
- [ ] `requiredCredential` set to `DERConnectionCredential` issued by the requesting DISCOM
- [ ] Access policy documented (who can request, what credentials are required)

### 9. (Optional) Enable secondary consumers

When SERC / MNRE / aggregator is the data consumer, the DISCOM acts as BPP and they present a role credential alongside `confirm`. The provider verifies the credential before delivery.

- [ ] Secondary-consumer credential model agreed (if in scope)
- [ ] Credential check wired into the DISCOM-side BPP

### 10. Production deployment and go-live

Deploy with the basics any production service needs and run one real end-to-end exchange before turning on the bulk subscription.

- [ ] HTTPS endpoints live; signing keys in a secrets manager
- [ ] Monitoring, alerting, and on-call set up
- [ ] One real production subscription completed and verified
- [ ] Operations runbook in place (key rotation, incident response, TSP outage handling, Layer 3 refresh on firmware update)

### 11. Nominate your team

Identify two roles: an **IT / data point of contact** for the technical integration and an **Authorised Signatory** who approves what your organisation publishes.

- [ ] IT/data SPOC nominated (name, email, phone)
- [ ] Authorised Signatory nominated (name, email, phone)

---

*Once these eleven items are in place, your organisation is exchanging DER visibility data on IES in a standardised, signed, auditable way. See the [DER Visibility use case](./README.md) for the detailed setup, the [energy-credentials basic checklist](../../checklists/energy-credentials-basic-checklist.md) for the credential service, and the [data-exchange basic checklist](../../checklists/data-exchange-basic-checklist.md) for the underlying network-onboarding steps.*
