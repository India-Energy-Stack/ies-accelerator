# Quick Start — Data Exchange

Get a complete data exchange running in under 10 minutes using the bootcamp stack (local Docker, mock BPP with real IES test data).

---

## Prerequisites

- Docker and Docker Compose installed
- `curl` available in your terminal
- Git

---

## 1. Clone and Navigate

```bash
git clone https://github.com/Beckn-One/DEG.git
cd DEG/devkits/data-exchange
```

---

## 2. Start the Bootcamp Stack

```bash
cd install
docker compose -f docker-compose-bootcamp.yml up -d --build
```

Wait ~15 seconds for ONIX to initialise, then verify all services:

```bash
curl http://localhost:8081/health      # → {"status":"ok"}
curl http://localhost:8082/health      # → {"status":"ok"}
curl http://localhost:3001/api/health  # → {"status":"ok"}
curl http://localhost:3002/api/health  # → {"status":"ok","datasets":["IES_Report","IES_ARR_Filing","IES_TariffIntelligence"]}
```

---

## 3. Run a Complete Exchange — Meter Telemetry

The Beckn protocol is a four-step sequence. Run each step and check the response.

### Step 1 — Select (browse available datasets)

```bash
curl -s -X POST http://localhost:8081/bap/caller/select \
  -H "Content-Type: application/json" \
  -d @usecase1/examples/select-request.json | python3 -m json.tool
```

Expected: `{"message":{"ack":{"status":"ACK"}}}`

The mock BPP receives this and sends `on_select` back through ONIX with the dataset catalog. Check the sandbox BAP logs:

```bash
docker logs sandbox-bap 2>&1 | grep on_select | tail -5
```

### Step 2 — Init (activate the contract)

```bash
curl -s -X POST http://localhost:8081/bap/caller/init \
  -H "Content-Type: application/json" \
  -d @usecase1/examples/init-request.json | python3 -m json.tool
```

Expected: `{"message":{"ack":{"status":"ACK"}}}`

### Step 3 — Confirm (lock the contract)

```bash
curl -s -X POST http://localhost:8081/bap/caller/confirm \
  -H "Content-Type: application/json" \
  -d @usecase1/examples/confirm-request.json | python3 -m json.tool
```

Expected: `{"message":{"ack":{"status":"ACK"}}}`

### Step 4 — Status (receive the data)

```bash
curl -s -X POST http://localhost:8081/bap/caller/status \
  -H "Content-Type: application/json" \
  -d @usecase1/examples/status-request.json | python3 -m json.tool
```

Expected: `{"message":{"ack":{"status":"ACK"}}}`

### Check the Data Arrived

The `on_status` callback arrives at the sandbox BAP. Inspect it:

```bash
docker logs sandbox-bap 2>&1 | tail -80
```

Look for `dataPayload` in the output — it contains the `IES_Report` with 15-minute interval meter readings.

Or check what the mock BPP sent:

```bash
docker logs mock-bpp 2>&1 | tail -30
```

---

## 4. Run the Automated Test

The test script runs all 15 steps (select → init → confirm → status + 11 intermediate verifications) in sequence:

```bash
cd ..
./scripts/test-workflow.sh usecase1
```

Successful output ends with:
```
✓ usecase1: All 15 steps passed
```

---

## 5. Try the Other Use Cases

```bash
# Use Case 2: ARR Filings (DISCOM → Regulator)
./scripts/test-workflow.sh usecase2

# Use Case 3: Tariff Policies (SERC → DISCOM)
./scripts/test-workflow.sh usecase3

# All three in sequence
./scripts/test-workflow.sh all
```

---

## 6. Inspect the Payloads

To see the actual IES data in a response, extract the `dataPayload`:

```bash
# Get on_status log from sandbox-bap and extract dataPayload
docker logs sandbox-bap 2>&1 | \
  python3 -c "
import sys, json
for line in sys.stdin:
    try:
        msg = json.loads(line)
        if 'dataPayload' in str(msg):
            print(json.dumps(msg, indent=2))
            break
    except: pass
"
```

---

## 7. Stop the Stack

```bash
cd install
docker compose -f docker-compose-bootcamp.yml down
```

---

## Next Steps

| Goal | Where to go |
|---|---|
| Understand the Beckn message format | [Core Concepts](./concepts.md) |
| Build your own BAP application | [Onboarding Guide](./onboarding.md#for-bap-implementors) |
| Build your own BPP / data provider | [Onboarding Guide](./onboarding.md#for-bpp-implementors) |
| Deep dive into a specific use case | [Use Cases](./use-cases/README.md) |
| Deploy to GCP | [`GCP-DEPLOY.md`](https://github.com/Beckn-One/DEG/blob/main/devkits/data-exchange/GCP-DEPLOY.md) |

---

## Using Postman Instead of curl

Import the collection:
```
usecase1/postman/data-exchange-usecase1.BAP-DEG.postman_collection.json
```

Set collection variables:

| Variable | Value |
|---|---|
| `bap_adapter_url` | `http://localhost:8081/bap/caller` |
| `bap_id` | `bap.example.com` |
| `bap_uri` | `http://onix-bap:8081/bap/receiver` |
| `bpp_id` | `bpp.example.com` |
| `bpp_uri` | `http://onix-bpp:8082/bpp/receiver` |
| `transaction_id` | *(generate any UUID)* |

Run requests in order: **select → init → confirm → status**.
