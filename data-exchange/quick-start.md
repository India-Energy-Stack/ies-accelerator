# Quick Start — Data Exchange

Run a working data exchange against the devkit's local sandbox in under 10 minutes — no real registry, no production credentials. This page also doubles as the onboarding checklist; the registry/production steps live on [Registry Setup](./registry-setup.md).

---

## 1. Pick your role and the flow shape

| You are | You run | You consume |
|---|---|---|
| **BAP** — Data Consumer (DISCOM, regulator, VAS provider, researcher) | BAP-side adapter + your application | Datasets published by BPPs |
| **BPP** — Data Provider (AMISP, DISCOM, SERC, data custodian) | BPP-side adapter + your provider implementation | (You serve) |
| Both | Both stacks | Datasets in both directions |

Not every Beckn action is needed. Pick the simplest flow that meets your case:

| Flow shape | Actions you need | When to use |
|---|---|---|
| **Minimal** | `confirm` → `on_confirm` (payload inline) | Pre-agreed bilateral exchange, one-shot delivery |
| Negotiated | + `select` / `init` before `confirm` | Terms (price, SLA, delivery mode) need agreement |
| Discoverable | + `publish-catalog` (BPP), `discover` (BAP) | Consumer doesn't yet know the provider |
| Async delivery | + `status` / `on_status` after `on_confirm` | Payload prepared asynchronously |
| Post-fulfilment | + `update` / `on_update` | Credential rotation, contract amendments |

---

## 2. Prerequisites

- Docker and Docker Compose
- Postman *(or `curl`)*
- Git
- ~2 GB free disk space for images

For local sandbox use, the devkit ships pre-configured identities (`bap.example.com` / `bpp.example.com`) — no real credentials needed. For real-network use, see [Registry Setup](./registry-setup.md).

---

## 3. Clone and start the stack

```bash
git clone https://github.com/beckn/DEG.git
cd DEG/devkits/data-exchange/install
docker compose up -d
```

Verify the services are up:

```bash
docker compose ps
curl http://localhost:8081/health    # onix-bap
curl http://localhost:8082/health    # onix-bpp
curl http://localhost:9000/health    # beckn-router
```

The stack lays out as in [Architecture](./architecture.md): `beckn-router:9000` is the bridge; each side runs `onix-{bap,bpp}` + `sandbox-{bap,bpp}` + redis.

---

## 4. Run the minimal exchange (`confirm` → `on_confirm`)

The minimal sanity check is one round-trip. From the BAP Postman collection, fire `confirm` and watch for `on_confirm` arriving back — that exercises sign → route → verify on both sides end-to-end.

### Import the collections

Each use case ships its own BAP and BPP Postman collections:

```
devkits/data-exchange/uc1-meter-data/postman/data-exchange-uc1-meter-data.{BAP,BPP}-DEG.postman_collection.json
devkits/data-exchange/uc2-regulatory-data/postman/data-exchange-uc2-regulatory-data.{BAP,BPP}-DEG.postman_collection.json
```

Import the **BAP** collection for the use case you care about (UC1 meter data or UC2 ARR filings).

### Set collection variables

| Variable | Local sandbox value |
|---|---|
| `bap_host_root` | `http://beckn-router:9000` *(in-stack)* or `http://localhost:9000` |
| `bpp_host_root` | `http://beckn-router:9000` *(in-stack)* or `http://localhost:9000` |

For a public tunnel (ngrok) or a deployed router, set both to that hostname. The Caddy router on `:9000` is the only public-facing port.

### Send `confirm` and verify

1. In Postman, open the BAP collection's `confirm` request and click **Send**. Expect `{"status":"ACK"}`.
2. Tail the BAP sandbox logs to see the matching callback:
   ```bash
   docker logs sandbox-bap 2>&1 | grep on_confirm | tail -5
   ```
3. The `on_confirm` body carries the dataset (for INLINE delivery) or a delivery handle. That's your end-to-end signal.

---

## 5. (Optional) Add other steps

The same Postman collection ships requests for the other actions; run them only when your use case needs them:

- `publish-catalog` (BPP collection) + `discover` (BAP) — for unknown providers
- `select` / `init` — for negotiated terms
- `status` / `on_status` — for asynchronous delivery (UC1 inline meter data flows often use this)
- `update` / `on_update` — for credential rotation

Each use case page lists which steps it actually exercises:
- [Meter Telemetry (UC1)](./use-cases/meter-telemetry/) — uses `confirm` + `on_status`
- [ARR Filings (UC2)](./use-cases/arr-filings.md) — uses `confirm` + `on_status`
- [Tariff Policies (UC3)](./use-cases/tariff-policies.md) — uses `confirm` + `on_status` (SERC publishes `IES_Policy` to DISCOM)

---

## 6. Stop the stack

```bash
cd DEG/devkits/data-exchange/install
docker compose down
```

---

## 7. Going beyond the sandbox

The sandbox identities (`bap.example.com` / `bpp.example.com`) and the placeholder network ID in the devkit payloads are local-only. To transact with real participants on the IES test network (`indiaenergystack.in/test-ies-data-sharing-network`) or the IES production network (`indiaenergystack.in/ies-data-sharing-network`):

1. Publish your own subscriber record on DeDi Global (your verified namespace + Ed25519 public key).
2. Ask the network owner to add your record to the network registry.
3. Update `config/local-simple-{bap,bpp}.yaml` so ONIX uses your real identity.

Full step-by-step on [Registry Setup](./registry-setup.md).

---

## Onboarding checklist

### BAP (Data Consumer)
- [ ] Devkit cloned, stack up (`docker compose up -d` in `install/`)
- [ ] BAP Postman collection imported, variables set
- [ ] `confirm` → `on_confirm` round-trip succeeds against `sandbox-bpp`
- [ ] Your application can consume the `dataPayload` body
- [ ] *(for real network)* Subscriber record published on DeDi; added to network registry; ONIX config updated → [Registry Setup](./registry-setup.md)

### BPP (Data Provider)
- [ ] Devkit cloned, stack up
- [ ] BPP Postman collection imported, variables set
- [ ] Your provider implementation handles inbound `confirm` and emits `on_confirm` (or `on_status` for async delivery) — start from the `sandbox-bpp` reference behaviour
- [ ] Example payloads in `uc*/examples/` align with your schema output
- [ ] *(for real network)* Subscriber record published on DeDi; added to network registry; ONIX config updated → [Registry Setup](./registry-setup.md)

---

## Reference

- [Architecture](./architecture.md) — stack topology, generic flow, context invariants
- [Devkit README](https://github.com/beckn/DEG/blob/main/devkits/README.md) — multi-network ONIX, hosting/TLS, ngrok
- [docs.nfh.global/beckn](https://docs.nfh.global/beckn) — network and registry primitives
- [Beckn protocol v2.0.0 spec](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0)
