# India Energy Stack
## IES Energy Data Exchange — Implementation Checklist
### Detailed Technical Reference: Testnet to Production

**Name of Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ BAP (Data Consumer) &nbsp; ☐ BPP (Data Provider) &nbsp; ☐ Both

**Technical Lead:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Use Cases:** &nbsp; ☐ UC1 Meter Telemetry &nbsp; ☐ UC2 ARR Filings &nbsp; ☐ UC3 Tariff Policies

---

## Stage 1 — Testnet Validation

*Complete this stage fully before moving to Stage 2. Testnet is a safe environment to catch integration issues.*

### Pre-requisites

- [ ] **1.0.a** Docker Engine (v24+) and Docker Compose installed
- [ ] **1.0.b** `curl`, `git`, and `python3` available in the terminal
- [ ] **1.0.c** ~2 GB free disk space for Docker images
- [ ] **1.0.d** IES testnet credentials received from IES team:
  - Testnet BAP ID: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  - Testnet BPP ID: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  - Ed25519 signing key pair: ☐ received
  - Network ID: `nfh.global/testnet-deg`

### Stack Setup

- [ ] **1.1** DEG devkit cloned:
  ```bash
  git clone https://github.com/Beckn-One/DEG.git
  cd DEG/devkits/data-exchange
  ```
- [ ] **1.2** Adapter configs updated with testnet credentials:
  - `config/local-simple-bap.yaml` → `participant_id`, `signing_key`, `callback_url`
  - `config/local-simple-bpp.yaml` → `participant_id`, `signing_key`
- [ ] **1.3** Bootcamp stack started:
  ```bash
  cd install
  docker compose -f docker-compose-bootcamp.yml up -d --build
  ```
- [ ] **1.4** All services healthy (wait ~15s after start):
  ```bash
  curl http://localhost:8081/health   # ONIX BAP → 200
  curl http://localhost:8082/health   # ONIX BPP → 200
  curl http://localhost:3001/api/health  # Sandbox BAP → 200
  curl http://localhost:3002/api/health  # Mock BPP → 200 + dataset list
  ```

### Use Case Testing

For each applicable use case, run the full 4-step exchange and verify the `dataPayload`:

**UC1 — Meter Telemetry (`IES_Report`)**
- [ ] **1.5.a** `test-workflow.sh usecase1` passes all 15 steps
- [ ] **1.5.b** `on_status` contains `IES_Report` with `payloadDescriptors`, `resources[]`, `intervals[]`
- [ ] **1.5.c** `intervalPeriod.duration` = `"PT15M"`, `payloads[].type` = `"USAGE"`, values are numbers

**UC2 — ARR Filings (`IES_ARR_Filing`)**
- [ ] **1.6.a** `test-workflow.sh usecase2` passes all 15 steps
- [ ] **1.6.b** `on_status` contains `IES_ARR_Filing` with `licensee`, `fiscalYears[]`, `lineItems[]`
- [ ] **1.6.c** `amountCrINR` fields are numbers; `year` follows `YYYY-YY` format

**UC3 — Tariff Policies (`IES_Policy` + `IES_Program`)**
- [ ] **1.7.a** `test-workflow.sh usecase3` passes all 15 steps
- [ ] **1.7.b** `on_status` contains `programs[]` and `policies[]` with `energySlabs[]`
- [ ] **1.7.c** Last energy slab has `toKWh: null`; surcharge percentages are signed numbers

**All use cases**
- [ ] **1.8** `test-workflow.sh all` passes end-to-end

### Testnet Sign-off

- [ ] **1.9** Postman collections imported and all requests run manually in order (select → init → confirm → status) for each applicable use case
- [ ] **1.10** At least one custom payload tested (modified date ranges or resource IDs) — not only the example files
- [ ] **1.11** Testnet validation sign-off — proceed to Stage 2: \_\_\_\_\_\_\_\_\_ (date)

---

## Stage 2 — DeDi Setup

*DeDi (Decentralised Data Infrastructure) anchors dataset hashes for provenance and enables dispute resolution. Set this up before network registration — your DeDi namespace is submitted as part of the registration package.*

### 2.1 Register a DeDi Namespace

- [ ] **2.1.a** DeDi namespace registration initiated at `dedi.global` for your organisation
- [ ] **2.1.b** Namespace name confirmed (typically your organisation identifier, e.g. `bescom` or `intelligrid`): \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **2.1.c** DeDi API key / write credentials received and stored in secrets manager
- [ ] **2.1.d** Namespace accessible — test a read against your namespace:
  ```bash
  curl https://dedi.global/dedi/query/{namespace}/vc-revocation-registry
  # Expected: empty registry or existing entries
  ```

