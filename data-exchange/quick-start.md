# Quick Start — Data Exchange

Run a working data exchange in under 10 minutes, then grow it in three phases — no real registry or production credentials needed for any of them:

| Phase | What you prove |
|---|---|
| **[A — Run it locally](#phase-a--run-it-locally)** | The full stack on your laptop, exchanging canned data |
| **[B — Go over the public internet](#phase-b--go-over-the-public-internet-ngrok)** | The same stack transacting through a real public tunnel (ngrok) |
| **[C — Make the sandbox your own](#phase-c--make-the-sandbox-your-own)** | The sandbox built from source and modified — or replaced by your own application |

Track overall onboarding with the [Onboarding Checklist](../checklists/data-exchange-checklist.md); joining a real IES network is [Registry Setup](./registry-setup.md).

---

## 1. Pick your role

| You are | You run | What you do |
|---|---|---|
| **BAP** — data consumer (DISCOM, regulator, VAS provider, researcher) | BAP-side adapter + your application | Send `confirm` (and optional discovery/negotiation), receive `on_confirm` / `on_status` callbacks |
| **BPP** — data provider (AMISP, DISCOM, SERC, data custodian) | BPP-side adapter + your provider implementation | Receive `confirm`, emit `on_confirm` (and `on_status` for async delivery) with the dataset |
| Both | Both stacks | Both flows in parallel |

The walkthrough uses the **BAP** path by default; BPP implementors, see the [BPP path](#bpp-path) in Phase A. The minimal flow — `confirm` → `on_confirm` — is all you need to start; the full action picker is in [Concepts § Beckn Protocol Lifecycle](./concepts.md#beckn-protocol-lifecycle).

---

## 2. Prerequisites

- Docker and Docker Compose, Git, Python 3, Postman *(or `curl`)*, ~2 GB free disk space

The devkit ships pre-configured sandbox identities (`bap.example.com` / `bpp.example.com`) — no real credentials needed.

**Domains to whitelist** — if your organisation restricts outbound traffic, allow these before starting:

| Purpose | Domain |
|---|---|
| Devkit and related repos (clone, raw schema fetches) | `https://github.com/beckn` |
| Discovery service (DS) — where ONIX routes `discover` | `https://34.93.165.42.sslip.io` |
| Catalog service (CS) + DeDi registry lookups — where ONIX routes `publish-catalog` and resolves participants | `https://fabric.nfh.global` |
| DeDi publishing — namespaces, registries, subscriber records | `https://publish.dedi.global` |
| Schema contexts — `@context` / `attributes.yaml` fetches | `https://schema.beckn.io`, `https://schema.nfh.global` |
| IES docs and hosted schemas | `https://india-energy-stack.gitbook.io/docs`, `https://india-energy-stack.github.io` |

---

## Phase A — Run it locally

### A1. Clone and start the stack

```bash
git clone https://github.com/beckn/DEG.git
cd DEG/devkits/data-exchange/install
docker compose up -d
```

Verify the services are up:

```bash
$ docker compose ps
# all 7 containers should show "running" (and the redis/sandbox ones "healthy")

$ curl -s http://localhost:8081/health   # onix-bap
{"status":"ok"}
$ curl -s http://localhost:8082/health   # onix-bpp
{"status":"ok"}
$ curl -s http://localhost:9000/         # beckn-router default route
beckn-router ok
```

> **If checks fail** — give ONIX ~15s after `docker compose up` to initialise, then re-curl. Persistent `connection refused` usually means a container isn't running; `docker compose logs onix-bap` / `onix-bpp` show why.

### A2. Run the minimal exchange (`confirm` → `on_confirm`)

One round-trip proves all the wiring: signing, routing, verification, callback delivery.

**Import the Postman collection** — each use case ships BAP and BPP collections; import the **BAP** one for your use case:

```
devkits/data-exchange/uc1-meter-data/postman/data-exchange-uc1-meter-data.{BAP,BPP}-DEG.postman_collection.json
devkits/data-exchange/uc2-regulatory-data/postman/data-exchange-uc2-regulatory-data.{BAP,BPP}-DEG.postman_collection.json
devkits/data-exchange/uc3-tariff-policy/postman/data-exchange-uc3-tariff-policy.{BAP,BPP}-DEG.postman_collection.json
```

**Check the collection variables** — the defaults are correct for local runs; don't change them:

| Variable | Default | What it is |
|---|---|---|
| `beckn_adapter_url` | `http://localhost:8081/bap/caller` | The HTTP target Postman POSTs to |
| `bap_host_root` / `bpp_host_root` | `http://beckn-router:9000` | Substituted into each payload's `context.bapUri`/`bppUri`; resolved by ONIX *inside* docker (change only in Phase B) |

The layering behind these two kinds of URL is explained in [Appendix § Hostnames and endpoints](./appendix.md#hostnames-and-endpoints--sandbox-vs-production).

**Send and verify:**

1. Open the `confirm` request, click **Send**. The synchronous response is the ACK envelope: `{"message":{"ack":{"status":"ACK"}}}` — "accepted, async callback pending." The ACK originates at the provider's webhook and cascades back through the adapters to Postman.
2. Tail the BAP sandbox logs to see the matching callback land:
   ```bash
   docker logs sandbox-bap 2>&1 | grep on_confirm | tail -5
   ```
3. The `on_confirm` body either carries the dataset (`INLINE`) or a handle pointing to a later `on_status`. Either way, seeing `on_confirm` in `sandbox-bap` is your end-to-end signal.

> **If you don't see `on_confirm`** — most common causes: (a) `bap_host_root`/`bpp_host_root` changed away from `http://beckn-router:9000`, (b) ONIX rejected the message on schema/signature — check `docker logs onix-bap | grep -i error` and `onix-bpp`, or (c) host alias DNS missing on `beckn-router` (only if you regenerated `install/docker-compose.yml` — see beckn/DEG#319).

#### BPP path

Same sanity check in reverse: import the **BPP** collection, trigger `on_confirm` from it (or wait for an inbound `confirm`), and tail:

```bash
docker logs sandbox-bpp 2>&1 | grep -E 'confirm|status' | tail -5
```

Then make the provider your own — see [Phase C](#phase-c--make-the-sandbox-your-own).

### A3. (Optional) Add other Beckn actions

Each action ships in the BAP or BPP collection — fire it only when your use case needs it:

| Action | Sent by | Use it when |
|---|---|---|
| `publish-catalog` | BPP collection | You're a provider listing datasets so consumers can discover you |
| `discover` | BAP collection | The consumer doesn't yet know which BPP holds the dataset |
| `select` / `init` | BAP collection | Terms (price, SLA, delivery mode) need agreeing before commitment |
| `status` | BAP collection | The payload is prepared *after* `on_confirm`; the BAP polls for it (all three use cases use this) |
| `update` | BAP collection | Post-fulfilment changes — credential rotation in streaming |

Each [use-case page](../use-cases/README.md) lists exactly which steps it exercises and where the example payloads live.

---

## Phase B — Go over the public internet (ngrok)

Once Phase A is green, prove the same stack interoperates over a real public tunnel — with another participant's laptop or a cloud host — without DeDi identity yet:

1. Create a free [ngrok](https://ngrok.com) account; copy the devkit's tunnel config and add your authtoken:
   ```bash
   cd DEG/devkits/data-exchange/install
   cp ngrok.yml.example ngrok.yml   # edit: paste your authtoken
   ngrok start --all --config ngrok.yml
   ```
2. In the Postman collection, set `bap_host_root` / `bpp_host_root` to the HTTPS URL ngrok prints (e.g. `https://abc123.ngrok-free.dev`) — the docker-only dummy hostnames aren't reachable from outside, so the payload URIs must carry your public tunnel URL instead. Leave `beckn_adapter_url` alone — Postman still POSTs to your local ONIX.
3. Fire `confirm` again; watch the hops in the ngrok inspector at [http://localhost:4040](http://localhost:4040).

For two-party interop, each side runs its own tunnel and you point `bpp_host_root` at the *other side's* URL. Details and the full recipe: [devkit README — Over-the-internet notes](https://github.com/beckn/DEG/blob/main/devkits/README.md#over-the-internet-notes). Revert the host variables to `http://beckn-router:9000` to return to local-only mode.

---

## Phase C — Make the sandbox your own

The bundled sandboxes are instances of **[beckn/sandbox](https://github.com/beckn/sandbox)**, wired to ONIX through the webhook URLs in the routing configs. Building it from source gives you a working app you can freely modify — the gentlest path from canned data to your own logic.

1. **Build it locally:**
   ```bash
   git clone https://github.com/beckn/sandbox.git
   cd sandbox
   docker build -t sandbox-2.0:local .
   ```
2. **Swap the container:** in `DEG/devkits/data-exchange/install/docker-compose.yml`, change the `sandbox-bpp` (or `sandbox-bap`) service's image from `fidedocker/sandbox-2.0:latest` to `sandbox-2.0:local`, keeping its volumes and environment, then:
   ```bash
   docker compose up -d sandbox-bpp
   ```
3. **Verify nothing broke:** re-run [Phase A § A2](#a2-run-the-minimal-exchange-confirm--on_confirm).
4. **Modify what you please:** change the canned responses (the JSON fixtures the devkit mounts over `dist/webhook/jsons/…`), add handler logic in `src/`, rebuild, re-swap. Your changes now answer real Beckn traffic.

### Replacing the sandbox with your own application

When you outgrow the sandbox, your app connects to ONIX in exactly two places — `bapUri`/`bppUri` are *not* one of them (those always point at ONIX receivers, never at your app):

- **Inbound** — after verifying a message, ONIX forwards it to the **webhook URL set in the routing config** ([`config/local-simple-routing-BAPReceiver.yaml`](https://github.com/beckn/DEG/blob/main/devkits/data-exchange/config/local-simple-routing-BAPReceiver.yaml) / `…-BPPReceiver.yaml`). Take over that URL and you've replaced the sandbox.
- **Outbound** — your app POSTs messages to ONIX's `caller` endpoint.

**BAP:** stand up a service with a webhook endpoint for the `on_*` callbacks your flow needs, reachable from `onix-bap` (on the `bap_side` docker network, or a routable host). Change `target.url` in `local-simple-routing-BAPReceiver.yaml` from `http://sandbox-bap:3001/api/bap-webhook` to your service, restart `onix-bap`, then stop `sandbox-bap`.

**BPP:** your provider receives requests (`confirm`, `status`, …) on the webhook set in `local-simple-routing-BPPReceiver.yaml` (devkit default: `http://sandbox-bpp:3002/api/webhook`). Acknowledge each with the ACK envelope, then respond asynchronously by POSTing the matching callback to `http://onix-bpp:8082/bpp/caller/on_<action>` — copy the wire shape from `uc*/examples/on-*-response*.json` and swap in your real data.

---

## Stop the stack

```bash
cd DEG/devkits/data-exchange/install && docker compose down
```

---

## Swap in your real identity

Phases A–C all ran on the shipped sandbox identities. To join a real IES network, replace them with yours in [`config/local-simple-bap.yaml`](https://github.com/beckn/DEG/blob/main/devkits/data-exchange/config/local-simple-bap.yaml) (and the matching `local-simple-bpp.yaml`):

```yaml
modules:
  - name: bapTxnReceiver
    handler:
      plugins:
        registry:
          config:
            allowedNetworkIDs: "indiaenergystack.in/test-ies-data-sharing-network"   # comma-separated string
        keyManager:
          config:
            networkParticipant: your.subscriber.id        # your DeDi subscriberId
            keyId: <recordId-from-DeDi>                   # the recordId DeDi gave you
            signingPrivateKey: <base64-ed25519-private>   # the half you keep
            signingPublicKey:  <base64-ed25519-public>    # the half you published in DeDi
```

Where these values come from — DeDi namespace, subscriber record, IES NFO handoff, and the full field mapping — is the subject of [Registry Setup](./registry-setup.md). Stay on the **test network** until certified; the recommended prod pattern is [two separate ONIX deployments](./registry-setup.md#two-registries-two-onix-deployments).

After the config swap, re-import the same Postman collection — only the identity ONIX signs with and the network it claims change. Use the same network ID in every payload's `context.networkId`: ONIX rejects messages whose `networkId` isn't in its `allowedNetworkIDs` ([Registry Setup § the gate](./registry-setup.md#allowednetworkids-is-the-gate)). A successful `confirm` against another participant on `indiaenergystack.in/test-ies-data-sharing-network` proves end-to-end onboarding.

---

## Reference

- [Onboarding Checklist](../checklists/data-exchange-checklist.md) — staged checklist from devkit to production
- [Core Concepts](./concepts.md) · [Appendix](./appendix.md)
- [beckn/sandbox](https://github.com/beckn/sandbox) — the sandbox source
- [Devkit README](https://github.com/beckn/DEG/blob/main/devkits/README.md) — multi-network ONIX, hosting/TLS, ngrok
- [Beckn protocol v2.0.0 spec](https://github.com/beckn/protocol-specifications-v2/tree/main/api/v2.0.0)
