# India Energy Stack
## IES Energy Data Exchange
### DISCOM / Organisation Readiness Checklist

**Name of Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ BAP (Data Consumer) &nbsp; ☐ BPP (Data Provider) &nbsp; ☐ Both

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Use Case(s):** &nbsp; ☐ UC1 Meter Telemetry &nbsp; ☐ UC2 ARR Filings &nbsp; ☐ UC3 Tariff Policies

---

### Stage 1 — Testnet Validation

*Goal: confirm your stack works end-to-end before touching production systems.*

- [ ] **1.a** IES testnet credentials received from IES team (BAP/BPP ID, signing key pair)
- [ ] **1.b** DEG devkit cloned and bootcamp stack running (all Docker services healthy)
- [ ] **1.c** Adapter configs updated with testnet credentials
- [ ] **1.d** Full 4-step exchange (select → init → confirm → status) working with mock BPP
- [ ] **1.e** `dataPayload` received and validated for each applicable use case
- [ ] **1.f** Automated test script (`test-workflow.sh`) passing for all applicable use cases

### Stage 2 — DeDi Setup

*Goal: establish your organisation's namespace on the decentralised data infrastructure before network registration — your DeDi namespace is referenced during registry onboarding.*

- [ ] **2.a** DeDi namespace registered for your organisation at `dedi.global`
- [ ] **2.b** DeDi namespace name noted (e.g. `bescom`, `intelligrid`): \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **2.c** DeDi API credentials received and stored securely
- [ ] **2.d** Namespace accessible — read test against your namespace passes
- [ ] **2.e** (BPP) Dataset hash publication tested — BPP able to anchor hashes to DeDi namespace
- [ ] **2.f** (BPP) Revocation registry URL configured for credentialed datasets

### Stage 3 — Production Network Registration

*Goal: become a registered participant on the live IES Beckn network. Your DeDi namespace is included in the registration submission.*

- [ ] **3.a** Production Ed25519 signing key pair generated (separate from testnet keys)
- [ ] **3.b** Public HTTPS domain set up with valid TLS certificate (domain + TLS in place before registration)
- [ ] **3.c** Registration submitted to IES team — includes public signing key, callback URL, BPP endpoint URL, and DeDi namespace
- [ ] **3.d** Production BAP/BPP ID assigned and noted
- [ ] **3.e** Public key confirmed resolving on the IES production network registry
- [ ] **3.f** Production network ID confirmed with IES team

### Stage 4 — Real Data Integration

*Goal: replace the mock BPP with a production server connected to real data systems.*

- [ ] **4.a** Production BPP server built — handles all four Beckn actions (`select`, `init`, `confirm`, `status`)
- [ ] **4.b** Real data source connected:
  - UC1: MDMS / AMISP system — live 15-min interval meter readings
  - UC2: ARR filing system — fiscal year cost line items
  - UC3: Tariff management system — current rate structures and slabs
- [ ] **4.c** `on_status` delivers real `dataPayload` (IES schema compliant) — not mock data
- [ ] **4.d** Dataset catalog published on the production network — discoverable by other participants
- [ ] **4.e** (BAP) Real consuming application integrated — processes `dataPayload` and ingests into internal systems

### Stage 5 — Production Infrastructure

*Goal: production-grade deployment with security, reliability, and observability.*

- [ ] **5.a** ONIX adapter deployed to production environment (GCP / on-premise) with production credentials
- [ ] **5.b** BPP server deployed with HTTPS, behind a load balancer
- [ ] **5.c** Secrets (signing keys, API keys) stored in a secrets manager — not in config files
- [ ] **5.d** Monitoring and alerting active for ONIX adapter health and data delivery SLA

### Stage 6 — Go-Live Verification

- [ ] **6.a** End-to-end exchange tested on production network with a real counterpart (not testnet mock)
- [ ] **6.b** Data integrity verified — delivered `dataPayload` matches source system data
- [ ] **6.c** DeDi hash anchoring confirmed on production datasets
- [ ] **6.d** Operations runbook prepared (key rotation, incident response, dataset updates)

---

*Reference: [IES Data Exchange Documentation](https://india-energy-stack.gitbook.io/docs/data-exchange) · [DEG Devkit](https://github.com/Beckn-One/DEG/tree/main/devkits/data-exchange) · [Beckn Protocol](https://becknprotocol.io)*