### 2.2 Configure Dataset Hash Anchoring (BPP)

*At delivery time, the BPP computes and publishes a hash of the delivered dataset to DeDi. This allows the BAP (and any auditor) to verify that the data received is identical to what was sent.*

- [ ] **2.2.a** Hash computation implemented in BPP at delivery time:
  ```python
  import hashlib, json

  def compute_dataset_hash(data_payload: dict) -> str:
      canonical = json.dumps(data_payload, sort_keys=True, separators=(',', ':'))
      return hashlib.sha256(canonical.encode()).hexdigest()
  ```
- [ ] **2.2.b** Hash published to DeDi namespace after each successful `on_status` delivery:
  ```bash
  POST https://dedi.global/dedi/publish/{namespace}/datasets
  Authorization: Bearer {dedi_api_key}
  Content-Type: application/json

  {
    "transaction_id": "<beckn transaction_id>",
    "dataset_hash": "<sha256 of dataPayload>",
    "dataset_type": "IES_Report",
    "delivered_at": "<ISO 8601 timestamp>",
    "bap_id": "<BAP participant ID>",
    "bpp_id": "<BPP participant ID>"
  }
  ```
- [ ] **2.2.c** DeDi namespace URL included in `on_status` response so BAP can independently verify:
  ```json
  {
    "items": [{
      "dataPayload": { /* ... */ },
      "provenanceUrl": "https://dedi.global/dedi/query/{namespace}/datasets?txn={transaction_id}"
    }]
  }
  ```
- [ ] **2.2.d** Hash anchoring tested — BAP retrieves hash from DeDi and recomputes from received `dataPayload` → hashes match

### 2.3 Configure DeDi Verification (BAP)

- [ ] **2.3.a** BAP application reads `provenanceUrl` from `on_status` response
- [ ] **2.3.b** BAP fetches published hash from DeDi and recomputes hash of received `dataPayload`
- [ ] **2.3.c** Mismatch handling implemented — BAP raises an alert and initiates dispute if hashes don't match
- [ ] **2.3.d** DeDi lookup tested end-to-end with a testnet transaction before moving to production

---

## Stage 3 — Production Network Registration

*Register as a formal participant on the live IES Beckn network. Your DeDi namespace and public HTTPS endpoints must be in place before submitting this registration.*

### 3.1 Domain and TLS Setup

- [ ] **3.1.a** Production domain provisioned for your ONIX adapter (e.g. `beckn.{discom}.in`)
- [ ] **3.1.b** Valid TLS certificate issued and installed (Let's Encrypt or CA-signed)
- [ ] **3.1.c** HTTPS accessible from the public internet:
  ```bash
  curl https://beckn.{yourdomain}.in/health
  ```
- [ ] **3.1.d** BAP callback URL publicly reachable: `https://beckn.{yourdomain}.in/bap/receiver`
- [ ] **3.1.e** BPP receiver URL publicly reachable: `https://beckn.{yourdomain}.in/bpp/receiver`
- [ ] **3.1.f** Firewall allows inbound HTTPS from IES network infrastructure; outbound HTTPS to `dedi.global` and IES registry

### 3.2 Generate Production Signing Keys

- [ ] **3.2.a** **Separate** Ed25519 key pair generated for production — do **not** reuse testnet keys:
  ```bash
  openssl genpkey -algorithm ed25519 -out prod-signing-key.pem
  openssl pkey -in prod-signing-key.pem -pubout -out prod-signing-key-pub.pem
  ```
- [ ] **3.2.b** Private key stored in secrets manager (AWS Secrets Manager / GCP Secret Manager / HashiCorp Vault) — never in a config file or repository
- [ ] **3.2.c** Public key fingerprint noted: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### 3.3 Submit Registration to IES Team

- [ ] **3.3.a** Registration package submitted to IES team containing:
  - Organisation legal name
  - Role: BAP / BPP / both
  - Production public signing key (PEM)
  - BAP callback URL (where `on_*` responses arrive)
  - BPP endpoint URL (where Beckn requests arrive)
  - DeDi namespace name
  - Use case(s) being implemented
- [ ] **3.3.b** Production BAP ID assigned and noted: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **3.3.c** Production BPP ID assigned and noted: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **3.3.d** Production network ID confirmed: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] **3.3.e** Registry lookup confirmed — participant ID resolves to your public key and URLs on the production registry

---

## Stage 4 — Real Data Integration

*Replace the mock BPP with a production server connected to your actual data systems.*

### 4.1 Production BPP Server (BPP role only)

