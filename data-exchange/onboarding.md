# Onboarding Guide — Data Exchange

This guide walks you through everything required to join the IES Data Exchange network, whether you are a data consumer (BAP) or data provider (BPP).

---

## Choose Your Role

| Role | You are | You do |
|---|---|---|
| **BAP** (Beckn Application Platform) | DISCOM, regulator, VAS provider, researcher | Discover and consume datasets published by BPPs |
| **BPP** (Beckn Provider Platform) | AMISP, DISCOM, SERC, data custodian | Publish and deliver datasets to BAPs |
| **Both** | DISCOM (receives meter data AND submits ARR filings) | Run both a BAP and a BPP adapter |

---

## Prerequisites

For either role:

- [ ] Docker and Docker Compose installed
- [ ] `curl` or Postman for testing
- [ ] ~2 GB disk space for Docker images
- [ ] IES testnet credentials (BAP ID, BPP ID, signing keys) — request from the IES team
- [ ] Git (to clone the devkit)

---

## Step 1 — Get Testnet Credentials

Contact the IES team to receive:

| Credential | Description |
|---|---|
| `bap_id` / `bpp_id` | Your network identity on the IES testnet |
| `bap_uri` / `bpp_uri` | Public URL where your ONIX adapter receives callbacks |
| Signing key pair | Ed25519 keys used by ONIX to sign Beckn messages |
| API key | For authenticating calls to the IES registry |

For local development, the devkit ships with sandbox credentials (`bap.example.com` / `bpp.example.com`) that work against the testnet mock infrastructure.

---

## Step 2 — Clone the Devkit

```bash
git clone https://github.com/Beckn-One/DEG.git
cd DEG/devkits/data-exchange
```

The devkit structure:

```
data-exchange/
├── config/                      # ONIX adapter configs (BAP + BPP)
├── install/
│   ├── docker-compose-adapter.yml      # full stack (real BPP)
│   └── docker-compose-bootcamp.yml     # bootcamp stack (mock BPP)
├── scripts/
│   ├── test-workflow.sh                # curl-based test runner
│   └── generate_postman_collection.py
├── usecase1/                    # Meter telemetry
├── usecase2/                    # ARR filings
└── usecase3/                    # Tariff policies
```

---

## Step 3 — Configure the Adapters

Edit the adapter configs in `config/` to replace the sandbox credentials with your testnet credentials:

**`config/local-simple-bap.yaml`** (BAP side):
```yaml
network_id: nfh.global/testnet-deg
participant_id: your-bap-id.example.com        # replace
signing_key: <your Ed25519 private key>        # replace
callback_url: https://your-bap-domain/bap/receiver  # replace
```

**`config/local-simple-bpp.yaml`** (BPP side):
```yaml
network_id: nfh.global/testnet-deg
participant_id: your-bpp-id.example.com        # replace
signing_key: <your Ed25519 private key>        # replace
```

For local development with sandbox credentials, no edits are required.

---

## Step 4 — Start the Stack

### Option A — Bootcamp Stack (recommended for getting started)

Includes a **Mock BPP** that auto-responds with real IES test data. No real BPP required.

```bash
cd install
docker compose -f docker-compose-bootcamp.yml up -d --build
```

Services started:

| Service | Port | Description |
|---|---|---|
| `redis` | 6379 | Message cache |
| `onix-bap` | 8081 | BAP adapter |
| `onix-bpp` | 8082 | BPP adapter |
| `sandbox-bap` | 3001 | BAP webhook receiver (logs `on_*` callbacks) |
| `mock-bpp` | 3002 | Mock BPP — auto-responds with IES data |

### Option B — Full Stack (for building a real BPP)

```bash
cd install
docker compose -f docker-compose-adapter.yml up -d
```

This starts only the ONIX adapters (no mock BPP). You bring your own BPP server.

---

## Step 5 — Verify Services

```bash
curl http://localhost:8081/health   # BAP adapter
curl http://localhost:8082/health   # BPP adapter
curl http://localhost:3001/api/health  # Sandbox BAP webhook
curl http://localhost:3002/api/health  # Mock BPP (shows loaded datasets)
```

