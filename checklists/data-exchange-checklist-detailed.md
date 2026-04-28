# India Energy Stack
## IES Energy Data Exchange — Implementation Checklist
### Detailed Technical Reference for Integration Teams

**Name of Organisation:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Role:** &nbsp; ☐ BAP (Data Consumer) &nbsp; ☐ BPP (Data Provider) &nbsp; ☐ Both

**Technical Lead:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Email:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Use Case(s):**  ☐ UC1 Meter Telemetry &nbsp; ☐ UC2 ARR Filings &nbsp; ☐ UC3 Tariff Policies

---

## Phase 0 — Pre-requisites

- [ ] **0.a** Docker Engine (v24+) and Docker Compose installed on the deployment host
- [ ] **0.b** `curl` and `git` available
- [ ] **0.c** ~2 GB free disk space for Docker images
- [ ] **0.d** IES testnet credentials received from IES team:
  - BAP ID: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  - BPP ID: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  - Ed25519 signing key pair: \_\_\_ received
  - Network ID confirmed as `nfh.global/testnet-deg`
- [ ] **0.e** Role confirmed — determines which adapters and configs you need:

| Role | Adapter needed | Config file |
|---|---|---|
| BAP only | ONIX BAP (port 8081) | `local-simple-bap.yaml` |
| BPP only | ONIX BPP (port 8082) | `local-simple-bpp.yaml` |
| Both | Both adapters | Both config files |

---

## Phase 1 — Repository Setup

- [ ] **1.a** DEG devkit cloned:
  ```bash
  git clone https://github.com/Beckn-One/DEG.git
  cd DEG/devkits/data-exchange
  ```
- [ ] **1.b** Directory structure confirmed:
  ```
  data-exchange/
  ├── config/        ← adapter configs to edit
  ├── install/       ← docker-compose files
  ├── scripts/       ← test-workflow.sh
  ├── usecase1/      ← meter telemetry examples
  ├── usecase2/      ← ARR filings examples
  └── usecase3/      ← tariff policies examples
  ```

---

## Phase 2 — Adapter Configuration

### 2.1 BAP Adapter Config (skip if BPP only)

- [ ] **2.1.a** Edit `config/local-simple-bap.yaml`:
  - [ ] `network_id` set to `nfh.global/testnet-deg`
  - [ ] `participant_id` set to your BAP ID (from IES team)
  - [ ] `signing_key` set to your Ed25519 private key
  - [ ] `callback_url` set to the public URL where your app receives `on_*` callbacks
- [ ] **2.1.b** For local development with sandbox credentials: no edits needed — sandbox values work against testnet mock

### 2.2 BPP Adapter Config (skip if BAP only)

- [ ] **2.2.a** Edit `config/local-simple-bpp.yaml`:
  - [ ] `network_id` set to `nfh.global/testnet-deg`
  - [ ] `participant_id` set to your BPP ID (from IES team)
  - [ ] `signing_key` set to your Ed25519 private key
- [ ] **2.2.b** Edit routing config (`local-simple-routing-BPPReceiver.yaml`) to point to your BPP server URL

---

## Phase 3 — Stack Deployment

### 3.1 Start the Stack

- [ ] **3.1.a** Choose deployment mode:
  - **Bootcamp/development** (mock BPP included — recommended for initial testing):
    ```bash
    cd install
    docker compose -f docker-compose-bootcamp.yml up -d --build
    ```
  - **Full stack** (you bring your own BPP server):
    ```bash
    cd install
    docker compose -f docker-compose-adapter.yml up -d
    ```

### 3.2 Verify All Services Healthy

- [ ] **3.2.a** Wait 15 seconds for ONIX to initialise, then run all health checks:
  ```bash
  curl http://localhost:8081/health         # ONIX BAP
  curl http://localhost:8082/health         # ONIX BPP
  curl http://localhost:3001/api/health     # Sandbox BAP webhook
  curl http://localhost:3002/api/health     # Mock BPP
  ```
- [ ] **3.2.b** All return HTTP 200 — note: mock BPP `/api/health` also shows loaded dataset names
- [ ] **3.2.c** If any service fails: check logs
  ```bash
  docker logs onix-bap    # check for config errors
  docker logs mock-bpp    # check for startup errors
  ```

---

## Phase 4 — Use Case Integration

Work through each use case you selected. Steps are the same for all three — only the example files and `dataPayload` schema differ.

### 4.1 Use Case 1 — Meter Telemetry (`IES_Report`) *(skip if not applicable)*

**Context:** AMISP (BPP) → DISCOM (BAP). Dataset: 15-minute kWh interval readings in OpenADR 3.1.0 format.

- [ ] **4.1.a** Run `select` step:
  ```bash
  curl -s -X POST http://localhost:8081/bap/caller/select \
    -H "Content-Type: application/json" \
    -d @usecase1/examples/select-request.json | python3 -m json.tool
  ```
  Expected: `{"message":{"ack":{"status":"ACK"}}}`