- [ ] **4.1.a** Production BPP server built in your language of choice (Python/Go/Node/Java)
- [ ] **4.1.b** All four Beckn actions implemented:
  - `POST /select` → return catalog of available datasets with access terms
  - `POST /init` → acknowledge and prepare contract
  - `POST /confirm` → activate contract, transition order to `CONFIRMED`
  - `POST /status` → deliver dataset — call ONIX BPP caller with `on_status` + `dataPayload`
- [ ] **4.1.c** Order state machine implemented: `DRAFT → SELECTED → INITIALIZED → CONFIRMED → DELIVERED`
- [ ] **4.1.d** `on_*` callbacks sent through ONIX BPP caller (not directly to BAP):
  ```bash
  POST http://localhost:8082/bpp/caller/on_status
  ```
- [ ] **4.1.e** `schemaContext` present in every response context:
  ```json
  { "context": { "schemaContext": "https://ies.energy/schemas/v1" } }
  ```
- [ ] **4.1.f** Nested `@context` fields stripped from `dataPayload` before sending (prevents ONIX validation errors)

### 4.2 Connect to Real Data Sources

**UC1 — Meter Telemetry**
- [ ] **4.2.a** MDMS / AMISP API connected — BPP can query 15-min interval kWh readings by meter ID and date range
- [ ] **4.2.b** Response mapped to `IES_Report` schema (OpenADR 3.1.0) — `resources[]`, `intervals[]`, `payloads[]`
- [ ] **4.2.c** Data freshness confirmed — readings are from live MDMS, not a static file
- [ ] **4.2.d** Large dataset handling tested — verified `dataPayload` size fits within Beckn message limits; chunking strategy decided if needed

**UC2 — ARR Filings**
- [ ] **4.2.e** ARR filing system / financial database connected — BPP can query cost line items by fiscal year and DISCOM
- [ ] **4.2.f** Response mapped to `IES_ARR_Filing` schema — `fiscalYears[]`, `lineItems[]`, `amountCrINR`
- [ ] **4.2.g** Filing version control handled — BAP always receives the latest submitted version, not a draft

**UC3 — Tariff Policies**
- [ ] **4.2.h** Tariff management system connected — SERC can serve current rate structures and energy slabs
- [ ] **4.2.i** Response mapped to `IES_Policy` + `IES_Program` schemas — `energySlabs[]`, `surchargeTariffs[]`
- [ ] **4.2.j** Effective date filtering implemented — only publish tariff policies that are currently in force

### 4.3 Dataset Catalog Publication

- [ ] **4.3.a** Catalog defined — lists all datasets your BPP can serve:
  ```json
  {
    "catalog": {
      "descriptor": { "name": "BESCOM Data Exchange" },
      "providers": [{
        "id": "bescom.discom.karnataka.ies.in",
        "items": [
          {
            "id": "bescom-ami-telemetry",
            "descriptor": { "name": "AMI Meter Telemetry", "code": "IES_Report" },
            "fulfillments": [{ "type": "INLINE" }]
          }
        ]
      }]
    }
  }
  ```
- [ ] **4.3.b** Catalog served correctly in `on_select` response
- [ ] **4.3.c** Catalog registered on IES production network discovery service — other participants can find your datasets via `select`

### 4.4 Production BAP Application (BAP role only)

- [ ] **4.4.a** BAP application sends Beckn messages to production ONIX BAP caller (not localhost — production URL)
- [ ] **4.4.b** BAP public callback URL receiving `on_*` responses from production network
- [ ] **4.4.c** `dataPayload` parsed and ingested into downstream systems:
  - UC1: meter readings loaded into internal MDMS or analytics system
  - UC2: ARR filing data loaded into regulatory processing system
  - UC3: tariff policy loaded into billing system (rate slabs applied)
- [ ] **4.4.d** DeDi hash verification integrated (see Stage 3.3)
- [ ] **4.4.e** Idempotency handled — duplicate `on_status` for the same `transaction_id` does not double-import data

---

## Stage 5 — Production Infrastructure

### 5.1 ONIX Adapter Deployment