All should return `{"status": "ok"}`.

---

## Step 6 — Run Your First Exchange

Use the automated test script:

```bash
cd ..
./scripts/test-workflow.sh usecase1    # meter telemetry (15 steps)
./scripts/test-workflow.sh usecase2    # ARR filings (15 steps)
./scripts/test-workflow.sh usecase3    # tariff policies (15 steps)
./scripts/test-workflow.sh all         # all three
```

Or run manually (see [Quick Start](./quick-start.md)).

---

## Step 7 — Register on the IES Testnet

To be discoverable by other participants on the testnet (not required for local testing):

1. Share your `bap_id`/`bpp_id` and public signing key with the IES team
2. The IES team registers you on the testnet registry
3. Other participants can now discover your published datasets via the `select` call

---

## For BPP Implementors — Building Your Provider

If you are publishing real data (not using the mock BPP), you need to build a server that:

1. Receives Beckn `select`, `init`, `confirm`, `status` calls from ONIX (via HTTP POST)
2. Returns `on_*` responses through the ONIX BPP caller

### Minimum BPP Interface

```
POST /select     → respond with on_select (catalog listing)
POST /init       → respond with on_init (ready to fulfill)
POST /confirm    → respond with on_confirm (contract active)
POST /status     → respond with on_status (data payload)
```

The `on_status` response embeds your dataset inline:

```json
{
  "context": { "action": "on_status", /* ... */ },
  "message": {
    "order": {
      "status": "DELIVERY_COMPLETE",
      "items": [
        {
          "id": "amisp-meter-data-ka-2026-q1",
          "dataPayload": { /* IES_Report, IES_ARR_Filing, or tariff schemas */ },
          "accessMethod": "INLINE"
        }
      ]
    }
  }
}
```

For a full reference implementation, see the [Mock BPP source](https://github.com/Beckn-One/DEG/blob/main/devkits/data-exchange/mock-bpp/app.py) — a FastAPI application handling all three use cases.

---

## For BAP Implementors — Consuming Data

Instead of using the sandbox BAP webhook, build your own application that:

1. Sends `select`, `init`, `confirm`, `status` to the ONIX BAP caller at `http://localhost:8081/bap/caller/{action}`
2. Receives `on_*` callbacks at your registered webhook URL
3. Parses the `dataPayload` from `on_status`

See [Quick Start](./quick-start.md) for the full `curl` sequence and expected responses.

---

## Postman Alternative

Import the Postman collections from each use case's `postman/` directory:

```
usecase1/postman/data-exchange-usecase1.BAP-DEG.postman_collection.json
usecase2/postman/data-exchange-usecase2.BAP-DEG.postman_collection.json
usecase3/postman/data-exchange-usecase3.BAP-DEG.postman_collection.json
```

Set these collection variables:

| Variable | Value |
|---|---|
| `bap_adapter_url` | `http://localhost:8081/bap/caller` |
| `bap_id` | `bap.example.com` |
| `bap_uri` | `http://onix-bap:8081/bap/receiver` |
| `bpp_id` | `bpp.example.com` |
| `bpp_uri` | `http://onix-bpp:8082/bpp/receiver` |
| `transaction_id` | *(any UUID)* |

Run requests in order: `select` → `init` → `confirm` → `status`.

---

## Checklist Summary

### BAP (Data Consumer)
- [ ] Testnet credentials received
- [ ] Devkit cloned
- [ ] Adapter config updated
- [ ] Bootcamp stack running (all 4 services healthy)
- [ ] `test-workflow.sh usecase1` passes
- [ ] Registered on testnet registry

### BPP (Data Provider)
- [ ] Testnet credentials received
- [ ] Devkit cloned
- [ ] Adapter config updated
- [ ] BPP server built (or using mock-bpp)
- [ ] `test-workflow.sh` passes end-to-end
- [ ] Datasets published and discoverable on testnet