- [ ] **4.1.b** Confirm `on_select` callback received — check sandbox BAP logs:
  ```bash
  docker logs sandbox-bap 2>&1 | grep on_select | tail -5
  ```
  Expected: log entry showing catalog with `IES_Report` dataset item

- [ ] **4.1.c** Run `init` step:
  ```bash
  curl -s -X POST http://localhost:8081/bap/caller/init \
    -H "Content-Type: application/json" \
    -d @usecase1/examples/init-request.json | python3 -m json.tool
  ```
  Expected: `{"message":{"ack":{"status":"ACK"}}}`

- [ ] **4.1.d** Run `confirm` step:
  ```bash
  curl -s -X POST http://localhost:8081/bap/caller/confirm \
    -H "Content-Type: application/json" \
    -d @usecase1/examples/confirm-request.json | python3 -m json.tool
  ```
  Expected: `{"message":{"ack":{"status":"ACK"}}}`

- [ ] **4.1.e** Run `status` step:
  ```bash
  curl -s -X POST http://localhost:8081/bap/caller/status \
    -H "Content-Type: application/json" \
    -d @usecase1/examples/status-request.json | python3 -m json.tool
  ```
  Expected: `{"message":{"ack":{"status":"ACK"}}}`

- [ ] **4.1.f** Confirm `on_status` contains `IES_Report` payload:
  ```bash
  docker logs sandbox-bap 2>&1 | tail -80
  # Look for "dataPayload" with "payloadDescriptors" and "resources" fields
  ```
- [ ] **4.1.g** Validate `dataPayload` structure:
  - [ ] `payloadDescriptors[0].payloadType` = `"USAGE"`
  - [ ] `payloadDescriptors[0].units` = `"KWH"`
  - [ ] `resources[]` contains at least one meter entry
  - [ ] Each meter has `intervals[]` with `intervalPeriod.duration` = `"PT15M"`
  - [ ] Each interval has `payloads[].values` = array of kWh readings

- [ ] **4.1.h** Automated test passing:
  ```bash
  ./scripts/test-workflow.sh usecase1
  # Expected: ✓ usecase1: All 15 steps passed
  ```

### 4.2 Use Case 2 — ARR Filings (`IES_ARR_Filing`) *(skip if not applicable)*

**Context:** DISCOM (BPP) → Regulator/SERC (BAP). Dataset: fiscal year cost line items.

- [ ] **4.2.a** Run `select` → `init` → `confirm` → `status` with `usecase2/examples/` files (same curl pattern as 4.1.a–e, replace `usecase1` with `usecase2`)
- [ ] **4.2.b** Confirm `on_status` contains `IES_ARR_Filing` payload:
  - [ ] `licensee` field present
  - [ ] `regulatoryCommission` field present
  - [ ] `fiscalYears[]` contains at least one year
  - [ ] Each fiscal year has `lineItems[]` with `category` and `amountCrINR` fields
- [ ] **4.2.c** Automated test passing:
  ```bash
  ./scripts/test-workflow.sh usecase2
  ```

### 4.3 Use Case 3 — Tariff Policies (`IES_Policy` + `IES_Program`) *(skip if not applicable)*

**Context:** SERC (BPP) → DISCOM (BAP). Dataset: machine-readable tariff rate structures.

- [ ] **4.3.a** Run `select` → `init` → `confirm` → `status` with `usecase3/examples/` files
- [ ] **4.3.b** Confirm `on_status` contains combined tariff payload:
  - [ ] `programs[]` array present — each entry has `id`, `name`, `consumerCategory`
  - [ ] `policies[]` array present — each entry has `programId`, `energySlabs[]`
  - [ ] `energySlabs[]` entries have `fromKWh`, `toKWh` (null for open-ended), `ratePerKWh`
  - [ ] `surchargeTariffs[]` present with `period`, `timeRange`, `surchargePercent`
- [ ] **4.3.c** Automated test passing:
  ```bash
  ./scripts/test-workflow.sh usecase3
  ```

---

## Phase 5 — Application Integration

### 5.1 BAP Application (skip if BPP only)

- [ ] **5.1.a** BAP application sends Beckn messages to ONIX BAP caller:
  - Endpoint: `POST http://localhost:8081/bap/caller/{action}`
  - Actions: `select`, `init`, `confirm`, `status`
  - `Content-Type: application/json`
- [ ] **5.1.b** BAP application registers a webhook to receive `on_*` callbacks:
  - URL registered in `config/local-simple-bap.yaml` as `callback_url`
  - Application handles: `on_select`, `on_init`, `on_confirm`, `on_status`
- [ ] **5.1.c** `dataPayload` correctly parsed from `on_status` response:
  - UC1: `IES_Report` parsed — meter readings extracted and ingested
  - UC2: `IES_ARR_Filing` parsed — cost line items extracted
  - UC3: `programs` + `policies` parsed — tariff slabs loaded into billing system
- [ ] **5.1.d** `transaction_id` tracked across all four steps of a single exchange
- [ ] **5.1.e** Application handles async pattern correctly — does not block on ACK waiting for data

### 5.2 BPP Server (skip if BAP only)

