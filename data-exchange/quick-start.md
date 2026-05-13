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

Onboarding is a two-phase progression. Don't skip phase 1.

### Phase 1 — Use the devkit as-is and prove the flows

Sections 1–6 above are the whole of phase 1. Run them with the shipped sandbox identities (`bap.example.com` / `bpp.example.com`), the placeholder `networkId` in the devkit payloads, and the sandbox signing keys committed in `config/`. The goal is to confirm:

- The Docker stack comes up cleanly and `beckn-router:9000` is reachable.
- `confirm` → `on_confirm` produces a callback you can see in `sandbox-bap` logs.
- Your application consumes the `dataPayload` shape you expect for whichever use case you care about.
- *(For BPPs)* your provider implementation emits the right `on_confirm` / `on_status` envelopes — start from the `sandbox-bpp` reference behaviour, swap your business logic in, keep the wire shape.

Iterate here until everything is green. Nothing in phase 1 touches DeDi or the IES networks.

### Phase 2 — Swap in your real identity

Only once phase 1 is solid, replace the sandbox identity with yours. Three knobs in [`devkits/data-exchange/config/local-simple-bap.yaml`](https://github.com/beckn/DEG/blob/main/devkits/data-exchange/config/local-simple-bap.yaml) and the matching `local-simple-bpp.yaml`:

| Knob | Sandbox value | Replace with |
|---|---|---|
| `allowedNetworkIDs` | placeholder | `indiaenergystack.in/test-ies-data-sharing-network` *(stay on test until certified — see [Registry Setup § Two registries, two ONIX deployments](./registry-setup.md#two-registries-two-onix-deployments))* |
| `networkParticipant` / `subscriberId` | `bap.example.com` / `bpp.example.com` | Your real `subscriberId` from the DeDi record you publish |
| `keyId` + Ed25519 private key | sandbox keys committed in `config/` | Your real `recordId` from DeDi and the matching Ed25519 private key |

The corresponding pre-work on DeDi (verify namespace → create subscriber registry → publish record with public key → ask IES to add your DeDi URL to the network reference registry) is the full subject of [Registry Setup](./registry-setup.md). The lookup URL you copied from DeDi is what you hand to IES; the `recordId` you noted is what you put in ONIX as `keyId`.

After the config swap, re-import the same Postman collection (or rerun the same Arazzo workflow) — the requests are identical, only the identity ONIX signs with and the network it claims has changed. A successful `confirm` against another participant on `indiaenergystack.in/test-ies-data-sharing-network` proves end-to-end onboarding.

Promote to `indiaenergystack.in/ies-data-sharing-network` only when testing is finished and IES has added your prod DeDi URL to the prod network's reference registry. The recommended pattern is **two separate ONIX deployments** with `allowedNetworkIDs` narrowed to one network each — see [Registry Setup](./registry-setup.md#two-registries-two-onix-deployments).

---

## Onboarding checklist

### BAP (Data Consumer)

Phase 1 — devkit as-is:
- [ ] Devkit cloned, stack up (`docker compose up -d` in `install/`)
- [ ] BAP Postman collection imported, variables set
- [ ] `confirm` → `on_confirm` round-trip succeeds against `sandbox-bpp`
- [ ] Your application can consume the `dataPayload` body

Phase 2 — real identity on `indiaenergystack.in/test-ies-data-sharing-network`:
- [ ] DeDi namespace verified; subscriber registry created
- [ ] Subscriber record published (public key, callback URL); `recordId` noted
- [ ] DeDi lookup URL handed to IES; reference entry added to the test network registry
- [ ] `config/local-simple-bap.yaml` updated: `allowedNetworkIDs`, `subscriberId`, `keyId`, private key
- [ ] Same flow passes against the test network → ready for IES to promote you to prod ([Registry Setup](./registry-setup.md))

### BPP (Data Provider)

Phase 1 — devkit as-is:
- [ ] Devkit cloned, stack up
- [ ] BPP Postman collection imported, variables set
- [ ] Your provider implementation handles inbound `confirm` and emits `on_confirm` (or `on_status` for async delivery) — start from the `sandbox-bpp` reference behaviour
- [ ] Example payloads in `uc*/examples/` align with your schema output

Phase 2 — real identity on `indiaenergystack.in/test-ies-data-sharing-network`:
- [ ] DeDi namespace verified; subscriber registry created
- [ ] Subscriber record published; `recordId` noted; DeDi lookup URL handed to IES
- [ ] `config/local-simple-bpp.yaml` updated: `allowedNetworkIDs`, `subscriberId`, `keyId`, private key
- [ ] End-to-end exchange completes with another participant on the test network → ready for prod ([Registry Setup](./registry-setup.md))

---

## Reference

- [Architecture](./architecture.md) — stack topology, generic flow, context invariants
- [Devkit README](https://github.com/beckn/DEG/blob/main/devkits/README.md) — multi-network ONIX, hosting/TLS, ngrok
- [docs.nfh.global/beckn](https://docs.nfh.global/beckn) — network and registry primitives
- [Beckn protocol v2.0.0 spec](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0)