- [ ] **5.1.a** ONIX adapters deployed to production environment — follow [`GCP-DEPLOY.md`](https://github.com/Beckn-One/DEG/blob/main/devkits/data-exchange/GCP-DEPLOY.md) for GCP or adapt for your platform
- [ ] **5.1.b** Production config files updated:
  - `network_id`: production network ID (from IES team)
  - `participant_id`: production BAP/BPP ID
  - `signing_key`: production Ed25519 private key (injected from secrets manager — never in file)
  - `callback_url`: production HTTPS callback URL
- [ ] **5.1.c** ONIX adapters deployed behind HTTPS reverse proxy (Nginx / Cloud Load Balancer)
- [ ] **5.1.d** Redis for ONIX message cache deployed with persistence enabled and memory limits set
- [ ] **5.1.e** Adapter restartable without losing in-flight transactions (Redis TTL configured appropriately)

### 5.2 Security

- [ ] **5.2.a** Production signing key never written to disk unencrypted — injected via secrets manager at runtime
- [ ] **5.2.b** All inter-service communication over HTTPS or within a private VPC
- [ ] **5.2.c** ONIX adapter not directly exposed to the internet — fronted by a load balancer or API gateway
- [ ] **5.2.d** Rate limiting applied to inbound Beckn endpoints (prevent flood from network)
- [ ] **5.2.e** Access to DeDi publish API restricted to BPP server only

### 5.3 Monitoring and Observability

- [ ] **5.3.a** ONIX adapter health (`/health`) polled every 60 seconds — alert on non-200
- [ ] **5.3.b** ONIX Prometheus metrics scraped (`/metrics`) — dashboard created for:
  - Message throughput (requests/min per action)
  - Signature verification failure rate
  - Callback delivery latency
- [ ] **5.3.c** Application-level SLA alert: `on_status` not received within 60 seconds of `status` call
- [ ] **5.3.d** DeDi publish failures alerted — dataset delivered but hash not anchored is a data integrity risk
- [ ] **5.3.e** Structured logging in place — every Beckn transaction logged with `transaction_id`, `action`, `bap_id`, `bpp_id`, timestamp, status. No dataset payload content in logs.

---

## Stage 6 — Go-Live Verification

### 6.1 Production Integration Test

- [ ] **6.1.a** End-to-end exchange completed on the production network with a real counterpart organisation (not testnet mock)
- [ ] **6.1.b** All four Beckn steps confirmed working on production: select → init → confirm → status
- [ ] **6.1.c** `dataPayload` received by BAP matches source system data — spot-checked against raw source

### 6.2 Data Integrity Verification

- [ ] **6.2.a** DeDi hash anchored for the test transaction — confirmed visible at `dedi.global`
- [ ] **6.2.b** BAP recomputed hash from received `dataPayload` → matches DeDi-anchored hash
- [ ] **6.2.c** Tamper test — modified `dataPayload` hash does **not** match DeDi record (hash mismatch detection works)

### 6.3 Operations Readiness

- [ ] **6.3.a** Key rotation runbook written and tested:
  - Generate new Ed25519 key pair
  - Register new public key with IES network registry
  - Update secrets manager
  - Rolling restart of ONIX adapter with new key
  - Confirm registry updated — old key no longer used
- [ ] **6.3.b** Incident response runbook covers:
  - ONIX adapter failure — restart procedure, in-flight transaction recovery
  - Data source outage — graceful error response to BAP (`on_status` with error, not a hang)
  - DeDi unavailable — delivery proceeds; hash anchoring retried asynchronously
- [ ] **6.3.c** Dataset update procedure defined (BPP):
  - How catalog is updated when new datasets become available
  - How existing consumers are notified of new dataset versions
- [ ] **6.3.d** Log retention policy confirmed — transaction IDs and metadata retained for audit; no PII or dataset content in logs

---

## Troubleshooting Reference

| Symptom | First thing to check |
|---|---|
| `connection refused` on ONIX ports | `docker logs onix-bap` — check for config parse errors or key load failure |
| ACK returned but no `on_*` callback | Check routing config points to correct BPP URL; check `docker logs mock-bpp` |
| `domain not allowed` in ONIX logs | BPP sending nested `@context` in `dataPayload` — strip before sending |
| Schema validation error | `schemaContext` missing from request context field |
| Signature verification failed on production | Production signing key in config doesn't match key registered on production registry |
| DeDi hash mismatch | Canonicalization differs between BPP (publisher) and BAP (verifier) — ensure `sort_keys=True, separators=(',', ':')` on both sides |
| BAP not receiving `on_status` | Confirm BAP callback URL is publicly reachable from the network; check firewall |
| Testnet works but production fails | Confirm `network_id` and `participant_id` in config are production values, not testnet sandbox values |

---

*Reference: [IES Data Exchange Documentation](https://india-energy-stack.gitbook.io/docs/data-exchange) · [DEG Devkit](https://github.com/Beckn-One/DEG/tree/main/devkits/data-exchange) · [DDM DatasetItem Schema](https://github.com/beckn/DDM) · [Beckn Protocol](https://becknprotocol.io)*
