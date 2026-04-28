# India Energy Stack
## IES Energy Data Exchange
### DISCOM / Organisation Readiness Checklist

**Name of Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ BAP (Data Consumer) &nbsp; ☐ BPP (Data Provider) &nbsp; ☐ Both

**Point of Contact:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

### 1. Testnet Access & Credentials

- [ ] **1.a** IES testnet credentials received (BAP/BPP ID, signing key pair)
- [ ] **1.b** Network ID confirmed: `nfh.global/testnet-deg`
- [ ] **1.c** Use case(s) identified: ☐ Meter Telemetry &nbsp; ☐ ARR Filings &nbsp; ☐ Tariff Policies

### 2. Infrastructure Setup

- [ ] **2.a** Docker and Docker Compose installed
- [ ] **2.b** DEG devkit cloned from GitHub
- [ ] **2.c** ONIX BAP adapter deployed and health check passing (port 8081)
- [ ] **2.d** ONIX BPP adapter deployed and health check passing (port 8082)
- [ ] **2.e** Adapter configs updated with testnet credentials (BAP/BPP ID, signing key)

### 3. Dataset Preparation

- [ ] **3.a** Dataset schema selected: `IES_Report` / `IES_ARR_Filing` / `IES_Policy` + `IES_Program`
- [ ] **3.b** Test dataset prepared and schema-compliant
- [ ] **3.c** (BPP only) Mock or real BPP server able to serve dataset in `on_status` response

### 4. Transaction Flow Integration

- [ ] **4.a** `select` → `on_select` exchange working (catalog returned)
- [ ] **4.b** `init` → `on_init` exchange working (contract activated)
- [ ] **4.c** `confirm` → `on_confirm` exchange working (contract locked)
- [ ] **4.d** `status` → `on_status` exchange working — dataset delivered in `dataPayload`
- [ ] **4.e** Automated test script (`test-workflow.sh`) passing for all applicable use cases

### 5. Application Integration

- [ ] **5.a** BAP application receiving `on_*` callbacks at webhook URL
- [ ] **5.b** `dataPayload` parsed and processed by consuming application
- [ ] **5.c** (BPP only) Real dataset delivery integrated — not just mock data

### 6. Go-Live

- [ ] **6.a** Testnet registration complete — discoverable by other participants
- [ ] **6.b** Production deployment planned (GCP / on-premise)
- [ ] **6.c** Monitoring and logging in place for ONIX adapter and application

---

*Reference: [IES Data Exchange Documentation](https://india-energy-stack.gitbook.io/docs/data-exchange) · [DEG Devkit](https://github.com/Beckn-One/DEG/tree/main/devkits/data-exchange)*