- [ ] **5.2.a** BPP server receives inbound Beckn calls routed by ONIX:
  - `POST /select` — return dataset catalog
  - `POST /init` — confirm readiness
  - `POST /confirm` — activate contract, transition state to `CONFIRMED`
  - `POST /status` — deliver `dataPayload` inline in `on_status`
- [ ] **5.2.b** Order state machine implemented: `DRAFT → SELECTED → INITIALIZED → CONFIRMED → DELIVERED`
- [ ] **5.2.c** `on_status` response sends `dataPayload` correctly:
  ```json
  {
    "message": {
      "order": {
        "status": "DELIVERY_COMPLETE",
        "items": [{
          "id": "<dataset-id>",
          "accessMethod": "INLINE",
          "dataPayload": { /* IES schema data */ }
        }]
      }
    }
  }
  ```
- [ ] **5.2.d** `schemaContext` present in request context:
  ```json
  { "context": { "schemaContext": "https://ies.energy/schemas/v1" } }
  ```
- [ ] **5.2.e** Nested `@context` fields stripped from `dataPayload` before sending (prevents ONIX schema validation errors — see [beckn-onix#655](https://github.com/beckn/beckn-onix/issues/655))
- [ ] **5.2.f** BPP sends `on_*` callbacks through ONIX BPP caller:
  - Endpoint: `POST http://localhost:8082/bpp/caller/{on_action}`

---

## Phase 6 — Schema Validation

- [ ] **6.a** `IES_Report` payload validated against OpenADR 3.1.0 schema:
  - `intervalPeriod.duration` uses ISO 8601 duration format (e.g. `PT15M`)
  - `payloads[].values` is an array of numbers
- [ ] **6.b** `IES_ARR_Filing` payload validated:
  - `amountCrINR` fields are numbers (not strings)
  - `fiscalYears[].year` follows `YYYY-YY` format (e.g. `"2026-27"`)
- [ ] **6.c** `IES_Policy`/`IES_Program` payload validated:
  - `toKWh: null` used for open-ended energy slab (last slab)
  - `surchargePercent` is a signed number (negative for off-peak discount)
- [ ] **6.d** ONIX schema validation not failing — no `domain not allowed` errors in ONIX logs

---

## Phase 7 — Testing Sign-off

- [ ] **7.a** `test-workflow.sh all` completes with all steps passing for all configured use cases
- [ ] **7.b** Each use case tested with at least one custom payload (not just the example files)
- [ ] **7.c** Network interruption tested — ONIX retry behaviour confirmed
- [ ] **7.d** Invalid `transaction_id` tested — ONIX rejects with appropriate error

---

## Phase 8 — Testnet Registration & Go-Live

- [ ] **8.a** Public signing key shared with IES team for testnet registry registration
- [ ] **8.b** Registered on testnet — confirmed discoverable via `select` from another participant
- [ ] **8.c** (BPP) Published at least one real dataset on the testnet
- [ ] **8.d** Production deployment environment chosen: ☐ GCP &nbsp; ☐ On-premise &nbsp; ☐ Other: \_\_\_\_\_
  - [ ] GCP deployment: follow [`GCP-DEPLOY.md`](https://github.com/Beckn-One/DEG/blob/main/devkits/data-exchange/GCP-DEPLOY.md)
- [ ] **8.e** Monitoring configured:
  - ONIX BAP/BPP adapter health endpoints polled every 60s
  - Alert on adapter restart or health check failure
  - Alert on `on_status` not received within 60s of `status` call (data delivery SLA)
- [ ] **8.f** Postman collections imported for manual testing and debugging:
  - `usecase1/postman/data-exchange-usecase1.BAP-DEG.postman_collection.json`
  - `usecase2/postman/data-exchange-usecase2.BAP-DEG.postman_collection.json`
  - `usecase3/postman/data-exchange-usecase3.BAP-DEG.postman_collection.json`
- [ ] **8.g** Internal runbook prepared:
  - How to restart ONIX adapters without losing in-flight transactions
  - How to rotate signing keys and re-register on testnet
  - How to debug missing `on_*` callbacks (check adapter logs, check routing config)

---

## Troubleshooting Reference

| Symptom | First thing to check |
|---|---|
| `connection refused` on 8081 or 8082 | `docker logs onix-bap` — wait 15s for initialisation |
| ACK returned but no `on_*` callback | `docker logs mock-bpp` — check for routing or schema errors |
| `domain not allowed` in ONIX logs | BPP is including nested `@context` in `dataPayload` — strip them |
| Schema validation error | `schemaContext` missing from request `context` field |
| Signature verification failed | Signing key in config doesn't match key registered on testnet |
| `test-workflow.sh` step fails at `on_status` | Check `docker logs mock-bpp` — state machine may be out of sequence |

---

*Reference: [IES Data Exchange Documentation](https://india-energy-stack.gitbook.io/docs/data-exchange) · [DEG Devkit](https://github.com/Beckn-One/DEG/tree/main/devkits/data-exchange) · [DDM DatasetItem Schema](https://github.com/beckn/DDM/tree/main/specification/schema/DatasetItem/v1)*
